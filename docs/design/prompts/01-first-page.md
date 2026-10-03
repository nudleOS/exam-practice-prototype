# Claude Design prompt 1 of N — the first page (the stage)

Decided with Murci, 2026-09-26: returning learners get Continue · a forgiving weekly practice streak · one
companion for now. Paste everything below the line into the Claude Design project that holds both
`Exam Missions.dc.html` (the original) and `Exam Practice.dc.html` (the latest).

---

This is the first of several page-by-page refinements. **Change only the first page now; leave every other
screen as it is.**

The latest `Exam Practice.dc.html` turned the first page into a card list with the companion off to one side.
That lost what made the original `Exam Missions.dc.html` feel like a game. **Bring back the original's first page
as the base**: the full-viewport stage with the companion (`<model-floor src="assets/avatar-lite.glb">`) centre
stage on the glowing floor ring, playing its `greet` clip on a loop; the big headline "Beat the paper."; and the one
glass selector bar along the bottom (the whole decision in one row, then Start). Keep its skin, type scale, spacing,
glass pills and spring motion exactly. Then make it feel alive and personal, like the home screen of a game you
want to open every day, in two states:

## State A — first visit (no attempts yet)
- Headline "Beat the paper." with the original subline ("100 XP a question. Nail it first try. Miss and it drops
  to 60, 20, zero. A clean streak multiplies it.").
- The companion greets, with a short speech bubble beside it: "Hi. Pick a paper and we'll beat it together."
- The bottom bar, fed by the two real papers only: **Level** TVET → **Programme** NATED (Report 191) · NC(V) →
  **Subject** Fluid Mechanics N6 · Applied Engineering Technology (Level 4) → **Paper** November 2022 · February
  2019 → **Start**. Each segment is a tap-to-open picker. A subject without a paper shows "No paper available yet"
  and Start stays disabled with that reason visible. Under the bar, small: "DHET question paper · marking reviewed
  by Nexera".

## State B — returning learner (has an attempt) — the default when one exists
- The companion beckons (same `greet` clip; only the words change) with a speech bubble naming the next
  mission: "Question 1.4 is waiting. You've banked 21 of 100."
- Headline "Welcome back." and one line: "Fluid Mechanics N6 · November 2022".
- **One big primary button: "Continue 1.4 · Stand pipes on pipe AC"** — the brand gradient, the largest thing
  on the page after the companion. A quiet secondary link beneath it: "Change paper" (opens the State A bar).
- Three glass pills along the top: **XP** ("⚡ 740 XP"), **marks banked on this paper** (a small ring or meter,
  "21 of 100"), and **the practice streak** ("3 days this week"). The streak counts days practised this week,
  resets gently each Monday, never multiplies XP, and a missed day never zeroes it — say so in its tooltip:
  "Days you practised this week. It never takes XP away."
- If the learner finished every mission of the paper: the button becomes "Review what cost you marks".

## Make it feel like a game, within these rules
- Motion that rewards arrival: the companion's entrance, the headline rising in, the pills counting up to their
  values (odometer style), the Continue button breathing softly. All of it off under reduced motion (the
  companion shows as a still pose; numbers appear instantly).
- The stage glow may warm slightly with the streak (more days → a touch more glow). No other stats, badges or
  rewards that don't exist.
- No hearts or lives, no timers, no leaderboard on this page. No emoji.

## Phones, performance, access
- Phone 360 px first: the companion fills the upper half, the bar or Continue button sits in the thumb zone at the
  bottom (≥ 52 px tall); pills wrap to one line of three compact pills.
- The companion model is 4.7 MB: show a still poster of the companion instantly and swap in the 3D model when it
  has loaded; on "Save data" or reduced motion, keep the poster.
- WCAG 2.2 AA: the speech bubble is real text (read by screen readers), focus rings on every control, 44 px
  targets, contrast as in the original tokens. Replace the off-brand `#7ea0ff` with `#81b1ff`.

## Sample data for the script block (use these exact field names)
```json
{"papers":[{"id":"fm-n6-2022-11","title":"Fluid Mechanics N6","programme":"nated","level_detail":"N6",
  "sitting":"November 2022","total_marks":100,"duration_minutes":180,"parts":32,
  "provenance_label":"DHET question paper · marking reviewed by Nexera"},
 {"id":"aet-l4-2019-02","title":"Applied Engineering Technology","programme":"ncv","level_detail":"Level 4",
  "sitting":"February 2019","total_marks":100,"duration_minutes":180,"parts":28,
  "provenance_label":"DHET question paper · marking reviewed by Nexera"}],
 "resume":{"attempt_id":"…","paper_id":"fm-n6-2022-11","next_mission":{"id":"m1-4","number":"1.4",
  "title":"Stand pipes on pipe AC"},"marks_earned":21,"total_marks":100,"finished":false},
 "me":{"xp_total":740,"days_practised_this_week":3}}
```
Show a control to flip between State A and State B so both can be reviewed.
