"""Physical Sciences P1 (Physics) Nov 2024, the whole paper (Questions 1 to 10), hand-transcribed into the catalogue format (as if
Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the
memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the
transcription is the source, kept in git (out/ is not). Read from the page IMAGES too: the paper sets formulas and symbols as
images, so its text layer has gaps. Polished one subject at a time (Murci, 2026-10-10: "next subject: Physical Sciences").

  python tools/ingest/transcribe_ps_p1_2024_11.py
  python tools/ingest/ingest.py "<...>/Physical Sciences P1 Nov 2024 Eng.pdf" "<...>/Physical Sciences P1 Nov 2024 MG Afr & Eng.pdf" --id ps-p1-2024-11 --from-json

How the memo's shapes map (as Physical Sciences P1 Nov 2025, with what its polish taught, 2026-10-10):
  multiple choice -> mcq (options printed as a table -> optTable); a definition/law -> rubric, ONE point worth 2 (each=2), its
  "key words" marking note in `notes` (a note in bullets is a point a learner earns); "Calculate" -> steps, each step ONE number
  the memo's method produces, its formula and substitution marks riding on it; a memo RANGE -> its centre with a tolerance
  covering it; "Choose ... Explain" in words -> rubric, the choice its own point; "decide by calculation" (8.3) -> steps, the
  conclusion riding on the decisive number (as a rubric of working, a right answer scored 0); "Draw / Sketch" -> draw with the
  memo's criteria (self-checked). A question whose diagram changes part-way is several missions (7, 9, 10).
Figure boxes are measured in PDF points (page 595.44 x 841.68) from the drawings themselves (scratchpad figs24.py) and checked on a
contact sheet (sheet24.py)."""
import json
from pathlib import Path

W, H = 595.44, 841.68
FIGS = {  # [page, x0, y0, x1, y1] in points
    "1.2": [3, 120, 425, 400, 575], "1.3": [4, 225, 170, 375, 280], "1.4": [4, 200, 490, 380, 585], "1.5": [5, 250, 135, 440, 232],
    "1.7": [6, 235, 145, 405, 282], "1.9": [7, 125, 135, 528, 320], "Q2": [8, 115, 222, 495, 563], "Q3": [9, 180, 220, 410, 388],
    "Q4": [10, 50, 238, 555, 393], "Q5": [11, 205, 198, 460, 306], "Q6": [12, 140, 225, 425, 375], "Q7a": [13, 190, 168, 418, 216],
    "Q7b": [13, 172, 312, 362, 372], "Q7c": [13, 185, 483, 432, 546], "Q8": [14, 100, 214, 478, 488], "Q9a": [15, 70, 142, 562, 292],
    "Q9b": [15, 100, 528, 570, 678], "Q10b": [16, 180, 252, 432, 378]}


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


# notes: the memo's marking notes that are NOT points (key words, "... 0/2", ACCEPT limits): never scored, never shown
rub = lambda n, q, marks, bullets, clues, each=None, notes=None: {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets,
                                                                 **({"each": each} if each else {}), **({"notes": notes} if notes else {})}
term = lambda n, q, a, clues, marks=1: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a}
num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}
KEYWORDS = "If any of the underlined key words/phrases in the correct context is omitted, deduct 1 mark."


def steps(n, q, marks, sts, clues):
    """sts: (label, marks, answer, tolerance, the memo's working)."""
    s = [{"id": "s%d" % (i + 1), "label": lab, "marks": m, "a": a, "tol": tol, "memo": memo} for i, (lab, m, a, tol, memo) in enumerate(sts)]
    assert sum(x["marks"] for x in s) == marks, n
    return {"t": "steps", "n": n, "marks": marks, "q": q, "clues": clues, "steps": s}


