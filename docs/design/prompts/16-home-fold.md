# Build prompt 16: the home fits every window (the fold fix)

**Target:** `Downloads/3rd design/Exam Practice.dc.html`, home screen (`01 Home`).
**Decided 2026-09-27:** the first of three home pieces, in the order 16 fold → 17 declutter → 18 "your studies".

## Why
On a wide but short desktop window, **Continue, Start and the paper picker sit below the bottom edge, and the page can't scroll to them.** This is the most common laptop setting: 1080p at Windows' 125% scaling leaves about 730px for the page.

**Measured at 1536×730:**

| Block | Height |
|---|---|
| top bar | 76 |
| design-only preview rows | 84 |
| heading | 61 |
| companion stage | 320 |
| action card | 293 |
| **total** | **834**, about 104px over |

- The Continue button's bottom was at 737 and the picker at 749–805.
- `scrollHeight` equalled the window height, so nothing could be scrolled.

**The three causes:**
1. The home is `height:100vh` with `overflow:hidden`, so anything past one window height is cut off, not scrollable.
2. On desktop the stage has a fixed `min-height:320px` (phones already shrink it to 22vh while the card shows).
3. The design-only preview rows (home state, and the class test's six states plus Reset) sit in the page flow and take 84px that a real learner never sees.

**Even without the preview rows,** the budget overflows by about 93px at 1366×657 and about 119px at 1280×631 (computed from the measured blocks).

## The rule
**The controls never give way; the companion does.**
- The stage shrinks first.
- If the window is still too short, the page scrolls.
- Nothing is ever clipped.

## Changes
1. **The home container:** `height:100vh; overflow:hidden` becomes `min-height:max(100dvh, homeMinH)` with `overflow-x:clip` and vertical overflow visible.
   - `dvh` follows a phone browser's moving address bar; `vh` doesn't.
   - Horizontal clipping stays, so the floor glow can't cause a sideways scroll.
2. **The desktop stage:** `min-height:320px` becomes `clamp(140px, 30vh, 320px)`.
   - The stage keeps `flex:1 1 0`, so it still fills any spare height on tall windows.
   - Phone and tablet values are unchanged.
3. **The preview controls move out of the flow.** A dashed "Preview" toggle sits in the top bar's empty spacer (icon-only on phones) and opens a floating panel below it. A bottom-left button was rejected because on a phone it would cover the Continue card:
   - It's design-only and labelled that way. It's closed by default, and `?preview=1` opens it.
   - Esc closes it, and focus returns to its button.
   - Its contents are the same two groups (home state; class test + Reset shared demo), unchanged.

## Verification (DOM rects, not screenshots: the pane scales emulated views)
For each window, the last home control's bottom must be at or above the window's bottom (with no scroll), or the page must scroll to reveal it:
- **Desktop:** 1280×631, 1366×657, 1536×730, 1440×900, 1920×955. All three states: returning + class test open, returning with no test, first visit / picker open.
- **Phone** 360×780 and **tablet** 768×1024 and 1024×768 (landscape grid): no regression. The same check applies, and the companion's head is not covered.
- **No horizontal scroll** at any size (`scrollWidth <= innerWidth`).
- **The drawer:** opens and closes; Esc returns focus; every preview button still works; `?preview=1` opens it.
- **The syntax check** of the logic class passes.

## Not in this brief
- Decluttering the home, the stat pills, and the Continue-while-locked bug (brief 17).
- "Your studies" and filtering the paper picker (brief 18).

## As built (design commit 89d80e3, 2026-09-27)
**Measured by DOM rects.** "Last control" means the lowest home button outside the preview panel.

| Window | Mode | Stage | Last control bottom | Fits |
|---|---|---|---|---|
| 1280×631 | desktop | 216 | 615 | ✅ (the page is 640 tall from the 640px floor, a 9px scroll) |
| 1366×657 | desktop | 232 | 631 | ✅ |
| 1536×730 | desktop | 300 | 701 | ✅ (was 805, unreachable) |
| 1440×900 | desktop | 460 | 864 | ✅ |
| 1920×955 | desktop | 512 | 917 | ✅ (the stage still fills spare height) |
| 360×780 | phone | 393 | 762 | ✅ |
| 360×640 | phone | 253 | 622 | ✅ |
| 768×1024 | tablet | 591 | 984 | ✅ |
| 1024×768 | tablet grid | 692 | 577 | ✅ (fr rows still stretch under `min-height`) |

- **No horizontal scroll** at any size.
- **At 1366×657,** every preview state fits: the class test upcoming, released and missed; first visit; finished. The picker sheet sits inside the window (24 to 633).
- **The drawer:** `?preview=1` opens it. Esc closes it and returns focus to the toggle. All 11 preview buttons are present, and the panel stays open while you switch states.
- **The syntax check** passes.

**Console:** the `{{ … }}` SVG-attribute warnings, the `{{ posterSrc }}` 404 and the `posterFailed is not defined` error all come from the browser parsing the raw template before the runtime binds it. They were already there and are untouched by this diff. A cleanup candidate, not a fold issue.
