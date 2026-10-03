# Question-type coverage audit (2026-10-03)

**Purpose.** The exam-practice experience was built from ONE paper (Life Sciences P1 May/June 2026). The platform's goal is that
internal users upload ANY past paper + memo and the app ingests it. This audit measures how far today's question-type catalogue
(`catalogue.md`) reaches, by marks, on eight papers chosen to differ most from the one we built.

**Method.** One AI auditor per paper read the question paper and memo (page images where layout mattered) and classified every
marks-bearing part as `fits` (an existing type as-is), `settings` (an existing type plus a named setting or small extension) or
`no-fit` (a new type), naming each need generically. Per-part data: the `*.json` files here. Totals were re-computed from the JSON.
**Caveat:** classifications are AI judgements, not re-checked part by part; treat them as a ranked map, not a verdict.

## Results (marks: fits / settings / no-fit)

| paper | fits | settings | no-fit |
|---|---|---|---|
| NC(V) Applied Engineering Technology L4 (100) | 92 | 0 | 8 |
| Life Sciences P2 Nov 2025 | 136 | 8 | 6 |
| Geography P2 Nov 2025 | 115 | 31 | 4 |
| Business Studies P1 Nov 2025 (150 a learner sits; 230 offered) | ~98 | ~12 | ~40 |
| Mathematical Literacy P2 Nov 2025 | 94 | 45 | 11 |
| Physical Sciences P1 Nov 2025 | 66 | 66 | 18 |
| Mathematics P2 Nov 2025 | 50 | 45 | 55 |
| Mathematics P1 Nov 2025 | 16 | 35 | 99 |

## The needs, across subjects (approximate, overlapping marks from the auditors' reports)

1. **Working marked by method** (~230): formula -> substitution -> answer with unit (Physical Sciences), multi-line algebra
   (Mathematics), verify-a-claim with a verdict (Maths Lit), other valid methods (memos give up to five), follow-through ACROSS parts.
2. **Maths input** (~70): expressions, intervals / inequalities, several roots, surds, scientific notation, allele notation.
3. **Written-answer settings** (~45): sub-max groups, a mark only if the identification is right, minimum categories.
4. **Structured essay** (40 sat): sections with caps + insight marks (Business Studies).
5. **Geometry proof** (23): statement + reason, tappable numbered angles.
6. **Map and image tools** (~30): zoomable map sheet with grid blocks, measure with a scale bar, bearings / degrees-minutes.
7. **Plot or sketch a graph** (~17).

## Findings for ingestion (not question types)

- Mathematics and Maths Lit papers are SCANS with no text layer: ingestion needs vision OCR.
- Resources referenced but not in the PDF: Geography's topographic map and orthophoto.
- Memos contain errors (NC(V): an unstated 1,5 kN load; "130" for about 13 degrees) and samples from other papers (Geography memo p.3):
  a human review gate is required before a paper goes live.
- Memos come as .doc too (NC(V)).

## A marking bug found (affects the built paper)

The term type's spelling tolerance (1 slip per 5 letters, max 2) accepts a DIFFERENT real term one or two letters away. Verified:
"complete dominance" passes for "incomplete dominance"; "Prophase II" / "Prophase I" pass for each other. ("discontinuous" vs
"continuous" is correctly rejected: distance 3.) Fix: a near-miss that is itself a known term is rejected (a reject list per part,
plus a subject glossary).