# ---- QUESTION 1: multiple choice, the question paper pages 3-7 and the memo page 2 ----
q1 = [
    mcq("1.1", "Several forces are acting on a moving object. Which ONE of the following statements is CORRECT when these forces are in equilibrium?",
        ["The velocity of the object is increasing.", "The object is moving at a constant velocity.", "The kinetic energy of the object is decreasing.",
         "The object has a non-zero acceleration."], 1,
        ["In equilibrium the net force is zero.", "Zero net force means zero acceleration: what does the velocity do?"]),
    mcq("1.2", "A stone thrown vertically downwards from the top of a building takes t seconds to strike the ground. Consider the acceleration-time graph "
        "below for the motion of the stone. The effects of air friction are ignored. What does the shaded area between 0 and t seconds, shown in the "
        "graph, represent?",
        ["The final velocity of the stone", "The change in position of the stone", "The constant velocity of the stone", "The change in velocity of the stone"], 3,
        ["Area under a graph = the quantity on the y-axis times the quantity on the x-axis.", "Acceleration x time is ...?"],
        figure=fig("1.2", "An acceleration-time graph: acceleration (m·s⁻²) up, time (s) across. A horizontal line at 9,8 runs from 0 to t, and the "
                          "rectangle under it, from 0 to t, is shaded.")),
    mcq("1.3", "A ball moving horizontally has constant momentum p and kinetic energy K. The ball collides with a wall and bounces back horizontally. "
        "Immediately after the collision, the ball has momentum ½p. The mass of the ball remains constant. Which ONE of the following is the kinetic "
        "energy of the ball immediately after the collision?", ["¼K", "½K", "2K", "4K"], 0,
        ["Same mass, half the momentum: what happens to the speed?", "K = ½mv²: halve v and K changes by the square of that factor."],
        figure=fig("1.3", "A ball moving right towards a vertical wall with momentum p; below it, the ball moving left away from the wall with momentum ½p.")),
    mcq("1.4", "A force F acts on a box as the box moves from rest down a rough incline at a constant acceleration. The force is parallel to the incline, as "
        "shown in the diagram below. Choose the option that CORRECTLY completes the following statement. The work done by the gravitational force is … "
        "the work done by the frictional force and the work done by F.",
        ["equal to the sum of", "less than the sum of", "greater than the sum of", "equal to the difference between"], 2,
        ["The box speeds up, so the net work done on it is positive.", "F and friction both act up the slope, against the motion."],
        figure=fig("1.4", "A box on a slope that goes down to the right, an arrow beside it pointing down the slope (its motion); force F acts on the "
                          "box up the slope, parallel to it.")),
    mcq("1.5", "A ball falling vertically downwards from point A strikes the ground with velocity v and bounces, reaching a maximum height at point B, as "
        "shown in the diagram below. Which ONE of the combinations below is CORRECT for the direction of the impulse on the ball upon striking the "
        "ground and the magnitude of the velocity with which the ball leaves the ground?",
        ["Impulse upward · leaves greater than v", "Impulse downward · leaves greater than v", "Impulse upward · leaves less than v",
         "Impulse downward · leaves less than v"], 2,
        ["The impulse is in the direction of the change in momentum.", "B is lower than A: did the ball leave faster or slower than it arrived?"],
        figure=fig("1.5", "A ball at A falls straight down to the ground (arrow down), and a ball bounces back up to B, which is lower than A (arrow up)."),
        optTable={"head": ["DIRECTION OF THE IMPULSE ON THE BALL", "MAGNITUDE OF THE VELOCITY WITH WHICH THE BALL LEAVES THE GROUND"],
                  "rows": [["Upward", "Greater than v"], ["Downward", "Greater than v"], ["Upward", "Less than v"], ["Downward", "Less than v"]]}),
    mcq("1.6", "The absorption spectrum of an element surrounding a moving star is observed on Earth and found to be red shifted. Which ONE of the "
        "following combinations is CORRECT for the movement of the star and the frequency of the observed light on Earth?",
        ["Away from Earth · decreased", "Towards Earth · decreased", "Away from Earth · increased", "Towards Earth · increased"], 0,
        ["Red light has a longer wavelength than blue.", "A longer observed wavelength means a lower observed frequency: is the source moving away or closer?"],
        optTable={"head": ["MOVEMENT OF STAR", "FREQUENCY OF OBSERVED LIGHT ON EARTH"],
                  "rows": [["Away from Earth", "Decreased"], ["Towards Earth", "Decreased"], ["Away from Earth", "Increased"], ["Towards Earth", "Increased"]]}),
    mcq("1.7", "Two small identical spheres, each with mass m and charge +Q, are placed in a vertical cylinder. The spheres remain stationary when their "
        "centres are r metres apart, as shown in the diagram below. Ignore ALL frictional effects. Which ONE of the following expressions can be used "
        "to CORRECTLY calculate the distance r?", ["√(kQ²/mg)", "√(kmg/Q²)", "√(Q²/kmg)", "√(mg/kQ²)"], 0,
        ["The top sphere is in equilibrium: the electrostatic force up equals its weight down.", "Set kQ²/r² = mg and solve for r."],
        figure=fig("1.7", "A vertical cylinder; one sphere of mass m and charge +Q rests at the bottom and an identical one floats above it, their "
                          "centres r apart.")),
    mcq("1.8", "The kilowatt-hour (kWh) is a unit of …", ["power.", "electric current.", "electrical energy.", "potential difference."], 2,
        ["A kilowatt is a unit of power; an hour is a time.", "Power x time is ...?"]),
    mcq("1.9", "The diagram below shows a simplified electric motor. The rotation of the coil is observed from the battery. Which ONE of the following "
        "statements is CORRECT while the motor is in operation? The coil and the …",
        ["slip rings rotate anti-clockwise.", "slip rings rotate clockwise.", "commutator rotate clockwise.", "commutator rotate anti-clockwise."], 3,
        ["A DC motor uses a split-ring commutator; slip rings belong to AC devices.", "Use the left-hand (motor) rule on each side of the coil to find the turning direction."],
        figure=fig("1.9", "A rectangular coil between the N pole (left) and S pole (right) of a magnet; its ends join a split ring with brushes, wired "
                          "to a battery below.")),
    mcq("1.10", "Which of the following statements is/are TRUE for the photoelectric effect? The photoelectric effect demonstrates that: (i) Light has a "
        "wave nature; (ii) Light has a particle nature; (iii) Light energy is quantised",
        ["(i) only", "(ii) only", "(i) and (iii) only", "(ii) and (iii) only"], 3,
        ["Einstein explained it with photons.", "Photons are packets (quanta) of energy: which statements match that?"]),
]

