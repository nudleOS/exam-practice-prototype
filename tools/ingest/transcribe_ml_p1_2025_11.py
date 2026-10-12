"""Mathematical Literacy P1 Nov 2025, the whole paper (Questions 1 to 5, 150 marks), hand-transcribed into the catalogue format (as
if Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, marks, answers and the memo's
working are the paper's and the memo's own; clues and figure captions are ours. The question paper is a SCAN (no text layer): read
from its page images. ANNEXURE A (the PAYE tables), ANSWER SHEET 3.2 and ANNEXURE B (two graphs) are printed in the SPECIAL ANSWER
BOOK (downloaded from DBE, 2026-10-07): the tables are typed, the graphs cropped from the answer book (figure source "answer_book").

  python tools/ingest/transcribe_ml_p1_2025_11.py
  python tools/ingest/ingest.py "<...>/Mathematical Literacy P1 Nov 2025 Eng.pdf" "<...>/Mathematical Literacy P1 Nov 2025 MG Afr & Eng.pdf" \
      --id ml-p1-2025-11 --from-json --answer-book "<...>/Mathematical Literacy P1 Nov 2025 Answer Book Eng.pdf"

How the memo's shapes map (Mathematical Literacy):
  a calculation, a "Verify ... whether the statement is VALID" and a number read off a table (Murci, 2026-10-10) -> mcq of four whole
  workings, "Choose the correct working.": the memo's FIRST method as it works it (a line per statement, "{a}/{b}" a fraction, numbers
  the South African way, the conclusion last) and three built from real errors (a wrong operation, a wrong base, a unit slip, a wrong
  row or column, rounding too early, a wrong conclusion), each ending in a confident result, every option the same number of lines;
  the part keeps its marks, all or nothing (`work`). A value the memo also accepts in another form (R8,28; 750 million) or from
  another method or reading (5.1.3's other conversions; 5.2.2's graph reading 1,41 – 1,43) never stands as a wrong option. A word
  read-off -> term; "discrete or continuous" -> mcq; terminology matched to definitions -> match; "arrange in ascending order" -> order;
  a formula -> strict term with the forms a learner types; "complete the graph" -> draw, self-checked.
  A written answer (O / A marks: 5.1.2(a) a reason, 5.2.4 a trend) -> statements (`stmt`, Murci 2026-10-10): the memo's own points
  and clearly false ones, pick marks/each of them (the bottom block; the rubric stays as the source). No memo in this paper weighs
  two sides, so there is no sort. A part whose options show an earlier part's answer carries "after" (AFTER, the bottom block)."""
import json
import random
import re
from pathlib import Path

W, H = 595.0, 842.0
FIGS = {  # answer book pages (2x renders measured, points = px / 2 + the clip's origin)
    "3.2": [8, 48, 138, 486, 733], "5.2": [14, 48, 136, 486, 680]}


def fig(name, caption, source="answer_book"):
    p, x0, y0, x1, y1 = FIGS[name]
    return {"page": p, "bbox": [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)], "caption": caption, "source": source}


def mcq(n, q, opts, a, clues, marks=2, **kw):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a, **kw}


def rub(n, q, marks, bullets, clues, each=None):
    return {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **({"each": each} if each else {})}


term = lambda n, q, a, clues, marks=2, strict=False: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a,
                                                      **({"strict": True} if strict else {})}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}

WORKED = []   # the typed calculations played as multiple choice of whole workings (Murci, 2026-10-10): (n, marks)
REASON = re.compile(r"\[[^\[\]]+\]\s*$")   # the page draws a line's trailing "[reason]" in its own column


def work(n, q, marks, right, wrong, at, clues):
    """A typed calculation as multiple choice of whole workings. `right` is the memo's FIRST method as the memo works it; `wrong` is
    three built from real errors, each ending in a confident result; `right` sits at index `at` (spread over A-D across the paper).
    One line per statement ("\\n"), "{a}/{b}" a fraction. All or nothing: the part keeps its marks."""
    opts = wrong[:at] + [right] + wrong[at:]
    lines = {o.count("\n") + 1 for o in opts}
    reasons = {sum(bool(REASON.search(ln)) for ln in o.split("\n")) for o in opts}
    assert len(wrong) == 3 and len(set(opts)) == 4 and 0 <= at <= 3 and opts[at] == right, n
    assert len(lines) == 1 and min(lines) >= 2 and len(reasons) == 1, (n, lines, reasons)
    WORKED.append((n, marks))
    return mcq(n, q + "\n\nChoose the correct working.", opts, at, clues, marks=marks)


def pairs(*names):
    """Every way a learner writes a pair: 'A and B', 'A B' (a comma or & drops out), both orders."""
    out = []
    for a, b in names:
        for x, y in ((a, b), (b, a)):
            out += ["%s and %s" % (x, y), "%s %s" % (x, y)]
    return out


JHB = "R18,07 + R111,59 + R41,41 + R105,24 + R41,91 + R223,23 + R52,38 + R104,96 + R163,31"   # the Johannesburg column, less canned beans

# ---- QUESTION 1, the question paper pages 3-5 and the memo pages 2-4 ----
q11 = [
    term("1.1.1", "Name the city where the cost of white sugar is the highest.", ["Cape Town"],
         ["Read the White sugar row.", "Compare the three cities' prices."]),
    work("1.1.2", "Calculate the cost of carrots, per kilogram, in Johannesburg.", 2,
         "Cost per kilogram = R41,41 ÷ 5\n= R8,282", [
             "Cost per kilogram = R41,41 × 5\n= R207,05",
             "Cost per kilogram = R39,63 ÷ 5\n= R7,926",
             "Cost per kilogram = R41,41 ÷ 10\n= R4,141"], 2,
         ["The table gives the price for 5 kg.", "Divide by the number of kilograms."]),
    work("1.1.3", "Determine, as a unit ratio rounded to THREE decimal places, the price of eggs in Cape Town compared to the price of eggs in "
         "Durban in the form 1 : …", 3,
         "Ratio = 165,52 : 169,62\n= 1 : 1,025", [
             "Ratio = 169,62 : 165,52\n= 1 : 0,976",
             "Ratio = 163,31 : 169,62\n= 1 : 1,039",
             "Ratio = 165,52 : 163,31\n= 1 : 0,987"], 0,
         ["Cape Town comes first in the ratio.", "Divide both sides by the Cape Town price."]),
    work("1.1.4", "Calculate the total price of ALL the food items in Johannesburg.", 2,
         "Total price = " + JHB + " + R101,94\n= R964,04", [
             "Total price = " + JHB + "\n= R862,10",
             "Total price = R17,16 + R100,58 + R39,63 + R90,04 + R34,24 + R197,07 + R54,73 + R78,80 + R169,62 + R84,46\n= R866,33",
             "Total price = (" + JHB + " + R101,94) ÷ 10\n= R96,40"], 3,
         ["Add the whole Johannesburg column.", "Ten items."])]
TERMS = ["Identification of the type of data", "Sum of money that is loaned by a bank or moneylender",
         "Goods and products, such as furniture, that can be purchased using a longer-term lease or agreement",
         "Interest charged on an amount due, inclusive of interest charges to date",
         "A bank product that allows you to buy goods and partially pay for them at the end of the month",
         "An arrangement whereby you give permission to a third party to withdraw money from your bank account on a regular basis",
         "Complete a frequency table using raw data", "Interest charged on the principal amount, resulting in the same interest amount every time"]
