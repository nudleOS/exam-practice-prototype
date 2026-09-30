# Implementation brief — port the Nexera curriculum-tool redesign into `nexera-gdd-tool`

**Read this whole file before writing any code.**

## 0. The single most important instruction

**The design files in this project are the specification. Do not infer, approximate, or reconstruct the design from this prose.** This document tells you *where to look* and *what the rules are*. Every pixel value, colour token, copy string, state machine and layout rule already exists as working code in the `.dc.html` files. Your job is to **transcribe** them into the Next.js app, not to redesign them.

Concretely, before implementing any screen:

1. Open the corresponding `.dc.html` file.
2. Read the `<helmet>` block for the CSS custom properties and keyframes.
3. Read the template markup for the exact structure, inline styles and copy.
4. Read the `class Component extends DCLogic` block for the state machine, derived values and handlers.
5. Only then write the React equivalent.

If a value in this brief ever disagrees with the design file, **the design file wins** — and tell me about the discrepancy rather than silently picking one.

The reason this matters: several rounds of this design were spent removing invented content, fixing arithmetic that restated a source of truth instead of deriving from it, and aligning copy to real behaviour. An inferred reimplementation will reintroduce exactly those defects, and they are not visually obvious.

---

## 1. The files, and what each one is

| Design file | Lines | Maps to app route |
|---|---|---|
| `Hero.dc.html` | 683 | `/` — `app/(operator)/page.tsx` |
| `Industries Library - 3 Directions.dc.html` | 428 | `/library` — industry grid |
| `Courses.dc.html` | 541 | `/library` — course grid (same route, filtered view) |
| `New XR Session.dc.html` | 3038 | `/work` — **the primary screen** |
| `Exam Quiz.dc.html` | 3029 | **new route, no backend yet** — see §9 |
| `Dashboard.dc.html` | 516 | `/dashboard` |
| `Settings.dc.html` | 457 | `/settings` |
| `Session.dc.html` | 3250 | superseded by `New XR Session.dc.html` — **reference only, do not port** |

⚠️ **One more file, and it is a different product.** `Exam Missions.dc.html` (~2,300 lines, plus two paper files and an avatar) is the **student-facing** page and belongs with the platform, not with `nexera-gdd-tool`. It has its own section — **§6b** — and its own schema implications in `publish-contract.md`. Do not port it into the authoring tool.

`New XR Session.dc.html` is where the great majority of the work is. Budget accordingly.

### How to read a `.dc.html` file

Each is a self-contained HTML document:

- `<helmet>` — CSS custom properties for both themes, `@keyframes`, font links, body resets. This is the **only** place with class-based CSS; everything else is inline.
- The template between `</helmet>` and `</x-dc>` — markup with `{{ value }}` holes, `<sc-if value="{{ flag }}">` conditionals and `<sc-for list="{{ rows }}" as="row">` loops. Inline `style="…"` throughout. `style-hover` / `style-focus` / `style-active` attributes are pseudo-state styles.
- `<script type="text/x-dc" data-dc-script>` — `class Component extends DCLogic`. `state = {…}` is the state shape. `renderVals()` returns every value the template consumes, by name. Methods are the behaviour.

Mapping to React: `state` → `useState`/`useReducer`, `renderVals()` → derived values in the component body, template → JSX. The `{{ x }}` holes tell you exactly which derived values exist and where they are consumed.

---

## 2. Design tokens — transcribe these verbatim

From `New XR Session.dc.html` `<helmet>`. Both themes. Do not substitute Tailwind palette values, do not round hex codes, do not swap `color-mix()` for a literal.

**Dark (`html[data-theme="dark"]`)**

```
--overlay1:rgba(255,255,255,0.04); --overlay3:rgba(255,255,255,0.10);
--thumb:rgba(255,255,255,0.16); --thumbHot:rgba(255,255,255,0.28);
--menuLine:rgba(255,255,255,0.10);
--bg:#191b1e; --panel:#202327; --panel2:#1d2023; --field:#23262a; --field2:#0f1214;
--stripeA:#121517; --stripeB:#0e1113;
--line:#2a2e33; --cardLine:#2f3439; --line2:#363b41; --btnLine:#454b52; --btnLine2:#2a3033;
--hover:#272b30;
--accentSoft:color-mix(in oklch, #0068f8 22%, #202327);
--text:#eceded; --text2:#a4a9ae; --text3:#8f9499; --text4:#878c91; --text5:#3a3e41;
--accent:#2a52ff; --accentHover:color-mix(in oklch, #1e46ff 40%, #ffffff);
--btnBgHover:#ffffff; --dot:rgba(125,147,184,0.24); --shadow:rgba(0,0,0,0.55);
--sidebarBg:rgba(24,26,29,0.22); --onAccent:#ffffff;
--composerBg:#23262a; --composerBorder:#363b41; --composerText:#eceded;
--composerMuted:rgba(236,237,237,0.62); --composerLine:rgba(255,255,255,0.09);
--composerAccent:color-mix(in oklch, #0068f8 55%, #ffffff);
--azure:#0068f8; --cobalt:#1e46ff; --violet:#671dff;
--menuBg:oklch(0.26 0.045 264 / 0.94); --vignette:oklch(0.24 0.004 264);
--caption:#8b9096; --scrim:rgba(16,18,20,0.74); --chipDash:rgba(255,255,255,0.22);
--danger:#f2777a; --warnInk:#e0a10f;
--warnWash:color-mix(in oklch, #e0a10f 10%, transparent);
--warnLine:color-mix(in oklch, #e0a10f 34%, transparent);
```