# ---- QUESTION 2, the question paper page 8 and the memo pages 3-4 ----
q2 = [
    rub("2.1", "Define the term static friction.", 2,
        ["The force that opposes the tendency of motion of a stationary object relative/parallel to a surface. (2)"],
        ["The object is not moving yet.", "Which force acts against the TENDENCY to move?"], each=2, notes=[KEYWORDS]),
    draw("2.2", "Draw a labelled free-body diagram showing ALL the HORIZONTAL forces acting on the crate JUST BEFORE it starts moving.", 2,
         [["T: tension / FT / Fstring, to the right (towards the pulley)", 1], ["fs: static friction / f / Ff, to the left", 1]],
         ["Only the horizontal forces.", "The string pulls one way; friction opposes."],
         memo="Mark for label and arrow. Vertical forces (w, N) shown: no penalty. Arrows not touching the dot, any other force, or no arrows: max 1/2."),
    steps("2.3.1", "Calculate the coefficient of static friction (µs).", 4,
          [("Tension in the string as the crate starts to move (N)", 1, 41.16, 0.05, "For the hanging mass: T = mg = 4,2(9,8) = 41,16 N ✓"),
           ("Coefficient of static friction µs", 3, 0.49, 0.005, "fs(max) = µsN ✓ (any one); µs(8,5)(9,8) ✓ = 41,16; µs = 0,49 ✓")],
          ["The crate just starts to move when the hanging mass is 4,2 kg (read the graph).", "Then T = weight of the hanging mass = fs(max) = µs N."]),
    steps("2.3.2", "Calculate the magnitude of the acceleration represented by Y on the graph if the coefficient of kinetic friction between the crate "
          "and the table is 0,40.", 5,
          [("Kinetic friction on the crate (N)", 1, 33.32, 0.05, "fk = µkN = 0,4(8,5)(9,8) ✓ = 33,32 N"),
           ("Acceleration Y (m·s⁻²)", 4, 2.47, 0.01, "Fnet = ma ✓ (any one); crate: T − 0,4(8,5)(9,8) = 8,5a ✓; hanging mass: 7,4(9,8) − T = 7,4a ✓; "
            "a = 2,47 m·s⁻² ✓ (T = 54,32 N may be found first)")],
          ["Y is read where the hanging mass is 7,4 kg.", "Write Fnet = ma for the crate and for the hanging mass, then add the equations."]),
    rub("2.4", "A 5 kg block is now placed inside the crate and the experiment is repeated. How will this affect the maximum static frictional force now "
        "experienced by the crate? Choose from INCREASES, DECREASES or REMAINS THE SAME. Give a reason for the answer.", 2,
        ["Increases (1)", "fs(max) = µsN: the normal force on the crate increases / the mass (weight) of the crate increases. (1)"],
        ["What does the extra mass do to the normal force?", "fs(max) = µs N."]),
]

