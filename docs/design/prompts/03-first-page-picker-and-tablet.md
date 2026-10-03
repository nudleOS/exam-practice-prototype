# Claude Design prompt 3 of N — first page: clipped sheet, tablets, a picker that looks tappable

Decided with Murci, 2026-09-26, after reviewing the 3rd design. Measured in a browser:
- **Sheet clipping, every width ≥ 600 px.** The centred sheet overflows the screen:
  - 768×1024: 170 px off the right, 113 px off the bottom;
  - 1280×800: 122 px off the bottom.
  Cause: the `pop` keyframes set `transform: scale()`, which replaces the sheet's `translate(-50%,-50%)` centring.
- **Tablets never designed.** 600–1099 px falls between the phone and desktop rules.
- **The picker reads as plain text.** The two words have no background, border or chevron, only a 2 px underline.
- **Focus never enters the sheet.** `componentDidUpdate(_, prev)` throws, because this runtime passes no previous
  state.

Murci chose to fix these before page 2. Paste everything below the line into the same Claude Design project.

---

This refines the **first page only** of `Exam Practice.dc.html` again. Keep everything that works: the stage and
companion, State A / B / Finished, pills, the streak dialog, the no-paper flow, and the skin and motion. Leave every
other screen as it is.

## 1. The picker sheet is clipped on tablets and desktop — fix it first

On every width from 600 px up, the centred sheet renders with its top-left corner at the centre of the screen:
- 768×1024: it runs 170 px off the right and 113 px off the bottom;
- 1280×800: it runs 122 px off the bottom.

The cause: the sheet is centred with `transform: translate(-50%,-50%)`, and its `pop` animation also sets
`transform: scale(...)` with fill `both`. The animation replaces the centring.

- **Centre without transforms.** Put the sheet inside a full-screen overlay (`position: fixed; inset: 0; display: grid;
  place-items: center; padding: 24px`) and animate only the sheet's own `scale` and `opacity`. Never use `transform`
  for position on anything that also animates.
- **Always fit the screen.** `max-height: min(640px, calc(100dvh - 48px))`. The header (title, close button, search)
  stays fixed; only the list scrolls. Nothing may run off-screen at 600×800, 768×1024, 1024×768 or 1280×800.
- The overlay dims the page behind it, and tapping the dim area closes the sheet.
- **Focus moves into the sheet when it opens:** into the search field for subjects, or the selected chip for sittings.
  Tab and Shift+Tab stay inside, Esc closes, and focus returns to the control that opened it. This runtime calls
  `componentDidUpdate(prevProps)` with no previous state, so `componentDidUpdate(_, prev)` throws and none of this
  runs today. Keep the last open sheet in an instance field (`this._lastSheet`) and compare against that.

## 2. Redesign the picker: the paper ticket (replaces the "I'm practising…" sentence)

People read the sentence as text and miss that it's a control. Replace it with **one large, obviously tappable
control** that shows what's chosen and says it can be changed. Place it directly above Start.

- **The ticket.** A full-width glass card button, at most 460 px wide on larger screens and at least 64 px tall,
  with a 1 px `rgba(129,177,255,0.45)` border and a faint azure fill (`rgba(0,104,248,0.12)`). Inside, left to right:
  - a paper icon;
  - a two-line stack: the subject, bold ("Fluid Mechanics N6"), then the sitting and facts, smaller ("November 2022 ·
    100 marks · 3 hours");
  - a "Change" pill with a chevron-down on the right.
- **What it looks like when touched.** Hover and press brighten the border and fill; press scales to 0.98.
- **The whole ticket is one button.** Its accessible name is "Paper: Fluid Mechanics N6, November 2022. Change
  paper".
- **The companion points to it.** On a first visit the bubble says "Pick your paper here, then tap Start." The ticket
  glows gently twice (the `suggest` ring) and then stays still. There's no glow under reduced motion, and none on
  later visits.
- **Tapping it opens one sheet with two steps:**
  1. **"What are you studying?"** — the existing search and list (subjects with a paper first, then "Also on Nexera"
     with "No paper yet").
  2. **"Which sitting?"** — the chips and the paper's facts.
  - If the chosen subject has only one paper, step 2 is skipped: the sheet closes, the ticket updates with a soft
    spring swap, and the companion nods.
  - A "Back" arrow returns from step 2 to step 1.
- **A subject without a paper:**
  - The ticket shows the subject with "No paper yet" in `var(--text3)`, and the Change pill stays.
  - The line "DHET question paper · marking reviewed by Nexera" is hidden, because it would be untrue.
  - Start keeps today's behaviour: the companion says "No paper for this subject yet. Pick another one?" and the
    sheet reopens.
- **Returning learners (State B)** keep Continue as the primary, with the ticket shown smaller (56 px) under
  Continue instead of the "Change paper" link. The ticket already names the paper, so the page never hides which
  paper they're on.
- **Continue's second line names the subject:** "Fluid Mechanics N6 · Stand pipes on pipe AC" (ellipsis if long).
  Today a returning learner on a phone sees no paper name anywhere.

## 3. Tablets — design them explicitly

Use three layouts:
- phone < 600 px;
- **tablet 600–1099 px**;
- desktop ≥ 1100 px.

Show the tablet in both orientations: **768×1024 portrait** and **1024×768 landscape**. Tablets are touch-first: no
hover-only states, 44 px targets, and the ticket and Start in thumb reach.

- **Tablet portrait:**
  - The companion is centred on the ring and takes about the upper 55 %.
  - The bubble sits beside its head, never over the cap or face.
  - The ticket and Start are centred below, 460 px wide.
  - The pills sit in the top bar with their full words.
  - The sheet is a centred dialog, 560 px wide.
- **Tablet landscape:**
  - Two columns: the companion on the ring at left (about 55 % of the width), and the headline, subline, ticket and
    Start stacked at right, vertically centred.
  - Nothing scrolls at 1024×768.
- **Phone:** the sheet stays a bottom sheet, with the same fit rule (`max-height: calc(100dvh - 24px)`).
- Add **Tablet portrait** and **Tablet landscape** to the preview control so both can be reviewed. The data is the
  same as the other states.

## 4. Small touch-ups
- On phones the speech bubble covers the right side of the companion's cap. Keep it fully clear of the head: above
  it, or beside it with a tail pointing at the companion.
- Contrast: the ticket's second line must meet 4.5:1 on its fill.

## Keep
- No hearts, lives, timers, leaderboards or emoji.
- No invented stats.
- WCAG 2.2 AA.
- Only the brand three blues plus `#81b1ff`, amber `#e0a10f`, error `#f2777a`, success `#3ddc97`.

Deliver:
- the updated `Exam Practice.dc.html`;
- the preview control with First visit · Returning · Finished · Picker open · Tablet portrait · Tablet landscape;
- a short list of what changed and why.
