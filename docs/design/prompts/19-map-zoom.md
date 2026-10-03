# Build prompt 19: zoom the map out to the whole paper (WITHDRAWN 2026-09-27)

> **Withdrawn by Murci on 2026-09-27:** "remove the zoom in controls completely and just have the roadmap show as it did". The zoom was removed in design commit 5815a49 (brief 21b). This brief is kept as a record of what was tried and measured.

**Target:** `Downloads/3rd design/Exam Practice.dc.html`, the `02 Map` screen (the Paper view).
**Decided 2026-09-27:**
- a three-level semantic zoom (not a plain scale);
- the order is 19 zoom → 20 finish line (its reveal uses this zoom) → 21 "Your studies".

## Why
- **The FM paper's map is 3454px tall at 925×648 (5.3 screens),** holding 13 missions and 4 sections. It has no zoom, overview or minimap, so a learner can't see the whole paper at once.
- **A plain zoom-out doesn't solve it.** The measured fit scale is about 0.12–0.19: the medals shrink to roughly 8–13px, the text to 2–3px, and the result is a picture rather than a map. So the map changes **what it draws** at each level.

## The three levels

| Level | Scale | What's shown |
|---|---|---|
| **Mission** | 100% | today's map: titles, state chips, companion, bubble |
| **Sections** | ≈ 50% | titles, chips and bubble fade; medal numbers are counter-scaled to stay ≥ 12px; section caps become compact pills |
| **Whole paper** | fit to window | medals become coloured dots; a "You are here" pin; the pills and the finish stay readable; the companion is hidden |

- **Tapping a section pill** zooms into that section at 100%.
- **"Fit" toggles** between "Show the whole paper" and "Back to your mission". The second returns to 100% and centres the next mission.

## Controls
- **− / + / Fit buttons,** each 44px, in the map's sticky sub-header beside Paper / Topics:
  - they never float over the map;
  - they're the single-pointer alternative that WCAG 2.5.1 requires;
  - − and + step through the three levels.
- **Pinch** (two fingers) on touch, and **Ctrl + scroll or trackpad pinch** on desktop. Both are continuous between fit and 100% and anchored under the fingers or cursor.
- **The keys + / − / 0** (0 = Fit) while the map has focus and nothing is typed.
- **Range:** fit … 100%. Zoom-in stops at 100%: above it the road would be wider than a phone (360px), and the page clips sideways overflow. **Browser zoom is never blocked** (no `user-scalable=no`), so magnification stays available (WCAG 1.4.4).
- **Each visit opens at 100%.** A live region announces the level ("Whole paper", "Sections", "Mission view").

## How it's built
- **The road sits in a zoom box.** The box's height is `roadH × z`, so the page's scroll length and `scrollIntoView` stay right. The road inside is `transform: translateX(-50%) scale(z)` with `transform-origin: 50% 0`.
- **Anchored zoom:** the road point under the focus y stays under it (`scrollY` is corrected with each step).
- **Gestures write the transform straight to the DOM for smoothness.** They commit to state when the level changes and when the gesture ends. Buttons animate over 260ms (reduced motion: instant).
- **The map box is `touch-action: pan-x pan-y`,** so one-finger scrolling stays native and our two-finger pinch doesn't fight the browser's.
- **In the whole-paper level,** the medals leave the tab order and ignore taps (8px dots can't be targets); the pills are the targets instead.
- **The see-through floaters found in review,** the bottom dock (0.82) and the Paper / Topics tabs (0.9), become opaque (0.97).

## Verification
- **At 925×648, 390×844, 1440×900 and 768×1024:**
  - Fit shows the whole road (the finish and the start both in view) with no horizontal scroll;
  - the pills and the pin read at ≥ 12px;
  - the three levels are reached with −/+ and with Fit, and focus returns;
  - tapping a pill lands at 100% on that section's first mission;
  - "Back to your mission" centres the next mission.
- **Anchoring:** the node under the viewport centre stays within ±24px across a − step.
- **Ctrl+wheel** zooms the map (and not the page) and anchors on the cursor. Pinch is exercised with synthetic touch events where the pane allows it.
- **Brief 17d's audits still pass** (layers, buried, tap targets, the overflow sweep). The syntax check passes.

## Not in this brief
The finish-line celebration (brief 20), zooming above 100%, and a minimap.

## As built (design commit 3e5b925, 2026-09-27)

**Changed from the plan:**
- **At the whole-paper level, the pills move beside the road, not onto it.** On the road they covered the medal dots: a three-mission section is about 63px tall on screen at z 0.08, and a 44px pill leaves no room. Beside the road, the whole trail of medals stays visible, which is what brief 20's reveal needs.
  - On phones the road moves left (60px) and the labels shorten ("Q1 · 27 marks · 3/4").
  - The finish becomes a pill.
- **"You are here":**
  - at the whole-paper level, a "You" badge inside the section's pill (a separate pin collided with the pill);
  - at the sections level, a pin above the next medal.
- **Medal dots at the whole-paper level** are kept at ≥ 12px on screen with the CSS `scale` property. That doesn't conflict with the medals' `transform` stamp animation.
- **Fit is measured, not assumed:**
  - the band runs from the real sub-header's bottom (it grows with the class-test card) to the dock;
  - the drawn content (pills + medals) is centred in it;
  - a 28px top pad is added for pages too short to scroll.
- **Anchored zoom re-measures the box on every paint.** The paper note above the map shows only at the mission level, so the box moves between levels. The first build drifted 48px because of it.
- **Also fixed:** the sticky sub-header had a transparent strip that let map text peek between the header and the tabs. It now has a full-bleed fade.

**Measured:**

| Window | Whole-paper z | Whole paper in band | Pill over medal / pill | Off-window | Horizontal scroll |
|---|---|---|---|---|---|
| 360×640 | 0.08 | ✅ | none | none | none |
| 390×844 | 0.14 | ✅ | none | none | none |
| 925×648 | 0.08 (class card showing) | ✅ | none | none | none |
| 1440×900 | 0.17 | ✅ | none | none | none |
| 768×1024 | 0.21 | ✅ | none | none | none |

- **Anchor drift across a − step:** 4–14px. Reaching fit by − behaves like Fit and centres the road.
- **The sections level:** medal numbers are 12px on screen and the titles are hidden.
- **Pills:** Question 3 lands at 100% on 3.1; Finish lands on the last mission.
- **Keys:** 0 goes to the whole paper, then back to my mission; − and + step between levels.
- **Wheel:** Ctrl+wheel is prevented and zooms (0.47); a plain wheel is left alone.
- **Pinch:** synthetic touches from 200px to 100px give z 0.5, `preventDefault` on move, and a commit on release.
- **The live region** says "Whole paper" / "Mission view".
- **Leaving the map** resets it to 100%.
- **The 17d audits pass** (layers, buried, tap targets, the overflow sweep). The only remaining flags are the two known false positives (picker rows scrolled out of view; medal-gradient contrast).
- **The tap-target check now skips non-targets** (`pointer-events:none`, `visibility:hidden`, `tabindex=-1`), and the helper is updated in the brain.

**Not verified:** a real touch device (the pinch was synthetic), and a screen reader walking through the pills.
