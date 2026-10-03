# Build prompt 11: teacher class tests, the learner side (the third sitting mode)

**Target:** `C:\Users\mokon\Downloads\3rd design\Exam Practice.dc.html`. The class test reuses the Hall's sitting engine (brief 08) with an assignment and a window.

The **teacher side** (T1–T5 in `design/screens.v2.md` §17) gets its own design file and its own brief (12). It is a calm tool in platform chrome, for a different user, and its screens are already designed.

## The rulings this must obey (decided)
- **R1, setter and moderator.** A class test reaches learners only with a setter and a moderator.
  - A teacher-set paper is moderated by the institution's `institution_admin`, never the setter.
  - A company paper is moderated by Nexera's curriculum team.
  - This is ARCH §9. It **supersedes** screens.v2 §17's "subject head or institution_admin (configurable)", which is stale.
- **R2 (b), class tests:** the institution moderator releases marks **after the window closes**. There is no standing policy, unlike the Hall.
- **§3, assessment mode:**
  - one attempt;
  - no clues;
  - no feedback per question;
  - the memo stays hidden until the window closes and the moderator releases;
  - the recorded mark stands;
  - a `disclosed` version is refused.
- **Refinement 3:** a class test is **not an official ICASS mark**. For a DHET past paper, that's also DHET's own rule (ICASS26:610-612). Every class-test screen carries **"Mock / class test · not an ICASS task"**.
- **Refinement 2:** score-based rewards only for teacher-supervised tests. The design shows the facts; **the platform decides** any reward.
- **R7:** no 3D in the test. **ARCH §7:** the service holds pseudonymous ids only, and the teacher's name comes from the platform BFF.

## What we found (measured in the design, 2026-09-27)
- The Hall's engine already does most of this: the clock, navigator, drafts, flags, autosave, hand-in, statuses, report and fix round (commit 3f2ff74).
- It differs in five places:
  1. The start comes from an **assignment with a window**, not from the learner.
  2. `ends_at` = min(start + duration, window close).
  3. Release happens after the window closes **and** the moderation sample (screens.v2 §17.3).
  4. The learner is told who sees their marks.
  5. A learner can miss the window.
- **A gap the Hall doesn't have:** during the window, a learner could practise the same paper (with hints and the memo) and then sit the test. The Hall's practice lock only covers an open sitting. A class test needs the lock for the **whole window**.

## 1. Where the test appears
- **Home:** a card above the paper ticket, "Set by your teacher". It shows:
  - the paper and its label, "Mock / class test · not an ICASS task";
  - the state line;
  - one action.
- **The map** for that paper: the same card, pinned under the Paper | Topics switch while the test is open.
- **States, and the action for each:**

  | State | Line | Action |
  |---|---|---|
  | Upcoming | "Opens Mon 08:00" | none |
  | Open | "Open now · closes Fri 17:00 · 3 hours once you start" | **Start the test** |
  | In progress (left and came back) | "In progress · 1:12:40 left" | **Back to the test** |
  | Handed in | "Handed in · marks after moderation" | **See where it's at** |
  | Released | "58 of 100 · released" | **See your result** |
  | Missed (closed, never started) | "Closed · you didn't sit this one" | **Practise this paper**. No penalty wording, and no red. |

- **The practice lock:** while the test is open, practice on that paper shows "Practice on this paper pauses until your class test closes (Fri 17:00)". Topics and drills on that paper are paused too. Other papers stay open.

## 2. Before you start (the notice)
- **Transparency first:** "Your teacher, ⟨name⟩, will see your marks for this." The name comes from the platform.
- **The rules, stated once:**
  - one attempt;
  - no hints;
  - the time;
  - "The clock stops at ⟨close⟩ if that comes first";
  - marks come after the test closes and the moderator checks them.
- **The label:** "Mock / class test · not an ICASS task".
- **One action: "Start · the clock begins".** It is only live while the window is open.
- This reuses the Hall entrance layout. The companion stays outside, and its line is "Good luck. I'll be here after."

## 3. Sitting
The Hall's sitting screen, unchanged in behaviour, with three differences:
- The header reads "Class test", and the clock uses `ends_at` = min(start + duration, window close).
- **Leaving** says: "The clock keeps running, and the test closes at ⟨close⟩."
  - The Hall's "costs the reward" line doesn't apply; the platform decides rewards.
- **At the window close,** an open sitting is handed in automatically with every saved answer. The server's clock decides.

