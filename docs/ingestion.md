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
  - `mcq.ab{a, b}`: COLUMN I / COLUMN II ("A only, B only, both A and B, none", LS P1 1.3 every sitting): COLUMN II's two items,
    with `q` as COLUMN I's description and `opts` exactly A only / B only / Both A and B / None (the validator checks). The page draws
    it as a Venn: the two items are its circles, and the learner taps the region the description belongs to.
  - `lettername.or[{letter, name[]}]`: other pairs the memo accepts instead (1.4.1(a): C – urethra OR D – penis).
  - `letternames{letters, count, pool[{letter, name[]}]}`: the LETTERS and NAMES of `count` parts in one numbered part, any order
    (1.5.2); one row per part, a letter on another row is dimmed (a tap moves it), 2 marks per part.
  - **Letter + name marking** (both, one helper `pairMarks`, Murci 2026-10-05): a letter earns its mark when it is one of the memo's
    letters; the name earns its mark only when it names THE PART OF THAT LETTER ("C – penis" = 1 of 2). A row whose letter is none
    of them is marked on its name alone (as a single letter + name always was). Each memo part counts once. A Life Sciences
    teacher should confirm the rule. The exam service marks the platform's attempts: it needs the same rule and types (not yet).
  - **`list.pool` is authored for its matcher:** each memo point is a group of accepted answers, and an answer scores a group when
    it holds the FIRST WORD of one of them (a substring test, so "protect" also takes "protected"). So every accepted answer must
    LEAD with a word only that point uses: `["body (the cell body is at one end)", "soma"]`, never `"cell body"` (any answer with
    "cell" scored, LS P1 Nov 2024 2.5.2) nor a lead word like "the", "same", "no", "many". The words after the first are what the
    memo shows (the group's first entry). A stand-in until the AI marker (Ollama) marks written lists.
  - `rubric.must[]`: the indexes of COMPULSORY points (the memo's "Compulsory mark * (1) + Any (5)", LS P1 Nov 2024 2.1.3). Each
    earns its own mark and nothing stands in for it: the other points together earn at most the marks less the compulsory ones
    (no "oogenesis" = 5 of 6 at most). The memo shows a compulsory point with its "*". The exam service needs the same rule.
  - `draw.build{kind:"hist", want, groups, answers, tol, top, steps, okSteps, snap, x, y, capWords, typeQ, typeHint, unit}`: a graph
    the memo marks T C L S P (type, caption, labels, scale, plotting) is BUILT on the phone, one criterion a step (LS P1 June 2026 3.1.3
    histogram; Nov 2025 2.3.4 bar graph). `want` is the right type (a wrong type loses T and S, as the memo rules); `x` / `y` are the
    axis label choices, the right one first; `capWords` are word groups the caption needs one of each; `snap` is what a drag moves to.
  - `genotype{alleles, count, pool}` (LS P2 Nov 2025 2.3.3(b), 2.4.2): genotypes BUILT from the paper's alleles on sockets filled
    from a tray, never typed. A typed genotype was lost twice: `term` folds case (`DD` passed for `dd`) and `list` keeps a-z only
    and tests "contains" (a wrong `IBIA` held "ibi" and earned the Iᴮi mark). Alleles are the paper's tokens with Unicode
    superscripts (Iᴮ, Xʰ), compared exactly; a genotype is its two alleles in any order; each memo genotype counts once. When the
    paper prints no symbols, the tray offers the system's WHOLE set (Iᴬ Iᴮ i): it shows the notation, not the answer.
  - `draw.build{kind:"cross", alleles, phenos, parents[{pheno, geno}], offspring[{geno, pheno}]}` (LS P2 Nov 2025 2.5.4): a
    monohybrid cross BUILT on a Punnett square. Only the two parents and the genotype -> phenotype key are data; the marker
    derives the gametes, the four offspring, their phenotypes and the ratio, so the data cannot contradict itself (the validator
    derives them too and refuses a cross with an offspring the key does not name). Marked on the memo's 8 points: P1 phenotypes,
    P1 genotypes, gametes, F1 genotypes, F1 phenotypes, ratio (COMPULSORY, and only with the right phenotypes; 2 : 2 is 1 : 1),
    P1 and F1, meiosis and fertilisation; the ratio's mark + at most marks - 1 from the other seven. The learner places the four
    labels on a rail (the memo marks them: printing them gives two marks away). The square may be either way round. Its criteria
    stay OUT of the part during play (they name the answers) and show in the memo at the end. The memo's gamete-line layout is
    not offered: the square earns the same two marks.
  - **Where an `mcq` plays:** in the MCQ card component, except when its options are all single letters (they play as letter balls
    on the page, as every letter pick does) or its mission has a `table` (the component shows an extract, not a table; LS P1 Nov
    2024 3.3.3). On the page an MCQ answers on the tap, as a card does.
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
- A `steps` label is on screen while the learner works, so it names the quantity and its unit only ("Percentage increase (%)").
  A label with working between numbers (`721 ÷ 609`) or any step's answer in it is an `error`: the memo marks that working
  (caught in LS P1 Nov 2025 2.5.4 and LS P2 Nov 2025 3.2.4, 2026-10-06).

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
# a hand transcription (no API call): LS P1 Nov 2024; the same for ls_p1_2025_11 and ls_p2_2025_11
python tools/ingest/transcribe_ls_p1_2024_11.py && python tools/ingest/ingest.py PAPER.pdf MEMO.pdf --id ls-p1-2024-11 --from-json
```
**Hand transcriptions** (`transcribe_*.py`) are the source and are committed, like `paper-ls-p1-2026.js`; their `out/` is
regenerated. They write `response.json` in the catalogue format, so they pass the same schema and semantic checks as an AI run.
What the catalogue cannot hold yet is flagged in the data (`flags`), never silently bent. LS P1 Nov 2024 Question 1 had three such
parts (1.1.6 table options, 1.4.1(a) alternative pairs, 1.5.2 two pairs in one part); the catalogue now holds all three.
Known limits: steps lose follow-through formulas (functions are not data); the stems builder is not in the catalogue (the
histogram, genotype and cross builders are; other drawings ingest as self-check); scanned PDFs rely on the model's vision (Mathematics, Maths Lit); resources not in the PDF (map
sheets) must be added by hand. A dihybrid cross (a 4 x 4 square) and a cross asked as a percentage chance still ingest as a
self-check `draw`.
