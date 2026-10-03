# Build prompt 22: the road runs across the wave into a whirlpool (the vortex map)

**Target:** `Downloads/3rd design/Exam Practice.dc.html`, the `02 Map` screen, and a new element `vortex-map.js`.

**Decided 2026-09-27/28 (Murci), designed in `_concept-map-portal.html` (untracked design scratch):**
- the road runs back across nexera-hero's dotted wave "as far ahead to the back as it can", with the finish line far
  at the back;
- the first mission sits on a whirlpool (the vortex) right over the start card; missions dive into it as you scroll up;
- the companion stands still on the start card's left edge ("not run or anything else");
- the start card's border wears the Nexera logo colours and turns only while the road moves;
- the map's ground is one step lighter than the first page, and the header matches it; the vortex stays dark so it
  reads as a hole.

## Architecture
- **`<vortex-map>`** is a custom element (the `model-floor.js` precedent: shadow DOM, driven by attributes). It draws
  everything from ONE value per frame (`scrollY`) on fixed layers: 0 the WebGL field (the hero's wave + the drain),
  1 the vortex (canvas), 2 the road (canvas), 3 the medals (slotted HTML), 4 front.
- **The page stays the source of truth.** `mapVals` still lays out every mission; it passes the same geometry
  (`vmGeom`) and each medal's paint (`vmPaint`: status colours, label, chips, tick, halo, stamp) as JSON. The element
  never re-derives a status.
- **The page's hooks keep working:** medals are light-DOM `<button data-node="i">` and the arch carries
  `data-finishbadge`, so focus return, bursts and "is it on screen" checks find them where they are drawn.
  `scrollToNode`, the finish run and the tracker's arrow ask the element (a fixed medal can't scroll the page).
- **Placement:** outside `<main>`, whose `rise` animation leaves a transform (it would trap fixed layers); `<main>`
  sits above with `pointer-events:none` so the sticky bars stay on top. No `contain`/`transform` on the host either.
- **One WebGL context per page:** the field is created once and re-attached on every visit (the map remounts).
- **Events:** `vortex-open { index }` opens the card; `vortex-dir { where }` drives the tracker's arrow, which settles
  180 ms after the view does (a re-render of this page is a 30–50 ms task on a modest device: never mid-scroll).
- **Colour:** one constant, `MAP_GROUND` (`#23262b`), feeds the map's background, the colour its dots fade into, the
  header and the preview strip. Every other screen, and `?map=classic`, keep `#191b1e`.
- **`?map=classic`** keeps the flat road, for comparison.

## Speed (measured, 3.4 GB laptop, scripted 2 × 5 s scroll of the whole road, then rest)

| | Before tuning | After |
|---|---|---|
| Scroll, mean | 18.7 fps | 35.5 fps (tier=low: 41) |
| Scroll, median frame | 50 ms | 16.8 ms |
| The element's clock, median | 11 ms | 6.2 ms |
| Script at rest | 259 ms/s | 108 ms/s |

What was slow (found by hiding one layer at a time and Chrome's Long Animation Frames API), and the fix:
- the road as an SVG under a full-screen mask, re-rasterised every frame and drawn twice a frame → a canvas, once;
- labels sharing their medal's layer (every move re-painted four blurred shadows) → their own compositor layers,
  DOM writes only on change;
- per-frame allocations (GC pauses of 50–180 ms) → pooled objects and scratch arrays;
- the ambient wave on the CPU → the hero's wave outside the drain in a vertex shader (only the drain is simulated);
- idle at 30/20/15 fps by tier; a governor steps quality down (never up) when frames keep running long.

The honest gap: the classic map scrolls at ~56 fps on the same laptop; the vortex at ~36 mean. This laptop's governor
steps to level 2 (no in-between dots near the drain).

## Verification (as built)
- Design commits: a619224 (the element), 530b3fa (wired in), 538116c (first page's background), fb07022 + 4bb82c6
  (the mouth lighter), f5d5067 (lighter ground, dark hole), 0337414 (header matches).
- Checked in the browser: medal tap → card; close → focus back on the medal; Continue; leave and return (same canvas,
  old clock stopped); "Finish · 85" (scroll to the arch, fireworks from it, lit 87%); 925×648, 390×844, 375×812;
  phone labels inside the window, no horizontal scroll.
