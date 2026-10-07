# Mark-map schema (one JSON file per DOCUMENT)

File name: `<pdf name without .pdf>.json` in this folder.

```json
{
  "file": "Life Sciences P1 Nov 2024 Eng.pdf",
  "kind": "QP | MG",
  "paper_total": 150,                      // as printed on the cover / at the end ("GRAND TOTAL")
  "sections": [ {"name": "SECTION B", "rule": "Answer ALL" , "questions": [2, 3]} ],
                                            // rule verbatim-ish: "Answer ALL", "Answer any TWO", "Answer any ONE"
  "questions": [
    {
      "q": 2,
      "printed_total": 50,                  // the [n] printed at the end of the question; null if none printed
      "items": [                            // LEAF mark allocations, in paper order
        {"label": "2.1.1(a)", "marks": 1},
        {"label": "2.1.3", "marks": 6}
      ],
      "subtotals": [ {"label": "2.1", "marks": 15} ],   // printed subtotals for a group (e.g. "(15)" closing 2.1)
      "notes": "anything odd: misprint, unreadable, marks not printed, etc."
    }
  ]
}
```

Rules
- Labels: dotted numbers exactly as printed (`2.1.3`); a lettered part gets `(a)`, `(b)` appended (`2.1.1(a)`).
  Roman-numeral or other parts likewise (`3.2.1(i)`).
- A leaf = the smallest part that has its own mark allocation. If marks are only printed for a group as `(10 x 2) (20)`,
  list each leaf (1.1.1 .. 1.1.10) with marks 2 and record the group in `subtotals` as `{"label":"1.1","marks":20}`.
- In a MEMO, `marks` = the allocation the memo prints for that item (the `(n)` after it, or `Max (n)`), NOT a count of ticks.
  If the memo prints no number for an item, count ticks and say so in `notes`.
- Essays / extended writing: one leaf for the whole essay (e.g. `{"label":"5","marks":40}`); put the memo's rubric breakdown
  (e.g. "Intro 2, Content 32, Conclusion 2, Insight 4") in `notes`.
- Record what is PRINTED. Do not correct the paper. If the printed numbers do not add up, record them as printed and say so in `notes`.
- Extract the QP and the memo INDEPENDENTLY: finish and save the QP file before opening the memo, so the memo cannot bias the QP read.

# Inventory fields (QP files only): add to EACH item

```json
{"label": "2.1.3", "marks": 6,
 "type": "mcq | match | term | true_false | fill_blank | short_answer | explain | calculation | proof | drawing | graph_plot | table_complete | map_measure | essay | other",
 "figure": "none | diagram | photo | graph | table | map | orthophoto | cartoon | scenario_text | data_sheet | annexure",
 "figure_ref": "e.g. 'diagram for 2.1' or 'ANNEXURE A' (null if none)",
 "answer_on": "answer_book | answer_sheet | special_answer_book",
 "phone_fit": "easy | medium | hard",       // how well a phone can take this answer (tap / one word = easy;
                                              // short typed sentence = medium; drawing, long working, essay, map measuring = hard)
 "prompt": "first ~12 words of the question text"}
```
And in MEMO items add `"memo_shape": "exact | any_n_of_list | open_marker_judgement | method_marks | rubric | alternatives"`.