q12 = [
    {"t": "match", "n": "1.2", "marks": 8, "q": "Match the definitions in TABLE 2 with the terminology below (1.2.1 Compound interest, 1.2.2 "
     "Hire-purchase, 1.2.3 Debit order, 1.2.4 Organising data).", "clues": ["Compound interest grows on interest already added.",
                                                                             "Hire-purchase is buying over time; a debit order is a standing permission."],
     "left": ["1.2.1 Compound interest", "1.2.2 Hire-purchase", "1.2.3 Debit order", "1.2.4 Organising data"], "right": TERMS, "a": [3, 2, 5, 6],
     "each": 2, "heads": ["TERMINOLOGY", "DEFINITION (A–H)"]}]
q13 = [
    term("1.3.1", "Write down the population group with the lowest number of females.", ["Indian/Asian", "Indian", "Asian", "Indian or Asian"],
         ["Read the NUMBER OF FEMALES column.", "Find the smallest number."]),
    mcq("1.3.2", "State whether the total number of people in the table above represents discrete data or continuous data.",
        ["Discrete data", "Continuous data"], 0, ["People are counted, not measured.", "Can you have half a person?"]),
    term("1.3.3", "Name the type of instrument used to collect the data above.", ["Questionnaire", "Survey", "Census", "Interview"],
         ["Stats SA collects population data from households.", "Think of the national count every few years."]),
    work("1.3.4", "Identify the total number of the South African population for 2022.", 2,
         "TOTAL row, NUMBER OF PEOPLE (TOTAL) column\n= 60 604 992", [
             "TOTAL row, NUMBER OF FEMALES column\n= 30 980 110",
             "5 339 919 + 1 554 996 + 4 639 268, the NUMBER OF PEOPLE (TOTAL) column\n= 11 534 183",
             "TOTAL row, NUMBER OF MALES column\n= 29 624 882"], 1,
         ["The population counts everyone: every group, males and females.", "The table has already added the groups up for you."]),
    work("1.3.5", "The total number of black South Africans is forty-nine million seventy thousand eight hundred and nine. Write this number in "
         "numerals without using words.", 2,
         "49 000 000 + 70 000 + 809\n= 49 070 809", [
             "49 000 000 + 700 000 + 809\n= 49 700 809",
             "49 000 000 + 7 000 + 809\n= 49 007 809",
             "4 900 000 + 70 000 + 809\n= 4 970 809"], 1,
         ["Split the words into millions, thousands and the rest, then write each part in digits.",
          "Every group after the millions has three digits: fill an empty place with 0."]),
    work("1.3.6", "Express the number of white males as a percentage of the total number of males.", 3,
         "Percentage = {2 242 589}/{29 624 882} × 100%\n= 7,569950827%", [
             "Percentage = {2 242 589}/{4 639 268} × 100%\n= 48,339285422%",
             "Percentage = {2 396 679}/{29 624 882} × 100%\n= 8,090087920%",
             "Percentage = {2 242 589}/{60 604 992} × 100%\n= 3,700337094%"], 3,
         ["White males ÷ total males.", "Multiply by 100%."])]
SLIP = ("INTERNATIONAL COMPUTER SPECIALISTS PTY LTD — salary slip (extract)\nEMPLOYEE NAME: M DAVIDS   AGE: 42 YEARS\nPAYMENTS: GROSS SALARY "
        "R35 000\nEMPLOYEE DEDUCTIONS: UIF R177,12; PAYE TAX A; MEDICAL AID R2 531,54; NET SALARY B\nEMPLOYER CONTRIBUTIONS: UIF R177,12; "
        "MEDICAL AID …\n\nMuriel does not contribute to a pension fund; hence her gross salary is her taxable income. She pays the medical aid for "
        "herself only and receives no bonus.\n\nANNEXURE A (from the ANSWER BOOK): the monthly PAYE deduction table (in the table) and the annual "
        "tax rates for the 2024/2025 tax year:\nTAX RATES — bracket 1: 0–237 100, 18% of taxable income; 2: 237 101–370 500, 42 678 + 26% of "
        "taxable income above 237 100; 3: 370 501–512 800, 77 362 + 31% of taxable income above 370 500; 4: 512 801–673 000, 121 475 + 36% of "
        "taxable income above 512 800; 5: 673 001–857 900, 179 147 + 39% of taxable income above 673 000; 6: 857 901–1 817 000, 251 258 + 41% "
        "of taxable income above 857 900; 7: 1 817 001 and more, 644 489 + 45% of taxable income above 1 817 000.\nREBATES AND TAX THRESHOLD "
        "2024/2025 — below age 65: rebate R17 235, threshold R95 750; age 65–74: R9 444, R148 217; age 75 and over: R3 145, R165 689.\nMEDICAL "
        "TAX CREDITS PER MONTH FOR 2024/2025 — taxpayer R364; taxpayer and one dependent R728; each additional dependent R246.")
PAYE = {"head": ["MONTHLY REMUNERATION", "ANNUAL EQUIVALENT", "TAX: BELOW 65", "TAX: 65–74", "TAX: 75+"],
        "rows": [["R32 250–R32 350", "R387 600", "R5 452", "R4 665", "R4 403"], ["…", "…", "…", "…", "…"],
                 ["R34 775–R34 875", "R417 900", "R6 235", "R5 448", "R5 186"], ["…", "…", "…", "…", "…"],
                 ["R34 977–R35 077", "R420 324", "R6 298", "R5 511", "R5 249"]]}

