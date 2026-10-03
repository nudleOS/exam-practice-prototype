# Build prompt 20: the finish line

**Targets:**
- `Downloads/3rd design/Exam Practice.dc.html`: the map, mission complete, the Hall result and the class-test result;
- `model-floor.js`: a clip start point.

**Decided 2026-09-27:**
- the celebration scales with the mark;
- the section-complete bursts and the Hall celebration are in this brief;
- it builds on brief 19's zoom (the reveal).

## Why
Today, finishing a whole paper is the flattest moment in the app:
- **The last mission skips the map.** Its `doneContinue` goes straight to a plain summary page (verified in code).
- **The companion only dances on a "Clean run".**
- **There's no particle layer, no fanfare,** and the Hall result has no celebration at all.

## Verified marks (they drive the tiers and the only "pass" wording the app may use)

| Qualification | Pass | Weighting | Top band | Source |
|---|---|---|---|---|
| NATED Report 191 (N4–N6) | "40% or higher", set **per subject** (e.g. Travel Services N6 needs 70%) | set per programme in *Report 191 Part 2* | **no distinction found** | DHET, *Report 191 ICASS Guidelines*, January 2026, §3.1 and p.20. ICASS ≥ 40% is needed for exam admission |
| NC(V) L2–L4 | Vocational 50% · Official language 40% · Life Orientation 40% · Maths / Maths Literacy 30% | 75% external / 25% ICASS (ISAT subjects: exam 70 / ISAT 30 of the external) | "Outstanding" 80–100% | Umalusi, *Directives for Certification NC(V) L2–4*, August 2013, §2.7, §2.8, §6 |
| NSC | Levels 1–7 (level 7 = 80–100%) | — | level 7 | **Secondary sources only, not verified.** NSC is hidden from learners (ruling 2026-09-27), so it's not needed yet |

**Fluid Mechanics N6 is sourced at 40%:**
- *Report 191 Part 2* (DHET) lists Fluid Mechanics N6 (`08190216`) under *National Certificate: N6 Engineering Studies* (`50608080`) **with no subject-specific promotion rule**. Overrides exist only for programmes such as Educare and Interior Decorating (for example 60:40 ratios).
- The *ICASS Guidelines* (p.20) give the Report 191 pass as "40% or higher".
- **FM N6 `pass_pct` = 40**, `pass_pct_source` = both documents.

**Not confirmed, and so never claimed in the app:**
- a NATED distinction;
- NATED condonation (the research agent's "38–39% condoned" wasn't in the DHET document);
- the FM N6 semester:exam ratio (the general norm sits in *Report 190*, not read).

**The research agent got NC(V) wrong in two places:** languages pass at 40% (it said 30%), and Maths / Maths Literacy at 30% (it said 40%). The primary document was read directly.

## The honesty rules
1. **A practice mark is not an exam result.** The app never says "you passed". The strongest wording is "above this subject's 40% pass mark", and only when the paper carries a **sourced** pass mark.
2. **A new paper field:** `pass_pct` plus `pass_pct_source` (a citation). Without it, the finish uses percentage tiers with **no pass wording**.
3. **The top tier is called by its number** ("80% and up"). It's never called a "distinction", because NATED has none on record. For NC(V) papers, "Outstanding" may be used (Umalusi's own word, 80–100%).

## The tiers (the paper's % of total marks)

| Tier | When | Celebration |
|---|---|---|
| **Top** | ≥ 80% | full fireworks · companion dance · fanfare (if sound is on) |
| **Solid** | ≥ the pass mark (when sourced), else ≥ 50% | confetti · dance · a short chime |
| **Finished** | below that | no fireworks · the companion's raised-hand wave · "You finished all 100 marks" · the fix round offered first |

Every tier celebrates **finishing**. Only the size of the celebration changes.

## A. The paper finish (on the map, about 6s, skippable)
1. **Back to the map.** The last medal stamps and the road lights to the full score (the existing `celebrate()`).
2. **The climb.** The companion glides to the finish flag.
3. **Fireworks** burst from the trophy (canvas-confetti, sized by tier), and the companion **dances**:
   - the `dance` clip starts at about 4.5s and holds the arms-wide pose at about 7.0s;
   - this needs a new `from="4.5"` on `model-floor`, alongside `hold`.
4. **The reveal.** The map zooms out to the whole paper (brief 19), with every medal lit.
5. **The finish card:**
   - the mark (a count-up), the tier line, and the pass-line fact when sourced;
   - two actions. At or above the tier line: **"Sit it in the Hall"** (primary) and "See what cost you marks". Below it: **"Start your fix round"** (primary) and "See what cost you marks".
- **Skip:** a labelled "Skip" button (not a tap-anywhere area) jumps to beat 5.
- **Where it starts:** the last mission's Complete screen now continues to the map finish, not the summary.

## B. A section complete (small, on the map)
When a section's last mission closes:
- a small burst from its cap, about 1.2s;
- the cap glows green once;
- no dance and no sound.

## C. The Hall result (the biggest moment: sat under exam conditions)
On the first visit to a **released** Hall report:
- tiered fireworks behind the big mark, and the mark counts up;
- below the tier line: no fireworks, and "You sat a full paper under exam conditions" is acknowledged first.
The reward rows stay.

