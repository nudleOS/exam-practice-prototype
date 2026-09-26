# Curriculum tool → Platform: publish contract

Status: the curriculum tool defines this shape. The platform conforms to it.

The tool is the authoring and QA surface; the platform receives and serves. Where the two disagree today, the tool is right and the platform changes — that decision is made, and the sections below are written as requirements rather than requests. Expect the shape to keep moving while the tool is still being built; this document follows the tool, not the other way round.

Last updated: 11 September 2026

---

## What this document is for

The curriculum tool authors and QAs exam papers. The platform (`nudlestudio_api`) serves them to learners and collects attempts. Right now there is no contract between the two, so publishing has no destination and results have no way back.

This describes both directions, and the three places the platform has to change to accept them.

---

## Direction 1 — Publish (tool → platform)

### When it fires

Only after a human on the curriculum team has confirmed an item. The agent check does not publish; it annotates. Nothing reaches a learner without a person approving it.

### What goes

A paper and its memo travel together, always. A paper without its memo cannot be marked, so the platform should reject the pair if either half is missing rather than accepting a partial.

```
POST /api/v1/exam-papers/

{
  "external_id": "ct_<uuid>",          // the tool's id, so re-publish updates rather than duplicates
  "title": "Life Sciences P1 — Mock A",
  "kind": "exam_paper",                 // exam_paper | quiz | flashcard_set

  "education_level": "high_school",     // see enum note below
  "grade": 12,
  "subject": "Life Sciences",
  "curriculum": "CAPS",
  "language": "en",                     // see language note below

  "total_marks": 150,
  "duration_minutes": 150,

  "sections": [
    {
      "name": "Section A",
      "marks": 20,
      "questions": [
        {
          "number": "1.1",
          "type": "multiple_choice",     // see question-type note below
          "marks": 2,
          "text": "...",
          "options": ["...", "...", "...", "..."],
          "answer_text": "B",            // kept, so today's readers keep working
          "memo": {                      // see "The memo is a list" below
            "points": [{ "text": "B", "marks": 2 }],
            "any_of": null,
            "marker_note": null
          },
          "cognitive_level": "L1",
          "topic": "DNA structure"
        }
      ]
    }
  ],

  "audience": "open",                   // open | institution | class
  "institution_id": null,               // required when audience != open
  "class_id": null,                     // required when audience == class
  "availability": {
    "mode": "now",                      // now | scheduled | timed_window
    "opens_at": null,
    "closes_at": null
  },

  "provenance": {
    "generated_from": ["Life Sciences P1 Nov 2025", "Life Sciences P1 Nov 2024"],
    "agent_check": "passed",             // passed | flagged
    "approved_by": "curriculum_team_user_id",
    "approved_at": "2026-09-09T11:20:00Z"
  }
}
```

**Response:** `201` with `{ "id", "external_id", "url" }`. The `url` is what a learner opens.

**Idempotency:** `external_id` is the key. A second POST with the same `external_id` is an update, not a new paper. This matters because the curriculum team will re-publish after fixing a flagged question.

**Unpublish:** `DELETE /api/v1/exam-papers/{external_id}/` should soft-delete — withdraw it from learners but keep attempts, or the results history breaks.

---

## Direction 2 — Results (platform → tool)

The tool needs to see how a published paper performed. Two reasons: the curriculum team learns which generated questions were bad, and teachers need their own class's breakdown.

**The data is already there, and richer than this endpoint needs.** Verified in the repo:

- `models/quiz.py` — `QuizAttempt` carries `score`, `percentage`, `time_taken_seconds`, `is_completed`
- `models/quiz.py` — `QuizAnswer` carries **per-question `is_correct` and `marks_awarded`**
- `routers/quizzes.py:72` writes attempts server-side; `routers/students.py` joins them per student; `admin/Students.tsx` and `admin/Analytics.tsx` already show them to educators

