# Build prompt 10: topic drills (the second sitting mode)

**Target:** `C:\Users\mokon\Downloads\3rd design\Exam Practice.dc.html`. The drill gets a Topics view on the map, a drill round that reuses screen `03 Mission`, and a drill result screen. It is practice only, in the same way as page 4.

## What we found (measured, 2026-09-27)
- **Topics are real data.** The service's approved papers carry a topic per part (`data/papers/*/paper.json`):

  **FM N6, 32 parts:**

  | Topic | Parts | Marks |
  |---|---|---|
  | Pipes | 8 | 25 |
  | Open channels and notches | 2 | 6 |
  | Orifices | 3 | 9 |
  | Ventilation | 1 | 8 |
  | Pumps | 11 | 23 |
  | Pelton wheel | 4 | 16 |
  | Water turbines | 3 | 13 |

  **AET L4:** Topics 1 to 4, plus one mixed part.

  **Life Sciences:** not tagged (design sample).

  The prototype's paper files carry no topics yet.
- **Syllabus weights** come from the N6 syllabus, as cited in LOOP §5.4: pipes 18, open channels 12, orifices 10, pumps 22, ventilation 10, water turbines 10, Pelton 10, vortex 8. Vortex flow has **no question in the bank**.
- **LOOP v2 already designs this mode** as "review rounds" (§5.6, §3.5). It sets three rules we must keep:
  1. **One paper can't drill a topic.** Spaced retrieval of the *same* items trains memory for those items, not the topic. So a drill serves, in this order:
     1. **template instances** (the same method with new numbers);
     2. **paper parts the learner hasn't seen**;
     3. only then **repeats**, labelled "Practised" and paying **no XP** (replay ruling).
  2. **Topic strength is honest:** it counts closed parts, and only unaided first tries (L4). It stays "Building" until it has **6 parts from 2 sources**, and it never shows 0% for a topic with no evidence.
  3. **Never serve the held-out Hall paper** (L12).
- **Templates are designed but not built** (ENGINE §5). The V-notch recipe is fully specified and measured in ENGINE §5.4: relation, parameter box, memo ticks, corner values.
- **Status of the rulings this leans on:**
  - L4 is a recommended default in `design/00-overview.md`. **L12 and P-T1 were DECIDED on 2026-09-27** (ARCH §9): L12 as the target rule with a labelled interim Hall; P-T1 accepted with practice-only instances.
  - The prototype labels its recipes "sample recipe · awaiting curriculum approval".

## 1. The Topics view (on the map)
- **A pinned switch**, "Paper | Topics", sits at the top of the map, above the design-only preview bar. Paper is the road that exists today.
- **Topics** is a list ordered by syllabus weight. Each row shows:
  - the topic and its weight, e.g. "Pumps · 22% of the syllabus";
  - **evidence:** "No evidence yet", "Building · 3 parts so far", "On track" or "Strong" (LOOP §5.5 bands; the drawer comes later);
  - **what a drill would serve:**
    - "Fresh numbers every time · sample recipe" when the topic has a recipe;
    - otherwise "8 parts new to you";
    - otherwise "Only repeats left · practice, no XP".
- A topic with no question says so: "Vortex flow · 8% · No questions in our bank yet". It's shown, not hidden.
- **The suggestion:** one row is marked "Suggested". It's the topic with the highest weight × (1 − evidence share) that has something to serve. Suggested, never forced (L5 open road).
- **Papers without tags:**
  - AET: "Topics arrive when this paper's text is transcribed".
  - Life Sciences: "This sample isn't tagged by topic".

## 2. The drill round
- **Six parts, built once at start** by a recorded rule: recipe instances and unseen paper parts **interleaved**, then repeats if needed. If the topic has fewer than 6 things to serve, the round is shorter and says so.
- It **plays as a mission** (a synthetic mission, so the play screen is unchanged). The existing rules all apply: three tries, hints, stamps, the companion, the keypad, the feedback bar and XP 100/60/20.
- The header chip reads "Open channels drill · 2 of 6". Closing it asks nothing: the finished parts count and the rest is dropped.
- **A recipe part** carries the tag "New numbers · Nexera recipe". Its memo is labelled "Written by Nexera's curriculum team" (ENGINE §3.8).
- **A repeat** carries "Practised · no XP". It is marked `replay`, and `check()` honours that.
- **Scenes follow the part:** a paper part keeps its scene or figure; a recipe part has none in this brief.

## 3. Two sample recipes (ENGINE §5.2 shape, prototype only)
Solved in plain JavaScript at play time from the recipe (SymPy verification is service work). Each instance is recorded as `(recipe_ref, seed)`.