# ---- QUESTION 2, the question paper pages 6-7, the answer book page 4 and the memo pages 5-10 ----
TAX = "Annual taxable income = R35 000 × 12\n= R420 000\nAnnual tax before rebates = "   # 2.1.4(c): every working's first lines
q21 = [
    term("2.1.1", "Write the acronym UIF in words.", ["Unemployment Insurance Fund"],
         ["It pays out when you lose your job.", "You and your employer each pay 1% of your salary into it."]),
    term("2.1.2", "Name the institution that collects tax on behalf of the government of South Africa.",
         ["SARS", "South African Revenue Service", "South African Revenue Services"],
         ["Employers pay the PAYE they deduct from salaries over to it.", "It also collects VAT from businesses."]),
    work("2.1.3", "Determine the employer contribution towards the medical aid if the employer contributes one third of the total contribution.", 2,
         "Employer medical aid contribution = R2 531,54 ÷ 2\n= R1 265,77", [
             "Employer medical aid contribution = R2 531,54 ÷ 3\n= R843,85",
             "Employer medical aid contribution = R2 531,54 × {3}/{2}\n= R3 797,31",
             "Employer medical aid contribution = R2 531,54 × 2\n= R5 063,08"], 0,
         ["If the employer pays one third, Muriel pays the other two thirds.", "Muriel's two thirds is R2 531,54: find one third."]),
    work("2.1.4(a)", "Write down the missing value A from the monthly PAYE deduction table in ANNEXURE A.", 2,
         "Row R34 977–R35 077, column Below 65\nA = R6 298", [
             "Row R34 977–R35 077, column 65–74\nA = R5 511",
             "Row R34 775–R34 875, column Below 65\nA = R6 235",
             "Row R34 977–R35 077, column 75+\nA = R5 249"], 2,
         ["Find the row her R35 000 falls in.", "Her age decides the column."]),
    work("2.1.4(b)", "Calculate the missing value B.", 2,
         "B = R35 000 – R177,12 – R6 298 – R2 531,54\n= R25 993,34", [
             "B = R35 000 – R6 298 – R2 531,54\n= R26 170,46",
             "B = R35 000 – R177,12 – R177,12 – R6 298 – R2 531,54\n= R25 816,22",
             "B = R35 000 – R177,12 – R6 235 – R2 531,54\n= R26 056,34"], 0,
         ["Net = gross minus every employee deduction.", "UIF, PAYE and medical aid."]),
    work("2.1.4(c)", "Muriel stated that she overpaid tax in the 2024/2025 tax year. Verify, showing ALL calculations, whether her statement is VALID.", 8,
         TAX + "R77 362 + 31% (R420 000 – R370 500)\n= R77 362 + R15 345\n= R92 707,00\n"
         "Annual tax after rebates = R92 707,00 – R17 235 – (R364 × 12)\n= R92 707,00 – R17 235 – R4 368\n= R71 104,00\n"
         "Monthly tax payable = R71 104,00 ÷ 12\n= R5 925,33\nR5 925,33 < R6 298 deducted: her statement is VALID", [
             TAX + "R77 362 + 31% × R420 000\n= R77 362 + R130 200\n= R207 562,00\n"
             "Annual tax after rebates = R207 562,00 – R17 235 – (R364 × 12)\n= R207 562,00 – R17 235 – R4 368\n= R185 959,00\n"
             "Monthly tax payable = R185 959,00 ÷ 12\n= R15 496,58\nR15 496,58 > R6 298 deducted: her statement is NOT VALID",
             TAX + "R77 362 + 31% (R420 000 – R370 500)\n= R77 362 + R15 345\n= R92 707,00\n"
             "Annual tax after rebates = R92 707,00 – R17 235 – R364\n= R92 707,00 – R17 599\n= R75 108,00\n"
             "Monthly tax payable = R75 108,00 ÷ 12\n= R6 259,00\nR6 259,00 < R6 298 deducted: her statement is VALID",
             TAX + "R77 362 + 31% (R420 000 – R370 500)\n= R77 362 + R15 345\n= R92 707,00\n"
             "Annual tax after rebates = R92 707,00 – R9 444 – (R364 × 12)\n= R92 707,00 – R9 444 – R4 368\n= R78 895,00\n"
             "Monthly tax payable = R78 895,00 ÷ 12\n= R6 574,58\nR6 574,58 > R6 298 deducted: her statement is NOT VALID"], 2,
         ["Find her annual tax with the tax rates, then subtract the rebate and 12 months of medical tax credits.",
          "Compare what she should pay with the R6 298 deducted each month."])]
METRO = {"head": ["TRIP PACKAGE", "DURATION", "ADULTS (15–59)", "CHILDREN (3–14)", "PENSIONERS (60+)"],
         "rows": [["1 trip", "Daily", "R14,20", "R10,30", "R4,20"], ["10 trips", "Weekly", "R106,00", "R76,40", "-"],
                  ["12 trips", "Weekly", "R127,10", "-", "-"], ["44 trips", "Monthly", "R465,60", "R336,30", "-"]]}
LEFT = "Package amount left = R416,30 – R35,00\n= R381,30\nNumber of weekly trips = "   # 2.2.4
q22 = [
    work("2.2.1", "Calculate the percentage savings a pensioner receives per bus trip when compared to the amount paid by an adult for the same bus trip.", 3,
         "% paid = {R4,20}/{R14,20} × 100%\n= 29,58%\n% savings = 100% – 29,58%\n= 70,42%", [
             "Saving = R14,20 – R4,20\n= R10,00\n% savings = {R10,00}/{R4,20} × 100%\n= 238,10%",
             "% paid = {R4,20}/{R10,30} × 100%\n= 40,78%\n% savings = 100% – 40,78%\n= 59,22%",
             "% paid = {R4,20}/{R14,20} × 100%\n= 0,3 × 100% = 30%\n% savings = 100% – 30%\n= 70%"], 1,
         ["Compare the 1-trip fares: R4,20 and R14,20.", "The saving is the part of the adult fare the pensioner does not pay."]),
    work("2.2.2", "Determine the amount Muriel will save per trip if she buys the monthly package instead of the daily trip package.", 5,
         "Cost per trip = {R465,60}/{44}\n= R10,58\nSaving per trip = R14,20 – R10,58\n= R3,62", [
             "Cost per trip = {R336,30}/{44}\n= R7,64\nSaving per trip = R14,20 – R7,64\n= R6,56",
             "Total cost = R14,20 × 44\n= R624,80\nSaving per trip = R624,80 – R465,60\n= R159,20",
             "Cost per trip = {R106,00}/{10}\n= R10,60\nSaving per trip = R14,20 – R10,60\n= R3,60"], 3,
         ["Muriel is an adult.", "Find the cost of one trip in the 44-trip package, then compare with R14,20."]),
    term("2.2.3", "Write down the probability of a 10-year old child purchasing a weekly package with 12 trips.",
         ["0", "0%", "Impossible", "0/4", "0/3", "Nil"], ["Look at the Children column for 12 trips.", "Can it happen at all?"]),
    work("2.2.4", "Johannesburg Metrobus introduced a compulsory card payment system. All passengers will be required to purchase the Metrobus card for R35 "
         "to activate the card. They will then have to upload trip fares according to the different available trip packages. Muriel purchased a "
         "Metrobus card together with an uploaded trip package to the total value of R416,30. Calculate the maximum number of weekly trips Muriel can "
         "take using this card.", 4,
         LEFT + "R381,30 ÷ R127,10\n= 3", [
             LEFT + "R381,30 ÷ R14,20\n= 26",
             "Cost per package with the card = R127,10 + R35,00\n= R162,10\nNumber of weekly trips = R416,30 ÷ R162,10\n= 2",
             LEFT + "R381,30 ÷ R76,40\n= 4"], 3,
         ["Take off the card's R35 first.", "Muriel is an adult: which weekly package fits the rest exactly?"])]

# ---- QUESTION 3, the question paper pages 8-9, the answer book page 8 and the memo pages 11-14 ----
SOCIAL = {"head": ["SOCIAL MEDIA PLATFORM", "PERCENTAGE MALE USERS", "MALE USERS (in millions)", "PERCENTAGE FEMALE USERS", "FEMALE USERS (in millions)"],
          "rows": [["Facebook", "57%", "1 732,8", "43%", "1 307,2"], ["Instagram", "51%", "1 020", "49%", "980"], ["Snapchat", "46%", "***", "54%", "405"],
                   ["X/Twitter", "56%", "346,64", "44%", "272,36"], ["TikTok", "43%", "645", "57%", "855"], ["YouTube", "54%", "1 350", "46%", "1 150"]]}
