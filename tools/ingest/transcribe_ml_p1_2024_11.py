"""Mathematical Literacy P1 Nov 2024, the whole paper (Questions 1 to 5, 150 marks), hand-transcribed into the catalogue format (as
if Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, the printed options, marks,
answers and the memo's working are the paper's and the memo's own (its English); clues, figure captions and the wrong options of the
authored multiple choice are ours. No API call: the transcription is the source, kept in git (out/ is not). The question paper and its ADDENDUM are SCANS (no text layer): read from their page
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
  a read-off of a word or a code -> term (a time slot, a fraction, a meter number, a tax bracket and a formula are strict terms: one
  digit or letter changes the answer); "Choose the statement (A-C)" / "Choose the correct option (A-E)" -> mcq in the paper's order; a
  word chosen from brackets -> mcq; definitions matched to terms -> match (2 marks a pair); "Identify the food items" -> list; a reason
  or a trend (O marks) -> rubric; three sources that must add up to 34% -> rubric with the memo's three sets as alternatives; "draw a
  line graph on the ANSWER SHEET" -> draw, self-checked.
  Authored multiple choice (Murci's ruling, 2026-10-10) for every number a learner would type (a number read off, "Calculate /
  Determine / Convert", "Verify ... whether ... valid"): the stem ends "Choose the correct working"; four options, one the memo's FIRST
  method as the memo works it, a line per step ("{a}/{b}" a stacked fraction; numbers as the memo writes them, decimal comma and space
  thousands; a verify part's conclusion its last line), and three built from real errors for that calculation (a wrong operation, the
  wrong base, a unit slip, a value from the wrong row or column, rounding too early, an error that turns the conclusion), each ending
  in a confident result. Every option of a part has the same number of lines; the part keeps its marks, all or nothing. A number read
  off (1.1.1, 2.2.1, 3.1.1) shows its reading as the working: which bar, line or row, then the value. 5.1.5 and 5.2.2 follow the
  paper's NOTE, not the memo's one-crore conversion (see their memo_issue flags).
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
lst =lambda n, q, count, pool, clues, marks: {"t": "list", "n": n, "marks": marks, "q": q, "clues": clues, "count": count, "pool": pool}
match = lambda n, q, left, right, a, each, clues, **kw: {"t": "match", "n": n, "marks": len(left) * each, "q": q, "clues": clues, "left": left,
                                                         "right": right, "a": a, **({"each": each} if each > 1 else {}), **kw}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}


WORK = "\n\nChoose the correct working."   # the stem's ending on every authored multiple choice (a typed calculation, Murci 2026-10-10)


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
    mcq("1.1.1", "Write down the number of voters at School Y from 16:00–16:30." + WORK, [
        "School Y is the black bar\nAt 16:00–16:30 it reaches 10 voters",
        "School Y is the patterned bar\nAt 16:00–16:30 it reaches 5 voters",
        "School Y is the patterned bar\nAt 16:00–16:30 it reaches 9 voters",
        "Both bars at 16:00–16:30\n10 + 5 = 15 voters"], 1,
        ["School Y's bars are the patterned ones.", "Find the 16:00–16:30 slot and read its bar against the axis."], marks=2),
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
    mcq("1.1.5", "Calculate the total number of voters at both schools who voted during the 17:00–17:30 time slot." + WORK, [
        "Total number = 25 + 25\n= 50",
        "Total number = 30 + 24\n= 54",
        "Total number = 12 + 9\n= 21",
        "Total number = 26 + 26\n= 52"], 3,
        ["Read both bars in the 17:00–17:30 slot.", "Add the two schools' voters."], marks=3)]
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
    mcq("1.2.2", "Determine the missing value, A." + WORK, [
        "Value of A = R12,60 + R45,56 + R52,97 + R40,68 + R22,07 + R37,73 + R86,80\n= R298,41",
        "Value of A = R15,14 + R48,47 + R57,33 + R35,52 + R20,10 + R46,75 + R93,06\n= R316,37",
        "Value of A = R12,60 + R45,56 + R52,97 + R40,68 + R22,07 + R37,73\n= R211,61",
        "Value of A = (R12,60 + R45,56 + R52,97 + R40,68 + R22,07 + R37,73 + R86,80) ÷ 7\n= R42,63"], 0,
        ["A is the TOTAL of the May 2022 column.", "Add all seven May 2022 prices."], marks=2),
    mcq("1.2.3", "Calculate the price of a dozen eggs during May 2022." + WORK, [
        "Price per dozen = R52,97 × 1,5\n= R79,46",
        "Price per dozen = R57,33 ÷ 1,5\n= R38,22",
        "Price per dozen = R52,97 ÷ 1,5\n= R35,31",
        "Price per dozen = R52,97 ÷ 12\n= R4,41"], 2,
        ["The tray in TABLE 1 holds 1,5 dozen eggs.", "Find the price of ONE dozen from the May 2022 price."], marks=2),
    mcq("1.2.4", "Write down the unit ratio, in the form 1 : …, for the price of the oranges in May 2022 to the price of the oranges in "
        "May 2023." + WORK, [
        "Ratio = 20,10 : 22,07\n= 1 : 1,0980099502\n≈ 1 : 1,10",
        "Ratio = 22,07 : 20,10\n= 1 : 0,9107385591\n≈ 1 : 0,91",
        "Ratio = 40,68 : 35,52\n= 1 : 0,8731563422\n≈ 1 : 0,87",
        "Ratio = 37,73 : 46,75\n= 1 : 1,2390670554\n≈ 1 : 1,24"], 1,
        ["May 2022 comes first in the ratio.", "Divide both sides by the May 2022 price."], marks=3)]
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
    mcq("2.1.2", "Determine the missing value, B." + WORK, [
        "B = R1 300,00 – R1 130,43\n= R169,57",
        "B = R1 300,00 × {15}/{100}\n= R195,00",
        "B = R1 130,43 × {15}/{115}\n= R147,45",
        "B = R1 300,00 + R1 130,43\n= R2 430,43"], 0,
        ["B is the VAT on the electricity.", "The TOTAL includes the VAT."], marks=3),
    mcq("2.1.3", "A partial residential electricity tariff table (excluding VAT) is shown below.\n\nDetermine the number of kWh units Miecke "
        "purchased." + WORK, [
        "Amount for Block 1 = 350 kWh × R2,19\n= R766,50\nAmount left for Block 2 = R1 300,00 – R766,50\n= R533,50\n"
        "Units in Block 2 = {R533,50}/{R2,91}\n= 183,3333333 kWh\nTotal kWh received = 350 kWh + 183,3333333 kWh\n= 533,33 kWh",
        "Amount for Block 1 = 350 kWh × R2,91\n= R1 018,50\nAmount left for Block 2 = R1 130,43 – R1 018,50\n= R111,93\n"
        "Units in Block 2 = {R111,93}/{R2,19}\n= 51,109589 kWh\nTotal kWh received = 350 kWh + 51,109589 kWh\n= 401,11 kWh",
        "Amount for Block 1 = 350 kWh × R2,19\n= R766,50\nAmount left for Block 2 = R1 130,43 – R766,50\n= R363,93\n"
        "Units in Block 2 = R363,93 × R2,91\n= 1 059,0363 kWh\nTotal kWh received = 350 kWh + 1 059,0363 kWh\n= 1 409,04 kWh",
        "Amount for Block 1 = 350 kWh × R2,19\n= R766,50\nAmount left for Block 2 = R1 130,43 – R766,50\n= R363,93\n"
        "Units in Block 2 = {R363,93}/{R2,91}\n= 125,0618557 kWh\nTotal kWh received = 350 kWh + 125,0618557 kWh\n= 475,06 kWh"], 3,
        ["The R1 130,43 for electricity excludes VAT, like TABLE 3's tariffs.",
         "The first 350 kWh are charged at the Block 1 tariff; what is left of the money buys units at the Block 2 tariff."], marks=7)]
SOLAR = {"title": "HOME SOLAR SYSTEM UNIT PAYMENT OPTIONS", "head": ["OPTION 1: RENT-TO-OWN", "OPTION 2: CASH PRICE"],
         "rows": [["Pay for 7 years at R1 549 p/m", "R78 200 (incl. VAT)"], ["Additional costs:", ""], ["R782 initiation fee", ""],
                  ["Buy-out after rental period R7 820", ""]]}
q22 = [
    mcq("2.2.1", "Write down the monthly instalment for the rent-to-own option." + WORK, [
        "Rent-to-own: R782 initiation fee\nMonthly instalment = R782",
        "Rent-to-own: 7 years = 84 months\nMonthly instalment = R78 200 ÷ 84 = R930,95",
        "Rent-to-own: pay for 7 years at R1 549 p/m\nMonthly instalment = R1 549",
        "Rent-to-own: R1 549 a year\nMonthly instalment = R1 549 ÷ 12 = R129,08"], 2,
        ["Read OPTION 1 in the advertisement.", "p/m means per month."], marks=2),
    mcq("2.2.2", "Calculate, excluding VAT, the cash price of the home solar system unit." + WORK, [
        "Price excluding VAT = R78 200 – (15% × R78 200)\n= R66 470",
        "Price excluding VAT = {R78 200}/{1,15}\n= R68 000",
        "Price excluding VAT = R78 200 × 1,15\n= R89 930",
        "Price excluding VAT = R78 200 × {15}/{115}\n= R10 200"], 1,
        ["The cash price R78 200 includes 15% VAT.", "So R78 200 is 115% of the price without VAT."], marks=3),
    mcq("2.2.3", "After seven years, Miecke decides to buy-out the rent-to-own option.\n\nCalculate the extra amount she has to pay compared to "
        "buying the home solar system unit for cash." + WORK, [
        "Number of months = 12 × 7\n= 84 months\nRent-to-own = (R1 549 × 84) + R782 + R7 820\n= R130 116 + R782 + R7 820\n= R138 718\n"
        "Difference = R138 718 – R68 000\n= R70 718",
        "Number of months = 12 × 7\n= 84 months\nRent-to-own = (R1 549 × 84) + R7 820\n= R130 116 + R7 820\n= R137 936\n"
        "Difference = R137 936 – R78 200\n= R59 736",
        "Number of months = 12 × 7\n= 84 months\nRent-to-own = (R1 549 × 84) + R782 – R7 820\n= R130 116 + R782 – R7 820\n= R123 078\n"
        "Difference = R123 078 – R78 200\n= R44 878",
        "Number of months = 12 × 7\n= 84 months\nRent-to-own = (R1 549 × 84) + R782 + R7 820\n= R130 116 + R782 + R7 820\n= R138 718\n"
        "Difference = R138 718 – R78 200\n= R60 518"], 3,
        ["Count the monthly instalments in 7 years, then add the initiation fee and the buy-out.", "Compare the total with the cash price."],
        marks=5)]
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
    mcq("2.3.2", "Calculate Miecke's annual tax payable for the 2023/2024 tax year." + WORK, [
        "Tax before rebate = 77 362 + 31% of taxable income above 370 500\n= R77 362 + 31% (R471 310,20 – R370 500)\n"
        "= R77 362 + 31% (R100 810,20)\n= R77 362 + R31 251,162\n= R108 613,162\nAnnual tax payable = R108 613,162 – R17 235\n"
        "= R91 378,162\n= R91 378,16",
        "Tax before rebate = 42 678 + 26% of taxable income above 237 100\n= R42 678 + 26% (R471 310,20 – R237 100)\n"
        "= R42 678 + 26% (R234 210,20)\n= R42 678 + R60 894,652\n= R103 572,652\nAnnual tax payable = R103 572,652 – R17 235\n"
        "= R86 337,652\n= R86 337,65",
        "Tax before rebate = 77 362 + 31% of taxable income above 370 500\n= R77 362 + 31% (R471 310,20 – R370 500)\n"
        "= R77 362 + 31% (R100 810,20)\n= R77 362 + R31 251,162\n= R108 613,162\nAnnual tax payable = R108 613,162 + R17 235\n"
        "= R125 848,162\n= R125 848,16",
        "Tax before rebate = 77 362 + 31% of taxable income above 370 500\n= R77 362 + 31% (R471 310,20 – R370 500)\n"
        "= R77 362 + 31% (R100 810,20)\n= R77 362 + R31 251,162\n= R108 613,162\nAnnual tax payable = R108 613,162 – R17 235 – (12 × R364)\n"
        "= R87 010,162\n= R87 010,16"], 0,
        ["Use her bracket's tax rate with her annual taxable income.", "She is under 65 and has no medical aid: which rebate applies, and are there "
         "any medical credits?"], marks=5)]

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
    mcq("3.1.1", "Identify the year in which there was a decrease in the number of employees in the Pick n Pay stores for the first time."
        + WORK, [
        "Pick n Pay (the lower line) first falls between 2014 and 2015\nYear of the first decrease: 2014",
        "Pick n Pay (the upper line) first falls between 2019 and 2020\nYear of the first decrease: 2020",
        "Pick n Pay (the lower line) first falls between 2014 and 2015\nYear of the first decrease: 2015",
        "Pick n Pay (the lower line) first falls between 2015 and 2016\nYear of the first decrease: 2016"], 2,
        ["Use GRAPH 2 and follow the Pick n Pay line from 2005.", "Find the first year in which the line goes down."], marks=2),
    mcq("3.1.2", "It is projected that the number of Pick n Pay stores will increase by 95,39% from 2023 to 2032.\n\nDetermine, by means of "
        "calculations, the projected number of Pick n Pay stores in 2032." + WORK, [
        "Projected number of stores = 3 543 × {95,39}/{100} + 3 543\n= 3 379,6677 + 3 543\n= 6 922,6677\n= 6 923",
        "Projected number of stores = 1 128 × {95,39}/{100} + 1 128\n= 1 075,9992 + 1 128\n= 2 203,9992\n= 2 204",
        "Projected number of stores = 2 204 × {95,39}/{100}\n= 2 204 × 0,9539\n= 2 102,3956\n= 2 102",
        "Projected number of stores = 2 204 × {95,39}/{100} + 2 204\n= 2 102,3956 + 2 204\n= 4 306,3956\n= 4 306"], 3,
        ["Start from the number of Pick n Pay stores in 2023 (GRAPH 1).", "Add 95,39% of it to itself."], marks=3),
    mcq("3.1.3", "An analyst stated that Shoprite employed more employees per store than Pick n Pay during 2023.\n\nVerify, showing ALL "
        "calculations, whether the analyst's statement is valid." + WORK, [
        "Average Shoprite = 3 543 ÷ 153 726\n= 0,023047… employees\nAverage Pick n Pay = 2 204 ÷ 90 000\n= 0,024488… employees\n"
        "Her statement is NOT VALID",
        "Average Shoprite = 153 726 ÷ 3 543\n= 43,388653… employees\nAverage Pick n Pay = 90 000 ÷ 2 204\n= 40,834845… employees\n"
        "Her statement is VALID",
        "Average Shoprite = 90 000 ÷ 3 543\n= 25,402201… employees\nAverage Pick n Pay = 153 726 ÷ 2 204\n= 69,748638… employees\n"
        "Her statement is NOT VALID",
        "Average Shoprite = 153 726 ÷ 1 581\n= 97,233396… employees\nAverage Pick n Pay = 90 000 ÷ 1 128\n= 79,787234… employees\n"
        "Her statement is VALID"], 1,
        ["Employees per store = the number of employees ÷ the number of stores, both in 2023.", "Employees are on GRAPH 2, stores on GRAPH 1."],
        marks=6),
    mcq("3.1.4", "Determine, as a percentage, the probability of randomly selecting a year where the number of Shoprite stores is fewer than "
        "2 000." + WORK, [
        "Probability = {3}/{10} × 100%\n= 30%",
        "Probability = {7}/{10} × 100%\n= 70%",
        "Probability = {3}/{9} × 100%\n= 33,33%",
        "Probability = {3}/{10}\n= 0,3%"], 0,
        ["Use GRAPH 1: count the years in which the Shoprite line is below 2 000.", "Divide by the number of years on the graph."], marks=3)]
TIMES = "12  15  25  25  40  28  18  23\n43  15  22  19  15  8  37  9\n24  23  15  67  25  29  6  17\n15  43  23  27  33  26  127  10"
q32 = [
    mcq("3.2.1", "Write down the number of customers that represent the sample size and the number of customers that represent the population "
        "size for this study." + WORK, [
        "Sample = 12 342 customers\nPopulation = 32 customers",
        "Sample = 32 customers\nPopulation = 12 342 + 32 = 12 374 customers",
        "Sample = 32 customers\nPopulation = 12 342 customers",
        "Sample = 32 customers\nPopulation = 12 342 – 32 = 12 310 customers"], 2,
        ["Each recorded time is one customer in the sample: count them.", "The population is the whole group the sample is taken from."],
        marks=3),
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
    mcq("3.2.4(a)", "Calculate the value of the upper quartile (Q3)." + WORK, [
        "Quartile 3 = {29 + 33}/{2}\n= 31",
        "Quartile 3 = {28 + 29}/{2}\n= 28,5",
        "Quartile 3 = {27 + 28}/{2}\n= 27,5",
        "Quartile 3 = {23 + 23}/{2}\n= 23"], 1,
        ["There are 32 values: the upper quartile is the middle of the upper 16.", "With an even count, average the two middle values."], marks=3),
    mcq("3.2.4(b)", "Vuyo stated that if the outlier value was removed from the data set, the new interquartile (IQR) value would be 13.\n\n"
        "Verify Vuyo's statement, showing ALL calculations." + WORK, [
        "New Quartile 1 = 15\nNew Quartile 3 = 28,5\nIQR = Q3 – Q1\nIQR = 28,5 – 15\n= 13,5 ≈ 13\nHe is CORRECT.",
        "New Quartile 1 = 15\nNew Quartile 3 = 29\nIQR = Q3 – Q1\nIQR = 29 – 15\n= 14\nHe is NOT CORRECT.",
        "New Quartile 1 = 15\nNew Quartile 3 = 28\nIQR = Maximum – Minimum\nIQR = 67 – 6\n= 61\nHe is NOT CORRECT.",
        "New Quartile 1 = 15\nNew Quartile 3 = 28\nIQR = Q3 – Q1\nIQR = 28 – 15\n= 13\nHe is CORRECT."], 3,
        ["Without 127 there are 31 values, and the median is the 16th.", "Q1 and Q3 are the middles of the 15 values below and the 15 above the median."],
        marks=5)]

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
    mcq("4.1.1(b)", "Complete the table by calculating the missing values P, Q and R." + WORK, [
        "P = 4 000\nQ = 5 250\nR = 9 000",
        "P = 4 000\nQ = 7 500\nR = 11 250",
        "P = 4 000\nQ = 11 500\nR = 15 250",
        "P = 2 400\nQ = 5 250\nR = 9 000"], 0,
        ["Up to 5 hours the cost does not change.", "After 5 hours, use your formula from (a)."], marks=4),
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
    mcq("4.1.3", "Lee's parents decide to hire DJ 5-Star for the 21st birthday party. DJ 5-Star will provide the music entertainment from 18:00 "
        "until 01:30.\n\nDetermine the total budgeted expenses for the party." + WORK, [
        "Time = 18:00 – 01:30\n= 7 hrs 30 min\n= 7,5 hrs\nCost for DJ = 7,5 × R1 000\n= R7 500\n"
        "Total cost = R18 000 + R750 + R6 185 + R1 250 + R7 500\n= R33 685",
        "Time = 18:00 – 01:30\n= 16 hrs 30 min\n≈ 17 hrs\nCost for DJ = 17 × R1 000\n= R17 000\n"
        "Total cost = R18 000 + R750 + R6 185 + R1 250 + R17 000\n= R43 185",
        "Time = 18:00 – 01:30\n= 7 hrs 30 min\n≈ 8 hrs\nCost for DJ = 8 × R1 000\n= R8 000\n"
        "Total cost = R18 000 + R750 + R6 185 + R1 250 + R8 000\n= R34 185",
        "Time = 18:00 – 01:30\n= 7 hrs 30 min\n≈ 8 hrs\nCost for DJ = 8 × R1 000\n= R8 000\n"
        "Total cost = R18 000 + R6 185 + R1 250 + R8 000\n= R33 435"], 2,
        ["Find how long DJ 5-Star plays: 'or part thereof' counts a part of an hour as a whole hour.",
         "Add the venue (deposit and the day), the food and drinks, the cake and the DJ."], marks=5),
    rub("4.1.4", "Give ONE reason why Lee's parents did not choose DJ Cool.", 2, [
        "He charges a flat/fixed rate, which is not economical if the party ends early (2).", "OR — He has a bad reputation (2)."],
        ["Compare how DJ Cool charges with how the other two DJs charge.", "Think about a party that ends earlier than planned."], each=2)]
GUESTS = {"title": "TABLE 6: ACTUAL NUMBER OF GUESTS PER FUNCTION", "head": ["YEAR", "NUMBER OF GUESTS", "", "", "", "", "", "", "", ""],
          "rows": [["2023", "180", "350", "400", "200", "215", "90", "150", "230", "160"],
                   ["2022", "360", "160", "300", "70", "160", "200", "240", "", ""]]}
q42 = [
    mcq("4.2.1", "Write, as a decimal, the probability that a cinema-style venue was chosen as a suitable function venue for all the functions "
        "held during 2022 and 2023." + WORK, [
        "Probability = {7}/{16}\n= 0,4375",
        "Probability = {4}/{12}\n= 0,33",
        "Probability = {2}/{9}\n= 0,22",
        "Probability = {4}/{16}\n= 0,25"], 3,
        ["The cinema-style venue is needed when a function has too many guests for either sit-down venue.", "Count the functions in both years."],
        marks=3),
    mcq("4.2.2", "Determine the median number of guests accommodated during 2023." + WORK, [
        "180 ; 350 ; 400 ; 200 ; 215 ; 90 ; 150 ; 230 ; 160\nMedian = 215",
        "90 ; 150 ; 160 ; 180 ; 200 ; 215 ; 230 ; 350 ; 400\nMedian = 200",
        "90 ; 150 ; 160 ; 180 ; 200 ; 215 ; 230 ; 350 ; 400\nMedian = {200 + 215}/{2} = 207,5",
        "90 ; 150 ; 160 ; 180 ; 200 ; 215 ; 230 ; 350 ; 400\nMedian = 1 975 ÷ 9 = 219,44"], 1,
        ["Arrange the nine 2023 values in order.", "The median is the middle value."], marks=3),
    mcq("4.2.3", "The manager stated that the range of the number of guests per function during 2022, is the same as the range of the number of "
        "guests per function during 2023.\n\nVerify, showing ALL calculations, whether his statement is valid." + WORK, [
        "Range 2022 = 360 – 240\n= 120\nRange 2023 = 180 – 160\n= 20\nHis statement is NOT VALID",
        "Range 2022 = 360 – 70\n= 290 ≈ 300\nRange 2023 = 400 – 90\n= 310 ≈ 300\nHis statement is VALID",
        "Range 2022 = 360 – 70\n= 290\nRange 2023 = 400 – 90\n= 310\nHis statement is NOT VALID",
        "Range 2022 = 360 – 70\n= 290\nRange 2023 = 360 – 70\n= 290\nHis statement is VALID"], 2,
        ["Range = highest value − lowest value.", "Work out each year's range, then compare them."], marks=5)]

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
    mcq("5.1.2", "General sales tax (GST) is a tax that is similar to VAT in South Africa.\n\nCalculate the missing percentage for GST on the pie "
        "chart." + WORK, [
        "GST % = 100% – (15% + 15% + 4% + 7% + 6% + 2% + 34%)\n= 100% – 83%\n= 17%",
        "GST % = 100% – (15% + 15% + 4% + 7% + 6% + 2%)\n= 100% – 49%\n= 51%",
        "GST % = 100% – (15% + 4% + 7% + 6% + 2% + 34%)\n= 100% – 68%\n= 32%",
        "GST % = 15% + 15% + 4% + 7% + 6% + 2% + 34%\n= 49% + 34%\n= 83%"], 0,
        ["A pie chart's percentages add up to 100%.", "Add all the other income percentages first."], marks=3),
    mcq("5.1.3", "Calculate, in lakh crores, the amount spent on defence in India." + WORK, [
        "Defence = 7% × 45,03 lakh crore\n= 3,1521 lakh crore",
        "Defence = 45,03 lakh crore ÷ 8%\n= 562,875 lakh crore",
        "Defence = 0,8 × 45,03 lakh crore\n= 36,024 lakh crore",
        "Defence = 8% × 45,03 lakh crore\n= 3,6024 lakh crore"], 3,
        ["Read Defence's percentage on the expenditure pie chart.", "Take that percentage of the 45,03 lakh crores."], marks=3),
    rub("5.1.4", "List THREE sources of income shown on the pie chart where the total percentages add up to the borrowing percentage value.", 3, [
        "Corporation tax (1).", "Income tax (1).", "Customs (1).",
        "OR — Corporation tax (1).", "GST (1).", "Non-debt capital receipts (1).",
        "OR — Income tax (1).", "GST (1).", "Non-debt capital receipts (1)."],
        ["Borrowings are 34% of the income.", "Try combinations of three slices until their percentages total exactly 34%."],
        notes=["CA from 5.1.2 for GST.", "Each set: 1RT correct source, 1RT correct source, 1RT correct source adding to 34%."]),
    mcq("5.1.5", "Sanji calculated, in lakh crores, the amount spent on interest payments. He rounded off his answer to the nearest whole "
        "number.\n\nSanji stated that the rounded answer he calculated did not make much difference in rupees when compared to the non-rounded "
        "answer.\n\nVerify, showing ALL calculations, whether his statement is valid." + WORK, [
        "Interest payments = 17% × 45,03 lakh crore\n= 7,6551 lakh crore\nUnrounded = 7,6551 × 100 000 × 10 000 000\n"
        "= 7 655 100 000 000 rupees\nRounded = 8 × 100 000 × 10 000 000\n= 8 000 000 000 000 rupees\n"
        "Difference = 8 000 000 000 000 – 7 655 100 000 000\n= 344 900 000 000 rupees\nHis statement is NOT VALID",
        "Interest payments = 20% × 45,03 lakh crore\n= 9,006 lakh crore\nUnrounded = 9,006 × 100 000\n= 900 600 rupees\n"
        "Rounded = 9 × 100 000\n= 900 000 rupees\nDifference = 900 600 – 900 000\n= 600 rupees\nHis statement is VALID",
        "Interest payments = 20% × 45,03 lakh crore\n= 9,006 lakh crore\nUnrounded = 9,006 × 100 000 × 10 000 000\n"
        "= 9 006 000 000 000 rupees\nRounded = 9 × 100 000 × 10 000 000\n= 9 000 000 000 000 rupees\n"
        "Difference = 9 006 000 000 000 – 9 000 000 000 000\n= 6 000 000 000 rupees\nHis statement is NOT VALID",
        "Interest payments = 20% × 45 lakh crore\n= 9 lakh crore\nUnrounded = 9 × 100 000 × 10 000 000\n= 9 000 000 000 000 rupees\n"
        "Rounded = 9 × 100 000 × 10 000 000\n= 9 000 000 000 000 rupees\nDifference = 9 000 000 000 000 – 9 000 000 000 000\n= 0 rupees\n"
        "His statement is VALID"], 2,
        ["Find 20% of the 45,03 lakh crores, then round it to a whole number.", "Change both amounts to rupees with the NOTE, then compare them."],
        marks=6)]
q52 = [
    mcq("5.2.1", "Convert R302,4 billion to million rands." + WORK, [
        "Amount expressed in million = R302,4 billion ÷ 1 000\n= R0,3024 million",
        "Amount expressed in million = R302,4 billion × 1 000\n= R302 400 million",
        "Amount expressed in million = R302,4 billion × 1 000 000\n= R302 400 000 million",
        "Amount expressed in million = R302,4 billion × 100\n= R30 240 million"], 1,
        ["1 billion = 1 000 million.", "Going to a smaller unit: does the number get bigger or smaller?"], marks=2),
    mcq("5.2.2", "Hence, convert the South African corporate income tax to lakh crore." + WORK, [
        "R302 400 million = R302 400 × 44,479891 lakh\n= 13 450 719,04 lakh\n= 13 450 719,04 ÷ 10 000 000\n= 1,345071904 lakh crore",
        "R302 400 million = R302 400 ÷ 44,479891 lakh\n= 6 798,58 lakh\n= 6 798,58 ÷ 10 000 000\n= 0,000679858 lakh crore",
        "R302 400 million = R302 400 × 44,479891 lakh\n= 13 450 719,04 lakh\n= 13 450 719,04 ÷ 100 000\n= 134,5071904 lakh crore",
        "R302 400 million = R302 400 × 44,479891 lakh\n= 13 450 719,04 lakh\n= 13 450 719,04 × 10 000 000\n"
        "= 134 507 190 400 000 lakh crore"], 0,
        ["Each R1 million is worth 44,479891 lakhs (the NOTE).", "Then use the NOTE in QUESTION 5.1 to go from lakhs to the larger unit."],
        marks=4)]
INFL = {"title": "TABLE 7: INFLATION RATES IN INDIA FOR THE LAST FIVE YEARS", "head": ["YEAR", "INFLATION RATE"],
        "rows": [["2024", "8%"], ["2023", "7,5%"], ["2022", "7%"], ["2021", "6,5%"], ["2020", "6%"]]}
q53 = [
    rub("5.3.1", "Describe the trend in the inflation rates in India.", 2, [
        "As the years increase (1).", "The inflation rate increases (1).", "OR — The inflation rate increases (1).", "From 2020 to 2024 (1)."],
        ["Read TABLE 7 from 2020 up to 2024.", "Does the rate go up, go down or stay the same, and over which years?"]),
    mcq("5.3.2", "Calculate how much the house was worth at the end of 2022." + WORK, [
        "Price at the end of 2023 = 5 000 000 × 1,08\n= 5 400 000 rupees\nPrice at end of 2022 = 5 400 000 rupees × 1,075\n= 5 805 000 rupees",
        "Price at the end of 2023 = 5 000 000 × 0,92\n= 4 600 000 rupees\nPrice at end of 2022 = 4 600 000 rupees × 0,925\n= 4 255 000 rupees",
        "Price at the end of 2023 = 5 000 000 ÷ 1,075\n= 4 651 162,79 rupees\nPrice at end of 2022 = 4 651 162,79 rupees ÷ 1,07\n"
        "= 4 346 881,11 rupees",
        "Price at the end of 2023 = 5 000 000 ÷ 1,08\n= 4 629 629,63 rupees\nPrice at end of 2022 = 4 629 629,63 rupees ÷ 1,075\n"
        "= 4 306 632,214 rupees"], 3,
        ["Work backwards a year at a time: the 2024 rate takes the value back to the end of 2023.",
         "Going back one year, divide by (100% + that year's rate)."], marks=6)]

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

# the parts that played as typed numbers (steps or num) until Murci's ruling of 2026-10-10, now authored multiple choice
AUTHORED = [i["n"] for m in missions for i in m["items"] if i["t"] == "mcq" and i["q"].endswith(WORK)]
AUTHORED_MARKS = sum(i["marks"] for m in missions for i in m["items"] if i["n"] in AUTHORED)

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
        {"n": AUTHORED[0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every typed calculation plays as the memo's "
                                                       "working plus three built from common errors, 0 or full marks: " + ", ".join(AUTHORED) +
                                                       " (" + str(AUTHORED_MARKS) + " marks). The right option is the memo's FIRST method as the "
                                                       "memo works it (5.1.5 and 5.2.2 follow the paper's NOTE instead: see their memo_issue "
                                                       "flags); a number read off (1.1.1, 2.2.1, 3.1.1) shows its reading as the working. The "
                                                       "wrong options come from a wrong operation, the wrong base, a unit slip, a value from the "
                                                       "wrong row, column, bar or line, rounding too early, or, in a verify part (3.1.3, "
                                                       "3.2.4(b), 4.2.3, 5.1.5), an error that turns the conclusion; each ends in a confident "
                                                       "result, and every option of a part has the same number of lines."},
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
                                                       "conclusion (NOT VALID) stands. Murci, 2026-10-10: both earn. Played as authored multiple "
                                                       "choice, which has one right option: the right option follows the NOTE (9,006 × 100 000 × "
                                                       "10 000 000 = 9 006 000 000 000 rupees, a difference of 6 000 000 000 rupees, NOT VALID), and "
                                                       "the memo's one-crore working (90 060 000 and 60 000 rupees) is not among the options. The "
                                                       "steps' `also` values that credited both are gone with the steps."},
        {"n": "5.2.2", "kind": "memo_issue", "detail": "The memo's 134 507,1904 'lakh crore' is in crore: 13 450 719,04 lakh ÷ 100 = 134 507,19 crore, "
                                                       "and its third method writes R1 000 000 = 0,44479891 lakh crore (÷ 10 000 000, one crore). "
                                                       "In lakh crore the tax is 1,345071904 (R302,4 billion = 1,345 × 10¹² rupees). Murci, "
                                                       "2026-10-10: both earn. Played as authored multiple choice, which has one right option: the "
                                                       "right option follows the NOTE (13 450 719,04 lakh ÷ 10 000 000 = 1,345071904 lakh crore), "
                                                       "and the memo's one-crore working (÷ 100 = 134 507,1904) is not among the options. The "
                                                       "step's `also` value that credited both is gone with the steps."},
    ],
}
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
qs = {}
for m in missions:
    qs[m["id"].split(".")[0]] = qs.get(m["id"].split(".")[0], 0) + m["marks"]
print("per question:", qs)
assert qs == {"1": 29, "2": 30, "3": 29, "4": 31, "5": 31}, qs
total = sum(i["marks"] for m in missions for i in m["items"])
assert total == 150, total
print("total:", total)

# ---- self-checks on the authored multiple choice (rule: the layout must never point at the answer) ----
WAS_TYPED = ["1.1.1", "1.1.5", "1.2.2", "1.2.3", "1.2.4", "2.1.2", "2.1.3", "2.2.1", "2.2.2", "2.2.3", "2.3.2", "3.1.1", "3.1.2", "3.1.3",
             "3.1.4", "3.2.1", "3.2.4(a)", "3.2.4(b)", "4.1.1(b)", "4.1.3", "4.2.1", "4.2.2", "4.2.3", "5.1.2", "5.1.3", "5.1.5", "5.2.1",
             "5.2.2", "5.3.2"]   # every steps / num part before the ruling (git 434aab6)


def shape(o):
    """An option's layout: its number of lines and of [reasons] at a line's end."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