# ---- QUESTION 3, the question paper page 9 and the memo pages 5-10 ----
q3 = [
    steps("3.1.1", "Using EQUATIONS OF MOTION ONLY, calculate the value of t, as shown in the graphs.", 5,
          [("t (s)", 5, 4, 0.01, "Δy = viΔt + ½aΔt² ✓; ball A: 12t + ½(−9,8)t² ✓; ball B: −5,4(t − 2) + ½(−9,8)(t − 2)² ✓; ΔyA = ΔyB ✓; "
            "t = 4 s ✓ (upwards positive; downwards positive and other options alike)")],
          ["Both balls end at the ground, the same displacement from the top.", "Ball B leaves 2 s later: its time in the air is t − 2."]),
    steps("3.1.2", "Using EQUATIONS OF MOTION ONLY, calculate the value of Z, as shown in the graphs.", 3,
          [("Z (m)", 3, 30.4, 0.05, "Δy = viΔt + ½aΔt² ✓; (12)(4) + ½(−9,8)(4)² ✓ = −30,4 m; Z = 30,4 m ✓ (positive marking from 3.1.1)")],
          ["Z is the height of the building: ball A's displacement from the top to the ground.", "Use t from 3.1.1."]),
    steps("3.1.3", "Using EQUATIONS OF MOTION ONLY, calculate the value of Y, as shown in the graphs.", 4,
          [("Height ball A rises above the top of the building (m)", 2, 7.335, 0.02, "vf² = vi² + 2aΔy ✓: 0 = (12)² + 2(−9,8)Δy ✓; Δy = 7,35 m"),
           ("Y (m)", 2, 37.735, 0.02, "Y = 7,35 + 30,4 ✓ = 37,75 m ✓ (range 37,72 – 37,75 m)")],
          ["Y is ball A's highest point above the ground.", "At the top vf = 0; add the building's height Z."]),
    draw("3.2", "On the same set of axes, sketch the velocity-time graphs for ball A and ball B while they are in free fall. Label the graphs A and B for "
         "ball A and ball B respectively. Clearly indicate the following on the graphs: the initial velocity of each ball; the time at which each ball "
         "is thrown; the time at which the balls strike the ground.", 4,
         [["Correct initial velocities of balls A and B (12 and −5,4 m·s⁻¹, upwards positive) with straight lines of the same sign of slope", 1],
          ["Correct initial times: A at 0 s, B at 2 s (B starts after A crosses the time axis)", 1], ["Both graphs end at 4 s (accept t)", 1],
          ["The graphs are parallel, B to the right of A", 1]],
         ["Free fall: both lines have the same gradient (−9,8 m·s⁻²).", "Ball B starts at 2 s with −5,4 m·s⁻¹ (upwards positive)."],
         memo="No labels A and B: deduct 1 mark."),
]

# ---- QUESTION 4, the question paper page 10 and the memo pages 11-12 ----
q4 = [
    rub("4.1", "Write down the principle of conservation of mechanical energy in words.", 2,
        ["The total mechanical energy / sum of gravitational potential energy and kinetic energy in an isolated system remains constant / is conserved. (2)"],
        ["Mechanical energy = potential + kinetic.", "In which kind of system does it stay the same?"], each=2, notes=[KEYWORDS]),
    steps("4.2", "Calculate the speed of trolley B at the bottom of the inclined plane.", 4,
          [("Speed of trolley B at the bottom of the incline (m·s⁻¹)", 4, 5.42, 0.01,
            "Emech(top) = Emech(bottom) ✓; (2)(9,8)(1,5) + 0 ✓ = 0 + ½(2)v² ✓; v = 5,42 m·s⁻¹ ✓ (or Wnc = ΔEk + ΔEp, Wnet = ΔEk, ΔEk = −ΔEp)")],
          ["The incline is frictionless: mechanical energy is conserved.", "All its kinetic energy at the bottom becomes potential energy at 1,5 m."]),
    steps("4.3.1", "For the t seconds that the spring takes to return to its natural length, calculate the change in momentum of trolley B.", 3,
          [("Change in momentum of trolley B (kg·m·s⁻¹)", 3, 10.84, 0.05, "Δp = mvf − mvi ✓ (any one); 2(5,42 − 0) ✓ = 10,84 kg·m·s⁻¹ to the right ✓")],
          ["B starts from rest and leaves with the speed from 4.2.", "Δp = m(vf − vi)."]),
    num("4.3.2", "For the t seconds that the spring takes to return to its natural length, write down the change in momentum of trolley A "
        "(its magnitude; it is opposite in direction to B's).", 10.84, 0.05, "kg·m·s⁻¹",
        ["The spring pushes both trolleys with equal and opposite forces for the same time.", "Equal and opposite impulses: equal and opposite changes in momentum."]),
    steps("4.4", "Calculate the speed of trolley A after t seconds.", 2,
          [("Speed of trolley A (m·s⁻¹)", 2, 7.23, 0.01, "ΔpA = mvf − mvi: −10,84 = 1,5(vf − 0) ✓; vf = −7,23 m·s⁻¹, speed 7,23 m·s⁻¹ ✓ "
            "(OR Σpi = Σpf: 0 = 1,5vf + (2)(5,42))")],
          ["Use A's change in momentum from 4.3.2.", "A has mass 1,5 kg and starts from rest."]),
]