MALES = "Male users = 750 000 000 × {46}/{100}\n= 345 000 000\nDifference = 405 000 000 – 345 000 000\n= 60 000 000\n"   # 3.1.3(b)
q31 = [
    work("3.1.1", "Calculate the median percentage for male social media users.", 4,
         "Median = 43%; 46%; 51%; 54%; 56%; 57%\n= {51% + 54%}/{2}\n= 52,5%", [
             "Median = 57%; 51%; 46%; 56%; 43%; 54%\n= {46% + 56%}/{2}\n= 51%",
             "Median = 43%; 46%; 51%; 54%; 56%; 57%\n= {43% + 46% + 51% + 54% + 56% + 57%}/{6}\n= 51,17%",
             "Median = 43%; 44%; 46%; 49%; 54%; 57%\n= {46% + 49%}/{2}\n= 47,5%"], 1,
         ["Arrange the six male percentages in order.", "With an even count, the median is the mean of the middle two."]),
    work("3.1.2", "Determine, as a decimal, the probability of randomly selecting a social media platform where the female users were fewer than the male users.", 3,
         "Probability = {4}/{6}\n= 0,67", [
             "Probability = {2}/{6}\n= 0,33",
             "Probability = {4}/{2}\n= 2,00",
             "Probability = {4}/{5}\n= 0,80"], 2,
         ["Count the platforms with fewer female than male users.", "Out of six platforms."]),
    work("3.1.3(a)", "Fezeka is interested in the number of male and female Snapchat users. Determine the total number of Snapchat users.", 2,
         "Total number of users = 405 000 000 × {100}/{54}\n= 750 000 000", [
             "Total number of users = 405 000 000 × {100}/{46}\n= 880 434 783",
             "Total number of users = 405 000 000 + {46}/{100} × 405 000 000\n= 591 300 000",
             "Total number of users = 405 000 000 × {54}/{100}\n= 218 700 000"], 0,
         ["405 million females are 54% of all Snapchat users.", "Divide by 54%."]),
    work("3.1.3(b)", "Fezeka stated that the difference between the number of female and male Snapchat users was 61 300 000. Verify, showing ALL "
         "calculations, whether her statement is VALID.", 4,
         MALES + "60 000 000 ≠ 61 300 000: her statement is NOT VALID", [
             "Male users = 405 000 000 × {46}/{100}\n= 186 300 000\nDifference = 405 000 000 – 186 300 000\n= 218 700 000\n"
             "218 700 000 ≠ 61 300 000: her statement is NOT VALID",
             MALES + "60 000 000 ≈ 61 300 000: her statement is VALID",
             "Percentage difference = 54% – 46%\n= 8%\nDifference = 8% × 405 000 000\n= 32 400 000\n32 400 000 ≠ 61 300 000: her statement is NOT VALID"], 1,
         ["Males are 46% of the total from 3.1.3(a).", "Compare your difference with 61,3 million."])]
LTE = {"head": ["PROVINCE", "NUMBER OF LTE DEVICES DURING 2023"], "rows": [["KwaZulu-Natal", "11 000 000"], ["Mpumalanga", "5 500 000"]]}
RANGE = "Range = Highest value – Lowest value\nRange = "   # 3.2.2(c)
q32 = [
    term("3.2.1", "Name the type of graph drawn on ANSWER SHEET 3.2.", ["Stacked bar graph", "Compound bar graph", "Stacked bar chart",
                                                                        "Compound bar chart", "Stacked bar", "Compound bar"],
         ["Look at how each bar is built from the three years in the key.", "Its name has two words before \"graph\"."]),
    term("3.2.2(a)", "Use the graph on ANSWER SHEET 3.2: write down the names of TWO provinces that had the same number of LTE devices during 2021.",
         pairs(("Limpopo", "North West"), ("Mpumalanga", "Eastern Cape"), ("LP", "NW"), ("MP", "EC")),
         ["Read only the hatched (2021) part of each bar.", "Find two bars whose 2021 parts end at the same height."]),
    work("3.2.2(b)", "Use the graph on ANSWER SHEET 3.2: determine the number of LTE devices in Limpopo during 2022.", 3,
         "Number of devices in Limpopo 2022 = 11 000 000 – 4 000 000\n= 7 000 000", [
             "Number of devices in Limpopo 2022 = 18 500 000 – 11 000 000\n= 7 500 000",
             "Number of devices in Limpopo 2022 = 8 000 000 – 4 000 000\n= 4 000 000",
             "Number of devices in Limpopo 2022 = 11 000 000 + 4 000 000\n= 15 000 000"], 0,
         ["The white (2022) part of Limpopo's bar.", "Its top minus its bottom."]),
    work("3.2.2(c)", "Use the graph on ANSWER SHEET 3.2: calculate the range of LTE devices in the provinces during 2021.", 4,
         RANGE + "16 000 000 – 1 000 000\n= 15 000 000", [
             RANGE + "16 000 000 – 2 000 000\n= 14 000 000",
             RANGE + "56 000 000 – 4 500 000\n= 51 500 000",
             RANGE + "34 500 000 – 3 000 000\n= 31 500 000"], 3,
         ["Range = highest − lowest.", "Use the 2021 (hatched) parts only."]),
    # BUILT (2026-10-11, the bar graph builder `hist` completing a stacked bar): the two bars the graph leaves without their 2023 part,
    # each drawn with its printed 2021 (hatched) and 2022 (white) parts on the answer sheet's scale (to 60 000 000, a line every 1 000 000;
    # the full graph is the figure above); the learner drags each bar's new part up from its 2022 top (snapping to 500 000) and chooses its
    # shading from the key. The memo's four marks (memo page 14), bar by bar: the end point (1: exactly the memo's) and the complete
    # stacked bar (1: the new part drawn in the 2023 shading, black)
    {**draw("3.2.3", "The data in the table represents the number of LTE devices for two provinces during 2023 that has been omitted in the graph. Use the "
            "data to complete the graph on ANSWER SHEET 3.2.", 4, [
        ["KwaZulu-Natal end point: 31 500 000", 1], ["KwaZulu-Natal: complete stacked bar graph (the 2023 part in its shading)", 1],
        ["Mpumalanga end point: 14 000 000", 1], ["Mpumalanga: complete stacked bar graph (the 2023 part in its shading)", 1]],
        ["Stack 2023 on top of each bar's 2022 part.", "KwaZulu-Natal's bar ends at 20 500 000 now; Mpumalanga's at 8 500 000."]),
     "build": {"kind": "hist", "want": "bar", "use": ["Plot"], "groups": ["KwaZulu-Natal", "Mpumalanga"], "answers": [31500000, 14000000], "tol": 0,
               "top": 60000000, "step": 10000000, "minor": 1000000, "snap": 500000, "axes": ["Province", "Number of LTE devices"],
               "stack": {"base": [[9000000, 20500000], [3500000, 8500000]], "series": ["2021", "2022", "2023"], "fill": ["hatch", "white", "black"], "want": 2}}},
    work("3.2.4", "Determine, as a fraction, the probability of randomly selecting a province that has a total number of LTE devices less than 8 million "
         "for the three-year period.", 2,
         "Free State (7 500 000) and Northern Cape (4 500 000): 2 of the 9 provinces\nProbability = {2}/{9}", [
             "The other 7 provinces are 8 000 000 or more: 7 of the 9 provinces\nProbability = {7}/{9}",
             "Free State (7 500 000) and Northern Cape (4 500 000): 2, against the other 7 provinces\nProbability = {2}/{7}",
             "Northern Cape (4 500 000) only, Free State read as 8 000 000: 1 of the 9 provinces\nProbability = {1}/{9}"], 2,
         ["Count the bars whose whole height is below 8 000 000.", "Out of nine provinces."])]