**Light (`html[data-theme="light"]`)**

```
--overlay1:rgba(0,0,0,0.05); --overlay3:rgba(0,0,0,0.12);
--thumb:rgba(20,22,26,0.26); --thumbHot:rgba(20,22,26,0.42);
--menuLine:rgba(20,22,26,0.16);
--bg:#f4f5f7; --panel:#ffffff; --panel2:#f8f9fb; --field:#fbfcfd; --field2:#f1efea;
--stripeA:#dbd7ce; --stripeB:#e6e2da;
--line:#e3e5ea; --cardLine:#dcdfe5; --line2:#cdd1d9; --btnLine:#b3b9c4; --btnLine2:#8b8272;
--hover:#eceef2;
--accentSoft:color-mix(in oklch, #0068f8 14%, #ffffff);
--text:#14161a; --text2:#41464c; --text3:#53585f; --text4:#5f656c; --text5:#82888f;
--accent:#1e46ff; --accentHover:#0068f8;
--btnBgHover:#2f3238; --dot:rgba(44,79,128,0.28); --shadow:rgba(18,20,24,0.16);
--sidebarBg:rgba(238,240,244,0.90); --onAccent:#ffffff;
--composerBg:#ffffff; --composerBorder:#dcdfe5; --composerText:#14161a;
--composerMuted:rgba(20,22,26,0.62); --composerLine:rgba(0,0,0,0.10);
--composerAccent:#0052c4;
--azure:#0068f8; --cobalt:#1e46ff; --violet:#671dff;
--menuBg:oklch(0.99 0.002 264 / 0.97); --vignette:oklch(0.955 0.003 264);
--caption:#5d6470; --scrim:rgba(244,245,247,0.84); --chipDash:rgba(20,22,26,0.30);
--danger:#c8372d; --warnInk:#7a5300;
--warnWash:color-mix(in oklch, #9a6a00 8%, transparent);
--warnLine:color-mix(in oklch, #9a6a00 26%, transparent);
```

### Colour rules that are non-negotiable

- **`--azure:#0068f8` → `--cobalt:#1e46ff` → `--violet:#671dff` is the brand gradient**, taken from the logo. Anywhere the design uses a blue or purple, it comes from these three or from `--accent`. There must be **no other blue or purple** in the application — no Tailwind `blue-500`, no separate avatar blue, no distinct "info" blue.
- The gradient literal, where it appears: `linear-gradient(135deg, #0068f8 0%, #1e46ff 50%, #671dff 100%)`.
- Light theme is **neutral grey-white**, not warm/brown. Dark theme is **charcoal (`#191b1e`)**, not black.
- Amber (`--warnInk` and friends) is the only warning colour. `--danger` is the only error colour.
- Both themes must be implemented. Theme is `"system" | "light" | "dark"`, cycled by one control. There is **exactly one** theme control per screen — in the sidebar footer on `/work`. Do not add a second.

---

## 3. Layout primitives

### Panes

`/work` and the Exam Quiz page are **multi-pane**, not a page with a sidebar. Panes, left to right:

1. **Sources** — resizable, collapsible to a 40px strip
2. **Chat** — never collapses
3. **Studio** — resizable, collapsible to a 40px strip
4. **Artifact panes** — the GDD document, the 3D preview; open on demand

Read `paneWidths()` in `New XR Session.dc.html`. It is the authority. Transcribe its arithmetic exactly. The essentials:

```
CHAT_FLOOR = 400   // comfortable width; the lifted composer needs this to lay out on one row
CHAT_MIN   = 320   // hard minimum
SRC_MIN    = 228
STUDIO_MIN = 240
PREVIEW_MIN= 640   // the 3D preview carries fixed ring geometry
DOC_MIN    = 420
GAP = 8, PAD = 16
```

The rule, and **why** it is written this way: rather than scale every pane past its floor and dump the shortfall on the chat, panes **drop in priority order** until the survivors genuinely fit. Sources drops first, then Studio. Each dropped pane **leaves its 40px collapsed strip** so the user can bring it back. The chat never collapses; it falls from `CHAT_FLOOR` to `CHAT_MIN` before anything is dropped.

