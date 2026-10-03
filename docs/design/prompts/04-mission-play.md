# Build prompt 4: mission play, "a coach at your shoulder"

Agreed with Murci on 2026-09-27. He accepted all four recommendations:
1. the bottom feedback bar;
2. dance, encourage or fall according to the marks;
3. zero-data chimes, on by default, with a remembered mute;
4. a coach strip on phones.

From page 2 on, Claude edits the design directly, so this is the brief Claude builds against, not a Claude Design prompt.

- **Target:** `C:\Users\mokon\Downloads\3rd design\Exam Practice.dc.html`, local git repo, screen `03 Mission`.
- **Scope:** the mission play screen only. The home page and map are approved and must not change, apart from the shared header flag this screen needs. The mission-complete screen is page 4.

---

## Goal
The play screen is a form today. Make every Check a moment, like a Duolingo lesson, while keeping every locked rule:
- no hearts, lives, timers or leaderboards;
- three tries, a hint after each miss, the memo after the third miss;
- XP 100 / 60 / 20 by try, and a multiplier only for first tries in a row. The page shows the server's `multiplier` and `xp_awarded` and calculates nothing;
- the learner never marks themselves;
- the answers and memo never appear before a part closes.

## 1. The screen shell (replaces the global header on this screen)
A lesson header, one line and sticky:
- **✕** (44 px, label "Back to the map") returns to the map.
- **Segmented progress:** one segment per part of the mission. Colours:
  - current: an azure outline;
  - not started: grey;
  - clean first try: gold `#e3b341`;
  - with hints: silver `#c3c8cf`;
  - memo shown: bronze `#b0764a`;
  - waiting for a marker: amber `#e0a10f`.

  These are the same grades and colours as the map's spheres. Each segment is a button that jumps to its part, with a label such as "Part 1.1.2, not started". State is never shown by colour alone: the segment's label says it, and the current segment is taller.
- **XP pill** (the number, with the word "XP" hidden on phones).
- **Streak pill** "×2 streak". It shows only when the server's multiplier is above 1, and pops in when it grows.
- **Sound toggle** (a speaker icon, 44 px, `aria-pressed`).

The global sticky header is hidden on this screen, the way it already is on the home page.

## 2. The companion, on every screen size (one `<model-floor>`)
**Phone (under 600 px): a coach strip above the question.**
- The companion is a 72 × 108 px 3D model on the left, with its speech bubble on the right as real text (`aria-live="polite"`).
- Its opening line frames the question in plain words, built from the data: "⟨number⟩ asks for ⟨stem, lower-cased and trimmed⟩. ⟨marks⟩ marks⟨, one per step⟩." For example: "1.1.1 asks for the discharge. 3 marks, one per step."

**Tablet portrait:** the same strip, with the companion at 92 × 138.

**Tablet landscape and desktop (landscape at 600 px and up, or any size from 1100 px):** two columns.
- A sticky left column about 300 px wide holds the companion at about 220 × 330, with the bubble above it.
- The question sits on the right, at most 640 px wide.
- The whole screen is at most 1060 px wide and centred.

**Shared rules**
- Remove the old desktop-only corner companion (`showCompanion`). Every size now has the companion in the shell.
- With Save-data or reduced motion, show the still silhouette instead of the 3D model; the words carry the reaction.

## 3. Reactions come from the marks, not from right or wrong
| Result (from the reply) | Clip | Bubble (examples) |
|---|---|---|
| Full marks (`result.full`) | `dance` | "Clean. All three steps." / "Correct on try 2. Nice recovery." |
| Some marks (0 < awarded < marks) | `greet`, restarted | "Two of three. Your method carried the last one." when a `follow_through` item is present, otherwise "Two of three. One step to fix." |
| Zero marks | `fall` | "Not this time. Here's a hint." |
| Memo revealed (the third miss, or "Show the memo") | `greet` | "Here's how the examiner marks it." |
| Written answer being marked | `greet` | "Reading your answer…" |
| Marker unavailable (`waiting`) | `greet` | "Saved. A marker will look at it." |
| Idle, when a part opens | `greet` | the framing line from section 2 |

Clip names are the ones in `avatar-lite.glb`: `greet`, `dance` and `fall`. Once Murci's walk clip exists, the map uses `walk`; this screen does not need it.