# ---- QUESTION 4, the question paper pages 10-11 and the memo pages 15-18 ----
TRAILERS = {"head": ["Number of days (n)", "1", "3", "5", "7", "10", "15"],
            "rows": [["Cost for small trailer", "R1 350", "R2 050", "B", "R3 450", "R4 500", "R6 250"],
                     ["Cost for large trailer", "R1 500", "R2 500", "R3 500", "R4 500", "R6 000", "R8 500"]]}
INCOME = "Income for both trailers = (R1 350 × 2) + (R1 500 × 6)\n= R2 700 + R9 000\n= R11 700\nTotal income after refund = R11 700 – "   # 4.1.3(a)
q41 = [
    term("4.1.1", "Write down a formula to calculate the rental cost, including the deposit, of a large trailer in the form: Cost = …", [
        "Cost = R1 000 + (R500 × n)", "Cost = R1 000 + (R500 × number of days)", "Cost = 1000 + 500n", "Cost = R1000 + R500n", "Cost = 1000 + 500 x n",
        "Cost = 500n + 1000", "Cost = R500n + R1000", "Cost = 500 x n + 1000", "Cost = 1000 + 500 x number of days", "C = 1000 + 500n",
        "1000 + 500n", "500n + 1000", "1000 + 500 x n"],
         ["A fixed deposit plus a cost for every day.", "Test your formula with TABLE 6: one day must give R1 500."], strict=True),
    work("4.1.2", "Calculate the missing value B.", 3,
         "B = R1 000 + (R350 × 5)\n= R2 750", [
             "B = R1 000 + (R500 × 5)\n= R3 500",
             "B = (R1 000 + R350) × 5\n= R6 750",
             "B = R350 × 5\n= R1 750"], 2,
         ["B is the small trailer for 5 days.", "Deposit plus R350 per day."]),
    work("4.1.3(a)", "On 12 December 2024, Monwabisi rented out TWO small trailers and SIX large trailers to different customers for a day. One of the "
         "trailers was returned with a damaged rear light. Monwabisi stated that his total income, after refunding the deposit, amounted to R4 550. "
         "Verify, showing ALL calculations, whether his statement is VALID.", 6,
         INCOME + "R7 000\n= R4 700\nR4 700 ≠ R4 550: the statement is NOT VALID", [
             INCOME + "R8 000\n= R3 700\nR3 700 ≠ R4 550: the statement is NOT VALID",
             "Income for both trailers = (R1 350 × 6) + (R1 500 × 2)\n= R8 100 + R3 000\n= R11 100\nTotal income after refund = R11 100 – R7 000\n"
             "= R4 100\nR4 100 ≠ R4 550: the statement is NOT VALID",
             INCOME + "R1 000\n= R10 700\nR10 700 ≠ R4 550: the statement is NOT VALID"], 3,
         ["Seven deposits go back; the damaged trailer's deposit is kept.", "Compare your income with R4 550."]),
    work("4.1.3(b)", "The following quotation for the repair and replacement of the rear light was received: new rear light: R242; labour at R480 per hour "
         "or part thereof; time required to complete the repair and replacement is 1 hour 30 minutes. Verify, showing ALL calculations, whether the "
         "deposit amount will be sufficient to cover the total cost of the entire repair and replacement.", 4,
         "Labour cost = R480 × 2\n= R960\nTotal cost = R960 + R242\n= R1 202\nR1 202 > R1 000: the deposit of R1 000 will not be sufficient", [
             "Labour cost = R480 × 1,3\n= R624\nTotal cost = R624 + R242\n= R866\nR866 < R1 000: the deposit of R1 000 will be sufficient",
             "Labour cost = R480 × 3\n= R1 440\nTotal cost = R1 440 + R242\n= R1 682\nR1 682 > R1 000: the deposit of R1 000 will not be sufficient",
             "Labour cost = R480 × 1,5\n= R720\nTotal cost = R720 + R242\n= R962\nR962 < R1 000: the deposit of R1 000 will be sufficient"], 0,
         ["'Or part thereof': half an hour is charged as a full hour.", "Add the light, then compare with R1 000."])]
VAT = {"head": ["ECONOMIC SECTOR", "NUMBER OF VENDORS", "VAT PAYMENTS (R million)", "AVERAGE PAYMENT PER VENDOR (R million)"],
       "rows": [["Financial", "197 178", "221 322", "1,12245"], ["Manufacturing", "46 901", "73 893", "1,57548"],
                ["Wholesale and retail trade", "86 610", "76 826", "0,88703"], ["Construction", "39 279", "25 593", "V"],
                ["Transport", "15 258", "29 418", "1,92804"], ["Community and social", "33 825", "32 458", "0,95959"], ["Utilities", "2 658", "22 141", "8,32995"]]}
PAYS = "221 322 + 73 893 + 76 826 + 25 593 + 29 418 + 32 458 + 22 141"   # 4.2.3: the VAT PAYMENTS column
q42 = [
    work("4.2.1", "Determine, rounded to the nearest thousand, the missing value V.", 3,
         "V = 25 593 ÷ 39 279\n= 0,651569541\n= 0,652", [
             "V = 39 279 ÷ 25 593\n= 1,534755597\n= 1,535",
             "V = 25 593 ÷ 15 258\n= 1,677349587\n= 1,677",
             "V = 76 826 ÷ 39 279\n= 1,955905191\n= 1,956"], 1,
         ["Average payment per vendor = VAT payments ÷ number of vendors.", "Round to three decimal places."]),
    term("4.2.2", "Write down the sector that has the third largest number of vendors.", ["Manufacturing"],
         ["Order the NUMBER OF VENDORS column from the largest.", "Count down three."]),
    work("4.2.3", "Calculate (in R million) the mean VAT payment amount per economic sector.", 3,
         "Mean = {" + PAYS + "}/{7}\n= {481 651}/{7}\n= 68 807,29", [
             "Mean = {" + PAYS + "}/{6}\n= {481 651}/{6}\n= 80 275,17",
             "Mean = the middle value of 22 141; 25 593; 29 418; 32 458; 73 893; 76 826; 221 322\n= the 4th value\n= 32 458",
             "Mean = {197 178 + 46 901 + 86 610 + 39 279 + 15 258 + 33 825 + 2 658}/{7}\n= {421 709}/{7}\n= 60 244,14"], 3,
         ["Add all seven VAT payments.", "Divide by the number of sectors."]),
    {"t": "order", "n": "4.2.4(a)", "marks": 2, "q": "Arrange the number of vendors in ascending order.",
     "clues": ["Smallest first.", "Seven values."], "opts": ["197 178", "46 901", "86 610", "39 279", "15 258", "33 825", "2 658"], "a": [6, 4, 5, 3, 1, 2, 0]},
    work("4.2.4(b)", "The value of quartile 3 (Q3) for the number of vendors is 86 610. Calculate the interquartile range (IQR) for the number of vendors. "
         "You may use the formula: Interquartile range (IQR) = Q3 – Q1.", 3,
         "IQR = Q3 – Q1\n2 658; 15 258; 33 825; 39 279; 46 901; 86 610; 197 178\nQ1 = 15 258\nIQR = 86 610 – 15 258\nIQR = 71 352", [
             "IQR = Q3 – Q1\n197 178; 46 901; 86 610; 39 279; 15 258; 33 825; 2 658\nQ1 = 46 901\nIQR = 86 610 – 46 901\nIQR = 39 709",
             "IQR = Q3 – Q1\n2 658; 15 258; 33 825; 39 279; 46 901; 86 610; 197 178\nQ1 = 39 279\nIQR = 86 610 – 39 279\nIQR = 47 331",
             "IQR = Q3 – Q1\n2 658; 15 258; 33 825; 39 279; 46 901; 86 610; 197 178\nQ1 = 2 658\nIQR = 86 610 – 2 658\nIQR = 83 952"], 2,
         ["Q1 is the middle of the lower half.", "IQR = Q3 − Q1."])]