So `QuizAnswer.is_correct` answers the open question this document used to ask. What is missing is only the **aggregate read scoped to one published paper** — the rows exist, nothing rolls them up per `external_id`.

⚠️ Note on the curriculum tool's own UI: it currently shows no attempt figures at all. That is a **product decision, not a platform limitation** — the published list there is the tool's record of what it made, and nothing more. If the loop below is built, the tool has somewhere to put it; until then the absence is deliberate. Do not read the tool's silence as evidence the data is unavailable.

```
GET /api/v1/exam-papers/{external_id}/results/?scope=all|institution|class&class_id=

{
  "attempts": 214,
  "mean_pct": 61,
  "median_pct": 63,
  "sections": [
    { "name": "Section A", "mean_pct": 74 },
    { "name": "Section B", "mean_pct": 58 },
    { "name": "Section C", "mean_pct": 49 }
  ],
  "questions": [
    { "number": "7.2", "correct_pct": 27, "topic": "meiosis and non-disjunction" },
    { "number": "1.4", "correct_pct": 92, "topic": "DNA base pairing" }
  ]
}
```

**Aggregates only, never learner rows.** The curriculum team is QAing questions, not monitoring students. A teacher scoped to their class is the only case where individual results are appropriate, and that view belongs on the platform, not here.

**Per-question `correct_pct` is the valuable field.** A question that 27% of learners got right is either genuinely hard or badly worded, and the curriculum team is the only group who can tell which. Without this, generated papers never improve.

---

## The memo is a list, not a string

This is the most consequential difference between the two systems, so it gets worked examples rather than a field name.

### What the platform does today

`services/extraction.py` reduces a memo to one string per question. Its own instruction to the parser:

> REMOVE from values: ✓✗√✔☑ ticks, (2)/[2] mark brackets, "Accept any N of the following", "Any ONE/FOUR", "OR", "NOTE TO MARKER"

What survives is `answer_text` — a bare string. `"B"`. `"photosynthesis / chlorophyll"`. `memo_validator.py` then scores question-to-answer alignment into `memo_match_score`, repairing below 0.60.

That is a sound design for the job it was built for: extracting answers from somebody else's memo so a student can be auto-marked on MCQs. It is not sufficient for a memo the tool *generates*.

### Why, in four questions

**MCQ, 2 marks.** *"Which of the following describes meiosis?"* → memo `B` → `answer_text = "B"` → auto-marked. Works exactly as intended.

**Short answer, 2 marks.** *"Name the hormone that stimulates uterine contractions."* → memo `Oxytocin ✓✓` → ticks stripped → `"Oxytocin"` → student types it, 2 marks. Works: both marks ride on one fact, so flattening loses nothing.

**Structured, 4 marks.** *"Explain how ADH regulates water balance. (4)"* The real memo carries four separate mark-bearing points:

- ADH is secreted by the posterior pituitary ✓
- it increases permeability of the kidney tubules ✓
- more water is reabsorbed into the blood ✓
- less urine is produced ✓

Flattened, that becomes one string and **the mark boundaries are gone**. A learner who writes two of the four points has earned 2 of 4, and nothing in the schema can express that. It is four marks or none.

**Essay, 20 marks.** Section C is a rubric — content marks against expected points, plus synthesis marks for structure and coherence. There is no representation for this at all.

### The consequence, stated plainly

In Life Sciences P1, Sections B and C are **130 of 150 marks**. If the platform cannot part-mark, the tool will generate papers that are correct, template-faithful, human-approved — and unusable as assessments, because only Section A can be marked.

### What the tool sends instead

Every question's memo is an ordered list of mark-bearing points. The marks on the points sum to the question's marks.

```json
{
  "number": "3.2",
  "marks": 4,
  "type": "structured",
  "text": "Explain how ADH regulates water balance.",
  "memo": {
    "points": [
      { "text": "ADH is secreted by the posterior pituitary", "marks": 1 },
      { "text": "it increases permeability of the kidney tubules", "marks": 1 },
      { "text": "more water is reabsorbed into the blood", "marks": 1 },
      { "text": "less urine is produced", "marks": 1,
        "alternatives": ["more concentrated urine is produced"] }
    ],
    "any_of": null,
    "marker_note": null
  }
}
```

