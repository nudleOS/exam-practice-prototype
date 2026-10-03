# Build prompt 23: "Your studies": the right papers for each learner

**Targets:** `Downloads/3rd design/Exam Practice.dc.html` (home, the paper picker) and this service (`/v1/me/studies`,
the papers filter).

**Decided 2026-09-27 (rulings, then "accept all three") and 2026-09-28 ("go with your recommendations"):**
- asked ONCE, in two taps, and skippable ("Show me every paper");
- stored in the exam service against the platform user id (pseudonymous);
- a chip changes it any time; the picker lists matching papers first;
- a teacher's class test always shows, whatever the learner picked;
- NSC stays in the model and HIDDEN from learners until there is a real NSC paper and a school on the platform;
- `programme` is renamed `qualification` now, while only two papers use it (it collided with the platform's
  `Programme`, a college's offering);
- step 2 differs by qualification, because that is how learners enrol: NC(V) learners pick ONE programme (its seven
  subjects come with it); NATED learners tick their subjects;
- both repos in this brief, and the missing brief 22 doc with it.

## The flow
1. **Step 1 — "What are you studying?"** NC(V) (Levels 2–4) or NATED (N4–N6), then the level.
2. **Step 2** — NC(V): "Your programme" (one choice; optional). NATED: "Your subjects" (only the subjects Nexera holds
   papers for at that level; none ticked = every paper at the level). A level with no paper says so plainly.
3. **The picker** — a chip ("NC(V) Level 4 · Engineering") reopens step 1 prefilled; "Your papers" first; the class
   test's subject pinned there with a "Class test" tag; everything else under "Also on Nexera". Its title is now
   "Pick a paper" (the question moved to step 1).

## Contract (the service; docs/API.md)
> **Superseded 2026-09-28 (Murci's ruling).** The learner's studies and the institutions belong to the Django
> platform (`UserProfile`, `InstitutionMembership`, `Institution`, `Campus`, `Programme`, `Subject`); the exam feature
> runs on the platform's exam page. `/v1/me/studies` and `learner_studies` were removed from the service before merge,
> and CORS went back to GET and POST. The design (ask once, skippable, "Your papers" first) stands; its data now comes
> from the platform, and the service is asked with `GET /v1/papers?qualification=&level=`. See the platform design note.
> The contract below is kept as the record of what was built.

- `GET /v1/me/studies` → `{"studies": null | {qualification, level, study_programme, subjects, updated_at}}`
- `PUT /v1/me/studies` — idempotent replace; folds whitespace, uppercases the level, drops duplicate subjects; a level
  its qualification doesn't have → `422 studies_level_invalid`
- `DELETE /v1/me/studies` → `204` ("Show me every paper")
- `GET /v1/papers?qualification=&level=` — narrows what is shown first; not access control
- Storage: `learner_studies`, one row per learner, keyed on `{iss, sub}` only (no name, no institution)

## Two findings worth keeping
- **The rename is at the boundary.** Approvals are pinned to the hash of the model's own dump
  (`registry.import_draft`), so dumping `qualification` would have voided BOTH approvals on the next sync. The model
  reads both keys and still stores `programme`; the API and code say `qualification`. A test pins it, and was seen
  failing without the fix. FM N6 and AET L4 both still match their `APPROVAL.json`.
- **CORS allowed only GET and POST,** so a browser `PUT` would have been refused before the route. Now GET, POST, PUT,
  DELETE, explicitly.

## Open (not built)
- ~~Unverified programme fixture~~ **Resolved 2026-09-28** (service 70977de, design, see below): the NC(V)
  curriculum pack `data/curricula/ncv.json` (20 programmes: 17 verified against DHET's 2026 ICASS Guidelines Annex F,
  3 single-source) and `GET /v1/curricula/{qualification}`; AET → Engineering and Related Design L4 is verified from
  DHET's own NOLS archive. Still open: each programme's subjects per level (DHET's subject matrix isn't published
  online — ask a college exam office or DHET), and the reported end of Umalusi certification for L2–L3 (Nov 2025).
- **The catalogue mixes programmes with subjects:** the "Also on Nexera" rows (`OTHER_SUBJECTS`) are NC(V) programme
  names and NATED N-Diploma programme names, not subjects. They are shown as they were; a subject catalogue per
  programme is the fix.
- **"Prefilled where possible":** the platform's optional sector field (TVET or school) isn't in the prototype's data;
  NSC is hidden anyway, so nothing changes for TVET learners today.
- **The skip lives on the device** (the service stores answers, never "didn't answer"): a learner who skips on one
  device is asked again on another.
- **Later (platform team, additive):** store qualification + level on the learner's enrolment, so we don't ask at all.

## Verification (as built, 2026-09-28)
- Service commit 65ae467: tests 48 → 60, all passing (12 new in `tests/test_studies.py`).
- Design commit 6fd0a22, checked in the browser at 375×812 and 1280×760:
  - first visit: the picker opens on step 1, focus on the first choice; "Next" with nothing picked → the alert;
  - NC(V) → Level 2/3/4 → "Your programme" (Engineering and Related Design · 1 paper) → Done → chip
    "NC(V) Level 4 · Engineering"; Your papers: Fluid Mechanics N6 (Class test · NATED) and Applied Engineering
    Technology L4; the stored row matches the service's shape;
  - the chip reopens step 1 prefilled; NATED N6 offers Fluid Mechanics; NATED N4 shows the "no paper yet" note;
  - "Show me every paper" → row deleted, "asked" kept, the list unfiltered, chip "Set your studies";
  - reload → the picker opens on "Pick a paper" (not asked again); the design-only reset brings the question back.