⚠️ **A dropped pane must render its strip, not its body.** The visibility flags read the budget's decision, not raw state: `srcOpen: state.srcPane && paneW.srcOpen !== false`. Getting this wrong produces a pane that is allocated zero width but still renders its contents — the single most common defect in this layout.

Verified behaviour at the sidebar-closed widths: 1200px → Sources strip, Studio open. 1350px and up → both open.

### Maximise

Every **generated-content** pane (GDD document, 3D preview) can be maximised to fill the screen: `position:fixed; inset:8px; z-index:130`. The sidebars cannot. While a pane is maximised the others are not rendered at all.

### Resize

Sources and Studio have drag handles. Studio's default width is **460px**. Persist user-dragged widths.

### Scrollbars

Chat and pane scrollers hide their scrollbars (`data-noscrollbar`); some panes use a thin bar (`data-thinbar`). Both rules are in `<helmet>`. Never use `scrollIntoView`.

---

## 4. `/work` — the primary screen

Source: `New XR Session.dc.html`. Work through it section by section. What follows is a checklist, not a substitute for reading it.

### 4.1 Navbar

Left to right: logo sidebar icon · industry name · course name · breadcrumbs · spacer · **New Course** · **Quiz** · theme-free right cluster · profile avatar.

- The logo icon shows the Nexera logo; **on hover it becomes an arrow**. It opens the sidebar.
- It is **horizontally aligned with the profile avatar** and sits **below the navbar separation line** where the design places it.
- The right cluster wraps as one group — the avatar must never orphan onto its own line.
- Profile initials come from `PROFILE_INITIALS`, derived from `PROFILE_USER`. **Both** the navbar avatar and the sidebar footer avatar read it. No hardcoded initials anywhere.
- There is a separation line under the navbar. Everything from the course name down sits **below** it.

### 4.2 Sidebar

