# Build prompt 8: the Hall, the first sitting mode

Agreed order (Murci, 2026-09-27):
1. layer 2 (bec9ef2);
2. the Fluid Mechanics pipe scene (1a495ae);
3. the Life Sciences figure scene (07066b3);
4. the sitting modes. **This brief is the first of them: the Hall.**

**Target:** `C:\Users\mokon\Downloads\3rd design\Exam Practice.dc.html`. The Hall gets its own flow: entrance, sitting, hand-in, waiting, report. It reuses screen `03 Mission` for the answering itself.

## The rulings this must obey (decided, not open)
- **R2 (ARCHITECTURE-v1.md §9).** The Hall is a mock the learner starts themselves, on an open company paper. Its release follows a standing release policy: marks release automatically when every mark is final and any disagreement between two markers has been resolved by a human.
- **The Hall UX rule:**
  - Anything that **motivates** stays on: the world, the map, unlocking, the readiness check, XP paid at release, the report and the fix round.
  - Anything that **assists** or signals correctness in the moment is off: clues, instant right or wrong, companion reactions and the combo multiplier.
  - The paper's real time, instructions and formula sheet are pinned.
- **§3, assessment mode:**
  - one attempt; no clues;
  - no feedback per question (the service answers 202 until release);
  - the memo stays hidden until release;
  - the recorded mark stands;
  - rewards are paid only for the first attempt;
  - a `disclosed` version is refused.
- **Refinement 2:** no score-proportional tokens on unsupervised sittings. Instead, reward three things: a full mock sat under conditions, a completed fix round, and improvement across papers the learner hasn't seen. The platform owns tokens; this service and design only emit facts.
- **R7:** no 3D in exams or the Hall. The companion's `model-floor` **must not mount** in the Hall.

## What we found (measured in the design, 2026-09-27)
- `?sitting=hall` already works. It hides stamps, hints, the coach, the memo, the memo ghost, scene consequences, XP and the flying "+XP". The bar reads "Answer saved".
- **It still breaks R7.** The three `model-floor` elements (home, map and play) mount regardless of the sitting. The Hall must use the 2D still. `POSTER_SRC` is still `null`, so the silhouette is what shows until `companion-greet.webp` is rendered.
- **It is still practice underneath.** Each part locks when its answer is saved, the map's road lights up by marks, and there's no clock, no hand-in and no release. A real exam lets you answer in any order and change an answer until you hand in. The Hall must do the same.
- The service has **no assessment or Hall endpoints**; the README's "Known limits" says so. The prototype mocks them, using the contract proposed in §6.

## 1. The entrance (a Hall door on the map)
- **Where:** a "Sit it in the Hall" button in the map's pinned controls and on the summary screen. It only appears for papers whose version is not `disclosed`.
- **The readiness check is advice, never a lock.** It says:
  - how many missions have been practised (for example "9 of 13 missions practised");
  - "Calculator in the app";
  - the paper's real time ("3 hours, in one go").

  No barrier to entry is the mission, so a learner can always enter.
- **The rules, stated once:**
  - one answer per question, changeable until you hand in;
  - no hints;
  - no marks until the paper is released;
  - the formula sheet and instructions are on hand.
- **One primary action: "Enter the Hall".** The clock starts on this tap, not before.

## 2. Sitting (screen `03 Mission` in Hall mode)
- **The clock** counts down from `duration_minutes` and sits in the header, pinned on every size.
  - Warnings come at 30, 10 and 5 minutes, as a quiet text change plus an `aria-live="polite"` announcement. No red flashing and no ticking sound.
  - **The clock does not pause.** Leaving and coming back keeps the time running, because the end time is the server's `ends_at`.
  - At zero, the paper is handed in automatically with whatever has been saved.
- **The question navigator** covers the whole paper: one small square per part, in paper order.
  - Squares show three states: empty (unanswered), filled (answered) and amber (flagged). There's also a ring on the current part.
  - On phones it sits in a horizontal strip under the header. On tablet landscape and desktop it's a sticky side column (where the companion column is in practice).
  - Tapping a square goes to that part.
  - The squares never show correctness.
