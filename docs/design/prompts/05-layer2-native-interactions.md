# Build prompt 5: layer 2, native interaction for every question type

Agreed with Murci, 2026-09-27: **design for the question type and the way a paper is taken, never for one subject.**

The three layers:
1. **Universal input**, built already.
2. **Native interaction per question type.** This brief.
3. **Optional scenes per subject family**, later.

The order is layer 2, then one scene per family as a proof (engineering pipes, biology figure), then the sitting modes.

**Target:** `C:\Users\mokon\Downloads\3rd design\Exam Practice.dc.html`, local git repo, screen `03 Mission`.

**Keep the page-3 shell exactly as built (7ed6e54):**
- the lesson header;
- the companion and its reactions;
- the feedback bar;
- stamps;
- the room glow;
- the chimes.

This brief replaces only the answer area inside the question column.

---

## Why
The papers are very different. Marks by type, from the papers' own data:

| Paper | Marks by type |
|---|---|
| Fluid Mechanics N6 | steps 93 · list 4 · rubric 3 |
| AET L4 | steps 34 · rubric 34 · list 14 · match 10 · draw 8 |
| Life Sciences P1 (design sample, NSC) | rubric 55 · term 33 · mcq 27 · lettername 12 · draw 9 · list 5 · num 4 · pickn 3 · order 2 |

Build each question type once, well, and every paper, present or future, gets a good experience with no extra authoring.