# ---- QUESTION 5, the question paper pages 12-13, the answer book page 14 and the memo pages 19-23 ----
CARS = {"head": ["DETAILS", "OPTION A", "OPTION B"],
        "rows": [["Payment period", "48 months", "48 months"], ["Deposit and first-month instalment", "£1 173,66", "£1 640,61"],
                 ["Additional months' instalment", "£195,61", "£182,29"], ["Compulsory monthly maintenance cover", "£25,36", "£24,00"]]}
EXCL = "Total price excluding VAT = £1 173,66 + (£195,61 × 47) + (£25,36 × 48)\n= £1 173,66 + £9 193,67 + £1 217,28\n= £11 584,61 excl VAT\n"   # 5.1.2(b)
DEP = "Deposit and first-month instalment = £1 173,66\nAmount in rand = "   # 5.1.3
q51 = [
    work("5.1.1", "Calculate the total maintenance cover for the payment period for OPTION B.", 2,
         "Total maintenance cover for option B = £24 × 48\n= £1 152", [
             "Total maintenance cover for option B = £24 × 47\n= £1 128",
             "Total maintenance cover for option B = £25,36 × 48\n= £1 217,28",
             "Total maintenance cover for option B = £24 × 4\n= £96"], 1,
         ["Option B's monthly maintenance cover.", "For every month of the payment period."]),
    rub("5.1.2(a)", "Candice chooses OPTION A. Give ONE possible reason why Candice chose OPTION A.", 2, [
        "The deposit and first-month instalment is much lower (2).", "OR — Option A has a smaller deposit (2)."],
        ["Compare the two options row by row in TABLE 8.", "What would a new small business need?"], each=2),
    work("5.1.2(b)", "Candice chooses OPTION A. Calculate the total amount, including VAT, that she would have paid at the end of the payment period.", 7,
         EXCL + "Total price including VAT = £11 584,61 × {120}/{100}\n= £13 901,53", [
             "Total price excluding VAT = £1 173,66 + (£195,61 × 48) + (£25,36 × 48)\n= £1 173,66 + £9 389,28 + £1 217,28\n= £11 780,22 excl VAT\n"
             "Total price including VAT = £11 780,22 × {120}/{100}\n= £14 136,26",
             EXCL + "Total price including VAT = £11 584,61 × {115}/{100}\n= £13 322,30",
             EXCL + "Total price including VAT = £11 584,61 × {100}/{120}\n= £9 653,84"], 0,
         ["47 more instalments after the first month; 48 months of maintenance cover.", "All amounts exclude 20% VAT."]),
    work("5.1.3", "Candice's aunt in Switzerland offers to pay the deposit and first-month instalment. Calculate, in Swiss franc (CHF), the deposit and "
         "first-month instalment for OPTION A.", 5,
         DEP + "{£1 173,66}/{0,043}\n= R27 294,42\nAmount in CHF = {R27 294,42}/{R20,48}\n= CHF 1 332,74", [
             "Deposit and first-month instalment = £1 640,61\nAmount in rand = {£1 640,61}/{0,043}\n= R38 153,72\n"
             "Amount in CHF = {R38 153,72}/{R20,48}\n= CHF 1 862,97",
             DEP + "{£1 173,66}/{0,049}\n= R23 952,24\nAmount in CHF = {R23 952,24}/{R20,48}\n= CHF 1 169,54",
             DEP + "{£1 173,66}/{0,04}\n= R29 341,50\nAmount in CHF = {R29 341,50}/{R20,48}\n= CHF 1 432,69"], 0,
         ["Convert pounds to rand first, then rand to Swiss francs.", "Use TABLE 9's factors."])]
INFL = {"head": ["MONTH", "INFLATION RATE (in %)"], "rows": [["Jul. 2024", "2,2"], ["Aug. 2024", "2,2"], ["Sep. 2024", "C"], ["Oct. 2024", "2,3"]]}
MEAN4 = "2,1 = {2,2 + 2,2 + 2,3 + C}/{4}\n2,1 = {6,7 + C}/{4}\n"   # 5.2.1
q52 = [
    work("5.2.1", "The average inflation rate over the four-month period during 2024 was 2,1%. Calculate the missing value C.", 3,
         MEAN4 + "2,1 × 4 = 6,7 + C\nC = 8,4% – 6,7%\n= 1,7%", [
             "2,1 = {2,2 + 2,2 + 2,3 + C}/{3}\n2,1 = {6,7 + C}/{3}\n2,1 × 3 = 6,7 + C\nC = 6,3% – 6,7%\n= –0,4%",
             MEAN4 + "2,1 × 4 = 6,7 + C\nC = 8,4% + 6,7%\n= 15,1%",
             MEAN4 + "{2,1}/{4} = 6,7 + C\nC = 0,525% – 6,7%\n= –6,175%"], 3,
         ["Mean × number of values = their total.", "Subtract the three known rates."]),
    work("5.2.2", "Candice stated that the difference in the cost of a full tank of petrol from Jul. 2024 to Aug. 2024, was £1,5. Verify, showing ALL "
         "calculations, whether her statement is VALID.", 5,
         "Difference = (£1,45 – £1,42) × 40 ℓ\n= £1,20\n£1,20 ≠ £1,5: her statement is NOT VALID", [
             "Difference = £1,45 – £1,42\n= £0,03\n£0,03 ≠ £1,5: her statement is NOT VALID",
             "Difference = (£1,45 – £1,37) × 40 ℓ\n= £3,20\n£3,20 ≠ £1,5: her statement is NOT VALID",
             "Difference = (£1,45 × 40 ℓ) – £1,42\n= £56,58\n£56,58 ≠ £1,5: her statement is NOT VALID"], 1,
         ["Read July and August from ANNEXURE B.", "The tank holds 40 litres."]),
    work("5.2.3", "Calculate, in £ per litre, the cost of petrol during Jun. 2024, if the petrol price from Jun. 2024 to Jul. 2024 changed in line with inflation.", 3,
         "Petrol price for June = {£1,45 × 100}/{102,2}\n= £1,42", [
             "Petrol price for June = {£1,45 × 102,2}/{100}\n= £1,48",
             "Petrol price for June = {£1,45 × 100}/{2,2}\n= £65,91",
             "Petrol price for June = {£1,42 × 100}/{102,2}\n= £1,39"], 2,
         ["July's price is June's price plus 2,2%.", "June's price × 1,022 = July's price: work backwards."]),
    rub("5.2.4", "Describe the trend in the inflation rate for the period Jul. 2024 to Oct. 2024.", 3, [
        "It remains the same (constant) from July to August (1).", "It decreases from August to September (1).", "It increases from September to October (1)."],
        ["Read TABLE 10 month by month (C from 5.2.1).", "Compare each month's rate with the month before: higher, lower or the same?"])]