- **Answering** uses the same layer-2 controls and keypad as practice.
  - "Check" becomes **"Save and next"**. It saves a draft and moves on; the part does **not** lock, and it can be edited until hand-in.
  - **"⚑ Flag"** marks a part to come back to.
- **Scenes follow "the paper as printed".**
  - The LS figures stay, because they ARE the printed figure, and tapping on them is input.
  - The FM pipe scenes are our own drawings, not the paper's, so they're off in the Hall. The question shows its printed givens only.
- **Pinned:** the kit (Instructions, Formula sheet, Figures) stays one tap away from every part.
- **The companion** is the 2D still, beside the clock on wide screens and absent on phones. It gives no reactions. On entry it says only one line: "You've got this. I'll wait outside."
- **Off:** clues, stamps, the memo, the ghost, the coach, chimes, reactions, the streak, the multiplier and the flying XP.

## 3. Hand-in
- **"Hand in"** is in the navigator. It opens a sheet showing:
  - answered of total;
  - how many are flagged;
  - the time left;
  - "Go to the N unanswered", which jumps to the first one.
- **Confirming is final.** The sheet says it plainly: "You can't change answers after you hand in."
- After hand-in comes **one calm moment, not a celebration** (no score exists yet): "Paper handed in · 2 h 19 min · 30 of 32 answered". Then "What happens next".

## 4. Waiting for release
- The status reads "Being marked", with progress in plain words: "24 of 32 marks final". Parts marked by the computer are final at once, parts marked by the model need their review, and any disagreement goes to a human.
- The design shows three states:
  - **marking**: some marks not yet final;
  - **waiting for a person**: a disagreement is being resolved;
  - **released**.
- The map shows this paper's Hall sitting as a sealed envelope pinned to the start pad. The road stays as practice left it: the Hall never lights the road.
- A learner can keep practising other papers while they wait.

## 5. The report (after release)
- **The mark:** "64 of 100", with the mark per question. This is the first place any mark appears.
- **The reward (a fact, not a price):** "Full paper, sat under conditions". It's earned when the paper was handed in within the time, in one sitting and with at least 80% answered. The XP for it is a **flat** amount paid at release; it is not proportional to the score. **The exact amount is the platform's call.** The design shows the fact and a placeholder.
- **The memo** now opens per question, the same as practice's See the memo.
- **The fix round:** "Fix round · 9 parts" takes the learner through the parts that lost marks, in practice mode (tries, clues and reactions come back). Completing it is its own rewarded fact. The Hall mark does not change: **the recorded mark stands**.

## 6. The contract the prototype mocks (PROPOSED, not built)
Written down so the service can build it. Each call is marked `// MOCK` in the design.

```http
POST /v1/sittings                  { "paper_version_id": "…", "mode": "hall" }
  201 { "sitting_id": "…", "started_at": "…", "ends_at": "…", "parts": [ { "key": "1.1.2", … } ] }
  409 { "error": "version_disclosed" }            // §3: assessment refuses a disclosed version
PUT  /v1/sittings/{id}/answers/{part_key}  { "answer": {…}, "flagged": false }
  200 { "saved_at": "…" }                          // a draft; no mark, no verdict
  409 { "error": "sitting_closed" }                // after hand-in or ends_at
POST /v1/sittings/{id}/events  { "type": "left" | "returned" }
  204                                              // how "one sitting" is known
POST /v1/sittings/{id}/submit
  202 { "status": "marking", "final": 0, "total": 32 }
GET  /v1/sittings/{id}/result
  202 { "status": "marking" | "awaiting_moderation", "final": 24, "total": 32 }
  200 { "status": "released", "marks": 64, "total_marks": 100,
        "by_question": [ { "q": "1", "marks": 18, "of": 27 } ],
        "by_part": [ { "key": "fm:1.1.1", "marks": 3, "of": 3, "route": "auto" | "model" | "person" | "offline" } ],
        "conditions": { "within_time": true, "one_sitting": true, "answered_ratio": 0.94 },
        "fix_parts": ["1.2", "2.3.1"] }
```

