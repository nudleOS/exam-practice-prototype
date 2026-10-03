# Build prompt 17: one card, one button (the home declutter)

**Target:** `Downloads/3rd design/Exam Practice.dc.html`, home screen (`01 Home`).
**Decided 2026-09-27:**
- the one-card rule, including more than one class test;
- XP is the only stat on home, and marks and days move behind it;
- the order is 16 → **17** → 18.

## Why
On the home, a returning learner met **three stacked cards with three buttons:** the class test, Continue, and the paper ticket. There were also **three stat pills** (XP, the marks ring, days).

Two more faults:
- **Continue did something other than its label.** While the class test was open, practice on that paper was paused, so Continue opened the class-test rules screen.
- **A second class test would silently disappear.** `liveFromBus()` keeps only the newest (`[0]`).

## The one-card rule
**The home shows one card with one primary button.** The most urgent thing the learner can **act on** takes it:
1. a class test **in progress** (the clock is running);
2. an **open** class test, the one that closes soonest first;
3. **released marks not yet seen**;
4. otherwise **practice**: Continue (returning), or the paper ticket + Start (first visit).

**What the card does not take:**
- **Tests the learner can't act on** (upcoming, handed in, missed, released and already seen) never take the card. They go on the card's footer line:
  - with one other test, the line names it ("Applied Engineering Technology L4 · opens Fri 09:00");
  - with more, it counts them ("2 more tests").
  - The line opens **"Your class tests"**, a sheet that lists every test with its state and its button when it has one. No test is ever hidden.
- **This refines the order agreed in chat.** There, an upcoming test was number 4 on the card. As built, it can't take the card: it has no button, and taking the card would push Continue down to a link.

**Below the card, one quiet link:** "Practise another paper" (or "Practise a paper instead" on a first visit). It opens the existing paper picker. The separate paper-ticket box under Continue is removed.

## Changes
1. **The top bar has one stat.**
   - The XP pill becomes a button that opens **"Your progress"**. It shows XP, the marks banked on the current paper, and the days practised this week, with the existing "resets gently each Monday" line.
   - The marks ring and the days pill leave the bar.
2. **The class-test card:**
   - its heading reads "Class test · Ms Rivera"; the "Live from the teacher tool" tag stays for the demo;
   - the title is the paper;
   - it has one line of state and a full-width primary button;
   - "not an ICASS task" leaves the home. The test's rules screen already says it.
3. **The Continue card:**
   - its heading is the paper and sitting;
   - its title is the next mission;
   - its full-width primary is "Continue 1.4" ("Review what cost you marks" when finished).
4. **The "Your class tests" sheet:** a new `sheet: "tests"` on the existing sheet frame (Esc closes it, focus returns to the footer line, Tab stays inside).
5. **Preview:** a "2nd test" toggle adds a seeded upcoming AET L4 class test, so the footer and list can be seen. **Prototype limit:** the learner prototype sits one test at a time (the FM paper). The live bus still carries one test, as in brief 15.
6. **`resultSeen[ref]`:** opening a released result marks it seen, and it gives up the card.

## Verification (DOM, then screenshots at desktop and phone)
- **For each preview state** (upcoming, open, in progress, handed in, released, missed) × (one test, two tests) × (first visit, returning):
  - exactly one primary button is on home;
  - the card shows the rule's winner;
  - the footer names or counts the rest.
- **Continue is never visible while the FM test is open** (the old Continue-to-rules fault).
- **The top bar has one stat pill.** "Your progress" opens and closes (Esc, outside click), and focus returns.
- **The tests sheet** lists every test; Esc returns focus.
- **Brief 16 still holds:** the fold check at 1366×657, 1536×730 and 360×640, with no horizontal scroll.
- **The syntax check** passes.

## Not in this brief
- **The map, play and report screens.** They get a measured clutter audit here, with findings and proposals, but no changes until Murci picks. Each is its own design call.
- **"Your studies"** (brief 18).

## As built (design commit 33f79e4, 2026-09-27)
**Verified in the DOM** at 1440×900: 6 test states × (one test, two tests) × (returning, first visit), 24 cases.
- **Every case has exactly one primary button on home** (`[data-classgo]`, `[data-homecontinue]` or `[data-homestart]`).
- **The winners:**
  - Open wins with "Start the test";
  - In progress wins with "Back to the test";
  - Released (unseen) wins with "See your result";
  - Upcoming, Handed in and Missed leave the card to Continue (returning) or Start (first visit), with the test on the footer line.
- **The footer:**
  - with one other test it names it ("Applied Engineering Technology L4 · opens …", "Fluid Mechanics N6 · closed · not sat");
  - with two it reads "2 more class tests".
