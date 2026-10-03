# Build prompt 13: teacher authoring, part 1 — upload a paper and its memo, then review and approve it

**Target:** `C:\Users\mokon\Downloads\3rd design\Teach Exams.dc.html`, which gets new views: Upload, Reading, Review, and Papers to approve.
- It replaces the "Upload a paper and its memo · next step" placeholder in the T1 bank.
- **Generate a practice paper is brief 14.** It reuses the Review and Approve screens built here, so they are built once.

## The rulings this must obey (decided)
- **R3:** teacher authoring is platform first. GDD teachers come later, on the same service.
- **R1:** a teacher's paper reaches learners only when another person approves it.
  - The setter reviews it, and an `institution_admin` who is **not the setter** approves it for the college.
  - Approvers see the **extracted text** learners will see, not the PDF (ARCH §7).
- **R5:** switching extraction to Claude is gated on an eval (FM N6 + AET L4). The prototype mocks the extractor. Nothing here claims a model reads the paper.
- **Uploads (ARCH §7):**
  - they are read by a sandboxed parser worker (no network, no database or model credentials, read-only files);
  - limits are about **20 MB and 60 pages**;
  - encrypted PDFs, PDFs with scripts or embedded files, and Word files with macros are refused;
  - **uploaded text is untrusted data** in every prompt, so invisible or instruction-like text is stripped or flagged at ingest.
- **Copyright (ARCH §9):**
  - DHET clearance for teacher uploads is not confirmed (DBE is cleared);
  - **until it is, a teacher's upload stays in their college's bank**, visible only to that college's learners;
  - the owner is the institution, so the paper survives the teacher leaving (ARCH §4).
- **Every memo is replayed (ENGINE §6.4):**
  - the server redoes each numeric memo line from the question's own numbers;
  - the gates below block approval;
  - checks must be acknowledged;
  - verdicts are counts, never a confidence score (ENGINE §6.1).
- **Memo pairs:** a paper needs its memo.
  - "No memo was published" stores it as **not publishable** (ENGINE §8.1 `pair_missing`).
  - The printed memo text is never edited. A resolution writes an erratum record with its reason (ruling 4).

## What we found (measured)
- **The Fluid Mechanics N6 board memo fails its own paper on 33 marks.** This was measured by the replay (ENGINE §6.4, QTYPES §2.5):

  | Item | Finding | Resolution |
  |---|---|---|
  | **1.3** | The memo prints Q₂ = 1 678,094 ℓ/s, but its own relation gives **497,803** (arithmetic) | erratum |
  | **1.4.5** | hf = 5,5 is used where 1.4.1 gives 6 m (untraceable given) | re-author |
  | **4.1.1–4.1.4** | 430 m against the paper's 500 m (and two more literals) | re-author |
  | **4.3.1–4.3.2** | 195 / −27 kPa against the paper's 196 / −28 | re-author |
  | **Q4 as a group** | both questions mismatched | "memo possibly written for another version of this paper" |

  That makes the real FM pair the ideal demo, **because the checks find real faults.**
- The prototype can't read a PDF in the browser. The upload is **simulated with the FM N6 paper the design already loads**, and it says so on screen. The findings come from the measured table above, not from invented faults.
- `screens.v2` §17.3 already specifies the review screen (item list and detail, gates, the replay panel, legal resolutions only). This brief builds it for the setter and the moderator.

## 1. Upload
- **Two drop zones,** one for the question paper and one for the memo (PDF). Each also works as a file picker, with at least 44 px targets.
- A checkbox, "No memo was published", replaces the memo zone.
  - The paper is then stored as not publishable, and the screen says so before upload: "It can be kept, but not given to learners until a memo exists."
- **The limits are stated up front:** "PDF · up to 20 MB · up to 60 pages".
- **Where it goes:** "It stays in your college's bank. Only your college's learners can see it." It gets a *Your college* badge, never "Checked by Nexera".
- **One action: "Read the paper".**

## 2. Reading (the ingest job, mock stages with honest errors)
- **The stages:**
  1. safe to open;
  2. text read (32 parts found);
  3. memo paired (code 8190216);
  4. marks add up (100);
  5. memo replayed ("33 marks flagged").
- Each stage shows a sentence, not a spinner alone. The job survives leaving the page: "You can leave; we'll keep reading."
- **Errors are sentences you can act on** (ENGINE §8.1). They're reachable from a design-only Preview row:

  | Error | What the screen says |
  |---|---|
  | Encrypted | "This PDF is encrypted, so it can't be read safely. Export a plain PDF and upload again." |
  | Scan | "This looks like a scan. It will be read with OCR, which needs a closer check." It continues, flagged. |
  | No memo | the `pair_missing` sentence |
  | Wrong pair | "The memo's paper code (8190217) differs from the paper's (8190216)." It needs acknowledgement. |
  | Hidden text | "We removed text you can't see on the page (white text on page 4). It can't reach learners or our marker." This is the injection guard, made visible. |

## 3. Review (the setter), T3's paper review
- **Layout:** an item list on the left (phone: a list that pushes to the detail) and the item detail on the right.
- **List states:** passed · flagged (n) · not reviewed. Plus the summary "29 of 32 items resolved".
- **The detail shows:**
  - **The stem, as learners will see it** (extracted text), with an **Edit** action. Edits are the setter's corrections, recorded.
  - **Memo points** with their marks.
  - **Checks, as counts:** "Points add up to 6 of 6 marks ✓", memo lint ("'Any relevant answer' is vague: add a marker note"), figures (alt text ✓, leak check ✓).
