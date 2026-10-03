# Build prompt 6: layer 3, the first scene, Fluid Mechanics pipe systems

Agreed order (Murci, 2026-09-27):
1. layer 2 (done, bec9ef2);
2. **one scene per family as a proof: this brief, engineering pipe systems**;
3. a Life Sciences figure scene;
4. the sitting modes.

**Target:** `C:\Users\mokon\Downloads\3rd design\Exam Practice.dc.html`, screen `03 Mission`.

## What a scene is (the rule for every future scene)
- **A scene is an optional layer on top of layer 2, never a replacement.**
  - The step fields, keypad, stamps and bar stay exactly as built. The step fields remain the source of truth and the accessible control.
  - The scene is a picture of the system, with **tags on it that are shortcuts** to those fields.
- **A mission opts in through data, not code.** Each mission gets a scene record:
  ```js
  SCENES["1.1"] = { template: "reservoirs_summit", tags: { "1.1.1": { s1: "levels", s2: "pipe", s3: "outlet" }, "1.1.2": { s1: "to_summit", s2: "summit_head", s3: "summit_gauge" } } }
  ```
  - Missions without one render exactly as today.
  - Later, the service can carry it as an optional `Mission.scene` field (an additive contract change for R-review, not in this brief).
- **Geometry comes from the part's `givens`, so the drawing is to proportion.** In 1.1 the summit sits at 260/720 along the pipe, and 3 m above the upper level against an 8 m drop.

## Three templates (one family, "pipe systems")
1. **`reservoirs_summit` (1.1):** two reservoirs at their real level difference, and a pipe rising over a summit and down.
   - Tags: `levels` (hf between the free surfaces), `pipe` (V), `outlet` (Q), `to_summit` (hf₁ over L₁), `summit_head` (p/ρg) and `summit_gauge` (p).
2. **`contraction` (1.2):** a horizontal pipe, 300 mm narrowing to 100 mm, drawn to the diameter ratio, with a U-tube manometer across the change.
   - Tags: `v1` (small section), `v2` (large section), `vh1`, `vh2`, `dh` (manometer head) and `dp` (kPa).
3. **`parallel_pipes` (1.3):** two tanks joined by three pipes drawn at d, 2d and 3d thickness, with Q₁ = 88 ℓ/s labelled on the smallest.
   - Tags: `ratio2`, `q2`, `ratio3` and `q3`.

## How it behaves
1. **Before answering:**
   - The scene sits at the top of the question column, under the shared information, at most 220 px tall on phones and 280 px on wide screens.
   - Every unknown is a tag ("V = ?"), and the tag for the current step is highlighted. Tapping a tag focuses its step field and opens the keypad on touch screens.
   - Tags show the learner's value **live** as they type ("V = 2,5|"). The scene never shows a value the learner hasn't entered, apart from the givens.
2. **After Check, the system answers back with the learner's own numbers only:**
   - **1.1, flow:** flow marks move along the pipe at a speed proportional to the learner's V (clamped so it's always visible), and the lower reservoir's level rises at a rate proportional to their Q.
   - **1.1, summit:** a pressure gauge at the summit shows the learner's p. If their p is at or below water's vapour pressure (about 2,3 kPa absolute at 20 °C), the summit shows an air pocket and the note "At this pressure the water would boil and the siphon would break". That's physics about *their* number, never a verdict.
   - **1.2:** flow marks run faster in the narrow section in proportion to the learner's V₁ against V₂, and the manometer's difference is drawn at the learner's head difference.
   - **1.3:** each pipe's flow marks come at a rate proportional to the learner's Q₂ and Q₃ against the given Q₁.
   - **Tags take the step's stamp** (✓, "carried forward ✓", ✕), the same as the step cards.
3. **Only after the part closes** (full marks, or the memo shown): a faint "examiner's flow" ghost plays next to the learner's flow for comparison, with the label "Yours · The memo's". Before that, nothing in the scene can reveal a correct value.

## Rules
- **Performance:**
  - One SVG, and only the scene on screen animates. It pauses when scrolled out of view (IntersectionObserver) and when the tab is hidden.
  - Flow marks are dash-offset animations on short paths. No filters, no canvas, and no 3D (R7 stays untouched).
- **Reduced motion:** static arrows sized by the learner's value instead of moving marks; the level shown as a fixed "rising" arrow.
- **Accessibility:**
  - The SVG is `aria-hidden`. A visually hidden text alternative, and a "Describe the system" disclosure under the scene, state the geometry and the givens in words.
  - Tags are real buttons (44 px) that are labelled ("V, velocity in the pipe, step 2, not answered").
  - Consequence notes are text in a live region.
- **The Hall:** the scene and tags stay, since they're the question. The consequences, stamps and ghost are off.
- **Brand:** water in `#378ADD` / `#81b1ff` tints, the brand blues for flow, amber for the air pocket. No emoji.

## Verification (DOM)
- **Scene and tags:** all three missions render their scene, and tag count equals step count for each part.
- **Tap:** a tag tap focuses the right field (and on touch opens the keypad for it).
- **Live values:** the tags mirror typed values.
- **Consequences:** after Check, the animation rates scale with the learner's values (read the computed durations for two different V values).
- **Air pocket:** appears for p ≤ 2,3 kPa and not for 40 kPa.
- **No leaks:** before close, no correct value appears anywhere in the scene's DOM (search the SVG text for the expected numbers).
- **The ghost:** appears only after close.
- **Reduced motion:** the static path.
- **Hall:** consequences off.
- **Sizes and overlaps:** 390, 768 and 1280 px, one model, no overlaps.