- **Continue is never visible while the FM test is open or in progress.** The old Continue-to-rules fault can no longer happen.
- **"Your progress":** the XP pill opens it (XP 740 · marks banked 21 of 100 · 3 days this week). Esc closes it and returns focus to the pill. The top bar has one stat.
- **"Your class tests"** lists both tests; the open one has its button. Esc returns focus to the footer line. "Practise another paper" opens the picker, and Esc returns focus to the link.
- **Seen results give up the card.** After "See your result", back on home, the card is Continue again.
- **Brief 16 holds:** 1366×657 at 631, 1536×730 at 701, and 360×640 at 622, all fitting, with no horizontal scroll. The syntax check passes.

**Found while building:**
- **"Practise another paper" puts home into its existing choosing-a-paper state** (`picking`: the ticket + Back + Start). The card hides until Back is pressed. That's the existing Change flow, kept as it was.
- **A seen result, a missed test and a handed-in test stay on the footer count forever** ("2 more class tests" after the result was seen). How long a test stays listed is `keepListed(t, now)`. It currently keeps everything, and the rule is Murci's call.
- **The prototype limit stands:** one sittable test (FM). The second test is an upcoming preview seed ("+ 2nd test" in Preview).

## Clutter audit: map, play, result (measured at 1440×900, no changes made)

| Screen | Controls | Words | Finding | Proposal |
|---|---|---|---|---|
| 03 Mission (play) | 12 | 79 | Already lean. Every control is a part, a tool, or Check. | No change |
| 02 Map | 15 | 234 | **"Fresh paper · In progress · Just finished" is a design-only preview row in the page flow.** It's the same fault as home's. The 7 gradient buttons are mission medals, not competing primaries. | Move the row into the Preview panel |
| 10 Class test · result | 10 | 97 | **"Test still open · Moderator checking · Released" is a design-only preview row in the flow.** Back to the map appears twice (header and footer). | Move the row into Preview; keep both backs (the page is long on phones) |

**Proposal:** one Preview toggle in the header of **every** screen, holding that screen's preview switches. The learner-facing page then never carries design controls.

## 17b: retention + glass cards (design commit 9596503, 2026-09-27)
**Murci's retention rule:**
- upcoming and handed-in tests always stay listed;
- a missed test drops 7 days after it closed;
- **gap filled by Claude, flagged:** a released result already seen is history too, so it also drops 7 days after close;
- an unseen result always stays (it holds the card anyway).

**Verified by running `keepListed` exactly as it stands in the page** over fixed cases:

| Case | Result |
|---|---|
| upcoming | listed |
| handed in, 1 and 30 days after close | listed |
| missed at 1 and 6.9 days | listed |
| missed at 7.1 days | dropped |
| released (seen) at 3 days | listed |
| released (seen) at 8 days | dropped |
| released (unseen) at 30 days | listed |

- **In the browser:** a missed test at 1 day gives "2 more class tests"; at 8 days, the footer names only the AET test.
- **The browser can't hold a test in "handed in" 30 days after close,** because the mock releases it by then (it took the card in the green released tone). That case was checked on the function alone.

**Glass cards** (`.glass-card`):
- blur(22px) + saturate(165%);
- a gradient hairline border (a `padding-box` / `border-box` background pair);
- an inset top highlight and a deep soft shadow;
- tones: `live` (blue), `released` (green), `calm`;
- a status dot in the kicker that pulses only while live (reduced motion stops it).

**Solid fallbacks:** under `@supports not (backdrop-filter)` and under `prefers-reduced-transparency`. Both rules are confirmed in the loaded stylesheet.

**Applied to:** the home test card, the Continue card, the first-visit ticket, the "Your class tests" rows, and "Your progress".

**Found while building:** the phone's action area sat on a 0.9-opaque dark fade, so the glass had nothing to frost. A card-sized light was added behind it. Its size is in px: in % it spread into a page-wide band on desktop.

**Fold:** 1280×631 at 615 and 360×640 at 622 still fit, with no horizontal scroll.

**Performance note:** `backdrop-filter` costs GPU time on low-end Android. It's used only on a few small, static cards, never over the moving 3D canvas. Measure on a real low-end phone before production.

## 17c: legibility, companion, collisions (design commit 59d7378, 2026-09-27)
**Murci's feedback:**
- the cards read blurry;
- he wants Apple-like sleekness and visibility;
- the glows hurt legibility;
- the companion's round floor shadow should go on every page;
- the home greeting visibly looped;
- his window (925×648, which is the tablet-grid layout) showed overflow and collisions.

