# Phone sweep — home page to industry page (2026-10-27)

**Device:** Samsung Galaxy A04 (SM-A045F), Android 14, Chrome 155, viewport 384×724 @ 1.875 dpr.
**How:** Chrome DevTools Protocol over Wi-Fi debugging, real touch gestures (`Input.synthesizeTapGesture` /
`synthesizeScrollGesture` with fling), while the phone recorded its own screen.
**Recording:** `_recordings/a04-sweep-2026-10-27.mp4` (≈3 min, not committed).
**Flow walked:** home at rest → 12 swipes through the bend and the loop (6 in, 6 back) → tap a card (opens) → tap again
(the 360° turn into the industry page) → 4 levels → View paper (sheet in the panel, scroll, full page, back, close) →
the path map (open, close) → Back home → search (type, tap a result).

## Defects found and fixed (commits)

| # | Defect | Where found | Fix |
|---|--------|-------------|-----|
| 1 | Front card swapped for frozen strips after a swipe (its float stopped) — scroll snaps to fractional px | A04 sweep | 351aaee: within 1 px of the start counts as the start |
| 2 | Tapped card opened 19 px off the screen (260 px from its 36% start) | A04 sweep | 351aaee: `min(260px, 64vw − 13px)` |
| 3 | Opened card slid into the bend: the loop read its step from slot 0, a copy of the opened card | pane at 384×724 | 351aaee: `hmAt()` finds the start card by position |
| 4 | Learner / Educator switch 36×30 px | A04 sweep | 351aaee, then removed with the switch (db348b4) |
| 5 | Industry page squeezed into its left half while a paper was open (body `pv-side` 560 px gap) | pane at 1366 | a622f32, then the reader moved to the bottom bar (6a7e771) |
| 6 | Bend looked folded/creased; swallowed cards visible far in the curve | Murci, measured | e323f9d: gradient shading, 10 px strips, far fade, one card in the bend |
| 7 | Flat "2D" flash as a card enters the curve (strip pictures still decoding) | Murci | 4760b1d: strips built ahead, shown after `img.decode()` |
| 8 | Hard swipes flung the deck 8 cards, out to its ends ("moves aside, hidden, comes back") | A04 sweep | 6d0f21f: `scroll-snap-stop: always` |
| 9 | Home page ran 10 px past the screen and scrolled | pane at 384×724 | 57988d8: card height `100dvh − 290px` |
| 10 | Paper sheet sat 1 px high (innerHeight fractional with the address bar) | A04 | dfeb5dc: placed from the top |
| 11 | Industry panel taller than the professional's card; content needed room | Murci | 857ece8: option B |
| 12 | 30 fps cap: one redraw of the home cost ~30 ms (art frame shadow + mask) | A04 | 85cd2b2 |
| 13 | 3.6 s of image decodes in three swipes (896 px originals) | A04 trace | 9d24105: card-sized images |
| 14 | 1.3 s layer rebuilds per 13 s of swiping (every card's style rewritten every frame) | A04 trace | 3f6a46e: write on change |
| 15 | Real swipes reloaded the whole app (deck, bend and scroll back to the start) | Murci; A04 navigation type "reload" mid-swipe | 12e2686: `overscroll-behavior-y: none` (Chrome's pull-to-refresh) |
| 16 | Bend strip copies held the float as a paused animation: a layer per copy, 33 ms frames | A04, part-by-part A/B | da69718: still copies (17 ms) |
| 17 | Strips built inside the swipe (300-850 ms stalls), kept for every card ever bent (4100 nodes, 444 images) | A04 profile | da69718: built at rest, 6 kept |
| 18 | Fast swipes: slivers and broken cards by the bend - the bend is drawn from the main thread, a frame or more behind the phone's own scroll (10 updates 223 px apart in three swipes) | Murci; A04 | 4ffc0c5: phones get a flat deck (tablet / desktop keep the bend). A scroll-driven CSS rebuild matched the bend to 0.06 px offline but ran 83 ms frames on the A04: parked in `git stash` |
| 19 | Sharp square corners where the deck's edge cut a card | Murci | 4ffc0c5: the edge clip is rounded like a card (18 px) |
| 20 | A card a fast swipe brought in showed no person for ~0.7 s | A04 frame capture | a62802e: pictures eager + sync; the person's live drop-shadow removed (Murci: keep it removed) - ~16 frames -> ~3 |

## Still open

**Caveat (Murci, the same evening):** the sweep's swipes are Chrome's synthesised gestures - even speed, one at a time.
They passed the deck checks, but Murci's real swipes on the A04 still show the deck / loop / bend misbehaving. A
synthetic pass is not a real-finger pass; real swipes are being logged frame by frame to find what differs.

| # | Item | Notes |
|---|------|-------|
| 0 | Real finger swipes | after 12e2686: 105 real swipes, no reloads. Phones now flat (4ffc0c5): four fast swipes 0.4-1.1 s each (bend: 1.2-1.7 s), frames 17 / 33 / 532 ms (median / 90th pct / worst; bend 17 / 83 / 649). One ~530 ms frame per run is still unexplained |
| A | Frames still slow on the A04 | swipes: median 20–35 ms, with 2–5 stalls of 280–700 ms per swipe; the card-turn open stalls up to 588 ms, Back home up to 773 ms. The floating professionals (decision pending) and the strip copies are the remaining costs. |
| B | `{{ indPro }}` image requests (404) | the page template is live markup and fetches its unfilled `src`; harmless but wasteful. |
| C | "Design preview: paper states" button (34×34) on the industry page | prototype control; remove with the other preview buttons? |
| D | Map found open on entering the industry page once | not reproduced in a direct two-tap test (map closed, focus on the title); likely left open by an aborted run in the same tab. Watch for it. |
| E | Back pill reported 76×36 | not a defect: its touch area is 44 px (invisible strip above and below); the checker sees only the visible box. |