at = []
for m in missions:
    for i in m["items"]:
        assert i["t"] not in ("steps", "num"), (i["n"], "a typed calculation is left")
        if i["n"] in AUTHORED:
            o = i["opts"]
            assert len(o) == 4 and len(set(o)) == 4 and 0 <= i["a"] < 4, (i["n"], "4 distinct options and the right one among them")
            assert len({shape(x) for x in o}) == 1, (i["n"], [shape(x) for x in o])
            assert shape(o[0])[0] >= 2, (i["n"], "a working is the method, then the result: 2 lines at least")
            at.append("ABCD"[i["a"]])
assert AUTHORED == WAS_TYPED, sorted(set(AUTHORED) ^ set(WAS_TYPED))
spread = {k: at.count(k) for k in "ABCD"}
assert max(spread.values()) - min(spread.values()) <= 1, spread
for n in ("5.1.5", "5.2.2"):   # the memo's one-crore working (× 100 × 100 000, ÷ 100) is no option: the right one follows the NOTE
    o = next(i["opts"] for m in missions for i in m["items"] if i["n"] == n)
    bad = [s for s in ("× 100 × 100 000", "90 060 000", "90 000 000 rupees", "60 000 rupees", "÷ 100\n", "134 507,19") for x in o if s in x]
    assert not bad, (n, bad)
print("authored multiple choice:", len(AUTHORED), "parts,", AUTHORED_MARKS, "marks; right options:", spread)

# written only once every check above has passed, so the ingest never reads a transcription that failed one
out = Path(__file__).parent / "out" / "ml-p1-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper, addendum and memo PDFs and their page "
                                                                       "images (no API call)",
                                                        "scope": "Questions 1 to 5 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