Three fields carry the conventions the flattening destroys:

- `alternatives` — wording the marker accepts for that point, replacing the discarded "OR"
- `any_of` — an integer when the memo reads "any 3 of the following", replacing the discarded "Accept any N"
- `marker_note` — replacing the discarded "NOTE TO MARKER"

An MCQ degenerates to a single point worth the full marks, so one shape covers every question type.

An essay carries its rubric the same way, with `marks` summing to the content total and a final synthesis point.

### Why this removes a control rather than adding one

An earlier draft of the generator offered "how much the memo explains" — answers only, standard, full working. That was wrong, and the reason is worth recording so it does not come back.

Verbosity is not a property of the memo. It is a property of **who is reading it**. One structure serves three readers with no setting at all:

- **the marker** reads the points as a memo, in DBE convention
- **the platform** marks against the points, so partial credit works
- **a learner afterwards** gets the working rendered from the same points

So verbosity becomes a rendering choice at the moment of reading, not a generation choice. The control was asking at generation time about something decided at reading time.

### Required

`answer_text` stays, populated with the joined point text, so everything reading it today keeps working. The structured memo lands alongside it as a new field. Nothing breaks on day one; part-marking becomes possible when the marker starts reading the new field.

---

## Three places the platform changes

### 1. Three levels, not five — and `primary` is not one of them

**Decided.** The tool offers exactly three, and the platform should match:

| `education_level` | Years |
|---|---|
| `secondary` | Grade 12 only (the NSC is written once) |
| `vocational` | NC(V) Levels 2–4 · NATED N4–N6 · occupational trade test |
| `university` | Undergraduate years 1–4, Postgraduate |

⚠️ **Do not add `primary_school`.** An earlier draft of this document asked for it; that is superseded. Primary is out of scope.

**What TVET needs that the current schema has no room for:** its three programme families do not share a ladder. NC(V) runs Levels, NATED runs N-levels, and an occupational programme has no year at all — it ends in a trade test. So the year is a property of the **programme**, not of the level.

**The four fields, exactly:**

```
education_level  enum   "secondary" | "vocational" | "university"        not null
curriculum       enum   "CAPS" | "IEB" | "DHET" | "Institutional"        not null
programme        enum   nullable — required when education_level = "vocational", null otherwise
level_detail     string not null — must be one of the programme's own years, below
```

**`programme`, the three TVET families:**

```
"ncv"           National Certificate (Vocational)
"nated"         NATED (Report 191)
"occupational"  Occupational & Skills Programmes
```

**`level_detail`, validated per programme — nothing else is accepted:**

| `programme` | Accepted `level_detail` | Awarding body |
|---|---|---|
| `ncv` | `Level 2` · `Level 3` · `Level 4` | DHET |
| `nated` | `N4` · `N5` · `N6` | DHET |
| `occupational` | `Trade test` | QCTO / NAMB |

For `secondary`, `programme` is null and `level_detail` is `Grade 12` — the NSC is written once. For `university`, `level_detail` is `1st year`…`4th year`.

⚠️ **Validate the pair, not the parts.** `programme: "nated"` with `level_detail: "Level 3"` is a well-formed row that means nothing, and it is exactly the mistake that serves an N6 paper to a first-year NC(V) student. Reject it.

**Subjects per programme** are in the tool's `LEVELS` constant (`Exam Missions.dc.html`) and should be lifted verbatim — 12 NC(V) programmes, 10 NATED, 7 occupational trades. Copy the strings; do not retype them.

**Migrate additively:** add the fields, backfill, write both for a period, move readers across one at a time, drop the old field only when nothing reads it.

### 2. `language` has no column

Currently deferred by product, but worth recording the shape now so the corpus never needs re-tagging.

