"""Mathematical Literacy P1 Nov 2024, the whole paper (Questions 1 to 5, 150 marks), hand-transcribed into the catalogue format (as
if Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks, answers and the
memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. No API call: the transcription
is the source, kept in git (out/ is not). The question paper and its ADDENDUM are SCANS (no text layer): read from their page
images; the memo has a text layer, checked against its page images.

  python tools/ingest/transcribe_ml_p1_2024_11.py
  python tools/ingest/ingest.py "<...>/Mathematical Literacy P1 Nov 2024 Eng.pdf" "<...>/Mathematical Literacy P1 Nov 2024 MG Afr & Eng.pdf" \
      --id ml-p1-2024-11 --from-json --answer-book "<...>/Mathematical Literacy P1 Nov 2024 Addendum Eng.pdf"

The paper reads three ANNEXURES printed in an ADDENDUM (the "answer book" of the ingest here): A (the tax tables) is typed, as 2.3's
table and extract; B (two line graphs) and C (two pie charts) are printed SIDEWAYS on the addendum's pages 3 and 4, so a crop would lie
on its side (as ANNEXURE D in ML P2 Nov 2025): B is described in 3.1's extract with its values read off the graphs ("about ..."), C is
typed as 5.1's table (income) and extract (expenditure). The ANSWER SHEET for QUESTION 4.1 is the question paper's page 14: its graph
is cropped from there, so no figure comes from the addendum.

How the memo's shapes map (Mathematical Literacy, as in ML P1 and P2 Nov 2025):
  a read-off -> num or term (a time slot, a fraction, a meter number, a tax bracket and a formula are strict terms: one digit or letter
  changes the answer); "Choose the statement (A-C)" / "Choose the correct option (A-E)" -> mcq in the paper's order; a word chosen from
  brackets -> mcq; definitions matched to terms -> match (2 marks a pair); "Identify the food items" -> list; "Calculate / Determine /
  Convert" -> steps, each step ONE number the memo's method produces (unit in the label's brackets), its RT/MA/CA/C/R marks riding on
  the number they lead to; "Verify ... whether ... valid" -> steps for the numbers, the conclusion (O) folded into the last step; a
  reason or a trend (O marks) -> rubric; three sources that must add up to 34% -> rubric with the memo's three sets as alternatives;
  "draw a line graph on the ANSWER SHEET" -> draw, self-checked.
  A memo range or two accepted answers -> a tolerance spanning them; the memo's NPR (no penalty for rounding if the first decimal is
  correct) widens a tolerance to cover the answer's one-decimal rounding.
Figure boxes are measured in PDF points (the scan's pages 595.2 x 841.68) from ink profiles of the page renders (scratchpad
ml1_24: ink_ml1_24.py, prof_ml1_24.py), set so that ingest's 1% pad keeps the drawing and leaves out the "[Adapted from ...]" lines and
the text around it, and checked on the cropped figures; `inset` where a printed label sits in the crop's top-left corner (the page's
Hide button sits there)."""
import json
import re
from pathlib import Path

W, H = 595.2, 841.68
FIGS = {  # [source, page, x0, y0, x1, y1] in points ("qp" the question paper, "ab" the addendum)
    "1.1": ["qp", 3, 105.0, 166.0, 513.5, 416.6], "3.2.4": ["qp", 9, 148.0, 556.0, 530.0, 648.0],
    "4.1": ["qp", 14, 58.0, 290.5, 530.0, 754.0]}
INSET = {"1.1": 40, "3.2.4": 40, "4.1": 40}


def fig(name, caption):
    src, p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption,
            **({"source": "answer_book"} if src == "ab" else {}), **({"inset": INSET[name]} if name in INSET else {})}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


def rub(n, q, marks, bullets, clues, each=None, must=None, notes=None, worth=None):
    return {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **({"each": each} if each else {}),
            **({"must": must} if must else {}), **({"notes": notes} if notes else {}), **({"worth": worth} if worth else {})}


term = lambda n, q, a, clues, marks=2, strict=False: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a,
                                                      **({"strict": True} if strict else {})}
num = lambda n, q, a, tol, unit, clues, marks=2: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
lst = lambda n, q, count, pool, clues, marks: {"t": "list", "n": n, "marks": marks, "q": q, "clues": clues, "count": count, "pool": pool}
match = lambda n, q, left, right, a, each, clues, **kw: {"t": "match", "n": n, "marks": len(left) * each, "q": q, "clues": clues, "left": left,
                                                         "right": right, "a": a, **({"each": each} if each > 1 else {}), **kw}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}


def steps(n, q, marks, sts, clues):
    """sts: (label, marks, answer, tolerance, the memo's working[, other values that also earn it])."""
    s = [{"id": "s%d" % (i + 1), "label": st[0], "marks": st[1], "a": st[2], "tol": st[3], "memo": st[4], **({"also": st[5]} if len(st) > 5 else {})}
         for i, st in enumerate(sts)]
    assert sum(x["marks"] for x in s) == marks, n
    return {"t": "steps", "n": n, "marks": marks, "q": q, "clues": clues, "steps": s}