**What changed:**
- **The card material is near-solid** (rgba 0.84) with blur(24px) saturate(180%):
  - a crisp 1px hairline and an inset top highlight;
  - a plain dark shadow; no coloured glow, no radial sheen, no gradient border;
  - tone is carried by an 8px dot (live pulses opacity only).
- **Type:**
  - labels are sentence case at 13px;
  - titles are 19px/700;
  - the status line is 14px in light grey with `text-wrap:pretty`;
  - **a 12px floor for every HTML label** (62 raised from 10.5–11.5px; the SVG diagram labels scale with their viewBox and are unchanged).
- **Glows:** the light behind the card was removed, and so were the dot and CTA halos.
- **The companion:**
  - the four HTML floor ovals are gone (home, map, mission coach, Hall entrance);
  - `model-floor` hides its 3D contact disc when `floor="none"` (every use);
  - `loop="once"` makes the home greeting play once and hold its final (rest) frame.
  - **The cached module hid the fix at first,** so the script is now `model-floor.js?v=17c`.
- **The speech bubble:**
  - the same material;
  - in the tablet grid it starts right of the head (`50% + 108px`, top 2%);
  - `width:max-content`, capped at the window edge, with `box-sizing:border-box` (the first cap forgot the 30px of padding + border).
- **The map and the class-test result:** their design-only state rows sit behind a Preview toggle in the shared header. **The map row was covering the companion's "Start with 1.1" bubble.**

**Verified by an automated sweep.** It checks overflow past the edge, horizontal scroll, truncation, text under 12px, contrast against composited solid backgrounds, and the bubble against the heading and cards.
- **Screens:** home (test open; test missed), map, mission, mission complete, Hall entrance.
- **Sizes:** 925×648, 1440×900, 1280×631, 1099×700, 1100×700, 1024×768, 768×1024, 390×844, 360×640.
- **Result: clean.** Each run lists the screens it visited, so a skipped screen would show.
- **Two false positives, explained:**
  - a screen-reader-only live region (clipped to 1px) read as past the edge;
  - the map's "1.1" medal label read as low contrast because the check can't see gradient backgrounds. It was checked by eye: white on blue.
- **Unconfirmed:** at 640×400, a 3px overshoot of the card title appears only in the first check after a load; at rest it fits. The page clips horizontal overflow, so nothing scrolls.

**Not verified:** real devices, a real screen reader, forced colours.

## 17d: layers never read through or sink; the greeting holds on the wave (design commit e897995, 2026-09-27)
**Murci's feedback:**
- the glass "Your progress" popover overlapped page text and was hard to read;
- check every page for the same, and for faults he hadn't thought of;
- hold the greeting on the pointing or raised-hand pose.

**Found by opening every layer on every screen** (390×844, 925×648, 1440×900, 768×1024):

| Fault | Where | Fix |
|---|---|---|
| **Buried popover:** "Welcome back." painted OVER "Your progress" | Home, phone and tablet | The top bar was z 3 and the heading block (also z 3) came later in the DOM. The top bar now stacks at **z 8** |
| See-through popover (0.84) over the bubble | Home, phone and tablet | Floating cards are opaque: `.glass-card[data-float]` 0.98 |
| Sticky bars read through (0.86 / 0.88) | Map (shared header), mission (sticky bar, e.g. under the calculator and the answer bar) | 0.97, blur kept only as an edge hint |
| A scroll-to target lands under a sticky bar | `scrollReveal` uses `block:"start"` | `html { scroll-padding-top:88px }` |
| Tap targets 36–42px on phones | Calculator keys + close, Formula sheet, the calculator button, map tabs, paper-kit tabs | 44px (Apple HIG). WCAG 2.2's 24px was already met |

- **Kept, and why:**
  - the mission part dots stay 37px wide (above the 24px WCAG minimum; 44px would overflow a phone on long missions);
  - the design-only controls are unchanged.
- **The buried check was proven to fire** (z 3 reports "YOUR PROGRESS under Welcome back.") and to clear (z 8).
- **False positive:** the picker's rows scrolled below the list's own fold read as buried. Every visible row was confirmed on top.

**The greeting:**
- `greet` was scrubbed frame by frame: 0.6–1.0s points at the viewer, 1.4s is a hand at the face, 1.8–2.2s is the hand raised to the side.
- `hold="1.95"` (with `loop="once"`) plays through once and pauses on the open-palm wave (measured: `time 1.95, paused true`).
- With reduced motion, it starts in that pose. The module is versioned `?v=17d`.

**Noted, not fixed (known pending item):** the Hall entrance shows a grey silhouette placeholder, because the companion still render doesn't exist yet.

**The audit scripts** are kept in `~/.claude/brain/knowledge/exam-service/ui-audit/`.