The requirement is broader than papers: it is the language *all generated content* is produced in, including the agent's own replies. So `language` belongs on the generation request, not only on the artifact.

**Required:** `language` on the paper/quiz models, ISO 639-1, defaulting to `en`.

### 3. Every question type must be servable — not just multiple choice

**Decided, and this one gates everything.** Generation currently accepts `multiple_choice` only. Real CAPS and NATED papers are mostly not that: Life Sciences P1 Section B is structured and essay; a NATED engineering paper is almost entirely calculation with method marks.

If the platform can only serve MCQs, **two thirds of every generated paper is unservable** and the tool is producing content nobody can sit.

**Serve and mark all nine.** The payload each one carries, verbatim from the working papers:

```jsonc
// every question, whatever the type
{ "number": "1.4.3",            // the paper's own numbering, never renumbered
  "type":   "…",                // one of the nine below
  "marks":  2,
  "marking": "answer" | "criteria" | "method",
  "text":   "…",
  "figure": "diagram-1.4.png",  // optional
  "note":   "…",                // optional — what the figure shows that the memo relies on
  "hints":  ["…", "…"] }        // shown after a miss, never pointing at a wrong answer

"multiple_choice"  options: string[]            answer: 0-based index
"short_answer"     answer: string[]             // every accepted spelling, matched loosely
"calculation"      answer: number   unit: "m"   tolerance: 0.002   // comma-decimal accepted
"select_n"         options: string[]  count: 3  pool: number[]     // any `count` from `pool`
"list"             count: 2  pool: string[][]   // each inner array = one answer's spellings
"sequence"         options: string[]            answer: number[]   // exact order
"label"            letters: string[]            answer: { letter, name: string[] }
"written"          criteria: string[]           // the memo's mark-per-point list
"drawing"          criteria: [string, number][]  memo: string
```

⚠️ **`answer` is optional on `calculation`.** When absent, `marking` must be `"method"` — see below.

**Player name → platform name.** The paper files use short names; the platform should use the long ones:

| player `t` | platform `type` |
|---|---|
| `mcq` | `multiple_choice` |
| `term` | `short_answer` |
| `num` | `calculation` |
| `pickn` | `select_n` |
| `list` | `list` |
| `order` | `sequence` |
| `lettername` | `label` |
| `rubric` | `written` |
| `draw` | `drawing` |

`methodOnly: true` in a paper file is `marking: "method"` on the platform.

Measured across the two papers transcribed so far — Life Sciences P1 (NSC, 150 marks) and Fluid Mechanics N6 (NATED, 100 marks):

| Type | Share of LS P1 | Share of FM N6 | Marking |
|---|---|---|---|
| `rubric` — written answer | **37%** | **94%** | memo awards a mark per point; scored against those criteria |
| `term` — supply the term | 22% | — | auto, against accepted spellings |
| `multiple_choice` | 18% | — | auto, against the key |
| `lettername` — letter **and** name | 8% | — | auto, both halves must match |
| `draw` — drawing / labelling | 6% | — | criteria-scored, like `rubric` |
| `list` — name N things | 3% | 4% | auto, order-independent, N of a pool |
| `num` — calculation | 3% | 2% | auto within tolerance; **method marks** where the memo gives them |
| `pickn` — pick N letters | 2% | — | auto |
| `order` — sequence | 1% | — | auto |

⚠️ **This is the whole argument for the ask.** An MCQ-only platform serves **18% of Life Sciences P1 and 0% of the NATED paper**. Not "most of a paper" — none of it, for an entire programme family.

**`rubric` is the type that matters most and the one usually left out.** It is the single largest category in both papers and the overwhelming majority of the NATED one. It is not free text scored by a model: the memo already awards a mark per point, so the criteria are the marking scheme. The player scores against those criteria directly, which is why it needs no human in the loop per attempt.

### TVET is marked on method, not on answers

This is the part a type list alone cannot express, and it is why the NATED paper needs saying separately.

