"""Grade 11 Mathematics P1 Nov 2017 (DBE common paper), the whole paper (Questions 1 to 9, 150 marks, 3 hours as the cover
prints them), hand-transcribed into the catalogue format, then run through `ingest.py --from-json` like any ingested paper.
Stems, marks, answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are
ours. No API call: the transcription is the source, kept in git (out/ is not). The question paper is a SCAN (no text layer, 7
pages, English only): read from its page images rendered at 150 dpi, exponents and roots (2.1, 2.2.1, 2.3, 2.4) checked on a crop
at 220 dpi. The memo has a text layer that garbles fractions, powers and roots, so it was read from its page images at 150 dpi,
zoomed to 220-250 dpi where a sign or an index mattered (2.4's exponents, 6.3's substitution line).

  python tools/ingest/transcribe_g11_math_p1_2017_11.py
  python tools/ingest/ingest.py "uploads/Grade 11 Mathematics P1 Nov 2017 Eng.pdf" "uploads/Grade 11 Mathematics P1 Nov 2017 MG Afr & Eng.pdf" --id g11-math-p1-2017-11 --from-json

How the memo's shapes map (the Grade 12 rulings of 2026-10-10, as in transcribe_math_p1_2025_11.py and the same grade's other
year, transcribe_g11_math_p1_2018_11.py):
  Every value, expression or set the memo WORKS OUT in two or more lines (solve, simplify, calculate, determine, show that, a
  'write down' whose memo shows a working: 4.1, 6.2, 6.4) -> authored whole-working multiple choice, `work`: the memo's FIRST
  method line by line ("{a}/{b}" a stacked fraction, a fractional power written ^(a/b)) and three workings each built from a
  DIFFERENT real error, every option of a part the same layout (`shape`), the right one's place spread over A-D across the paper;
  the part keeps its marks, all or nothing. In a 'show that' (2.4, 4.5, 9.2) every option ends in the given result: a wrong one
  reaches it through a wrong step, a calculator's rounding or by starting from the answer. A form the memo ALSO accepts never
  appears in a wrong option, and neither does a memo slip's reading (5.8's x < −3).
  An answer the memo states with no working (a pair of roots, asymptotes, a range, an interval) -> authored multiple choice of
  answers: the memo's and three common errors. One number with no working (6.5) stays num.
  The sketch 5.7 -> draw with build "sketch" (2026-10-11: f and g placed on one grid, each curve drawn through its features,
  marked online against the memo's six criteria); the tree diagram 8.1.1 -> draw with build "tree" and the Venn diagram 9.1 -> draw
  with build "venn" (2026-10-11: each branch's outcome and probability and each end's outcome; each region's number or form in x;
  marked online against the memo's criteria). No written answer in this paper: 8.2.1 and 8.2.2 justify 'with appropriate calculations', so they are
  workings, as the 2018 paper's 9.1.
  Where a part's stem, options or criteria show an EARLIER part's answer it carries "after" (the assert at the end).
Missions: Questions 4, 5, 6 and 9 share one stem (a pattern, two functions, a graph, a survey), so each is one mission;
Questions 1, 2, 3, 7 and 8 are their numbered groups (1.1, 1.2, ...; 8.1 with its bag, 8.2 with its events).
The figure box is measured in PDF points (page 595 x 841, read from the PDF) from the ink on the scan (scratch tool
lower/g11-math-p1-2017-11/figs.py) and checked on the padded crop (ingest's 1% pad applied)."""
import json
import re
from pathlib import Path

PID = "g11-math-p1-2017-11"
W, H = 595.0, 841.0
FIGS = {  # [page, x0, y0, x1, y1] in points, tight round the ink (ingest.py adds 1% of the page on each side)
    "Q6": [5, 56.5, 166.2, 549.4, 470.4]}   # f, g, the axes and the points A(−2 ; 4), B, C, D, O


def fig(name, caption):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


num = lambda n, q, a, tol, unit, clues, marks=1, **kw: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol,
                                                        "unit": unit, **kw}
draw = lambda n, q, marks, criteria, clues, memo="", **kw: {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                           "criteria": [{"text": t, "marks": m} for t, m in criteria],
                                                           **({"memo": memo} if memo else {}), **kw}

ANSWER = "\n\nChoose the correct answer."
WORK = "\n\nChoose the correct working."
AUTHORED = []   # the whole-working multiple choice, in paper order