# ---- QUESTION 5, the question paper page 11 and the memo pages 13-14 ----
q5 = [
    rub("5.1", "Define the term work done by a force.", 2,
        ["The work done on an object by a constant force F is FΔx cos θ, where F is the magnitude of the force, Δx the magnitude of the displacement and "
         "θ the angle between the force and the displacement. (2)",
         "OR — The work done on an object is the product of the force and the displacement of the object in the direction of the displacement. (2)"],
        ["It involves a force and a displacement.", "W = FΔx cos θ: say it in words."], each=2, notes=[KEYWORDS]),
    draw("5.2", "Draw a labelled free-body diagram showing ALL the forces acting on the crate as it moves.", 4,
         [["w: weight / Fg / mg / 58,8 N / gravitational force, downwards", 1], ["N: normal force / FN, upwards", 1],
          ["f: friction / Ff / fk, to the left (against the motion)", 1], ["F: applied force / FA, at 30° above the horizontal", 1]],
         ["Four forces act.", "Draw F at its angle; do not split it into components."],
         memo="Mark for label and arrow. Any other force, no arrows, forces not touching the dot, or F drawn as components: max 3/4."),
    steps("5.3", "Using ENERGY PRINCIPLES ONLY, calculate the magnitude of force F.", 4,
          [("Change in kinetic energy of the crate from A to B (J)", 1, 12, 0.05, "ΔEk = ½(6)(2² − 0²) ✓ = 12 J"),
           ("Magnitude of F (N)", 3, 20.78, 0.015, "Wnet = ΔEk / Wnc = ΔEk + ΔEp ✓ (any one); F(1,5)cos 30° + 10(1,5)cos 180° ✓ = 12; "
            "F = 20,78 N ✓ (range 20,769 – 20,79 N)")],
          ["Only F and friction do work along the horizontal.", "Work by F = F(1,5)cos 30°; work by friction = 10(1,5)cos 180°."]),
    mcq("5.4", "A 2 kg object is placed in the crate. What effect will this have on the work done by the same force F when the crate is again moved from "
        "point A to point B? Write only INCREASES, DECREASES or REMAINS THE SAME.", ["Increases", "Decreases", "Remains the same"], 2,
        ["W = FΔx cos θ.", "Do F, Δx or θ change?"]),
]

# ---- QUESTION 6, the question paper page 12 and the memo page 15 ----
q6 = [
    term("6.1", "Name the phenomenon that explains why the wavelengths shown in the graph differ.", ["Doppler effect", "Doppler"],
         ["A moving source changes the wavelength a listener detects.", "It is named after an Austrian physicist."]),
    rub("6.2", "Is the car moving TOWARDS or AWAY FROM the listener? Give a reason for the answer.", 2,
        ["Away (from the listener) (1)",
         "The wavelength detected by the listener is longer than the wavelength emitted by the source / λL > λS OR the frequency detected is lower than "
         "the frequency of the source / fL < fs. (1)"],
        ["Compare λL with λS on the graph.", "A source moving away stretches the waves."]),
    steps("6.3.1", "Calculate the frequency of the sound emitted by the siren.", 3,
          [("Frequency of the siren (Hz)", 3, 902.63, 0.05, "v = fλ ✓; 343 = f(0,38) ✓; f = 902,63 Hz ✓ (c = fλ: −1; 340 used: −1 for the answer)")],
          ["The siren's own wavelength is λS.", "v = fλ with v = 343 m·s⁻¹."]),
    steps("6.3.2", "Calculate the magnitude of the velocity of the car.", 6,
          [("Frequency detected by the listener (Hz)", 2, 857.5, 0.05, "v = fλ: 343 = f(0,40) ✓; fL = 857,5 Hz ✓"),
           ("Speed of the car (m·s⁻¹)", 4, 18.25, 0.2, "fL = v/(v + vs) fs ✓; 857,5 = 343/(343 + vs) (902,63) ✓✓; vs = 18,05 m·s⁻¹ ✓ "
            "(range 18,05 – 18,45 m·s⁻¹)")],
          ["Work out the frequency the listener hears from λL first.", "The car moves away: fL = v/(v + vs) fs."]),
]