## D. A class test
- **Hand-in:** a quiet check animation and "Handed in". No confetti; the marks aren't known yet.
- **Release:** tiered like C, with "Released by your college's moderator · not an ICASS mark" kept.

## Build notes
- **canvas-confetti 1.9.4** (ISC, 0 dependencies, about 6 KB, verified on npm and jsDelivr 2026-09-27):
  - loaded from jsDelivr, pinned to 1.9.4, with an SRI hash added at build;
  - bundled from npm in production;
  - `disableForReducedMotion: true`;
  - `useWorker: true` (Safari has no OffscreenCanvas and falls back to the main thread);
  - particle counts capped by tier;
  - bursts stop by about 2.5s.
- **Photosensitivity (WCAG 2.3.1):** particles only; no full-screen flashes; nothing flashes more than 3 times a second.
- **Reduced motion:** no particles, no camera flight and no count-up. The companion holds the arms-wide pose and the card appears.
- **Data saver:** no fireworks.
- **Sound:** WebAudio only (as today). A fanfare arpeggio for the top tier and a chime for the solid tier. It **follows the learner's sound setting**.
- **Accessibility:**
  - a live region announces "Paper finished. 78 of 100.";
  - focus moves to the card heading, and Esc closes the card;
  - Skip is a real button.
- **Performance:**
  - one WebGL companion plus one 2D canvas, removed after the burst;
  - the burst position is measured from the finish badge's rect after the reveal settles.

## Verification
- **Each tier** (seeded marks 85 / 55 / 25) × (normal / reduced motion / data saver) × (phone 390, 925×648, desktop 1440): the right beats run, the Skip button works, the card actions match the tier, and there's no wording about passing without `pass_pct`.
- **Each section:** its burst fires once, when the section's last mission closes.
- **The Hall and class results:** each celebrates only on the first view after release.
- **The 17d audits** (layers, buried, tap targets, overflow) run with the finish card open.

## Questions for Murci
1. **The sound default.** The prototype's sound starts **on**; the research advises off by default. Should the fanfare only play if the learner has turned sound on at some point?
2. **~~Fluid Mechanics N6's pass mark.~~ Resolved:** *Report 191 Part 2* was read, and FM N6 has no override. `pass_pct` is 40, with the citation above.
3. **Copy.** Is the top tier's line "80% and up" wording you like, or do you want a warmer word that's still not an official claim (for example "Top form")?

## Murci's answers (2026-09-27)
- **Sound is OFF by default.** A learner who turned it on keeps it on (`exam.sound = "on"`).
- **The top tier is "Top form".**
- **Build it.**

## As built (design commit d1add78, 2026-09-27)
**Measured, 925×648 unless stated:**

| Preset | pct | Tier | Card title | Line | Primary | Particles | Companion |
|---|---|---|---|---|---|---|---|
| Finish · 85 | 87 | top | Top form (gold) | Well above this subject's 40% pass mark. | Sit it in the Hall | fireworks | dance, held on arms-wide (from 4.5 → hold 7.0) |
| Finish · 55 | 51 | solid | A solid finish | Above this subject's 40% pass mark. | Sit it in the Hall | cannons | dance |
| Finish · 25 | 24 | finished | You finished all 100 marks | Next: go through what cost you marks… | See what cost you marks | none | greet, held on the wave (1.95) |

**The timeline** (fin85, from the tap): stamp at 1.9s → the run at 3.1s → dance and fireworks at 4.3s → the reveal at 6.8s → the card at about 7.5–8.4s. The existing 2.7s stamp beat is included, so it's about 1.5s longer than the brief's estimate. Skip is always offered.

**What else was checked:**
- **The real path:** the last mission's Complete → "Cross the finish line" → the card after 7.75s.
- **Skip** clears the particles and holds the pose.
- **Reduced motion:** the card straight away, no particles, the final mark (no count-up).
- **Data saver:** no particles; the card still appears.
- **The section burst** fires at the stamp (1.7s) from an on-screen point, and never mid-section.
- **Results:** "Top form" plus bursts on the first view after release. Leaving stops them, and a second view gets 0 bursts. A low class result reads "You sat the class test", with no particles.
- **Sound default** for a fresh learner: false.
- **SRI:** confetti loads with its hash, and there's no integrity error.
- **The finish card:** no medal or pill is under it at 925×648 (it sits right, the road moves to 24%), 390×844 (a bottom sheet with the map re-fitted above it), or 360×640 (a compact card, 191px).
- **The 17d audits pass** (layers, buried, tap targets, overflow), with the finish card open too.

**Found while building:**
- **The research agent's CDN URL (`confetti.browser.min.js`) doesn't exist.** The 1.9.4 package ships `dist/confetti.browser.js` (24.9 KB), and SRI `sha256-SfS8vFbnzrXD0l0T2x0NqWW2zRyKVKcHuwVb4GhbCpU=` comes from jsDelivr's metadata API.
- **The section burst was first anchored to the section's cap.** The road climbs, so the cap sits at the section's bottom, off-screen (y 1400 of 648). The burst was invisible. It now comes from the medal that completed the section.
- **Result fireworks kept firing on the next screen.** They now stop when the result screen is left.
- **The dock repeated the card's actions and sat under it.** It now hides while the card is open.

**Not verified:** a real device (WebAudio and the WebGL dance together), iOS Safari's main-thread confetti cost, and a screen reader walking through the card.