- **The replay panel (a gate).** It shows the flagged line and both values, and **only the legal resolutions** (ENGINE §6.4):
  - a disproven value: **Correct it** (erratum), **Accept both**, or **Printed stands**, which needs a written reason **and** a second approver;
  - an untraceable literal: **Rewrite this memo from the paper's own numbers**, or record a derivation showing the literal traces;
  - a group mismatch: a group flag that must be ruled before approving the group.
- **The follow-through gate:** "1.4.5 uses 1.4.1's answer. Can a wrong 1.4.1 still earn marks here?" (Yes)(No). There is no default.
- **"Mark item reviewed"** stays disabled while a gate on that item is open.
- **"Send for approval"** stays disabled until every item is resolved. It says "An institution admin at your college approves it, and it can't be you."

## 4. Papers to approve (the institution admin)
- It's a queue in T3 (Moderate): "⟨paper⟩ · uploaded by ⟨name⟩ · 32 of 32 resolved · 8 resolutions (for FM: 1 erratum on 1.3, 7 items re-authored)".
- It opens the **same review screen, read-only for content,** with every resolution and its reason visible.
- **The approver ≠ author gate:** their own upload shows "You uploaded this paper, so another admin must approve it", with no button.
- **"Approve for the college"** puts it in the bank as *Your college · approved*. It can then be assigned in T2, like a Nexera paper, and moderated as a class test in the same way.
- "Needs changes", with a note, sends it back to the setter.

## 5. The contract the prototype mocks (PROPOSED, from ENGINE §4.7 and §8, and ARCH §4)
```http
POST /v1/banks/{bank_ref}/sources      multipart: paper, memo | memo_status=none_published
  202 { "job_id": "…" }   413 { "error": "too_large" }   422 { "error": "pdf_refused" | "doc_refused" | "pair_missing" }
GET  /v1/jobs/{job_id}                 200 { "state": "reading|pairing|enforcing|replaying|succeeded|failed", "sentence": "…", "paper_version_id": "…" }
GET  /v1/papers/{version}/review       200 { "items": [ { "key", "stem", "memo_points", "verdict": { "gates": [...], "checks": [...] } } ] }
POST /v1/papers/{version}/items/{key}/resolutions   { "finding_id", "resolution": "erratum|accept_both|printed_stands|reauthor|derivation", "reason", "second_approver"? }
POST /v1/papers/{version}/submit       → awaiting_approval        POST /v1/papers/{version}/approve  403 when approver = author
```
- **Security:**
  - the source files live in a private bucket;
  - approvers get the extracted text only;
  - the memo text is `memo:read`-scoped and audited;
  - uploaded text is never followed as an instruction.

## As built (design commit 9dfc498, 2026-09-27)
**Verified in the DOM:**
- **Upload errors:**
  - an empty form says "Add the question paper first";
  - a missing memo gives the `pair_missing` sentence;
  - an encrypted PDF stops at "Safe to open" with its sentence and "Upload again".
- **A wrong pair:** the "Memo paired" stage is flagged, and sending stays disabled until the setter confirms the pair.
- **A clean read:** "33 marks flagged (1.3, 1.4.5, 4.1 and 4.3) · 3 conventions to confirm · the 3.3 definitions need an expert's check". 18 of 32 items pass outright; 14 are flagged.
- **Item 1.3:** both values (1 678,094 / 497,803) and exactly three resolutions. "Printed stands" needs a written reason, and "Mark item reviewed" stays disabled until the reason exists.
- **Item 4.1.1:** only "rewrite" or "derivation", plus "Correcting the single number isn't offered…". It also needs the Question 4 ruling.
- **Item 1.4.5:** the follow-through question has no default.
- **Sending:** it works at 32 of 32 with the pair confirmed. The paper then shows "Waiting for approval" on home.
- **As admin:**
  - "Papers to approve" lists it with "11 resolutions (1 erratum, 7 re-authored, 3 other)";
  - every resolution is read-only for the admin;
  - Approve stays disabled until the admin countersigns "printed stands";
  - once approved, it appears in T2 as "Your college · approved".
- **The admin's own upload** shows "You uploaded this paper, so another admin must approve it", with no Approve button.
- **No memo:** the paper is stored, the notice shows, and Send is disabled ("A paper needs its memo before learners can use it").
- **Needs changes:** the note reaches the teacher, and the teacher can resend.
- **Phones (360):** no horizontal scroll. The item list stacks above the detail, as a 260 px scrolling list.

**Prototype shortcuts, stated:**
- Reading is simulated with the FM paper already loaded, and the memo points shown for unflagged items are the service copy's.
- "Memo points add up" is shown as passed rather than computed.
- On phones, the list doesn't push to a separate detail view.

## 6. Verification (DOM, desktop / tablet / phone)
- The upload refuses nothing silently: each Preview error shows its sentence. "No memo" says "not publishable" before upload.
- **The review:**
  - 1.3 shows both values (1 678,094 / 497,803) and exactly three resolutions;
  - "Printed stands" needs a reason and a second approver;
  - 4.1.1 offers **no** "correct it" option, only re-author or derivation;
  - Q4 shows the group flag;
  - 1.4.5 shows the follow-through question with no default.
- "Send for approval" is disabled until every item is resolved, then works.
- **As admin:** your own upload has no approve button; another teacher's is approvable. After approval the paper appears in T2 step 1 as *Your college · approved*.
- The upload says it is simulated, and nothing on screen claims a model read the paper.
- No overlaps, no horizontal scroll, and focus lands on each item's heading when it's opened.

## Not in this brief
- Generate a practice paper (brief 14; it reuses §3–§4).
- OCR itself.
- Word conversion.
- Extracting and linking figures (a figure is shown as "linked to 1.4" only).
- Real parsing.
- Sharing beyond the college (waits on DHET clearance).
