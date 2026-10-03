# Build prompt 7: layer 3, the second scene, Life Sciences figures

Agreed order (Murci, 2026-09-27):
1. layer 2 (bec9ef2);
2. the Fluid Mechanics pipe scene (1a495ae);
3. **this brief, the biology family: figures you answer on**;
4. the sitting modes.

**Target:** `C:\Users\mokon\Downloads\3rd design\Exam Practice.dc.html`, screen `03 Mission`, with a new tool in the service repo.

## What we found (measured, 2026-09-27)
- **The missions name their figure's page:** 1.4 and 1.5 are on page 8, 1.6 on page 9, 2.1 on page 10, 2.4 on page 12. The paper's own PDF is on disk (`uploads/Life Sciences P1 May-June 2026 Eng.pdf`).
- **The figures' letters are real PDF text with coordinates.** Page 9 (the inner ear) has A (283, 118), B (393, 207), C (407, 230), D (401, 309), E (219, 310) and F (220, 204), and the figure's images have their own boxes. Hotspots can therefore be **extracted, not hand-placed**.
- **The questions on these figures are all layer-2 types:**
  - letter-and-name: 1.6.2, 2.1.2, 2.4.3;
  - pick letters P–T: 1.4.2;
  - order stages A–C: 1.5.4;
  - multiple choice with letter options: 1.5.3.
- **Copyright:** the pages say "Copyright reserved" and "SC/NSC Confidential" (DBE, State copyright). Using them in this **private design prototype** matches how we already treat the papers: internal only, never published. Showing them to real learners needs DBE permission or our own redrawn figures. That's a decision for later, and nothing here publishes a figure.

## 1. A figure-extraction tool (service repo, reusable for any paper)
`tools/extract_figure.py <paper.pdf> <page> --near <question number> --out <dir>`:
1. **Finds the figure's box:** the union of the page's image boxes, plus the single-letter text spans inside or next to them. Letters in the question text (the "A" in "1.6.1 (a) A") are excluded, because they sit outside the figure cluster.
2. **Renders that box** at 3× (about 216 dpi) as PNG. It's cropped, not the whole page.
3. **Writes a hotspot file** with each letter's centre as a percentage of the crop, plus its box:
   ```json
   { "image": "p9-inner-ear.png", "w": 651, "h": 657,
     "hotspots": [ { "letter": "A", "x": 0.31, "y": 0.04, "w": 0.05, "h": 0.06 }, … ] }
   ```
4. **Also writes a review PNG** with every hotspot circled, for a human to check before use. Nothing is trusted unreviewed; that's the R1 rule.

Run it for pages 8, 9, 10 and 12. On page 8, which has several figures, pick the cluster for each mission. Output goes to `assets/figures/ls-p1-2026/` in the design folder.

## 2. The figure scene (design)
- **Where:** the same scene slot as the pipes, at the top of the question column. It's used when the mission has a `SCENES` record with `template: "figure"` and the hotspot file.
- **The figure** is shown on a light surface: the paper's line art is black on white, so it's given a white card with rounded corners inside the dark scene frame. It's full width, and pinch-zoom is allowed inside the figure.
- **Hotspots** are buttons over the printed letters, at least 36 px wide. (B and C on the inner ear are about 37 px apart on a phone, so 44 px would overlap. 36 px still passes WCAG 2.2 AA 2.5.8, which asks for 24 px.) Each is labelled "Letter B on the figure".
- **What a tap does, by question type.** It's the same state as the layer-2 controls, which stay underneath as the accessible alternative:

  | Type | Tap on a letter |
  |---|---|
  | letter-and-name | Sets the letter; the name field takes focus |
  | pick letters | Toggles the pick; the counter updates |
  | order | Appends to the sequence, with a number badge on the figure |
  | multiple choice with letters | Picks that option |

- **Before close:** only the learner's selection shows (an azure ring and the number badge). Names of parts are never shown.
- **After Check (practice):** the picked hotspots take their stamps (✓ / ✕ / "letter ✓", "name ✕").
- **After the part closes (full marks, or See the memo):** the memo's letter gets a green "✓ memo" ring. Its name appears in the memo panel as it does now.
- **Enlarge:** a button opens a dialog (focus trapped, Esc closes) with the figure at up to 2× and the same hotspots, working the same way. Closing returns focus to the Enlarge button.
- **Text alternative:** "Diagram: ⟨the mission's own sentence, e.g. 'the structure of the inner ear'⟩, with parts labelled A to F." Plus the letter list.
- **The Hall:** selecting works; stamps and the memo ring are off.

## 3. Verification
- **Tool output:**
  - one crop and one hotspot file per mission figure;
  - the review PNG shows every circle on its printed letter (check by eye, then by numbers: each hotspot centre lies inside that letter's text box from the PDF);
  - no question-text letter is included.
- **Answer shapes:**
  - a tap on the figure produces the same answer as the tile would: 1.6.2(a) → `{letter: "F", …}` after tapping F;
  - 1.4.2 picks toggle, and the limit holds;
  - 1.5.4 builds `[1, 0, 2]` by taps;
  - 1.5.3 picks the right option index.
- **Before close:** no part name anywhere in the scene's DOM (search it for the memo names).
- **Enlarge:** the dialog opens and closes with focus returned.
- **Hotspot spacing:** hotspots don't overlap each other at 390 px.
- **The Hall.**
- **Sizes and the companion:** one companion, and no overlaps at 390, 768 and 1280.