PRICES = {"head": ["FOOD ITEMS", "QUANTITY", "JOHANNESBURG", "DURBAN", "CAPE TOWN"],
          "rows": [["Salt", "1 kg", "R18,07", "R17,16", "R10,24"], ["Onions #", "10 kg", "R111,59", "R100,58", "R104,10"],
                   ["Carrots #", "5 kg", "R41,41", "R39,63", "R35,08"], ["Butternuts #", "10 kg", "R105,24", "R90,04", "R96,91"],
                   ["Curry powder", "200 g", "R41,91", "R34,24", "R39,82"], ["White sugar", "10 kg", "R223,23", "R197,07", "R229,49"],
                   ["Apples", "3 kg", "R52,38", "R54,73", "R46,31"], ["Oranges", "7 kg", "R104,96", "R78,80", "R86,64"],
                   ["Eggs #", "60 eggs", "R163,31", "R169,62", "R165,52"], ["Canned beans", "410 g × 6", "R101,94", "R84,46", "R81,94"],
                   ["TOTAL", "", "…", "", ""]]}
DEFS = {"head": ["LETTER", "DEFINITION"], "rows": [[chr(65 + i), t] for i, t in enumerate(TERMS)]}
POP = {"head": ["POPULATION GROUP", "NUMBER OF MALES", "NUMBER OF FEMALES", "NUMBER OF PEOPLE (TOTAL)", "% DISTRIBUTION OF TOTAL"],
       "rows": [["Black", "…", "25 085 330", "…", "81,0"], ["Coloured", "2 601 932", "2 737 987", "5 339 919", "8,8"],
                ["Indian/Asian", "794 882", "760 114", "1 554 996", "2,6"], ["White", "2 242 589", "2 396 679", "4 639 268", "7,6"],
                ["TOTAL", "29 624 882", "30 980 110", "60 604 992", "100"]]}
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Food prices", "marks": 9, "table": PRICES,
     "lead": "TABLE 1 shows the prices of some food items in three cities of South Africa, namely Johannesburg, Durban and Cape Town. NOTE: # indicates "
             "zero-rated VAT items.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Financial and data terminology", "marks": 8, "table": DEFS,
     "lead": "TABLE 2 gives definitions of terminology used in Mathematical Literacy.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Population data", "marks": 13, "table": POP,
     "lead": "TABLE 3 shows the population data for South Africa by population group and gender for 2022.", "items": q13},
    {"id": "2.1", "title": "Question 2.1", "kind": "Income tax", "marks": 18, "table": PAYE,
     "lead": "In South Africa, employees need to pay income tax based on their earnings. An extract of Muriel Davids' salary slip for one month for the "
             "tax year ending February 2025 is shown below. Some information has been omitted. The table is ANNEXURE A's monthly PAYE deduction table "
             "for the 2024/2025 tax year (rows between have been left out, as printed).", "extract": SLIP, "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Bus fares", "marks": 14, "table": METRO,
     "lead": "Muriel Davids travels to work by bus. TABLE 4 shows information on the Metrobus service in Johannesburg for three categories of passengers "
             "travelling by bus.", "items": q22},
    {"id": "3.1", "title": "Question 3.1", "kind": "Social media data", "marks": 13, "table": SOCIAL,
     "lead": "Social media platforms enable users to share information and ideas virtually through texts, photographs, videos and much more. TABLE 5 "
             "shows the use of popular social media platforms categorised by gender.", "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "LTE devices", "marks": 17, "table": LTE,
     "lead": "There has been an increase in the number of long-term evolution (LTE) devices in South Africa over the last three years. ANSWER SHEET 3.2 "
             "shows a graph for the number of LTE devices per province over a three-year period. Some of the information on the graph has been omitted. "
             "NOTE: LTE is a term used for a particular type of 4G that delivers a fast mobile internet experience. The table holds the 2023 data "
             "omitted from the graph (QUESTION 3.2.3).",
     "figure": fig("3.2", "ANSWER SHEET 3.2, a graph, NUMBER OF LTE DEVICES PER PROVINCE, 0 to 60 000 000 in steps of 1 000 000 (key: hatched "
                   "2021, white 2022, black 2023), one bar for each of Gauteng, KwaZulu-Natal, Limpopo, Western Cape, Mpumalanga, Eastern Cape, "
                   "North West, Free State and Northern Cape; KwaZulu-Natal and Mpumalanga have no 2023 part (3.2.3 completes them)."),
     # (no graph type and no readings: 3.2.1 asks for the type, 3.2.2 for readings off the bars, which carry no printed values)
     "items": q32},
    {"id": "4.1", "title": "Question 4.1", "kind": "Trailer rental", "marks": 15, "table": TRAILERS,
     "lead": "Monwabisi operates a trailer rental business. His rental costs for hiring a trailer are:\n• R1 000 refundable deposit per trailer if there is "
             "no damage to the trailer\n• R350 per day per small trailer\n• R500 per day per large trailer\nTABLE 6 shows the rental costs of trailers, "
             "including the deposit.", "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "VAT payments", "marks": 13, "table": VAT,
     "lead": "TABLE 7 shows the VAT payments made to SARS by vendors in certain economic sectors for 2023/2024. NOTE: A vendor is a person or company "
             "offering goods or services for sale.", "items": q42},
    {"id": "5.1", "title": "Question 5.1", "kind": "Buying a car", "marks": 16, "table": CARS,
     "lead": "Candice started a small delivery business in London and planned to purchase an electric car (a Dolphin hatchback) for the business. TABLE 8 "
             "shows information on TWO car purchase options, A and B, that she could choose from. NOTE: All amounts exclude 20% VAT.",
     "extract": "TABLE 9: CURRENCY CONVERSION FACTORS\nSwiss franc (CHF): ZAR per unit 20,48; units per ZAR 0,049\nPound sterling (£): ZAR per unit 23,20; "
                "units per ZAR 0,043", "items": q51},
    {"id": "5.2", "title": "Question 5.2", "kind": "Petrol and inflation", "marks": 14, "table": INFL,
     "lead": "Candice's husband has a car with a 40 ℓ petrol tank capacity. The price of petrol may change from month to month. ANNEXURE B shows the graph "
             "of the average petrol price per month in pounds (£) for a four-month period during 2024. TABLE 10 shows the monthly inflation percentages "
             "for a four-month period during 2024.",
     "figure": fig("5.2", "ANNEXURE B, a bar graph, AVERAGE PETROL PRICE PER MONTH FOR A FOUR-MONTH PERIOD, the average monthly petrol price in £ per "
                   "litre from 1,2 to 1,5 for Jul. 2024, Aug. 2024, Sep. 2024 and Oct. 2024."),   # (no readings: 5.2.2-5.2.3 read them off the bars)
     "items": q52},
]


