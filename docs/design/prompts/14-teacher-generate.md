# Build prompt 14: teacher authoring, part 2 — generate a practice paper

**Target:** `C:\Users\mokon\Downloads\3rd design\Teach Exams.dc.html`, which gets new views: Blueprint, Generating, and Suggestions.
- It replaces the "Generate a practice paper · next step" placeholder.
- **A successful draft goes to brief 13's Review and Approve screens.** They are generalised from "the FM upload" to "any draft", so there is still one quality gate.

## The rulings this must obey (decided or already designed)
- **Authoring time only (ENGINE §4.1, ARCH §4).**
  - Nothing generated reaches a learner without human review and approval.
  - Generation never runs at learner time, and there is **no silent fallback**.
- **R5:** Claude sits behind the adapter, and switching generation to it is **gated on an eval** (FM N6 + AET L4). The prototype mocks the model. It claims no output quality, and every draft is labelled *Generated*.
- **Never ground on past-paper text (ENGINE §4.2).** State copyright applies, and the old generator could leak it.
  - Grounding comes from **the syllabus / subject guideline** and optional **teacher excerpts**. The setter asserts their rights over excerpts (`teacher_supplied`).
  - Past papers shape only the **blueprint numbers** (topic marks, marks, time), never the words.
  - `past_paper` excerpts are refused (422).
  - Output is checked with **`C-no-verbatim-overlap`**: 12-word shingles against the bank's papers.
- **Generated content passes the same gates as an upload (ENGINE §6.3):**
  - **G-memo-replay** on every memo;
  - **C-memo-agreement**: an independent solve, marked by the production marker, must earn full marks;
  - **C-grounded**: every item cites its source;
  - **C-blueprint-fit**: topic marks within ±5 of the blueprint;
  - **C-cognitive-spread**: within ±10 points;
  - verdicts are counts, never a confidence score.
- **Failure → suggestions (ENGINE §7.2).**
  - A failed job ends with a sentence, then ranks **approved** bank papers by fit, lexicographically: same subject, level and language; then topics covered; then the smallest deviation in topic marks; then the most recent.
  - **The setter chooses. Nothing is chosen automatically.**
- **The job is a persisted state machine (ENGINE §4.6, §11.2).**
  - Its states: `queued → reserving_budget → planning → retrieving → drafting → enforcing → (redrafting, once) → checking → writing_draft → succeeded`.
  - Or `suggesting → failed`, with the reason `refused | budget | no_blueprint | model_refusal`.
  - **Human approval is not a state of the job.** It lives on the paper version.
- **Teacher quotas (ARCH §8):**
  - generation runs in its own model workspace, with a college quota;
  - `llm_budget` gives "The monthly generation budget for this workspace is used up."

## Two calls this brief made (DECIDED 2026-09-27, ARCH §9)
1. **Generated papers are practice-only until generation passes its R5 eval.** In T2, the mock / class-test card is disabled for a generated paper: "Generated papers are for practice until our quality check of generation is complete."
2. **Learners see who made it.** The label is "Written with AI from the syllabus · checked by ⟨college⟩". The `origin = generated` fact travels with every result (ARCH §3).

## 1. Blueprint
- **Subject:** Fluid Mechanics N6. Its pack is the N6 syllabus, with weights as in brief 10.
- **Topics:** every syllabus topic, each with its weight shown.
  - The teacher ticks topics and sets marks per topic. "Fill from weights" spreads the total by syllabus weight.
  - Vortex flow is shown, and can be ticked. It's the one topic with **no bank question**, which is exactly where generation helps.
- **Total marks and time:** time comes from the paper's rate (180 minutes per 100 marks), editable.
- **The default sample blueprint** is 14 marks and 25 minutes: pipe flow 3, open channels 4, pumps 7.
- **Your notes (optional):**
  - a text box for the teacher's own notes or textbook passages;
  - a checkbox, "I have the right to use this text", is required if the box is used;
  - the note: "Past papers are never used as source text; they only shape the numbers (marks, topics, time)."
