# Build prompt 9: page 4, mission complete

**Target:** `C:\Users\mokon\Downloads\3rd design\Exam Practice.dc.html`, screen `04 Complete`. It's practice only: the Hall and the fix round never reach it.

## What we found (measured in the design, 2026-09-27)
- **The XP stat is dead code.** `mXp` is `reduce((a, p) => a + 0, 0)`, so it's always 0. XP earned per part is **never stored**: `check()` adds it to the total, and `prog[key]` has no `xp` field. The screen shows "parts with XP" as a stand-in.
- **"First-try streak" shows the current streak.** That's often 0 right after a miss, which reads as a penalty on a reward screen.
- **"Next mission" skips the map's finish moment.** `celebrate()` runs only when the map is entered from `done`. The main button goes straight into the next mission, so the road never lights up on the most-used path.
- **Nothing says which parts lost marks,** or that a part is still waiting for a marker.
- **No companion appears.** The `dance` clip exists and is used in play, but the reward screen has no companion at all.
- **Paper progress isn't shown.** The learner can't see how this mission moved them toward the paper's total.

## The screen (one column; a centred 560 px card on tablet and desktop)
1. **The companion**, mounted only here and never at the same time as the play screen's model (one WebGL context at a time).
   - It plays `dance` on a clean run and `greet` otherwise.
   - With reduced motion or Save-Data, it's the still or silhouette, as elsewhere.
   - On phones it sits above the title (about 150 px). On wide screens it sits beside the stats.
2. **The grade:** the kicker and ring colour come from the mission state that already exists. Clean run is gold, with hints is silver, memo shown is bronze.
   - If a part is still waiting for a marker, a neutral amber "1 part waiting for a marker" replaces the grade. Its marks land on the map later.
3. **Two stats, counting up** (instantly with reduced motion):
   - **XP this mission,** e.g. "+260", with a reason line built from the parts: "2 first tries · ×2 streak", "got it on try 2", or "memo shown · no XP".
   - **Marks,** e.g. "6/6".
   - **No time stat:** practice has no timers (standing rule).
4. **Paper progress:** "15 → 21 of 100 banked", with a bar that fills from before to after. These are the same numbers as the header meter.
5. **To revisit** (only when marks were lost): up to three rows, each showing the part, its marks lost and a short step label.
   - Tapping a row replays that part. The existing replay rule applies: **no XP**, and the row says so.
6. **Up next:** the next mission's number, title and tags. On the last mission it says "Review my paper" instead.
7. **The main button is "Continue",** which goes to the map. It is not "Next mission".
   - On the map, the existing finish moment runs: the road lights, the ring stamps and the companion moves on.
   - **Then, new: the next mission's card opens itself,** with focus on its Play button. The reward comes first, then the next step one tap away.
   - A secondary text button, "Back to the map", is dropped: Continue already goes there.
8. **Sound:** one `full` chime on a clean run, and none otherwise. It respects the existing mute.

## Data changes (design)
- `prog[key].xp`: the XP paid for that part, written in `check()` beside `best`. Mission XP is the sum; replays add 0.
- `missionStart`: the paper's banked marks when the mission opened, captured in `openMission()`. That gives the "before" value for paper progress.
- The streak number is not shown here. A live streak of 2 or more shows as the reason line "×2 streak carries into 1.2" instead of a stat.

## Accessibility
- On arrival, focus moves to the `h1` (tabIndex -1), not to the button.
- An `aria-live="polite"` region reads the result once, for example: "Mission 1.1 complete. Clean run. 6 of 6 marks, 260 XP."
- The count-up is `aria-hidden`; the final numbers are in the text.
- The To revisit rows are buttons, at least 44 px tall.

## As built (design commit c85e8f8, 2026-09-27)
- **Mission XP comes from a run log,** not only from `prog[key].xp`. `runLog` is reset in `openMission()`, and every Check, memo and waiting reply appends to it. The log carries the server's `multiplier` as it was replied, so the design never computes one. `prog[key].xp` is also written, as the per-part fact.
- **The streak line counts first tries, not a multiplier:** "2 first tries in a row · the streak carries into 1.2". Predicting the next multiplier would mean computing it on the client.
- **Up next is the next mission that isn't done** (every part closed or waiting), searching forward and then wrapping. It's the same mission whose card opens on the map.
- **A replay really pays no XP now.** The bar's Replay button and To revisit both set `prog[key].replay`, which `check()` honours. Before, the Replay button's "no XP" label wasn't enforced.
- **A To revisit replay returns to page 4** ("Back to the results"). It doesn't walk on through the mission.

## Verification (DOM, at phone / tablet portrait / tablet landscape / desktop)
- XP on the screen equals the sum of `xp_awarded` over the mission's replies, for a clean run, a with-hints run and a memo run.
- Paper before and after match the header meter before opening and after closing.
- Continue leads to the map: the finish moment runs, then the next card opens with focus on Play. On the last mission, Continue leads to the summary.
- To revisit lists exactly the parts with best below their marks, and each row opens that part.
- At most one `model-floor` exists in the DOM at any time.
- There are no overlaps, and the page has no horizontal scroll.

## Not in this brief
- Per-mark XP (the L1/L2 proposal, still unruled).
- Daily goals and streak-of-days.
- Sharing a result.
