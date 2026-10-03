# Build prompt 12: the teacher tool (T1–T5), class tests from the teacher's side

**Target:** a new design file, `C:\Users\mokon\Downloads\3rd design\Teach Exams.dc.html`.
- It uses the same tokens as the folder's other designs (`--bg #191b1e`, `--panel`, `--line`, `--tint`, Sora).
- It's a **calm tool:** no XP, no companion, no celebrations.
- It's desktop first (teachers mark on laptops) and works on tablets and phones.
- The source design is `design/screens.v2.md` §17. This brief corrects it where a later ruling changed it.

## The rulings this must obey (decided)
- **R1, setter and moderator:**
  - a paper or test reaches an audience only with a setter and a moderator, and **the moderator is never the setter**;
  - a teacher-set paper or class test is moderated by that institution's **`institution_admin`**;
  - a company paper's *content* is already approved by Nexera's curriculum team.
  - **This supersedes screens.v2 §17's "subject head or institution_admin (configurable)", which is stale.**
- **R2 (b):** class-test marks are released by the institution moderator **after the window closes**.
- **Refinement 3:** a class test is **not an ICASS task**. It's labelled that way on every screen, and in the gradebook column: "⟨paper⟩ mock · AI-marked, moderated sample n = ⟨k⟩ · not ICASS".
- **R3:** teacher authoring is platform first. **Upload and generate are the next brief (13).** Here, a teacher assigns from the bank.
- **ARCH §7 (identity):**
  - the service holds pseudonymous ids, and names come from the platform;
  - `InstitutionMembership.role ∈ {teacher, institution_admin}` can set and assign;
  - `campus_manager` is scoped to its campus;
  - `simulation_designer` has no exam authority;
  - any aggregate under 5 learners is hidden (k ≥ 5).
- **Platform facts (measured 2026-09-21/26):**
  - there is **no class or enrolment model**, so audiences are **college or campus only**, and "A class" is shown disabled with its reason;
  - `/auth/me` doesn't expose `institution_role` yet; the platform team owns that gate.

## 1. T1 · Teaching home
Three blocks:
1. **Waiting for you:**
   - Marking ⟨n⟩;
   - Moderation sample ⟨n⟩ (institution admin only);
   - Assessments to approve ⟨n⟩ (institution admin only);
   - Marks to release ⟨n⟩.
2. **Your assignments:**
   - paper · kind · audience · state;
   - "31 of 38 handed in" for an open test;
   - "Closed · sample needed" for a closed one.
3. **Paper bank:**
   - rows show the provenance badge ("Checked by Nexera"), marks, time and "Can be used for: practice · mock / class test";
   - "Upload a paper and its memo" and "Generate a practice paper" are shown **as next-step placeholders** (brief 13), not as dead buttons.

Also on the page:
- **The banner:** "Classes aren't on the platform yet, so you assign to your whole college or a campus. Tests here are mocks, not ICASS tasks."
- **The primary action:** "Assign a paper".
- **Design-only switch:** "Viewing as: Teacher (Ms Rivera) | Institution admin (Mr Okafor)". Names are SAMPLES; the real ones come from the platform. The admin view adds the moderation queues.

## 2. T2 · Assign a paper (four steps, one screen with a stepper)
1. **Paper:**
   - the bank rows, filtered to the teacher's subject;
   - a `disclosed` version can't be picked for a test, and says why;
   - a paper this audience has practised is flagged: "Your learners have practised this paper, so it isn't an unseen test".
2. **Mode:** two radio cards.
   - **Practice (a challenge):** three tries, hints, the memo after three tries, no tokens.
   - **Mock / class test · not an ICASS task:** one attempt, no hints, marks after moderation.
   - For a DHET past paper, the card adds: "DHET says old exam papers aren't authentic ICASS tasks, so use this as a mock." (ICASS26:610-612)
3. **Audience and window:**
   - audience: "Everyone at ⟨College⟩" or "⟨Campus⟩ campus"; "A class" is disabled with "Classes aren't on the platform yet";
   - opens and closes (date and time);
   - duration: the paper's own;
   - extra time per learner shows "needs per-learner data the platform doesn't have yet" (Q8).
4. **Check and send:**
   - the summary;
   - the learner's notice, previewed exactly: "Your teacher ⟨name⟩ will see your marks for this. This is a mock, not an ICASS task.";
   - **Practice → "Publish to learners"** (the setter alone may release practice to their own audience, labelled "Set by your teacher").
   - **Class test → "Send for moderation"**: "An institution admin must approve this before learners see it."

## 3. T3 · Moderate (institution admin)
- **Assessments to approve:** the test's summary and paper. The setter's own test shows "You set this test, so another institution admin must approve it", with no approve button.
- **The moderation sample,** before any class-test marks can be released (follows ICASS26:2256-2290):
  - **Size:** 10% of submitted scripts or at least 5, whichever is larger. All scripts if fewer than 5.
  - **Stratified** by AI total: best, middle and weakest.
  - **A blind re-mark:** names are hidden, and the AI's marks are hidden until the moderator saves.
    - In the prototype, the moderator re-marks **per question total** (Q1–Q4).
    - Per-point marking lives in T4.
  - **Variance** per script = |AI total − moderator total| ÷ paper total. If more than 5% on **more than half** of the sample, **release is blocked** until the batch is re-marked.
  - The screen shows, for example:
    - "Moderation sample: 4 of 5 done";
    - per script, "AI 58 · you 61 · 3% ✓";
    - a summary, "1 of 5 over 5% · release allowed", or "3 of 5 over 5% · re-mark the batch before release".