- **The quota:** "This month: 7 of 10 generations left for your college" (SAMPLE).
- **One action: "Generate a draft".** It's disabled until at least one topic has marks.

## 2. Generating (the job)
- **The states from §11.2 shown as sentences:**
  1. Budget reserved.
  2. Blueprint checked against the syllabus.
  3. Syllabus text retrieved (⟨n⟩ passages · no past-paper text).
  4. Draft written.
  5. Marks and memos enforced.
  6. Checked (⟨n⟩ flags for you).
  7. Draft saved · awaiting your review.
- "You can leave; it keeps going."
- **Design-only Preview outcomes:**

  | Outcome | What happens |
  |---|---|
  | Success | The draft goes to review. |
  | Refused twice | "The draft was refused twice: G3's memo points add up to 2, but G3 is worth 3 marks." The job moves to `suggesting`, then `failed`. |
  | Budget | The `llm_budget` sentence, and **no** suggesting step. |
  | Model declined | "The model declined part of this request. Try again, or use an approved paper." |
  | No blueprint | "This subject's exam shape isn't known yet, so a blueprint can't be checked." |

## 3. The sample draft (built for the prototype, labelled SAMPLE; physics checked)
Five items, 14 marks. Two carry real-looking faults, so the gates are exercised.

| Item | Topic | Marks | What it is |
|---|---|---|---|
| G1 | Pipe flow | 3 | Reservoirs 10 m apart, a 600 m pipe of 0,5 m diameter, f = 0,006. Answers: hf = 10 m, V = 2,610 m/s, Q = 0,512 m³/s. **Flag C-no-verbatim-overlap:** the stem shares 14 words with FM N6 Nov 2022 1.1. **The fix is to rewrite the stem.** The check re-runs on save, and passes when the shingle is gone. |
| G2 | Open channels | 4 | A 60° V-notch, 420 ℓ/s, Cd 0,62 → H = 755,837 mm (the ENGINE §5.4 MEASURED sample). Passes. |
| G3 | Pumps | 3 | Q = 0,05 m³/s, H = 30 m, η = 75% → water power 14,715 kW; shaft power **19,62 kW**. **Flag C-memo-agreement:** the draft memo multiplies by η (11,04 kW). The independent solve divides, giving 19,62 kW. Resolutions as for an arithmetic fault: correct it · accept both · printed stands (reason + a second approver). |
| G4 | Pumps | 2 | Define cavitation. The memo points come from the service's authored memo. Passes. |
| G5 | Pumps | 2 | Explain why a centrifugal pump must be primed before starting. Memo: air has far lower density than water, so the impeller cannot create enough pressure difference to lift water; priming fills the casing and suction pipe. Passes. |

- **Paper-level checks:**
  - **C-blueprint-fit** is computed against the teacher's actual blueprint. If they change it, the check shows the real deviation; over ±5 marks on a topic, it must be acknowledged.
  - C-cognitive-spread ✓.
  - C-grounded ✓: every item cites a syllabus topic.
- Each item's detail shows **"Source: N6 syllabus · ⟨topic⟩"** and the **Generated** label.

## 4. Suggestions (when a job fails with `refused`)
- **The heading:** "Generation didn't produce a paper you can use. Here are ⟨n⟩ approved papers that fit this blueprint."
- **Each suggestion shows:**
  - its provenance line and licence status;
  - the topics it covers from the blueprint;
  - "Use this paper", which opens T2 with it preselected (practice). **Nothing is picked automatically.**
- **Ranked by the rule in §7.2:** FM N6 Nov 2022 (Checked by Nexera) first, then the college's approved upload if one exists.
- **If nothing fits:** "No approved paper fits this blueprint. Edit the blueprint or try again."