In Fluid Mechanics N6, **30 of 32 questions carry `methodOnly`** and **31 of 32 carry an explicit method**. A question reads:

> A pipeline 720 m long connects two reservoirs with an 8 m difference in level… Determine the discharge. **(3)**
>
> — Apply the Darcy friction formula hf = 4fLV²/(2gd) with hf = 8 m
> — Substitute f = 0,01, L = 720 m, d = 1,2 m and solve for V
> — Q = A × V, with A = πd²/4

Three marks, three steps. A student who applies Darcy correctly and fumbles the arithmetic **earns two of three**. A platform that stores one right answer per question scores that as zero, and the paper becomes unusable for the exact learners it is for.

**So `marking` is orthogonal to `type`.** The same `calculation` is answer-marked in an NSC paper and method-marked in a NATED one:

```
question {
  type:    "multiple_choice" | "short_answer" | "calculation" | "written" |
           "list" | "sequence" | "select_n" | "label" | "drawing"
  marking: "answer"      // auto, against a key or a tolerance
         | "criteria"    // memo awards a mark per point — NSC written answers
         | "method"      // marks per step — the NATED default
  marks:   3
  method:  ["Apply Darcy hf = 4fLV²/(2gd)…", "Substitute and solve for V", "Q = A × V"]
  answer:  0.225         // optional — absent when no memo was published
  tolerance: 0.002
}
```

**`method[]` is the field that does not exist today and must.** Without it there is nowhere to put the three steps, and partial credit has nothing to score against.

⚠️ **A NATED paper may ship with no memo at all.** The November 2022 Fluid Mechanics paper did — DHET published the questions and no marking guideline. That is why `answer` has to be optional: inventing a rounding convention marks a student wrong for being right. When `answer` is absent, `marking` must be `"method"` and the platform must say so on the paper.

Anything auto-marked needs an answer key; anything model-marked needs the memo note surfaced to the marker, and must be labelled as model-marked so two runs differing is expected rather than a bug.

---

## Subject list

The tool ships subject catalogues per level as a **design proposal**, not a mirror of the platform.

The platform's `Subject` table has one verified row (`aixr` / AI and XR Fundamentals). Migration `0009` records the other fixture subjects as `verified: false` — invented or third-party-scraped — and holds them in the frontend fixture until confirmed.

So there is no academic subject list in either repo to defer to. The tool's catalogues need confirming against the DBE subject lists, and the confirmed ones should then be written back as global `Subject` rows (`institution = NULL`).

Until then, `subject` travels as a string.

---

## Three rules the player learned the hard way

Found by playing both papers end to end and checking a perfect run scores the paper's own total. Each one silently under-marked a student before it was fixed.

**1. A question's tick criteria must sum to its marks.** Method steps were weighted 1 each, so a 6-mark question with 4 steps could only ever earn 4. **17% of the NATED paper was unreachable** — a perfect student maxed at 83/100. Weights are now spread across the steps so the total is always reachable.

**2. There are three rubric shapes, and they are not interchangeable.**

| Shape | When | Marking |
|---|---|---|
| a mark per point | steps === marks | tick each |
| **any N of M** | memo lists more points than marks — "State THREE ways", seven options | each worth 1, caps at the marks |
| **weighted steps** | steps < marks — the NATED default | marks spread across the steps |

The middle one must say so on screen. A student who ticks all seven of a 3-mark question and scores 3 will otherwise think the marking is broken.

**3. Accepted answers may be a string or a list of spellings.** A pool written as `["radial flow", "axial flow"]` and one written as `[["ovary","ovaries"], …]` are both natural, and assuming the second crashed every question authored the first way. Accept either.

## TVET coverage — what is proven and what is not

| Family | Ladder | Papers transcribed | Schema status |
|---|---|---|---|
| NATED (Report 191) | N4–N6 | **1** — Fluid Mechanics N6, Nov 2022 | method-marking proven against a real paper |
| NC(V) | Levels 2–4 | **0** | **assumed** — no paper read |
| Occupational / trade test | trade test | **0** | **assumed** — assessment may not be a written paper at all |

