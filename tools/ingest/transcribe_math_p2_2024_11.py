"""Mathematics P2 Nov 2024, the whole paper (Questions 1 to 11: statistics, analytical geometry, trigonometry, Euclidean geometry),
hand-transcribed into the catalogue format (as if Claude had produced it), then run through `ingest.py --from-json` like any
ingested paper. Stems, marks, answers and the memo's working are the paper's and the memo's own (its English); clues, figure
captions and the wrong options of the authored multiple choice are ours. No API call: the transcription is the source, kept in git
(out/ is not). The question paper and the answer book are SCANS (no text layer) and the memo's text layer garbles fractions, roots
and diagrams: everything was read from the page IMAGES (1,5x).

  python tools/ingest/transcribe_math_p2_2024_11.py
  python tools/ingest/ingest.py "<...>/Mathematics P2 Nov 2024 Eng.pdf" "<...>/Mathematics P2 Nov 2024 MG Afr & Eng.pdf" \
      --id math-p2-2024-11 --from-json --answer-book "<...>/Mathematics P2 Nov 2024 Answer Book Afr & Eng.pdf"

How the memo's shapes map (as Mathematics P2 Nov 2025: the phone has a number keypad, multiple choice, short text and self-checked
drawings, no algebra input):
  every calculation the memo works (a, b, a prediction, a quartile, a percentage, a gradient, an equation of a line, a length, a
  ratio, an area ratio, a coordinate, a trig value, a solved equation, a maximum, a distance, "Calculate, with a reason" an angle)
  -> authored multiple choice, `work` (Murci, 2026-10-10): the memo's FIRST working line by line, its result last, and three
  workings built from real errors (a wrong formula, a sign slip, the wrong root rejected, a misread value, a ratio upside down,
  rounding too early, the wrong quadrant, a wrong reason), each ending in a confident result; 0 or full marks. 4.1's memo gives
  the coordinates only, so its working (the midpoint) is ours. A form the memo also accepts (2.5's 35 employees, 8.2's sine
  rule or EB̂C = 32°) is never a wrong option;
  a one-value read-off or write-down (1.2 r, 1.4 the mean, 2.1 the median, 2.2 Q₁, 6.3.2, 7.1 the asymptote's x = 90°, 7.3.1
  the period) -> num, its tolerance covering the memo's rounding (0,006 for a value keyed at two decimals);
  "How does ... influence the standard deviation" -> term (its phrasings, 'increases' / 'decreases' rejected);
  "Draw a box and whisker diagram" (2.4) -> draw with build "boxplot" (2026-10-11: the five values placed on the answer book's
  scaled line, the box and whiskers drawn from them, marked online against the memo's two ticks; flagged no_fit); "draw the graph of g" (7.3.2)
  -> draw with build "sketch" (2026-10-11: its turning points placed on a grid, the curve drawn through them, marked online
  against the memo's criteria).
  A part whose options or criteria show an earlier part's answer opens only once that part is answered (`after`).
  Authored multiple choice (Murci, 2026-10-10) for every part a word or number marker cannot score: an interval (7.2), an expression
  in p (5.2), a general solution with working (7.4), "Show that" (3.3, 4.3, 4.4, 6.1.2), a derivation (6.1.1) and the proofs (4.6,
  9.2, 10.1, 10.2.1, 11.1-11.4). The stem gets "Choose the correct answer." (a short answer) or "Choose the correct working." (a
  working or a proof); four options: the memo's own answer or first method, and three built from real errors (a sign slip, a lost
  solution, the wrong theorem or reason, a converse, a circular reason, a flawed step that still claims the result). Options are
  laid out AS THE MEMO: one step per line ("\n"), a proof's [reason] at the END of its line, a fraction {numerator}/{denominator}
  (drawn stacked); every option of a part has the same number of lines and [reasons], so the layout never points at the answer;
  the right option sits at A, B, C and D ten times each over the paper (proofs and calculations). Each keeps its marks (0 or full).
A mission is a question with its stem and diagram; a question whose stem changes part-way is two or three missions (5, 6, 10). A
single-line MCQ in a figure mission carries the figure itself (the MCQ stage shows an item's own figure only); a working MCQ plays
on the page, under the mission's figure.
Figure boxes are measured in PDF points (page 595.2 x 841.68) from the 1,5x page images and ink-column profiles, and checked on
crops made as the ingest makes them (1% pad, 150 dpi; scratchpad math2_24: figs.py + figs.json); `inset` 40 on Q1 and Q2, whose
axis labels sit near the crop's top-left corner (the page's Hide button sits there). No figure comes from the answer book: its
diagrams repeat the question paper's (the push-up table, the ogive, Q3-Q5, the graph of tan x, Q8-Q11), and 2.4's scaled line is
described in the draw's memo; --answer-book is passed anyway, so an answer-book figure added later needs no change to the command."""
import json
import re
from pathlib import Path

W, H = 595.2, 841.68
FIGS = {  # tools: scratchpad math2_24/figs.py + figs.json; [source, page, x0, y0, x1, y1] in points ("qp" the question paper, "ab" the answer book)
    "Q1": ["qp", 3, 122, 253, 517, 497], "Q2": ["qp", 4, 93, 141, 530, 397], "Q3": ["qp", 5, 113, 148, 493, 477],
    "Q4": ["qp", 6, 93, 172, 483, 453], "Q5": ["qp", 7, 213, 141, 343, 263], "Q7": ["qp", 9, 87, 150, 513, 427],
    "Q8": ["qp", 10, 137, 205, 488, 530], "Q9": ["qp", 11, 190, 190, 383, 410], "Q10.1": ["qp", 12, 190, 147, 410, 317],
    "Q10.2": ["qp", 12, 140, 453, 483, 697], "Q11": ["qp", 13, 130, 180, 443, 397]}
INSET = {"Q1": 40, "Q2": 40}


def fig(name, caption):
    src, p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption,
            **({"source": "answer_book"} if src == "ab" else {}), **({"inset": INSET[name]} if name in INSET else {})}


def mcq(n, q, opts, a, clues, marks=1, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


term = lambda n, q, a, clues, marks=1, strict=False, reject=None: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a,
                                                                  **({"strict": True} if strict else {}), **({"reject": reject} if reject else {})}
num = lambda n, q, a, tol, unit, clues, marks=1, **kw: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol,
                                                        "unit": unit, **kw}
draw = lambda n, q, marks, criteria, clues, memo="", **kw: {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                           "criteria": [{"text": t, "marks": m} for t, m in criteria],
                                                           **({"memo": memo} if memo else {}), **kw}


ANS, WORK = "\n\nChoose the correct answer.", "\n\nChoose the correct working."
DP2 = 0.006   # a value keyed at two decimals
AUTHORED = []   # the typed calculations played as authored multiple choice (work), in paper order


