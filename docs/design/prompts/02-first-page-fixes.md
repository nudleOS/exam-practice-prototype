# Claude Design prompt 2 of N — first page fixes + the one-sentence paper picker

Decided with Murci, 2026-09-26, after reviewing the 2nd design (`Exam Practice.dc.html`, State A/B at 1280 and 360 px,
script block read): fix the eight issues found and replace the four-segment bar with a one-sentence picker. Paste
everything below the line into the same Claude Design project.

---

This refines the **first page only** of `Exam Practice.dc.html`. It is close — the companion is back centre stage, and
"Welcome back.", Continue, the pills and the First visit / Returning / Finished toggle all work. Keep its skin, type
scale, glass pills, spring motion and both states. Change only what is listed here. Leave every other screen as it is,
except fix 1, which touches a flag they share.

## 1. Fixes (all required)

1. **One companion, never two.** On desktop a second, smaller companion renders bottom-right on the home page, because
   `showCompanion` includes `s.screen === "pick"`. Remove `"pick"` from it. Each screen owns exactly one companion;
   the home page's is the stage one. Only one `<model-floor>` may be mounted at a time (each is a 4.7 MB model and a
   WebGL context).
2. **XP maths comes from the server, never the page.** The mock computes `mult = Math.min(4, streak)` after
   incrementing the streak (×2 on the second clean answer). The real service uses the streak *before* this answer:
   `multiplier = min(1 + floor(streak / 2), 4)`, so clean first tries in a row pay ×1, ×1, ×2, ×2, ×3, ×3, ×4. Make the
   mock match that exactly. Every screen shows the reply's `multiplier` and `xp_awarded`; nothing on the page calculates
   XP.
3. **Phone 360 px must match the brief.**
   - The companion fills the upper half of the screen.
   - The speech bubble sits above the companion's head (or beside it), never over the face or body.
   - No empty band between the stage and the action.
   - The primary action sits in the thumb zone.
   - Pills fit one line of three compact pills and never break mid-label:
     - "⚡ 740"
     - the ring plus "21/100"
     - "3 days"
     Longer wording ("days this week") goes in the explanation from fix 6, not the pill.
   - The Continue label fits one line at 360 px. Shorten to "Continue 1.4" with the mission title as a second, smaller
     line inside the same button if needed.
4. **A real poster of the companion.** The current poster is only a blue glow, so with Save data or reduced motion the
   learner sees no companion at all. Add an image slot `assets/companion-greet.webp`: a still of the companion in its
   greet pose on the ring, same framing as the 3D model, at most 60 KB. Show it instantly and cross-fade the 3D model
   in when it loads; keep the still on Save data and reduced motion. Until the image exists, draw the companion's
   silhouette in the same place so the layout never jumps (we will supply the still, rendered from `avatar-lite.glb`).
5. **Finished shows finished numbers.** In the Finished state:
   - the marks pill shows the paper's final marks, not "21 of 100";
   - the bubble reads "Every mission is done. You banked ⟨n⟩ of 100. Let's look at what cost you marks.";
   - the button reads "Review what cost you marks".
   Add `"marks_earned": 64, "finished": true` as a second `resume` sample so this state has its own data.
6. **Explain the streak without hover.** `title` tooltips never show on phones or to screen readers. Make the streak
   pill a button (44 px target) that opens a small glass popover: "Days you practised this week. It resets gently each
   Monday and never takes XP away." Close on tap outside and Esc, and return focus to the pill.
7. **The companion stands on the ring.** On desktop the bottom bar hides the companion's feet. The feet must sit on
   the glowing floor ring, fully visible, with the picker and actions below the ring.
8. **The 3D stage fills the full width.** On a 360 px phone emulation the stage showed a hard edge at about 300 px,
   although the canvas measured 360. Make sure the renderer resizes with its element (a `ResizeObserver` on the
   `<model-floor>` element, not only a window resize), so no edge appears at any width.

## 2. The paper picker: one sentence instead of four menus

The bar asks four questions, but two aren't real choices. **Level** has one option (TVET). **Programme** follows from
the subject: Fluid Mechanics N6 is NATED, Applied Engineering Technology Level 4 is NC(V). Replace the whole bar with
this, in State A and behind "Change paper":

- **The companion asks.** Its bubble: "What are we beating today?"
- **One sentence under the stage**, large and centred: "I'm practising **Fluid Mechanics N6**, **November 2022**."
  - The two bold parts are the only controls: underlined in `#81b1ff`, each a real button (44 px tall, focus ring, an
    accessible name like "Subject: Fluid Mechanics N6, change").
  - Below it, the one primary: **Start** (brand gradient).
  - Below that, small: "DHET question paper · marking reviewed by Nexera".
- **Tap the subject → a bottom sheet** (glass, spring up; a centred popover on desktop):
  - Heading: "What are you studying?"
  - A search field, focused on open, with placeholder "Fluid, engineering, N6…".
  - Results:
    - Subjects with a paper first, each with a small tag for the programme and count ("NATED · 1 paper").
    - Then "Also on Nexera": the subjects already listed in the script's `OTHER_SUBJECTS`, tagged "No paper yet".
  - No results: "We don't have that subject yet."
  - Choosing a subject closes the sheet and updates the sentence. If the new subject has one paper, the paper part
    fills itself in.
- **Tap the paper → a small sheet of chips**, one chip per sitting ("November 2022"), with the paper's facts under
  them: "100 marks · 3 hours · 13 missions".
- **A subject without a paper:**
  - The sentence reads "I'm practising **Mechanical Engineering**, *no paper yet*."
  - Start stays enabled. Tapping it makes the companion say "No paper for this subject yet. Pick another one?" and
    reopens the subject sheet.
  - Never a greyed-out, dead button.
- **Returning learners (State B) don't see the picker** until they tap "Change paper". Then the sentence opens
  pre-filled with their current paper, and a quiet "Back" returns to Continue.
- Keyboard and screen reader:
  - Both sheets are dialogs (focus trapped, Esc closes, focus returns to the word that opened them).
  - The list is a listbox with arrow-key movement.
  - The sentence is announced as one sentence, not as fragments.

Motion for the picker:
- The sentence rises in after the headline.
- A changed word does a soft spring swap.
- The companion nods (its `greet` clip restarting is enough) when a paper is chosen.
- All motion is off under reduced motion.

## 3. Sample data (keep the existing `HOME` fields; add these)
```json
{"resume_finished":{"attempt_id":"…","paper_id":"fm-n6-2022-11","next_mission":null,
  "marks_earned":64,"total_marks":100,"finished":true},
 "subjects":[{"name":"Fluid Mechanics N6","programme":"nated","paper_ids":["fm-n6-2022-11"]},
             {"name":"Applied Engineering Technology (Level 4)","programme":"ncv","paper_ids":["aet-l4-2019-02"]}]}
```

## 4. Keep
- No hearts, lives, timers, leaderboards or emoji on this page.
- No stats or badges that don't exist.
- WCAG 2.2 AA:
  - the speech bubble is real text;
  - 44 px targets;
  - a visible focus ring on every control;
  - every state is readable without colour.
- Only the brand three blues plus `#81b1ff`, amber `#e0a10f`, error `#f2777a`, success `#3ddc97`.

Deliver:
- the updated `Exam Practice.dc.html`;
- the state toggle extended to First visit · Returning · Finished · Picker open;
- a short list of what changed and why.
