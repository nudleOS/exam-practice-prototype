# Claude Design prompt — Exam Missions learner UI (platform `/exams`)

Paste everything below the line into Claude Design, in the SAME project that holds `Exam Missions.dc.html`
(attach it if it is a new project). It asks for a refinement of that design wired to the live service's
real data, so the approved export can be ported without guesswork.

---

Refine the existing **Exam Missions** design (`Exam Missions.dc.html`) into the learner exam-practice UI that
will live on the Nexera platform at `/exams`. Keep its look and feel: the dark charcoal game skin, Sora,
glass pills, the vertical road of spheres with grade rings, the brand gradient only on the one primary action
per screen, spring motion, the companion. Change BEHAVIOUR where listed below — the backend is now built and
its rules are fixed. Do not redesign it into something else.

## Who and where
South African TVET learners practising for national exams, mostly on low-end Android phones on prepaid data.
Design **phone 360 px first**, then tablet 768 px and desktop 1280 px. English is most learners' second
language: plain words, short sentences, no idioms.

## The two real papers (use them, do not invent others)
1. **Fluid Mechanics N6 · November 2022 · NATED (DHET) · 100 marks · 3 hours** — 32 parts in 13 missions:
   Pipeline over a summit between two reservoirs (6 marks, 2 parts) · Pressure difference in a horizontal pipe (6) ·
   Three pipes in parallel (6) · Stand pipes on pipe AC — FIGURE 1 (9, 5 parts) · Sizing a 90° V-notch (4) ·
   Jet from an orifice in a vertical wall (9) · Splitting mine ventilation air between two branches (8) ·
   Single-stage centrifugal pump (14, 6 parts) · Three-throw pump (6) · Definitions (3) · Triple-jet Pelton wheel (16) ·
   Classifying reaction turbines (4) · Vertical-shaft Francis turbine (9). Almost every mark is a calculation
   marked per method step. It has FIGURE 1, a data table and a 3-page formula sheet.
2. **Applied Engineering Technology · NC(V) Level 4 · February 2019 · 100 marks · 3 hours** — 28 parts: method-marked
   calculations, short written answers, lists, a 10-item **matching columns** question (Column A terms → Column B
   descriptions, 11 descriptions, one is a decoy) and two drawings to scale (not marked online).
Provenance label shown for both: "DHET question paper · marking reviewed by Nexera".

## Screens to design (the Monday demo scope)
1. **Pick a paper** — the two papers as cards: title, programme and level, sitting, marks, time, parts, provenance
   label; "Start practising" / "Continue". Honest empty state for any other subject: "No paper available yet."
2. **Paper map** — the road, bottom-up, sections as capsules ("QUESTION 1 · 27 MARKS"), one sphere per mission,
   named "⟨number⟩ · ⟨mission title⟩" with "⟨n⟩ parts · ⟨m⟩ marks" and asset tags ("FIGURE 1"). **No locks** —
   every mission is open. States: not started · suggested · in progress · closed with grade ring (gold "Clean run",
   silver "With hints", bronze "Memo shown") · "1 waiting for a marker". Header: marks earned of 100 meter, XP pill,
   "Paper kit" (instructions, formula sheet, figures).
3. **Mission play**, one part at a time, with the mission's shared context pinned above, the part number and
   marks, "Try ⟨n⟩ of 3", and a **Check** primary. One screen per response family:
   - **Method steps** (most of FM): one input card per step, each with its label and marks, a value field and the
     unit shown ("m/s"). Chips for the paper's rules ("Round to THREE decimal places", "g = 9,81 m/s²") and a
     "Formula sheet" drawer. Decimal comma accepted — say so. The app never calculates for the learner.
   - **Short term / list** ("Name FOUR types of reaction turbines" — four numbered fields).
   - **Matching columns** (AET 4.2) — tap a Column A item, then its description; one decoy; works by tap only.
   - **Written answer** (e.g. "Define: Cavitation · 1 mark") — a coach line from the question's own wording
     ("The question asks you to Define. It is worth 1 mark."), a textarea, a character count. **No live score, no
     keyword meter, no semantic bar.**
   - **Drawing** (AET 2.1, 2.3) — "Draw it on paper. This one isn't marked online." then the criteria after submit.