def bare(s):
    """How the app compares a STRICT term: lower case, letters and digits only (spacing and punctuation are free)."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def unique(forms):
    """Forms that differ to a strict term, the first spelling of each kept (the memo's own wording first)."""
    seen, out = set(), []
    for f in forms:
        if bare(f) not in seen:
            seen.add(bare(f)); out.append(f)
    return out


def slot():
    """The time slot 17:30-18:00 as learners write it: 24-hour (17:30, 17h30), 12-hour (5:30 pm) or in words, joined by a dash, 'to'
    or 'until' (the memo: 1A for the start, 1A for the end)."""
    pairs = [("17:30", "18:00"), ("17h30", "18h00"), ("5:30 pm", "6:00 pm"), ("5:30", "6:00 pm"), ("5:30 pm", "6 pm"), ("5:30 pm", "6:00"),
             ("Half past five", "6 o'clock"), ("Half past five", "six o'clock")]
    out = ["17:30 – 18:00", "5:30 pm – 6:00 pm", "Half past five until 6 o'clock in the afternoon",
           "Half past five until 6 o'clock in the evening"]
    out += ["%s%s%s" % (a, j, b) for a, b in pairs for j in (" – ", " to ", " until ")]
    return unique(out)


def formulas():
    """DJ Rain's cost for more than 5 hours, Cost = R4 000 + R1 250 x (number of hours exceeding 5), in the forms a learner types:
    with or without 'Cost =' and the R, x as a letter or a sign, the variable named or n, either term first."""
    pre, fixed, rate, mul = ["Cost = ", "C = ", ""], ["R4 000", "4 000"], ["R1 250", "1 250"], [" × ", " x "]
    var = ["(number of hours exceeding 5)", "(number of hours more than 5)", "n", "n, where n = number of hours exceeding 5",
           "n, where n = number of hours more than 5", "(number of hours − 5)", "(hours − 5)", "(n − 5)"]
    out = ["Cost = R4 000 + R1 250 × (number of hours exceeding 5)", "Cost = R4 000 + R1 250 × n, where n = number of hours exceeding 5"]
    for p in pre:
        for f in fixed:
            for r in rate:
                for m in mul:
                    for v in var:
                        out += ["%s%s + %s%s%s" % (p, f, r, m, v)]
                        if not v.startswith("n,"):
                            out += ["%s%s%s%s + %s" % (p, r, m, v, f)]
    return unique(out)


# ---- QUESTION 1, the question paper pages 3-5 and the memo pages 2-4 ----
q11 = [
    num("1.1.1", "Write down the number of voters at School Y from 16:00–16:30.", 5, 0.01, "voters",
        ["School Y's bars are the patterned ones.", "Find the 16:00–16:30 slot and read its bar against the axis."]),
    term("1.1.2", "Identify the time slot when 30 people voted at School X.", slot(),
         ["School X's bars are the black ones.", "Find the bar that reaches the 30 line, then read its time slot below."], strict=True),
    mcq("1.1.3", "Choose the statement (A–C) below that BEST describes the trend of the voters at School Y.", [
        "As time went by, the voter numbers increased to a maximum and then decreased.",
        "The voter numbers started high, then decreased and then picked up again.",
        "The number of voters decreased, then increased and finally decreased with time."], 2,
        ["Follow School Y's patterned bars from the first slot to the last.", "Note each place where the bars change from going down to going up, or back."]),
    term("1.1.4", "The probability of randomly selecting a voter from School X is 0,56 during the 17:30–18:00 time slot.\n\nWrite 0,56 as a "
         "simplified fraction.", ["14/25", "14 over 25"],
         ["0,56 is 56 hundredths: write it over 100 first.", "Divide the top and the bottom by their highest common factor."], strict=True),
    steps("1.1.5", "Calculate the total number of voters at both schools who voted during the 17:00–17:30 time slot.", 3, [
        ("Total number of voters at both schools", 3, 52, 0.01, "Total number = 26 + 26 ✓RT ✓MA = 52 ✓A")],
          ["Read both bars in the 17:00–17:30 slot.", "Add the two schools' voters."])]
FOOD = {"title": "TABLE 1: COMPARATIVE FOOD PRICES FOR SOME LUNCH ITEMS",
        "head": ["FOOD ITEMS", "PRICE IN RAND: MAY 2022", "PRICE IN RAND: MAY 2023", "PERCENTAGE CHANGE: YEAR ON YEAR",
                 "PERCENTAGE CHANGE: MONTH ON MONTH"],
        "rows": [["410 g beans", "12,60", "15,14", "20,2", "0,5"], ["250 g instant coffee", "45,56", "48,47", "6,4", "–1,0"],
                 ["Eggs 1,5 dozen tray", "52,97", "57,33", "8,2", "1,6"], ["750 mℓ sunflower oil", "40,68", "35,52", "–12,7", "–2,3"],
                 ["Oranges per kg", "22,07", "20,10", "–8,9", "–14,5"], ["Chicken giblets per kg", "37,73", "46,75", "23,9", "2,2"],
                 ["Chicken portions per 2 kg", "86,80", "93,06", "7,2", "0,6"], ["TOTAL", "A", "R316,37", "", ""]]}
q12 = [
    lst("1.2.1", "Identify the food items that showed a decrease in both the month-on-month and year-on-year percentage change.", 2,
        [["Sunflower oil", "Oil"], ["Oranges", "Orange"]],
        ["A decrease is a negative percentage change.", "Both percentage columns must be negative in the same row."], 3),
    steps("1.2.2", "Determine the missing value, A.", 2, [
        ("Total price A for May 2022 (R)", 2, 298.41, 0.005, "Value of A = R12,60 + R45,56 + R52,97 + R40,68 + R22,07 + R37,73 + R86,80 ✓MA "
         "= R298,41 ✓A. NPU")],
          ["A is the TOTAL of the May 2022 column.", "Add all seven May 2022 prices."]),
    steps("1.2.3", "Calculate the price of a dozen eggs during May 2022.", 2, [
        ("Price of a dozen eggs in May 2022 (R)", 2, 35.31, 0.015, "Price per dozen = R52,97 ÷ 1,5 ✓A (OR × 1/1,5) = R35,31 ✓A (OR 1 egg = "
         "R52,97 ÷ 18 ✓A, price per dozen = R2,94277 × 12 = R35,31 ✓A; OR price for ½ dozen = R52,97 ÷ 3 ✓A = R17,65666, price for a "
         "dozen = R17,65666 × 2 = R35,31 ✓A). NPR")],
          ["The tray in TABLE 1 holds 1,5 dozen eggs.", "Find the price of ONE dozen from the May 2022 price."]),
    steps("1.2.4", "Write down the unit ratio, in the form 1 : …, for the price of the oranges in May 2022 to the price of the oranges in "
          "May 2023.", 3, [
        ("Price of oranges in May 2022 (R)", 1, 22.07, 0.005, "22,07 ✓RT"),
        ("Price of oranges in May 2023 (R)", 1, 20.10, 0.005, "20,10 ✓RT"),
        ("The unit ratio 1 : … (the number after the colon)", 1, 0.91, 0.011, "= 22,07 : 20,10 = 1 : 0,9107385591 ≈ 1 : 0,91 ✓A "
         "(simplification in correct order). NPR")],
          ["May 2022 comes first in the ratio.", "Divide both sides by the May 2022 price."])]
TERMS = ["An increase in the price of a basket of goods or services over time that is representative of the economy as a whole",
         "Sum of all the values divided by the number of values",
         "The income received from the item sold and the cost price of the item is the same",
         "Value or values appearing most often in a data set", "The difference between the highest and lowest values in a data set",
         "An amount paid regularly at a particular rate for the use/loan of money",
         "These are amounts that must be paid every month and which stay the same, like rent, school fees and transport costs",
         "Middle value in an ordered data set",
         "Expenses that change over time or from one week/month to the next, e.g. telephone and electricity costs",
         "The point where the income exceeds the expenses"]
DEFS = {"title": "TABLE 2: TERMINOLOGY USED IN MATHEMATICAL LITERACY", "head": ["LETTER", "DEFINITION"],
        "rows": [[chr(65 + i), t] for i, t in enumerate(TERMS)]}
q13 = [match("1.3", "Use TABLE 2 above and match the definitions with the terminology below. Write only the letter (A–J) next to the question "
             "numbers (1.3.1 to 1.3.4), e.g. 1.3.5 K.", ["1.3.1 Break-even point", "1.3.2 Inflation", "1.3.3 Variable expenses", "1.3.4 Mean"],
             TERMS, [2, 0, 8, 1], 2,
             ["At the break-even point there is neither a profit nor a loss.",
              "Two definitions describe expenses: one kind stays the same each month, the other kind changes."],
             heads=["TERMINOLOGY", "DEFINITION (A–J)"])]

# ---- QUESTION 2, the question paper pages 6-7, ANNEXURE A (the addendum page 2) and the memo pages 5-8 ----
SLIP = ("TAX INVOICE VAT NO. 4420106777\n*** PREPAID ELECTRICITY ***\nElectricity Municipal Prepaid\nVAT REGISTRATION NO. 4370102313\n"
        "Meter: 07032985769\n\nDOMESTIC HOUSEHOLD TARIFF\n\nTransaction Sequence No.: 56332515\n\nAmount: R1 300,00\nUnits: *** kWh\n\n"
        "Electricity: R1 130,43\nVAT 15%: B\nTOTAL: R1 300,00")
TARIFF = {"title": "TABLE 3: RESIDENTIAL ELECTRICITY TARIFF", "head": ["BLOCK", "CONSUMPTION (kWh)", "TARIFF (R/kWh)"],
          "rows": [["Block 1", "0–350", "2,19"], ["Block 2", "More than 350", "2,91"]]}
q21 = [
    term("2.1.1", "Write down the meter number.", ["07032985769"],
         ["Look near the top of the till slip.", "Copy every digit exactly as printed."], strict=True),
    steps("2.1.2", "Determine the missing value, B.", 3, [
        ("VAT amount B (R)", 3, 169.565, 0.006, "B = R1 300,00 ✓RT – R1 130,43 ✓MA = R169,57 ✓A (OR B = R1 130,43 × 15/100 OR × 0,15 = R169,56; "
         "OR B = R1 300 × 15/115 = R169,57). AO")],
          ["B is the VAT on the electricity.", "The TOTAL includes the VAT."]),
    steps("2.1.3", "A partial residential electricity tariff table (excluding VAT) is shown below.\n\nDetermine the number of kWh units Miecke "
          "purchased.", 7, [
        ("Cost of the Block 1 units, excluding VAT (R)", 2, 766.50, 0.005, "Amount for Block 1 = 350 kWh × R2,19 ✓MA = R766,50 ✓CA (OR with "
         "the tariffs including VAT ✓A: R2,19 × 115/100 = R2,5185 and R2,91 × 115/100 = R3,3465; amount spent in Block 1 = 350 kWh × "
         "R2,5185 = R881,475 ✓MCA)"),
        ("Amount left for the Block 2 units (R)", 1, 363.93, 0.005, "Amount left for Block 2 = R1 130,43 – R766,50 = R363,93 ✓MCA (OR "
         "R1 300 – R881,475 = R418,525 ✓MCA)"),
        ("Number of Block 2 units (kWh)", 2, 125.06, 0.045, "Units in Block 2 = R363,93 ÷ R2,91 ✓MCA = 125,0618557 kWh ✓CA (OR R418,525 ÷ "
         "R3,3465 ✓MCA = 125,06 kWh ✓CA)"),
        ("Total number of kWh units purchased (kWh)", 2, 475.06, 0.045, "Total kWh received = 350 kWh + 125,0618557 kWh ✓MCA = 475,06 kWh "
         "✓CA. NPR")],
          ["The R1 130,43 for electricity excludes VAT, like TABLE 3's tariffs.",
           "The first 350 kWh are charged at the Block 1 tariff; what is left of the money buys units at the Block 2 tariff."])]
SOLAR = {"title": "HOME SOLAR SYSTEM UNIT PAYMENT OPTIONS", "head": ["OPTION 1: RENT-TO-OWN", "OPTION 2: CASH PRICE"],
         "rows": [["Pay for 7 years at R1 549 p/m", "R78 200 (incl. VAT)"], ["Additional costs:", ""], ["R782 initiation fee", ""],
                  ["Buy-out after rental period R7 820", ""]]}
q22 = [
    num("2.2.1", "Write down the monthly instalment for the rent-to-own option.", 1549, 0.01, "R",
        ["Read OPTION 1 in the advertisement.", "p/m means per month."]),
    steps("2.2.2", "Calculate, excluding VAT, the cash price of the home solar system unit.", 3, [
        ("Cash price excluding VAT (R)", 3, 68000, 0.005, "Price excluding VAT = R78 200 ✓RT ÷ 1,15 ✓MA = R68 000 ✓A (OR R78 200 × 100/115 "
         "= R68 000; OR VAT amount = R78 200 × 15/115 = R10 199,999 ≈ R10 200, price excluding VAT = R78 200 – R10 200 = R68 000)")],
          ["The cash price R78 200 includes 15% VAT.", "So R78 200 is 115% of the price without VAT."]),
    steps("2.2.3", "After seven years, Miecke decides to buy-out the rent-to-own option.\n\nCalculate the extra amount she has to pay compared to "
          "buying the home solar system unit for cash.", 5, [
        ("Number of months in the rental period", 1, 84, 0.01, "Number of months = 12 × 7 = 84 months ✓A"),
        ("Total cost of the rent-to-own option (R)", 2, 138718, 0.005, "Rent-to-own = (R1 549 × 84) + R782 + R7 820 = R130 116 + R782 + R7 820 "
         "✓MCA = R138 718 ✓CA"),
        ("Extra amount compared to the cash price (R)", 2, 60518, 0.005, "Difference = R138 718 – R78 200 ✓MCA = R60 518 ✓CA")],
          ["Count the monthly instalments in 7 years, then add the initiation fee and the buy-out.", "Compare the total with the cash price."])]
TAX = {"title": "ANNEXURE A: TAX RATES FROM 1 MARCH 2023 TO 29 FEBRUARY 2024", "head": ["Tax Bracket", "Taxable income (R)", "Tax rates (R)"],
       "rows": [["A", "1–237 100", "18% of taxable income"], ["B", "237 101–370 500", "42 678 + 26% of taxable income above 237 100"],
                ["C", "370 501–512 800", "77 362 + 31% of taxable income above 370 500"],
                ["D", "512 801–673 000", "121 475 + 36% of taxable income above 512 800"],
                ["E", "673 001–857 900", "179 147 + 39% of taxable income above 673 000"],
                ["F", "857 901–1 817 000", "251 258 + 41% of taxable income above 857 900"],
                ["G", "1 817 001 and above", "644 489 + 45% of taxable income above 1 817 000"]]}
TAX_MORE = ("ANNEXURE A (continued)\n\nTAX REBATES 2023/2024\nPrimary: R17 235\nSecondary (person 65 and older): R9 444\nTertiary (person 75 "
            "and older): R3 145\n\nTAX THRESHOLDS 2023/2024\nUnder 65: R95 750\n65 and older: R148 217\n75 and older: R165 689\n\n2023/2024 "
            "MEDICAL CREDITS – MONTHLY CONTRIBUTION\nFor the taxpayer or for a dependant who is a member of a medical aid: R364\nFor the taxpayer "
            "and one dependant: R728\nFor each additional dependant: R246")
q23 = [
    term("2.3.1", "Identify the tax bracket that Miecke will use to calculate her income tax payable.", ["C", "Bracket C", "Tax bracket C"],
         ["ANNEXURE A's brackets are for ANNUAL taxable income.", "Work out her yearly income, then find the row whose range holds it."],
         marks=3, strict=True),
    steps("2.3.2", "Calculate Miecke's annual tax payable for the 2023/2024 tax year.", 5, [
        ("Tax before the rebate (R)", 3, 108613.16, 0.006, "Tax before rebate = 77 362 + 31% of taxable income above 370 500 = R77 362 + 31% "
         "(R471 310,20 – R370 500) ✓SF = R77 362 + 31% (R100 810,20) = R77 362 + R31 251,162 ✓MCA = R108 613,162 ✓CA (CA from 2.3.1)"),
        ("Annual tax payable (R)", 2, 91378.16, 0.006, "Annual tax payable = R108 613,162 – R17 235 ✓RT = R91 378,162 = R91 378,16 ✓CA (OR "
         "= R77 362 + 0,31 (R471 310,20 – R370 500) ✓SF ✓✓MCA – R17 235 ✓RT = R91 378,16 ✓CA)")],
          ["Use her bracket's tax rate with her annual taxable income.", "She is under 65 and has no medical aid: which rebate applies, and are there "
           "any medical credits?"])]

# ---- QUESTION 3, the question paper pages 8-9, ANNEXURE B (the addendum page 3, sideways: typed) and the memo pages 9-10 ----
GRAPHS = ("ANNEXURE B (printed sideways in the addendum; typed here, values read off the graphs)\n\n"
          "GRAPH 1: TRENDS IN THE TOTAL NUMBER OF STORES — a line graph: Total number of stores (0 to 4 000, gridlines every 1 000) against "
          "YEAR (every year from 2014 to 2023); a solid line for Shoprite and a broken line for Pick n Pay.\n"
          "• Shoprite: 1 581 in 2014 (labelled), about 1 800 in 2015, about 1 880 in 2016, about 2 380 in 2017, about 2 450 in 2018, about "
          "2 350 in 2019, about 2 380 in 2020, about 2 500 in 2021, about 3 000 in 2022 and 3 543 in 2023 (labelled).\n"
          "• Pick n Pay: 1 128 in 2014 (labelled), about 1 200 in 2015, about 1 450 in 2016, about 1 550 in 2017, about 1 700 in 2018, about "
          "1 800 in 2019, about 1 850 in 2020, about 1 980 in 2021, about 2 050 in 2022 and 2 204 in 2023 (labelled).\n\n"
          "GRAPH 2: TRENDS IN THE TOTAL NUMBER OF EMPLOYEES — a line graph: Total number of employees (gridlines at 50 000, 100 000 and "
          "150 000) against YEAR (only 2005, 2014 and 2023 marked; the years between are evenly spaced).\n"
          "• Shoprite: about 60 000 in 2005, rising every year to about 124 000 in 2014; then about 132 000 in 2015, about 137 000 in 2016, "
          "about 143 000 in 2017, about 147 000 in 2018 and 2019, about 141 000 in 2020, about 142 000 in 2021, about 145 000 in 2022 and "
          "153 726 in 2023 (labelled).\n"
          "• Pick n Pay: about 60 000 in 2005, a line rising steadily (drawn dotted from about 2006) to about 72 000 in 2014; then about "
          "70 000 in 2015, about 70 000 in 2016, about 80 000 in 2017, about 85 000 in 2018, about 90 000 in 2019, and level at 90 000 "
          "(labelled) from 2019 to 2023.")
q31 = [
    num("3.1.1", "Identify the year in which there was a decrease in the number of employees in the Pick n Pay stores for the first time.", 2015,
        0.01, "", ["Use GRAPH 2 and follow the Pick n Pay line from 2005.", "Find the first year in which the line goes down."]),
    steps("3.1.2", "It is projected that the number of Pick n Pay stores will increase by 95,39% from 2023 to 2032.\n\nDetermine, by means of "
          "calculations, the projected number of Pick n Pay stores in 2032.", 3, [
        ("Number of Pick n Pay stores in 2023", 1, 2204, 0.5, "2 204 ✓RT"),
        ("Projected number of Pick n Pay stores in 2032", 2, 4306.5, 0.51, "Projected number of stores = 2 204 × 95,39/100 ✓MA + 2 204 = "
         "2 102,3956 + 2 204 = 4 306,3956 = 4 306 ✓CA (OR 2 204 × 195,39/100 OR × 1,9539 = 4 306 stores). Accept: 4 307. AO")],
          ["Start from the number of Pick n Pay stores in 2023 (GRAPH 1).", "Add 95,39% of it to itself."]),
    steps("3.1.3", "An analyst stated that Shoprite employed more employees per store than Pick n Pay during 2023.\n\nVerify, showing ALL "
          "calculations, whether the analyst's statement is valid.", 6, [
        ("Shoprite employees per store in 2023", 3, 43.39, 0.015, "Average Shoprite = 153 726 ✓RT ÷ 3 543 ✓RT = 43,388653… employees ✓CA"),
        ("Pick n Pay employees per store in 2023", 3, 40.83, 0.035, "Average Pick n Pay = 90 000 ÷ 2 204 ✓RT (both values) = 40,834845… "
         "employees ✓CA. Her statement is VALID ✓O. NPR")],
          ["Employees per store = the number of employees ÷ the number of stores, both in 2023.", "Employees are on GRAPH 2, stores on GRAPH 1."]),
    steps("3.1.4", "Determine, as a percentage, the probability of randomly selecting a year where the number of Shoprite stores is fewer than "
          "2 000.", 3, [
        ("Probability (%)", 3, 30, 0.005, "Probability = 3 ✓RT / 10 ✓RT × 100% = 30% ✓CA. AO")],
          ["Use GRAPH 1: count the years in which the Shoprite line is below 2 000.", "Divide by the number of years on the graph."])]
TIMES = "12  15  25  25  40  28  18  23\n43  15  22  19  15  8  37  9\n24  23  15  67  25  29  6  17\n15  43  23  27  33  26  127  10"
q32 = [
    steps("3.2.1", "Write down the number of customers that represent the sample size and the number of customers that represent the population "
          "size for this study.", 3, [
        ("Sample size (customers)", 2, 32, 0.01, "Sample = 32 ✓A ✓A (1A counting to 32, 1A sample)"),
        ("Population size (customers)", 1, 12342, 0.01, "Population = 12 342 ✓A (OR 32 and 12 342: 2A sample in correct order, 1A population in "
         "correct order; no words used)")],
          ["Each recorded time is one customer in the sample: count them.", "The population is the whole group the sample is taken from."]),
    mcq("3.2.2", "Choose the correct option (A, B, C, D or E) that represents the stage in the data handling process that uses the measures of "
        "central tendency and spread.", ["Collecting data", "Classifying and organising data", "Summarising data", "Representing data",
                                         "Analysing data"], 4,
        ["The stages run in order: collect, organise, summarise, represent, then use the results.",
         "Which stage USES the measures to draw conclusions about the data?"]),
    rub("3.2.3", "Give a reason why the value of 127 is considered to be an outlier in the data set.", 2, [
        "The value 127 is 60 minutes more than the second highest time in the dataset (2)."],
        ["Compare 127 with the next largest value in the data.", "How far apart are they?"], each=2,
        notes=["The memo underlines 'more than the second highest' (2O conclusion)."])]
RANKED = "6  8  9  10  12  15  15  15  15  15  17\n18  19  22  23  23  23  24  25  25  25  26\n27  28  29  33  37  40  43  43  67  127"
q324 = [
    steps("3.2.4(a)", "Calculate the value of the upper quartile (Q3).", 3, [
        ("Upper quartile (Q3)", 3, 28.5, 0.005, "Quartile 3 = (28 + 29) ✓RT ÷ 2 ✓MA = 28,5 ✓CA. AO")],
          ["There are 32 values: the upper quartile is the middle of the upper 16.", "With an even count, average the two middle values."]),
    steps("3.2.4(b)", "Vuyo stated that if the outlier value was removed from the data set, the new interquartile (IQR) value would be 13.\n\n"
          "Verify Vuyo's statement, showing ALL calculations.", 5, [
        ("New lower quartile (Q1)", 1, 15, 0.01, "New Quartile 1 = 15 ✓RT"),
        ("New upper quartile (Q3)", 1, 28, 0.01, "New Quartile 3 = 28 ✓RT"),
        ("New interquartile range (IQR)", 3, 13, 0.01, "IQR = Q3 – Q1 ✓A; IQR = 28 – 15 ✓MCA = 13. He is CORRECT ✓O")],
          ["Without 127 there are 31 values, and the median is the 16th.", "Q1 and Q3 are the middles of the 15 values below and the 15 above the median."])]

# ---- QUESTION 4, the question paper pages 10-11, the ANSWER SHEET (page 14) and the memo pages 11-14 ----
PARTY = {"title": "TABLE 4: BUDGETED EXPENSES FOR THE PARTY", "head": ["", ""],
         "rows": [["Cost of the venue", "R750 deposit and R6 185 for the day"], ["Food and drinks", "R18 000"], ["Birthday cake", "R1 250"],
                  ["OPTIONS FOR DISC JOCKEYS (DJs)", ""],
                  ["DJ Rain", "R4 000 for 5 hours or less. Thereafter the tariff is an additional R1 250 per hour."],
                  ["DJ 5-Star", "R1 000 per hour or part thereof"], ["DJ Cool", "R6 000 for the party"]]}
DJ_RAIN = ("TABLE 5: COST TO HIRE DJ RAIN PER HOUR (also printed on the ANSWER SHEET)\nNumber of hours: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9\n"
           "Cost (in R): 4 000 | 4 000 | P | 4 000 | 4 000 | Q | 6 500 | 7 750 | R")
q41 = [
    term("4.1.1(a)", "The table below represents the cost to hire DJ Rain (TABLE 5: COST TO HIRE DJ RAIN PER HOUR).\n\nWrite a formula to "
         "calculate the cost to hire DJ Rain for more than 5 hours in the following form:\nCost = …", formulas(),
         ["The first 5 hours cost one fixed amount.", "Every hour after the fifth adds the same tariff."], marks=3, strict=True),
    steps("4.1.1(b)", "Complete the table by calculating the missing values P, Q and R.", 4, [
        ("Value of P (R)", 1, 4000, 0.01, "P = 4 000 ✓A"),
        ("Value of Q (R)", 2, 5250, 0.01, "Q = 5 250 ✓✓A"),
        ("Value of R (R)", 1, 9000, 0.01, "R = 9 000 ✓A")],
          ["Up to 5 hours the cost does not change.", "After 5 hours, use your formula from (a)."]),
    term("4.1.2(a)", "The graphs showing the costs to hire DJ 5-Star and DJ Cool are shown on the ANSWER SHEET.\n\nName the type of graph used to "
         "represent the cost to hire DJ 5-Star.", ["Step graph", "Stepwise graph", "Step-wise graph"],
         ["Look at DJ 5-Star's graph between the whole hours.", "The cost stays the same for each part of an hour, then jumps: what shape does "
          "that make?"]),
    draw("4.1.2(b)", "Use TABLE 5, showing the cost to hire DJ Rain for up to 9 hours, to draw a line graph on the same grid on the ANSWER SHEET.", 4, [
        ["Starting point (0 ; 4 000)", 1], ["(5 ; 4 000)", 1], ["End point (9 ; 9 000)", 1],
        ["Joining ALL the points plotted on the slanted part of the graph", 1]],
        ["Plot each value in TABLE 5, with your P, Q and R.", "Join the points with straight lines."],
        memo="CA from 4.1.1(b). The line runs flat at R4 000 from (0 ; 4 000) to (5 ; 4 000), then rises through (6 ; 5 250), (7 ; 6 500) and "
             "(8 ; 7 750) to (9 ; 9 000)."),
    steps("4.1.3", "Lee's parents decide to hire DJ 5-Star for the 21st birthday party. DJ 5-Star will provide the music entertainment from 18:00 "
          "until 01:30.\n\nDetermine the total budgeted expenses for the party.", 5, [
        ("Number of hours DJ 5-Star charges for", 1, 8, 0.01, "Time = 18:00 – 01:30 = 7 hrs 30 min ≈ 8 hrs ✓A"),
        ("Cost of DJ 5-Star (R)", 2, 8000, 0.01, "Cost for DJ = 8 × R1 000 ✓MCA = R8 000 ✓CA"),
        ("Total budgeted expenses for the party (R)", 2, 34185, 0.01, "Total cost = R18 000 + R750 + R6 185 + R1 250 + R8 000 ✓MCA = R34 185 ✓CA")],
          ["Find how long DJ 5-Star plays: 'or part thereof' counts a part of an hour as a whole hour.",
           "Add the venue (deposit and the day), the food and drinks, the cake and the DJ."]),
    rub("4.1.4", "Give ONE reason why Lee's parents did not choose DJ Cool.", 2, [
        "He charges a flat/fixed rate, which is not economical if the party ends early (2).", "OR — He has a bad reputation (2)."],
        ["Compare how DJ Cool charges with how the other two DJs charge.", "Think about a party that ends earlier than planned."], each=2)]
GUESTS = {"title": "TABLE 6: ACTUAL NUMBER OF GUESTS PER FUNCTION", "head": ["YEAR", "NUMBER OF GUESTS", "", "", "", "", "", "", "", ""],
          "rows": [["2023", "180", "350", "400", "200", "215", "90", "150", "230", "160"],
                   ["2022", "360", "160", "300", "70", "160", "200", "240", "", ""]]}
q42 = [
    steps("4.2.1", "Write, as a decimal, the probability that a cinema-style venue was chosen as a suitable function venue for all the functions "
          "held during 2022 and 2023.", 3, [
        ("Functions that needed the cinema-style venue", 1, 4, 0.01, "4 ✓A (numerator)"),
        ("Functions held during 2022 and 2023", 1, 16, 0.01, "16 ✓A (denominator)"),
        ("Probability, as a decimal", 1, 0.25, 0.005, "Probability = 4/16 = 0,25 ✓CA")],
          ["The cinema-style venue is needed when a function has too many guests for either sit-down venue.", "Count the functions in both years."]),
    steps("4.2.2", "Determine the median number of guests accommodated during 2023.", 3, [
        ("Median number of guests in 2023", 3, 200, 0.01, "90 150 160 180 200 215 230 350 400 ✓A (arranging); Median = 200 ✓✓A. AO")],
          ["Arrange the nine 2023 values in order.", "The median is the middle value."]),
    steps("4.2.3", "The manager stated that the range of the number of guests per function during 2022, is the same as the range of the number of "
          "guests per function during 2023.\n\nVerify, showing ALL calculations, whether his statement is valid.", 5, [
        ("Range of the number of guests in 2022", 3, 290, 0.01, "Range 2022 = 360 – 70 ✓RT (both values) ✓MCA = 290 ✓CA"),
        ("Range of the number of guests in 2023", 2, 310, 0.01, "Range 2023 = 400 – 90 = 310 ✓A. His statement is NOT VALID ✓O")],
          ["Range = highest value − lowest value.", "Work out each year's range, then compare them."])]

# ---- QUESTION 5, the question paper pages 12-13, ANNEXURE C (the addendum page 4, sideways: typed) and the memo pages 15-18 ----
INCOME = {"title": "ANNEXURE C — Indian Union Budget Income Sources in 2023-2024 (45,03 lakh crores), a pie chart",
          "head": ["INCOME SOURCE", "PERCENTAGE"],
          "rows": [["Corporation tax", "15%"], ["Income tax", "15%"], ["Customs", "4%"], ["Excise duties", "7%"], ["GST", "…"],
                   ["Non-tax receipts", "6%"], ["Non-debt capital receipts", "2%"], ["Borrowings", "34%"]]}
SPEND = ("ANNEXURE C (printed sideways in the addendum; both pie charts typed here, the income sources in the table)\n\n"
         "Indian Union Budget 2023-2024 Expenditure (45,03 lakh crores), a pie chart:\nCentral sector schemes 17%\nInterest payments 20%\n"
         "Defence 8%\nSubsidies 7%\nFinance commission and others 9%\nState shares of taxes 18%\nPensions 4%\nOther expenditure 8%\n"
         "Centrally sponsored schemes 9%")
q51 = [
    mcq("5.1.1", "Choose the correct word from those given in brackets. Write down only the word next to the question number (5.1.1).\n\nA budget "
        "is a (deficit/surplus/balanced) budget when the income is less than the expenditure.", ["deficit", "surplus", "balanced"], 0,
        ["Income less than expenditure: is money left over, missing, or exactly enough?", "A balanced budget has income equal to expenditure."]),
    steps("5.1.2", "General sales tax (GST) is a tax that is similar to VAT in South Africa.\n\nCalculate the missing percentage for GST on the pie "
          "chart.", 3, [
        ("Missing percentage for GST (%)", 3, 17, 0.005, "GST % = 100% – (15% + 15% + 4% + 7% + 6% + 2% + 34%) ✓RT ✓MA = 100% – 83% = 17% "
         "✓CA. AO")],
          ["A pie chart's percentages add up to 100%.", "Add all the other income percentages first."]),
    steps("5.1.3", "Calculate, in lakh crores, the amount spent on defence in India.", 3, [
        ("Amount spent on defence (lakh crore)", 3, 3.6024, 0.0025, "Defence = 8% ✓RT × 45,03 lakh crore ✓MA = 3,6024 lakh crore ✓CA. NPR. AO")],
          ["Read Defence's percentage on the expenditure pie chart.", "Take that percentage of the 45,03 lakh crores."]),
    rub("5.1.4", "List THREE sources of income shown on the pie chart where the total percentages add up to the borrowing percentage value.", 3, [
        "Corporation tax (1).", "Income tax (1).", "Customs (1).",
        "OR — Corporation tax (1).", "GST (1).", "Non-debt capital receipts (1).",
        "OR — Income tax (1).", "GST (1).", "Non-debt capital receipts (1)."],
        ["Borrowings are 34% of the income.", "Try combinations of three slices until their percentages total exactly 34%."],
        notes=["CA from 5.1.2 for GST.", "Each set: 1RT correct source, 1RT correct source, 1RT correct source adding to 34%."]),
    steps("5.1.5", "Sanji calculated, in lakh crores, the amount spent on interest payments. He rounded off his answer to the nearest whole "
          "number.\n\nSanji stated that the rounded answer he calculated did not make much difference in rupees when compared to the non-rounded "
          "answer.\n\nVerify, showing ALL calculations, whether his statement is valid.", 6, [
        ("Interest payments (lakh crore)", 2, 9.006, 0.0005, "Interest payments = 20% × 45,03 lakh crore ✓RT (both values) = 9,006 lakh crore ✓A"),
        ("Unrounded interest payments (rupees)", 1, 90060000, 0.5, "Unrounded = 9,006 × 100 × 100 000 = 90 060 000 rupees ✓C. Also "
         "accepted: 9 006 000 000 000 rupees (by the NOTE a lakh crore is 100 000 × 10 000 000 rupees)", [9006000000000]),
        ("Interest payments rounded to the nearest whole number (lakh crore)", 1, 9, 0.01, "Rounded = 9 ✓R (9 × 100 × 100 000 = 90 000 000 rupees)"),
        ("Difference between the two amounts (rupees)", 2, 60000, 0.5, "Difference = 90 060 000 – 90 000 000 = 60 000 rupees ✓CA. His "
         "statement is NOT VALID ✓O (OR 9,006 – 9,000 = 0,006 lakh crore ✓R ✓CA; amount in rupees = 0,006 × 100 × 100 000 = 60 000 ✓C). "
         "Also accepted: 6 000 000 000 rupees (the NOTE's lakh crore)", [6000000000])],
          ["Find 20% of the 45,03 lakh crores, then round it to a whole number.", "Change both amounts to rupees with the NOTE, then compare them."])]
q52 = [
    steps("5.2.1", "Convert R302,4 billion to million rands.", 2, [
        ("Corporate income tax (R million)", 2, 302400, 0.01, "Amount expressed in million = R302,4 billion × 1 000 ✓MA = R302 400 million ✓A "
         "(OR R302 400 000 000). AO")],
          ["1 billion = 1 000 million.", "Going to a smaller unit: does the number get bigger or smaller?"]),
    steps("5.2.2", "Hence, convert the South African corporate income tax to lakh crore.", 4, [
        ("Corporate income tax in lakhs", 2, 13450719.04, 0.045, "R302 400 million = R302 400 × 44,479891 lakh ✓MA = 13 450 719,04 lakh ✓CA "
         "(CA from 5.2.1)"),
        ("Corporate income tax in lakh crore", 2, 134507.19, 0.015, "= 13 450 719,04 ÷ 100 ✓MCA = 134 507,1904 lakh crore ✓CA. NPR (OR "
         "R302 400 000 000 ÷ R1 000 000 × 4 447 989,1 ✓MA = 1,345071904 × 1 000 000 000 000 ✓CA ÷ 100 000 ÷ 100 ✓MCA = 134 507,1904 lakh "
         "crore ✓CA; OR R1 000 000 = 0,44479891 lakh crore ✓C, R302 400 000 000 × 0,44479891 ✓MA ÷ 1 000 000 ✓MCA = 134 507,1904 lakh "
         "crore ✓CA). Also accepted: 1,345071904 lakh crore (by the NOTE, 13 450 719,04 lakh ÷ 10 000 000)", [1.345071904])],
          ["Each R1 million is worth 44,479891 lakhs (the NOTE).", "Then use the NOTE in QUESTION 5.1 to go from lakhs to the larger unit."])]
INFL = {"title": "TABLE 7: INFLATION RATES IN INDIA FOR THE LAST FIVE YEARS", "head": ["YEAR", "INFLATION RATE"],
        "rows": [["2024", "8%"], ["2023", "7,5%"], ["2022", "7%"], ["2021", "6,5%"], ["2020", "6%"]]}
q53 = [
    rub("5.3.1", "Describe the trend in the inflation rates in India.", 2, [
        "As the years increase (1).", "The inflation rate increases (1).", "OR — The inflation rate increases (1).", "From 2020 to 2024 (1)."],
        ["Read TABLE 7 from 2020 up to 2024.", "Does the rate go up, go down or stay the same, and over which years?"]),
    steps("5.3.2", "Calculate how much the house was worth at the end of 2022.", 6, [
        ("Value of the house at the end of 2023 (rupees)", 3, 4629629.63, 0.035, "Price at the end of 2023 = 5 000 000 ÷ 1,08 ✓A ✓MA (OR "
         "5 000 000 ÷ 108% OR 5 000 000 × 100/108) = 4 629 629,63 rupees ✓CA"),
        ("Value of the house at the end of 2022 (rupees)", 3, 4306632.21, 0.015, "Price at end of 2022 = 4 629 629,63 rupees ÷ 1,075 ✓MCA ✓MA "
         "(OR ÷ 107,5% OR × 100/107,5) = 4 306 632,214 rupees ✓CA (OR 5 000 000 × 100/108 × 100/107,5 = 4 306 632,214 rupees). NPU. NPR")],
          ["Work backwards a year at a time: the 2024 rate takes the value back to the end of 2023.",
           "Going back one year, divide by (100% + that year's rate)."])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Voters per time slot", "marks": 11,
     "lead": "School X and School Y conducted an election for new members to serve on the school governing body (SGB). The graph below shows "
             "the number of voters voting during different time slots at School X and School Y.",
     "figure": fig("1.1", "A double bar graph, NUMBER OF VOTERS PER TIME SLOT AT SCHOOL X AND SCHOOL Y: Number of voters (0 to 35, gridlines "
                   "every 5) for eight half-hour time slots from 15:00–15:30 to 18:30–19:00; black bars for School X, patterned bars for "
                   "School Y. School X has no bar in the first two slots, then about 10 (16:00–16:30), 12 (16:30–17:00), 26 (17:00–17:30), 30 "
                   "(17:30–18:00), 18 (18:00–18:30) and 8 (18:30–19:00). School Y: about 18 (15:00–15:30), 12 (15:30–16:00), 5 (16:00–16:30), "
                   "9 (16:30–17:00), 26 (17:00–17:30), 24 (17:30–18:00), 5 (18:00–18:30) and 2 (18:30–19:00)."), "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Food prices", "marks": 10, "table": FOOD,
     "lead": "The newly elected SGB planned to have lunch with the staff.\n\nTABLE 1 below shows the average comparative food prices for May 2022 "
             "and May 2023 needed for some of the lunch items.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Financial and data terminology", "marks": 8, "table": DEFS,
     "lead": "TABLE 2 below gives definitions of terminology used in Mathematical Literacy.", "items": q13},
    {"id": "2.1", "title": "Question 2.1", "kind": "Prepaid electricity", "marks": 12, "table": TARIFF,
     "lead": "Miecke purchased prepaid electricity and received the following till slip. Note that some information has been omitted.",
     "extract": SLIP, "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Solar system payment options", "marks": 10, "table": SOLAR,
     "lead": "Miecke plans to install a home solar system unit consisting of solar panels, a battery and an inverter. She sees the advertisement "
             "below in a community newspaper showing the two different payment options for the same unit.", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Income tax", "marks": 8, "table": TAX,
     "lead": "Miecke is 45 years old and earns a monthly taxable income of R39 275,85 in the 2023/2024 tax year. She does not belong to a "
             "medical aid.\n\nANNEXURE A shows the annual tax table for individuals for the 2023/2024 tax year.", "extract": TAX_MORE, "items": q23},
    {"id": "3.1", "title": "Question 3.1", "kind": "Stores and employees", "marks": 14,
     "lead": "ANNEXURE B shows two graphs. GRAPH 1 shows the trends in the total number of Shoprite and Pick n Pay stores for the period 2014 to "
             "2023. GRAPH 2 shows the trends in the total number of employees in these two stores for the period 2005 to 2023.",
     "extract": GRAPHS, "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Time spent in a store", "marks": 7,
     "lead": "A study relating to the amount of time spent (in minutes) by a selected number of customers in a store was conducted on a particular "
             "Saturday. On that Saturday, a total of 12 342 customers visited the store.", "extract": TIMES, "items": q32},
    {"id": "3.2.4", "title": "Question 3.2.4", "kind": "Quartiles and box-and-whisker plot", "marks": 8,
     "lead": "Shown below, in rank order, is selected data of the time spent by customers in the store and an incomplete box-and-whisker plot of "
             "the same data.", "extract": RANKED,
     "figure": fig("3.2.4", "An incomplete box-and-whisker plot above a number line from 0 to 140 (marked every 20): the left whisker starts at "
                   "6 (labelled), the box starts at 15 (labelled), a line inside the box at about 23, the box's right end labelled Q3 (its value "
                   "not given), and the right whisker ends at 127 (labelled)."), "items": q324},
    {"id": "4.1", "title": "Question 4.1", "kind": "Party budget and DJ costs", "marks": 20, "table": PARTY,
     "lead": "Lee's parents plan to celebrate his 21st birthday. This special event will be held at a popular hotel, starting at 18:00.\n\nTABLE 4 "
             "below shows some of the budgeted expenses for the party.", "extract": DJ_RAIN,
     "figure": fig("4.1", "The ANSWER SHEET graph, COMPARISON OF THE COST FOR THE DIFFERENT DJs: Cost in rand (0 to 10 000, gridlines every 1 000) "
                   "against Number of hours playing (0 to 9). DJ 5-Star: a horizontal segment at each cost, from an open circle to a closed dot "
                   "one hour later: R1 000 from 0 to 1 hour, R2 000 from 1 to 2, R3 000 from 2 to 3, and so on up to R9 000 from 8 to 9 hours. "
                   "DJ Cool: a dash-dot horizontal line at R6 500 across the whole grid. DJ Rain is not drawn yet (QUESTION 4.1.2(b))."),
     "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Guests per function", "marks": 11, "table": GUESTS,
     "lead": "The hotel has three other smaller venues, each accommodating a maximum number of guests per function, as listed below:\n"
             "Cinema-style venue: 400 guests\nSit-down venue without dancing space: 250 guests\nSit-down venue with dancing space: 200 guests\n\n"
             "TABLE 6 shows the number of guests accommodated for functions at the three venues during a specific month in 2022 and 2023.",
     "items": q42},
    {"id": "5.1", "title": "Question 5.1", "kind": "Indian Union budget", "marks": 17, "table": INCOME,
     "lead": "The pie charts on ANNEXURE C show the Indian Union budgets for income and expenditure for 2023/2024. Some values have been omitted."
             "\n\nThe currency used in India is the rupee. India also has different denominations for the larger currency amounts.\n\n"
             "NOTE: 100 000 rupees = 1 lakh\n100 lakhs = 1 crore", "extract": SPEND, "items": q51},
    {"id": "5.2", "title": "Question 5.2", "kind": "Currency conversion", "marks": 6,
     "lead": "In 2024, South Africa received R302,4 billion from corporate income tax.\n\nNOTE: R1 000 000 = 4 447 989,1 rupees\n"
             "4 447 989,1 rupees = 44,479891 lakhs", "items": q52},
    {"id": "5.3", "title": "Question 5.3", "kind": "House prices and inflation", "marks": 8, "table": INFL,
     "lead": "A house in Chennai, India, is valued at 5 000 000 rupees at the end of 2024.\n\nTABLE 7 shows the inflation rates in India for house "
             "prices for the last five years.", "items": q53},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P1", "sitting": "November 2024", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematical Literacy", "total": 150, "missions": missions}],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 5), hand-transcribed from scanned page images: the question "
                                                           "paper (with its ANSWER SHEET, page 14) and the addendum (ANNEXURES A to C) have no "
                                                           "text layer; the memo's English read from its text layer and checked against its page "
                                                           "images. No API call."},
        {"n": "3.1", "kind": "no_fit", "detail": "The ANNEXURES are printed in the ADDENDUM, passed to the ingest as --answer-book: the 'answer book' "
                                                 "here is the addendum of annexures. ANNEXURE A (tax tables) is typed: the tax rates as 2.3's table, "
                                                 "the rebates, thresholds and medical credits in its extract. ANNEXURE B (two line graphs) and "
                                                 "ANNEXURE C (two pie charts) are printed SIDEWAYS on the addendum's pages 3 and 4, so a crop would "
                                                 "lie on its side (as ANNEXURE D in ML P2 Nov 2025): B is described in 3.1's extract with values read "
                                                 "off the graphs, C typed as 5.1's table (income) and extract (expenditure). No figure is cropped "
                                                 "from the addendum."},
        {"n": "3.1", "kind": "figure_unclear", "detail": "GRAPH 2 marks only 2005, 2014 and 2023 on its YEAR axis: the yearly values in 3.1's extract "
                                                         "are placed by the even spacing between those years and are approximate ('about'). The "
                                                         "Pick n Pay line's first fall lands on 2015, the memo's answer to 3.1.1; GRAPH 1's "
                                                         "Shoprite values fall below 2 000 in 2014-2016 only, the memo's 3 of 10 in 3.1.4."},
        {"n": "1.2.1", "kind": "no_fit", "detail": "The two food items play as a list of two, 1,5 marks each; the memo gives 2 for the first correct "
                                                   "item and 1 for the second."},
        {"n": "1.1.2", "kind": "no_fit", "detail": "Terms the memo marks in parts play all or nothing: 1.1.2 (start + end of the slot), 1.1.4 (fraction "
                                                   "+ simplification), 2.3.1 (the bracket: the memo's annual income R471 310,20 earns MA + A, AO "
                                                   "full marks) and 4.1.1(a) (the formula's three A marks). Each is strict, listing the forms a "
                                                   "learner types (a time slot in 24-hour, 12-hour and words; the formula with or without 'Cost =' "
                                                   "and R, n or the hours named)."},
        {"n": "2.1.3", "kind": "no_fit", "detail": "Calculations play as steps: each step is the number the memo's method produces, its RT/MA/CA/C/R "
                                                   "marks riding on that number. 'Verify' parts (3.1.3, 3.2.4(b), 4.2.3, 5.1.5) fold the memo's "
                                                   "conclusion (the O mark) into the last step. 2.1.3's steps follow the memo's first method (tariffs "
                                                   "excluding VAT); its second method (VAT-inclusive tariffs R2,5185 and R3,3465: R881,475 and "
                                                   "R418,525) reaches the same 125,06 and 475,06 kWh, but its first two numbers differ. The memo's "
                                                   "NPR widens the tolerances where it applies (1.2.3, 1.2.4, 2.1.3, 3.1.3, 5.1.3, 5.2.2, 5.3.2)."},
        {"n": "4.1.2(b)", "kind": "no_fit", "detail": "Drawing DJ Rain's line graph on the ANSWER SHEET is done on paper and self-checked against the "
                                                      "memo's criteria."},
        {"n": "5.1.4", "kind": "no_fit", "detail": "The three sources play as a rubric with the memo's three alternative sets (each adds up to the 34% "
                                                   "of borrowings); a list would credit any three of the five sources the sets name."},
        {"n": "3.2.2", "kind": "low_confidence", "detail": "The memo's answer is E (Analysing data). In CAPS the measures of central tendency and "
                                                           "spread are calculated under 'Summarising data' (C), so a reviewer may want to confirm; "
                                                           "transcribed as the memo has it."},
        {"n": "4.1", "kind": "memo_issue", "detail": "The question paper's TABLE 4 gives DJ Cool as R6 000 for the party, but the ANSWER SHEET graph (and "
                                                     "the memo's graph) draws DJ Cool at R6 500. No answer depends on it (4.1.4 asks for a reason); "
                                                     "the caption describes the graph as printed."},
        {"n": "5.1.5", "kind": "memo_issue", "detail": "The memo converts lakh crore to rupees as × 100 × 100 000 (one crore). By the paper's NOTE, "
                                                       "1 lakh crore = 100 000 crore = 1 000 000 000 000 rupees, so 9,006 lakh crore is "
                                                       "9 006 000 000 000 rupees and the difference is 6 000 000 000 rupees (not 60 000); the "
                                                       "conclusion (NOT VALID) stands. Murci, 2026-10-10: BOTH earn the rupee steps (the memo's 90 060 000 "
                                                       "and 60 000, and the NOTE's values, as each step's `also`)."},
        {"n": "5.2.2", "kind": "memo_issue", "detail": "The memo's 134 507,1904 'lakh crore' is in crore: 13 450 719,04 lakh ÷ 100 = 134 507,19 crore, "
                                                       "and its third method writes R1 000 000 = 0,44479891 lakh crore (÷ 10 000 000, one crore). "
                                                       "In lakh crore the tax is 1,345071904 (R302,4 billion = 1,345 × 10¹² rupees). Murci, "
                                                       "2026-10-10: BOTH earn the last step (134 507,19 and, as its `also`, 1,345071904)."},
    ],
}
out = Path(__file__).parent / "out" / "ml-p1-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper, addendum and memo PDFs and their page "
                                                                       "images (no API call)",
                                                        "scope": "Questions 1 to 5 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
qs = {}
for m in missions:
    qs[m["id"].split(".")[0]] = qs.get(m["id"].split(".")[0], 0) + m["marks"]
print("per question:", qs)
assert qs == {"1": 29, "2": 30, "3": 29, "4": 31, "5": 31}, qs
print("total:", sum(i["marks"] for m in missions for i in m["items"]))