def shape(o):
    """An option's layout: its line count and how many lines end in a [reason]."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


def work(n, q, marks, opts, a, clues, **kw):
    """A worked part as authored multiple choice: opts are the memo's FIRST working and three workings built from common errors,
    one step a line, a fraction {numerator}/{denominator}; the part keeps its marks, all or nothing. kw: "after"."""
    assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
    assert len({shape(o) for o in opts}) == 1 and shape(opts[0])[0] >= 2, (n, [shape(o) for o in opts])
    assert 0 <= a <= 3, (n, a)
    AUTHORED.append(n)
    return mcq(n, q + WORK, opts, a, clues, marks=marks, **kw)


# ---- QUESTION 1, the question paper page 3 and the memo pages 2-3 ----
QF = "x = {−b ± √(b² − 4ac)}/{2a}\n"
SQ = "√(x − 1) = x − 3\n(√(x − 1))² = (x − 3)²\n"
q11 = [
    mcq("1.1.1", "(2x − 3)(x + 7) = 0" + ANSWER, ["x = −{3}/{2} or x = 7", "x = 3 or x = −7", "x = {3}/{2} or x = −7", "x = {2}/{3} or x = −7"], 2,
        ["When is a product of two factors equal to zero?", "What equation does each bracket give, and how do you solve 2x − 3 = 0?"], marks=2),
    work("1.1.2", "7x² + 3x − 2 = 0 (leave your answer correct to TWO decimal places)", 3, [
        "x = {−b ± √(b² − 4ac)}/{a}\nx = {−(3) ± √((3)² − 4(7)(−2))}/{7}\nx = {−3 ± √65}/{7}\nx = 0,72 or x = −1,58",          # divided by a, not 2a
        QF + "x = {−(3) ± √((3)² − 4(7)(−2))}/{2(7)}\nx = {−3 ± √65}/{14}\nx = −0,79 or x = 0,36",                                # the memo
        "x = {b ± √(b² − 4ac)}/{2a}\nx = {3 ± √((3)² − 4(7)(−2))}/{2(7)}\nx = {3 ± √65}/{14}\nx = 0,79 or x = −0,36",            # b for −b
        QF + "x = {−(3) ± √((3)² − 4(7)(2))}/{2(7)}\nx = {−3 ± √(−47)}/{14}\nNo real roots"], 1,                                   # c's sign lost
        ["Does the trinomial factorise, or do you need the quadratic formula?", "What are a, b and c, and what does b² − 4ac come to?"]),
    work("1.1.3", "√(x − 1) + 3 = x", 6, [
        SQ + "x − 1 = x² − 6x + 9\nx² − 7x + 10 = 0\n(x − 2)(x − 5) = 0\nx = 2 or x = 5",                                         # no check: x = 2 kept
        SQ + "x − 1 = x² + 9\nx² − x + 10 = 0\nΔ = (−1)² − 4(1)(10) = −39\nNo real solution",                                     # (x − 3)² taken as x² + 9
        "√(x − 1) + 3 = x\n(√(x − 1))² + 3² = x²\nx − 1 + 9 = x²\nx² − x − 8 = 0\nx = {1 ± √33}/{2}\nx = 3,37 or x = −2,37",     # squared term by term
        SQ + "x − 1 = x² − 6x + 9\nx² − 7x + 10 = 0\n(x − 2)(x − 5) = 0\nx = 5 (x ≠ 2)"], 3,                                      # the memo
        ["What should be on its own on one side before you square both sides?", "Why must you test each answer in the original equation?"]),
    work("1.1.4", "x² > 3(x + 6)", 4, [
        "x² − 3x − 18 > 0\n(x − 6)(x + 3) > 0\nx < −3 or x > 6",           # the memo
        "x² − 3x − 18 > 0\n(x − 6)(x + 3) > 0\n−3 < x < 6",                # the region between the roots
        "x² − 3x − 18 > 0\n(x + 6)(x − 3) > 0\nx < −6 or x > 3",           # the signs in the factors swapped
        "x² − 3x − 6 > 0\nx = {3 ± √33}/{2}\nx < −1,37 or x > 4,37"], 0,   # 3(x + 6) expanded as 3x + 6
        ["What do you get when you expand the bracket and move every term to one side?", "Is the parabola above the x-axis between its "
                                                                                         "roots or outside them?"])]
SUB = "x = 1 − 2y\n(1 − 2y)² + y² + 3y(1 − 2y) + y = 0\n"
q12 = [
    work("1.2", "Solve for x and y simultaneously:\n2y + x = 1\nx² + y² + 3xy + y = 0", 6, [
        SUB + "1 + 4y² + y² + 3y − 6y² + y = 0\n−y² + 4y + 1 = 0\ny = 2 ± √5\ny = 4,24 or y = −0,24\nx = −7,47 or x = 1,47",   # (1 − 2y)² as 1 + 4y²
        SUB + "1 − 4y + 4y² + y² + 3y + 6y² + y = 0\n11y² + 1 = 0\ny² = −{1}/{11}\ny² cannot be negative\nNo solution",          # 3y(1 − 2y) as 3y + 6y²
        SUB + "1 − 4y + 4y² + y² + 3y − 6y² + y = 0\n1 − y² = 0\n(1 − y)(1 + y) = 0\ny = 1 or y = −1\nx = −1 or x = 3",          # the memo
        SUB + "1 − 4y + 4y² + y² + 3y − 6y² + y = 0\n1 − y² = 0\ny² = 1\ny = 1\nx = −1"], 2,                                     # only the positive root
        ["Which equation is easier to make x or y the subject of?", "After substituting and collecting like terms, what equation in y do "
                                                                    "you get?"])]
q13 = [
    work("1.3", "If f(x) = 0 has roots x = (−5 ± √(3 − 12k²))/4, for which values of k will the roots be equal?", 3, [
        "Equal roots: 3 − 12k² ≥ 0\n1 − 4k² ≥ 0\nk² ≤ {1}/{4}\n−{1}/{2} ≤ k ≤ {1}/{2}",   # the condition for real roots
        "Equal roots: 3 − 12k² = 0\n1 − 4k² = 0\nk² = {1}/{4}\nk = ±{1}/{2}",             # the memo
        "Equal roots: 3 − 12k² = 0\n12k² = 3\nk² = 4\nk = ±2",                            # the division upside down
        "Equal roots: 3 − 12k² = 0\n1 − 4k² = 0\nk² = {1}/{4}\nk = {1}/{2}"], 1,          # the negative root lost
        ["Which part of the formula decides the nature of the roots?", "What is true of the discriminant when the two roots are equal?"])]

# ---- QUESTION 2, the question paper page 3 and the memo pages 4-5 ----
q21 = [
    work("2.1", "Simplify fully, WITHOUT using a calculator:\n(3ᵐ⁺⁴ − 6 · 3ᵐ⁺¹)/(7 · 3ᵐ⁺²)", 4, [
        "= {3ᵐ⁺¹(3³ − 6)}/{7 · 3ᵐ⁺¹ · 3}\n= {3³ − 6}/{7 · 3}\n= {21}/{21}\n= 1",          # the memo
        "= {3ᵐ⁺¹(3⁴ − 6)}/{7 · 3ᵐ⁺¹ · 3}\n= {3⁴ − 6}/{7 · 3}\n= {75}/{21}\n= {25}/{7}",   # 3ᵐ⁺⁴ split as 3ᵐ⁺¹ · 3⁴
        "= {3ᵐ⁺¹(3³ − 6)}/{7 · 3ᵐ⁺¹}\n= {3³ − 6}/{7}\n= {21}/{7}\n= 3",                   # the 3 of 3ᵐ⁺² = 3ᵐ⁺¹ · 3 lost
        "= {3ᵐ⁺¹(3³ − 6)}/{7 · 3ᵐ⁺¹ · 3}\n= {3³ − 6}/{7 · 3}\n= {3}/{21}\n= {1}/{7}"], 0, # 3³ taken as 9
        ["Which power of 3 can you take out as a common factor of every term?", "How can you write 3ᵐ⁺⁴ and 3ᵐ⁺² as 3ᵐ⁺¹ times a number?"])]
P2 = "2²ˣ − 2ˣ = 2\n"
q22 = [
    work("2.2.1", "x^(−3/4) = 8", 3, [
        "x = (2³)^(4/3)\nx = 2⁴\nx = 16",                  # raised to 4/3, the sign of the exponent lost
        "x = (2³)^(−3/4)\nx = 2^(−9/4)\nx = 0,21",         # raised to the same power, not its reciprocal
        "x = (2³)^(−4/3)\nx = 2⁻⁴\nx = {1}/{16}",          # the memo
        "x = (2³)^(−4/3)\nx = 2⁻⁴\nx = −16"], 2,           # 2⁻⁴ taken as −16
        ["What power must you raise x^(−3/4) to, to leave x on its own?", "How can you write 8 as a power of a prime?"]),
    work("2.2.2", "4ˣ − 2ˣ = 2", 4, [
        P2 + "2²ˣ − 2ˣ − 2 = 0\n(2ˣ − 1)(2ˣ + 2) = 0\n2ˣ = 1 or 2ˣ ≠ −2\nx = 0",            # the signs in the factors swapped
        P2 + "2²ˣ − 2ˣ = 2¹\nThe bases are all 2\n2x − x = 1\nx = 1",                     # the exponents of a difference equated (the memo's 0/4)
        P2 + "2²ˣ − 2ˣ − 2 = 0\n(2ˣ − 1)(2ˣ − 2) = 0\n2ˣ = 1 or 2ˣ = 2\nx = 0 or x = 1",   # k² − k − 2 factorised as (k − 1)(k − 2)
        P2 + "2²ˣ − 2ˣ − 2 = 0\n(2ˣ + 1)(2ˣ − 2) = 0\n2ˣ ≠ −1 or 2ˣ = 2\nx = 1"], 3,      # the memo
        ["How can you write 4ˣ as a power of 2ˣ?", "If you let k = 2ˣ, what kind of equation do you get, and can 2ˣ be negative?"])]
XY = "(x + y)² = ({3 − √a}/{√2} + {4 + √a}/{√2})²\n"
q23 = [
    work("2.3", "If x = (3 − √a)/√2 and y = (4 + √a)/√2, determine the value of (x + y)²", 3, [
        "(x + y)² = ({3 − √a}/{√2})² + ({4 + √a}/{√2})²\n= {9 − 6√a + a + 16 + 8√a + a}/{2}\n= {25 + 2√a + 2a}/{2}\n"
        "= 12{1}/{2} + √a + a",                                                       # (x + y)² taken as x² + y²
        XY + "= ({7}/{√2})²\n= {49}/{2}\n= 24{1}/{2}",                                # the memo
        XY + "= ({7 + 2√a}/{√2})²\n= {49 + 28√a + 4a}/{2}\n= 24{1}/{2} + 14√a + 2a",  # −√a + √a taken as 2√a
        XY + "= ({7}/{2√2})²\n= {49}/{8}\n= 6{1}/{8}"], 1,                            # the denominators added
        ["Do x and y share a denominator, and what happens to the √a terms when you add them?", "What is (√2)²?"])]
R24 = "10^(1/12) · ⁶√(64 · 10) · ⁴√(81 · 10) · √(4 · 10)\n"
q24 = [
    work("2.4", "Show, WITHOUT using a calculator, that ¹²√10 × ⁶√640 × ⁴√810 × √40 = 120", 4, [
        "10^(1/12) · 640^(1/6) · 810^(1/4) · 40^(1/2)\n= 1,2115 × 2,9356 × 5,3348 × 6,3246\n= 1,21 × 2,94 × 5,33 × 6,32\n= 119,83\n"
        "≈ 120",                                                                                  # a calculator and rounding
        R24 + "= 10^(1/12) · 2 · 10^(1/6) · 3 · 10^(1/4) · 2 · 10^(1/2)\n= 2 × 3 × 2 × 10^(4/24)\n= 12 × 10\n= 120",   # 1/12 + 1/6 + 1/4 + 1/2 as 4/24, then 10
        R24 + "= 10^(1/12) · ⁶√(2⁶ · 10) · ⁴√(3⁴ · 10) · √(2² · 10)\n= 10^(1/12) · 2^(6/6) · 10^(1/6) · 3^(4/4) · 10^(1/4) · 2^(2/2) · "
              "10^(1/2)\n= 2 × 3 × 2 × 10^(12/12)\n= 120",                                         # the memo
        "√10 × √640 × √810 × √40\n= √(10 × 640 × 810 × 40)\n= √207 360 000\n= 14 400\n= √14 400 = 120"], 2,   # every root read as a square root
        ["How can you write 640, 810 and 40 as a power of a prime times 10?", "How do you multiply powers of 10 with different fractional "
                                                                              "exponents?"])]

# ---- QUESTION 3, the question paper page 4 and the memo page 6 ----
q31 = [
    work("3.1.1", "Determine a formula for the nᵗʰ term of the pattern.", 2, [
        "d = 17 − 12 = 5\nTₙ = 5n + c, with T₁ = 5 + c = 12\nTₙ = 5n + 7",         # the memo
        "d = 17 − 12 = 5\nTₙ = 5n + c, with c = T₁ = 12\nTₙ = 5n + 12",            # the first term taken as c
        "d = 17 − 12 = 5\nTₙ = 5n + c, with c = 12 + 5\nTₙ = 5n + 17",             # the difference added to the first term for c
        "d = 12 − 17 = −5\nTₙ = −5n + c, with T₁ = −5 + c = 12\nTₙ = −5n + 17"], 0,  # the difference taken the wrong way round
        ["What is the constant difference between consecutive terms?", "Which value of c makes T₁ equal to the first term?"]),
    work("3.1.2", "Calculate the value of T₁₂.", 2, [
        "T₁₂ = 12 + 12(5)\n= 72",       # a + nd, not a + (n − 1)d
        "T₁₂ = 5(11) + 7\n= 62",        # n − 1 put into a formula already in n
        "T₁₂ = 5(12 + 7)\n= 95",        # a bracket round n + 7
        "T₁₂ = 5(12) + 7\n= 67"], 3,    # the memo
        ["Which value of n stands for the 12th term?", "What do you get when you substitute it into your general term?"], after=["3.1.1"]),
    work("3.1.3", "Determine the number of terms in the pattern.", 2, [
        "5n + 7 = 172\n5n = 179\nn = 35,8",       # 7 moved without its sign change
        "172 − 12 = 160\n160 ÷ 5 = 32\nn = 32",   # the steps counted, not the terms
        "5n + 7 = 172\n5n = 165\nn = 33",         # the memo
        "5n + 7 = 172\n5n = 165\nn = 825"], 2,    # multiplied by 5 instead of divided
        ["Is 172 a position in the pattern or the value of its last term?", "Which n makes your general term equal to 172?"], after=["3.1.1"])]
EQD = "x − 3 = y − x\ny = 2x − 3\n"
q32 = [
    work("3.2", "Given the first four terms of a linear pattern: 3; x; y ; 30\n\nCalculate the values of x and y.", 4, [
        EQD + "x − 3 = y − 30\nx − 3 = 2x − 3 − 30\n−x = −30\nx = 30\ny = 57",                          # the third difference taken as y − 30
        EQD + "x − 3 = 30 − y\nx − 3 = 30 − 2x + 3\n3x = 36\nx = 12\ny = 21",                           # the memo
        EQD + "x − 3 = 30 − y\nx − 3 = 30 − 2x − 3\n3x = 30\nx = 10\ny = 17",                           # −(2x − 3) taken as −2x − 3
        EQD + "4d = 30 − 3 (four terms)\nd = {27}/{4}\nx = 3 + {27}/{4}\nx = 9{3}/{4}\ny = 16{1}/{2}"], 1,  # four steps counted between four terms
        ["What is the same between consecutive terms of a linear pattern?", "Which two equations in x and y do the equal differences give "
                                                                            "you?"])]

# ---- QUESTION 4, the question paper page 4 and the memo pages 7-8 ----
DIF = "First differences: −51 ; −45 ; −39\nSecond differences: 6 ; 6\n"
T508 = "3n² − 60n + 301 = 508\n3n² − 60n − 207 = 0\n"
q4 = [
    work("4.1", "Write down the next term of the pattern.", 2, [
        DIF + "T₅ = 109 + (−39 − 6) = 64",     # the second difference subtracted
        DIF + "T₅ = 109 + (−39) = 70",         # the last first difference used again
        DIF + "T₅ = 109 + 6 = 115",            # the second difference added to the term
        DIF + "T₅ = 109 + (−39 + 6) = 76"], 3,  # the memo
        ["What are the first and second differences of the pattern?", "What will the next first difference be?"]),
    work("4.2", "Determine a formula for the nᵗʰ term of the pattern.", 4, [
        "2a = 6, so a = 3\n3a + b = −51, so b = −60\na + b + c = 244, so c = 301\nTₙ = 3n² − 60n + 301",          # the memo
        "a = 6 (the second difference)\n3a + b = −51, so b = −69\na + b + c = 244, so c = 307\nTₙ = 6n² − 69n + 307",  # a taken as the second difference
        "2a = 6, so a = 3\n3a + b = −51, so b = −42\na + b + c = 244, so c = 283\nTₙ = 3n² − 42n + 283",          # 9 added instead of subtracted for b
        "2a = 6, so a = 3\n3a + b = −51, so b = −60\na + b + c = 244, so c = 187\nTₙ = 3n² − 60n + 187"], 0,      # a + b moved without its sign change
        ["How is the second difference related to a in Tₙ = an² + bn + c?", "Which expressions in a, b and c give the first first difference "
                                                                            "and the first term?"]),
    work("4.3", "Which term of the pattern will have a value of 508?", 4, [
        T508 + "n² − 20n − 69 = 0\n(n + 3)(n − 23) = 0\nn = 23 or n = −3",           # the negative root kept
        T508 + "n² − 20n − 69 = 0\n(n − 3)(n + 23) = 0\nn = 3 (n ≠ −23)",            # the signs in the factors swapped
        T508 + "n² − 20n − 69 = 0\n(n + 3)(n − 23) = 0\nn = 23 (n ≠ −3)",            # the memo
        T508 + "n² − 20n − 207 = 0\nn = {20 ± √1 228}/{2}\nn = 27,52 (n ≠ −7,52)"], 2,  # −207 not divided by 3
        ["What equation do you get when you set your general term equal to 508?", "Can n, a term's position, be negative or a fraction?"],
        after=["4.2"]),
    work("4.4", "Between which TWO consecutive terms of the quadratic pattern will the first difference be 453?", 3, [
        "Tₙ = a + nd\n453 = −51 + 6n\n453 + 51 = 6n\n504 = 6n\nn = 84\nBetween T₈₄ and T₈₅",                                         # a + nd, not a + (n − 1)d
        "Tₙ = a + (n − 1)d\n453 = −51 + (n − 1)6\n453 = −57 + 6n\n510 = 6n\nn = 85\nBetween T₈₅ and T₈₆",                              # the memo
        "Tₙ = a + (n − 1)d\n453 = −51 + (n − 1)6\n453 = −57 + 6n\n396 = 6n\nn = 66\nBetween T₆₆ and T₆₇",                              # −57 moved without its sign change
        "Tₙ = 453\n3n² − 60n + 301 = 453\n3n² − 60n − 152 = 0\nn = {60 ± √5 424}/{6}\nn = 22,27 or n = −2,27\nBetween T₂₂ and T₂₃"], 1,  # a term set equal to 453
        ["What kind of pattern do the first differences form, and what is its general term?", "If the nth first difference is 453, between "
                                                                                             "which two terms does it lie?"],
        after=["4.2"]),
    work("4.5", "Show that all the terms of the quadratic pattern are positive.", 4, [
        "Tₙ = 3n² − 60n + 301\n= 3(n − 10)² + 1\n(n − 10)² ≥ 0 for n ∈ N\n3(n − 10)² ≥ 0\n3(n − 10)² + 1 > 0\nAll terms in the pattern are positive",
        # (above) the memo
        "T₁ = 244\nT₅ = 76\nT₁₀ = 1\nT₁₅ = 76\nT₂₀ = 301\nAll terms in the pattern are positive",                     # a few terms tried: no proof
        "Tₙ = 3n² − 60n + 301\n= 3(n − 10)² + 201\n(n − 10)² ≥ 0 for n ∈ N\n3(n − 10)² ≥ 0\n3(n − 10)² + 201 > 0\n"
        "All terms in the pattern are positive",                                                                       # the 100 completed not multiplied by 3
        "T₁ = 244 > 0\nSecond difference = 6 > 0\nSo the pattern has a minimum value\nThe first term is the minimum\nTₙ ≥ 244 for every n\n"
        "All terms in the pattern are positive"], 0,                                                                   # the minimum taken as the first term
        ["What does completing the square tell you about the smallest value of Tₙ?", "Can the square of a number ever be negative?"],
        after=["4.2"])]

# ---- QUESTION 5, the question paper page 4 and the memo pages 8-10 ----
YI = "y = {−3}/{0 + 2} + 1 = −{1}/{2}\ny-intercept (0 ; −{1}/{2})\n"
XI = "0 = {−3}/{x + 2} + 1\n−1 = {−3}/{x + 2}\n"
q5 = [
    work("5.1", "Determine f(−3).", 1, [
        "f(−3) = {−3}/{−3 + 2} + 1\n= −2",       # −3 ÷ (−1) taken as −3
        "f(−3) = {−3}/{3 + 2} + 1\n= {2}/{5}",   # the minus of −3 lost in the denominator
        "f(−3) = {−3}/{−3 + 2}\n= 3",            # the + 1 left off
        "f(−3) = {−3}/{−3 + 2} + 1\n= 4"], 3,    # the memo
        ["Where does −3 go in the formula for f(x)?", "What is a negative number divided by a negative number?"]),
    work("5.2", "Determine x if g(x) = 4.", 2, [
        "4 = 2⁻ˣ − 4\n8 = 2⁻ˣ\n2³ = 2⁻ˣ\nx = 3",            # the minus of −x lost
        "4 = 2⁻ˣ − 4\n8 = 2⁻ˣ\n2³ = 2⁻ˣ\nx = −3",           # the memo
        "4 = 2⁻ˣ − 4\n4 − 4 = 2⁻ˣ\n2⁻ˣ = 0\nNo solution",    # − 4 moved without its sign change
        "4 = 2⁻ˣ − 4\n8 = 2⁻ˣ\n−x = {8}/{2}\nx = −4"], 1,   # 8 divided by the base
        ["What equation do you get when you set g(x) equal to 4?", "How can you write 8 as a power of 2?"]),
    mcq("5.3", "Write down the asymptotes of f." + ANSWER, ["x = 2 and y = 1", "x = 1 and y = −2", "x = −2 and y = −3", "x = −2 and y = 1"], 3,
        ["Which value of x makes the denominator zero?", "Which value does f(x) approach as x becomes very large?"], marks=2),
    mcq("5.4", "Write down the range of g." + ANSWER, ["y > −4", "y ≥ −4", "y < −4", "y > 4"], 0,
        ["What happens to 2⁻ˣ as x becomes very large?", "Can g ever reach its asymptote, and is it above or below it?"]),
    work("5.5", "Determine the coordinates of the x- and y-intercepts of f.", 5, [
        "y = {−3}/{0 + 2} + 1 = −{5}/{2}\ny-intercept (0 ; −{5}/{2})\n" + XI + "−x − 2 = −3, so x = 1\nx-intercept (1 ; 0)",  # −3/2 + 1 with the wrong sign
        YI + XI + "−x − 2 = −3, so x = 5\nx-intercept (5 ; 0)",                                                              # −2 moved without its sign change
        YI + XI + "−x − 2 = −3, so x = 1\nx-intercept (1 ; 0)",                                                              # the memo
        YI + XI + "x + 2 = {1}/{3}, so x = −{5}/{3}\nx-intercept (−{5}/{3} ; 0)"], 2,                                        # the fraction turned upside down
        ["What is x at a y-intercept, and what is y at an x-intercept?", "How can you clear the fraction once the 1 is on the other side?"]),
    work("5.6", "Determine the equation of the axis of symmetry of f which has a negative gradient. Leave your answer in the form y = mx + c.", 2, [
        "y = −x + c\n1 = −(−2) + c\n−1 = c\ny = −x − 1",                          # the memo
        "y = x + c\n1 = (−2) + c\n3 = c\ny = x + 3",                              # the other axis, with a positive gradient
        "y = −x + c\n1 = −(−2) + c\n3 = c\ny = −x + 3",                           # 2 added instead of subtracted
        "y = −x + c\n−{1}/{2} = −(0) + c\n−{1}/{2} = c\ny = −x − {1}/{2}"], 0,   # the y-intercept of f used for the point
        ["Through which point do both axes of symmetry of a hyperbola pass?", "What is the gradient of the axis of symmetry that slopes "
                                                                              "downwards?"], after=["5.3", "5.5"]),
    draw("5.7", "Sketch the graphs of f and g on the same system of axes. Clearly show ALL intercepts with the axes and any asymptotes.", 6, [
        ["f: the asymptotes x = −2 and y = 1", 1], ["f: both pieces (branches) of the hyperbola", 1],
        ["f: the x- and y-intercepts (1 ; 0) and (0 ; −1/2)", 1], ["g: the asymptote y = −4", 1], ["g: the x-intercept (−2 ; 0)", 1],
        ["g: the y-intercept (0 ; −3)", 1]],
        ["Where are the asymptotes of each graph, and where does each graph cut the axes?", "Is a in f(x) = a/(x + p) + q positive or "
                                                                                            "negative, and where does that put the branches?"],
        memo="The memo's sketch: f's two branches about the dashed asymptotes x = −2 and y = 1, one top left and one bottom right, the "
             "bottom-right branch cutting the y-axis at −0,5 and the x-axis at 1; g decreasing from the top left, cutting the x-axis at −2 "
             "and the y-axis at −3, and levelling off above its dashed asymptote y = −4.", after=["5.3", "5.4", "5.5"],
        # built on a grid (2026-10-11): f and g on one set of axes, each memo criterion its features (or f's shape); criterion 0 is
        # both asymptotes of f together and criterion 2 both intercepts of f, so one feature of each carries its mark; the memo marks
        # no shape for g, so g's curve is only drawn through its features
        build={"kind": "sketch", "family": "hyperbola", "x": [-6, 4, 1], "y": [-6, 6, 0.5], "features": [
            {"id": "fva", "kind": "vline", "label": "vertical asymptote of f", "at": -2, "tol": 0, "marks": 1, "crit": 0, "graph": "f"},
            {"id": "fha", "kind": "hline", "label": "horizontal asymptote of f", "at": 1, "tol": 0, "marks": 0, "crit": 0, "graph": "f"},
            {"id": "fx", "kind": "point", "label": "x-intercept of f", "at": [1, 0], "tol": 0, "marks": 1, "crit": 2, "graph": "f"},
            {"id": "fy", "kind": "point", "label": "y-intercept of f", "at": [0, -0.5], "tol": 0, "marks": 0, "crit": 2, "graph": "f"},
            {"id": "gha", "kind": "hline", "label": "asymptote of g", "at": -4, "tol": 0, "marks": 1, "crit": 3, "graph": "g"},
            {"id": "gx", "kind": "point", "label": "x-intercept of g", "at": [-2, 0], "tol": 0, "marks": 1, "crit": 4, "graph": "g"},
            {"id": "gy", "kind": "point", "label": "y-intercept of g", "at": [0, -3], "tol": 0, "marks": 1, "crit": 5, "graph": "g"}],
               "graphs": [{"id": "f", "family": "hyperbola", "label": "f",
                           "shape": {"label": "Shape of f", "answer": "top left and bottom right", "marks": 1, "crit": 1}},
                          {"id": "g", "family": "exponential", "label": "g"}]}),
    mcq("5.8", "If it is given that f(−1) = g(−1), determine the values of x for which g(x) ≥ f(x)." + ANSWER,
        ["−3 ≤ x ≤ −1", "x ≤ −3 or −2 < x ≤ −1", "−3 ≤ x < −2 or x ≥ −1", "x ≤ −3 or −2 ≤ x ≤ −1"], 1,
        ["At which x-values do the graphs of f and g meet?", "Where is the graph of g on or above the graph of f, and what happens at f's "
                                                             "vertical asymptote?"], marks=2, after=["5.2", "5.3"])]
for i in q5:   # the built sketch: its features' and shapes' marks are the memo criteria's, criterion by criterion
    b = i.get("build") or {}
    if b.get("kind") == "sketch":
        got = {}
        for x in b["features"] + [g["shape"] for g in b.get("graphs", []) if g.get("shape")] + ([b["shape"]] if b.get("shape") else []):
            got[x["crit"]] = got.get(x["crit"], 0) + x["marks"]
        assert got == {k: c["marks"] for k, c in enumerate(i["criteria"])}, (i["n"], got)
        assert not b.get("graphs") or all(f.get("graph") in {g["id"] for g in b["graphs"]} for f in b["features"]), i["n"]

# ---- QUESTION 6, the question paper page 5 and the memo pages 11-12 ----
X0 = "0 = −x² − x + 6\n"
FT = "f(−{1}/{2}) = −(−{1}/{2})² − (−{1}/{2}) + 6\n"
FTP = "f(x) = −(x + {1}/{2})² + {25}/{4}\n"
A4 = "f(r) = 4 at A(−2 ; 4), and r < 0: r = −2\n"
q6 = [
    work("6.1", "Determine the x-intercepts f.", 4, [
        X0 + "x² + x − 6 = 0\n(x − 3)(x + 2) = 0\nx = 3 or x = −2\nB(−2 ; 0) and C(3 ; 0)",                    # the signs in the factors swapped
        X0 + "x² + x − 6 = 0\n(x + 3)(x − 2) = 0\nx = −3 or x = 2\nB(−3 ; 0) and C(2 ; 0)",                    # the memo
        X0 + "x² − x + 6 = 0\nΔ = (−1)² − 4(1)(6) = −23\nΔ < 0: no real roots\nf has no x-intercepts",          # −1 multiplied into −x² only
        X0 + "x² + x − 6 = 0\n(x + 3)(x − 2) = 0\nx = −3 or x = 2\nB(2 ; 0) and C(−3 ; 0)"], 1,                # B and C swapped
        ["What is the value of y at an x-intercept?", "What do you get when you multiply the equation by −1, and does it factorise?"]),
    work("6.2", "Write down the equation of the axis of symmetry of f.", 2, [
        "x = {−b}/{2a}\nx = {−(−1)}/{2(1)}\nx = {1}/{2}",         # a taken as 1, not −1
        "x = {−b}/{a}\nx = {−(−1)}/{−1}\nx = −1",                 # divided by a, not 2a
        "y = {−b}/{2a}\ny = {−(−1)}/{2(−1)}\ny = −{1}/{2}",       # a horizontal line written for the axis
        "x = {−b}/{2a}\nx = {−(−1)}/{2(−1)}\nx = −{1}/{2}"], 3,   # the memo
        ["Which formula gives the x-value of a parabola's turning point?", "What are a and b in f(x) = −x² − x + 6?"]),
    work("6.3", "Determine the range of f.", 3, [
        FT + "= 6{1}/{4}\nTP (−{1}/{2} ; 6{1}/{4})\nRange: y ∈ [6{1}/{4} ; ∞)",        # the range the wrong way round
        FT + "= 6{3}/{4}\nTP (−{1}/{2} ; 6{3}/{4})\nRange: y ∈ (−∞ ; 6{3}/{4}]",       # −(−1/2)² taken as +1/4
        FT + "= 6{1}/{4}\nTP (−{1}/{2} ; 6{1}/{4})\nRange: y ∈ (−∞ ; 6{1}/{4}]",       # the memo (its substitution line a slip)
        FT + "= 6{1}/{4}\nTP (−{1}/{2} ; 6{1}/{4})\nRange: y ∈ (−∞ ; −{1}/{2}]"], 2,   # the turning point's x-value for y
        ["At which x-value does f reach its turning point?", "Does f have a largest or a smallest y-value, and what is it?"], after=["6.2"]),
    work("6.4", "Write down the equation of g in the form g(x) = mx + c.", 3, [
        "D(0 ; 6)\nm(AD) = {6 − 4}/{0 − (−2)}\n= 1\ng(x) = x + 6",                          # the memo
        "D(0 ; 6)\nm(AD) = {6 − 4}/{0 − 2}\n= −1\ng(x) = −x + 6",                           # A's x-value subtracted without its sign
        "D(0 ; 6)\nm(AD) = {6 − 4}/{0 − (−2)}\n= 1\ng(x) = x + 4",                          # A's y-value taken as c
        "D(−0,5 ; 6,25)\nm(AD) = {6,25 − 4}/{−0,5 − (−2)}\n= 1,5\ng(x) = 1,5x + 7"], 0,     # D taken as the turning point
        ["Where does D lie, and what is f(0)?", "Which two points of g do you know, and how is a gradient worked out from them?"],
        after=["6.3"]),
    num("6.5", "Write down the average gradient between points A and D.", 1, 0, "",
        ["What are the coordinates of A and D?", "How do you work out the average gradient between two points?"]),
    work("6.6", "Determine the equation of h, if h is the reflection of f about the x-axis and then translated 3 units to the right. Leave your "
         "answer in the form h(x) = a(x + p)² + q.", 3, [
        FTP + "h(x) = (x + {1}/{2} + 3)² − {25}/{4}\nh(x) = (x + {7}/{2})² − {25}/{4}",    # translated to the left
        FTP + "h(x) = (x + {1}/{2} − 3)² − {25}/{4}\nh(x) = (x − {5}/{2})² − {25}/{4}",    # the memo
        FTP + "h(x) = (x + {1}/{2} − 3)² + {25}/{4}\nh(x) = (x − {5}/{2})² + {25}/{4}",    # q not reflected
        FTP + "h(x) = (x + {1}/{2})² − {25}/{4} + 3\nh(x) = (x + {1}/{2})² − {13}/{4}"], 1,  # translated 3 units up, not right
        ["What happens to every y-value when a graph is reflected about the x-axis?", "In y = a(x + p)² + q, how does moving the graph 3 "
                                                                                      "units to the right change p?"], after=["6.3"]),
    mcq("6.7", "Write down the values of x for which f(x) > 0." + ANSWER, ["x < −3 or x > 2", "−3 ≤ x ≤ 2", "−2 < x < 3", "−3 < x < 2"], 3,
        ["Where does f cut the x-axis?", "Is the graph of f above the x-axis between those points or outside them?"], marks=2, after=["6.1"]),
    work("6.8", "If f(p) = f(r) = 4, calculate the value of p − r if r < 0.", 4, [
        A4 + "By symmetry about x = −{1}/{2}: p = 1\np − r = 1 − 2 = −1",                         # r's minus sign lost in p − r
        A4 + "By symmetry about the y-axis: p = 2\np − r = 2 − (−2) = 4",                          # reflected in the y-axis
        A4 + "By symmetry about x = −{1}/{2}: p = 1\np − r = 1 − (−2) = 3",                        # the memo
        "f(p) = 4 at A(−2 ; 4): p = −2\nBy symmetry about x = −{1}/{2}: r = 1\np − r = −2 − 1 = −3"], 2,   # p and r swapped (r < 0 ignored)
        ["Which point on the graph already has a y-value of 4?", "How far is that point from the axis of symmetry, and which other x-value is "
                                                                 "the same distance on the other side?"], after=["6.2"])]

# ---- QUESTION 7, the question paper page 6 and the memo pages 13-14 ----
EFF = "1 + i(eff) = (1 + {i(nom)}/{m})ᵐ\n"
q71 = [
    work("7.1", "A company bought machinery costing R80 000. Using the reducing balance method, the machinery had a book value of R20 000 "
         "after 5 years.\n\nCalculate the rate of depreciation.", 3, [
        "A = P(1 − i·n)\n20 000 = 80 000(1 − 5i)\n0,25 = 1 − 5i\n5i = 0,75\ni = {0,75}/{5}\ni = 0,15\ni = 15%",                      # straight-line depreciation
        "A = P(1 − i)ⁿ\n80 000 = 20 000(1 − i)⁵\n4 = (1 − i)⁵\n⁵√4 = 1 − i\ni = 1 − ⁵√4\ni = −0,31950791\ni = −31,95%",              # A and P swapped
        "A = P(1 − i)ⁿ\n20 000 = 80 000(1 − i)⁵\n0,25 = (1 − i)⁵\n{0,25}/{5} = 1 − i\ni = 1 − {0,25}/{5}\ni = 0,95\ni = 95%",      # divided by 5, not the fifth root
        "A = P(1 − i)ⁿ\n20 000 = 80 000(1 − i)⁵\n0,25 = (1 − i)⁵\n⁵√0,25 = 1 − i\ni = 1 − ⁵√0,25\ni = 0,24214417\ni = 24,21%"], 3,  # the memo
        ["Which formula gives a reducing-balance book value after n years?", "Which value is P and which is A here, and how do you undo a "
                                                                             "fifth power?"])]
q72 = [
    work("7.2", "Calculate the effective interest rate if interest is compounded at 5% p.a., compounded quarterly.", 3, [
        EFF + "1 + i(eff) = (1 + {0,05}/{4})⁴\ni(eff) = 0,050945336…\nEffective rate = 5,09% p.a.",        # the memo
        EFF + "1 + i(eff) = (1 + {0,05}/{12})¹²\ni(eff) = 0,051161897…\nEffective rate = 5,12% p.a.",      # compounded monthly
        EFF + "1 + i(eff) = (1 + {0,05}/{4})⁴\ni(eff) = 1,050945336…\nEffective rate = 105,09% p.a.",      # the 1 not subtracted
        EFF + "1 + i(eff) = (1 + 0,05)⁴\ni(eff) = 0,21550625\nEffective rate = 21,55% p.a."], 0,           # the yearly rate each quarter
        ["How many times a year is the interest added?", "Which formula links a nominal rate compounded m times a year to the effective rate?"])]
q73 = [
    work("7.3", "Sipho invested R30 000 for 6 years. The investment earned interest at 12% p.a., compounded monthly for the first two years. "
         "Thereafter the interest rate changed to 10,8% p.a., compounded semi-annually for the rest of the period.\n\nCalculate the value of "
         "the investment at the end of 6 years. (No other transactions were made on the account.)", 4, [
        "A = P(1 + i)ⁿ\nA = 30 000(1 + {0,12}/{12})²⁴(1 + 0,108)⁸\nA = R86 527,13",             # the yearly rate each half-year
        "A = P(1 + i)ⁿ\nA = 30 000(1 + {0,12}/{12})²(1 + {0,108}/{2})⁸\nA = R46 611,05",        # 2 periods, not 24 months
        "A = P(1 + i)ⁿ\nA = 30 000(1 + {0,12}/{12})²⁴(1 + {0,108}/{2})⁸\nA = R58 017,51",       # the memo
        "A = P(1 + i)ⁿ\nA = 30 000(1 + {0,12}/{12})²⁴(1 + {0,108}/{2})¹²\nA = R71 601,41"], 2,  # 6 years at the second rate, not 4
        ["How many months make up the first stretch, and how many half-years the rest of the 6 years?", "What is the interest rate for each "
                                                                                                        "period in each stretch?"])]
G18 = "(1 + {0,18}/{12})"
q74 = [
    work("7.4", "Mary deposited R25 000 into a savings account with an interest rate of 18% p.a., compounded monthly. Mary withdrew R8 000 from "
         "the account 2 years after depositing the initial amount. She deposited another R4 000 into this account 3½ years after the initial "
         "deposit. What amount will Mary have 5 years after making the initial deposit in this account?", 6, [
        "n = 5 × 12, 2 × 12 and 3,5 × 12 months\nA = 25 000" + G18 + "⁶⁰ − 8 000" + G18 + "²⁴ + 4 000" + G18 + "⁴²\nA = R57 119,86",  # times from the start
        "n = 5 × 12, 3 × 12 and 1,5 × 12 months\nA = 25 000" + G18 + "⁶⁰ − 8 000" + G18 + "³⁶ + 4 000" + G18 + "¹⁸\nA = R52 636,74",  # the memo
        "n = 5 × 12 months\nA = 25 000" + G18 + "⁶⁰ − 8 000 + 4 000\nA = R57 080,49",                                              # R8 000 and R4 000 not grown
        "n = 5 × 12, 3 × 12 and 1,5 × 12 months\nA = 25 000" + G18 + "⁶⁰ + 8 000" + G18 + "³⁶ − 4 000" + G18 + "¹⁸\nA = R69 524,25"],  # the signs swapped
        1, ["For how long does each amount earn interest before the end of the 5 years?", "How do you account for money taken out of the "
                                                                                          "account part-way through?"])]

# ---- QUESTION 8, the question paper page 6 and the memo page 15 ----
AOB = "P(A or B) = P(A) + P(B) − P(A and B)\n0,58 = 0,4 + 0,3 − P(A and B)\nP(A and B) = 0,12 ≠ 0\n"
q81 = [
    draw("8.1.1", "Draw a tree diagram to represent the information above. Show the probabilities associated with EACH branch, as well as the "
         "possible outcomes.", 3, [
        ["Branches: blue and red for the first marble, and blue and red after each for the second", 1],
        ["Probabilities: 3/5 and 2/5 for the first marble; after blue 2/4 and 2/4, after red 3/4 and 1/4", 1],
        ["Outcomes: (B ; B), (B ; R), (R ; B) and (R ; R)", 1]],
        ["How many marbles of each colour are in the bag at the start?", "After one marble is put aside, how many marbles are left, and how "
                                                                         "many of that colour?"],
        memo="The memo's tree: the first marble B 3/5 (0,6) and R 2/5 (0,4); after B: B 2/4 and R 2/4 (1/2 or 0,5 each); after R: B 3/4 and "
             "R 1/4; the outcomes (B ; B), (B ; R), (R ; B) and (R ; R) at the ends of the branches.",
        # built (2026-10-11): the branches drawn (two, then two after each); the learner chooses each branch's outcome (✓ branches), types its
        # probability, a fraction or a decimal, any equal form (✓ probabilities: 2/4 = 1/2 = 0,5 as the memo allows) and chooses each end's
        # outcome (✓ outcomes)
        build={"kind": "tree", "outcomes": [{"id": "B", "name": "blue"}, {"id": "R", "name": "red"}], "stages": ["First marble", "Second marble"],
               "tree": [{"id": "B", "p": "3/5", "next": [{"id": "B", "p": "2/4"}, {"id": "R", "p": "2/4"}]},
                        {"id": "R", "p": "2/5", "next": [{"id": "B", "p": "3/4"}, {"id": "R", "p": "1/4"}]}],
               "crit": {"branches": 0, "p": 1, "out": 2}}),
    work("8.1.2", "Determine the probability of first taking a red marble and then taking a blue marble, in that order.", 2, [
        "P(R ; B) = {2}/{5} × {3}/{4}\n= {3}/{10}",     # the memo
        "P(R ; B) = {2}/{5} × {3}/{5}\n= {6}/{25}",     # as if the first marble went back
        "P(R ; B) = {2}/{5} + {3}/{4}\n= {23}/{20}",    # the probabilities along a branch added
        "P(R ; B) = {2}/{5} × {1}/{4}\n= {1}/{10}"], 0, # red then red
        ["Which branch of your tree is red first and then blue?", "Along a branch, do you add or multiply the probabilities?"], after=["8.1.1"])]
q82 = [
    work("8.2.1", "Are events A and B mutually exclusive?\nJustify your answer with appropriate calculations.", 3, [
        AOB + "Events A and B are mutually exclusive",                                                                       # the wrong conclusion
        "P(A or B) = P(A) + P(B) + P(A and B)\n0,58 = 0,4 + 0,3 + P(A and B)\nP(A and B) = −0,12 ≠ 0\nEvents A and B are not mutually "
        "exclusive",                                                                                                          # + P(A and B)
        "P(A and B) = P(A) + P(B)\n= 0,4 + 0,3\nP(A and B) = 0,7 ≠ 0\nEvents A and B are not mutually exclusive",             # 'and' taken as a sum
        AOB + "Events A and B are not mutually exclusive"], 3,                                                               # the memo
        ["Which identity links P(A or B), P(A), P(B) and P(A and B)?", "What is P(A and B) for two mutually exclusive events?"]),
    work("8.2.2", "Are events A and B independent?\nJustify your answer with appropriate calculations.", 3, [
        "P(A and B) = 0,12\nP(A) + P(B) = 0,4 + 0,3\n= 0,7\n∴ P(A and B) ≠ P(A) + P(B)\nA and B are not independent events",   # the sum, not the product
        "P(A or B) = 0,58\nP(A) × P(B) = 0,4 × 0,3\n= 0,12\n∴ P(A or B) ≠ P(A) × P(B)\nA and B are not independent events",     # P(A or B) compared
        "P(A and B) = 0,12\nP(A) × P(B) = 0,4 × 0,3\n= 0,12\n∴ P(A and B) = P(A) × P(B)\nA and B are independent events",        # the memo
        "P(A and B) = 0,12\nP(A) × P(B) = 0,4 × 0,3\n= 1,2\n∴ P(A and B) ≠ P(A) × P(B)\nA and B are not independent events"], 2,  # 0,4 × 0,3 as 1,2
        ["What must be true of P(A and B) when two events are independent?", "Which value of P(A and B) did you find in 8.2.1?"],
        after=["8.2.1"])]

# ---- QUESTION 9, the question paper page 7 and the memo page 16 ----
AL2 = "P(at least two sports) = "
q9 = [
    draw("9.1", "Draw a Venn diagram to represent the information above.", 5, [
        ["14 (R and V only), 12 (R and C only) or 15 (V and C only) in its region", 1], ["26 − x in R only", 1], ["13 − x in V only", 1],
        ["5 in C only", 1], ["3 outside the three circles", 1]],
        ["Which number goes in the region where all three circles overlap?", "How many like rugby only, once the overlaps are taken out of "
                                                                             "the 52?"],
        memo="The memo's Venn diagram: a rectangle holding three overlapping circles R, V and C: 26 − x in R only, 13 − x in V only, 5 in C "
             "only, 14 in R and V only, 12 in R and C only, 15 in V and C only, x in all three, and 3 outside the circles.",
        # built (2026-10-11): the learner fills all eight regions, each with a form in x where it holds one (26 − x, 13 − x, x). The memo's
        # "✓ 14 or 12 or 15" is one mark for ANY ONE of the three pairs' regions right (any); x in all three is the stem's own value and
        # the memo gives it no tick, so that region is filled but not marked
        build={"kind": "venn", "sets": [{"id": "R", "name": "rugby"}, {"id": "V", "name": "volleyball"}, {"id": "C", "name": "chess"}],
               "outside": True, "unknown": "x",
               "regions": [{"in": "RV", "at": 14, "crit": 0}, {"in": "RC", "at": 12, "crit": 0}, {"in": "VC", "at": 15, "crit": 0},
                           {"in": "R", "at": "26 − x", "crit": 1}, {"in": "V", "at": "13 − x", "crit": 2}, {"in": "C", "at": 5, "crit": 3},
                           {"in": "out", "at": 3, "crit": 4}, {"in": "RVC", "at": "x"}], "any": [0]}),
    work("9.2", "Show that x = 8.", 2, [
        "26 − 8 + 14 + 8 + 12 + 5 + 15 + 13 − 8 + 3 = 80\n80 = 80\nSo x = 8",                                         # starts from the answer
        "26 − x + 14 + x + 12 + 5 + 15 + 13 − x + 3 = 80\n88 − 80 = x\nx = 8",                                        # the memo
        "26 + 14 + 12 + 5 + 15 + 13 + 3 + x = 80\n88 + x = 80, so x = −8\nx = 8 (a number of learners cannot be negative)",  # the −x terms lost
        "Chess: 5 + 12 + 15 + x = 40 (half the learners)\n32 + x = 40\nx = 8"], 1,                                     # half the learners assumed
        ["What must all the regions of the Venn diagram add up to?", "Which regions contain x, and with which sign?"], after=["9.1"]),
    work("9.3", "How many learners like only rugby?", 1, [
        "Rugby only = 26 + x = 26 + 8\n= 34",    # x added
        "Rugby only = 52 − x = 52 − 8\n= 44",    # only x taken out of the 52
        "Rugby only = 52 − 14 − 12\n= 26",       # x not taken out
        "Rugby only = 26 − x = 26 − 8\n= 18"], 3, # the memo
        ["Which region of the Venn diagram holds the learners who like only rugby?", "What is that region's expression once you know x?"],
        after=["9.1", "9.2"]),
    work("9.4", "Calculate the probability that a learner, chosen randomly, likes at least TWO different types of sport.", 3, [
        AL2 + "{12 + 14 + 15 + 8}/{80}\n= {49}/{80}",   # the memo
        AL2 + "{12 + 14 + 15}/{80}\n= {41}/{80}",       # exactly two sports
        AL2 + "{12 + 14 + 15 + 8}/{77}\n= {7}/{11}",    # the 3 who like no sport left out of the total
        AL2 + "1 − {3}/{80}\n= {77}/{80}"], 0,          # at least one sport
        ["Which regions hold learners who like two or all three sports?", "Out of how many learners is the one chosen?"], after=["9.1", "9.2"])]


def venn_ok(i):
    """A built Venn diagram: every region of its sets (and outside, when it is filled) listed once, every criterion earned by a region, every
    entry a whole number or one of the forms the builder offers (x, x + n, x − n, n − x)."""
    b = i["build"]
    ids = [s["id"] for s in b["sets"]]
    want = ([ids[0], ids[0] + ids[1], ids[1]] if len(ids) == 2 else
            [ids[0], ids[1], ids[2], ids[0] + ids[1], ids[0] + ids[2], ids[1] + ids[2], "".join(ids)]) + (["out"] if b["outside"] else [])
    assert sorted(g["in"] for g in b["regions"]) == sorted(want), (i["n"], "regions")
    assert sorted({g["crit"] for g in b["regions"] if "crit" in g}) == list(range(len(i["criteria"]))), (i["n"], "every criterion a region")
    x = b.get("unknown", "x")
    for g in b["regions"]:
        s = re.sub(r"\s+", "", str(g["at"])).replace("−", "-")
        assert re.fullmatch(r"\d+|%s|%s[+-]\d+|\d+[+-]%s" % (x, x, x), s), (i["n"], g)


def tree_ok(i):
    """A built tree: every branch an outcome of the stem's, a point's branches each a different outcome, every probability a fraction or a
    decimal, each point's adding up to 1, and every criterion earned by something the learner gives."""
    b = i["build"]
    ids = [x["id"] for x in b["outcomes"]]
    val = lambda p: (lambda t: float(t[0]) / float(t[1]) if len(t) == 2 else float(t[0]))(p.replace(",", ".").split("/"))
    for kids in [b["tree"]] + [t["next"] for t in b["tree"]]:
        assert all(t["id"] in ids for t in kids) and len({t["id"] for t in kids}) == len(kids), (i["n"], "outcomes")
        assert abs(sum(val(t["p"]) for t in kids) - 1) < 1e-9, (i["n"], "a point's branches add up to 1")
    named = set(b["crit"].values()) | {t["crit"] for t in b["tree"] + [u for t in b["tree"] for u in t["next"]] if "crit" in t}
    assert sorted(named) == list(range(len(i["criteria"]))), (i["n"], "every criterion earned by a component")