## 4. After hand-in
The status steps are:
1. Handed in.
2. The test closes ⟨close⟩.
3. The moderator checks a sample.
4. Marks released.

Two lines of copy:
- "No marks or memo until then, for anyone in the class." It explains the wait and shows it's fair.
- "Marked by the computer and the model; a moderator from your college re-marks a sample before release."

## 5. Released
- The Hall's report, with the kicker **"Class test · released"** and the line "Released by your college's moderator · not an ICASS mark".
- Marks by question, the memo per part, and the fix round (practice, as in the Hall).
- **No conditions reward card.** The platform owns class-test rewards (refinement 2), so the design emits `mode: assessment`, `kind: class_test` and `review`, and shows nothing it can't promise.

## 6. The contract the prototype mocks (PROPOSED)
```http
GET  /v1/me/assignments
  200 [ { "assignment_ref": "…", "kind": "class_test", "mode": "assessment", "paper_version_id": "…",
          "opens_at": "…", "closes_at": "…", "duration_minutes": 180, "state": "upcoming|open|closed",
          "my_sitting": null | { "sitting_id": "…", "status": "in_progress|submitted|released" } } ]
POST /v1/sittings  { "assignment_ref": "…" }
  201 { "sitting_id": "…", "started_at": "…", "ends_at": "min(start + duration, closes_at)", "parts": [ … ] }
  409 { "error": "window_not_open" | "window_closed" | "already_sat" | "version_disclosed" }
GET  /v1/sittings/{id}/result
  202 { "status": "window_open" | "moderation" }   200 { "status": "released", "released_at": "…", … as the Hall }
```
- **Names never come from this service.** The BFF adds the teacher's display name from the platform (ARCH §7).
- **The practice lock is server-side.** While an assignment is open for the learner's audience, practice attempts on that `paper_version_id` return 409 `class_test_open`.

## As built (design commit c1e5d2a, 2026-09-27)
**Verified in the DOM:**
- **All six card states render on home:**
  - "Opens Tue 17:44 · in 2 days";
  - "Open now · closes Wed 17:44 · 3 hours once you start";
  - "In progress · 2:29:59 left";
  - "Handed in · marks after moderation";
  - "6 of 100 · released";
  - "Closed · you didn't sit this one".
- **The notice** leads with "Your teacher, Ms Rivera, will see your marks for this." It has no reward section and no `model-floor`.
- **The sitting header** reads "Class test". The design hook `window.__examHall.closeIn(4)` capped the 3-hour clock at 0:00:03, handed in at the close with the saved answer, then went "window_open → moderation → released". The report says "Class test · released · Released by your college's moderator · not an ICASS mark", with no reward card.
- **The practice lock:** while the window is open, the FM mission card reads "Paused for your class test". The card, the Topics drill and the Hall door all lead to the notice, and the FM Hall entrance is disabled with its reason. The Life Sciences Hall opens normally.
- **Phones:** the home screen still fits one 360 × 780 screen, because the companion's stage shrinks (22vh) while the card shows.

**Changes made while building:**
- "Handed in when the test closed" is now told apart from "when your time ran out".
- The fix-round line says "Your test mark stays as it is".
- Preview: `?test=upcoming|open|inprogress|handed|released|missed` or the home "Class test" preview row. The results screen has its own preview (Test still open / Moderator checking / Released).

**Decided 2026-09-27 (Murci, ARCH §9):** during the window, the test is home's one primary button, and the companion's line points at it. This was built in design commit c4c1481.

**Open for Murci:**
- **One assessment slot.** The prototype holds one assessment sitting at a time, so starting a class test replaces a finished Hall result in the dock. The service has no such limit.

## 7. Verification (DOM, all four sizes)
- Each of the six card states renders on home and on the map. Use a design-only Preview state switch; `?test=upcoming|open|inprogress|handed|released|missed` also works.
- `ends_at` is capped at the window close: set the close 1 minute ahead, and the sitting hands in at the close, not at 3 hours.
- The practice lock holds while the window is open: missions, topics, drills and the Review link on that paper lead to the notice. Other papers are unaffected.
- Leak check: no memo, stamp or mark before release. No `model-floor` in the test.
- The notice names the teacher, and every class-test screen carries "not an ICASS task".
- The Hall and practice are unchanged.

## Not in this brief
- The teacher side (brief 12: assign, moderate with the 10%-or-5 sample, the marking queue, results with groups under 5 hidden).
- Extra time per learner (needs per-learner data, Q8).
- Late and offline answers.
- Appeals.