# ---- QUESTION 7, the question paper page 13 and the memo pages 16-17 ----
q7a = [
    steps("7.1", "Calculate the magnitude of the electric field at X.", 3,
          [("Electric field at X (N·C⁻¹)", 3, 5000, 1, "E = kQ/r² ✓; (9 x 10⁹)(2 x 10⁻⁹)/(0,06)² ✓; E = 5 x 10³ N·C⁻¹ ✓")],
          ["The field of a point charge: E = kQ/r².", "Convert to SI: 2 nC = 2 x 10⁻⁹ C and 6 cm = 0,06 m."]),
]
q7b = [
    draw("7.2", "Draw the resultant electric field pattern due to charges P and S.", 3,
         [["Correct direction of the field lines (from P to S)", 1], ["Correct shape between the charges and outside them", 1],
          ["No field lines crossing; lines touch the charges but do not go inside", 1]],
         ["P is positive and S is negative: unlike charges.", "Lines leave the positive charge and end on the negative one."],
         memo="The field of two like charges: 0/3. Only one charge drawn: 0/3."),
]
q7c = [
    rub("7.3.1", "State Coulomb's law in words.", 2,
        ["The magnitude of the electrostatic force exerted by one point charge on another point charge is directly proportional to the product of the "
         "magnitudes of their charges and inversely proportional to the square of the distance between them. (2)"],
        ["It is about the force between two point charges.", "Directly proportional to one thing, inversely to the square of another."], each=2,
        notes=[KEYWORDS, "If reference to masses / if the word FORCE in context is omitted: 0/2."]),
    mcq("7.3.2", "What is the polarity of charge T? Choose from POSITIVE or NEGATIVE.", ["Positive", "Negative"], 0,
        ["S (−2 nC) is much closer to T than P (+2 nC) is.", "The net force on T is to the LEFT, towards S: does S attract or repel T?"], marks=1),
    steps("7.3.3", "Calculate the magnitude of charge T.", 5,
          [("Magnitude of charge T (C)", 5, 6.25e-9, 0.01e-9,
            "F = kQ1Q2/r² ✓; FST = (9 x 10⁹)(2 x 10⁻⁹)QT/(0,02)² and FPT = (9 x 10⁹)(2 x 10⁻⁹)QT/(0,06)² ✓; Fnet = FST − FPT ✓ ✓: "
            "2,5 x 10⁻⁴ = …; QT = 6,25 x 10⁻⁹ C ✓ (OR ES = 45 000 N·C⁻¹, Enet = 4 x 10⁴ N·C⁻¹, F = Eq)")],
          ["T is 2 cm from S and 6 cm from P.", "Net force = force from S − force from P = 2,5 x 10⁻⁴ N: solve for QT."]),
]