def shape(o):
    """(lines, trailing [reasons]): every option of one part must match, so the layout never points at the answer."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


def work(n, q, marks, opts, a, clues, **kw):
    """A typed calculation as authored multiple choice (Murci, 2026-10-10): opts are the memo's FIRST working and three workings
    built from common errors, one step a line, a fraction {numerator}/{denominator}; the part keeps its marks, all or nothing."""
    assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
    assert len({shape(o) for o in opts}) == 1 and shape(opts[0])[0] >= 2, (n, [shape(o) for o in opts])
    assert 0 <= a <= 3, (n, a)
    AUTHORED.append(n)
    return mcq(n, q + WORK, opts, a, clues, marks=marks, **kw)

# ---- QUESTION 1, the question paper page 3 and the memo page 3 ----
q1 = [
    work("1.1", "Determine the equation of the least squares regression line for the data.", 3, [
        "a = 55,584360…\nb = −1,079146…\nŷ = 55,58 − 1,08x",          # the push-ups entered as x and the weights as y
        "a = 39,456001…\nb = −0,797945…\nŷ = 39,46 − 0,80x",          # r (−0,797945…) read off the screen as b
        "a = 39,456001…\nb = −0,590018…\nŷ = 39,46 − 0,59x",          # the memo (correct answer only: full marks)
        "a = 39,710937…\nb = −0,594769…\nŷ = 39,71 − 0,59x"], 2,      # 14 pairs: the last pair (31 ; 20) left out
        ["Put the weights in as x and the push-ups as y in your calculator's linear regression (STAT, A + BX) mode.",
         "The heavier players did fewer push-ups: which sign must b have?"]),
    num("1.2", "Write down the correlation coefficient.", -0.8, DP2, "",
        ["Find r on your calculator, with the same data as in 1.1.", "The points fall from left to right: which sign does r have?"]),
    work("1.3", "The coach uses the least squares regression line to set the target for the minimum number of push-ups by each team member "
         "according to their weight. Predict the number of push-ups that a member of the team, who weighs 29 kg, should do to meet the target.", 2, [
        "y = 39,46 − 0,59(29)\ny = 22,35",                # the memo (OR 22,35 on the calculator)
        "y = 39,46 − 0,8(29)\ny = 16,26",                 # r = −0,8 used as the gradient
        "y = (39,46 − 0,59)(29)\ny = 1 127,23",           # subtracts before it multiplies
        "y = 39 − 0,6(29)\ny = 21,6"], 0,                 # a and b rounded too early
        ["Substitute the weight into your equation from 1.1.", "x is the weight in kg."], after=["1.1"]),
    num("1.4", "Write down the mean number of push-ups for the given data.", 18.33, DP2, "push-ups",
        ["Use the y-values only.", "Your calculator gives ȳ in the same statistics mode."]),
    term("1.5", "The players trained hard during the season. At the end of the season, the coach reported that each player was able to do 5 more "
         "push-ups per minute than they did at the beginning of the season. How does the increase in the number of push-ups influence the "
         "standard deviation of the data?",
         ["No influence", "It has no influence", "The increase has no influence", "The standard deviation stays the same",
          "The standard deviation remains the same", "It stays the same", "It remains the same", "Stays the same", "Remains the same",
          "No change", "It does not change", "Does not change", "It will not change", "Unchanged", "It is unchanged", "No effect",
          "It has no effect", "The same"],
        ["The standard deviation measures how spread out the data is around the mean.", "Adding the same number to every value moves the "
                                                                                          "data: does it spread it out?"],
        reject=["It increases", "Increases", "It increases by 5", "It decreases", "Decreases", "An influence", "It has an influence",
                "It changes", "Changes"]),
    work("1.6", "At the beginning of the season, the coach used the least squares regression line as the minimum target for a player to aim "
         "for. Determine the maximum possible increase in the number of push-ups that a team member must obtain to reach the minimum target.", 2, [
        "Furthest point below the line: (40 ; 6)\nŷ = 39,46 − 0,59(40) = 15,86\nThe target at 40 kg: 15 push-ups\n"
        "Increase = 15 − 6 = 9 push-ups",                   # rounds 15,86 down: 15 push-ups miss the target
        "Furthest point below the line: (40 ; 6)\nȳ = 18,33\nThe target: 18 push-ups\nIncrease = 18 − 6 = 12 push-ups",   # the mean as the target
        "Furthest point below the line: (40 ; 6)\nŷ = 39,46 − 0,59(6) = 35,92\nThe target: 36 push-ups\n"
        "Increase = 36 − 6 = 30 push-ups",                  # the push-ups put in for x
        "Furthest point below the line: (40 ; 6)\nŷ = 39,46 − 0,59(40) = 15,86\nThe target at 40 kg: 16 push-ups\n"
        "Increase = 16 − 6 = 10 push-ups"], 3,              # the memo: 6 is furthest below; up to (40 ; 16), a difference of 10
        ["Find the point that lies furthest BELOW the regression line on the scatter plot.", "Read the line's value at that weight, in whole "
                                                                                             "push-ups."], after=["1.1", "1.4"]),
]

# ---- QUESTION 2, the question paper page 4 and the memo page 4 ----
q2 = [
    num("2.1", "Estimate the median travel time.", 65, 0.5, "minutes",
        ["The median is the middle value: half of the 60 employees.", "Go across from that cumulative frequency to the ogive, then down."]),
    num("2.2", "Estimate the lower quartile.", 44, 0.5, "minutes",
        ["The lower quartile is a quarter of the way through the data.", "A quarter of 60 employees: read the time at that cumulative "
                                                                          "frequency."]),
    work("2.3", "Estimate the interquartile range.", 2, [
        "Q₃ = 84\nIQR = 84 − 65\n= 19",              # the median taken away, not Q₁
        "Q₃ = 84\nIQR = 84 − 44\n= 40",              # the memo
        "Q₃ = 45\nIQR = 45 − 44\n= 1",               # the cumulative frequency 45 written as Q₃
        "Q₃ = 84\nIQR = 120 − 5\n= 115"], 1,         # the range, not the interquartile range
        ["Find the upper quartile the same way: three quarters of 60.", "IQR = Q₃ − Q₁."], after=["2.1", "2.2"]),
    draw("2.4", "The minimum and maximum times taken for an employee to travel to work are 5 and 120 minutes respectively. On the scaled line "
         "in the ANSWER BOOK, draw a box and whisker diagram to indicate the distribution of the data as represented in the ogive above.", 2, [
        ["Box: from the lower quartile (44) to the upper quartile (84), with the median (65) inside", 1],
        ["Whiskers ending at 5 and 120", 1]],
        ["You need five numbers: the minimum, Q₁, the median, Q₃ and the maximum.", "The box runs between the quartiles; the whiskers reach the "
                                                                                     "smallest and largest times."],
        memo="The answer book gives a scaled line from 0 to 120 minutes (labels every 10, ticks every 5). Five-number summary: 5 ; 44 ; 65 ; "
             "84 ; 120.", after=["2.1", "2.2", "2.3"],
        # built on the answer book's scaled line (2026-10-11), marked as the memo marks it: ✓ box (Q₁ 44, the median 65 and Q₃ 84 together)
        # and ✓ whiskers ending at 5 & 120 (both together). The quartiles are 2.1-2.3's ogive readings (65, 44, 84), so the line snaps to
        # every minute (44 and 84 sit between its 5-minute ticks); the minimum and maximum are the stem's
        build={"kind": "boxplot", "x": [0, 120, 1], "tick": 5, "label": 10, "tol": 0,
               "at": {"min": 5, "q1": 44, "med": 65, "q3": 84, "max": 120},
               "crit": {"q1": 0, "med": 0, "q3": 0, "min": 1, "max": 1}}),
    work("2.5", "The company manager decided that all employees who travel for an hour or more will be allowed to work from home for part of "
         "the day. What percentage of the employees will be allowed to work from home for part of the day?", 2, [
        "Number of employees who qualify = 34\n% of employees who qualify = {34}/{60} × 100\n= 56,67% of the employees",   # the memo (OR 35, 58,33%)
        "Number of employees who qualify = 26\n% of employees who qualify = {26}/{60} × 100\n= 43,33% of the employees",   # those UNDER an hour
        "Number of employees who qualify = 34\n% of employees who qualify = {34}/{65} × 100\n= 52,31% of the employees",   # the axis top, 65, as all
        "Number of employees who qualify = 3\n% of employees who qualify = {3}/{60} × 100\n= 5% of the employees"], 0,     # an hour read at 100 minutes
        ["Read the cumulative frequency at 60 minutes: that many travel for less than an hour.",
         "An hour or more: count the employees who are not included up to 60 minutes."]),
    work("2.6", "Employees work 8 hours in a normal working day. The manager decided on the following rule for time to work from home:\n"
         "• An employee is allowed to work half an hour from home for each time interval of 20 minutes, or part thereof, above an hour taken "
         "to travel to work.\nOn a certain day, an employee takes 110 minutes to travel to work. Calculate the number of minutes that this "
         "employee will be allowed to work from home on this day.", 2, [
        "Number of intervals = 2\nTime allowed to work from home = 2(30 minutes)\n= 60 minutes",      # the 10 minutes left over not counted
        "Number of intervals = 6\nTime allowed to work from home = 6(30 minutes)\n= 180 minutes",     # counts from 0 minutes, not above an hour
        "Number of intervals = 3\nTime allowed to work from home = 3(30 minutes)\n= 90 minutes",      # the memo (OR 1,5 hours)
        "Number of intervals = 2,5\nTime allowed to work from home = 2,5(30 minutes)\n= 75 minutes"], 2,   # a part interval counted as a half
        ["How many minutes above an hour is 110 minutes?", "Each interval earns half an hour: 30 minutes."]),
]
for i in q2:   # the built box and whisker diagram: every memo criterion is earned by its values, and each value sits on the line's steps
    b = i.get("build") or {}
    if b.get("kind") == "boxplot":
        assert sorted(set(b["crit"].values())) == list(range(len(i["criteria"]))), (i["n"], b["crit"])
        assert all(b["x"][0] <= u <= b["x"][1] and abs(u / b["x"][2] - round(u / b["x"][2])) < 1e-9 for u in b["at"].values()), (i["n"], b["at"])

# ---- QUESTION 3, the question paper page 5 and the memo pages 5-7 ----
q3 = [
    work("3.1", "Calculate the gradient of DC.", 2, [
        "m(DC) = {3 − (−9)}/{−9 − 0}\nm(DC) = −{4}/{3}",          # x over y: the formula upside down
        "m(DC) = {−9 − 0}/{3 − (−9)}\nm(DC) = −{3}/{4}",          # the memo
        "m(DC) = {−9 − 0}/{3 + (−9)}\nm(DC) = {3}/{2}",           # a sign slip: 3 − (−9) taken as 3 + (−9)
        "m(DC) = {−9 − 0}/{−9 − 3}\nm(DC) = {3}/{4}"], 1,         # D first on top, C first below
        ["m = (y₂ − y₁)/(x₂ − x₁) with D and C.", "Watch the signs when you subtract a negative coordinate."]),
    work("3.2", "Determine the equation of DC in the form y = mx + c.", 2, [
        "0 = −{3}/{4}(−9) + c\nc = {27}/{4}\ny = −{3}/{4}x + {27}/{4}",      # a sign slip taking 27/4 across
        "−9 = −{3}/{4}(0) + c\nc = −9\ny = −{3}/{4}x − 9",                   # C's coordinates swapped: (0 ; −9)
        "0 = −{4}/{3}(−9) + c\nc = −12\ny = −{4}/{3}x − 12",                 # the upside-down gradient −4/3
        "0 = −{3}/{4}(−9) + c\nc = −{27}/{4}\ny = −{3}/{4}x − {27}/{4}"], 3, # the memo (c = −27/4 or −6 3/4)
        ["You have the gradient from 3.1.", "Substitute C or D into y = mx + c to find c."], after=["3.1"]),
    mcq("3.3", "Show that k = −6." + WORK, [
        "k = −{3}/{4}(−1) − {27}/{4}\nk = −{3}/{4} − {27}/{4}\nk = −6",
        "−1 = −{3}/{4}k − {27}/{4}\n{3}/{4}k = −{23}/{4}\nk = −6",
        "k = −{3}/{4}(−1) − {27}/{4}\nk = {3}/{4} − {27}/{4}\nk = −6",
        "k = −6 gives B(−1 ; −6)\n−6 = −{3}/{4}(−1) − {27}/{4}\n−6 = −6, so k = −6"], 2,
        ["B lies on DC: its coordinates satisfy the equation from 3.2.", "Substitute B's x-coordinate: a 'show that' may not start from the value it must show."],
        after=["3.2"]),
    work("3.4", "Calculate the length of DC.", 2, [
        "DC = √((3 + 9)² + (−9 − 0)²)\nDC = 15 units",            # the memo
        "DC = √((3 − 9)² + (−9 − 0)²)\nDC = 10,82 units",         # a sign slip: 3 − (−9) taken as 3 − 9
        "DC = (3 + 9)² + (−9 − 0)²\nDC = 225 units",              # the square root left off
        "DC = √((3 + 9)² − (−9 − 0)²)\nDC = 7,94 units"], 0,      # the squares subtracted
        ["Use the distance formula with D and C.", "d = √((x₂ − x₁)² + (y₂ − y₁)²)."]),
    work("3.5", "Calculate the ratio of DB/DC.", 2, [
        "DB = (3 − (−1))² + (−9 − (−6))²\nDB = 25\n∴ {DB}/{DC} = {25}/{15} = {5}/{3}",            # the square root left off
        "DB = √((3 − 1)² + (−9 − (−6))²)\nDB = √13 = 3,61\n∴ {DB}/{DC} = {3,61}/{15} = 0,24",    # B's x taken as 1, not −1
        "DB = √((3 − (−1))² + (−9 − (−6))²)\nDB = 5\n∴ {DB}/{DC} = {5}/{15} = {1}/{3}",          # the memo
        "DB = √((3 − (−1))² + (−9 − (−6))²)\nDB = 5\n∴ {DB}/{DC} = {5²}/{15²} = {1}/{9}"], 2,    # squares the lengths (an area ratio)
        ["B is (−1 ; −6), from 3.3.", "Find DB with the distance formula, then divide by DC from 3.4."], after=["3.4"]),
    work("3.6", "If M is a point on AD such that AC ∥ MB, calculate the ratio of Area △MBD / Area △ACD.", 4, [
        "{DM}/{MA} = {DB}/{BC} = {1}/{2}\n{Area △MBD}/{Area △ACD} = {½(DM)(DB) sin D̂}/{½(MA)(BC) sin D̂}\n= {1}/{2} × {1}/{2}\n"
        "= {1}/{4}",                                                                               # the parts MA and BC, not the sides DA and DC
        "{DM}/{DA} = {DB}/{DC} = {1}/{3}\n{Area △MBD}/{Area △ACD} = {½(DA)(DC) sin D̂}/{½(DM)(DB) sin D̂}\n= 3 × 3\n= 9",   # upside down
        "{DM}/{DA} = {DB}/{DC} = {1}/{3}\n{Area △MBD}/{Area △ACD} = {½(DB) × h}/{½(DC) × h}\n= {5}/{15}\n= {1}/{3}",   # a common height they lack
        "{DM}/{DA} = {DB}/{DC} = {1}/{3}\n{Area △MBD}/{Area △ACD} = {½(DM)(DB) sin D̂}/{½(DA)(DC) sin D̂}\n= {1}/{3} × {1}/{3}\n"
        "= {1}/{9}"], 3,                                                                           # the memo
        ["MB is parallel to AC in △ACD: a line parallel to one side divides the other two sides in proportion.",
         "Both triangles share the angle D: area = ½ × side × side × sin D̂."], after=["3.5"]),
    work("3.7", "If it is further given that the gradient of AD is −4 and the length of AD is √612 units, calculate the coordinates of A.", 6, [
        "−9 = −4(3) + c\nc = 3, ∴ y = −4x + 3\n(x − 3)² + (y + 9)² = 612\n(x − 3)² + (−4x + 3 + 9)² = (√612)²\n17x² − 102x − 459 = 0\n"
        "x² − 6x − 27 = 0\n(x + 9)(x − 3) = 0\nx = −9 or x = 3 (N/A)\ny = −4(−9) + 3 = 39\nA(−9 ; 39)",       # the factors' signs swapped
        "−9 = −4(3) + c\nc = 3, ∴ y = −4x + 3\n(x − 3)² + (y + 9)² = 612\n(x − 3)² + (−4x + 3 + 9)² = (√612)²\n17x² − 102x − 459 = 0\n"
        "x² − 6x − 27 = 0\n(x − 9)(x + 3) = 0\nx = 9 (N/A) or x = −3\ny = −4(−3) + 3 = 15\nA(−3 ; 15)",       # the memo
        "−9 = −4(3) + c\nc = 3, ∴ y = −4x + 3\n(x − 3)² + (y + 9)² = 612\n(x − 3)² + (−4x + 3 + 9)² = (√612)²\n17x² − 102x − 459 = 0\n"
        "x² − 6x − 27 = 0\n(x − 9)(x + 3) = 0\nx = 9 or x = −3 (N/A)\ny = −4(9) + 3 = −33\nA(9 ; −33)",       # the wrong root rejected
        "−9 = 4(3) + c\nc = −21, ∴ y = 4x − 21\n(x − 3)² + (y + 9)² = 612\n(x − 3)² + (4x − 21 + 9)² = (√612)²\n17x² − 102x − 459 = 0\n"
        "x² − 6x − 27 = 0\n(x − 9)(x + 3) = 0\nx = 9 (N/A) or x = −3\ny = 4(−3) − 21 = −33\nA(−3 ; −33)"], 1,   # the gradient's sign lost
        ["Find the equation of AD from its gradient and D.", "A lies on AD at a distance √612 from D: solve the two together; A is in the "
                                                             "second quadrant."]),
]

# ---- QUESTION 4, the question paper page 6 and the memo pages 8-11 ----
q4 = [
    work("4.1", "Write down the coordinates of L.", 2, [   # the memo gives L(−1 ; −3) only: the working (the midpoint) is ours
        "M(1 ; 3) is the midpoint of PL\n{3 + x}/{2} = 1, ∴ x = −1\n{9 + y}/{2} = 3, ∴ y = −3\nL(−1 ; −3)",     # the memo's L
        "O(0 ; 0) is the midpoint of PL\n{3 + x}/{2} = 0, ∴ x = −3\n{9 + y}/{2} = 0, ∴ y = −9\nL(−3 ; −9)",     # O taken as the centre
        "M(1 ; 3) is the midpoint of PL\n{3 + x}/{2} = 1, ∴ x = −2\n{9 + y}/{2} = 3, ∴ y = −6\nL(−2 ; −6)",     # never multiplies by 2
        "M(1 ; 3) is the midpoint of PL\n{3 + x}/{2} = 1, ∴ x = −1\n{9 + y}/{2} = 3, ∴ y = 3\nL(−1 ; 3)"], 0,  # a sign slip: 6 − 9 = 3
        ["PL passes through the centre M: it is a diameter.", "M is the midpoint of PL."]),
    work("4.2", "Determine the equation of tangent ST to the circle at P.", 4, [
        "m(MP) = {9 − 3}/{3 − 1} = 3\nm(ST) = 3\n9 = 3(3) + c\nc = 0\ny = 3x",                                      # the radius's gradient kept
        "m(MP) = {9 − 3}/{3 − 1} = 3\nm(ST) = −3\n9 = −3(3) + c\nc = 18\ny = −3x + 18",                             # the sign changed, not inverted
        "m(MP) = {9 − 3}/{3 − 1} = 3\nm(ST) = {1}/{3}\n9 = {1}/{3}(3) + c\nc = 8\ny = {1}/{3}x + 8",                # inverted, the sign kept
        "m(MP) = {9 − 3}/{3 − 1} = 3\nm(ST) = −{1}/{3}\n9 = −{1}/{3}(3) + c\nc = 10\ny = −{1}/{3}x + 10"], 3,     # the memo
        ["A tangent is perpendicular to the radius at the point of contact.", "Then put P into y = mx + c."]),
    mcq("4.3", "Show that the equation of the circle with centre M is x² + y² − 2x − 6y − 30 = 0." + WORK, [
        "(x + 1)² + (y + 3)² = r²\n(3 + 1)² + (9 + 3)² = r²\nr² = 160\n(x + 1)² + (y + 3)² = 160\nx² + 2x + 1 + y² + 6y + 9 = 160\n"
        "x² + y² − 2x − 6y − 30 = 0",
        "(x − 1)² + (y − 3)² = r²\n(3 − 1)² + (9 − 3)² = r²\nr² = 40\n(x − 1)² + (y − 3)² = 40\nx² − 2x + 1 + y² − 6y + 9 = 40\n"
        "x² + y² − 2x − 6y − 30 = 0",
        "(x − 1)² + (y − 3)² = r²\n(3 − 1)² + (9 − 3)² = r²\nr² = 40\n(x − 1)² + (y − 3)² = 40\nx² − 1 + y² − 9 = 40\n"
        "x² + y² − 2x − 6y − 30 = 0",
        "(x − 1)² + (y − 3)² = r²\n(3 + 1)² + (9 + 3)² = r²\nr² = 160\n(x − 1)² + (y − 3)² = 160\nx² − 2x + 1 + y² − 6y + 9 = 160\n"
        "x² + y² − 2x − 6y − 30 = 0"], 1,
        ["The centre is M(1 ; 3) and P(3 ; 9) is on the circle: r = MP.", "Check each line: the signs in (x − a)², and each expansion."], marks=4),
    mcq("4.4", "Show that d = 7." + WORK, [
        "d = 7: (7)² + (1)² − 2(7) − 6(1) − 30\n= 49 + 1 − 14 − 6 − 30\n= 0\nR(7 ; 1) lies on the circle\n∴ d = 7",
        "d² + (1)² − 2d − 6(1) − 30 = 0\nd² − 2d − 35 = 0\n(d + 7)(d − 5) = 0\nd = −7 or d = 5\n∴ d = 7",
        "d² + (1)² − 2d − 6(1) − 30 = 0\nd² − 2d − 35 = 0\nd² − 2d = 35\nd(d − 2) = 35\n∴ d = 7",
        "d² + (1)² − 2d − 6(1) − 30 = 0\nd² − 2d − 35 = 0\n(d − 7)(d + 5) = 0\nd = 7 or d = −5\n∴ d = 7"], 3,
        ["R(d ; 1) is on the circle: substitute it into the equation from 4.3.", "A 'show that' may not start from the answer; d > 0."], marks=2),
    work("4.5", "Calculate the size of L̂.", 5, [
        "m(PO) = 3, ∴ tan PÔV = 3\nPÔV = 71,565…°\nm(RL) = {1 − (−3)}/{7 − (−1)} = {1}/{2}\ntan RV̂N = {1}/{2}, ∴ RV̂N = 26,565…°\n"
        "L̂ = 71,565…° + 26,565…° [ext ∠ of △]\nL̂ = 98,13°",                     # adds the angles
        "m(PO) = 3, ∴ tan PÔV = 3\nPÔV = 71,565…°\nm(RL) = {1 + 3}/{7 − 1} = {2}/{3}\ntan RV̂N = {2}/{3}, ∴ RV̂N = 33,690…°\n"
        "L̂ = 71,565…° − 33,690…° [ext ∠ of △]\nL̂ = 37,87°",                     # a sign slip: 7 − (−1) taken as 7 − 1
        "m(PO) = 3, ∴ tan PÔV = 3\nPÔV = 71,565…°\nm(RL) = {1 − (−3)}/{7 − (−1)} = {1}/{2}\ntan RV̂N = {1}/{2}, ∴ RV̂N = 26,565…°\n"
        "L̂ = 71,565…° − 26,565…° [ext ∠ of △]\nL̂ = 45°",                        # the memo
        "m(PO) = 3, ∴ tan PÔV = 3\nPÔV = 71,565…°\nm(RL) = {1 − (−3)}/{7 − (−1)} = {1}/{2}\ntan RV̂N = {1}/{2}, ∴ RV̂N = 26,565…°\n"
        "L̂ = 180° − 71,565…° − 26,565…° [sum of ∠s in △]\nL̂ = 81,87°"], 2,     # both taken as interior angles of △OVL
        ["The gradients of PL and RL give their angles of inclination with the x-axis.",
         "In △OVL, the angle at O's side is an exterior angle: use the exterior angle of a triangle."], after=["4.1"]),
    mcq("4.6", "TR is a tangent to the circle at R. Prove that PT ⊥ RT." + WORK, [
        "m(RM) = {1 − 3}/{7 − 1} = −{1}/{3}\nm(RT) = 3 [tan ⊥ rad]\nm(PT) = −{1}/{3}\nm(RT) × m(PT) = −1\n∴ PT ⊥ RT",
        "m(RM) = {1 − 3}/{7 − 1} = −{1}/{3}\nm(RT) = 3 [tan-chord theorem]\nm(PT) = −{1}/{3}\nm(RT) × m(PT) = −1\n∴ PT ⊥ RT",
        "m(RM) = {1 − 3}/{7 − 1} = {1}/{3}\nm(RT) = −3 [tan ⊥ rad]\nm(PT) = −{1}/{3}\nm(RT) × m(PT) = −1\n∴ PT ⊥ RT",
        "m(RM) = {1 − 3}/{7 − 1} = −{1}/{3}\nm(RT) = 3 [PT ⊥ RT]\nm(PT) = −{1}/{3}\nm(RT) × m(PT) = −1\n∴ PT ⊥ RT"], 0,
        ["RT is a tangent at R: it is perpendicular to the radius MR.", "PT lies on tangent ST (4.2); perpendicular gradients multiply to −1."],
        marks=3, after=["4.2"]),
]

# ---- QUESTION 5, the question paper page 7 and the memo pages 12-13 ----
q51 = [
    work("5.1.1", "cos A", 2, [
        "r = √((−3)² + (−4)²) = 5\ncos A = −{4}/{5}",          # y over r: that is sin A
        "r = √((−3)² + (−4)²) = 5\ncos A = −{3}/{5}",          # the memo
        "r = √((−3)² + (−4)²) = 5\ncos A = {3}/{5}",           # the sign lost: A ends in the third quadrant
        "r = (−3)² + (−4)² = 25\ncos A = −{3}/{25}"], 1,       # the square root left off
        ["Use Pythagoras with x = −3 and y = −4.", "P is in the third quadrant: which sign does cos A have there?"]),
    work("5.1.2", "cos 2A", 2, [
        "cos 2A = 2cos² A − 1\n= 2(−{3}/{5})² − 1\n= −{43}/{25}",     # (−3/5)² taken as −9/25
        "cos 2A = 2cos A\n= 2(−{3}/{5})\n= −{6}/{5}",                 # cos 2A taken as 2 cos A
        "cos 2A = 1 − 2cos² A\n= 1 − 2(−{3}/{5})²\n= {7}/{25}",       # cos in the 1 − 2sin² A form
        "cos 2A = 2cos² A − 1\n= 2(−{3}/{5})² − 1\n= −{7}/{25}"], 3,  # the memo
        ["Choose a double angle formula for cos 2A.", "Use your cos A from 5.1.1 (sin A = −4/5)."], after=["5.1.1"]),
    work("5.1.3", "sin(A − B), if it is further given that sin B = 4/5 and 90° < B < 360°", 4, [
        "x = −3\nsin(A − B) = sin A cos B − cos A sin B\n= (−{4}/{5})(−{3}/{5}) − (−{3}/{5})({4}/{5})\n= {12}/{25} + {12}/{25}\n= {24}/{25}",  # memo
        "x = 3\nsin(A − B) = sin A cos B − cos A sin B\n= (−{4}/{5})({3}/{5}) − (−{3}/{5})({4}/{5})\n= −{12}/{25} + {12}/{25}\n= 0",  # B in quad 1
        "x = −3\nsin(A − B) = sin A − sin B\n= (−{4}/{5}) − ({4}/{5})\n= −{4}/{5} − {4}/{5}\n= −{8}/{5}",       # sin shared out over A − B
        "x = −3\nsin(A − B) = cos A cos B − sin A sin B\n= (−{3}/{5})(−{3}/{5}) − (−{4}/{5})({4}/{5})\n= {9}/{25} + {16}/{25}\n= 1"], 0,  # cos(A+B)'s
        ["sin B is positive between 90° and 360° only in the second quadrant: draw B there.", "Expand sin(A − B) with the compound angle "
                                                                                            "formula."], after=["5.1.1"]),
]
q52 = [
    mcq("5.2", "If cos α = p, express the following expression in terms of p:\n(cos(α/2 − 45°).sin(α/2 − 45°))/2" + WORK, [
        "{cos(α/2 − 45°).sin(α/2 − 45°)}/{2}\n= {2 cos(α/2 − 45°).sin(α/2 − 45°)}/{2.2}\n= {sin(α − 90°)}/{4}\n= {cos α}/{4}\n= {p}/{4}",
        "{cos(α/2 − 45°).sin(α/2 − 45°)}/{2}\n= {sin 2(α/2 − 45°)}/{2}\n= {sin(α − 90°)}/{2}\n= {−cos α}/{2}\n= {−p}/{2}",
        "{cos(α/2 − 45°).sin(α/2 − 45°)}/{2}\n= {2 cos(α/2 − 45°).sin(α/2 − 45°)}/{2.2}\n= {sin(α − 90°)}/{4}\n= {−cos α}/{4}\n= {−p}/{4}",
        "{cos(α/2 − 45°).sin(α/2 − 45°)}/{2}\n= {2 cos(α/2 − 45°).sin(α/2 − 45°)}/{2.2}\n= {sin(α − 45°)}/{4}\n= {−cos α}/{4}\n= {−p}/{4}"], 2,
        ["2 sin θ cos θ = sin 2θ: multiply the numerator and the denominator by 2.", "Then write sin(α − 90°) in terms of cos α: which sign does it take?"],
        marks=4),
]

# ---- QUESTION 6, the question paper page 8 and the memo pages 14-15 ----
N6, D6 = "cos(90° − x)cos y + sin(−y)cos(180° + x)", "cos x cos(360° + y) + sin(360° − x)sin y"
q61 = [
    mcq("6.1.1", "Use the compound angle identity given above to derive a formula for cos(x + y)." + WORK, [
        "cos(x + y) = cos(x − (−y))\n= cos x cos(−y) + sin x sin(−y)\n= cos x cos y + sin x sin y",
        "cos(x + y) = cos(x − (−y))\n= cos x cos(−y) + sin x sin(−y)\n= cos x cos y − sin x sin y",
        "cos(x + y) = cos(x − (−y))\n= cos x cos(−y) + sin x sin(−y)\n= −cos x cos y − sin x sin y",
        "cos(x + y) = −cos(x − y)\n= −(cos x cos y + sin x sin y)\n= cos x cos y − sin x sin y"], 1,
        ["Write x + y as x − (−y), then use the identity given.", "Which of cos(−y) and sin(−y) changes sign?"], marks=2),
    mcq("6.1.2", "Hence, or otherwise, show that:\n(" + N6 + ")/(" + D6 + ") = tan(x + y)" + WORK, [
        "LHS = {" + N6 + "}/{" + D6 + "}\n= {(sin x)cos y + (−sin y)(cos x)}/{cos x(cos y) + (−sin x)sin y}\n"
        "= {sin x cos y − cos x sin y}/{cos x cos y − sin x sin y}\n= {sin(x + y)}/{cos(x + y)}\n= tan(x + y)\n= RHS",
        "LHS = {" + N6 + "}/{" + D6 + "}\n= {(sin x)cos y + (−sin y)(−cos x)}/{cos x(cos y) + (sin x)sin y}\n"
        "= {sin x cos y + cos x sin y}/{cos x cos y + sin x sin y}\n= {sin(x + y)}/{cos(x + y)}\n= tan(x + y)\n= RHS",
        "LHS = {" + N6 + "}/{" + D6 + "}\n= {(cos x)cos y + (−sin y)(−cos x)}/{cos x(cos y) + (−sin x)sin y}\n"
        "= {cos x cos y + cos x sin y}/{cos x cos y − sin x sin y}\n= {sin(x + y)}/{cos(x + y)}\n= tan(x + y)\n= RHS",
        "LHS = {" + N6 + "}/{" + D6 + "}\n= {(sin x)cos y + (−sin y)(−cos x)}/{cos x(cos y) + (−sin x)sin y}\n"
        "= {sin x cos y + cos x sin y}/{cos x cos y − sin x sin y}\n= {sin(x + y)}/{cos(x + y)}\n= tan(x + y)\n= RHS"], 3,
        ["Reduce each angle first: cos(90° − x), sin(−y), cos(180° + x), cos(360° + y), sin(360° − x).",
         "The numerator and the denominator are then compound angle expansions."], marks=6, after=["6.1.1"]),
]
q62 = [
    work("6.2", "Given: f(x) = √(6 sin² x − 11 cos(90° + x) + 7)\nSolve for x in the interval x ∈ (0° ; 360°) if f(x) = 2.", 6, [
        "√(6 sin² x − 11 cos(90° + x) + 7) = 2\n6 sin² x − 11 cos(90° + x) + 7 = 4\n6 sin² x − 11(sin x) + 7 = 4\n6 sin² x − 11 sin x + 3 = 0\n"
        "(3 sin x − 1)(2 sin x − 3) = 0\nsin x = {1}/{3} or sin x = {3}/{2} (no solution)\nref ∠ = 19,47°\nx = 19,47° or x = 160,53°",
        # cos(90° + x) taken as + sin x
        "√(6 sin² x − 11 cos(90° + x) + 7) = 2\n6 sin² x − 11 cos(90° + x) + 7 = 2\n6 sin² x − 11(−sin x) + 7 = 2\n6 sin² x + 11 sin x + 5 = 0\n"
        "(6 sin x + 5)(sin x + 1) = 0\nsin x = −{5}/{6} or sin x = −1\nref ∠ = 56,44°\nx = 236,44° ; 270° or 303,56°",
        # the root dropped without squaring the 2
        "√(6 sin² x − 11 cos(90° + x) + 7) = 2\n6 sin² x − 11 cos(90° + x) + 7 = 4\n6 sin² x − 11(−sin x) + 7 = 4\n6 sin² x + 11 sin x + 3 = 0\n"
        "(3 sin x + 1)(2 sin x + 3) = 0\nsin x = −{1}/{3} or sin x = −{3}/{2} (no solution)\nref ∠ = 19,47°\nx = 199,47° or x = 340,53°",
        # the memo
        "√(6 sin² x − 11 cos(90° + x) + 7) = 2\n6 sin² x − 11 cos(90° + x) + 7 = 4\n6 sin² x − 11(−sin x) + 7 = 4\n6 sin² x + 11 sin x + 3 = 0\n"
        "(3 sin x + 1)(2 sin x + 3) = 0\nsin x = −{1}/{3} or sin x = −{3}/{2} (no solution)\nref ∠ = 19,47°\nx = 160,53° or x = 199,47°"], 2,
        # the second and third quadrants, not the third and fourth
        ["Square both sides, then reduce cos(90° + x).", "Factorise the quadratic in sin x: one of the two factors gives no solution."]),
]
q63 = [
    work("6.3.1", "Calculate the maximum value of g.", 3, [
        "g(x) = {4(1 − 2sin² x)}/{3}\n= {4 cos 2x}/{3}\nMaximum value of cos 2x is 1\n∴ maximum value of g(x) = 4",              # the ÷ 3 dropped
        "g(x) = {4(1 − 2sin² x)}/{3}\n= {4 cos 2x}/{3}\nMaximum value of cos 2x is 1\n∴ maximum value of g(x) = {4}/{3}",        # the memo
        "g(x) = {4(1 − 2sin² x)}/{3}\n= {4 cos 2x}/{3}\nMaximum value of cos 2x is 2\n∴ maximum value of g(x) = {8}/{3}",        # the 2 in 2x as the amplitude
        "g(x) = {4(1 − 2sin² x)}/{3}\n= {4 cos 2x}/{3}\ng is a maximum when sin² x = 1, cos 2x = −1\n∴ maximum value of g(x) = −{4}/{3}"], 1,
        # the LARGEST sin² x taken
        ["Take out the common factor 4: 1 − 2sin² x is a double angle.", "Or: g is largest when sin² x is smallest."]),
    num("6.3.2", "Write down the smallest possible value of x for which g will have a maximum value in the interval x ∈ (0° ; 360°].", 180, 0, "°",
        ["g is a maximum where sin x = 0 (cos 2x = 1).", "The interval leaves out 0°."], after=["6.3.1"]),
]

# ---- QUESTION 7, the question paper page 9 and the memo page 16 ----
F7 = ("The graph of f(x) = tan x for x from −180° to 180°, with y marked from −3 to 3: dashed asymptotes at x = −90° and x = 90°; f passes "
      "through (−180° ; 0), (0 ; 0) and (180° ; 0), each of its three branches rising from left to right.")
q7 = [
    num("7.1", "Write down the equation of the asymptote of f in the interval x ∈ [0° ; 180°].", 90, 0, "°",
        ["An asymptote of tan x is a vertical dashed line.", "Find the one between 0° and 180°."]),
    mcq("7.2", "Write down the values of x in the interval x ∈ [−180° ; 0°] for which f(x) ≤ 0." + ANS, [
        "x = −180° or −90° < x ≤ 0°", "−90° < x ≤ 0°", "x = −180° or −90° ≤ x ≤ 0°", "−180° ≤ x < −90°"], 0,
        ["Look for where the graph is on or below the x-axis between −180° and 0°.", "Check each end point of your interval on the graph."],
        marks=2, figure=fig("Q7", F7)),
    num("7.3.1", "Given: g(x) = cos 2x + 1\nWrite down the period of g.", 180, 0, "°",
        ["The period is the length of one full wave.", "cos 2x repeats twice as fast as cos x."]),
    draw("7.3.2", "Given: g(x) = cos 2x + 1\nOn the grid given in the ANSWER BOOK, draw the graph of g(x) = cos 2x + 1 for the interval "
         "x ∈ [−180° ; 180°]. Clearly show the intercepts with the axes as well as the coordinates of the turning points.", 3, [
        ["Turning points on the x-axis: x = −90° ; 90°", 1], ["Shape", 1], ["Turning point on the y-axis at (0 ; 2)", 1]],
        ["cos 2x has period 180° and lies between −1 and 1.", "The + 1 lifts the whole graph one unit up."],
        memo="The answer book's grid repeats the paper's graph of f(x) = tan x. g runs from (−180° ; 2) down to (−90° ; 0), up to (0 ; 2), "
             "down to (90° ; 0) and up to (180° ; 2).", after=["7.3.1"],
        # built on a grid (2026-10-11, as transcribe_g11_math_p2_2017_11.py 6.2.3): the answer book's axes (x from −180° to 180°, y from
        # −3 to 3; f itself is not drawn), x on 15° steps. The memo's three turning points are three features with ONE name, matched as a
        # set: criterion 0 the two on the x-axis (one carries its mark), criterion 2 the one on the y-axis; they are also the intercepts
        # the stem asks for, so no intercept is placed twice. The shape (criterion 1) is the cosine the learner's own points fix
        build={"kind": "sketch", "family": "cos", "b": 2, "x": [-180, 180, 15], "y": [-3, 3, 0.5], "domain": [-180, 180], "features": [
            {"id": "t1", "kind": "point", "label": "turning point", "at": [-90, 0], "tol": 0, "marks": 1, "crit": 0, "turn": True},
            {"id": "t2", "kind": "point", "label": "turning point", "at": [90, 0], "tol": 0, "marks": 0, "crit": 0, "turn": True},
            {"id": "t3", "kind": "point", "label": "turning point", "at": [0, 2], "tol": 0, "marks": 1, "crit": 2, "turn": True}],
               "shape": {"label": "Shape", "answer": "drawn", "marks": 1, "crit": 1}}),
    mcq("7.4", "Use the graphs to determine the general solution of 2cos³ x − sin x = 0." + WORK, [
        "2cos³ x − sin x = 0\n2cos³ x = sin x\n2cos² x = {sin x}/{cos x}\n2cos² x = tan x\n2cos² x − 1 = tan x − 1\ncos 2x + 1 = tan x\n"
        "x = 45° + k.360° ; k ∈ Z",
        "2cos³ x − sin x = 0\n2cos³ x = sin x\n2cos² x = {sin x}/{cos x}\n2cos² x = tan x\n2cos² x − 1 = tan x − 1\ncos 2x + 1 = tan x\n"
        "x = 45° + k.180° ; k ∈ Z",
        "2cos³ x − sin x = 0\n2cos³ x = sin x\n2cos² x = {sin x}/{cos x}\n2cos² x = tan x\n2cos² x − 1 = tan x\ncos 2x = tan x\n"
        "x = 45° + k.180° ; k ∈ Z",
        "2cos³ x − sin x = 0\n2cos³ x = sin x\n2cos² x = {cos x}/{sin x}\n2cos² x = tan x\n2cos² x − 1 = tan x − 1\ncos 2x + 1 = tan x\n"
        "x = 45° + k.180° ; k ∈ Z"], 1,
        ["Divide by cos x to bring in tan x, then make the left side cos 2x + 1.", "Where do the graphs of g and f meet on the grid?"], marks=4),
]
for i in q7:   # the built sketch: its features' and shape's marks are the memo criteria's, criterion by criterion
    if (i.get("build") or {}).get("kind") == "sketch":
        got = {}
        for x in i["build"]["features"] + [i["build"]["shape"]]:
            got[x["crit"]] = got.get(x["crit"], 0) + x["marks"]
        assert got == {k: c["marks"] for k, c in enumerate(i["criteria"])}, (i["n"], got)

# ---- QUESTION 8, the question paper page 10 and the memo pages 17-18 ----
q8 = [
    work("8.1", "Calculate the length of AC, the distance between the observer at A and the foot of the building.", 2, [
        "tan DÂC = {AC}/{DC}\nAC = 16 tan 46,85°\nAC = 17,07 m",            # tan as adjacent over opposite
        "sin DÂC = {DC}/{AC}\nAC = {16}/{sin 46,85°}\nAC = 21,93 m",        # AC taken as the hypotenuse
        "tan DÂC = {DC}/{AC}\nAC = {19}/{tan 46,85°}\nAC = 17,81 m",        # AB's 19 m read as the height
        "tan DÂC = {DC}/{AC}\nAC = {16}/{tan 46,85°}\nAC = 15 m"], 3,       # the memo
        ["△ACD has a right angle at C.", "Which trig ratio links the side opposite the 46,85° angle with the side next to it?"]),
    work("8.2", "Calculate how far the painter at E is from the top of the building.", 7, [
        "(AB)² = (BC)² + (AC)² − 2(BC)(AC) cos BĈA\n(19)² = x² + (15)² − 2x(15) cos 105,61°\nx² + 8,07x − 136 = 0\n"
        "x = {−8,07 ± √((8,07)² − 4(1)(−136))}/{2(1)}\nx = 8,30 m or x ≠ −16,38 m\nBÊC = 58°\ntan BÊC = {BC}/{EC}, ∴ EC = {8,3}/{tan 58°}\n"
        "EC = 5,19 m\nDE = 16 − 5,19 = 10,81 m",                                                       # the memo (cosine rule, BÊC)
        "(AB)² = (BC)² + (AC)² − 2(BC)(AC) cos BĈA\n(19)² = x² + (15)² + 2x(15) cos 105,61°\nx² − 8,07x − 136 = 0\n"
        "x = {8,07 ± √((−8,07)² − 4(1)(−136))}/{2(1)}\nx = 16,38 m or x ≠ −8,30 m\nBÊC = 58°\ntan BÊC = {BC}/{EC}, ∴ EC = {16,38}/{tan 58°}\n"
        "EC = 10,24 m\nDE = 16 − 10,24 = 5,76 m",                                                      # a sign slip in the cosine rule
        "(AB)² = (BC)² + (AC)² − 2(BC)(AC) cos BĈA\n(19)² = x² + (15)² − 2x(15) cos 105,61°\nx² + 8,07x − 136 = 0\n"
        "x = {−8,07 ± √((8,07)² − 4(1)(−136))}/{2(1)}\nx = 8,30 m or x ≠ −16,38 m\nBÊC = 58°\ntan BÊC = {EC}/{BC}, ∴ EC = 8,3 tan 58°\n"
        "EC = 13,28 m\nDE = 16 − 13,28 = 2,72 m",                                                      # tan upside down in △BCE
        "(AB)² = (BC)² + (AC)² − 2(BC)(AC) cos BĈA\n(19)² = x² + (15)² − 2x(15) cos 105,61°\nx² + 8,07x − 136 = 0\n"
        "x = {−8,07 ± √((8,07)² − 4(1)(−136))}/{2(1)}\nx = 8,30 m or x ≠ −16,38 m\nBÊC = 58°\ntan BÊC = {BC}/{EC}, ∴ EC = {8,3}/{tan 58°}\n"
        "EC = 5,19 m\nDistance from the top = EC = 5,19 m"], 0,                                        # EC, the distance from the FOOT
        ["In △ABC you know AB, AC and the angle C: the cosine rule gives a quadratic in BC.",
         "BÊC is on a straight line with DÊB; then use △BCE (right-angled at C) for EC, and DE = DC − EC."], after=["8.1"]),
]

# ---- QUESTION 9, the question paper page 11 and the memo page 19 ----
q9 = [
    work("9.1", "Calculate, with a reason, the value of Â₁.", 2, [
        "Â₁ = Ĉ₁ [ext ∠ of a cyclic quad]\n∴ Â₁ = 86°",                           # Â₂ left out of the opposite angle DÂB
        "Â₁ + 46° + 86° = 180° [opp ∠s of cyclic quad]\n∴ Â₁ = 48°",              # Ĉ₁ taken as the opposite interior angle
        "Â₁ + 46° = 86° [ext ∠ of a cyclic quad]\n∴ Â₁ = 40°",                   # the memo: Â₁ = 40° [ext ∠ of a cyclic quad]
        "Â₁ + 46° = 86° [ext ∠ of △]\n∴ Â₁ = 40°"], 2,                           # the right sum, the wrong reason (the R mark)
        ["Ĉ₁ lies outside ABCD, on the produced side BCE.", "Which angle of ABCD is opposite BĈD? Â₂ is part of it."]),
    mcq("9.2", "Hence, prove that AD = DC." + WORK, [
        "B̂ = 80° [Â₁ = ½B̂]\nD̂ = 100° [opp ∠s of cyclic quad]\n∴ Ĉ₂ = 40° [∠s opp equal sides]\n∴ Ĉ₂ = Â₁ = 40°\n∴ AD = DC [sides opp = ∠s]",
        "B̂ = 80° [Â₁ = ½B̂]\nD̂ = 100° [ext ∠ of cyclic quad]\n∴ Ĉ₂ = 40° [sum of ∠s in △]\n∴ Ĉ₂ = Â₁ = 40°\n∴ AD = DC [sides opp = ∠s]",
        "B̂ = 80° [Â₁ = ½B̂]\nD̂ = 100° [opp ∠s of cyclic quad]\n∴ Ĉ₂ = 40° [sum of ∠s in △]\n∴ Ĉ₂ = Â₁ = 40°\n∴ AD = DC [sides opp = ∠s]",
        "B̂ = 80° [Â₁ = ½B̂]\nD̂ = 100° [opp ∠s of cyclic quad]\n∴ Ĉ₂ = 40° [sum of ∠s in △]\n∴ Ĉ₂ = Â₁ = 40°\n∴ AD = DC [∠s opp equal sides]"], 2,
        ["Find B̂ from Â₁ = ½B̂, then D̂ in the cyclic quadrilateral.", "Show that the two angles of △ADC opposite AD and DC are equal."],
        marks=4, after=["9.1"]),
]

# ---- QUESTION 10, the question paper page 12 and the memo pages 20-22 ----
CON = "Construction: join SB and TA; draw h₁ from B ⊥ AR and h₂ from A ⊥ RB"
R1, R2 = "{area △RAB}/{area △ASB} = {½RA × h₁}/{½AS × h₁} = {RA}/{AS}", "{area △RAB}/{area △ABT} = {½RB × h₂}/{½BT × h₂} = {RB}/{BT}"
R1x, R2x = "{area △RAB}/{area △ASB} = {½RA × h₂}/{½AS × h₂} = {RA}/{AS}", "{area △RAB}/{area △ABT} = {½RB × h₁}/{½BT × h₁} = {RB}/{BT}"
END = "∴ {area △RAB}/{area △ASB} = {area △RAB}/{area △ABT}\n∴ {RA}/{AS} = {RB}/{BT}"
COM = "area △RAB = area △RAB [common]"
q101 = [
    mcq("10.1", "Prove the theorem which states that a line drawn parallel to one side of a triangle divides the other two sides proportionally, "
        "i.e. RA/AS = RB/BT" + WORK, [
        "\n".join([CON, R1, R2, COM, "but area △ASB = area △ABT [prop theorem; AB ∥ ST]", END]),
        "\n".join([CON, R1x, R2x, COM, "but area △ASB = area △ABT [same base & height; AB ∥ ST]", END]),
        "\n".join([CON, R1, R2, COM, "but area △ASB = area △ABT [same base & height; AS ∥ BT]", END]),
        "\n".join([CON, R1, R2, COM, "but area △ASB = area △ABT [same base & height; AB ∥ ST]", END])], 3,
        ["Compare triangles that share a height: their areas are in the ratio of their bases.",
         "△ASB and △ABT stand on the same base AB between the parallel lines AB and ST."], marks=6),
]
q102 = [
    mcq("10.2.1", "Prove, with reasons, that OR : WS = 1 : 2" + WORK, [
        "PR = RS [line from centre ⊥ to chord]\nPO = OW [radii]\n∴ OR = {1}/{2}WS [midpt theorem]\n∴ OR : WS = 1 : 2",
        "PR = RS [line from centre to midpt of chord]\nPO = OW [radii]\n∴ OR = {1}/{2}WS [midpt theorem]\n∴ OR : WS = 1 : 2",
        "PR = RS [line from centre ⊥ to chord]\nPO = OW [radii]\n∴ OR = {1}/{2}WS [prop theorem; OR ∥ WS]\n∴ OR : WS = 1 : 2",
        "PR = RS [midpt theorem]\nPO = OW [radii]\n∴ OR = {1}/{2}WS [line from centre ⊥ to chord]\n∴ OR : WS = 1 : 2"], 0,
        ["OR is drawn from the centre perpendicular to the chord PS: what does it do to PS?", "R and O are then midpoints of two sides of △PSW."],
        marks=5),
    work("10.2.2", "Calculate the length of PT if ST = 15 units.", 4, [
        "{OV}/{OT} = {RS}/{ST} = {1}/{4} [prop theorem; RO ∥ SW]\n{RS}/{15} = {1}/{4}\nRS = 3,75 units\n"
        "PR = RS = 3,75 units [line from centre ⊥ to chord]\n∴ PT = 22,5 units",                     # OT paired with ST, not VT
        "{OV}/{VT} = {RS}/{ST} = {1}/{3} [prop theorem; RO ∥ SW]\n{RS}/{15} = {1}/{3}\nRS = 5 units\n"
        "PR = RS = 5 units [line from centre ⊥ to chord]\n∴ PT = 25 units",                          # the memo
        "{OV}/{VT} = {ST}/{RS} = {1}/{3} [prop theorem; RO ∥ SW]\n{15}/{RS} = {1}/{3}\nRS = 45 units\n"
        "PR = RS = 45 units [line from centre ⊥ to chord]\n∴ PT = 105 units",                        # the ratio upside down
        "{OV}/{VT} = {RS}/{ST} = {1}/{3} [prop theorem; RO ∥ SW]\n{RS}/{15} = {1}/{3}\nRS = 5 units\n"
        "PR = RS = 5 units [line from centre ⊥ to chord]\n∴ PT = 20 units"], 1,                      # PR left out of PT
        ["OV : OT = 1 : 4, so OV : VT = 1 : 3; in △ORT, VS is parallel to OR.", "PT = PR + RS + ST."], after=["10.2.1"]),
]

# ---- QUESTION 11, the question paper page 13 and the memo pages 23-25 ----
GF0, GF1, GF2 = "{GF}/{BC} = {AF}/{AC} [△AGF ||| △ABC]", "{GF}/{BC} = {AC}/{AF} [△AGF ||| △ABC]", "∴ GF = {BC.AF}/{AC}"
SIM, SIMx = "△ACD ||| △FGC [∠∠∠]", "△ACD ||| △FGC [prop theorem; DC ∥ FG]"
MID = "∴ {AC}/{GF} = {AD}/{FC}\n∴ AC = {AD.FG}/{FC}\n∴ GF = BC.AF ÷ {AD.FG}/{FC}"
INV, INVx, LAST = "GF = BC.AF × {FC}/{AD.FG}", "GF = BC.AF × {AD.FG}/{FC}", "∴ GF² = {BC.FC.AF}/{AD}"
q11 = [
    mcq("11.1", "If EÂG = x, determine with reasons, FOUR other angles that are equal to x." + WORK, [
        "D̂₁ = EÂG = x [∠s in the same seg]\nĈ₁ = D̂₁ = x [tan-chord theorem]\nĈ₄ = Ĉ₁ = x [vert opp ∠s =]\nAF̂G = EÂG = x [tan-chord theorem]",
        "D̂₁ = EÂG = x [tan-chord theorem]\nĈ₁ = D̂₁ = x [tan-chord theorem]\nĈ₄ = Ĉ₁ = x [vert opp ∠s =]\nAF̂G = EÂG = x [tan-chord theorem]",
        "D̂₁ = EÂG = x [tan-chord theorem]\nĈ₃ = D̂₁ = x [tan-chord theorem]\nĈ₄ = Ĉ₁ = x [vert opp ∠s =]\nAF̂G = EÂG = x [tan-chord theorem]",
        "D̂₁ = EÂG = x [tan-chord theorem]\nĈ₁ = D̂₁ = x [tan-chord theorem]\nĈ₄ = Ĉ₁ = x [vert opp ∠s =]\nAĜF = EÂG = x [tan-chord theorem]"], 1,
        ["EA is a tangent to BOTH circles at A, and EF is a tangent to the smaller circle at C.",
         "The angle between a tangent and a chord equals the angle in the alternate segment."], marks=6),
    mcq("11.2", "Prove that AG.AD = AC.AF" + WORK, [
        "D̂₁ = AF̂G = x\n∴ DC ∥ FG [corresp ∠s; DC ∥ FG]\n{AG}/{AC} = {AF}/{AD} [prop theorem; DC ∥ FG]\n∴ AG.AD = AC.AF",
        "D̂₁ = AF̂G = x\n∴ DC ∥ FG [corresp ∠s =]\n{AG}/{AC} = {AD}/{AF} [prop theorem; DC ∥ FG]\n∴ AG.AD = AC.AF",
        "D̂₁ = AF̂G = x\n∴ DC ∥ FG [alt ∠s =]\n{AG}/{AC} = {AF}/{AD} [prop theorem; DC ∥ FG]\n∴ AG.AD = AC.AF",
        "D̂₁ = AF̂G = x\n∴ DC ∥ FG [corresp ∠s =]\n{AG}/{AC} = {AF}/{AD} [prop theorem; DC ∥ FG]\n∴ AG.AD = AC.AF"], 3,
        ["From 11.1, D̂₁ and AF̂G are equal: what does that make DC and FG?", "Then a line parallel to one side of △AGF divides the other sides "
                                                                              "in proportion."], marks=4, after=["11.1"]),
    mcq("11.3", "Prove that △AGF ||| △ABC" + WORK, [
        "In △AGF and △ABC\nĜ = B̂₂ [∠s in the same seg]\nAF̂G = Ĉ₁ = x [proved in 11.1]\nÂ₃ = Â₂ [sum of ∠s in △]\n△AGF ||| △ABC [∠∠∠]",
        "In △AGF and △ABC\nĜ = B̂₂ [tan-chord theorem]\nAF̂G = Ĉ₁ = x [proved in 11.1]\nÂ₃ = Â₂ [sum of ∠s in △]\n△AGF ||| △ABC [∠∠∠]",
        "In △AGF and △ABC\nĜ = B̂₂ [∠s in the same seg]\nAF̂G = Ĉ₄ = x [proved in 11.1]\nÂ₃ = Â₂ [sum of ∠s in △]\n△AGF ||| △ABC [∠∠∠]",
        "In △AGF and △ABC\nĜ = B̂₂ [∠s in the same seg]\nAF̂G = Ĉ₁ = x [proved in 11.1]\nÂ₃ = Â₂ [sum of ∠s in △]\n△AGF ||| △ABC [sides in prop]"], 0,
        ["Ĝ and B̂₂ both stand on the chord AF of the larger circle.", "Use an angle equal to x from 11.1 that lies inside △ABC."], marks=4,
        after=["11.1"]),
    mcq("11.4", "Prove that GF² = (BC.FC.AF)/AD" + WORK, [
        "\n".join([GF1, GF2, SIM, MID, INV, LAST]),
        "\n".join([GF0, GF2, SIMx, MID, INV, LAST]),
        "\n".join([GF0, GF2, SIM, MID, INV, LAST]),
        "\n".join([GF0, GF2, SIM, MID, INVx, LAST])], 2,
        ["From 11.3, write GF in terms of BC, AF and AC.", "Find a second pair of similar triangles that gives AC in terms of AD, FG and FC, "
                                                            "then substitute."], marks=6),
]

PUSH = {"head": ["Weight (in kg) (x)", "Number of push-ups per minute (y)"],
        "rows": [[a, b] for a, b in zip("34 32 40 27 33 28 27 55 39 44 30 57 28 32 31".split(), "26 21 6 20 16 26 23 7 18 14 17 8 28 25 20".split())]}
REASONS = "Provide reasons for your statements in QUESTIONS 9, 10 and 11."
missions = [
    {"id": "1", "title": "Question 1", "kind": "Regression and correlation", "marks": 10,
     "lead": "At the beginning of a season, the coach of a junior boys' rugby team recorded the weight (in kg) of the 15 players in his team "
             "and the number of push-ups that each player was able to do in one minute. The data is represented in the table and scatter "
             "plot below. The least squares regression line for the data is drawn.", "table": PUSH,
     "figure": fig("Q1", "A scatter plot: weight (in kg) from 0 to 60 across, push-ups per minute from 0 to 30 up. The 15 players' points from "
                   "the table, most of them between 27 and 34 kg, and the least squares regression line falling from left to right through "
                   "them, from about 27 kg to about 57 kg."), "items": q1},
    {"id": "2", "title": "Question 2", "kind": "Ogive and box and whisker", "marks": 10,
     "lead": "The cumulative frequency graph (ogive) shows the time taken (in minutes) for 60 employees to travel to work each morning.",
     "figure": fig("Q2", "An ogive: time (in minutes) from 0 to 140 across, cumulative frequency from 0 to 65 up, on a fine grid. The curve has "
                   "plotted points at 0, 20, 40, 60, 80, 100 and 120 minutes: it starts at (0 ; 0), rises slowly at first, most steeply "
                   "between 60 and 100 minutes, and levels off at 60 employees at 120 minutes."), "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Lines and a triangle", "marks": 19,
     "lead": "In the diagram below, △ACD has vertices A, D(3 ; −9) and C(−9 ; 0), where A is a point in the second quadrant. B(−1 ; k) lies "
             "on side DC.",
     "figure": fig("Q3", "Axes with origin O. Triangle ACD: A high up in the second quadrant, C(−9 ; 0) on the negative x-axis and D(3 ; −9) "
                   "in the fourth quadrant. Side AD crosses the x-axis just right of O. B(−1 ; k) is marked on side DC, just left of the "
                   "y-axis."), "items": q3},
    {"id": "4", "title": "Question 4", "kind": "The circle and its tangents", "marks": 20,
     "lead": "In the diagram, M(1 ; 3) is the centre of the circle. The circle cuts the x-axis at N. ST is a tangent to the circle at P(3 ; 9). "
             "R(d ; 1), with d > 0, and L lie on the circle. O and V are the x-intercepts of PL and RL respectively.",
     "figure": fig("Q4", "Axes with origin O. A circle with centre M(1 ; 3) through P(3 ; 9) at the top, R(d ; 1) on the right just above the "
                   "x-axis, N where it cuts the positive x-axis, and L below the x-axis on the left. The tangent ST touches the circle at P, "
                   "S on the y-axis and T to the right. Chord PL passes through M and O; chord PR is drawn; chord RL cuts the x-axis at V, "
                   "between O and N."), "items": q4},
    {"id": "5.1", "title": "Question 5.1", "kind": "Ratios from a point", "marks": 8,
     "lead": "In the diagram, line OP is given with P(−3 ; −4). KÔP = A.\nDetermine, without using a calculator, the value of:",
     "figure": fig("Q5", "Axes with origin O and the point K on the positive x-axis. The line OP runs into the third quadrant to P(−3 ; −4). A "
                   "curved arrow marks the angle A, turning anticlockwise from OK round to OP."), "items": q51},
    {"id": "5.2", "title": "Question 5.2", "kind": "Double angles and co-functions", "marks": 4, "items": q52},   # the whole stem is the part's
    {"id": "6.1", "title": "Question 6.1", "kind": "Compound angle identities", "marks": 8,
     "lead": "Given the identity: cos(x − y) = cos x cos y + sin x sin y", "items": q61},
    {"id": "6.2", "title": "Question 6.2", "kind": "Trigonometric equations", "marks": 6, "items": q62},
    {"id": "6.3", "title": "Question 6.3", "kind": "Maximum of a trig function", "marks": 4,
     "lead": "Consider the function: g(x) = (4 − 8 sin² x)/3", "items": q63},
    {"id": "7", "title": "Question 7", "kind": "Trigonometric graphs", "marks": 11,
     "lead": "In the diagram below, the graph of f(x) = tan x is drawn for the interval x ∈ [−180° ; 180°].", "figure": fig("Q7", F7),
     "items": q7},
    {"id": "8", "title": "Question 8", "kind": "Heights and distances in 3D", "marks": 9,
     "lead": "In the diagram, C is the foot of a vertical building and D is the top of the same building. The height of the building, CD, is "
             "16 m. Two observers are standing 19 m apart at points A and B, where A, B and C lie in the same horizontal plane. A painter is "
             "working at point E on the building. The angle of elevation of D from A is 46,85°. DÊB = 122° and BĈA = 105,61°.",
     "figure": fig("Q8", "A drawing of a building with its vertical edge CD: C its foot, D its top, CD marked 16. E is a point on CD. On the "
                   "shaded ground, triangle ABC: B on the left, A on the right, AB = 19 and BĈA = 105,61°, with right angles at C between CD "
                   "and the ground. Lines DA and EB are drawn: the angle at A between AC and AD is 46,85°, and DÊB = 122° is marked at E."),
     "items": q8},
    {"id": "9", "title": "Question 9", "kind": "Cyclic quadrilaterals", "marks": 6,
     "lead": REASONS + " In the diagram, ABCD is a cyclic quadrilateral. BC is produced to E. AC is drawn. Â₁ = ½B̂, Â₂ = 46° and Ĉ₁ = 86°.",
     "figure": fig("Q9", "A circle through A (top), B (right), C (bottom) and D (left): cyclic quadrilateral ABCD with the diagonal AC. BC is "
                   "produced beyond C to E. At A, angle 1 lies between AD and AC, angle 2 (46°) between AC and AB. At C, angle 1 (86°) lies "
                   "between CE and CD, angle 2 between CD and CA, angle 3 between CA and CB."), "items": q9},
    {"id": "10.1", "title": "Question 10.1", "kind": "Proportionality theorem", "marks": 6,
     "lead": REASONS + " In the diagram, △RST is drawn. Line AB intersects RS and RT at A and B respectively such that AB ∥ ST.",
     "figure": fig("Q10.1", "Triangle RST with R at the top, S at the bottom left and T at the bottom right. A lies on RS and B on RT; AB and "
                   "ST are marked parallel (arrows)."), "items": q101},
    {"id": "10.2", "title": "Question 10.2", "kind": "Proportion in a circle", "marks": 9,
     "lead": REASONS + " In the diagram, O is the centre of the circle. △PWS is drawn with P, W and S on the circle. OR ⊥ PS. PRS is produced "
             "to T. SW and OT intersect at V. OV : OT = 1 : 4",
     "figure": fig("Q10.2", "A circle with centre O; P at the top and W at the bottom, PW passing through O. S is on the circle to the right of "
                   "P; chord PS is produced beyond S to T, outside the circle on the right. R lies on PS with OR ⊥ PS (the right angle marked "
                   "at R). Chord SW is drawn, and OT cuts SW at V."), "items": q102},
    {"id": "11", "title": "Question 11", "kind": "Tangent circles and similar triangles", "marks": 20,
     "lead": REASONS + " In the diagram, A, B, G and F lie on the larger circle. A smaller circle is drawn to touch the larger circle internally "
             "at A. EA is a common tangent to both circles. EBCF is a tangent to the smaller circle at C. AC is produced to G. AF cuts the "
             "smaller circle at D. AB, CD and GF are drawn.",
     "figure": fig("Q11", "A larger circle through A (upper left), F (right), G (bottom) and B (left), and a smaller circle inside it touching "
                   "it at A. EA touches both circles at A, E outside on the left. The line EBCF touches the smaller circle at C and cuts the "
                   "larger circle at B and F. AC produced meets the larger circle at G; AF cuts the smaller circle at D. AB, CD and GF are "
                   "drawn. Angles: at A, 1 between AE and AB, 2 between AB and AC, 3 between AC and AF; at B, 1 and 2 either side of BA; at C, "
                   "1 between CB and CA, 2 between CA and CD, 3 between CD and CF, 4 between CF and CG; at D, 1 and 2 either side of DC; at "
                   "F, 1 between FA and FC, 2 between FC and FG."), "items": q11},
]

PROOFS = ["3.3", "4.3", "4.4", "4.6", "5.2", "6.1.1", "6.1.2", "7.2", "7.4", "9.2", "10.1", "10.2.1", "11.1", "11.2", "11.3", "11.4"]
# every part that played as typed steps before 2026-10-10 (7.1, one number read off, plays as num), now authored multiple choice
assert tuple(AUTHORED) == ("1.1", "1.3", "1.6", "2.3", "2.5", "2.6", "3.1", "3.2", "3.4", "3.5", "3.6", "3.7", "4.1", "4.2", "4.5", "5.1.1",
                           "5.1.2", "5.1.3", "6.2", "6.3.1", "8.1", "8.2", "9.1", "10.2.2"), AUTHORED
ITEMS = [i for m in missions for i in m["items"]]
assert not [i["n"] for i in ITEMS if i["t"] == "steps"], "a typed calculation is left"
PROOF_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in PROOFS)
AUTHORED_MARKS = sum(i["marks"] for i in ITEMS if i["n"] in AUTHORED)
paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematics", "title": "Mathematics P2", "sitting": "November 2024", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematics", "total": 150, "missions": missions}],
    "flags": [
        {"n": "3.3", "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): " + ", ".join(PROOFS) + " ask for written "
                                                 "working or an answer a word marker cannot read (an interval, an expression in p, a general "
                                                 "solution, a 'show that', a derivation, a proof); each is played as four options, the memo's "
                                                 "answer or first method and three built from common errors, and keeps its marks (%d marks, "
                                                 "all or nothing)." % PROOF_MARKS},
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every typed calculation plays as the memo's "
                                                       "working plus three built from common errors, 0 or full marks: " + ", ".join(AUTHORED)
                                                       + " (%d parts, %d marks). The right option is the memo's FIRST method line by line; "
                                                         "4.1's memo gives the coordinates only (L(−1 ; −3)), so its working (M the midpoint of "
                                                         "PL) is ours, and 9.1's single line (Â₁ = 40° [ext ∠ of a cyclic quad]) is written as "
                                                         "Â₁ + 46° = 86°. A form the memo also accepts is never a wrong option (1.3's calculator "
                                                         "answer, 2.5's 35 employees, 2.6's 1,5 hours, 8.2's sine rule and EB̂C = 32°)."
                                                       % (len(AUTHORED), AUTHORED_MARKS)},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 11), hand-transcribed from the page IMAGES: the question "
                                                           "paper and answer book are scans with no text layer, and the memo's text layer garbles "
                                                           "fractions, roots and diagrams; no API call."},
        {"n": "1", "kind": "no_fit", "detail": "The paper prints the data table ACROSS (the 15 weights in one row, the push-ups in the next); it is "
                                               "typed as 15 rows of (x ; y) pairs, the same data in the same order."},
        {"n": "1.5", "kind": "no_fit", "detail": "The influence on the standard deviation is a term listing the memo's two answers (no influence OR "
                                                 "the standard deviation stays the same) in common phrasings, with 'increases' and 'decreases' "
                                                 "rejected; another wording is marked wrong."},
        {"n": "1.6", "kind": "low_confidence", "detail": "The memo keys the increase as 10 (from (40 ; 6) up to the target (40 ; 16)); the right "
                                                         "working shows the line's 15,86 at 40 kg taken up to 16 whole push-ups, which the memo "
                                                         "leaves unwritten, and no option ends in 9,86."},
        {"n": "2.1", "kind": "low_confidence", "detail": "Ogive read-offs (2.1 median 65, 2.2 Q₁ 44) are keyed as the memo prints them with a "
                                                         "tolerance of half a minute: the memo gives one value and no range, so a reading of 64 "
                                                         "or 66 is marked wrong."},
        {"n": "2.4", "kind": "no_fit", "detail": "The box and whisker diagram 2.4 is BUILT on the answer book's scaled line (2026-10-11: 0 to 120, "
                                                 "a number every 10, a tick every 5, placements to the minute): the learner places the five "
                                                 "values, the box and whiskers are drawn from them, and the memo's two ticks are marked from "
                                                 "them (the box: Q₁ 44, the median 65 and Q₃ 84 together; the whiskers: 5 and 120 together). "
                                                 "The quartiles are 2.1-2.3's ogive readings, keyed exactly as the memo prints them (as 2.1 and "
                                                 "2.2 are), so a box from a reading one minute off earns nothing; the memo's consistent "
                                                 "accuracy for a learner's own readings is not followed."},
        {"n": "7.3.2", "kind": "no_fit", "detail": "The graph of g (7.3.2) is BUILT on a grid with the answer book's axes (2026-10-11; the graph "
                                                   "of f that the answer book prints is not drawn on it): the learner places g's three turning "
                                                   "points, the curve is drawn through them, and the memo's three criteria are marked from "
                                                   "them (the shape from the curve the learner's own points fix)."},
        {"n": "2.5", "kind": "no_fit", "detail": "The memo accepts two readings (34 employees, 56,67%; OR 35 employees, 58,33%): the right option "
                                                 "uses its first; no option uses the second."},
        {"n": "7.1", "kind": "no_fit", "detail": "The asymptote x = 90° plays as the number 90 on the keypad (unit °): the keypad takes no letters, "
                                                 "and a typed term compares letters and digits only, so x = −90° would pass as x = 90°."},
        {"n": "4.5", "kind": "no_fit", "detail": "The working follows the memo's first method (the angles of inclination PÔV and RV̂N); its other "
                                                 "methods (R̂ = 90° with a trig ratio, the cosine rule) reach the same 45° and are not options."},
        {"n": "8.2", "kind": "no_fit", "detail": "The working follows the memo's cosine-rule route with BÊC = 58°; its sine-rule route (BC = 8,3 m) "
                                                 "and EB̂C = 32° reach the same DE = 10,81 m and are not options."},
        {"n": "9.1", "kind": "no_fit", "detail": "'Calculate, with a reason' an angle (9.1) plays as a working: the S and R marks go together "
                                                 "(0 or 2), so a right sum with a wrong reason is a wrong option."},
        {"n": "11.1", "kind": "low_confidence", "detail": "The memo accepts more than one set of four angles (its OR method reaches Ĉ₁ through "
                                                          "EA = EC [tans from common pt] and Ĉ₁ = EÂG [∠s opp equal sides]); the right option is "
                                                          "its first set, and each wrong option changes one line (a wrong reason or a wrong angle)."},
    ],
}

QTOTAL = {"1": 10, "2": 10, "3": 19, "4": 20, "5": 12, "6": 18, "7": 11, "8": 9, "9": 6, "10": 15, "11": 20}   # the paper's [n] per question
per_q, at = {}, []
NUMS = {i["n"] for i in ITEMS}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    per_q[m["id"].split(".")[0]] = per_q.get(m["id"].split(".")[0], 0) + got
    for i in m["items"]:
        assert set(i.get("after", [])) <= NUMS, (i["n"], i["after"])
        if i["t"] == "mcq":
            assert len({shape(o) for o in i["opts"]}) == 1, (i["n"], [shape(o) for o in i["opts"]])
            assert len(set(i["opts"])) == len(i["opts"]), (i["n"], "two options are the same")
            at.append("ABCD"[i["a"]])
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
assert per_q == QTOTAL, per_q
assert sorted(i["n"] for i in ITEMS if i["t"] == "mcq") == sorted(PROOFS + AUTHORED)
# the right letter, spread evenly over A-D across the paper (proofs and calculations)
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 1, spread
print("right options, the paper:", spread, "calculations:", {k: ["ABCD"[i["a"]] for i in ITEMS if i["n"] in AUTHORED].count(k) for k in "ABCD"})
total = sum(i["marks"] for i in ITEMS)
assert total == 150, total
print("authored calculations:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; proofs:", len(PROOFS), "parts,", PROOF_MARKS, "marks")
print("total:", total)
out = Path(__file__).parent / "out" / "math-p2-2024-11"   # written only once every check above has passed
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper, memo and answer book PDFs' page images (no API call)",
                                                        "scope": "Questions 1 to 11 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