⚠️ The schema above is derived from **one** NATED paper. It is the right shape for that paper and almost certainly for its siblings, because N4–N6 engineering subjects share a house style. It is **not** evidence for the other two families.

**NC(V) is not NATED.** It is a school-equivalent qualification carrying internal assessment alongside the external paper, so the unit of delivery may not be "a paper" at all.

**An occupational programme ends in a trade test**, which is practical and observed. A schema built for written questions may be the wrong tool entirely — worth confirming these belong in this product before designing for them.

**Ask:** one NC(V) Level 4 paper and one trade-test assessment guide. Two documents settle both.

## TVET — the build order

Focus is TVET, and the three families are not equal work. NATED is the one with a transcribed paper and a proven shape, so it goes first.

### 1 · NATED (Report 191) — build this now

Ten programmes, N4–N6, DHET. Almost entirely `calculation` and `written`, almost entirely **method-marked**.

What it needs beyond the common payload:

```jsonc
{ "type": "calculation", "marks": 2, "marking": "method",
  "answer": 0.225, "unit": "m", "tolerance": 0.002,   // answer OPTIONAL
  "method": ["m = A / P = d / 4 for a circular pipe running full"] }
```

⚠️ **`method[]` is the field that does not exist today.** Without it the three steps of a three-mark question have nowhere to live, and partial credit has nothing to score against. It is the single highest-value addition in this document.

**Mark arithmetic:** `marks_awarded = (steps the student got) × (marks ÷ steps)`, rounded to the paper's convention. A three-mark question with three method steps pays 1 per step. Where `steps ≠ marks`, distribute evenly and round down — never award more than `marks`.

### 2 · NC(V) — needs one paper before building

Twelve programmes, Levels 2–4, DHET. Schema is **assumed** — no paper read.

NC(V) carries **internal assessment (ICASS) alongside the external paper**, so a learner's result is not the paper's result. Two consequences worth settling before the schema hardens:

- the unit of delivery may be a **subject across a level**, not a single paper
- the platform may need to hold a mark that did not come from a paper at all

**Needed:** one NC(V) Level 4 external paper with its marking guideline.

### 3 · Occupational / trade test — do not build yet

Seven trades, assessed by **QCTO / NAMB**. A trade test is **practical and observed** — a candidate welds a joint and an assessor watches.

⚠️ **A written-question schema is probably the wrong tool for this entirely.** Serving it as questions would misrepresent how the qualification is actually earned. The honest options are an observation checklist (a different model), or leaving it out of scope.

**Needed:** one trade-test assessment guide, to decide which.

### What this means for the enum

All three `programme` values ship now, because the tool already offers them and a learner picking `occupational` must get an honest empty state rather than a 404. Only `nated` carries papers at first.

## Still open

Two of these were mine to answer and now are. What remains needs someone who knows the platform, or a document I have not seen.

1. ~~Which question types can the platform serve?~~ **Specified** — nine types with their exact payloads in §3, and `marking` (`answer` / `criteria` / `method`) as a separate field. Nothing left to decide; `method[]` is the one genuinely new column.
2. ~~The level vocabulary~~ **Specified** — three `education_level` values, three `programme` values, and `level_detail` validated against the programme, all in §1. Validate the pair.
3. Is `external_id` an acceptable idempotency key, or does the platform prefer its own?
4. ~~Does `QuizAttempt` record per-question correctness?~~ **Answered from the repo: yes** — `QuizAnswer.is_correct` and `.marks_awarded`, one row per question per attempt. No schema change needed for the results endpoint; only the aggregate query.
5. For `audience: class`, is there an existing class/enrolment model to scope against?
6. ~~Who owns the DBE Terms of Use review?~~ **Confirmed** — DBE past papers are cleared for this use. The pipeline still derives structure and generates new items rather than redistributing paper text.