- **Marks to release:**
  - it shows the distribution, "All ⟨n⟩ marking disagreements resolved", "Moderation sample passed (n = 5)", and anything still provisional;
  - **Release marks** is disabled until every gate passes;
  - the confirm says: "Release marks to 38 learners? They'll see their marks and the memo. This can't be undone."

## 4. T4 · Marking queue
- **Items:** AI-marking disagreements (two model reads that differ), drawings (Life Sciences), and moderation-sample scripts.
- **The layout:** the learner's answer on the left ("Names hidden while marking", on by default) and the memo criteria on the right.
  - The criteria are **checkboxes for human marking**, with an optional comment each.
  - A disagreement shows both AI reads with their evidence, and the moderator decides.
  - Buttons: "Save mark" and "Save and next".

## 5. T5 · Results (k ≥ 5)
- **The header:** "⟨paper⟩ · Mock / class test · not an ICASS task · closed ⟨date⟩ · ⟨n⟩ submitted · marks released ⟨date⟩ · AI-marked, moderated sample n = 5".
- **Marks:** a 10-mark-bin histogram **with a data-table twin**. Also by question (averages), by topic (the service's topics), and by campus.
- **Any slice under 5 learners** renders "Fewer than 5 learners · hidden to protect privacy".
- **Learners who sat this assignment:** the setter sees them by name, because learners were told. Nothing crosses the assignment boundary.
- **No export in v1.**

## 6. Data (prototype mocks, labelled MOCK)
- **One college, two campuses:** North has 35 learners who sat, South has 3 (to show suppression).
- **38 scripts** with AI totals per question, drawn from a seeded distribution, not from real learners. The names are SAMPLE names from many cultures.
- The FM N6 class test, the same assignment as the learner prototype (brief 11): opens ⟨date⟩, closes ⟨date⟩, 180 minutes.
- **The contract mocked:**
  - `POST /v1/assignments` (draft → `awaiting_moderation` → `open`);
  - `POST /v1/assignments/{ref}/approve` (403 if the approver is the setter);
  - `GET /v1/assignments/{ref}/sample`, then `PUT` per script;
  - `POST /v1/assignments/{ref}/release` (409 until the sample passes and the window is closed);
  - `GET /v1/assignments/{ref}/results` (k ≥ 5 applied **server-side**).

## As built (design commit 7746119, 2026-09-27)
**Verified in the DOM:**
- **T2:**
  - The flashcard edition (`disclosed`) disables the class-test mode, with its reason.
  - FM shows "22 of your learners have practised this paper, so it isn't an unseen test".
  - The DHET ICASS line appears on the mock card, and "A class" is disabled ("Classes aren't on the platform yet").
  - A South-campus test warns "fewer than 5 learners: results stay hidden".
  - The notice preview names the teacher. "Send for moderation" leaves the test "Waiting for an institution admin".
- **R1:** Mr Okafor approved Ms Rivera's test. His own test shows "You set this test, so another institution admin must approve it" with **no** approve button.
- **The sample:** 38 scripts → 5, labelled best, middle × 3 and weakest, with names hidden and the AI's marks hidden until saved. "Far apart" gives 3 of 5 over 5% and release is blocked; "close" gives 0 of 5 and release is allowed.
- **Release:** it stays disabled until the 3 marking disagreements are resolved (T4). The confirm says "Release marks to 38 learners? … This can't be undone", and focus starts on Cancel.
- **T5:**
  - The bins sum to 38, and the table twin has 10 rows.
  - North shows "58% (n = 35)"; South shows "Fewer than 5 learners · hidden to protect privacy".
  - The admin (not the setter) sees no names; the setter sees all 38.
- **Phones (360 wide):** no horizontal scroll on any view, and the header no longer overlaps (the admin label is shortened to "Admin").

**DECIDED 2026-09-27 (Murci, ARCH §9): option (a).** k ≥ 5 protects learners from viewers without individual access. The setter sees their own assignment's learners, and everyone else gets suppressed aggregates. The record of the question follows.

**Was open for Murci:**
- **§17.5's two rules collide.**
  - Rule 1 lets the setter see every learner by name and mark.
  - Rule 2 hides a campus slice under 5.
  - The setter's list shows each learner's campus, so the hidden South average is derivable from the 3 South rows.
  - Options:
    - (a) accept it, because the setter may see individuals anyway;
    - (b) drop the campus column from the setter's list when that campus is under 5;
    - (c) hide small campuses' learners from the list.
  - Recommended: (a) for the setter, since learners were told. Keep suppression for everyone else, which the admin view already shows.
- **Two prototype shortcuts:**
  - Marks decided in T4 mark the item resolved but don't change the script totals.
  - A failed sample has no "re-mark the batch" flow yet; the preview only refills the sample.

## 7. Verification (DOM, desktop / tablet / phone)
- **Setter ≠ moderator:** as the teacher, no approve button on their own test; as the admin, approval works.
- **The sample rule:** 38 scripts → 5 sampled, stratified (best, middle, weakest).
  - 1 of 5 over 5% → release allowed.
  - 3 of 5 over → release blocked.
- **Release** is disabled before the window closes and before the sample passes. The confirm names the count.
- **Results:** South (n = 3) is hidden on every slice, the histogram has its table twin, and no name appears outside the setter's own list.
- **The labels:** "not an ICASS task" on T1 rows, T2 step 2, T4, T5 and the gradebook label.
- No overlaps, no horizontal scroll, and focus flows through the stepper and dialogs.

## Not in this brief
- Upload and generate (brief 13).
- Roster and classes (a platform prerequisite).
- Appeals, and late answers.
- Wiring this prototype to the learner prototype (it could share the assignment through `localStorage` on the same origin; offered as a follow-up).