## Shared rules (every question type)
1. **The answer shape does not change.** Each interaction produces exactly the `answer` in `docs/API.md` (the table under "POST … /responses"). The mock marker and the service stay as they are.
2. **Tap first, type only when the answer is words or numbers.**
   - Targets are at least 44 px; tiles are at least 52 px tall on phones.
   - Everything works by tap alone. There is no drag-only interaction: where drag is offered, tap does the same job.
   - Everything works by keyboard too (Tab, Space or Enter, and arrow keys where there's a list of choices).
3. **Check is enabled only when the answer is complete enough to mark**, per question type (see below). When it's disabled, the footer says why, for example "Pick 3 · 1 picked".
4. **Stamps after Check** use each type's own `items[].key` from the reply. They're shown on the element the learner touched (the tile, chip, card or line), as an icon plus text, never colour alone. They clear when that element is changed for the next try.
5. **Locked while the bar is open**, and after the part closes (the same rule as now).
6. **Sitting-mode switch.** A `sitting` prop, `practice` (default) or `hall`.
   - In the Hall there are no stamps or instant verdicts; the calculator stays and the coach goes (see below).
   - This brief builds the practice behaviour and the switch. The Hall screen itself is later.
7. **Reduced motion:** no springs or flights; state changes are instant.
8. **Brand only:**
   - the three blues and the `#81b1ff` tint;
   - success `#3ddc97`, amber `#e0a10f`, error `#f2777a`;
   - no emoji;
   - never position with `transform` on anything that also animates.

## Per question type

### `mcq`: pick one (Life Sciences 1.1.x)
- **Big answer tiles,** one per option, labelled A, B, C, D (the option order is the paper's), each with the full option text.
- **Picking:** tap to select, with a tile spring and the azure outline. Tapping again changes the choice. The tiles are a radio group (arrow keys move, Space selects).
- **Answer:** the option index. **Check:** enabled after one pick.
- **After Check:**
  - the picked tile gets ✓ or ✕;
  - a wrong pick is never followed by showing the right tile until the part closes;
  - on close, the correct tile gets "✓ memo".

### `pickn`: pick exactly N (Life Sciences 1.4.2)
- **Tiles as above, but a checkbox group,** with a counter "Pick 3 · 2 picked".
- **Limit:** a fourth tap is refused with a gentle shake, and the counter says "Pick 3: unpick one first".
- **Answer:** the array of indices. **Check:** enabled at exactly N.
- **After Check:** each picked tile stamped ✓ or ✕.

### `term`: type a term (Life Sciences 1.2.x)
- **One field** with the command line from the stem ("Give the correct biological term").
- **Input:** `autocapitalize="off"` and `spellcheck="false"` (the marker already accepts small slips).
- **Answer:** the text. **Check:** enabled when non-empty.
- **After Check:** the field is stamped ✓ or ✕. A near-miss the marker accepted still shows ✓, and the memo spelling appears only on close.

### `list`: name N things (Life Sciences 1.4.3; FM 4.2; AET 1.2 and 3.1.2)
- **Chip entry.** One field, and Enter or a comma turns the entry into a numbered chip ("1 · axial flow").
  - Tap a chip to edit it; ✕ on a chip removes it.
  - Shows "2 of 4 named".
  - At N chips the field hides, and "Change one" reopens it.
- **Answer:** the array of chip texts. **Check:** enabled at one chip or more.
- **After Check:** each chip stamped ✓ or ✕.
  - The marker counts only the first N (a service rule), so chips beyond N are never possible.
  - Duplicates the marker refused (for example two gears that are synonyms) are stamped "same as 1".

### `order`: put in order (Life Sciences 1.5.4)
- **Cards in the paper's order.** Tap cards in the order you choose; each gets a numbered badge 1, 2, 3, and a strip on top shows the growing sequence.
- **Changing it:** tap a numbered card to take it and everything after it back out. Drag to reorder is optional; tap does everything.
- **Answer:** the array of indices in the chosen order. **Check:** enabled when every card has a number.
- **After Check:** each position stamped ✓ or ✕ (the service marks whole or per position, whichever its judge returns).

### `lettername`: letter plus name (Life Sciences 1.6.2)
- **When a figure exists** (`figure_refs`): show the figure large and tappable, with each letter as a hotspot chip. Tap a letter chip (or pick it from the letter row under the figure), then type its name in the field that appears.
- **When the figure isn't available yet:** a row of letter tiles plus the name field, and a "Figure" button that opens the paper kit's figure.
- **Answer:** `{letter, name}`. **Check:** enabled when both are given.
- **After Check:** two stamps, "letter ✓/✕" and "name ✓/✕" (the judge gives half marks for each).

### `num`: one number with a unit (Life Sciences 2.5.2)
- **The calculator keypad** (below), with the unit shown after the value. **Answer:** the text, for example "12" or "0,225 m".

### `steps`: method, one value per step (FM, AET)
- Keep the step cards, and add the **calculator keypad** (below) as the way to enter values on phones.
- **The focused step's formula line:**
  - It appears *only when the paper's own formula sheet is part of the kit*, shows the relevant sheet entry by its printed name, and never substitutes numbers.
  - It's hidden in the Hall.
  - Until the content has a mapping from step to formula-sheet entry, show "Formula sheet" as a button instead, which is today's behaviour.
- **Answer:** as now.

### The calculator keypad (shared by `num` and `steps`), the biggest efficiency win
- **An in-app keypad replaces the phone keyboard for numeric fields on phones and tablets.**
  - Tapping a numeric field opens the keypad, and the OS keyboard stays closed (`inputmode="none"`).
  - Desktop keeps normal typing, with the keypad available as a toggle.
- **Keys:** 0–9, the decimal comma, ±, ×10ⁿ, ⌫ and clear. Calculator keys: + − × ÷ ( ) √ x² and "=".
  - "=" evaluates the expression the learner typed into the display.
  - "Set" writes the display's value into the focused field.
  - Showing the expression is fine. The learner builds it; the app never fills in a formula or a given value on its own.
- **Chips above the keypad.** Tapping a chip types its number into the display:
  - **Givens** from the part's `givens` (the learner view sends stem, table and instruction givens), labelled by symbol and unit ("L 720 m");
  - **your earlier values** in this part ("hf 8 m" once s1 has a value), exactly as typed.
  - There are no chips for anything the learner hasn't been given or entered.
- **Numbers:** the SA decimal comma is the default display, and a point is accepted too. The value sent is exactly what the field shows.
  - **Standard form** (built 2026-10-07): a value typed as `1,045×10^15` stays as typed after Set. A result of 10⁹ or more, or below 0,001, is written the same way (`3,978×10^-19`), never rounded to "0". The marker reads `×10^` and `e` alike.
  - The display reads left to right ("1,045×10^15"). It keeps the newest digits in view when long, but the expression is never mirrored.
- **In the Hall:** keypad and chips stay (a permitted exam calculator); formula lines go.
- **Rule note:** earlier briefs said "the app never calculates for the learner". This keypad is the learner's own calculator, operated by them, like the scientific calculator permitted in the exam room.

### `match`: two columns (AET 4.2)
- **Two columns.** Tap a left item, then its description; a line connects them. On phones the columns stack, and the pairing shows as a letter badge on the left item.
- **Unpairing:** tap a paired item to unpair it. One description is a decoy, and the note says so.
- **Answer:** the array of right indices (or null). **Check:** enabled at one pair or more.
- **After Check:** each left item stamped (as now).

### `rubric`: a written answer (Life Sciences 2.1.4; AET)
- **The command-word coach.** A strip above the textarea, taken from the stem's command word:

  | Command word | Coach line |
  |---|---|
  | Define | "One precise sentence: what it is." |
  | Explain | "A point, then *because* …" |
  | Describe | "What it looks like or does, step by step." |
  | Compare / Differentiate | "Both sides, one line each." |
  | Name / State / List | "Short answers, no explanation needed." |

- **Marks:** show "3 marks: aim for 3 separate points".
- **No live score, no keyword hints and no memo words**, same as now. The coach speaks only about the *shape* of an answer.
- **Answer:** text, at most 2 500 characters, with a counter.
- **In the Hall** the coach is hidden.

### `draw`: on paper (Life Sciences, AET 2.1 and 2.3)
- As built (I've drawn it, then criteria), with one addition: a small printable-sized preview of the axes or scale from the stem, if present (text only for now). A photo upload is a later feature, not in this brief.

## Design sample for the question types FM and AET lack
- Wire `paper-ls-p1-2026.js` (already in the design folder) into the practice prototype as a third paper.
- It carries mcq, term, pickn, list, order, lettername, rubric, num and draw.
- Label it everywhere as **"Life Sciences P1 · NSC Grade 12 · design sample"**. It's for testing the interactions only; it isn't a TVET paper, and it isn't in the service.
- It shows in the picker's "Also on Nexera" with a "Design sample" tag.
- Map its fields to the learner view: `opts` → `options`, `count` → `count`, `letters` → `letters`, `q` → `stem`.
- The mock marker judges it from `a` / `pool` / `bullets`, the same way the page's mock does today.

## Verification (DOM, as before)
- **Every question type:** answered once correctly and once wrongly on a real part, with the expected answer shape logged against the `docs/API.md` table.
- **Check behaviour:** the Check-enabled rule and its reason text; stamps on the touched element; stamps clearing on change.
- **Input devices:** keyboard-only for mcq, pickn, order and match; the keypad writes into the right field; chips type the right numbers.
- **Sizes:** 390, 768, 1024 × 768 and 1280, with one companion and no overlaps (tiles, keypad or chips against the feedback bar).
- **The Hall switch** (`sitting="hall"`) hides stamps, the coach and the formula line, and keeps the keypad.
- **Commit** the result with what was and wasn't verified.