- **Result event facts** (for the platform):
  - `mode: "assessment"`, `origin: "hall"`, `review` taken from the version;
  - `conditions` (the three booleans and the ratio);
  - **no** reward amount.
- **Security:**
  - the sitting belongs to the learner's `sub`, and every call checks it;
  - drafts are refused after `ends_at` (the server's clock, not the browser's);
  - the result route returns no memo content while the status isn't `released`.
- **Hall is its own sitting**, not the practice `attempt`: its answers never reach the practice `reply`/`reveal` path.

## As built (design commit 3f2ff74, 2026-09-27)
Built in `Exam Practice.dc.html` with the contract mocked in `HALL_API` (every method marked MOCK). Two departures from the text above, both made while building:
- **The companion is not inside the Hall on any size.** It stands at the entrance and says "You've got this. I'll wait outside." The sitting is just the learner and the paper. That matches its own line and keeps R7 simple, because no companion view exists in the sitting at all.
- **A paper marked wholly by the computer releases the moment it is handed in.** This follows the policy: every mark is final, so it releases. The report then appears straight away, with no waiting state.

Also found while building, and designed in:
- **Practice on a paper whose Hall sitting is open leads back into the Hall.** Otherwise a learner could leave, practise the same questions with hints and the memo, and come back.
- Autosave runs every second, so an answer typed just before the time runs out is kept.
- Leaving asks first and says it costs the conditions reward.

Preview switches (design only): `?sitting=hall`, `&paper=ls`, `&hallMinutes=N`, the result screen's Preview state bar, and `window.__examHall.endIn(seconds)`.

## Ruling L12, decided 2026-09-27 (ARCH §9): BUILT (design commit 6f5886d)
- **The report line:** while a subject has one paper, the Hall report says, for example, "You've practised 9 of 13 missions on this paper, so this mark may run high".
- **No readiness use:** Hall marks feed no readiness and no topic-strength evidence.
- **The conditions reward stays**, because it pays for behaviour, not score.
- **When a second approved paper exists,** one paper becomes Hall-only.
- **As built:**
  - The practised count is snapshotted when the learner enters the Hall.
  - The report reads "You'd practised 5 of 13 missions on this paper before sitting it, so this mark may run high. It isn't counted towards your readiness." (amber), or "You hadn't practised this paper before sitting it…" (muted). Class-test reports don't show it.
  - **Found while building:** seeing a memo in the report or the fix round didn't count as "seen". Fix-round parts, and every part of a question opened in the report, are now marked `memoSeen`. Drills stop calling them "new to you", and their first tries weigh 0.3 (seen evidence), not 1.0.

## 7. Verification (in the DOM, at phone, tablet portrait, tablet landscape and desktop)
- **R7:** no `model-floor` element exists in the DOM on any Hall screen.
- **Leak check:** before release, the Hall's DOM contains none of the memo's answers, no stamps and no "✓"/"✕". This is the same search as the figure scene's leak check.
- **Drafts stay editable:** edit an answered part, and the navigator and hand-in counts update.
- **The clock:** simulate `ends_at` by setting it one minute ahead; the automatic hand-in fires and the summary is right.
- **Overlaps:** none between the clock, the navigator, the footer and the keypad; the keypad's `fitKpField` still works.
- **Focus:**
  - the hand-in sheet traps focus, and Esc closes it;
  - focus returns to the Hand in button;
  - the timer warnings are announced.
- **Practice is unchanged:** with `?sitting` absent, every earlier check still passes.

## Not in this brief
- The endpoints themselves (service work).
- Topic drills, teacher class tests (moderator release) and the proof of "improvement across unseen papers" (needs two papers per subject).
- The walk clip.
- Rendering `companion-greet.webp` (the silhouette holds its place).