Opens from the logo icon. Contains the Nexera logo at the top (aligned with the icon's position), recents, and a footer with the theme control and the profile.

**Recents are sessions/workspaces, not chats.** A recent opens a workspace. They group by course. Each carries a state:

| State | Indicator |
|---|---|
| `idle` | hollow dot |
| `working` | filled accent dot, pulsing (`chatPulse 1.4s ease-in-out infinite`) |
| `active` | filled accent dot |
| `waiting` | **amber pause glyph**, tooltip "Waiting on you" |

`waiting` is the one state a dot cannot carry — it needs a glyph you read.

### 4.3 Sources pane

- Every source has a checkbox. **All ticked by default.**
- The count line reads **"N of M sources will be read"** — where N counts sources that are both ticked **and** in scope for the open course. Do not count raw selections against scoped totals; that mismatch was a real bug.
- "Select all / Clear all" control, which keeps its intrinsic width and never wraps mid-label.
- **Filing is shown, not set.** Each row shows where the source applies beside its size: `"Whole course"`, `"Module 01"`, `"This lesson"`, or `"Unsorted"` (in amber). Plus a muted `"agent-filed"` tag when the agent filed it. **There is no control to change filing by hand.**
- **"Sort sources"** action beside "Add curriculum", tooltip "Read the unsorted sources and file each one where it belongs". Disabled when nothing is unsorted.
- **Dilution note**, under the list, when more than four ticked sources are course-wide: *"Past four course-wide sources, grounding starts to dilute — ask the agent to sort them."* Amber.
- **Empty selection is a decision, not an accident.** When nothing is ticked, the count line turns amber and reads *"No sources selected — this lesson will be marked ungrounded"*. While that holds, every build tile that cannot start is dimmed to **55%** with `cursor:not-allowed` and that same sentence as its tooltip. A tile whose artifact already exists stays openable and looks normal.
- Empty states distinguish no-course from no-sources-in-this-course, and say which.

### 4.4 Chat

- Turns: `user`, `agent`, `system`.
- **Action lines** render inside the agent's column, above its prose:
  - *About-to* line — play-triangle icon, muted: `"About to <verb> <scope> — <time estimate>; you can stop any time."`
  - *Receipt* line — check icon, result in normal weight, muted meta after a middle dot: `"Read 3 sources · equipment handbook, haul truck spec sheet, safety standard"`. A **failed** receipt uses a warning icon, `--danger` for the result, and names what failed: `"Model failed — TripoSR unavailable"`.
- **A receipt can be the entire turn.** A correction does not need narrating — `{ who: "agent", receipts: [{ result: "Updated the plan", meta: "scene 3 — Load distribution and tyre wear" }] }` is a complete turn.
- **Agent questions** are ordinary agent turns with a thin `--composerAccent` bar on the left edge of the text.
  - ⚠️ **The bar's rule is arrival, not correctness.** It is on only while it is the last agent question with **no user turn after it**. Any user reply clears the bar, even one that answered something else entirely. Compute the waiting index **once** and share it with the pinned line, so the two can never disagree.
  - The `"Answered · yes"` tag is separate, driven by an `answered` field (`"yes" | "no" | "changed"`) — that is about *what* the reply was, not *whether* one arrived.
- **Working indicator** at the bottom of the turn list, above the composer: pulsing dot, "Working", middle dot, elapsed `m:ss`. Send becomes Stop. The run stays on until Stop is pressed — no fake timeout.
- **Pinned waiting line**, in the same slot, when a question is unanswered: pause icon, "Waiting on you", middle dot, first few words of the question.
- **Composer** is inside the chat pane. A `<textarea>` that grows with its content to a cap of 132px then scrolls. **Enter sends, Shift+Enter is a newline.** The command bar (model picker, source count) is inside the pane, not floating outside it.
- **Source count** where the mode picker used to be: `"12 sources"`, tooltip "Sources this lesson reads", hidden entirely when zero. **There is no mode picker** — it was removed.
- Chat sticks to newest. ⚠️ The pin guard must key on **both** `scrollHeight` and `clientHeight` — a pane opening changes `clientHeight` while `scrollHeight` holds, and a guard keyed on `scrollHeight` alone silently stops re-pinning. Also re-pin on window resize.

### 4.5 Studio pane

Course card, then the module/lesson outline, then build tiles.

**Course card:** cover, name, description, meta, progress, and a small **level pill** that opens the level/year picker. Nothing else — there is no "Always"/standing-rules block; it was designed, then removed on request.

**Outline:** `MODULES` → module → lessons. Clicking a module shows only that module and its lessons. Lessons are **plain text, not boxed**, visibly nested under the module title and numbered. Module titles are larger, and the module name is clickable to go back to that module, exactly as "All modules" goes back to all. Module names and "All modules" show the brand gradient on hover. The nesting must be consistent on every page — a module title nests from "All modules", a lesson title nests from the module name, and nested module names align vertically with the "A" in "All modules".

**Build tiles** — one state each, never two:

| State | Presentation |
|---|---|
| `Not built` | muted |
| `Queued` | muted; Approve suppressed |
| `Generating` | thin progress bar + **Stop** action; Approve suppressed |
| `Failed` | `--danger`, `"Failed — <generator> unavailable"`, **Try again** action |
| `Built` | normal, **Approve** button |
| `Approved` | **Re-open** button |
| `Approved · inputs changed` | amber, **Re-open** button |

- The generator name in a failure **comes from the failure**, not a fixed string. TRELLIS.2, TripoSR, Tripo, Flux and LTX are all possible.
- **Stop is a real action** — it stops the job on the server. Not cancel-and-forget.
- Approval belongs to the artifact and **goes stale when its inputs move on**.
- The five tiles are **Game Design Document · Storyboard · Nexera Studio · 3D Quick Preview · Lesson Video**.
- The **Nexera Studio** tile, once built, offers **"Republish to Studio"**, tooltip "Send the current lesson to Studio again".
- **Config modal rows, trimmed to what exists** — do not add fields:
  - Game Design Document: "Anything it must cover?" only
  - Storyboard: "Where should it start and end?" only
  - Nexera Studio: no option rows, only Build
  - 3D Quick Preview: reference-image drop, "How rough: Fastest / Standard", describe-the-model text
  - Lesson Video: "What should the video show?" only
- Footer line on every config modal: *"Goes to review — the agent checks it and flags anything that needs your eye."*
- Modals are **rectangular**, not square-ish, and must not require scrolling for their content.

### 4.6 The GDD document pane

⚠️ **This is the one place where the design deliberately departs from the current app.** The live app renders the GDD as one flowing numbered document. **The design is tabbed, and the tabbed version is what ships.** Do not "correct" it back to the flowing document — I made that mistake and it was wrong.

- Six tabs, as a segmented control: **Brief · Loading screen · The system · Scenes · Conclusion · Build spec**. Scenes and Build spec carry counts.
- Active tab lifts onto `--panel` with a hairline and a shadow. It does **not** take an accent fill.
- Above the tab row: a muted identity line **`GDD-114 · v4`**, tooltip "Document reference · content version", shown only when the lesson has generated content. `version` is real — it comes from `content._production`.
- Section numbering is **document-wide** so it matches the export; the tab only filters what is on screen.
- In the **Brief** tab, the object list comes from **the lesson's own objects**, not from iterating scenes. Each row is an object; where scenes reference it, name them after it — `"Excavator · scenes 2, 3"`. **An object no scene references still appears**, and its "no scene" marker is amber. That absence is the useful signal.
- Heading: **"What the learner will be able to do"** (not "Skills demonstrated").
- Section intros, block labels and the metadata rows mirror the app's own constants in `lib/gddLabels.ts` (`GDD_SECTION_INTROS`, `GDD_S1_LABELS`, `GDD_LOADER_LABELS`, `GDD_SECTION_TITLES`). **Read that file and use those strings** — do not retype them.
- Media frames are **not all one shape**: a scene's still frames are **16:9**, a scene's video is **3:2**. Each gets its own frame box at its own ratio. Neither may letterbox or crop the other.

### 4.7 The 3D Quick Preview pane

- The **hero ripple animation is the floor the model stands on.** Not a backdrop, not a 2D graphic behind it.
- Implementation, already working in `model-floor.js` — **port this file as-is**, do not rewrite the maths:
  - **One three.js scene holds both the model and the rings**, sharing one camera. Orbit the object and the rings turn with it, flattening toward edge-on as the camera drops. That shared camera is what makes it read as ground.
  - Four rings on a **30s cycle**, staggered 7.5s apart, azure/cobalt alternating, lying flat at `y=0`.
  - Rings are **textured planes**, not ring geometry — a radial-gradient canvas texture gives the bright core, outer bloom and soft blur that a geometric ring cannot.
  - Expansion is **eased** (`1 - (1-p)^1.7`), not linear.
  - A soft additive **light pool** under the feet and a **contact shadow** — without the shadow the model floats however well the rings are placed.
  - The model is normalised to ~2.4 units tall, standing at `y=0`, centred. The camera targets the **floor point (0,0,0)**, not the figure's mid-height, so its feet sit dead centre.
  - `OrbitControls` with damping, `maxPolarAngle = π × 0.495` so the camera never drops under the floor.
  - Caption: **"Drag to orbit · ⌘-scroll to zoom"**. Plus Spin on/off and Reset view. No other buttons.
  - `controls.saveState()` after framing, so Reset returns to the framed view.
- Requires the pinned three.js import map and `GLTFLoader`. The sample model is `assets/teacher-preview.glb`.
- The config modal takes **a reference image and a text prompt** — that is how the real 3D pipeline works. Sources sit opposite the generator; the model picker is a toggle. It must support generating **multiple** models.

### 4.8 New Course modal

Course name, optional one-line description, education level, year within that level. Footer: **Cancel** and **Create course**.

**Creating a course opens it as an empty workspace** — it belongs to an industry, has no modules, and the level the modal set becomes the course's own. A brand-new course must show **empty** chat and **empty** sources; the seeded fixtures belong to the seeded course only.

Also needed: **New Module** and **New Lesson**, each a modal that takes its name. Nothing creates a named thing without asking for the name first.

### 4.9 Vocabulary — use the app's, not mine

| Design says | App's real value | Source |
|---|---|---|
| Primary School | `primary` | `core/education.py` |
| **Secondary School** | `secondary` → label is **"High School"** | `lib/levels.ts` ⚠️ |
| Higher Education | `university` | `lib/levels.ts` |
| TVET | `vocational_training` — ⚠️ but `Exam Quiz.dc.html` records this as `tvet`. **Confirm which the platform actually stores before porting.** | `lib/levels.ts` |

⚠️ **Use "High School".** `lib/levels.ts::LEVEL_LABELS` is the source of truth for that copy; my design says "Secondary School" and is wrong.

Years per level — `core/education.py::YEARS_BY_LEVEL`, mirrored in `lib/teacherSetup.ts`. These match the design exactly:

- `primary`: "Grade R", "Grade 1" … "Grade 7"
- `secondary`: "Grade 8" … "Grade 12"
- `university`: "1st year", "2nd year", "3rd year", "4th year", "Postgraduate"
- `vocational_training`: "NQF Level 1" … "NQF Level 8"

Default is `vocational_training` / "NQF Level 4". `level_detail` is normalised server-side by `normalize_level_detail` — **use the real endpoint, do not validate client-side only**.

**The level and year chips are removed from the command bar** once a course is open; the course owns those. The subject chip stays. On the hero, where no course exists, the chips stay as they are.

**Industries:** 50, from `core/industries.py::SEEDED_INDUSTRIES`. Users cannot create industries. Read them from the API (`/industries`), do not hardcode. The "keep only two industries" migration was superseded by `a7f2c9d4e618` — 50 is current.

**Models:** the picker's list must come from the app's model endpoint. `qwen3:32b` was removed from the design's list.

---

## 5. Four known design-vs-app conflicts

Resolve each as stated. Do not resolve them silently in either direction.

### 5.1 Level label — change the design

Use `"High School"` from `lib/levels.ts`. One word. The app wins.

### 5.2 Modules are not an entity — **ask before building**

The app stores a module as a **string key with an ordering array**:

```ts
Workspace.module_order?: string[] | null
Workspace.module_plans?: Record<string, PlannedLesson[]> | null
Lesson.module_name?: string | null
```

No id, no row, no description, **no per-module status**.

The design draws module cards with numbers and their own status badges. **Per-module status has nowhere to live.** Implement the module outline and navigation as the design shows, but **do not invent a module status field** — either omit the badge or derive it from the lessons inside it, and **tell me which you chose**. Whether modules become a real table is a product decision, not yours or mine to take mid-port.

### 5.3 Lesson status vocabulary — align to the app

The app has `GDDStatus = "draft" | "approved" | "locked"`. The design uses `"outline" | "draft" | "in review" | "approved"` — `outline` and `in review` are **invented**, and `locked` is real but missing from the design.

Use the app's three. Map the design's presentation onto them: `draft` → the design's draft treatment, `approved` → its approved treatment, `locked` → the approved treatment plus a lock affordance. Flag anywhere this leaves a visual gap.

### 5.4 The artifact lifecycle — the app already has it

Good news, and a reason not to invent: the app's real lifecycle is

```ts
state: "absent" | "generating" | "ready" | "failed" | "approved"
approved: boolean
stale: boolean        // from content._production
version: number
```

This maps almost 1:1 onto the design's tile states. **Bind to these fields.** `Not built` = `absent`, `Built` = `ready`, `Approved · inputs changed` = `approved && stale`. Do not build a parallel client-side state machine.

---

## 6. The Exam Quiz page

⚠️ **Read this before starting it. It is greenfield.**

There is **no `PastPaper` model, no exam model, and no exam route** in `nexera-gdd-tool`. The only CAPS reference in the whole backend is a comment in an agent prompt. There is **no `curriculum` field** (CAPS/IEB) anywhere.

So this page is a **new feature**, not a redesign of something that exists. Do not try to wire it to endpoints that aren't there; build the UI against a typed mock layer with a clearly marked seam, and tell me what the API needs to be.

`publish-contract.md` in this project is the contract for the platform side of it — read it.

What the page is, so the mock is shaped right:

- **Three panes: Sources · Chat · Studio** — same shell as `/work`, same pane budget, same maximise rules.
- **One product, not two tabs.** Quiz and Exam were merged; Exam is a maker in the Quiz studio. There is no Quiz/Exam tab pair.
- **Scope chips: Level → Subject → Curriculum → Language**, cascading parent-to-child. **Level determines which subjects are available** — a Grade 7 filter must not offer Accounting. Changing a parent that invalidates a child resets the child.
- **Makers:** Exam paper (memo included — never a separate memo generator), Quiz, Flashcards. **Gap analysis and study notes were removed.**
- **Sources are paper + memo pairs.** A paper without its memo is **refused at upload** — the memo is the marking scheme, and without it the questions have no answers. Refuse at the door rather than accumulating rows nobody can use.
  - Upload takes one pair at a time. The bulk "a year at a time" mode was removed.
  - Plus a **"find it on the DBE site"** search route. Results list pairs; a paper whose memo is unpublished shows `no memo` and **cannot be taken**.
- **The agent check annotates by default and holds only arithmetic impossibilities** — marks that don't total, a question with no memo entry, a reference to a section the template doesn't have. Everything requiring judgement annotates and goes to the queue. A blocked item is invisible, and in the first weeks the signal about where the pipeline fails is worth more than the reviewer time it costs.
- **Everything derives from the blueprint**, which is learned from the papers. Section shapes, marks, topic chips. Never restate a paper's structure in a second place — that is how the two drift, and it happened twice during design.
- **Check tab carries this line:** *"Multiple choice marks itself. Structured, numerical and essay answers are marked by the model, so two runs can differ — check those yourself."*
- **Flashcards** take the nexera_quiz card interface: question on the front, answer on the back, pick difficulty and count. **No Again/Hard/Good/Easy rating row** — see §7.
- **Publish** goes to the platform with an audience and an availability window. The published list is **our record of what we made**: name, kind, date, who published it, scope, marks. **No attempt figures** — see §7.

---

## 6b. Exam Missions — the student-facing page

⚠️ **Different product, different audience, different repo.** Everything above is the curriculum tool, which internal teams use to AUTHOR. `Exam Missions.dc.html` is what a LEARNER opens: a real past paper played as a run of missions. It belongs with the platform, not with `nexera-gdd-tool`.

Read `publish-contract.md` alongside this section — it carries the schema this page implies.

### The files

| File | Lines | What it is |
|---|---|---|
| `Exam Missions.dc.html` | ~2,300 | the whole page: pick → map → mission → report |
| `paper-ls-p1-2026.js` | 400 | Life Sciences P1, May/June 2026 (DBE · NSC) — paper + memo |
| `paper-fm-n6-2022.js` | 260 | Fluid Mechanics N6, Nov 2022 (DHET · NATED) — paper, **no memo** |
| `avatar-stage.js` | — | the `<avatar-stage>` element: GLB + clip playback |
| `assets/nexera-avatar.glb` | 19.5 MB | the companion, with named animation clips |

### How a paper is registered

A paper file assigns one global and nothing else:

```js
window.PAPER_LS_P1_2026 = {
  id: "ls-p1-2026", subject: "Life Sciences", paper: "Paper 1",
  sitting: "May/June 2026", board: "DBE · NSC", total: 150, time: "2½ hours",
  sections: [ { id: "A", title: "Section A", total: 50, missions: [ … ] } ]
};
```

The page's `PAPERS` array is the index — level, year, subject, and a thunk:

```js
{ level: "secondary", year: "Grade 12", subject: "Life Sciences", data: () => window.PAPER_LS_P1_2026 }
```

A thunk, not a reference, because the paper scripts load after the page script. **Adding a paper is one file plus one row.**

### The nine question types, verbatim

These are transcribed from two real papers. `judge()` in the page is the authority on each — read it before reimplementing.

| `t` | Student does | Judged by |
|---|---|---|
| `mcq` | picks one | `pick === a` (index) |
| `term` | types a term | `matches()` against `a[]` — an array of accepted spellings |
| `num` | types a number | `abs(typed − a) <= tol`, comma-decimal accepted |
| `pickn` | picks exactly `count` | every pick ∈ `pool`, and `picks.length === count` |
| `list` | names `count` things | each answer matched against `pool[][]`, **no double-counting** |
| `order` | sequences options | `chosen` equals `a[]` exactly |
| `lettername` | picks a letter AND names it | both must be right |
| `rubric` | writes an answer | **self-marked** against `bullets[]` |
| `draw` | draws | **self-marked** against `criteria[][]`, each with its own mark |

⚠️ **`matches()` is deliberately forgiving** — case, punctuation and surrounding words are ignored, because "negative feedback" and "the negative feedback mechanism" are the same answer. Do not tighten it to string equality.

Two examples, exactly as they appear:

```js
{ n: "1.2.1", t: "term", marks: 1,
  q: "The process where the change in the level of one hormone brings about an opposite response…",
  a: ["negative feedback mechanism", "negative feedback"],
  clues: ["It is a control mechanism — two words plus a third.", "Opposite response … think 'negative'."] }

{ n: "3.1.3", t: "draw", marks: 6,
  q: "Draw a histogram to represent the results in women aged 40 to 79.",
  criteria: [["Type of graph: histogram is drawn", 1], ["Caption includes both variables", 1], … ],
  memo: "Bars at 450, 620, 600, 240 for 40–49 … Y-axis 'Number of women (per 100 000 people)'." }
```

### Method marking — the NATED case

The Fluid Mechanics paper **shipped with no marking guideline**, and this is not an edge case: it is how DHET publishes.

```js
{ n: "1.4.3", t: "num", marks: 2, a: 0.225, unit: "m", tol: 0.002, methodOnly: true,
  q: "Calculate the hydraulic mean depth of the pipe.",
  bullets: ["m = A / P = d / 4 for a circular pipe running full"] }
```

`methodOnly: true` means **the student marks themselves against the method**, not against the number. Three marks is three steps; getting the method right and the arithmetic wrong earns partial credit.

⚠️ **This is the single most important thing to carry into the platform.** A schema storing one right answer per question scores a method-marked paper as zero and makes it unusable. See the TVET section of `publish-contract.md` — the `marking` field is orthogonal to `type`.

### Scoring

```js
const XP_LADDER = [100, 60, 20];                                  // by try
const mult = tries === 0 && combo % 3 === 0 ? 3 : 1;              // clean-streak only: every third first try in a row is x3 (combo counts this answer)
gained = XP_LADDER[tries] * mult;
```

Three tries, a clue after each miss, then the memo answer for zero. The streak pays in threes (Murci, 2026-09-30): the third first try in a row earns x3 (300 XP), then the count starts again, so a clean run of nine earns 100, 100, 300 three times (1 500 XP); a miss resets it. It replaced a x1-x4 ramp. **A multiplier only ever applies to a first-try answer** — it rewards sustained accuracy, not persistence. There is no speed bonus: rewarding speed on an exam-prep tool teaches the wrong habit.

**Retakes award no XP.** `earned[]` records what a question has already paid; re-running a mission re-scores the mark but never pays twice.

### The companion

`<avatar-stage>` with `clip`, `scale`, `lift`, `yaw`:

| Moment | Clip | Loop |
|---|---|---|
| Pick screen | `greet` | loops |
| Miss | `fall` | **once, clamped** — stays down through the clue |
| Correct | `dance` | loops |

Clips match on a substring, so exporter suffixes (`greet_04.001`) don't matter.

⚠️ **The GLB is 19.5 MB**, which puts the standalone bundle at 24 MB. Fine for a prototype, wrong for a learner on mobile data — compress with Draco or meshopt before shipping. Expect under 3 MB.

### What is fixture and what is real

**Real:** both papers, every question, mark and memo answer, transcribed from the PDFs. Section totals are the papers' own.

**Fixture:** XP, streaks, unlocked avatars, and per-paper progress — held in `localStorage` under `nx-missions`. On the platform these are server state tied to a learner.

⚠️ **The subject pickers list every Grade 12 NSC subject and every TVET programme — around sixty. Two have papers.** Every other combination correctly shows an empty state. **That is not a bug.** Do not invent papers to fill it.

### Coverage, honestly

| Family | Papers read | Status |
|---|---|---|
| NSC Grade 12 | 1 | proven |
| NATED N4–N6 | 1 | method marking proven |
| NC(V) Levels 2–4 | **0** | assumed |
| Occupational / trade test | **0** | assumed |

An occupational programme ends in a **practical, observed trade test** — a written-question schema may be the wrong tool for it entirely. Settle that before building for it.

## 7. Two deliberate omissions — do not "fix" these

Both were removed on instruction. Both look like gaps. **Leave them out**, and if you think they should return, raise it rather than adding it.

**Attempt analytics.** The published list shows no attempts, no means, no per-question scores, and there is no results modal.

⚠️ For the record, and it matters if this ever comes back: the data **does** exist. `nexera_quiz` has `QuizAttempt` written server-side (`routers/quizzes.py:72`) and `QuizAnswer` with per-question `is_correct` and `marks_awarded`; `routers/students.py` joins it and the admin UI already shows it to educators. The localStorage in `useOfflineSync.ts` is an offline queue that syncs, not the store of record. So the absence in this UI is a **product decision, not a platform limitation** — do not document it as the latter.

**Flashcard spaced-repetition ratings.** The four-button rating row is out. `FlashcardReview` does store full SM-2 state (`ease_factor`, `interval_days`, `next_review`, `last_rating`), but the router is descoped in the pilot — so the buttons would promise a schedule that never arrives. The deck keeps Back, Next and the flip.

---

## 8. Content and copy rules

- **Every copy string in the design is deliberate.** Several rounds went into wording that describes real behaviour rather than aspiration. Transcribe strings exactly. Do not paraphrase, do not "improve", do not expand a terse label into a sentence.
- **No invented content.** If the design shows three modules, show three. Do not pad lists, add placeholder sections, or invent statistics, badges or icons. An empty-feeling section is a layout problem, not a content gap.
- **Derive, never restate.** Wherever a figure describes something that already exists elsewhere — section marks, question counts, topic lists, source counts — compute it from the source. Hardcoding a matching number is the defect that recurred most during this design, and it is invisible until the source changes.
- **Every empty state says what is empty and what to do.** "Select industry" when none is chosen, "Select course" when an industry is open but no course, "No sources in <course> yet…" when a course has none.
- **No emoji.** No AI-slop tropes: no aggressive gradient backgrounds beyond the brand gradient's defined uses, no rounded-container-with-left-border-accent, no Inter/Roboto/Arial.
- Minimum contrast 4.5:1 for text, 3:1 for headline-scale. Full-opacity ink on accent grounds.

---

## 9. Definition of done

Per screen:

1. Open the `.dc.html` side by side with the running app at the same viewport. They should be **indistinguishable** in layout, spacing, type scale, colour and copy.
2. Both themes.
3. Every interactive state exercised: hover, focus, active, disabled, loading, empty, error.
4. Pane behaviour at 1200 / 1350 / 1500 / 1800px, and with each pane collapsed, open and maximised.
5. No console errors.
6. Zero hardcoded values that should derive — grep your own diff for numbers that also appear in a fixture.
7. Tokens match §2 byte for byte. No stray blue or purple outside the brand three.

**Report back on:** the module-status decision (§5.2), any place §5.3's mapping leaves a visual gap, the Exam Quiz API seam (§6), and every instance where a design file disagreed with this brief.

**For Exam Missions (§6b) additionally:** confirm `methodOnly` questions score partial credit rather than zero, that adding a paper needs only one file plus one index row, and that the GLB was compressed before it reached a learner.

---

## 10. Order of work

1. Tokens and the pane shell (§2, §3) — everything else sits on these.
2. `/work` navbar, sidebar, chat, composer (§4.1–4.4).
3. Sources pane with the full grounding logic (§4.3).
4. Studio: course card, outline, build tiles (§4.5).
5. GDD document pane, tabbed (§4.6).
6. 3D preview — port `model-floor.js` as-is (§4.7).
7. Hero, Library, Courses, Dashboard, Settings.
8. Exam Quiz last, against a mock layer (§6).

**Exam Missions (§6b) is separate work in a separate repo.** It does not sit in this sequence — start it when the platform is ready to receive papers, and read `publish-contract.md` first.

Stop and ask whenever the design and the app disagree in a way this brief does not cover. A question costs minutes; an inferred answer costs a rebuild.