# ---- QUESTION 8, the question paper page 14 and the memo pages 18-19 ----
q8 = [
    rub("8.1", "Define the term power.", 2,
        # the memo's phrase-level slashes as OR wordings: "The rate at which work is done" alone scored 0 (its words are all short)
        ["The rate at which work is done OR the rate at which energy is transferred/dissipated OR work done per unit time. (2 or 0)"],
        ["Power links work (or energy) and time.", "How fast work is done."], each=2),
    steps("8.2.1", "If both light bulbs operate as RATED, calculate the reading on ammeter A2.", 3,
          [("Reading on ammeter A2 (A)", 3, 1.5, 0.01, "P = VI ✓; 48 = 32I ✓; I = 1,5 A ✓ (OR R = V²/P = 21,33 Ω, then I = V/R)")],
          ["A2 is in series with L2 (48 W ; 32 V).", "P = VI."]),
    steps("8.2.2", "If both light bulbs operate as RATED, calculate the reading on ammeter A1.", 3,
          [("Current through L1 (A)", 2, 1.8, 0.01, "For L1: P = VI: 36 = 20I ✓; I = 1,8 A ✓"),
           ("Reading on ammeter A1 (A)", 1, 3.3, 0.01, "ITOT = 1,5 + 1,8 = 3,3 A ✓")],
          ["A1 carries the current of both parallel branches.", "Find L1's current from its rating, then add L2's."]),
    steps("8.2.3", "If both light bulbs operate as RATED, calculate the resistance of resistor R1.", 4,
          [("Potential difference across R1 (V)", 2, 12, 0.05, "VR1 + VL1 = V∥: VR1 + 20 = 32 ✓; VR1 = 12 V ✓"),
           ("Resistance of R1 (Ω)", 2, 6.67, 0.01, "V = IR: 12 = 1,8R1 ✓; R1 = 6,67 Ω ✓")],
          ["R1 and L1 are in series, and together in parallel with L2 (32 V).", "The branch current is L1's 1,8 A."]),
    steps("8.2.4", "If both light bulbs operate as RATED, calculate the emf of the battery.", 4,
          [("Potential difference across R2 (V)", 1, 13.2, 0.05, "V2 = ITOT R2 = 3,3(4) ✓ = 13,2 V"),
           ("Emf of the battery (V)", 3, 47.175, 0.02, "ε = Vext + Ir ✓; (13,2 + 32) ✓ + 3,3(0,6) ✓; ε = 47,18 V (range 47,16 – 47,19 V)")],
          ["The external circuit: R2 in series with the parallel part (32 V).", "ε = V(external) + Ir, with r = 0,6 Ω."]),
    # decide by calculation (as P1 Nov 2025 5.4 and 7.4): the conclusion "No" (1) rides on the decisive current, more than L2's rated 1,5 A
    steps("8.3", "Bulb L1 burns out after a while. Assume that the resistance of bulb L2 remains constant. Will bulb L2 continue to glow after bulb L1 "
          "burns out? Choose from YES or NO. Support your answer with a suitable calculation.", 5,
          [("Resistance of bulb L2 (Ω)", 1, 21.33, 0.01, "P = V²/R: 48 = 32²/R ✓; RL2 = 21,33 Ω (if already calculated, award the mark)"),
           ("Current through L2 after L1 burns out (A)", 4, 1.82, 0.01,
            "ε = I(R + r) ✓; 47,18 = I(21,33 + 4 + 0,6) ✓; I = 1,82 A ✓: more than L2's rated 1,5 A, so NO ✓ (accept: does not glow)")],
          ["With L1 gone, only L2, R2 and the internal resistance are in the circuit.", "Compare the new current through L2 with its rated 1,5 A."]),
]