## 4. The feedback bar (the Duolingo move, not a modal)
Check sits in a sticky footer. After Check, the footer becomes a result bar that slides up from the bottom and replaces the Check area only. The stamped inputs stay visible above it.
- **Full marks:** a green bar (`#3ddc97` family). "Correct · 3 of 3 marks", then "+100 XP · first try", or the server's figure, for example "+200 XP · ×2 streak". A replay reads "Replay — no XP". Button: **Next part**, or **Finish mission** on the last part, which opens the existing complete screen.
- **Some marks:** an amber bar. "2 of 3 marks so far", then the server's `clue`. Button: **Try again · 2 tries left**.
- **Zero:** a red bar (`#f2777a` family). "Not yet", then the clue. Button: **Try again · N tries left**.
- **Third miss:** the bar says "Out of tries" and the button is **See the memo**, which opens the existing reveal panel. Each memo line carries its provenance ("As printed in the guideline", "Corrected by Nexera's curriculum team: …", or "Written by Nexera's curriculum team"), never the word "Official".
- **Written answer:** "Being marked…" with three animated dots while marking runs, which can take up to about 20 s on the local marker. Then the per-point results, with the learner's own quoted words highlighted and the note "Marked by AI against the memo". If the marker is unavailable, an amber "Your answer is saved and waiting for a marker."
- **Drawing:** "Draw it on paper. This one isn't marked online." Then the criteria. It closes without a retry loop.

**Bar accessibility**
- The bar is `role="status"`, and its headline is announced.
- Focus moves to the bar's button, so Enter continues.
- It never covers an input: the question area gets bottom padding equal to the bar's height.

## 5. Stamps on the steps, in place
- Each method step or list field shows its verdict at its right edge, as an icon plus text:
  - "✓ 1" for `correct`;
  - "carried forward ✓" for `follow_through`;
  - "✕ 0" for `incorrect`;
  - "missing" for `missing`;
  - "couldn't read it", with the `reason`, for `unreadable`.
- The field's border takes the verdict colour too.
- Nothing hints at the right value. The clue does that.
- When the learner edits a stamped field for the next try, that stamp clears.

## 6. Phone ergonomics
- **Shared information** folds to one line with **Read**. It opens by default on a mission's first part and is folded on the rest. It's a disclosure button with `aria-expanded`.
- **Paper rules** go on one compact line ("3 decimals · g = 9,81 · decimal comma OK"), with **Formula sheet** as a button next to them that opens the existing Paper kit on its formula tab.
- **Inputs:**
  - steps and numbers use `inputmode="decimal"` and show the unit after the field;
  - Enter moves to the next field, and Enter on the last field presses Check;
  - Check is disabled while marking, so a double submit is impossible.
- The sticky footer sits above the on-screen keyboard (the visual viewport) and keeps a 52 px target.

## 7. The room reacts, and sound
- **Room glow:** a fixed background glow fades to green on full marks, amber on some marks and red on zero, over 900 ms, then settles. It's off under reduced motion.
- **XP flight:** "+100" flies from the bar to the XP pill, and the pill lands with a bump. Off under reduced motion; the number just updates.
- **Sound: zero-byte chimes made with WebAudio. No audio files are downloaded.**
  - Full marks: two rising notes (about 1046 → 1318 Hz, sine, 90 ms each, soft attack and release).
  - Some marks: one soft mid note.
  - Zero: a low, soft thud (about 220 Hz, triangle, 120 ms).
  - The `AudioContext` is created on the first Check, since browsers require a user gesture.
  - Mute is remembered in `localStorage` (`exam.sound`, wrapped in try/catch). If storage fails, sound stays on.
  - The chimes play whether or not reduced motion is on, because sound isn't motion. The mute button is the control.

## 8. Every response mode keeps working
- The shell, reactions, bar and stamps apply to every mode the page supports today: `steps` (method), `list`, `match` (tap to pair, with a decoy), `rubric` (written, with a character count and a coach line), and `draw`.
- Inputs are restyled to match the map's premium surfaces: glass cards, gradient-bordered focus, 44 px targets.
- No new modes are added.

## 9. Constraints
- **The contract stays the same:** the part's learner view and the Check reply keep the shapes in `docs/API.md`. The page's mock marker stands in for the service and returns those shapes.
- **Brand colours only:** the three blues, the `#81b1ff` tint, amber `#e0a10f`, error `#f2777a` and success `#3ddc97`. No emoji. No positioning with `transform` on anything that also animates.
- **Performance:** one WebGL context on the page. Animate only `transform` and `opacity`. No SVG blur filters.
- **WCAG 2.2 AA:**
  - 44 px targets;
  - a visible focus ring;
  - every state readable without colour;
  - an accessible name on every button;
  - a single live region per message (the bubble and the bar headline).

## 10. How Claude verifies before calling it done
The browser pane throttles frames, so checks run against the DOM.
- **Four sizes:** 390 × 844, 768 × 1024, 1024 × 768 and 1280 × 800.
- **The companion:** exactly one `<model-floor>` at every size, and the right clip for each outcome (full, partial, zero, memo).
- **No overlaps:** between the feedback bar and any input, and between the companion or its bubble and the question.
- **Focus:** Check → the bar's button → the next part. Enter moves between fields, and Check can't be double-submitted.
- **Reduced motion:** no animations run, and the silhouette shows instead of the model.
- **Sound:** no `AudioContext` exists before the first Check, and mute persists across reloads.
- **Contrast:** measured on the bar text.
- **Git:** committed to the local design repo with a message that lists what was verified and what wasn't.