## 5. The contract the prototype mocks (PROPOSED)
```http
POST /v1/banks/{bank_ref}/generations  { "blueprint": { "total_marks", "duration_minutes", "topic_marks": [...] },
                                         "grounding_excerpts": [ { "text", "source_class": "teacher_supplied", "licence": "asserted_by_setter" } ] }
  202 { "job_id": "…" }   422 { "error": "past_paper_excerpt" }   429 { "error": "llm_budget" }
GET  /v1/jobs/{job_id}   200 { "state": "…", "sentence": "…", "paper_version_id"?: "…", "suggestions"?: [ { "paper_version_id", "fit": { "topics_covered", "deviation" } } ] }
```
- The draft is a paper version with `origin: generated`. It goes to the same review, resolution, submit and approve routes as brief 13.
- **Security:**
  - excerpts are untrusted data, never instructions;
  - draft memos live in one memo-grade table, purged 7 days after the job ends (§4.6);
  - there is no LangGraph checkpoint copy.

## As built (design commit 31c9be3, 2026-09-27)
**Verified in the DOM:**
- **Brief 13 still passes after the review was generalised:**
  - the encrypted PDF gives its sentence;
  - a clean read gives 18 of 32 resolved, and 1.3 offers 3 resolutions;
  - 4.1.1 needs the Question 4 ruling;
  - the 1.4.5 follow-through and the 3.3.1 expert check are present.
- **The blueprint form:**
  - notes without the rights box are refused;
  - "Fill from weights" with 20 marks over pumps, pipes and open channels gives 8 / 7 / 5 (largest remainder, it adds up exactly);
  - the sample blueprint gives 14 marks and 25 minutes.
- **A successful job:** the seven named steps, then the review with G1 and G3 flagged.
- **G1:** the overlap check finds a **real 23-word run** shared with FM N6 Nov 2022 1.1 ("the pipeline rises 3 m above the upper reservoir at 260 m…"). It clears once the stem is rewritten; the check re-runs on save.
- **G3:** "Printed 11,036 kW · Independent solve 19,62 kW", with exactly three resolutions.
- **Sending and approval:** send at 5 of 5, then the admin approves. The paper lands in the bank as *Your college · generated*. In T2 its class-test mode is disabled: "Generated papers are for practice until our quality check of generation is complete."
- **Blueprint fit:** a blueprint of Pumps 14 shows "Pumps 7 of 14 (−7)", and sending stays locked until the teacher confirms the fit.
- **Failures:**
  - Refused twice: the sentence at "Marks and memos enforced", then 2 ranked suggestions. "Use this paper" opens T2 at step 2 with practice preselected.
  - Budget: the sentence at "Budget reserved", with no suggestions.
  - Model declined: the sentence at "Draft written".
  - Shape unknown: the sentence at "Blueprint checked".
- **Phones (360):** no horizontal scroll on the form.

**Changes made while building:**
- A job refused before any model call ("shape unknown") keeps its budget reservation, so it doesn't use up the quota.
- The papers-to-approve line says "generated for" rather than "uploaded by".
- The second value on G3 is labelled "Independent solve".
- The flashcard edition ranks level with the faithful paper in the suggestions. It is practice-usable, and the rule has no tie-break beyond recency.

## 6. Verification (DOM, desktop / tablet / phone)
- **The blueprint:** "Fill from weights" spreads the marks. Notes without the rights checkbox block generation. The quota is shown.
- **Success:**
  - the job shows the seven steps;
  - the draft opens in review with G1 and G3 flagged;
  - G1 stays flagged until the stem is rewritten;
  - G3 offers exactly three resolutions;
  - changing the blueprint to Pumps 14 shows a real C-blueprint-fit deviation.
- **Refused:** the sentence, then ranked suggestions. "Use this paper" opens T2 preselected, and nothing is auto-chosen.
- **Budget:** the sentence, with no suggestions step.
- **After admin approval,** the generated paper is in the bank as *Your college · generated*. In T2 its class-test mode is disabled with the R5 reason.
- **The upload review still passes** every brief 13 check, now that the review is generalised.
- No overlaps, and no horizontal scroll.

## Not in this brief
- Real retrieval (pgvector) and the embedding model (unsized, §4.3).
- Batch pricing.
- Recipes / templates for teachers (brief 10 has samples; P-T1 is now decided, ARCH §9).
- Section structure beyond topics.
- Languages other than en-ZA.
