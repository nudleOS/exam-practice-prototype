# Build prompt 21: the map's controls live in the top bar

**Target:** `Downloads/3rd design/Exam Practice.dc.html`, the `02 Map` screen and the shared header.

**Decided 2026-09-27 (Murci):** the map's controls were "in the way of the map and blocking it". Everything moves into one slim bar.

**Renumbering:** "Your studies" becomes brief 22.

## Before → after

| Control | Before | After |
|---|---|---|
| Paper / Topics | a segmented track in a sticky sub-header | **the title is the view menu** (▾); the subtitle reads "Paper · 21 of 100 marks" |
| Zoom level | three icons in the sub-header | **one icon** showing the current level; it opens Mission · Sections · Whole paper |
| Class test open | a full card under the sub-header | **a blue dot**; it opens the line, the lock note and "Start the test" |
| Paper kit · the Hall · Review | a bottom dock (plus a header kit button) | **one ⋯ menu** with the Hall's full label ("Hall · paused for your test", "Hall report · 78 of 100", …) |
| Design preview | a dashed header toggle | a quiet item at the bottom of ⋯ (design-only) |
| XP | a header pill | unchanged on wider screens; **on phones it heads the ⋯ menu,** so the title can breathe |

## Behaviour
- **Popovers:**
  - opaque (`data-float`);
  - `position: fixed` 74px from the top, so they sit clear of the 67px bar;
  - capped at `100vw − 24px`.
- **Closing:** a tap outside (a full-screen catcher under the bar), Esc, or Tab closes them. Focus returns to the trigger (`closeLayer`, `data-trigger`).
- **Menus:**
  - `role="menu"`, with `menuitemradio` or `menuitemcheckbox` items;
  - ↑/↓ cycle, and Home/End jump;
  - focus lands on the checked item, or the first.
- **The zoom band** runs from the bar's bottom + 12px to the window's bottom − 16px (there's no dock now). When the design-only preview row is open, the band starts below it.

## Verification (as built, design commit f0f124b, 2026-09-27)

| Window | Bar buttons | Title | Popovers (in window · below bar · no layer/buried faults) | Tap targets | Horizontal scroll |
|---|---|---|---|---|---|
| 925×648 | 5, all 44px, in window | full | 4/4 ✅ | clean | none |
| 1440×900 | 5, in window | full | 4/4 ✅ | clean | none |
| 390×844 | 5, in window | 158px ("Fluid Mechanic…") | 4/4 ✅ | clean | none |
| 360×640 | 5, in window | 128px ("Fluid Mech…") | 4/4 ✅ | clean | none |

- **The view menu:** focus opens on "Paper ✓". ↓ moves to Topics, and picking it switches the view, closes the menu and updates the subtitle.
- **The zoom menu:** Whole paper, then back to Mission. The icon's label follows the level.
- **⋯:** Paper kit opens the kit. Esc closes it with focus back on ⋯; an outside tap closes it too.
- **The class dot:** it shows the full notice, with focus on "Start the test".
- **The 17d audits pass.** The finish reveal (brief 20) has no medal under the card, and with no dock the reveal now runs to the bottom edge.

**Found while building:**
- **The first cut squeezed the phone title to 30–60px** (below the 44px target and unreadable). Dropping the XP pill on the phone map, and tightening the gaps to 6px, fixed it.
- **The popovers started at 64px,** 3px inside the 67px bar. They now start at 74px.

**Not verified:** a screen reader moving through the menus, and a real phone.

## 21b: the zoom is removed; a pinned tracker resumes where you left off (design commit 5815a49, 2026-09-27)
**Murci's direction:** "remove the zoom in controls completely and just have the roadmap show as it did, and the start paper box at the beginning of the map to be pinned and not scroll with the map, and it can resume from where you left off, kind of like tracks the progress and where you are on the map."

**Removed:**
- all of brief 19: the zoom icon and menu in the bar, the pills, the pin, the zoom box, the level-based visibility, pinch, Ctrl+wheel, the keys, and every zoom method and value;
- the road is back in the page flow exactly as before;
- the finish (brief 20) loses its zoom-out reveal beat, and the card follows the dance (about 6.8s).

**The pinned tracker** (bottom, opaque, `min(520px, 100%)`):
- **The ring** shows the marks banked.
- **The title** is "Start at 1.1", "Continue at 1.4" or "Review my paper". The line under it is the mission title plus "4 of 13 done" (or "All 13 missions done · 51 of 100 marks").
- **The arrow** shows where the next mission is: ↑ above the view, ↓ below it, › on screen. It's driven by a passive scroll listener (at most one `trackerCheck` per frame). Its label says the same ("It's above you on the map").
- **A tap** resumes: it scrolls to the next mission and opens its card (the existing `startGo`).
- **It steps aside** for the mission card, the paper kit and the finish (otherwise a panel half-covered it at 925×648).

**Found and fixed while building:**
- **Without the reveal, the wide-screen finish card covered 4.3's title.** The road now makes room with a right padding (408px), the same way the desktop mission card does. Measured: 0 medals, labels or badge under the card.
- **On phones the flag sat behind the bottom sheet.** After the card appears, the flag and the dancing companion scroll into the space above it (badge 198–235, sheet from 573).
- **The companion's bubble at the finish collided with the marking-guideline note** (by 14px on a phone). The note now keeps 128px clear of the road (the bubble clears it by 18px at 390 wide and 12px at 925), and the bubble hides while the finish card is showing.

**The 17d audits pass** at 925×648 and 390×844. The only flags are design-only controls.