# ---- QUESTION 9, the question paper page 15 and the memo page 20 ----
q9a = [
    mcq("9.1", "Name the type of generator. Choose from AC or DC.", ["AC", "DC"], 1,
        ["Does the current in the graph ever change direction?", "It stays on one side of the time axis."], marks=1),
    rub("9.2", "State the energy conversion that takes place in this generator while it is in operation.", 2,
        ["Mechanical / kinetic (energy) to electrical (energy). (2 or 0)"],
        ["A generator is turned by something.", "What goes in, and what comes out?"], each=2),
    rub("9.3", "Give a reason why this generator is NOT suitable for the transmission of electricity over long distances.", 1,
        ["Power / energy / voltage loss cannot be reduced / will be too large OR the current cannot be made smaller. ACCEPT: transformers do not work "
         "with DC / it cannot be stepped up or down. (1)"],
        ["Long-distance lines use transformers.", "Can DC be stepped up?"]),
    steps("9.4", "Calculate the frequency at which the coil rotates in the generator.", 2,
          [("Frequency of rotation (Hz)", 2, 50, 0.1, "f = 1/T = 1/0,02 ✓ = 50 Hz ✓ (OR 2 cycles / 0,04 s)")],
          ["One full rotation of the coil gives two humps here.", "Find the time for one rotation, then f = 1/T."]),
    rub("9.5", "Define the term root mean square (rms) current.", 2,
        ["The (root-mean-square) current is the alternating current that dissipates the same amount of energy as an equivalent DC current. (2)"],
        ["It compares an AC current with a DC current.", "Which AC current gives the same energy as a DC current?"], each=2, notes=[KEYWORDS]),
    steps("9.6", "Calculate the root-mean-square current delivered by the generator.", 3,
          [("rms current (A)", 3, 0.85, 0.005, "Irms = Imax/√2 ✓ = 1,2/√2 ✓ = 0,85 A ✓")],
          ["Read the peak current from the graph.", "Irms = Imax/√2."]),
]
q9b = [
    rub("9.7", "The graph below shows how the induced current varies with time after a change was made to the operation of the generator. Fully describe "
        "the change that was made.", 2,
        ["The speed of rotation was halved/half. ACCEPT: the frequency was halved/half OR the period was doubled. (2)"],
        ["Compare the peak current and the time per hump with the first graph.", "Both changed by the same factor."], each=2,
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
        ["Only two of the colours eject electrons from potassium.", "The lower-frequency one of those two gives the smaller kinetic energy."], marks=1),
    rub("10.2.2", "Explain the answer to QUESTION 10.2.1.", 2,
        ["Green light has a lower frequency / a longer wavelength than blue light / photons of blue light have more energy than photons of green light. (1)",
         "so green light ejects the electrons with the lower (maximum) kinetic energy. (1)"],
        ["E = hf: compare the frequencies of the colours that eject electrons.", "E = W0 + Ek(max): less photon energy, less kinetic energy."]),
    steps("10.2.3", "The electrons with a maximum kinetic energy of 2,65 x 10⁻²⁰ J are ejected by light that has a frequency of 5,85 x 10¹⁴ Hz. "
          "Calculate the frequency of the light that ejected electrons with a maximum kinetic energy of 6,96 x 10⁻²⁰ J.", 5,
          [("Work function of potassium (J)", 3, 3.61e-19, 0.01e-19, "E = W0 + Ek(max) ✓ (any one); (6,63 x 10⁻³⁴)(5,85 x 10¹⁴) ✓ = W0 + 2,65 x 10⁻²⁰ ✓; "
            "W0 = 3,61 x 10⁻¹⁹ J"),
           ("Frequency of the light (Hz)", 2, 6.5e14, 0.01e14, "(6,63 x 10⁻³⁴)f = 3,61 x 10⁻¹⁹ + 6,96 x 10⁻²⁰ ✓; f = 6,5 x 10¹⁴ Hz ✓")],
          ["The work function of potassium is the same for both colours.", "Find W0 from the first light, then use it for the second."]),
    mcq("10.2.4", "The intensity of the red light is increased, while the intensities of the blue light and green light remain the same. What effect will "
        "this change have on the rate at which electrons are ejected? Choose from INCREASES, DECREASES or REMAINS THE SAME.",
        ["Increases", "Decreases", "Remains the same"], 2,
        ["Does red light eject any electrons from potassium?", "More photons that cannot eject electrons change nothing."]),
]
q10c = [
    term("10.3.1", "Name the type of spectrum formed.", ["emission spectrum", "line emission spectrum", "emission"],
         ["Coloured lines on a black background.", "The gas gives out light."]),
    rub("10.3.2", "Explain the presence of the coloured lines in the spectrum.", 2,
        ["The coloured lines represent the (associated) frequencies / wavelengths / energies of the emitted photons (1)",
         "when atoms / electrons move (drop) to a lower energy level. (1)"],
        ["Each line is one frequency of light.", "When do excited atoms give out light?"]),
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
    {"id": "6", "title": "Question 6", "kind": "Doppler effect", "marks": 12,
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
     "figure": fig("Q9a", "Induced current (A) against time (s): four equal humps, each rising from 0 to a peak of 1,2 A and back to 0, one every 0,01 s "
                          "from 0 to 0,04 s; the current never goes below zero."), "items": q9a},
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

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Physical Sciences", "title": "Physical Sciences P1", "sitting": "November 2024", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Physics", "total": 150, "missions": missions}],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 10), hand-transcribed from the paper and memo PDFs and their "
                                                           "page images (formulas are images); no API call."},
        {"n": "2.3.1", "kind": "no_fit", "detail": "Calculations play as steps: each step is a number the memo's method produces, its formula and substitution "
                                                   "marks riding on it (the phone sees numbers, not working). 4.3.1 asks for a vector: the direction mark rides "
                                                   "on the magnitude; 4.3.2 is the magnitude (the direction is printed in the question)."},
        {"n": "8.3", "kind": "no_fit", "detail": "Decide by calculation: steps on L2's resistance and the new current (1,82 A, more than its rated 1,5 A); the "
                                                 "conclusion 'No' rides on the current. As a rubric of working, a right answer scores nothing."},
        {"n": "2.2", "kind": "no_fit", "detail": "Drawings (2.2, 3.2, 5.2, 7.2) are done on paper and self-checked against the memo's criteria."},
        {"n": "3.1.3", "kind": "memo_issue", "detail": "Memo ranges played as their centre with a tolerance covering them: 3.1.3 (7,32 – 7,35 m and "
                                                       "37,72 – 37,75 m), 5.3 (20,769 – 20,79 N), 6.3.2 (18,05 – 18,45 m·s⁻¹), 8.2.4 (47,16 – 47,19 V)."},
    ],
}
out = Path(__file__).parent / "out" / "ps-p1-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs and their page images (no API call)",
                                                        "scope": "Questions 1 to 10 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for m in missions:
    print(m["id"], "parts:", len(m["items"]), "marks:", sum(i["marks"] for i in m["items"]), "/", m["marks"])
print("total:", sum(i["marks"] for m in missions for i in m["items"]))