4. **Feedback after Check** (inline under the input, never a modal):
   - full marks: "Correct · 3 marks", "+100 XP" flying to the pill (×2, ×3… on a first-try streak);
   - partial: "2 of 3 marks so far" with each step stamped ✓ / ✕ / **"carried forward"** (the learner's earlier
     value used correctly — earns the mark); nothing revealed about what is missing;
   - miss: a hint box ("One down — here is a hint") with the approved hint text;
   - written answers: "Being marked…" (up to ~20 s on the local marker), then per-point results with the learner's
     own words highlighted, and "Marked by AI against the memo";
   - "Your answer is saved and waiting for a marker." when marking is unavailable.
5. **Reveal** (after the third try or "Show the memo") — the examiner's-eye list: each memo point or method step
   with its marks and **where it came from**, per line: "As printed in the guideline", "Corrected by Nexera's
   curriculum team: ⟨why⟩", or "Written by Nexera's curriculum team". Never the word "Official".
6. **Mission complete** — grade, marks, XP, streak, "Next mission" / "Back to the map".
7. **Summary / review** — marks per section, XP, parts closed, and a list of parts below full marks.

## Rules the design must follow (the backend enforces them)
- Learners never mark themselves: **remove the prototype's tick-your-own-answer checklist** completely.
- XP by try: 100 / 60 / 20; a multiplier (×1–×4) only for first-try answers in a row; **no speed bonus**, no timer
  on XP; a question pays XP once ever — a replay shows "Replay — no XP".
- Three tries per part; a hint after each miss; the third miss reveals the memo.
- Answers and memo never appear before a part closes.
- Only the brand three blues (azure `#0068f8`, cobalt `#1e46ff`, violet `#671dff`, gradient
  `linear-gradient(135deg,#0068f8 0%,#1e46ff 50%,#671dff 100%)`) — replace the prototype's `#7ea0ff` with
  `#81b1ff` (a tint of azure). Amber `#e0a10f` is the only warning colour, `#f2777a` the only error colour,
  `#3ddc97` for full marks. No emoji. No new illustrations or statistics that don't exist.
- Accessibility: WCAG 2.2 AA; 44 px targets; visible focus ring; every state readable without colour; respect
  reduced motion (no flights or shakes); Enter in a text field never double-submits; pick/order/match work by tap.

## Data contract — use these EXACT shapes as the sample data in the script block
The learner view of a part (answers are never in it):
```json
{"number":"1.1.1","marks":3,"response_mode":"steps","marking_mode":"method","stem":"The discharge.",
 "topic":"Flow in pipes and hydraulic gradient","clues_available":2,
 "steps":[{"id":"s1","label":"Friction head available between the reservoirs, hf (m)","marks":1,"unit_hint":"m"},
          {"id":"s2","label":"Velocity in the pipe, V (m/s)","marks":1,"unit_hint":"m/s"},
          {"id":"s3","label":"Discharge, Q (m³/s)","marks":1,"unit_hint":"m**3/s"}]}
```
Other `response_mode`s: `num` (`unit_hint`), `term`, `list` (`count`), `mcq`/`pickn`/`order` (`options`),
`lettername` (`letters`), `match` (`match.left[]`, `match.right[]`), `rubric` (written), `draw`.
The mission's shared text is `mission.context` (e.g. "A pipeline, 720 m long, connects the new and existing
reservoirs which have a difference in level of 8 m…").

The reply after Check:
```json
{"part":"1.1.1","try":1,"tries_left":2,"closed":false,"revealed":false,"best_marks":2,
 "result":{"marks_awarded":2,"marks":3,"full":false,"marker":"auto","message":null,
   "items":[{"key":"s1","awarded":1,"available":1,"verdict":"correct"},
            {"key":"s2","awarded":0,"available":1,"verdict":"incorrect"},
            {"key":"s3","awarded":1,"available":1,"verdict":"follow_through",
             "reason":"Correct method with your earlier value carried forward."}]},
 "clue":"With shock losses ignored, the whole difference in level between the reservoirs is used up by pipe friction.",
 "reveal":null,"xp_awarded":0,"multiplier":1,"streak":0}
```
`verdict` ∈ correct · follow_through · incorrect · missing · unreadable (with a `reason` to show) · not_marked_online.
When `closed`, `reveal` holds `steps[]` (label, marks, `memo_text`), or `memo.points[]` (text, marks), plus
`provenance.memo_source` ∈ board · board_corrected · authored and `provenance.note`.

Summary: `{marks_earned, total_marks, percentage, xp_earned, streak, best_streak, sections:[{title, marks, earned}],
parts:[{number, marks, best_marks, tries_used, closed, revealed, first_try_full}]}`.

## Deliver
One `.dc.html` with the screens above as states of one page (like the original), every state reachable from a
control, the sample data above in the script block, phone and desktop layouts, and short notes on anything you
changed from the original and why.
