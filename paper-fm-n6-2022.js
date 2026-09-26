// Fluid Mechanics N6 · November 2022 (DHET, National Certificate) — transcribed from the
// question paper. Numbering, marks and section totals are the paper's own.
//
// ⚠ NO MEMO WAS PUBLISHED WITH THIS PAPER.
// Every numeric answer in an N6 paper depends on the marking guideline's rounding, its
// accepted formula route and its method marks. Inventing those would mark a student wrong
// for being right, so no calculation here carries a "correct answer". Instead each one
// self-marks against its METHOD — the steps the mark allocation implies — which is the same
// pattern the app already uses for extended writing. `methodOnly: true` is what the UI reads
// to say so. The three definitions and the turbine-naming question are textbook recall and
// are marked normally.
//
// Replace with memo-marked answers the moment DHET publishes the marking guideline.
window.PAPER_FM_N6_2022 = {
  id: "fm-n6-2022", subject: "Mechanical Engineering",
  offering: "Fluid Mechanics", paper: "N6", sitting: "November 2022",
  board: "DHET · National Certificate", code: "8190216", total: 100, time: "3 hours",
  methodOnly: true,
  memoNote: "DHET has not published a marking guideline for this sitting. Calculations are marked against method, not against a memo answer.",
  sections: [
    { id: "1", title: "Question 1", total: 27, missions: [

      { id: "1.1", title: "Question 1.1", kind: "Pipeline between reservoirs", marks: 6, items: [
        { n: "1.1.1", t: "rubric", marks: 3, methodOnly: true,
          q: "A pipeline 720 m long connects a new and an existing reservoir with a 8 m difference in level. The pipeline rises 3 m above the upper reservoir at 260 m from the entrance, then falls to the new lower reservoir. The pipe is 1,2 m in diameter with a coefficient of 0,01. Ignore shock losses. Determine the discharge.",
          bullets: ["Apply the Darcy friction formula hf = 4fLV²/(2gd) with hf = 8 m", "Substitute f = 0,01, L = 720 m, d = 1,2 m and solve for V", "Q = A × V, with A = πd²/4"],
          clues: ["The whole 8 m difference in level is consumed by friction — shock losses are ignored.", "Darcy gives you V; the area gives you Q."] },
        { n: "1.1.2", t: "rubric", marks: 3, methodOnly: true,
          q: "Determine the pressure at the highest point of the pipeline. Atmospheric pressure may be taken as 101,3 kPa.",
          bullets: ["Find the friction head over the first 260 m at the velocity from 1.1.1", "Apply Bernoulli between the upper reservoir surface and the summit, 3 m above it", "Convert the resulting head to pressure and subtract from atmospheric"],
          clues: ["The summit sits 3 m ABOVE the supply reservoir, so the pressure there is below atmospheric.", "Only the first 260 m of pipe has produced friction by that point."] }
      ] },

      { id: "1.2", title: "Question 1.2", kind: "Pressure difference", marks: 6, items: [
        { n: "1.2", t: "rubric", marks: 6, methodOnly: true,
          q: "Calculate the pressure difference in a horizontally placed pipeline. The large diameter section is 300 mm, the small diameter section is 100 mm, and the quantity is 180 m³ of water per hour. Flow is from the smaller to the bigger section. Ignore ALL losses.",
          bullets: ["Convert 180 m³/h to m³/s", "Find V₁ and V₂ from Q = AV at each diameter", "Apply Bernoulli with Z₁ = Z₂ (horizontal) and no loss term", "Express the head difference as a pressure in kPa"],
          clues: ["Horizontal means the elevation terms cancel — only the velocity heads differ.", "Flow from small to large means it slows down, so pressure rises."] }
      ] },

      { id: "1.3", title: "Question 1.3", kind: "Pipes in parallel", marks: 6, items: [
        { n: "1.3", t: "rubric", marks: 6, methodOnly: true,
          q: "Two water tanks are connected by three pipes of diameters d, 2d and 3d, laid in parallel. The three pipes have the same length and coefficient of friction f. If the smallest pipe discharges 88 ℓ/s, calculate the discharge through each of the other TWO pipes in litres per second.",
          bullets: ["Parallel pipes share the same head loss, so hf is equal for all three", "From hf = 4fLV²/(2gd) with hf, f and L fixed, show Q ∝ d^2,5", "Apply the ratio to 88 ℓ/s for 2d and for 3d"],
          clues: ["Equal head loss is what makes them comparable — that is what 'parallel' buys you.", "Work out the power of d that Q follows before substituting any numbers."] }
      ] },

      { id: "1.4", title: "Question 1.4", kind: "Stand pipes on a main", marks: 9,
        fig: "FIGURE 1 — pipe AC, 2,5 km long and 900 mm in diameter, with stand pipes connected to the main",
        items: [
        { n: "1.4.1", t: "rubric", marks: 1, methodOnly: true,
          q: "FIGURE 1 shows a pipe AC, 2,5 km long and 900 mm in diameter carrying non-flowing water, with stand pipes connected to the main. Determine the friction head.",
          bullets: ["Read the difference in stand-pipe levels from the figure"],
          clues: ["With the water not flowing there is no friction yet — the figure gives you the head directly."] },
        { n: "1.4.2", t: "rubric", marks: 2, methodOnly: true,
          q: "Determine the hydraulic gradient.",
          bullets: ["i = hf / L", "Use L = 2,5 km in metres"],
          clues: ["The hydraulic gradient is a slope: head lost per metre of pipe."] },
        { n: "1.4.3", t: "num", marks: 2, a: 0.225, unit: "m", tol: 0.002, methodOnly: true,
          q: "Calculate the hydraulic mean depth of the pipe.",
          bullets: ["m = A / P = d / 4 for a circular pipe running full"],
          clues: ["For a full circular pipe the hydraulic mean depth is simply the diameter over four."] },
        { n: "1.4.4", t: "rubric", marks: 2, methodOnly: true,
          q: "Determine the friction factor if a new and clean pipe is used.",
          bullets: ["Select the friction factor for a new, clean pipe from the standard table", "State the value used"],
          clues: ["This is a table value, not a calculation — the paper expects the standard figure for new clean pipe."] },
        { n: "1.4.5", t: "rubric", marks: 2, methodOnly: true,
          q: "Hence, calculate the velocity of water if it starts flowing upwards.",
          bullets: ["Substitute hf, f, L and d into hf = 4fLV²/(2gd)", "Solve for V"],
          clues: ["Everything you need is now known — rearrange Darcy for V."] }
      ] }
    ] },

    { id: "2", title: "Question 2", total: 21, missions: [

      { id: "2.1", title: "Question 2.1", kind: "V-notch", marks: 4, items: [
        { n: "2.1", t: "rubric", marks: 4, methodOnly: true,
          q: "V-notches are used to determine flow in streams and small rivers. A V-notch must be designed for a maximum flow of 860 litres per second. The 90° V-notch has a coefficient of discharge of 0,98. Calculate a suitable height (in mm) for this V-notch to handle that maximum flow.",
          bullets: ["Use Q = (8/15)·Cd·√(2g)·tan(θ/2)·H^2,5 from the formula sheet", "Substitute θ/2 = 45°, so tan(θ/2) = 1", "Solve for H and convert to mm"],
          clues: ["A 90° notch makes the tangent term equal to one, which simplifies the substitution.", "Convert 860 ℓ/s to m³/s before substituting."] }
      ] },

      { id: "2.2", title: "Question 2.2", kind: "Jet from an orifice", marks: 9, items: [
        { n: "2.2.1", t: "rubric", marks: 4, methodOnly: true,
          q: "A jet of water issues from an orifice in a vertical wall. The orifice has a diameter of 60 mm and discharges 2 m below the surface. The jet strikes the ground 4,2 m horizontally from the opening. The coefficient of velocity is 0,98. Calculate the time taken for the jet to strike the surface level.",
          bullets: ["Treat the fall as projectile motion: y = ½gt²", "Substitute y = 2 m and g = 9,81 m/s²", "Solve for t"],
          clues: ["The horizontal distance plays no part in the fall time — only the drop does.", "This is the vertical component only."] },
        { n: "2.2.2", t: "rubric", marks: 2, methodOnly: true,
          q: "Calculate the head of water above the orifice.",
          bullets: ["Find the actual velocity from V = x / t", "Use H = V² / (Cv²·2g) to recover the head"],
          clues: ["The horizontal distance and the time you just found give the actual jet velocity.", "Cv relates actual velocity to the theoretical velocity the head would produce."] },
        { n: "2.2.3", t: "rubric", marks: 3, methodOnly: true,
          q: "Calculate the theoretical discharge in ℓ/s.",
          bullets: ["Theoretical velocity Vt = √(2gH)", "A = πd²/4 with d = 60 mm", "Q = A·Vt, converted to ℓ/s"],
          clues: ["Theoretical means no coefficient applied — use the head directly.", "Watch the units: 60 mm is 0,06 m."] }
      ] },

      { id: "2.3", title: "Question 2.3", kind: "Mine ventilation branches", marks: 8, items: [
        { n: "2.3", t: "rubric", marks: 8, methodOnly: true,
          q: "At a colliery plant, 25 m³/s of air is pumped into a section which splits into two branches at the same point. Branch A: length 110 m, width 800 mm, height 950 mm. Branch B: length 75 m, diameter 800 mm. Calculate the quantity of air delivered by each branch. Assume equal values for k and that each branch discharges into areas having the same pressure.",
          bullets: ["Find the area and perimeter of each branch", "Both branches discharge to the same pressure, so the pressure drop is equal", "Use Pr = kSV²/a with equal k and equal Pr to relate Q_A and Q_B", "Apply Q_A + Q_B = 25 m³/s and solve the pair"],
          clues: ["Equal discharge pressure is what makes the two branches comparable — it fixes their pressure drops equal.", "Branch A is rectangular and branch B is circular, so their areas and rubbing surfaces are found differently."] }
      ] }
    ] },

    { id: "3", title: "Question 3", total: 23, missions: [

      { id: "3.1", title: "Question 3.1", kind: "Centrifugal pump", marks: 14, items: [
        { n: "3.1.1", t: "rubric", marks: 2, methodOnly: true,
          q: "A single-stage centrifugal pump operating at 1 500 r/min delivers 300 m³ of water per hour against a total head of 10 m at an efficiency of 85%. The impeller has an outer diameter of 210 mm and the width of the flow passages at outlet is 60 mm. Calculate the peripheral velocity of the impeller at outlet.",
          bullets: ["u = πDN/60", "Substitute D = 0,21 m and N = 1 500 r/min"],
          clues: ["Peripheral velocity is the rim speed — circumference times revolutions per second."] },
        { n: "3.1.2", t: "rubric", marks: 3, methodOnly: true,
          q: "Calculate the radial (flow) velocity of the water leaving the impeller.",
          bullets: ["Convert 300 m³/h to m³/s", "Outlet flow area = πD × width", "Vf = Q / area"],
          clues: ["The flow leaves through the cylindrical band at the impeller rim, not through a circle."] },
        { n: "3.1.3", t: "rubric", marks: 2, methodOnly: true,
          q: "Calculate the tangential (whirl) velocity of the water leaving the impeller.",
          bullets: ["Manometric efficiency relates head to whirl: h = ηm·u·Vw / g", "Rearrange for Vw using the 85% efficiency and the 10 m head"],
          clues: ["The whirl component is what actually does the work on the water."] },
        { n: "3.1.4", t: "rubric", marks: 3, methodOnly: true,
          q: "Calculate the outlet angle of the impeller vane.",
          bullets: ["tan β = Vf / (u − Vw)", "Substitute the three velocities already found", "State the angle in degrees"],
          clues: ["The vane angle comes from the outlet velocity triangle — flow velocity against the difference between rim and whirl speed."] },
        { n: "3.1.5", t: "rubric", marks: 2, methodOnly: true,
          q: "Calculate the output power of the motor driving the pump if the mechanical efficiency is 82%.",
          bullets: ["Water power = ρ·g·Q·H", "Divide by the pump efficiency, then by the mechanical efficiency"],
          clues: ["Work outwards from the water: each efficiency divides the power up the chain."] },
        { n: "3.1.6", t: "rubric", marks: 2, methodOnly: true,
          q: "Calculate the speed at which flow will commence when the pump is started against a static head of 7 m. Use N = 60√(2ghs) / (πDo).",
          bullets: ["Substitute hs = 7 m and Do = 0,21 m into the given formula", "Evaluate N in r/min"],
          clues: ["The formula is supplied — this is a substitution, not a derivation."] }
      ] },

      { id: "3.2", title: "Question 3.2", kind: "Three-throw pump", marks: 6, items: [
        { n: "3.2.1", t: "rubric", marks: 4, methodOnly: true,
          q: "A three-throw pump has a stroke of 400 mm, a bore of 150 mm, a crank speed of 50 r/min, a head of 900 m, a slip of 5% and an efficiency of 92%. Determine the actual delivery.",
          bullets: ["Q = ALSN/60 with three cylinders", "A = πd²/4 with d = 0,15 m; L = 0,4 m; N = 50 r/min", "Reduce the theoretical delivery by the 5% slip"],
          clues: ["Three-throw means three cylinders — the formula sheet's ALSEN/60 accounts for that.", "Slip reduces the delivery below theoretical."] },
        { n: "3.2.2", t: "rubric", marks: 2, methodOnly: true,
          q: "Determine the power required.",
          bullets: ["P = ρ·g·Q·H using the actual delivery", "Divide by the 92% efficiency"],
          clues: ["Use the actual delivery from 3.2.1, not the theoretical one."] }
      ] },

      { id: "3.3", title: "Question 3.3", kind: "Definitions", marks: 3, items: [
        { n: "3.3.1", t: "rubric", marks: 1,
          q: "Define the following term: Water hammer",
          bullets: ["The pressure surge caused when a flowing liquid is suddenly stopped or its velocity abruptly changed, e.g. by rapid valve closure"],
          clues: ["Think about what happens to moving water when a valve slams shut."] },
        { n: "3.3.2", t: "rubric", marks: 1,
          q: "Define the following term: Cavitation",
          bullets: ["The formation and collapse of vapour bubbles when local pressure falls below the vapour pressure of the liquid, causing damage to the surfaces"],
          clues: ["It begins when the pressure drops far enough for the liquid to boil at ordinary temperature."] },
        { n: "3.3.3", t: "rubric", marks: 1,
          q: "Define the following term: Piston pump",
          bullets: ["A positive-displacement reciprocating pump in which a piston moving in a cylinder draws in and discharges a fixed volume of liquid each stroke"],
          clues: ["Positive displacement — a fixed volume per stroke, unlike a centrifugal pump."] }
      ] }
    ] },

    { id: "4", title: "Question 4", total: 29, missions: [

      { id: "4.1", title: "Question 4.1", kind: "Pelton wheel", marks: 16, items: [
        { n: "4.1.1", t: "rubric", marks: 3, methodOnly: true,
          q: "The pipeline supplying a triple-jet Pelton wheel is 3 km long. The water height of the reservoir above the wheel is 500 m. The turbine develops 7 000 kW at 500 r/min. Pipeline losses are 15% of the gross head and the friction factor is 0,005. Take the coefficient of velocity of the jets as 0,97, the bucket speed as 0,45 of the jet speed and the turbine efficiency as 92%. Calculate the velocity of water entering the buckets.",
          bullets: ["Net head = gross head − 15% losses", "V = Cv·√(2gH) using the net head", "State the jet velocity in m/s"],
          clues: ["Take the losses off the 500 m before applying the velocity formula.", "Cv accounts for the nozzle not being ideal."] },
        { n: "4.1.2", t: "rubric", marks: 3, methodOnly: true,
          q: "Calculate the mean diameter of the wheel.",
          bullets: ["Bucket speed u = 0,45 × jet velocity", "u = πDN/60 with N = 500 r/min", "Rearrange for D"],
          clues: ["The bucket speed ratio gives you u; the rotational speed then gives you the diameter."] },
        { n: "4.1.3", t: "rubric", marks: 7, methodOnly: true,
          q: "Calculate the diameter of a jet.",
          bullets: ["Find the water power required from the 7 000 kW output and the 92% efficiency", "Q = P / (ρ·g·H) using the net head", "Divide by three — the wheel is triple-jet", "A = Q/V per jet, then d = √(4A/π)"],
          clues: ["Triple-jet means the total discharge is shared three ways before you size one nozzle.", "Work back from the power to the flow, then from the flow to the area."] },
        { n: "4.1.4", t: "rubric", marks: 3, methodOnly: true,
          q: "Calculate the diameter of the supply pipe if f = 0,007 and the length of the supply pipe is 1,5 km.",
          bullets: ["The allowable friction head is the 15% loss", "Express V in terms of d from Q = AV", "Substitute into hf = 4fLV²/(2gd) and solve for d"],
          clues: ["The loss you already used as a head is now the constraint that sizes the pipe.", "Both V and the area depend on d, so substitute before solving."] }
      ] },

      { id: "4.2", title: "Question 4.2", kind: "Reaction turbines", marks: 4, items: [
        { n: "4.2", t: "list", marks: 4,
          q: "Reaction turbines can be classified with respect to the direction of the water flow. Name FOUR types of reaction turbine.",
          pool: ["radial flow", "axial flow", "mixed flow", "tangential flow"], count: 4,
          clues: ["The classification is by the direction the water takes through the runner.", "Radial splits into two — inward and outward."] }
      ] },

      { id: "4.3", title: "Question 4.3", kind: "Francis turbine", marks: 9, items: [
        { n: "4.3.1", t: "rubric", marks: 7, methodOnly: true,
          q: "A vertical-shaft Francis turbine is supplied with water at 22,5 m³/min. The inlet pressure is 196 kPa and the inlet diameter is 0,7 m. The pressure at the tail-water end is −28 kPa and that diameter is 1,3 m. The vertical height between the two points is 2,5 m. Calculate the effective turbine pressure head.",
          bullets: ["Convert 22,5 m³/min to m³/s", "Find V₁ and V₂ from Q = AV at each diameter", "Convert both pressures to head (p/ρg), keeping the sign on −28 kPa", "Apply Bernoulli between inlet and tail-water including the 2,5 m elevation", "State the effective head"],
          clues: ["The negative tail-water pressure is below atmospheric — carry the sign through.", "All three terms matter here: pressure, velocity and elevation."] },
        { n: "4.3.2", t: "rubric", marks: 2, methodOnly: true,
          q: "Calculate the input power supplied to the turbine.",
          bullets: ["P = ρ·g·Q·H using the effective head from 4.3.1", "State the power in kW"],
          clues: ["Input power uses the head the water actually delivers to the machine."] }
      ] }
    ] }
  ]
};