# ---- Written answers as STATEMENTS (Murci 2026-10-10): the memo's own points (right, one reading of its "OR") and CLEARLY false ones
# (never a true point the memo leaves out); the learner picks marks/each of them, each right pick earns `each`; the cards are shuffled
# the same way every run. The rubrics above stay as the source.
def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random("ml-p1-2025-11:" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts,
            "pool": sorted(k for k, i in enumerate(order) if i < len(right)), "count": count}


STATEMENTS = {
    # MG p19: 2O for ONE reason, "much lower deposit and first-month instalment" OR "a smaller deposit"; the false ones from TABLE 8
    # (both 48 months; A's later instalments £195,61 > £182,29 and cover £25,36 > £24,00; the NOTE: all amounts exclude VAT)
    "5.1.2(a)": (2, ["Option A's deposit and first-month instalment is much lower than Option B's.", "Option A has a smaller deposit."],
                 ["Option A has a shorter payment period than Option B.",
                  "Option A's additional monthly instalments are lower than Option B's.",
                  "Option A's compulsory monthly maintenance cover is cheaper than Option B's.",
                  "Option A's amounts include VAT, while Option B's amounts exclude VAT."]),
    # MG p23: 1A each, the three steps of the trend (C = 1,7 from 5.2.1); the false ones are each step's opposite and "no change"
    "5.2.4": (1, ["It remains the same (constant) from July to August.", "It decreases from August to September.",
                  "It increases from September to October."],
              ["It increases from July to August.", "It increases from August to September.", "It decreases from September to October.",
               "It remains the same for the whole period from July to October."]),
}
# Gates: a part whose options show an earlier part's answer opens once that part is answered
AFTER = {"2.1.4(b)": ["2.1.4(a)"],             # its workings use A = R6 298
         "2.1.4(c)": ["2.1.4(a)"],             # every working compares with the R6 298 deducted (and its clue names it)
         "3.1.3(b)": ["3.1.3(a)"],             # its workings take 46% of 750 000 000, 3.1.3(a)'s total
         "4.2.4(b)": ["4.2.2", "4.2.4(a)"],    # its workings list the vendors in ascending order (4.2.4(a)), the third largest 46 901 (4.2.2)
         "5.2.4": ["5.2.1"]}                   # its cards say the rate decreases from August to September: C below 2,2 (5.2.1)
for _m in missions:
    for _k, _it in enumerate(_m["items"]):
        if _it["t"] == "rubric" and _it["n"] in STATEMENTS:
            _each, _right, _wrong = STATEMENTS[_it["n"]]
            _m["items"][_k] = stmt(_it["n"], _it["q"], _it["marks"], _right, _wrong, _it["clues"], _each)
        if _it["n"] in AFTER:
            _m["items"][_k]["after"] = AFTER[_it["n"]]
assert sorted(AFTER) == sorted(i["n"] for m in missions for i in m["items"] if i.get("after"))
assert not [i["n"] for m in missions for i in m["items"] if i["t"] in ("rubric", "steps")], "a written part or typed steps left"
for i in [i for m in missions for i in m["items"]]:   # a completed stacked bar (build-play.js "hist" stack): its end and its shading, bar by bar
    b = i.get("build") or {}
    if b.get("stack"):
        st = b["stack"]
        assert len(i["criteria"]) == 2 * len(b["groups"]) == 2 * len(st["base"]) == 2 * len(b["answers"]), i["n"]
        assert all(a > base[-1] and a % b["snap"] == 0 and a <= b["top"] for a, base in zip(b["answers"], st["base"])), i["n"]
        assert len(st["series"]) == len(st["fill"]) and 0 <= st["want"] < len(st["series"]), i["n"]
assert [i["n"] for m in missions for i in m["items"] if i.get("build")] == ["3.2.3"]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P1", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematical Literacy", "total": 150, "missions": missions}],
    "flags": [
        {"n": WORKED[0][0], "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): every typed calculation plays as the memo's working "
                                                        "plus three built from common errors, 0 or full marks: " + ", ".join(n for n, _ in WORKED)
                                                        + " (%d parts, %d marks; the read-offs 1.3.4, 1.3.5 and 2.1.4(a) as the row and column read, "
                                                          "then the value). A value the memo also accepts never stands as a wrong option: R8,28 "
                                                          "(1.1.2), 750 million, 7 million, 15 million (3.1.3(a), 3.2.2(b), 3.2.2(c)), 5.1.3's other "
                                                          "conversions (R27 228,91; CHF 1 329,54, 1 337,43, 1 334,22) and 5.2.2's graph readings "
                                                          "1,41 – 1,43 (£0,80 – £1,60)." % (len(WORKED), sum(m for _, m in WORKED))},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper, hand-transcribed from the SCANNED question paper's page images, the memo and "
                                                           "the special answer book (ANNEXURE A typed; ANSWER SHEET 3.2 and ANNEXURE B cropped from it)."},
        {"n": "4.1.1", "kind": "no_fit", "detail": "A formula plays as a strict term listing the forms a learner types (all or nothing: the memo's 1 "
                                                   "for the deposit and 1 for the variable cost)."},
        {"n": "3.2.3", "kind": "no_fit", "detail": "Completing the stacked bar graph is BUILT (2026-10-11, the bar graph builder completing a "
                                                   "stacked bar): KwaZulu-Natal's and Mpumalanga's bars with their printed 2021 and 2022 parts; "
                                                   "the learner drags each new part up (snapping to 500 000) and chooses its shading from the "
                                                   "key; the memo's end point and complete stacked bar (the 2023 shading) earn 1 each, bar by bar."},
        {"n": "5.1.2(a)", "kind": "no_fit", "detail": "The written answers play as statements (Murci, 2026-10-10): 5.1.2(a) picks ONE of the memo's two "
                                                      "reasons (2 marks) and 5.2.4 the trend's THREE steps (1 mark each), among clearly false "
                                                      "statements read off TABLE 8 and TABLE 10."},
        {"n": "1.1.3", "kind": "memo_issue", "detail": "The memo's explanation reads '1RT 169,92' where the table and its working use R169,62."},
        {"n": "4.2.1", "kind": "memo_issue", "detail": "The paper asks for V 'rounded to the nearest thousand'; the memo rounds to three decimal places "
                                                       "(0,652, the nearest thousandth)."},
    ],
}
out = Path(__file__).parent / "out" / "ml-p1-2025-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the scanned question paper, the memo and the special answer book "
                                                                       "(no API call)", "scope": "Questions 1 to 5 (the whole paper)"}, "paper": paper},
                                              indent=1, ensure_ascii=False), encoding="utf-8")
for m in missions:
    got = sum(i["marks"] for i in m["items"])
    assert got == m["marks"], (m["id"], got, m["marks"])
    print(m["id"], "parts:", len(m["items"]), "marks:", got)
items = [i for m in missions for i in m["items"]]
assert not [i["n"] for i in items if i["t"] in ("steps", "num")], "a typed calculation is left"
spread = [sum(1 for i in items if (i["n"], i["marks"]) in WORKED and i["a"] == k) for k in range(4)]
assert max(spread) - min(spread) <= 1, spread   # the right working sits evenly over A-D
print("worked:", len(WORKED), "parts,", sum(m for _, m in WORKED), "marks; right letter A-D:", spread)
total = sum(i["marks"] for i in items)
assert total == 150, total
print("total:", total)
