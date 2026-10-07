# Exam Practice: the question-type catalogue (as built, 2026-10-03)

The learner app turns a past exam paper into interactive practice. Every marks-bearing question part is rendered by ONE of these
types and auto-marked against the official memo. Judge each question part against THIS list only.

| type | what the learner does | marked how | settings it already takes |
|---|---|---|---|
| mcq | taps one of 2-6 option cards (text, optional image above the stem) | exact | options, the answer index, an image |
| pickn | picks N of several options | each right pick scores | options, N, the right set |
| order | taps options into a sequence | whole sequence exact | the items, the order |
| term | types one term / short phrase (one line) | exact or close spelling (1 slip per 5 letters), list of accepted synonyms; `strict`: letters and digits exact (spacing and punctuation free), for IUPAC names, formulas and cell notation, where one letter is another compound (hexane / hexene) | accepted answers, strict |
| lettername | picks a LETTER label on a diagram, then types the part's NAME | letter exact + name as term | the letters, the answer |
| num | types one number (own calculator keypad), optional unit shown | within a tolerance | value, tolerance, unit |
| steps | a calculation in numbered steps, each a NUMBER box; follow-through marks if an earlier step was wrong | per step within tolerance, follow-through | step labels, values, tolerances, follow-through formulas |
| list | N numbered one-line answers ("Name TWO ...") | each line against synonym groups, a group scores once | N, synonym groups |
| rubric (written) | free text box (Explain / Describe / Discuss); or numbered one-line slots for "State / Give THREE ..." | AI marker against the memo's marking points (each point worth 1 or 2); alternatives (OR) supported | the memo points, worth per point |
| match | pairs Column A items with Column B items | per pair | the two columns, the pairs |
| draw (self-check) | draws on paper, then ticks the memo's criteria; NOT marked online | none (not banked) | the criteria |
| build: hist | builds a histogram in steps: graph type, caption, axis labels (picked from options), Y scale step, drag bar heights | memo criteria T/C/L/S/P | groups, values, tolerance, label options, scale options |
| build: stems | for each labelled item in a diagram, picks one of a few end-states | one mark per item | items, states, answers |

Shared context the app already shows: a lead line, an extract (text) as a sheet, data TABLES (rows and columns, read-only),
figures (an image with optional tappable letter hotspots), the question paper and memo as page images.

NOT supported today (examples): a table the learner FILLS IN, a line/scatter graph to plot on a grid, algebra/expression input
with symbols (fractions, exponents, roots), a sketch of a function, geometry constructions or proofs, map reading ON a map
(coordinates, bearings, measuring distance), long essays with structure (intro/body/conclusion) beyond one free box, accounting
ledgers / journals, an engineering drawing to scale, a multi-part answer that mixes types inside one part.