- **`fm-vnotch` (Open channels), isomorphic to 2.1** (ENGINE §5.4):
  - Relation: Q = (8/15)·Cd·√(2g)·tan(θ/2)·H^2,5.
  - Parameters: Q from 150 to 1 500 ℓ/s, step 10; Cd from 0,58 to 0,98, step 0,02; θ ∈ {60°, 90°, 120°}. Constraint: H between 50 and 1 500 mm.
  - Steps: flow in m³/s (1 mark), then head H in mm (3 marks).
  - A typed number can't show the formula and substitution ticks. So they are awarded **with** a correct H. That mapping is written on the recipe for the curriculum team to approve.
  - Check: the paper's own values give H = 672,930 mm.
- **`fm-pipe-summit` (Pipes), isomorphic to 1.1.1:**
  - Relations: hf = Δz; V = √(2g·d·hf / (4f·L)); Q = (π d²/4)·V.
  - Parameters: L from 300 to 1 500 m; Δz from 3 to 20 m; d from 0,3 to 1,5 m; f from 0,005 to 0,01. Constraint: V between 0,5 and 6 m/s.
  - Check: the paper's values give V = 2,557 m/s and Q = 2,892 m³/s.
- **Three wording variants each.** They are ILLUSTRATIVE; the approver writes the real ones. Stems are Nexera-authored, never the paper's wording.

## 4. The drill result (new screen `08 Drill · result`)
- The heading shows the topic name.
- Two stats: **first tries** ("4 of 6") and **XP**, with the reason: "new questions" or "repeats · no XP".
- **Topic evidence, before and after:** "No evidence yet → Building · 6 parts", with the one-line rule: "We say more after 6 parts from 2 sources."
- The main button is **"Another round"** (fresh instances; a new seed). The second is **"Back to topics"**.
- Same focus and live-region rules as page 4.

## 5. The contract the prototype mocks (PROPOSED)
```http
GET  /v1/papers/{id}/topics            200 [ { "topic_ref": "…", "label": "Pumps", "weight": 22, "parts": ["…"] } ]
POST /v1/sittings  { "purpose": "drill", "topic_ref": "…", "size": 6 }
  201 { "sitting_id": "…", "parts": [ { "key": "fm:3.1.2" } | { "recipe_ref": "fm-vnotch", "seed": 1234, "number": "R1" } ] }
GET  /v1/me/strength?subject=…         200 [ { "topic_ref": "…", "band": "building", "n_parts": 3, "n_sources": 1 } ]
```
- The drill reuses the practice answer and reply shapes. A recipe instance's reply is the same `reply` as a paper part's.
- **Security:** a recipe instance is re-created from `(recipe_ref, seed)` on the server to mark it. The client never sends expected values, and the learner view carries no answers.

## As built (design commit 53709bf, 2026-09-27)
**Verified in the DOM:**
- The Topics counts match the service paper: pipes 8, open channels 2, orifices 3, ventilation 1, pumps 11, Pelton 4, turbines 3, and vortex "Not in the question bank".
- An Open channels drill served recipe, 1.4.3, recipe, 2.1, recipe, recipe. Every recipe answer solved from its own stem was marked full.
- The drill result showed "4 of 5 first tries, +500 XP, No evidence yet → Building · 5 parts so far". Round 2 was all fresh recipe instances.
- A repeat is tagged "Practised · no XP" and restarts at try 1.
- No expected value is in the DOM before a part closes.

**Found while building:**
- **FM parts without a key** (2.1 and 2.3 in the prototype) go to "waiting for a marker". They give no first-try evidence, and the result says "nothing marked yet: a marker reads these" instead of "0 of 0".
- **Evidence weights:** a recipe instance counts 1.0 the first time a learner meets that recipe and 0.7 after (LOOP §5.5). A repeat or a part whose memo was shown counts 0.3.
- **Preview seeds** ("In progress · 21") carry first-try observations: clean 1, with hints 0,5, memo 0. They're preview data only.
- **Continue from page 4 always returns to the road view,** so the finish moment is never hidden behind Topics.

## 6. Verification (DOM, all four sizes)
- The Topics list matches the service's topic counts, and vortex flow shows "No questions".
- A drill on a topic with a recipe serves recipe instances first, interleaved with unseen paper parts, and never repeats before those run out.
- Recipe answers match the checks in §3.
- A repeat pays 0 XP, and the result screen's XP equals the sum of the run log.
- Evidence counts only first tries without a hint, and moves bands by the rule.
- No memo or expected value is in the DOM before a part closes (leak check).
- No overlaps, and no horizontal scroll.

## Not in this brief
- Spacing and decay (a topic falling due).
- The "Why this?" drawer.
- The pattern finder ("Missed twice: converting ℓ/s").
- Formula rounds.
- Recipes beyond the two samples.
- Teacher-assigned drills (they come with class tests).
