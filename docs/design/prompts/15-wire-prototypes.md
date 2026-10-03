# Build prompt 15: wire the teacher and learner prototypes into one class-test loop

**Targets:** `Downloads/3rd design/Teach Exams.dc.html` and `Downloads/3rd design/Exam Practice.dc.html`. Both are served from the same origin (`exam-design-3`, localhost:8767).

## Why
Today each prototype mocks the other side:
- **The learner's class test** is a preview seed (`CLASS_TEST`, six preview states).
- **The teacher's closed test** holds 38 seeded scripts.

Wiring them gives the demo the real sequence, with two tabs side by side:
1. a teacher assigns;
2. an admin approves;
3. a learner sits and hands in;
4. the admin moderates and releases;
5. the learner sees their marks.

It is also the first place the **proposed contracts from briefs 11 and 12 meet each other**. A field one side writes and the other can't read shows up here, before either is built for real. This is the lesson of "two halves green on their own opinion".

## The mechanism (prototype only, labelled MOCK)
- **One key in `localStorage`,** `nexera.proto.v1`, stands in for the exam service:
  ```json
  { "v": 1,
    "assignments": [ { "ref", "paperId": "fm-n6-2022-11", "kind": "class_test", "opensAt", "closesAt", "minutes": 180,
                       "setterName", "state": "awaiting_moderation|open", "releasedAt": null } ],
    "submissions": [ { "ref", "sub": "learner-this-browser", "submittedAt", "byPart": { "1.1.1": 3, … }, "answered": 3 } ] }
  ```
  - `v` is a schema version: a missing or unknown version is treated as empty.
  - Every read and write is wrapped in try/catch; private windows can block storage.
  - Both prototypes still work alone when the key is empty.
- **Live updates:** a `storage` event reloads the bus in the *other* open tab. A tab doesn't receive its own writes, so each writer also updates its own state.
- **Each side reads only what the real service would send it:**
  - the learner reads assignments for its audience and `releasedAt`, never other submissions;
  - the teacher reads submissions for their own assignments.
  - **No memo, key or expected value is ever written to the bus.** The learner's marks come from the learner prototype's own mock marker, as they do today.
- **This is not a security boundary.** Browser storage is readable by anyone at the keyboard. It stands in for server routes whose security is specified in briefs 11 and 12 (sub-scoped sittings, k ≥ 5 server-side, memo scopes).

## 1. Teacher → learner: the assignment
- **Approving a class test on the FM paper** (T3) writes it to the bus as `open`, with its window and the setter's display name. Creating it writes `awaiting_moderation`, which the learner never shows.
- **The learner's class-test card** uses the newest approved FM class test from the bus, when there is one:
  - it takes the window (upcoming, open or closed) and the teacher's name;
  - a small "Live from the teacher tool" tag shows the source;
  - if the bus has none, the card falls back to the preview seed, exactly as today.
- **The learner's "Class test" preview row gains "Live",** selected automatically when a live assignment exists.
  - Picking a preview state switches back to local previews.
  - "Live" returns to the bus.
- **T2 step 3 gains "Opens now",** which sets the window to now → now + 2 hours. A demo can then run without waiting a day.

## 2. Learner → teacher: the hand-in
- **Handing in a live class test** writes a submission. It holds:
  - the per-part marks from the learner's mock marker (online parts only);
  - `answered`;
  - a pseudonymous `sub`. The teacher sees the name "You (this browser) · sample", because the platform would join names, not the service.
- **The teacher's T1 row** counts "n of 40 handed in" from the bus for a live assignment.
- **T3 moderation gets an assignment picker:** the seeded closed test, or a live one once its window has closed.
- **For a live assignment:**
  - the scripts are the bus submissions;
  - the sample follows the same rule: 10% or at least 5, **all scripts if fewer than 5**. With one script, the sample is that one script;
  - release has the same gates: the window closed, the sample passed, disagreements resolved. The seeded T4 queue belongs to the seeded test only.
- **"Close now"** in T3 (design-only) ends a live window, so the demo can reach moderation.
- **T5 results for a live assignment** follow k ≥ 5. With one learner, **every slice reads "Fewer than 5 learners · hidden to protect privacy"**, and the setter's own named list still shows the one learner. The privacy rule shows itself live.

