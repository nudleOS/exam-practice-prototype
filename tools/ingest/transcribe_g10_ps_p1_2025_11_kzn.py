"""Grade 10 Physical Sciences P1 (Physics) November 2025 (KwaZulu-Natal Department of Education), the whole paper (Questions 1 to 8,
100 marks, 2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options, marks and the
memo's working are the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): re-published by
Stanmore Secondary (stanmorephysics.com) as one scanned PDF, the question paper (pages 1-13, with the data sheet) then the marking
memorandum (pages 14-19), no text layer: read from its page images (100 dpi). Split into '<id> QP.pdf' and '<id> MG.pdf'.

  python tools/ingest/transcribe_g10_ps_p1_2025_11_kzn.py
  python tools/ingest/ingest.py "uploads/provincial/g10-ps-p1-2025-11-kzn/g10-ps-p1-2025-11-kzn QP.pdf" "uploads/provincial/g10-ps-p1-2025-11-kzn/g10-ps-p1-2025-11-kzn MG.pdf" --id g10-ps-p1-2025-11-kzn --from-json

The Grade 12 rulings, as in transcribe_g10_ps_p1_2024_11_nw.py: multiple choice printed in the paper as printed (1.1 and 1.3 print their
options as tables: typed into the option text); a choice printed in the stem an MCQ of the printed choices; every calculation an authored
working (provincial.py); a definition or explanation statements. Figure boxes in PDF points (page 595 x 842), measured on the page
images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-ps-p1-2025-11-kzn", 595.44, 841.68, {
    "1.1": [3, 178, 230, 416, 352], "1.3": [4, 130, 110, 463, 378], "2.2": [6, 132, 178, 440, 330], "Q4": [7, 195, 150, 390, 268],
    "Q5": [8, 82, 160, 535, 410], "6.1": [9, 68, 150, 562, 319], "6.2": [10, 132, 170, 440, 352], "Q7": [11, 79, 180, 547, 328],
    "Q8": [12, 142, 196, 330, 335]}, start=5)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term

# ---- QUESTION 1: multiple choice, the question paper pages 3-5 and the memo page 2 ----
q1 = [
    mcq("1.1", "Pulse P, moving to the right, with an amplitude of X metres overlaps with pulse R, moving to the left, to form a TROUGH with an "
        "amplitude of 2,25X metres. Which of the following combinations will be CORRECT when the pulses meet at the same point in the medium?",
        ["Type of interference: constructive; amplitude of pulse R: 1,25X", "Type of interference: destructive; amplitude of pulse R: 1,25X",
         "Type of interference: constructive; amplitude of pulse R: 3,25X", "Type of interference: destructive; amplitude of pulse R: 3,25X"], 3,
        ["A crest meets a trough: what kind of interference is that?", "X − (amplitude of R) = −2,25X."],
        figure=P.fig("1.1", "Pulse P, a crest, moving right, and pulse R, a deeper trough, moving left towards it.")),
    mcq("1.2", "Which of the following indicates the region of low pressure in a longitudinal wave?", ["Compression", "Crest", "Rarefaction",
        "Trough"], 2, ["Particles are spread out there.", "Crests and troughs belong to transverse waves."]),
    mcq("1.3", "A 12 V battery is connected to 3 resistors as shown in the circuit diagram below. Which of the following combinations of voltmeter "
        "readings will be CORRECT?", ["V₁ 4 V; V₂ 4 V; V₃ 4 V", "V₁ 6 V; V₂ 6 V; V₃ 6 V", "V₁ 4 V; V₂ 8 V; V₃ 8 V", "V₁ 8 V; V₂ 4 V; V₃ 4 V"], 1,
        ["Two 2Y Ω resistors in parallel make Y Ω.", "Equal resistances in series share the voltage equally."],
        figure=P.fig("1.3", "A 12 V battery in series with R₁ = Y Ω and with R₂ = 2Y Ω and R₃ = 2Y Ω in parallel; voltmeter V₁ across R₁, V₂ "
                            "across R₂ and V₃ across R₃.")),
    mcq("1.4", "Which ONE of the following statements is TRUE? An object experiences negative acceleration when it is moving in the …",
        ["negative direction at a constant velocity.", "positive direction, experiencing a constant decrease in speed.",
         "negative direction, experiencing a constant decrease in speed.", "positive direction, experiencing a constant increase in speed."], 1,
        ["Acceleration is negative when it points in the negative direction.", "Slowing down while moving the positive way …"]),
    mcq("1.5", "The mechanical energy of an object dropped from the top of a building of height H metres is E. Which ONE of the following is the "
        "mechanical energy of the object when it is ¼H metres above the ground?", ["E", "½E", "¼E", "¾E"], 0,
        ["Air resistance is not mentioned.", "Mechanical energy is conserved."])]

# ---- QUESTION 2, the question paper pages 5-6 and the memo pages 2-3 ----
q21 = [
    mcq("2.1.1", "Are the seismic waves described above TRANSVERSE or LONGITUDINAL waves?", ["TRANSVERSE", "LONGITUDINAL"], 1,
        ["The particles move back and forth in the direction the wave travels.", "Like sound."], marks=1),
    work("2.1.2(a)", "Calculate the speed of the wave.", 3, [
        "speed = {distance}/{time}\n= {300 000}/{45}\n= 6 666,67 m·s⁻¹",      # the memo
        "speed = {distance}/{time}\n= {300}/{45}\n= 6,67 m·s⁻¹",              # km not converted
        "speed = {time}/{distance}\n= {45}/{300 000}\n= 1,5 × 10⁻⁴ m·s⁻¹",     # upside down
        "speed = distance × time\n= 300 000 × 45\n= 1,35 × 10⁷ m·s⁻¹"],       # multiplied
        ["The wave travels 300 km in 45 s.", "Convert km to m."]),
    work("2.1.2(b)", "Calculate the frequency of the wave.", 3, [
        "v = fλ\n6 666,67 = f × 3 600\nf = 1,85 Hz",          # the memo
        "v = {f}/{λ}\n6 666,67 = {f}/{3 600}\nf = 2,4 × 10⁷ Hz",   # the wave equation upside down
        "v = fλ\n6 666,67 = f × 3,6\nf = 1 851,85 Hz",        # λ in km
        "f = {1}/{T}\nT = 45 s\nf = 0,02 Hz"],                # the travel time as the period
        ["Which equation links speed, frequency and wavelength?", "λ = 3 600 m."], after=["2.1.2(a)"]),
    work("2.1.3", "Determine the number of waves that pass the seismic station in the first minute of the earthquake.", 4, [
        "t = 60 − 45 = 15 s\n1,85 = {number of waves}/{15}\n= 27,75 waves",       # the memo
        "t = 60 s\n1,85 = {number of waves}/{60}\n= 111 waves",                    # the 45 s before the first wave counted
        "t = 60 − 45 = 15 s\n1,85 = {15}/{number of waves}\n= 8,11 waves",         # upside down
        "t = 60 + 45 = 105 s\n1,85 = {number of waves}/{105}\n= 194,25 waves"],    # added
        ["The first wave reaches the station at 45 s.", "Frequency = waves per second."], after=["2.1.2(b)"])]
q22 = [
    stmt("2.2.1", "Define the term wavelength in words.", 2,
         ["The distance between two successive points in phase.", "The distance between two consecutive crests (or troughs)."],
         ["The number of waves per second.", "The time taken for one complete wave.", "The maximum disturbance from the rest position.",
          "The speed of the wave in a medium."],
         ["It is a distance.", "Between two points doing the same thing."], 2),
    work("2.2.2", "Determine the wavelength of the sound wave.", 5, [
        "speed = {6 500}/{19} = 342,11 m·s⁻¹\nv = fλ\n342,11 = 490 × λ\nλ = 0,7 m",         # the memo
        "speed = {19}/{6 500} = 0,0029 m·s⁻¹\nv = fλ\n0,0029 = 490 × λ\nλ = 5,97 × 10⁻⁶ m",  # speed upside down
        "speed = {6 500}/{19} = 342,11 m·s⁻¹\nv = {f}/{λ}\n342,11 = {490}/{λ}\nλ = 1,43 m",  # the wave equation upside down
        "speed = 6 500 × 19 = 123 500 m·s⁻¹\nv = fλ\n123 500 = 490 × λ\nλ = 252,04 m"],      # multiplied
        ["First find the speed of sound from the distance and the time.", "Then v = fλ."])]

# ---- QUESTION 3, the question paper page 6 and the memo page 3 ----
q3 = [
    work("3.1", "Use suitable calculations to show that UV-B will cause damage to DNA.", 4, [
        "E = hf\n= 6,63 × 10⁻³⁴ × 1,2 × 10¹⁵\n= 7,96 × 10⁻¹⁹ J\n7,96 × 10⁻¹⁹ J > 4,5 × 10⁻¹⁹ J, so UV-B damages DNA",       # the memo
        "E = hf\n= 6,63 × 10⁻³⁴ × 1,2 × 10¹⁵\n= 7,96 × 10⁻¹⁹ J\n7,96 × 10⁻¹⁹ J > 4,5 × 10⁻¹⁹ J, so UV-B does not damage DNA",  # the conclusion reversed
        "E = {h}/{f}\n= {6,63 × 10⁻³⁴}/{1,2 × 10¹⁵}\n= 5,53 × 10⁻⁴⁹ J\n5,53 × 10⁻⁴⁹ J < 4,5 × 10⁻¹⁹ J, so UV-B does not damage DNA",  # divided
        "E = hf\n= 6,63 × 10⁻³⁴ × 1,2 × 10⁻¹⁵\n= 7,96 × 10⁻⁴⁹ J\n7,96 × 10⁻⁴⁹ J < 4,5 × 10⁻¹⁹ J, so UV-B does not damage DNA"],  # the power's sign
        ["E = hf.", "Compare the photon's energy with 4,5 × 10⁻¹⁹ J."]),
    work("3.2", "A sunscreen claims to absorb ultraviolet radiation with wavelengths as short as 300 nm. Determine if this sunscreen will provide "
         "protection against UV-B.", 4, [
        "c = fλ\n3 × 10⁸ = f × 300 × 10⁻⁹\nf = 1 × 10¹⁵ Hz\n1 × 10¹⁵ Hz < 1,2 × 10¹⁵ Hz: it will NOT protect against UV-B",      # the memo
        "c = fλ\n3 × 10⁸ = f × 300 × 10⁻⁹\nf = 1 × 10¹⁵ Hz\n1 × 10¹⁵ Hz < 1,2 × 10¹⁵ Hz: it WILL protect against UV-B",          # the conclusion reversed
        "c = fλ\n3 × 10⁸ = f × 300\nf = 1 × 10⁶ Hz\n1 × 10⁶ Hz < 1,2 × 10¹⁵ Hz: it will NOT protect against UV-B",                # nm not converted
        "c = {f}/{λ}\n3 × 10⁸ = {f}/{300 × 10⁻⁹}\nf = 90 Hz\n90 Hz < 1,2 × 10¹⁵ Hz: it will NOT protect against UV-B"],          # the equation upside down
        ["Find the highest frequency the sunscreen absorbs.", "Is it as high as UV-B's 1,2 × 10¹⁵ Hz?"])]

# ---- QUESTION 4, the question paper page 7 and the memo page 3 ----
q4 = [
    stmt("4.1", "Write down the principle of charge quantisation in words.", 2,
         ["All charges in the universe consist of an integer multiple of the charge on one electron.",
          "Any charge is a whole number of electron charges."],
         ["Charge can be created or destroyed.", "The total charge of an isolated system stays constant.",
          "Charges of the same sign attract each other.", "A charge can be any fraction of an electron's charge."],
         ["Quantised means it comes in fixed amounts.", "Which basic charge?"], 2),
    work("4.2", "Calculate the number of electrons that were transferred in this process.", 3, [
        "Q = nqₑ\n4 × 10⁻⁶ = n × 1,6 × 10⁻¹⁹\nn = 2,5 × 10¹³",       # the memo
        "Q = nqₑ\n2 × 10⁻⁶ = n × 1,6 × 10⁻¹⁹\nn = 1,25 × 10¹³",      # the final charge, not the change
        "Q = {n}/{qₑ}\n4 × 10⁻⁶ = {n}/{1,6 × 10⁻¹⁹}\nn = 6,4 × 10⁻²⁵",   # upside down
        "Q = nqₑ\n8 × 10⁻⁶ = n × 1,6 × 10⁻¹⁹\nn = 5 × 10¹³"],        # both spheres' changes added
        ["Each sphere's charge changed by 4 × 10⁻⁶ C.", "Q = nqₑ."]),
    work("4.3.1", "Determine the initial charge on sphere Y.", 2, [
        "Q_Y = 2 × 10⁻⁶ + 4 × 10⁻⁶\n= 6 × 10⁻⁶ C",      # the memo
        "Q_Y = 2 × 10⁻⁶ − 4 × 10⁻⁶\n= −2 × 10⁻⁶ C",     # the change's sign
        "Q_Y = 2 × 10⁻⁶ × 2\n= 4 × 10⁻⁶ C",             # doubled
        "Q_Y = 4 × 10⁻⁶ − 2 × 10⁻⁶\n= 2 × 10⁻⁶ C"],     # subtracted the wrong way
        ["Y gained electrons, so its charge went DOWN by 4 × 10⁻⁶ C.", "What did it start at?"]),
    work("4.3.2", "Determine the initial charge on sphere X.", 3, [
        "Q = {Q_X + Q_Y}/{2}\n2 × 10⁻⁶ = {Q_X + 6 × 10⁻⁶}/{2}\nQ_X = −2 × 10⁻⁶ C",       # the memo's working (its answer writes 10⁻⁹, flag)
        "Q = Q_X + Q_Y\n2 × 10⁻⁶ = Q_X + 6 × 10⁻⁶\nQ_X = −4 × 10⁻⁶ C",                  # not shared
        "Q = {Q_X + Q_Y}/{2}\n2 × 10⁻⁶ = {Q_X + 6 × 10⁻⁶}/{2}\nQ_X = 2 × 10⁻⁶ C",          # the sign lost
        "Q = {Q_X − Q_Y}/{2}\n2 × 10⁻⁶ = {Q_X − 6 × 10⁻⁶}/{2}\nQ_X = 10 × 10⁻⁶ C"],       # subtracted
        ["Identical spheres share the total charge equally.", "Use Q_Y from 4.3.1."], after=["4.3.1"])]

# ---- QUESTION 5, the question paper page 8 and the memo page 4 ----
q5 = [
    stmt("5.1", "Define the term resistance in words.", 2,
         ["The ratio of the potential difference across a resistor to the current in the resistor.",
          "Resistance = potential difference ÷ current."],
         ["The rate of flow of charge.", "The energy transferred per unit charge.", "The product of current and potential difference.",
          "The power used by a resistor."],
         ["R = V/I.", "Which two quantities?"], 2),
    work("5.2.1", "Determine the reading on ammeter A₁.", 4, [
        "V₆Ω = IR = 0,5 × 6 = 3 V\nV₁₂Ω = 3 V\n3 = I × 12\nI = 0,25 A",         # the memo
        "V₆Ω = IR = 0,5 × 6 = 3 V\nV₁₂Ω = 3 V\n3 = {I}/{12}\nI = 36 A",          # I = V × R
        "V₆Ω = IR = 0,5 × 6 = 3 V\nV₁₂Ω = 18 V\n18 = I × 12\nI = 1,5 A",        # the battery's emf across 12 Ω
        "V₆Ω = IR = 0,5 × 6 = 3 V\nV₁₂Ω = 3 V\nI = 0,5 + 0,25\nI = 0,75 A"],    # the total current
        ["The 6 Ω and 12 Ω resistors are in parallel.", "Same voltage, then I = V/R."]),
    work("5.2.2", "Determine the resistance of resistor Rₓ.", 4, [
        "V_Rx = 18 − 3 = 15 V\nI_Rx = 0,5 + 0,25 = 0,75 A\nRₓ = {V}/{I}\n= {15}/{0,75} = 20 Ω",     # the memo
        "V_Rx = 18 V\nI_Rx = 0,5 + 0,25 = 0,75 A\nRₓ = {V}/{I}\n= {18}/{0,75} = 24 Ω",             # the parallel pair's 3 V ignored
        "V_Rx = 18 − 3 = 15 V\nI_Rx = 0,5 A\nRₓ = {V}/{I}\n= {15}/{0,5} = 30 Ω",                    # one branch's current
        "V_Rx = 18 − 3 = 15 V\nI_Rx = 0,5 + 0,25 = 0,75 A\nRₓ = VI\n= 15 × 0,75 = 11,25 Ω"],         # multiplied
        ["Rₓ is in series with the parallel pair.", "Its current is the sum of the branch currents."], after=["5.2.1"]),
    work("5.2.3", "Determine the energy transferred in the 6 Ω resistor in 3 minutes.", 5, [
        "Q = IΔt = 0,5 × 180 = 90 C\nW = VQ\n= 3 × 90\n= 270 J",       # the memo
        "Q = IΔt = 0,5 × 3 = 1,5 C\nW = VQ\n= 3 × 1,5\n= 4,5 J",       # minutes not converted
        "Q = IΔt = 0,5 × 180 = 90 C\nW = VQ\n= 18 × 90\n= 1 620 J",    # the battery's emf
        "Q = IΔt = 0,5 × 180 = 90 C\nW = {V}/{Q}\n= {3}/{90}\n= 0,03 J"],   # divided
        ["How many seconds are in 3 minutes?", "W = VQ, with V across the 6 Ω resistor."])]

# ---- QUESTION 6, the question paper pages 9-10 and the memo page 5 ----
q61 = [
    stmt("6.1.1", "Define the term displacement in words.", 2,
         ["The difference in position in space.", "The change in position, with its direction."],
         ["The total length of the path travelled.", "The rate of change of position.", "The speed in a given direction.",
          "The time taken to move."],
         ["Displacement is a vector.", "Start to end, in a straight line."], 2),
    answer("6.1.2", "Write down the position of the player relative to the halfway line after the first 6 seconds.", 1,
           ["20 m west", "30 m west", "40 m west", "20 m east"], ["He starts 10 m east of the halfway line.", "He runs 30 m west."]),
    work("6.1.3", "Determine the average velocity of the player for the entire motion.", 4, [
        "Δx = 30 − 15 + 25 = 40 m west\nv = {Δx}/{Δt}\n= {40}/{14}\n= 2,86 m·s⁻¹ west",        # the memo
        "Δx = 30 + 15 + 25 = 70 m\nv = {Δx}/{Δt}\n= {70}/{14}\n= 5 m·s⁻¹ west",                # the distance for the displacement
        "Δx = 30 − 15 + 25 = 40 m west\nv = {Δx}/{Δt}\n= {40}/{11}\n= 3,64 m·s⁻¹ west",        # the 3 s tackle left out
        "Δx = 30 − 15 + 25 = 40 m west\nv = Δx × Δt\n= 40 × 14\n= 560 m·s⁻¹ west"],            # multiplied
        ["West is positive here: the tackle pushes him back east.", "Total time 6 + 3 + 5 s."]),
    stmt("6.1.4", "Is the average speed for the entire motion GREATER THAN, LESS THAN or EQUAL TO the average velocity? Explain the answer.", 3,
         ["GREATER THAN", "The player changes direction (he is pushed east).", "So the distance is greater than the displacement."],
         ["LESS THAN", "EQUAL TO", "The player moves in one direction only."],
         ["Speed uses distance; velocity uses displacement.", "Did he double back?"], 1, after=["6.1.3"])]
q62 = [
    work("6.2.1", "Determine the distance covered by the player for the first 13 seconds.", 4, [
        "Δx = ½ × 4 × 8 + 6 × 8 + ½ × 3 × 8\n= 16 + 48 + 12\nDistance = 76 m",       # the memo
        "Δx = 4 × 8 + 6 × 8 + 3 × 8\n= 32 + 48 + 24\nDistance = 104 m",               # the triangles as rectangles
        "Δx = ½ × 4 × 8 + 10 × 8 + ½ × 3 × 8\n= 16 + 80 + 12\nDistance = 108 m",     # the flat part from 0 s
        "Δx = ½ × 13 × 8\n= 52\nDistance = 52 m"],                                   # one triangle
        ["The area under a velocity-time graph is the displacement.", "Split it into a triangle, a rectangle and a triangle."]),
    work("6.2.2", "The player is tackled at 13 seconds and is pushed eastwards at a constant acceleration of −0,5 m·s⁻² for 4 seconds. Using the "
         "graph only (no equations of motion), determine the displacement of the player over the entire 17 seconds.", 5, [
        "−0,5 = {Z − 0}/{17 − 13}\nZ = −2 m·s⁻¹\nΔx₁₃₋₁₇ = ½ × 4 × (−2) = −4 m\nΔx = 76 − 4\n= 72 m west",      # the memo
        "−0,5 = {Z − 0}/{17 − 13}\nZ = −2 m·s⁻¹\nΔx₁₃₋₁₇ = ½ × 4 × (−2) = −4 m\nΔx = 76 + 4\n= 80 m west",      # the negative area added
        "−0,5 = {Z − 0}/{17 − 13}\nZ = −2 m·s⁻¹\nΔx₁₃₋₁₇ = 4 × (−2) = −8 m\nΔx = 76 − 8\n= 68 m west",          # the triangle as a rectangle
        "−0,5 = {Z − 0}/{17}\nZ = −8,5 m·s⁻¹\nΔx₁₃₋₁₇ = ½ × 4 × (−8,5) = −17 m\nΔx = 76 − 17\n= 59 m west"],   # Δt as 17 s
        ["Find Z from the gradient (the acceleration).", "Area below the time axis is negative displacement."], after=["6.2.1"])]

# ---- QUESTION 7, the question paper page 11 and the memo page 6 ----
q7 = [
    stmt("7.1", "Define the term acceleration in words.", 2,
         ["The rate of change of velocity.", "The change in velocity per unit time."],
         ["The rate of change of position.", "The change in speed over a distance.", "The total distance per total time.",
          "The force per unit mass."],
         ["Acceleration changes which quantity?", "Rate means per unit time."], 2),
    work("7.2", "Calculate the time taken for the car to reach a maximum velocity of 50 m·s⁻¹ east.", 3, [
        "vf = vi + aΔt\n50 = 0 + 4Δt\nΔt = 12,5 s",       # the memo
        "vf = vi + aΔt\n50 = 20 + 4Δt\nΔt = 7,5 s",       # the train's speed as vi
        "vf = vi + aΔt\n50 = 0 + 4Δt\nΔt = 200 s",        # multiplied
        "vf = vi + aΔt\n0 = 50 + 4Δt\nΔt = −12,5 s"],     # vi and vf swapped
        ["The car starts from rest.", "vf = vi + aΔt."]),
    work("7.3", "Determine the distance between the front of the train and the car when the car reaches maximum velocity.", 5, [
        "Car: Δx = viΔt + ½aΔt² = ½(4)(12,5²) = 312,5 m\nTrain: Δx = vΔt = (20)(12,5) = 250 m\nDistance = 250 + 180 − 312,5\n= 117,5 m",   # the memo
        "Car: Δx = viΔt + ½aΔt² = ½(4)(12,5²) = 312,5 m\nTrain: Δx = vΔt = (20)(12,5) = 250 m\nDistance = 312,5 − 250\n= 62,5 m",          # the train's length ignored
        "Car: Δx = viΔt + ½aΔt² = (4)(12,5²) = 625 m\nTrain: Δx = vΔt = (20)(12,5) = 250 m\nDistance = 625 − (250 + 180)\n= 195 m",        # the ½ left out
        "Car: Δx = vΔt = (50)(12,5) = 625 m\nTrain: Δx = vΔt = (20)(12,5) = 250 m\nDistance = 625 − (250 + 180)\n= 195 m"],                # top speed the whole time
        ["How far does each travel in 12,5 s?", "The front of the train starts 180 m ahead of the car."], after=["7.2"])]

# ---- QUESTION 8, the question paper page 12 and the memo page 6 ----
q8 = [
    work("8.1", "Calculate the mechanical energy of the stone.", 3, [
        "E = mgh + ½mv²\n= 0,5 × 9,8 × 50 + ½ × 0,5 × 12²\n= 281 J",       # the memo
        "E = mgh\n= 0,5 × 9,8 × 50\n= 245 J",                               # the kinetic energy left out
        "E = mgh + ½mv²\n= 0,5 × 9,8 × 50 + ½ × 0,5 × 12\n= 248 J",        # v not squared
        "E = mgh + ½mv²\n= 0,5 × 9,8 × 20 + ½ × 0,5 × 12²\n= 134 J"],      # the window's height
        ["The stone has both height and speed at the top.", "E = Ep + Ek."]),
    work("8.2.1", "Determine the gravitational potential energy of the stone at the bottom of the window.", 3, [
        "Ep = mgh\n= 0,5 × 9,8 × 30\n= 147 J",     # the memo
        "Ep = mgh\n= 0,5 × 9,8 × 20\n= 98 J",      # 20 m below the top used as the height
        "Ep = mgh\n= 0,5 × 9,8 × 50\n= 245 J",     # the top's height
        "Ep = mg\n= 0,5 × 9,8\n= 4,9 J"],          # no height
        ["The window's bottom is 20 m below the top of a 50 m building.", "How high is it above the ground?"]),
    work("8.2.2", "Determine the speed of the stone at the bottom of the window.", 4, [
        "Ek = 281 − 147 = 134 J\nEk = ½mv²\n134 = ½ × 0,5 × v²\nv = 23,15 m·s⁻¹",     # the memo
        "Ek = 281 − 147 = 134 J\nEk = ½mv²\n134 = 0,5 × v²\nv = 16,37 m·s⁻¹",         # the ½ left out
        "Ek = 281 + 147 = 428 J\nEk = ½mv²\n428 = ½ × 0,5 × v²\nv = 41,38 m·s⁻¹",     # added
        "Ek = 281 − 147 = 134 J\nEk = ½mv²\n134 = ½ × 0,5 × v\nv = 536 m·s⁻¹"],       # v not squared
        ["Mechanical energy is conserved.", "Ek = E − Ep."], after=["8.1", "8.2.1"])]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Multiple choice", "marks": 10, "items": q1},
    {"id": "2.1", "title": "Question 2.1", "kind": "Waves", "marks": 11,
     "lead": "During an earthquake, seismic waves travel through the earth's crust. In a type of seismic wave, called p-waves, the particles in "
             "the medium move back and forth in the same direction that the wave travels. A seismic station located 300 km from the epicentre of "
             "an earthquake detects the first wave 45 seconds after the start of the earthquake. The measured wavelength of the seismic wave is "
             "3 600 m.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Sound", "marks": 7,
     "lead": "An earthquake produces a loud sound, of frequency 490 Hz, that travels through the air. A town lies 6 500 m east of the earthquake's "
             "epicentre, and the sound wave from the earthquake reaches the town in 19 seconds. The speed of sound in air does not change between "
             "the epicentre and the town.",
     "figure": P.fig("2.2", "The earthquake's epicentre on the left and a town 6 500 m to the east, with a compass."), "items": q22},
    {"id": "3", "title": "Question 3", "kind": "Electromagnetic radiation", "marks": 8,
     "lead": "Sunscreens contain ingredients that absorb ultraviolet (UV) radiation before it damages skin cells. A photon of ultraviolet "
             "radiation, UV-B, has a maximum frequency of 1,2 × 10¹⁵ Hz. Photon energies of at least 4,5 × 10⁻¹⁹ J result in damage to DNA.",
     "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Electrostatics", "marks": 10,
     "lead": "Two identical conducting spheres X and Y are placed on insulating stands. The charge on both spheres is unknown. The spheres are "
             "allowed to touch, resulting in ELECTRONS MOVING FROM SPHERE X TO Y, and are then separated. After separation:\n• Each sphere now "
             "carries a charge of 2 × 10⁻⁶ C.\n• The charge on each sphere changed by 4 × 10⁻⁶ C.",
     "figure": P.fig("Q4", "Two identical spheres X and Y on insulating stands on a bench."), "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Electric circuits", "marks": 15,
     "lead": "A battery with an emf of 18 V is connected to four resistors as shown in the circuit diagram below. The connecting wires and the "
             "battery have negligible resistance. 0,5 A of current passes through the 6 Ω resistor.",
     "figure": P.fig("Q5", "An 18 V battery with a 15 Ω resistor and an open switch S in one branch, and in the other branch a 6 Ω resistor in "
                           "parallel with a 12 Ω resistor and ammeter A₁, in series with Rₓ; 0,5 A in the 6 Ω resistor."), "items": q5},
    {"id": "6.1", "title": "Question 6.1", "kind": "Motion in one dimension", "marks": 10,
     "lead": "A rugby player catches the ball at point A, 10 m east of the halfway line on a standard 100 m pitch. The halfway line is on the 50 m "
             "mark. The player then performs the following sequence of movements along a straight line:\n• Runs 30 m westwards, towards the "
             "opponents' try line, in 6 seconds.\n• Gets tackled and is pushed 15 m eastwards in 3 seconds.\n• Recovers and sprints 25 m westward "
             "in 5 seconds, before passing the ball.",
     "figure": P.fig("6.1", "A 100 m rugby pitch, the opponents' try line on the west, the halfway line at 50 m and point A 10 m east of it."),
     "items": q61},
    {"id": "6.2", "title": "Question 6.2", "kind": "Motion graphs", "marks": 9,
     "lead": "In a different play the rugby player, starting from rest, runs towards the opponents' try line, due west of his initial position, "
             "along a straight line. His motion is shown in the velocity-time graph (not drawn to scale) below.",
     "figure": P.fig("6.2", "A velocity-time graph: velocity rises from 0 to 8 m·s⁻¹ at 4 s, stays at 8 m·s⁻¹ until 10 s, falls to 0 at 13 s, "
                            "then falls below the axis to Z at 17 s."), "items": q62},
    {"id": "7", "title": "Question 7", "kind": "Equations of motion", "marks": 10,
     "lead": "A train of length 180 m is moving at a constant velocity of 20 m·s⁻¹ east. A car parked alongside the train takes off from rest "
             "when the front of the car is in line with the back of the train. The car also travels due east and accelerates uniformly at "
             "4 m·s⁻² to reach a maximum speed of 50 m·s⁻¹.",
     "figure": P.fig("Q7", "A 180 m train moving east at 20 m·s⁻¹, and a car at rest level with the back of the train."), "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Mechanical energy", "marks": 10,
     "lead": "A 0,5 kg stone is thrown vertically downward at 12 m·s⁻¹ from the top of a 50 m high building. The bottom of a window is located "
             "20 m below the top of the building, as shown in the diagram. Ignore the effects of air friction.",
     "figure": P.fig("Q8", "A 50 m building with a window whose bottom is 20 m below the top; a stone thrown down at 12 m·s⁻¹ from the top."),
     "items": q8}]

P.finish(missions,
         {"subject": "Physical Sciences", "title": "Physical Sciences P1 (Physics)", "sitting": "November 2025", "total_marks": 100,
          "time": "2 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "4.3.2", "kind": "memo_issue", "detail": "The memo's working is 2 × 10⁻⁶ = (Q_X + 6 × 10⁻⁶)/2, then it writes Q_X = −2 × 10⁻⁹ C; "
                                                         "the working gives −2 × 10⁻⁶ C (X lost electrons: from −2 μC to +2 μC, a change of "
                                                         "4 μC). The right option is −2 × 10⁻⁶ C."}],
         {"1": 10, "2": 18, "3": 8, "4": 10, "5": 15, "6": 19, "7": 10, "8": 10}, 100,
         {"2.1.2(b)": ["2.1.2(a)"], "2.1.3": ["2.1.2(b)"], "4.3.2": ["4.3.1"], "5.2.2": ["5.2.1"], "6.1.4": ["6.1.3"], "6.2.2": ["6.2.1"],
          "7.3": ["7.2"], "8.2.2": ["8.1", "8.2.1"]},
         "Questions 1 to 8 (the whole paper)")