for i in q81 + q9:
    k = (i.get("build") or {}).get("kind")
    if k == "venn":
        venn_ok(i)
    if k == "tree":
        tree_ok(i)

# (no caption names a value, an intercept, a turning point or a direction a question asks for: captions show in the enlarged view and
# to screen readers)
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Equations and inequalities", "marks": 15, "lead": "Solve for x:", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Simultaneous equations", "marks": 6, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Nature of roots", "marks": 3, "items": q13},
    {"id": "2.1", "title": "Question 2.1", "kind": "Exponents", "marks": 4, "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Exponential equations", "marks": 7, "lead": "Solve for x, WITHOUT using a calculator:",
     "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Surds", "marks": 3, "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Surds and exponents", "marks": 4, "items": q24},
    {"id": "3.1", "title": "Question 3.1", "kind": "Linear patterns", "marks": 6, "lead": "Given the finite linear pattern: 12 ; 17 ; 22 ; … ; 172",
     "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Linear patterns", "marks": 4, "items": q32},
    {"id": "4", "title": "Question 4", "kind": "Quadratic patterns", "marks": 17, "lead": "Given the quadratic pattern: 244 ; 193 ; 148 ; 109 …",
     "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Hyperbola and exponential graph", "marks": 21,
     "lead": "Given: f(x) = −3/(x + 2) + 1 and g(x) = 2⁻ˣ − 4", "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Parabola and straight line", "marks": 22,
     "lead": "The diagram below shows the graphs of f(x) = −x² − x + 6 and g(x) = mx + c. A(−2 ; 4) is the point of intersection of the "
             "graphs.",
     "figure": fig("Q6", "The parabola f, with its turning point above the x-axis, cuts the x-axis at B, to the left of the origin O, and at "
                   "C, to the right of O, and cuts the y-axis at D. The straight line g cuts the x-axis to the left of B, meets f at "
                   "A(−2 ; 4) and passes through D on the y-axis."), "items": q6},
    {"id": "7.1", "title": "Question 7.1", "kind": "Depreciation", "marks": 3, "items": q71},
    {"id": "7.2", "title": "Question 7.2", "kind": "Effective interest", "marks": 3, "items": q72},
    {"id": "7.3", "title": "Question 7.3", "kind": "Compound interest", "marks": 4, "items": q73},
    {"id": "7.4", "title": "Question 7.4", "kind": "Deposits and withdrawals", "marks": 6, "items": q74},
    {"id": "8.1", "title": "Question 8.1", "kind": "Tree diagrams", "marks": 5,
     "lead": "A bag contains 3 blue marbles and 2 red marbles. A marble is taken from the bag, the colour is recorded and the marble is put "
             "aside. A second marble is taken from the bag, the colour is recorded and then put aside.", "items": q81},
    {"id": "8.2", "title": "Question 8.2", "kind": "Probability rules", "marks": 6,
     "lead": "A and B are two events. The probability that event A will occur is 0,4 and the probability that event B will occur is 0,3. The "
             "probability that either event A or event B will occur is 0,58.", "items": q82},
    {"id": "9", "title": "Question 9", "kind": "Venn diagrams", "marks": 11,
     "lead": "A survey was done among 80 learners on their favourite sport.\nThe results are shown below.\n• 52 learners like rugby (R)\n"
             "• 42 learners like volleyball (V)\n• 5 learners like chess (C) only\n• 14 learners like rugby and volleyball but not chess\n"
             "• 12 learners like rugby and chess but not volleyball\n• 15 learners like volleyball and chess but not rugby\n• x learners "
             "like all 3 types of sport\n• 3 learners did not like any sport", "items": q9},
]