## 3. Teacher → learner: the release
- **Releasing a live assignment** writes `releasedAt`.
- **The learner's result screen moves to "Released"** as soon as the bus says so. It doesn't wait on its own timer. "Released by your college's moderator · not an ICASS mark" follows as today.
- **The live assignment decides the release, not the timer.** The learner prototype's class-test clock and its local "moderation after 6 seconds" timer are replaced, for a live assignment, by the bus's `closesAt` and `releasedAt`.

## 4. Both sides
- **"Reset the shared demo"** (design-only) clears the key, in both prototypes. It's on the teacher's home and next to the learner's preview row.
- **Every place that reads the bus names it in a code comment:** `// MOCK: the exam service`.

## 5. Verification (two tabs in the browser pane, then each alone)
1. **Empty bus:** each prototype behaves exactly as before (brief 11 and 12 checks).
2. **The teacher side:** the teacher assigns FM as a class test with "Opens now", and the admin approves it.
3. **The learner tab,** without reloading, shows "Open now · closes … · 3 hours once you start" and names Ms Rivera. The tag reads "Live from the teacher tool".
4. **The learner sits it,** answering 1.1.1 correctly, and hands in. The teacher's row counts 1 handed in, without reloading.
5. **The admin closes the window,** and the picker offers the live test. The sample is 1 of 1. Re-marking passes, and release is allowed. Releasing shows its confirm, naming 1 learner.
6. **The learner tab moves to released,** showing the learner's own mark.
7. **Teacher T5** hides every slice ("fewer than 5"), while the setter's list shows the one learner.
8. **Reset clears both.** No memo text or key value exists in `localStorage` at any point (a leak check over the stored JSON).
9. **Storage blocked** (simulated by throwing in the accessor): both prototypes still run on their seeds.

## As built (design commit c26edea, 2026-09-27)
**Verified with two tabs in the browser pane:**
1. **An empty bus:** the learner card is on its seed ("Open now · closes Wed …"), with no Live chip. The teacher reads "0 tests · 0 hand-ins".
2. **The teacher side:** assign FM as a class test with "Opens now" (the bus shows `awaiting_moderation`), then the admin approves (the bus shows `open`). The bus keys are exactly `ref, paperId, kind, opensAt, closesAt, minutes, setterName, state, releasedAt`.
3. **The learner tab, without reloading,** shows "Live from the teacher tool · Open now · closes Sun 20:47". The Live chip is pressed, and the notice reads "Your teacher, Ms Rivera, will see your marks for this".
4. **The sitting clock started at 1:59:44,** capped at the 2-hour window. After 1.1.1 was answered correctly and handed in, the bus holds 1 submission (`1.1.1: 3`, answered 1). **The leak check over the stored JSON found no memo or answer text.**
5. **The teacher's row reads "1 of 40 handed in".**
   - The picker offers "Live test · 1 handed in · open".
   - Before the close, release is locked.
   - "Close now" leads to a sample of "Script 1 of 1 · Every script", and the re-mark passes.
   - The confirm says "Release marks to 1 learner?", and the bus gets `releasedAt`.
6. **The learner tab moves by itself** to "Class test · released · Released by your college's moderator · 3 of 100".
7. **T5 for the live test:** the histogram, by question, by topic, and North and South all read "Fewer than 5 learners · hidden to protect privacy". The setter's list shows the one learner.
8. **Reset** (from the learner tab) clears the key. The learner is back on its seed, and the teacher reads "0 tests · 0 hand-ins" through the storage event.
9. **`?nostorage=1`** leaves both on their seeds. The teacher says "storage is blocked, so this runs on its own".

**Found while building:**
- **The results route only suppressed the histogram and campuses.** It now suppresses **every** slice under 5 (by question and by topic too), server-side in the mock. On the seeded 38 this never showed; it took one live learner to reveal it.
- **A live assignment can't be released with zero scripts.** The sample gates now need at least one script.
- **The known edge:** picking a local preview state while a live sitting is in progress drops the learner's view of that sitting. The service row remains, so re-sitting is refused as `already_sat`.

## Not in this brief
- More than one learner (a second browser profile would add one; the rule already handles it).
- Practice assignments reaching the learner.
- Uploads or generated papers being assigned live (T2 can pick them; the learner prototype only has the FM paper's content).
