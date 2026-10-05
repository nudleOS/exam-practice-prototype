# Paper ingestion (AI): question paper + memo -> playable practice

**Status (2026-10-03):** the pipeline is built and its back half is proven offline (LS P1 fixture: loads as its own paper, marks
83/83). The first real run (Life Sciences P2 Nov 2025) waits on credentials. The review routing rule (`validate.route`) is pending.
**2026-10-05:** Life Sciences P1 Nov 2024, Question 1 (Section A) is in, HAND-transcribed through the same back half (below); an MCQ
can now carry its own figure, its options as a table, and the catalogue has `letternames` and `lettername.or` (Murci's mockups).

## Purpose
Internal users upload a past paper and its memo; the app turns it into the same interactive, memo-marked practice the hand-built
Life Sciences P1 has. AI decides WHAT each question is (which catalogue type, its answers); the app's tested code decides how it
looks and how it is marked. AI never generates UI.

## Architecture and data flow
```
paper.pdf + memo.pdf
   -> ingest.py: Claude (claude-opus-5-5, vision, adaptive thinking, structured output = catalog/paper.schema.json)
   -> response.json (raw) -> validate.check: schema + semantic checks -> validate.review: auto / check / blocked per part
   -> crop_figures: page + bbox -> figures/*.png (palette PNG), a mission's figure and an MCQ's own
   -> to_app -> paper.js (window.PAPERS_INGESTED) + report.json
   -> review.html?id=<id> (a person checks) -> Exam Practice.dc.html?ingested=<id>&paper=<id>
```
In the app, `buildPapers` -> `fromData(src, meta)` builds every paper from data with its own key prefix (`<id>:<part>`); an
ingested mission's figure registers its own FIGS / SCENES entry; an MCQ's own figure rides on its part as `img` and shows under the
stem in the MCQ card (as Life Sciences P1's `QIMGS`); `HOME_TO_LOCAL[id] = id` links the paper map's catalogue entry.

## Contract
- **Catalogue** `tools/ingest/catalog/nexera-exam-catalog.v1.json` (`catalogId` `https://nexera.app/catalogs/exam/v1`): the 11 types
  (mcq, pickn, order, term, list, lettername, letternames, num, steps, rubric, draw), each a JSON Schema of its props. Follows
  A2UI's catalog convention (https://a2ui.org/concepts/catalogs/); the output is OUR paper data, not A2UI surface messages.
  - `mcq.optTable{head, rows}`: options the paper prints as a TABLE (1.1.6); one row of cells per option, in the order of `opts`
    (which stay each row read as a line: the medal card and the memo use them). The card shows one full-width row per option under
    the column heads; a screen reader hears "C: muscle in X relaxed, structure Y taut, part Z less convex".
  - `lettername.or[{letter, name[]}]`: other pairs the memo accepts instead (1.4.1(a): C – urethra OR D – penis).
  - `letternames{letters, count, pool[{letter, name[]}]}`: the LETTERS and NAMES of `count` parts in one numbered part, any order
    (1.5.2); one row per part, a letter on another row is dimmed (a tap moves it), 2 marks per part.
  - **Letter + name marking** (both, one helper `pairMarks`, Murci 2026-10-05): a letter earns its mark when it is one of the memo's
    letters; the name earns its mark only when it names THE PART OF THAT LETTER ("C – penis" = 1 of 2). A row whose letter is none
    of them is marked on its name alone (as a single letter + name always was). Each memo part counts once. A Life Sciences
    teacher should confirm the rule. The exam service marks the platform's attempts: it needs the same rule and types (not yet).
- **Output** `catalog/paper.schema.json`: `{catalog, paper{subject,title,sitting,total_marks,time}, sections[{title,total,missions[
  {id,title,kind,lead,marks,extract,table,figure{page,bbox,caption},items[component]}]}], flags[{n,kind,detail}]}`. An `mcq` may
  carry its own `figure{page,bbox,caption}` when the paper prints one for that question alone (LS P1 Nov 2024 1.1.6, 1.1.9, 1.1.10).
- **App data** (`paper.js`): the paper-ls-p1-2026.js shape plus `id`, `subject`, `catalog`; `figure{src,w,h,caption}` per mission;
  `img{src,w,h,alt}` on an MCQ with its own figure. Crops are keyed `<mission id>` and `part:<number>` (a block with one part, 4.2,
  shares its number, so the two never share a key).
- Source of truth for `catalog/*.json` is `catalog.py` (`python tools/ingest/catalog.py`).

## Error handling and observability
- API errors are caught per type (auth, bad request, rate limit, status, connection) with a plain message; `stop_reason` refusal
  or max_tokens stops the run (no partial JSON is used). Server-side `fallbacks: "default"` re-runs a safety decline.
- Each run logs the request id, model, stop reason, tokens and duration; `report.json` keeps them with the issues and flags.
- Validation issues: `error` (cannot go live) / `warn` (a person looks); the AI's own flags: low_confidence, no_fit,
  memo_issue, missing_resource, figure_unclear.

## Security
- Credentials: the SDK chain (`ANTHROPIC_API_KEY`, `ant auth login`), else `%USERPROFILE%\.nexera\anthropic.env`, OUTSIDE the
  project: the dev server serves this folder (with .git) to the phone. Never a key in the repo or in chat.
- The documents are data: the system prompt tells the model to flag, not follow, any instruction inside them.
- Output is schema-validated before it is used; `?ingested=` accepts word characters, dots and dashes only.
- `tools/ingest/out/` is git-ignored (memo answers; regenerate instead).

## Runbook
```
pip install anthropic jsonschema                      # once
python tools/ingest/catalog.py                        # after any catalogue change
python tools/ingest/ingest.py PAPER.pdf MEMO.pdf --id ls-p2-2025-11            # ~US$1-2 per paper at claude-opus-5-5
python tools/ingest/ingest.py PAPER.pdf MEMO.pdf --id ls-p2-2025-11 --from-json # re-check, free
open http://localhost:8767/tools/ingest/review.html?id=ls-p2-2025-11
# offline test of the back half
python tools/ingest/fixture_from_ls_p1.py && python tools/ingest/ingest.py "uploads/Life Sciences P1 May-June 2026 Eng.pdf" "uploads/Life Sciences P1 May-June 2026 MG Eng.pdf" --id ls-p1-fixture --from-json
# a hand transcription (no API call): LS P1 Nov 2024
python tools/ingest/transcribe_ls_p1_2024_11.py && python tools/ingest/ingest.py PAPER.pdf MEMO.pdf --id ls-p1-2024-11 --from-json
```
**Hand transcriptions** (`transcribe_*.py`) are the source and are committed, like `paper-ls-p1-2026.js`; their `out/` is
regenerated. They write `response.json` in the catalogue format, so they pass the same schema and semantic checks as an AI run.
What the catalogue cannot hold yet is flagged in the data (`flags`), never silently bent. LS P1 Nov 2024 Question 1 had three such
parts (1.1.6 table options, 1.4.1(a) alternative pairs, 1.5.2 two pairs in one part); the catalogue now holds all three.
Known limits: steps lose follow-through formulas (functions are not data); builders (histogram, stems) are not in the catalogue
(drawings ingest as self-check); scanned PDFs rely on the model's vision (Mathematics, Maths Lit); resources not in the PDF (map
sheets) must be added by hand.