ITEMS = [i for m in missions for i in m["items"]]
assert tuple(AUTHORED) == ("1.1.2", "1.1.3", "1.1.4", "1.2", "1.3", "2.1", "2.2.1", "2.2.2", "2.3", "2.4", "3.1.1", "3.1.2", "3.1.3", "3.2",
                           "4.1", "4.2", "4.3", "4.4", "4.5", "5.1", "5.2", "5.5", "5.6", "6.1", "6.2", "6.3", "6.4", "6.6", "6.8", "7.1",
                           "7.2", "7.3", "7.4", "8.1.2", "8.2.1", "8.2.2", "9.2", "9.3", "9.4"), AUTHORED
ANSWERS = [i["n"] for i in ITEMS if i["t"] == "mcq" and i["n"] not in AUTHORED]   # multiple choice of answers (no working)
assert ANSWERS == ["1.1.1", "5.3", "5.4", "5.8", "6.7"], ANSWERS
assert not [i["n"] for i in ITEMS if i["t"] in ("steps", "rubric")], "a typed calculation or a written answer is left"
assert [i["n"] for i in ITEMS if i["t"] == "num"] == ["6.5"]   # the one read-off number
assert not [i["n"] for i in ITEMS if i["t"] in ("term", "match", "pickn")], "no term, sort or statements in this paper"
assert [i["n"] for i in ITEMS if i["t"] == "draw"] == ["5.7", "8.1.1", "9.1"]
assert [i["n"] for i in ITEMS if (i.get("build") or {}).get("kind") == "sketch"] == ["5.7"]
for i in ITEMS:   # a line that ends in "[...]" draws as a proof's reason: no working here has one
    assert i["t"] != "mcq" or not any(shape(o)[1] for o in i["opts"]), i["n"]
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P1", "sitting": "November 2017", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematics", "total": 150, "missions": missions}],
    "flags": [
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice, whole workings: every part the memo works out in two or more "
                                                       "lines (a solution, a simplification, a term, a formula, a value, an equation, a rate, an "
                                                       "amount, a probability, a 'show that', a 'write down' with a working) plays as four "
                                                       "workings, the memo's FIRST method line by line and three built from real errors (a sign "
                                                       "or factor slip, a wrong formula, rate or period, a misread value, a dropped step or root, "
                                                       "a wrong region or count), one step a line, 0 or full marks: " + ", ".join(AUTHORED) +
                                                       " (%d parts, %d marks). In a 'show that' (2.4, 4.5, 9.2) every option ends in the given "
                                                       "result; a wrong one reaches it through a wrong step, a calculator's rounding or by "
                                                       "starting from the answer. 2.2.2's option that reaches x = 1 by equating the exponents "
                                                       "of a difference (2x − x = 1) is the memo's own 'breakdown: 0/4' case. 4.1 (answer only "
                                                       "2/2 in the memo) plays as its working of differences." % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "1.1.1", "kind": "no_fit", "detail": "Authored multiple choice, answers: " + ", ".join(ANSWERS) + " ask for an answer the memo states "
                                                   "with no working (a pair of roots, the asymptotes, a range, an interval) that a word marker "
                                                   "cannot read (y > −4 from y ≥ −4, x ≤ −3 from x < −3): four options, the memo's answer and "
                                                   "three common errors, 0 or full marks."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 9), hand-transcribed from a SCANNED question paper (no "
                                                           "text layer) and the memo's page images (its text layer garbles fractions, powers and "
                                                           "roots); no API call."},
        {"n": "6.5", "kind": "no_fit", "detail": "One read-off number stays typed on the keypad: 6.5 (the average gradient between A and D, the "
                                                 "gradient of g: 1, exact)."},
        {"n": "5.7", "kind": "no_fit", "detail": "The sketch of f and g is BUILT on one grid (2026-10-11): the learner places f's two asymptotes "
                                                 "and both intercepts, and g's asymptote and both intercepts; each curve is drawn through its "
                                                 "own features, and the memo's six criteria are marked from the placed features and f's shape "
                                                 "(both branches). The memo marks no shape for g. The tree diagram (8.1.1) and the Venn diagram "
                                                 "(9.1) are BUILT (2026-10-11): the tree's branches are drawn, the learner choosing each "
                                                 "branch's outcome (✓ branches), typing its probability (✓ probabilities, any equal form: 2/4 "
                                                 "= 1/2 = 0,5) and choosing each end's outcome (✓ outcomes); the Venn diagram's eight regions "
                                                 "are filled, each a number or a form in x (26 − x, 13 − x, x)."},
        {"n": "9.1", "kind": "no_fit", "detail": "The memo's '✓ 14 or 12 or 15' is one mark for ANY ONE of the three pairs' regions right "
                                                 "(R and V only 14, R and C only 12, V and C only 15). x in all three is the stem's own value and "
                                                 "the memo gives it no tick: the learner fills that region, and it is not marked."},
        {"n": "6.1", "kind": "low_confidence", "detail": "The paper prints 'Determine the x-intercepts f.' (an 'of' missing); kept as printed."},
        {"n": "3.2", "kind": "memo_issue", "detail": "The memo's difference diagram (page 6) labels the third difference y − 30; its working uses "
                                                     "30 − y (x − 3 = 30 − y, x = 12, y = 21). The right option is the working; the wrong option "
                                                     "built on y − 30 ends in x = 30 and y = 57, never the memo's values."},
        {"n": "5.8", "kind": "memo_issue", "detail": "The memo (page 10) gives x ≤ −3 or −2 < x ≤ −1, OR x ∈ (−∞ ; −3) ∪ (−2 ; −1]: its interval "
                                                     "leaves out −3, where f(−3) = g(−3) = 4, so −3 belongs. The right option is x ≤ −3 or −2 < x "
                                                     "≤ −1; the slip's reading (x < −3 or −2 < x ≤ −1) is in no option."},
        {"n": "6.3", "kind": "memo_issue", "detail": "The memo's substitution line (page 11) reads −(1/2)² − (1/2) + 6, which is 5 1/4; its result 6 "
                                                     "1/4 is f(−1/2) = −(−1/2)² − (−1/2) + 6. The right option writes −(−1/2)² − (−1/2) + 6 = 6 "
                                                     "1/4; no option uses the slip's line."},
    ],
}
QTOTAL = {"1": 24, "2": 18, "3": 10, "4": 17, "5": 21, "6": 22, "7": 16, "8": 11, "9": 11}   # the paper's [n] per question
per_q = {}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    print(m["id"], "parts:", len(m["items"]), "marks:", got, "/", m["marks"])
assert per_q == QTOTAL, per_q
# the right letter (no printed multiple choice in this paper, so every letter is ours): the 39 authored workings as even as 39 allows
# (9 or 10 each: the brief's 3-7 band is for fewer workings), and all 44 four-option questions even (11 each)
at = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq"]
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 1, spread
worked = {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"}
assert max(worked.values()) - min(worked.values()) <= 1 and min(worked.values()) >= 3, worked
four = ["ABCD"[i["a"]] for i in ITEMS if i["t"] == "mcq" and len(i["opts"]) == 4]
fspread = {k: four.count(k) for k in "ABCD"}
assert len(four) == len(at) and max(fspread.values()) - min(fspread.values()) <= 3, fspread
print("right options, the paper:", spread, "authored workings:", worked, "four-option:", fspread)
total = sum(i["marks"] for i in ITEMS)
assert total == 150, total
print("authored workings:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; answers:", len(ANSWERS), "parts")
print("total:", total)
# every gate, so a dropped "after" fails the run
assert {i["n"]: i["after"] for i in ITEMS if i.get("after")} == {
    "3.1.2": ["3.1.1"], "3.1.3": ["3.1.1"],                        # Tₙ = 5n + 7
    "4.3": ["4.2"], "4.4": ["4.2"], "4.5": ["4.2"],                # Tₙ = 3n² − 60n + 301
    "5.6": ["5.3", "5.5"],                                         # (−2 ; 1), and a wrong option's y-intercept −1/2
    "5.7": ["5.3", "5.4", "5.5"],                                  # the criteria: f's asymptotes and intercepts, g's asymptote y = −4
    "5.8": ["5.2", "5.3"],                                         # x = −3 (g(x) = 4) and the asymptote x = −2
    "6.3": ["6.2"], "6.8": ["6.2"],                                # x = −1/2
    "6.4": ["6.3"], "6.6": ["6.3"],                                # the turning point (−1/2 ; 6 1/4)
    "6.7": ["6.1"],                                                # x = −3 and x = 2
    "8.1.2": ["8.1.1"],                                            # the tree: 2/5, then 3/4
    "8.2.2": ["8.2.1"],                                            # P(A and B) = 0,12
    "9.2": ["9.1"],                                                # the Venn regions 26 − x, 13 − x, ...
    "9.3": ["9.1", "9.2"], "9.4": ["9.1", "9.2"]}                  # x = 8
out = Path(__file__).parent / "out" / PID   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper's page images and the memo's "
                                                                       "page images (no API call)",
                                                        "scope": "Questions 1 to 9 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
