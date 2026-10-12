"""Grade 10 Physical Sciences P1 (Physics) November 2024 (North West Department of Education, provincial assessment), the whole
paper (Questions 1 to 9, 100 marks, 2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`.
Stems, options, marks, answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions
are ours. Source (PROVENANCE-g10-g11.md): education.nwpg.gov.za, Examination > Assessment, the question paper PDF (English, 14
pages with the data sheets; its diagrams are images) and the marking guidelines PDF (English and Afrikaans, 6 pages), read from
their text and page images (100 dpi).

  python tools/ingest/transcribe_g10_ps_p1_2024_11_nw.py
  python tools/ingest/ingest.py "uploads/provincial/g10-ps-p1-2024-11-nw/08-November-2024-S2-GR10-Physical-Sciences-QP-P1-ENG.pdf" "uploads/provincial/g10-ps-p1-2024-11-nw/08-November-2024-S2-GR10-Physical-Sciences-MG-P1-ENG-AFR.pdf" --id g10-ps-p1-2024-11-nw --from-json

The Grade 12 rulings, as in transcribe_g11_ps_p1_2024_11_ec.py: multiple choice printed in the paper as printed; a choice printed
in the stem (INCREASE / DECREASE / ...) an MCQ of the printed choices; every calculation an authored working (provincial.py); a
definition, law or explanation statements; a one-word name a term. Where the memo's answer is wrong physics (5.3 and its
explanation 5.4), the right answer is the physics and the memo's is flagged.
Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-ps-p1-2024-11-nw", 595.32, 841.92, {
    "1.2": [3, 105, 306, 467, 424], "1.4": [4, 175, 126, 403, 251], "1.6": [4, 122, 452, 378, 491],
    "Q2": [5, 60, 136, 532, 288], "2.5a": [6, 222, 111, 338, 188], "2.5b": [6, 77, 233, 465, 340],
    "Q4": [8, 145, 167, 381, 258], "Q5": [9, 78, 186, 446, 430], "Q8": [11, 70, 152, 452, 380], "Q9": [12, 60, 152, 506, 535]},
    start=8)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term
CHANGE = ["INCREASE", "DECREASE", "REMAIN THE SAME"]

# ---- QUESTION 1: multiple choice, the question paper pages 3-4 and the memo page 2 ----
q1 = [
    mcq("1.1", "The number of wave pulses per second is called …", ["wavelength", "period", "frequency", "amplitude"], 2,
        ["Which quantity counts waves in one second?", "Its unit is the hertz (Hz)."]),
    mcq("1.2", "Consider the diagram of two pulses shown below. When the two pulses meet at point X, the type of interference and the "
        "resultant amplitude of the disturbance will be …",
        ["Destructive; 40 cm", "Destructive; 20 cm", "Constructive; 40 cm", "Constructive; 20 cm"], 2,
        ["Are both pulses on the same side of the rest position?", "When pulses overlap, their amplitudes add (with their signs)."],
        figure=P.fig("1.2", "Two upward pulses moving towards each other along a rope: the left one 30 cm high moving right, the right "
                            "one 10 cm high moving left, with point X between them.")),
    mcq("1.3", "A certain electromagnetic wave has 4,97 × 10⁻¹⁴ J of energy. The frequency of the wave is:",
        ["1,3 × 10²⁰ Hz", "7,5 × 10¹⁹ Hz", "3,3 × 10⁻⁴⁷ Hz", "1,7 × 10⁻²² Hz"], 1,
        ["Which equation links the energy of a photon and its frequency?", "f = E/h, with h = 6,63 × 10⁻³⁴ J·s."]),
    mcq("1.4", "In the following circuit the light bulbs are identical. Which switches must be closed for bulb A only to light up?",
        ["S₁, S₂ and S₃", "S₁ and S₂", "S₁ and S₃", "S₂ and S₃"], 1,
        ["Which switch is in the line every current must pass through?", "Which switch is in bulb A's branch, and which in bulb B's?"],
        figure=P.fig("1.4", "A battery with two parallel branches: bulb B with switch S₃, and bulb A with switch S₂; switch S₁ is in the "
                            "line joining the branches to the battery.")),
    mcq("1.5", "The straight line difference in position in space is called …", ["speed.", "velocity.", "distance.", "displacement."], 3,
        ["Is it a change in position or a rate?", "Which quantity is measured in a straight line from start to end?"]),
    mcq("1.6", "Consider the vector diagram given below. Which ONE of the following CORRECTLY describes the relationship between vectors "
        "A, B and C?", ["A + B = C", "A + C = B", "B + C = A", "A + B + C = 0"], 0,
        ["Which vectors point right, and which left?", "Add A and B head to tail: where does the result end?"],
        figure=P.fig("1.6", "Vector A, long, pointing right. Below it vector C pointing right to the middle, and vector B pointing left "
                            "from the right end to the middle; C and B are each half as long as A.")),
    mcq("1.7", "The kinetic energy of a moving body will increase the most if its …",
        ["velocity is doubled.", "mass is doubled.", "velocity is halved.", "mass is halved."], 0,
        ["Ek = ½mv²: how does Ek depend on m, and on v?", "What happens to v² when v doubles?"])]

# ---- QUESTION 2, the question paper pages 5-6 and the memo page 2 ----
q2 = [
    stmt("2.1", "Define the term transverse wave.", 2,
         ["A wave in which the particles of the medium vibrate at right angles to the direction of motion of the wave.",
          "A wave in which the particles of the medium vibrate perpendicular to the direction in which the wave travels."],
         ["A wave in which the particles of the medium vibrate parallel to the direction of motion of the wave.",
          "A wave that needs no medium to travel through.", "A wave made of compressions and rarefactions.",
          "A wave in which the particles move along with the wave, away from the source."],
         ["How do the particles move compared with the direction the wave travels?", "Think of a wave on a rope."], 2),
    answer("2.2", "Write down the amplitude, in metres, of this wave.", 1, ["0,4 m", "40 m", "0,8 m", "4 m"],
           ["How far does the wave rise above the rest position?", "How many metres is 40 cm?"]),
    answer("2.3", "Determine the period of this wave.", 1, ["8 s", "4 s", "16 s", "0,125 s"],
           ["How long does one complete wave take?", "Measure from one crest to the next crest."]),
    term("2.4.1", "If the distance d on the diagram is 0,9 m: what is the name of the physical quantity given to distance d?",
         ["wavelength", "the wavelength"], ["d spans one complete wave.", "What is the length of one complete wave called?"]),
    work("2.4.2", "If the distance d on the diagram is 0,9 m: calculate the speed of the complete wave as shown in the diagram above.", 5, [
        "f = {1}/{T} = {1}/{8} = 0,125 Hz\nv = fλ\n= (0,125)(0,9)\n= 0,11 m·s⁻¹",       # the memo
        "f = {1}/{T} = {1}/{8} = 0,125 Hz\nv = {f}/{λ}\n= {0,125}/{0,9}\n= 0,14 m·s⁻¹",   # the wave equation upside down
        "f = T = 8 Hz\nv = fλ\n= (8)(0,9)\n= 7,2 m·s⁻¹",                                  # the period taken as the frequency
        "f = {1}/{T} = {1}/{4} = 0,25 Hz\nv = fλ\n= (0,25)(0,9)\n= 0,23 m·s⁻¹"],          # half a period taken as T
        ["How is the frequency related to the period?", "Which equation links speed, frequency and wavelength?"], after=["2.3"])]
q25 = [
    mcq("2.5.1", "Identify the sound waves as TRANSVERSE or LONGITUDINAL.", ["TRANSVERSE", "LONGITUDINAL"], 1,
        ["How do air particles move when sound passes through them?", "Sound is made of compressions and rarefactions."], marks=1),
    answer("2.5.2", "Which ONE of the patterns (A, B or C) represents a LOUDER note than the original note? Give a reason for your answer.",
           2, ["B: it has a greater amplitude", "C: it has a higher frequency", "A: it has a lower frequency",
               "B: it has a higher frequency"],
           ["Which property of a sound wave decides how loud it is?", "Compare the heights of the patterns with the original."],
           figure=P.fig("2.5b", "Three oscilloscope patterns: A, a wave about as tall as the original with more waves on the screen; B, "
                                "a much taller wave with more waves; C, a wave about as tall as the original with many more waves.")),
    answer("2.5.3", "Above which frequency is a sound wave classified as ultrasound?", 1, ["20 kHz", "20 Hz", "2 kHz", "200 kHz"],
           ["What is the highest frequency humans can hear?", "Ultrasound is above that."]),
    stmt("2.5.4", "Name ONE use of ultrasound in the medical treatment of patients.", 1,
         ["Monitoring a fetus.", "Cleaning medical equipment.", "Diagnosing tumours and/or gallstones.", "Evaluating blood flow."],
         ["Taking X-ray photographs of broken bones.", "Killing cancer cells with gamma rays.", "Heating food in a microwave oven."],
         ["Ultrasound is high-frequency sound that reflects off tissues.", "Which uses are of sound, not of electromagnetic radiation?"], 1)]

# ---- QUESTION 3, the question paper page 7 and the memo page 3 ----
q3 = [
    term("3.1", "How are electromagnetic waves generated?", ["accelerating charges", "accelerating charge", "accelerated charges",
                                                             "accelerating charged particles"],
         ["What kind of moving charge sends out electromagnetic radiation?", "A charge moving at a constant velocity does not."]),
    stmt("3.2", "Explain what is meant by the dual nature of electromagnetic radiation.", 2,
         ["Some aspects of the behaviour of electromagnetic radiation are best explained by a wave model, and others by a particle model.",
          "Electromagnetic radiation behaves both as a wave and as a particle (a photon)."],
         ["Electromagnetic radiation travels as a wave in a vacuum and as a particle in a medium.",
          "Electromagnetic radiation has an electric field and a magnetic field.", "Electromagnetic radiation can be reflected and refracted.",
          "Electromagnetic radiation is made of transverse and longitudinal waves."],
         ["What are the two models used to describe light?", "Do both models describe all of its behaviour?"], 2),
    term("3.3.1", "From the information above, name the type of electromagnetic radiation that is used in hospitals to identify broken bones.",
         ["x-rays", "x-ray", "x rays"], ["Which radiation passes through flesh but not bone?", "It is used for photographs of the skeleton."]),
    term("3.3.2", "From the information above, name the type of electromagnetic radiation that is used in Wi-Fi (Wireless Fidelity).",
         ["radio waves", "radio wave", "radio"], ["Which radiation in the list carries signals through the air?",
                                                  "It has the longest wavelength in the list."]),
    term("3.3.3", "From the information above, name the type of electromagnetic radiation that has the highest energy.",
         ["gamma rays", "gamma ray", "gamma radiation", "gamma"], ["Energy increases with frequency.",
                                                                  "Which radiation in the list has the highest frequency?"]),
    work("3.4", "Calculate the energy of a photon of microwaves with a wavelength of 2,1 × 10⁻² m.", 3, [
        "E = {hc}/{λ}\n= {(6,63 × 10⁻³⁴)(3 × 10⁸)}/{2,1 × 10⁻²}\n= 9,47 × 10⁻²⁴ J",     # the memo
        "E = hλ\n= (6,63 × 10⁻³⁴)(2,1 × 10⁻²)\n= 1,39 × 10⁻³⁵ J",                          # the wavelength for the frequency
        "E = {hλ}/{c}\n= {(6,63 × 10⁻³⁴)(2,1 × 10⁻²)}/{3 × 10⁸}\n= 4,64 × 10⁻⁴⁴ J",       # λ and c swapped
        "E = {hc}/{λ}\n= {(6,63 × 10⁻³⁴)(3 × 10⁸)}/{2,1 × 10²}\n= 9,47 × 10⁻²⁸ J"],      # the sign of the power lost
        ["Which equation gives a photon's energy from its wavelength?", "h = 6,63 × 10⁻³⁴ J·s and c = 3 × 10⁸ m·s⁻¹."])]

# ---- QUESTION 4, the question paper page 8 and the memo page 3 ----
q4 = [
    work("4.1", "If the charge on sphere D was −2 nC BEFORE the spheres touched, calculate the initial charge on sphere E.", 3, [
        "Q = {Q_D + Q_E}/{2}\n+5 × 10⁻⁹ = {(−2 × 10⁻⁹) + Q_E}/{2}\nQ_E = +12 × 10⁻⁹ C",      # the memo
        "Q = Q_D + Q_E\n+5 × 10⁻⁹ = (−2 × 10⁻⁹) + Q_E\nQ_E = +7 × 10⁻⁹ C",                  # the charge not shared
        "Q = {Q_D + Q_E}/{2}\n+5 × 10⁻⁹ = {(+2 × 10⁻⁹) + Q_E}/{2}\nQ_E = +8 × 10⁻⁹ C",      # the sign of D's charge lost
        "Q = {Q_D + Q_E}/{2}\n+5 × 10⁻⁹ = {(−2 × 10⁻⁹) + Q_E}/{2}\nQ_E = +3 × 10⁻⁹ C"],     # the 2 not multiplied across
        ["After identical spheres touch, how is the total charge shared?", "What was the total charge, if each now has +5 nC?"]),
    work("4.2", "Calculate the number of electrons transferred when the spheres touched.", 4, [
        "ΔQ = +5 × 10⁻⁹ − (−2 × 10⁻⁹) = 7 × 10⁻⁹ C\nn = {ΔQ}/{q_e}\n= {7 × 10⁻⁹}/{1,6 × 10⁻¹⁹}\n= 4,375 × 10¹⁰ electrons",     # the memo
        "ΔQ = +5 × 10⁻⁹ − (+2 × 10⁻⁹) = 3 × 10⁻⁹ C\nn = {ΔQ}/{q_e}\n= {3 × 10⁻⁹}/{1,6 × 10⁻¹⁹}\n= 1,875 × 10¹⁰ electrons",     # the sign of D's charge lost
        "ΔQ = +5 × 10⁻⁹ − (−2 × 10⁻⁹) = 7 × 10⁻⁹ C\nn = ΔQ × q_e\n= (7 × 10⁻⁹)(1,6 × 10⁻¹⁹)\n= 1,12 × 10⁻²⁷ electrons",       # multiplied, not divided
        "ΔQ = +12 × 10⁻⁹ + (−2 × 10⁻⁹) = 10 × 10⁻⁹ C\nn = {ΔQ}/{q_e}\n= {10 × 10⁻⁹}/{1,6 × 10⁻¹⁹}\n= 6,25 × 10¹⁰ electrons"],  # the total charge
        ["By how much did D's charge change?", "How many electrons make up that charge?"]),
    mcq("4.3", "Were electrons transferred from D to E or from E to D during contact?", ["From D to E", "From E to D"], 0,
        ["D went from −2 nC to +5 nC: did it gain or lose electrons?", "Electrons move from the sphere that loses them."], marks=1)]

# ---- QUESTION 5, the question paper page 9 and the memo page 4 ----
q5 = [
    stmt("5.1", "Define the term potential difference.", 2,
         ["The energy transferred per unit electric charge flowing through a conductor.",
          "The work done per unit charge between the ends of a conductor."],
         ["The rate of flow of charge through a conductor.", "The opposition to the flow of charge in a conductor.",
          "The total charge that flows through a conductor.", "The energy transferred per unit time in a conductor."],
         ["Potential difference is measured in volts: J per what?", "It is energy compared with charge."], 2),
    work("5.2.1", "Calculate the total resistance of the circuit.", 4, [
        "{1}/{R_p} = {1}/{2} + {1}/{2}\nR_p = 1 Ω\nR_T = 1 + 4\n= 5 Ω",                    # the memo
        "R_p = 2 + 2\nR_p = 4 Ω\nR_T = 4 + 4\n= 8 Ω",                                      # the parallel resistors added in series
        "{1}/{R_p} = {1}/{2} + {1}/{2}\nR_p = 1 Ω\nR_T = {1}/{1} + {1}/{4}\n= 1,25 Ω",     # the 4 Ω taken in parallel too
        "{1}/{R_p} = {1}/{2} + {1}/{2}\nR_p = 1 Ω\nR_T = 1 × 4\n= 4 Ω"],                   # multiplied, not added
        ["Which resistors are in parallel, and which is in series with them?", "How do you combine resistors in parallel?"]),
    work("5.2.2", "Calculate the amount of charge that flows through ammeter A₁ in 120 s.", 3, [
        "I = {V}/{R} = {12}/{4} = 3 A\nQ = IΔt\n= (3)(120)\n= 360 C",                      # the memo
        "I = 1,5 A (one branch's ammeter)\nQ = IΔt\n= (1,5)(120)\n= 180 C",                # a branch current for the total
        "I = {V}/{R} = {12}/{4} = 3 A\nQ = {I}/{Δt}\n= {3}/{120}\n= 0,03 C",               # divided, not multiplied
        "I = {V}/{R} = {12}/{5} = 2,4 A\nQ = IΔt\n= (2,4)(120)\n= 288 C"],                 # the 4 Ω's voltage over the total resistance
        ["What current flows through the 4 Ω resistor, which A₁ is in series with?", "Which equation links charge, current and time?"]),
    work("5.2.3", "Calculate the reading on V₁, if the voltmeter uses 5 400 J of energy and the same amount of charge calculated at QUESTION "
         "5.2.2 flows through it.", 3, [
        "V = {W}/{Q}\n= {5 400}/{360}\n= 15 V",                     # the memo
        "V = WQ\n= (5 400)(360)\n= 1 944 000 V",                    # multiplied, not divided
        "V = {Q}/{W}\n= {360}/{5 400}\n= 0,07 V",                   # upside down
        "V = {W}/{Q}\n= {5 400}/{120}\n= 45 V"],                    # the time for the charge
        ["Which equation links potential difference, energy and charge?", "Use the charge from 5.2.2."], after=["5.2.2"]),
    mcq("5.3", "A wire with negligible resistance is now connected from X to Y in the circuit. How will the reading on voltmeter V₁ be "
        "affected? Choose from INCREASE, DECREASE or REMAIN THE SAME.", CHANGE, 2,
        ["What does V₁ measure, connected across the battery?", "The battery's internal resistance is ignored: are any volts lost "
                                                               "inside it?"], marks=1),
    stmt("5.4", "Explain the answer to QUESTION 5.3 WITHOUT any calculations.", 2,
         ["The battery's internal resistance is ignored, so no potential difference is lost inside the battery.",
          "V₁ reads the emf of the battery, which does not depend on the external resistance.",
          "The external resistance decreases and the current increases, but the battery's terminal potential difference stays the same."],
         ["The current increases, so the reading on V₁ decreases.", "The wire adds resistance to the circuit, so the current decreases.",
          "The total resistance increases, so V₁ increases.", "The wire stops the current from flowing through the battery."],
         ["With no internal resistance, what is the battery's terminal potential difference?", "Does the emf depend on the circuit "
                                                                                                "connected to it?"], 1, after=["5.3"])]

# ---- QUESTION 6, the question paper page 10 and the memo page 5 ----
q6 = [
    stmt("6.1", "Define the term average speed.", 2,
         ["The total distance travelled per total time.", "The total distance covered divided by the total time taken."],
         ["The total displacement per total time.", "The rate of change of velocity.", "The speed at a particular instant.",
          "The total time taken per total distance travelled."],
         ["Is speed a scalar or a vector?", "Which total is divided by which?"], 2),
    work("6.2", "Calculate the average speed that Tatjana swam to win the 100 m breaststroke event.", 3, [
        "v = {d}/{Δt}\n= {100}/{65}\n= 1,54 m·s⁻¹",      # the memo
        "v = {d}/{Δt}\n= {50}/{65}\n= 0,77 m·s⁻¹",       # one length of the pool
        "v = {Δt}/{d}\n= {65}/{100}\n= 0,65 m·s⁻¹",      # upside down
        "v = {Δx}/{Δt}\n= {0}/{65}\n= 0 m·s⁻¹"],         # the displacement (back at the start) for the distance
        ["What total distance did she swim?", "Average speed uses distance, not displacement."])]

# ---- QUESTION 7, the question paper page 10 and the memo page 5 ----
TC = "Traffic car: Δx = viΔt + ½aΔt² = (0)(12,5) + ½(2)(12,5)² = 156,25 m\n"
q7 = [
    stmt("7.1", "Define the term acceleration.", 2,
         ["The rate of change of velocity.", "The change in velocity per unit time."],
         ["The rate of change of position.", "The rate of change of displacement.", "The change in speed over a distance.",
          "The total distance travelled per total time."],
         ["Acceleration changes which quantity?", "Rate means per unit time."], 2),
    answer("7.2", "Convert 84 km·h⁻¹ to m·s⁻¹.", 1, ["23,33 m·s⁻¹", "302,4 m·s⁻¹", "84 000 m·s⁻¹", "1,4 m·s⁻¹"],
           ["How many metres in a kilometre, and seconds in an hour?", "Divide by 3,6."]),
    work("7.3", "A traffic officer starts his car from rest just as the taxi passes him. The traffic car accelerates uniformly at 2 m·s⁻² "
         "until it reaches a maximum velocity of 25 m·s⁻¹. Calculate the time t that it will take the traffic car to reach its maximum "
         "velocity.", 3, [
        "vf = vi + aΔt\n25 = 0 + 2Δt\nΔt = 12,5 s",                # the memo
        "vf = vi + aΔt\n25 = 23,33 + 2Δt\nΔt = 0,84 s",            # the taxi's speed as vi
        "vf = vi + aΔt\n25 = 0 + 2Δt\nΔt = 50 s",                  # multiplied, not divided
        "vf = vi + aΔt\n0 = 25 + 2Δt\nΔt = −12,5 s"],              # vi and vf swapped
        ["What is the traffic car's initial velocity?", "Which equation links vf, vi, a and Δt?"]),
    work("7.4", "Determine by calculation which vehicle (the taxi or the traffic car) is ahead after time t seconds has passed. Assume "
         "that the taxi maintains its constant speed.", 5, [
        TC + "Taxi: Δx = vΔt = (23,33)(12,5) = 291,63 m\nThe taxi is still ahead",                                       # the memo
        "Traffic car: Δx = viΔt + ½aΔt² = (0)(12,5) + (2)(12,5)² = 312,5 m\nTaxi: Δx = vΔt = (23,33)(12,5) = 291,63 m\n"
        "The traffic car is ahead",                                                                                         # the ½ left out
        "Traffic car: Δx = vΔt = (25)(12,5) = 312,5 m\nTaxi: Δx = vΔt = (23,33)(12,5) = 291,63 m\nThe traffic car is ahead",  # its top speed the whole time
        TC + "Taxi: Δx = vΔt = (84)(12,5) = 1 050 m\nThe taxi is still ahead"],                                           # km·h⁻¹ not converted
        ["How far does each vehicle travel in 12,5 s?", "The traffic car accelerates from rest; the taxi keeps a constant speed."],
        after=["7.2", "7.3"])]

# ---- QUESTION 8, the question paper page 11 and the memo page 6 ----
q8 = [
    answer("8.1", "The short time interval between the traffic light turning green (for GO) and the driver responding to the signal is "
                  "known as \"the driver's reaction time\". How long does the driver take to respond when the traffic light changes to "
                  "green?", 1, ["0,8 s", "0 s", "5,8 s", "8 s"],
           ["At what time does the velocity start to increase?", "Before that, the car is still at rest."]),
    answer("8.2", "Determine the maximum speed of the car.", 1, ["12,5 m·s⁻¹", "15 m·s⁻¹", "10 m·s⁻¹", "8 m·s⁻¹"],
           ["Where does the graph level off?", "Read the velocity axis at that level."]),
    work("8.3", "Use the graph only (NO equations of motion) to calculate the average acceleration of the car.", 4, [
        "a = gradient = {Δv}/{Δt}\n= {12,5 − 0}/{5,8 − 0,8}\n= 2,5 m·s⁻²",        # the memo
        "a = gradient = {Δv}/{Δt}\n= {12,5 − 0}/{5,8 − 0}\n= 2,16 m·s⁻²",         # the reaction time ignored
        "a = gradient = {Δv}/{Δt}\n= {12,5 − 0}/{8 − 0,8}\n= 1,74 m·s⁻²",         # the level part included
        "a = gradient = {Δt}/{Δv}\n= {5,8 − 0,8}/{12,5 − 0}\n= 0,4 m·s⁻²"],        # upside down
        ["What does the gradient of a velocity-time graph give?", "Between which times does the velocity change?"]),
    work("8.4", "Use the graph only (NO equations of motion) to determine the displacement of the car over these 8 s.", 4, [
        "Δx = area under the graph\n= ½(5,8 − 0,8)(12,5) + (8 − 5,8)(12,5)\n= 31,25 + 27,5\n= 58,75 m",    # the memo
        "Δx = area under the graph\n= (5,8 − 0,8)(12,5) + (8 − 5,8)(12,5)\n= 62,5 + 27,5\n= 90 m",         # the triangle as a rectangle
        "Δx = area under the graph\n= ½(5,8 − 0)(12,5) + (8 − 5,8)(12,5)\n= 36,25 + 27,5\n= 63,75 m",      # the triangle from t = 0
        "Δx = area under the graph\n= ½(8 − 0,8)(12,5) + 0\n= 45 + 0\n= 45 m"],                          # one triangle over the whole time
        ["What does the area under a velocity-time graph give?", "Split it into a triangle and a rectangle."])]

# ---- QUESTION 9, the question paper page 12 and the memo page 6 ----
q9 = [
    stmt("9.1", "Define gravitational potential energy.", 2,
         ["The energy an object has because of its position in the gravitational field relative to a reference point.",
          "The energy an object has because of its height above a reference point."],
         ["The energy an object has because of its motion.", "The total of the kinetic and potential energy of an object.",
          "The force of gravity acting on an object.", "The energy stored in a stretched or compressed spring."],
         ["Does it depend on motion or on position?", "Ep = mgh."], 2),
    answer("9.2", "Determine the maximum potential energy of the bob.", 2, ["0,30 J", "0,15 J", "1,00 J", "0 J"],
           ["Where on the graph is Ep largest?", "Read the energy axis at A or C."]),
    work("9.3", "Calculate the maximum gain in height (h) of the bob.", 4, [
        "m = 50 g = 0,05 kg\nmgh = 0,30\n0,05 × 9,8 × h = 0,30\nh = 0,61 m",            # the memo
        "m = 50 g\nmgh = 0,30\n50 × 9,8 × h = 0,30\nh = 6,12 × 10⁻⁴ m",                  # grams not converted
        "m = 50 g = 0,5 kg\nmgh = 0,30\n0,5 × 9,8 × h = 0,30\nh = 0,06 m",               # the wrong conversion
        "m = 50 g = 0,05 kg\nmgh = 0,30\nh = {0,05 × 9,8}/{0,30}\nh = 1,63 m"],          # upside down
        ["Which equation gives Ep from the height?", "Convert the mass to kilograms first."], after=["9.2"]),
    work("9.4", "Calculate the maximum speed of the bob at position B.", 3, [
        "ME at A = ME at B\n(Ep + Ek)A = (Ep + Ek)B\n0,30 + 0 = 0 + ½(0,05)v²\nv = 3,46 m·s⁻¹",       # the memo
        "ME at A = ME at B\n(Ep + Ek)A = (Ep + Ek)B\n0,30 + 0 = 0 + ½(50)v²\nv = 0,11 m·s⁻¹",        # grams not converted
        "ME at A = ME at B\n(Ep + Ek)A = (Ep + Ek)B\n0,30 + 0 = 0 + (0,05)v²\nv = 2,45 m·s⁻¹",       # the ½ left out
        "ME at A = ME at B\n(Ep + Ek)A = (Ep + Ek)B\n0,30 + 0 = 0 + ½(0,05)v\nv = 12 m·s⁻¹"],        # v not squared
        ["At A the bob is at rest; at B it is at the lowest point.", "Mechanical energy is conserved: Ep at A becomes Ek at B."],
        after=["9.2"]),
    stmt("9.5", "State the law of conservation of mechanical energy in words.", 2,
         ["The total energy of an isolated system remains constant.",
          "In an isolated system, the total mechanical energy (kinetic plus potential) remains constant."],
         ["Energy is created when an object falls.", "The kinetic energy of an object is always equal to its potential energy.",
          "The total mechanical energy of a moving object always decreases.", "The potential energy of an object always stays the same."],
         ["What happens to the total of Ek and Ep when there is no friction?", "What does 'isolated system' mean?"], 2)]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 14, "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Transverse waves", "marks": 10,
     "lead": "The diagram below represents a transverse wave produced by a source.",
     "figure": P.fig("Q2", "A graph of amplitude (cm) against time (s): the wave starts at 40 cm, has troughs of −40 cm at 4 s and "
                           "12 s and crests of 40 cm at 8 s and 16 s. An arrow labelled d spans from the trough at 4 s to the trough at "
                           "12 s."), "items": q2},
    {"id": "2.5", "title": "Question 2.5", "kind": "Sound", "marks": 5,
     "lead": "The following sound wave, produced by a tuning fork, is observed on an oscilloscope. A few more notes are played on "
             "different tuning forks and patterns A, B and C are observed.",
     "figure": P.fig("2.5a", "An oscilloscope screen showing the original note: one wave across the screen, of medium height."),
     "items": q25},
    {"id": "3", "title": "Question 3", "kind": "Electromagnetic radiation", "marks": 9,
     "lead": "The electromagnetic spectrum includes amongst others, radio waves, ultraviolet light, gamma rays, visible light and "
             "x-rays.", "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Electrostatics", "marks": 8,
     "lead": "The diagram below shows two small identical spheres, D and E, on an insulated stand. The spheres are brought together "
             "to touch and then separated. After touching and separating, the charge on spheres D and E is +5 nC.",
     "figure": P.fig("Q4", "Two identical spheres D and E on insulating stands, each labelled +5 nC."), "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Electric circuits", "marks": 15,
     "lead": "The circuit diagram below shows three resistors connected to a battery. The voltmeter over the 4 Ω resistor has a reading "
             "of 12 V. Voltmeter V₁ and ammeter A₁ are connected as shown in the diagram below. The resistance of the battery, ammeter "
             "and connecting wires can be ignored.",
     "figure": P.fig("Q5", "A battery with voltmeter V₁ across it, in series with a 4 Ω resistor (a voltmeter across it reads 12 V), "
                           "two 2 Ω resistors in parallel (a voltmeter across them reads 3 V; an ammeter in each branch reads 1,5 A) and "
                           "ammeter A₁. Point X is between the 4 Ω resistor and the parallel pair; point Y is between the battery and "
                           "A₁."), "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Motion in one dimension", "marks": 5,
     "lead": "In the Paris 2024 Olympics, Tatjana Smith won a gold medal in the 100 m breaststroke event, when she completed this event "
             "in 65 seconds. Olympic swimming pools are 50 m in length.", "items": q6},
    {"id": "7", "title": "Question 7", "kind": "Equations of motion", "marks": 11,
     "lead": "A taxi is travelling at a constant speed of 84 km·h⁻¹ on a straight and level road where the speed limit is 60 km·h⁻¹.",
     "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Motion graphs", "marks": 10,
     "lead": "A driver stops his car at the red traffic light. The graph of the car's velocity against time shows its motion for 8 s "
             "from the time the traffic light turns green.",
     "figure": P.fig("Q8", "A velocity-time graph: the velocity is 0 until 0,8 s, rises in a straight line to 12,5 m·s⁻¹ at 5,8 s, "
                           "then stays at 12,5 m·s⁻¹ until 8 s."), "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Mechanical energy", "marks": 13,
     "lead": "The graph below shows energy against position for a pendulum bob (mass 50 g) as it moves from A to B and to C. Air "
             "resistance is negligible.",
     "figure": P.fig("Q9", "A pendulum swinging from A through D and the lowest point B to C, A and C at the same height h above B. "
                           "Below it, a graph of potential energy against position: 0,30 J at A, falling in a straight line to 0 at B, "
                           "and rising to 0,30 J at C."), "items": q9}]

P.finish(missions,
         {"subject": "Physical Sciences", "title": "Physical Sciences P1 (Physics)", "sitting": "November 2024", "total_marks": 100,
          "time": "2 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "5.3", "kind": "memo_issue", "detail": "The memo gives DECREASE, and 5.4 explains that the current increases so the reading "
                                                       "on V₁ decreases. V₁ is connected across the battery and the stem says the "
                                                       "battery's resistance can be ignored, so V₁ reads the emf (15 V, as 5.2.3 finds) "
                                                       "whatever the external resistance: REMAIN THE SAME. The right answer here is the "
                                                       "physics; 5.4's cards follow it."},
          {"n": "2.4.2", "kind": "low_confidence", "detail": "The diagram's horizontal axis is time (s), so d spans one period (8 s), not a "
                                                             "distance; the paper gives d = 0,9 m and the memo reads it as the "
                                                             "wavelength (v = fλ = 0,11 m·s⁻¹). The options follow the memo."}],
         {"1": 14, "2": 15, "3": 9, "4": 8, "5": 15, "6": 5, "7": 11, "8": 10, "9": 13}, 100,
         {"2.4.2": ["2.3"], "5.2.3": ["5.2.2"], "5.4": ["5.3"], "7.4": ["7.2", "7.3"], "9.3": ["9.2"], "9.4": ["9.2"]},
         "Questions 1 to 9 (the whole paper)")
