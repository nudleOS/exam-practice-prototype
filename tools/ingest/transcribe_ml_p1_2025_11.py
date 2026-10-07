"""Mathematical Literacy P1 Nov 2025, the whole paper (Questions 1 to 5, 150 marks), hand-transcribed into the catalogue format (as
if Claude had produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, marks, answers and the memo's
working are the paper's and the memo's own; clues and figure captions are ours. The question paper is a SCAN (no text layer): read
from its page images. ANNEXURE A (the PAYE tables), ANSWER SHEET 3.2 and ANNEXURE B (two graphs) are printed in the SPECIAL ANSWER
BOOK (downloaded from DBE, 2026-10-07): the tables are typed, the graphs cropped from the answer book (figure source "answer_book").

  python tools/ingest/transcribe_ml_p1_2025_11.py
  python tools/ingest/ingest.py "<...>/Mathematical Literacy P1 Nov 2025 Eng.pdf" "<...>/Mathematical Literacy P1 Nov 2025 MG Afr & Eng.pdf" \
      --id ml-p1-2025-11 --from-json --answer-book "<...>/Mathematical Literacy P1 Nov 2025 Answer Book Eng.pdf"

How the memo's shapes map (Mathematical Literacy):
  a calculation -> steps, each ONE number the memo's method produces (unit in the label), the method marks (MA, CA, RT, A) riding on
  it; "Verify ... whether the statement is VALID" -> steps for its numbers, the conclusion mark (O) riding on the last one (the phone
  sees numbers); a memo range or several accepted methods -> a tolerance spanning them; a read-off -> num or term; "discrete or
  continuous" -> mcq; terminology matched to definitions -> match; "arrange in ascending order" -> order; a formula -> strict term with
  the forms a learner types; "complete the graph" -> draw, self-checked."""
import json
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
num = lambda n, q, a, tol, unit, clues, marks=2: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
draw = lambda n, q, marks, criteria, clues, memo="": {"t": "draw", "n": n, "marks": marks, "q": q, "clues": clues,
                                                     "criteria": [{"text": t, "marks": m} for t, m in criteria], **({"memo": memo} if memo else {})}


def steps(n, q, marks, sts, clues):
    """sts: (label, marks, answer, tolerance, the memo's working)."""
    s = [{"id": "s%d" % (i + 1), "label": lab, "marks": m, "a": a, "tol": tol, "memo": memo} for i, (lab, m, a, tol, memo) in enumerate(sts)]
    assert sum(x["marks"] for x in s) == marks, n
    return {"t": "steps", "n": n, "marks": marks, "q": q, "clues": clues, "steps": s}


def pairs(*names):
    """Every way a learner writes a pair: 'A and B', 'A B' (a comma or & drops out), both orders."""
    out = []
    for a, b in names:
        for x, y in ((a, b), (b, a)):
            out += ["%s and %s" % (x, y), "%s %s" % (x, y)]
    return out


# ---- QUESTION 1, the question paper pages 3-5 and the memo pages 2-4 ----
q11 = [
    term("1.1.1", "Name the city where the cost of white sugar is the highest.", ["Cape Town"],
         ["Read the White sugar row.", "Compare the three cities' prices."]),
    steps("1.1.2", "Calculate the cost of carrots, per kilogram, in Johannesburg.", 2,
          [("Cost of carrots per kilogram in Johannesburg (R)", 2, 8.282, 0.003, "Cost per kilogram = R41,41 ✓RT ÷ 5 = R8,282 OR R8,28 ✓A")],
          ["The table gives the price for 5 kg.", "Divide by the number of kilograms."]),
    steps("1.1.3", "Determine, as a unit ratio rounded to THREE decimal places, the price of eggs in Cape Town compared to the price of eggs in "
          "Durban in the form 1 : …", 3, [
        ("Price of eggs in Cape Town (R)", 1, 165.52, 0.005, "165,52 ✓RT"),
        ("Price of eggs in Durban (R)", 1, 169.62, 0.005, "169,62 ✓RT"),
        ("The unit ratio 1 : … (the number after the colon)", 1, 1.025, 0.0004, "165,52 : 169,62 = 1 : 1,025 ✓A")],
          ["Cape Town comes first in the ratio.", "Divide both sides by the Cape Town price."]),
    steps("1.1.4", "Calculate the total price of ALL the food items in Johannesburg.", 2, [
        ("Total price of all the food items in Johannesburg (R)", 2, 964.04, 0.005,
         "R18,07 + R111,59 + R41,41 + R105,24 + R41,91 + R223,23 + R52,38 + R104,96 + R163,31 + R101,94 ✓MA = R964,04 ✓A")],
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
    num("1.3.4", "Identify the total number of the South African population for 2022.", 60604992, 0.5, "people",
        ["Read the TOTAL row.", "The NUMBER OF PEOPLE column."]),
    num("1.3.5", "The total number of black South Africans is forty-nine million seventy thousand eight hundred and nine. Write this number in "
        "numerals without using words.", 49070809, 0.5, "", ["49 million, then 70 thousand, then 809.", "Fill every place value."]),
    steps("1.3.6", "Express the number of white males as a percentage of the total number of males.", 3, [
        ("White males as a percentage of all males (%)", 3, 7.57, 0.075, "2 242 589 / 29 624 882 ✓RT × 100% ✓MA = 7,569950827% ✓A "
         "(no penalty for rounding when the first decimal is correct)")],
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
q21 = [
    term("2.1.1", "Write the acronym UIF in words.", ["Unemployment Insurance Fund"], ["It pays out when you lose your job.", "U ... Insurance Fund."]),
    term("2.1.2", "Name the institution that collects tax on behalf of the government of South Africa.",
         ["SARS", "South African Revenue Service", "South African Revenue Services"], ["Four letters.", "The South African ... Service."]),
    steps("2.1.3", "Determine the employer contribution towards the medical aid if the employer contributes one third of the total contribution.", 2, [
        ("Employer's medical aid contribution (R)", 2, 1265.77, 0.005, "R2 531,54 ÷ 2 ✓MA = R1 265,77 ✓A (Muriel pays two thirds; OR total = "
         "3/2 × R2 531,54 = R3 797,31, ÷ 3 = R1 265,77)")],
          ["If the employer pays one third, Muriel pays the other two thirds.", "Muriel's two thirds is R2 531,54: find one third."]),
    num("2.1.4(a)", "Write down the missing value A from the monthly PAYE deduction table in ANNEXURE A.", 6298, 0.5, "R",
        ["Find the row her R35 000 falls in.", "She is 42: the 'below 65' column."]),
    steps("2.1.4(b)", "Calculate the missing value B.", 2, [
        ("Net salary B (R)", 2, 25993.34, 0.005, "B = R35 000 – R177,12 – R6 298 – R2 531,54 ✓MCA = R25 993,34 ✓CA (CA from 2.1.4(a))")],
          ["Net = gross minus every employee deduction.", "UIF, PAYE and medical aid."]),
    steps("2.1.4(c)", "Muriel stated that she overpaid tax in the 2024/2025 tax year. Verify, showing ALL calculations, whether her statement is VALID.", 8, [
        ("Annual taxable income (R)", 1, 420000, 0.5, "R35 000 × 12 = R420 000 ✓A"),
        ("Annual tax before rebates (R)", 2, 92707, 0.5, "R77 362 + 31% (R420 000 – R370 500) ✓MCA (the correct bracket) = R77 362 + R15 345 = R92 707,00 ✓CA"),
        ("Annual tax after the rebate and medical tax credits (R)", 3, 71104, 0.5,
         "R92 707,00 – R17 235 ✓RT – (R364 × 12) ✓MA = R92 707,00 – R17 235 – R4 368 = R71 104,00 ✓CA"),
        ("Monthly tax she should pay (R)", 2, 5925.33, 0.01, "R71 104,00 ÷ 12 = R5 925,33 ✓CA, less than the R6 298 deducted (OR R6 298 × 12 = R75 576 "
         "a year): her statement is VALID ✓O (CA from 2.1.4(a))")],
          ["Find her annual tax with the tax rates, then subtract the rebate and 12 months of medical tax credits.",
           "Compare what she should pay with the R6 298 deducted each month."])]
METRO = {"head": ["TRIP PACKAGE", "DURATION", "ADULTS (15–59)", "CHILDREN (3–14)", "PENSIONERS (60+)"],
         "rows": [["1 trip", "Daily", "R14,20", "R10,30", "R4,20"], ["10 trips", "Weekly", "R106,00", "R76,40", "-"],
                  ["12 trips", "Weekly", "R127,10", "-", "-"], ["44 trips", "Monthly", "R465,60", "R336,30", "-"]]}
q22 = [
    steps("2.2.1", "Calculate the percentage savings a pensioner receives per bus trip when compared to the amount paid by an adult for the same bus trip.", 3, [
        ("The pensioner's fare as a percentage of the adult fare (%)", 2, 29.58, 0.005, "R4,20 / R14,20 × 100% ✓MA ✓A = 29,58%"),
        ("Percentage saving (%)", 1, 70.42, 0.005, "100% – 29,58% = 70,42% ✓CA (OR (R14,20 – R4,20)/R14,20 × 100% = 70,42%)")],
          ["Compare the 1-trip fares: R4,20 and R14,20.", "The saving is the part of the adult fare the pensioner does not pay."]),
    steps("2.2.2", "Determine the amount Muriel will save per trip if she buys the monthly package instead of the daily trip package.", 5, [
        ("Cost per trip with the monthly package (R)", 3, 10.58, 0.005, "R465,60 ✓RT ÷ 44 ✓MA = R10,58 ✓CA"),
        ("Saving per trip (R)", 2, 3.62, 0.005, "R14,20 – R10,58 ✓MCA = R3,62 ✓CA (OR R14,20 × 44 = R624,80; R624,80 – R465,60 = R159,20; ÷ 44 = R3,62)")],
          ["Muriel is an adult.", "Find the cost of one trip in the 44-trip package, then compare with R14,20."]),
    term("2.2.3", "Write down the probability of a 10-year old child purchasing a weekly package with 12 trips.",
         ["0", "0%", "Impossible", "0/4", "0/3", "Nil"], ["Look at the Children column for 12 trips.", "Can it happen at all?"]),
    steps("2.2.4", "Johannesburg Metrobus introduced a compulsory card payment system. All passengers will be required to purchase the Metrobus card for R35 "
          "to activate the card. They will then have to upload trip fares according to the different available trip packages. Muriel purchased a "
          "Metrobus card together with an uploaded trip package to the total value of R416,30. Calculate the maximum number of weekly trips Muriel can "
          "take using this card.", 4, [
        ("Package amount left after the card (R)", 2, 381.30, 0.005, "R416,30 – R35,00 ✓RT ✓A = R381,30"),
        ("Number of weekly 12-trip packages", 2, 3, 0.01, "R381,30 ÷ R127,10 ✓MCA = 3 ✓CA (OR R416,30 – R127,10 – R127,10 – R127,10 = R35)")],
          ["Take off the card's R35 first.", "Muriel is an adult: which weekly package fits the rest exactly?"])]

# ---- QUESTION 3, the question paper pages 8-9, the answer book page 8 and the memo pages 11-14 ----
SOCIAL = {"head": ["SOCIAL MEDIA PLATFORM", "PERCENTAGE MALE USERS", "MALE USERS (in millions)", "PERCENTAGE FEMALE USERS", "FEMALE USERS (in millions)"],
          "rows": [["Facebook", "57%", "1 732,8", "43%", "1 307,2"], ["Instagram", "51%", "1 020", "49%", "980"], ["Snapchat", "46%", "***", "54%", "405"],
                   ["X/Twitter", "56%", "346,64", "44%", "272,36"], ["TikTok", "43%", "645", "57%", "855"], ["YouTube", "54%", "1 350", "46%", "1 150"]]}
q31 = [
    steps("3.1.1", "Calculate the median percentage for male social media users.", 4, [
        ("Median percentage of male users (%)", 4, 52.5, 0.005, "43% 46% 51% 54% 56% 57% ✓MA (arranged); (51% ✓RT + 54%) ÷ 2 ✓MA = 52,5% ✓CA")],
          ["Arrange the six male percentages in order.", "With an even count, the median is the mean of the middle two."]),
    steps("3.1.2", "Determine, as a decimal, the probability of randomly selecting a social media platform where the female users were fewer than the male users.", 3, [
        ("Probability, as a decimal", 3, 0.667, 0.004, "4 ✓A / 6 ✓A = 0,67 ✓CA")],
          ["Count the platforms with fewer female than male users.", "Out of six platforms."]),
    steps("3.1.3(a)", "Fezeka is interested in the number of male and female Snapchat users. Determine the total number of Snapchat users.", 2, [
        ("Total number of Snapchat users (in millions)", 2, 750, 0.5, "405 000 000 ÷ 54% ✓MA = 750 000 000 (750 million) ✓CA (OR males = 46/54 × 405 000 000 "
         "= 345 000 000; 405 000 000 + 345 000 000)")],
          ["405 million females are 54% of all Snapchat users.", "Divide by 54%."]),
    steps("3.1.3(b)", "Fezeka stated that the difference between the number of female and male Snapchat users was 61 300 000. Verify, showing ALL "
          "calculations, whether her statement is VALID.", 4, [
        ("Number of male Snapchat users (in millions)", 2, 345, 0.5, "46/100 × 750 000 000 ✓MCA = 345 000 000 ✓CA"),
        ("Difference between female and male users (in millions)", 2, 60, 0.5, "405 000 000 – 345 000 000 = 60 000 000 ✓CA: her statement is NOT VALID "
         "✓O (OR 54% – 46% = 8%; 8% × 750 million = 60 000 000)")],
          ["Males are 46% of the total from 3.1.3(a).", "Compare your difference with 61,3 million."])]
LTE = {"head": ["PROVINCE", "NUMBER OF LTE DEVICES DURING 2023"], "rows": [["KwaZulu-Natal", "11 000 000"], ["Mpumalanga", "5 500 000"]]}
q32 = [
    term("3.2.1", "Name the type of graph drawn on ANSWER SHEET 3.2.", ["Stacked bar graph", "Compound bar graph", "Stacked bar chart",
                                                                        "Compound bar chart", "Stacked bar", "Compound bar"],
         ["Each bar is built from three years on top of each other.", "A ... bar graph."]),
    term("3.2.2(a)", "Use the graph on ANSWER SHEET 3.2: write down the names of TWO provinces that had the same number of LTE devices during 2021.",
         pairs(("Limpopo", "North West"), ("Mpumalanga", "Eastern Cape"), ("LP", "NW"), ("MP", "EC")),
         ["Read only the hatched (2021) part of each bar.", "Find two bars whose 2021 parts end at the same height."]),
    steps("3.2.2(b)", "Use the graph on ANSWER SHEET 3.2: determine the number of LTE devices in Limpopo during 2022.", 3, [
        ("Number of LTE devices in Limpopo during 2022", 3, 7000000, 0.5, "11 000 000 – 4 000 000 ✓RT (both values) ✓MA = 7 000 000 ✓CA "
         "(OR 18 500 000 – 4 000 000 – 7 500 000)")],
          ["The white (2022) part of Limpopo's bar.", "Its top minus its bottom."]),
    steps("3.2.2(c)", "Use the graph on ANSWER SHEET 3.2: calculate the range of LTE devices in the provinces during 2021.", 4, [
        ("Range of LTE devices in 2021", 4, 15000000, 0.5, "16 000 000 ✓RT – 1 000 000 ✓RT ✓MA = 15 000 000 ✓CA")],
          ["Range = highest − lowest.", "Use the 2021 (hatched) parts only."]),
    draw("3.2.3", "The data in the table represents the number of LTE devices for two provinces during 2023 that has been omitted in the graph. Use the "
         "data to complete the graph on ANSWER SHEET 3.2.", 4, [
        ["KwaZulu-Natal: the 2023 part ends at 31 500 000", 1], ["KwaZulu-Natal: the stacked bar completed in the 2023 shading", 1],
        ["Mpumalanga: the 2023 part ends at 14 000 000", 1], ["Mpumalanga: the stacked bar completed in the 2023 shading", 1]],
        ["Stack 2023 on top of each bar's 2022 part.", "KwaZulu-Natal's bar ends at 20 500 000 now; Mpumalanga's at 8 500 000."]),
    steps("3.2.4", "Determine, as a fraction, the probability of randomly selecting a province that has a total number of LTE devices less than 8 million "
          "for the three-year period.", 2, [
        ("Probability (a fraction: enter it with the calculator's ÷ key)", 2, 0.2222, 0.003, "2 ✓A / 9 ✓A")],
          ["Count the bars whose whole height is below 8 000 000.", "Out of nine provinces."])]

# ---- QUESTION 4, the question paper pages 10-11 and the memo pages 15-18 ----
TRAILERS = {"head": ["Number of days (n)", "1", "3", "5", "7", "10", "15"],
            "rows": [["Cost for small trailer", "R1 350", "R2 050", "B", "R3 450", "R4 500", "R6 250"],
                     ["Cost for large trailer", "R1 500", "R2 500", "R3 500", "R4 500", "R6 000", "R8 500"]]}
q41 = [
    term("4.1.1", "Write down a formula to calculate the rental cost, including the deposit, of a large trailer in the form: Cost = …", [
        "Cost = R1 000 + (R500 × n)", "Cost = R1 000 + (R500 × number of days)", "Cost = 1000 + 500n", "Cost = R1000 + R500n", "Cost = 1000 + 500 x n",
        "Cost = 500n + 1000", "Cost = R500n + R1000", "Cost = 500 x n + 1000", "Cost = 1000 + 500 x number of days", "C = 1000 + 500n",
        "1000 + 500n", "500n + 1000", "1000 + 500 x n"],
         ["A fixed deposit plus a cost for every day.", "R1 000 deposit; R500 per day for a large trailer."], strict=True),
    steps("4.1.2", "Calculate the missing value B.", 3, [
        ("Cost B for a small trailer for 5 days (R)", 3, 2750, 0.5, "R1 000 ✓A + (R350 × 5) ✓MA = R2 750 ✓CA (OR R2 050 + R350 + R350)")],
          ["B is the small trailer for 5 days.", "Deposit plus R350 per day."]),
    steps("4.1.3(a)", "On 12 December 2024, Monwabisi rented out TWO small trailers and SIX large trailers to different customers for a day. One of the "
          "trailers was returned with a damaged rear light. Monwabisi stated that his total income, after refunding the deposit, amounted to R4 550. "
          "Verify, showing ALL calculations, whether his statement is VALID.", 6, [
        ("Income for all eight trailers for one day, deposits included (R)", 3, 11700, 0.5, "(R1 350 × 2) + (R1 500 × 6) ✓MA = R2 700 ✓A + R9 000 = "
         "R11 700 ✓CA"),
        ("Total income after refunding the deposits (R)", 3, 4700, 0.5, "R11 700 – R7 000 ✓MCA (seven undamaged trailers) = R4 700 ✓CA: the statement is "
         "NOT VALID ✓O (OR R700 + R3 000 + R1 000 kept deposit = R4 700)")],
          ["Seven deposits go back; the damaged trailer's deposit is kept.", "Compare your income with R4 550."]),
    steps("4.1.3(b)", "The following quotation for the repair and replacement of the rear light was received: new rear light: R242; labour at R480 per hour "
          "or part thereof; time required to complete the repair and replacement is 1 hour 30 minutes. Verify, showing ALL calculations, whether the "
          "deposit amount will be sufficient to cover the total cost of the entire repair and replacement.", 4, [
        ("Labour cost (R)", 2, 960, 0.5, "R480 × 2 ✓MA (1 h 30 min is charged as 2 hours) = R960 ✓CA"),
        ("Total cost of the repair (R)", 2, 1202, 0.5, "R960 + R242 = R1 202 ✓CA: the deposit of R1 000 will not be sufficient ✓O (OR R1 000 – R480 – R480 "
         "– R242 = –R202)")],
          ["'Or part thereof': half an hour is charged as a full hour.", "Add the light, then compare with R1 000."])]
VAT = {"head": ["ECONOMIC SECTOR", "NUMBER OF VENDORS", "VAT PAYMENTS (R million)", "AVERAGE PAYMENT PER VENDOR (R million)"],
       "rows": [["Financial", "197 178", "221 322", "1,12245"], ["Manufacturing", "46 901", "73 893", "1,57548"],
                ["Wholesale and retail trade", "86 610", "76 826", "0,88703"], ["Construction", "39 279", "25 593", "V"],
                ["Transport", "15 258", "29 418", "1,92804"], ["Community and social", "33 825", "32 458", "0,95959"], ["Utilities", "2 658", "22 141", "8,32995"]]}
q42 = [
    steps("4.2.1", "Determine, rounded to the nearest thousand, the missing value V.", 3, [
        ("V before rounding (R million)", 2, 0.65157, 0.0005, "25 593 ÷ 39 279 ✓MA = 0,651569541 ✓CA"),
        ("V rounded to three decimal places (R million)", 1, 0.652, 0.0003, "= 0,652 ✓R")],
          ["Average payment per vendor = VAT payments ÷ number of vendors.", "Round to three decimal places."]),
    term("4.2.2", "Write down the sector that has the third largest number of vendors.", ["Manufacturing"],
         ["Order the NUMBER OF VENDORS column from the largest.", "Count down three."]),
    steps("4.2.3", "Calculate (in R million) the mean VAT payment amount per economic sector.", 3, [
        ("Mean VAT payment per sector (R million)", 3, 68807.29, 0.01, "(221 322 + 73 893 + 76 826 + 25 593 + 29 418 + 32 458 + 22 141) ✓MA ÷ 7 ✓MA = "
         "481 651 ÷ 7 = 68 807,29 ✓CA")],
          ["Add all seven VAT payments.", "Divide by the number of sectors."]),
    {"t": "order", "n": "4.2.4(a)", "marks": 2, "q": "Arrange the number of vendors in ascending order.",
     "clues": ["Smallest first.", "Seven values."], "opts": ["197 178", "46 901", "86 610", "39 279", "15 258", "33 825", "2 658"], "a": [6, 4, 5, 3, 1, 2, 0]},
    steps("4.2.4(b)", "The value of quartile 3 (Q3) for the number of vendors is 86 610. Calculate the interquartile range (IQR) for the number of vendors. "
          "You may use the formula: Interquartile range (IQR) = Q3 – Q1.", 3, [
        ("Quartile 1 (Q1)", 1, 15258, 0.5, "2 658  15 258  33 825  39 279  46 901  86 610  197 178: Q1 = 15 258 ✓A"),
        ("Interquartile range (IQR)", 2, 71352, 0.5, "86 610 – 15 258 ✓MCA = 71 352 ✓CA (CA from 4.2.4(a))")],
          ["Q1 is the middle of the lower half.", "IQR = Q3 − Q1."])]

# ---- QUESTION 5, the question paper pages 12-13, the answer book page 14 and the memo pages 19-23 ----
CARS = {"head": ["DETAILS", "OPTION A", "OPTION B"],
        "rows": [["Payment period", "48 months", "48 months"], ["Deposit and first-month instalment", "£1 173,66", "£1 640,61"],
                 ["Additional months' instalment", "£195,61", "£182,29"], ["Compulsory monthly maintenance cover", "£25,36", "£24,00"]]}
q51 = [
    steps("5.1.1", "Calculate the total maintenance cover for the payment period for OPTION B.", 2, [
        ("Total maintenance cover for Option B (£)", 2, 1152, 0.005, "£24 ✓RT × 48 = £1 152 ✓CA")],
          ["Option B's monthly maintenance cover.", "For every month of the payment period."]),
    rub("5.1.2(a)", "Candice chooses OPTION A. Give ONE possible reason why Candice chose OPTION A.", 2, [
        "The deposit and first-month instalment is much lower (2).", "OR — Option A has a smaller deposit (2)."],
        ["Compare the first payment of the two options.", "What would a new small business need?"], each=2),
    steps("5.1.2(b)", "Candice chooses OPTION A. Calculate the total amount, including VAT, that she would have paid at the end of the payment period.", 7, [
        ("Total amount excluding VAT (£)", 5, 11584.61, 0.01, "£1 173,66 ✓RT + (£195,61 × 47 ✓A) + (£25,36 × 48 ✓A) ✓MCA = £1 173,66 + £9 193,67 + "
         "£1 217,28 = £11 584,61 ✓CA"),
        ("Total amount including 20% VAT (£)", 2, 13901.53, 0.01, "£11 584,61 × 120/100 ✓MCA = £13 901,53 ✓CA (OR + VAT £2 316,92)")],
          ["47 more instalments after the first month; 48 months of maintenance cover.", "All amounts exclude 20% VAT."]),
    steps("5.1.3", "Candice's aunt in Switzerland offers to pay the deposit and first-month instalment. Calculate, in Swiss franc (CHF), the deposit and "
          "first-month instalment for OPTION A.", 5, [
        ("Deposit and first-month instalment (£)", 1, 1173.66, 0.005, "£1 173,66 ✓RT"),
        ("The same amount in rand (R)", 2, 27261.67, 33, "£1 173,66 ÷ 0,043 ✓MA = R27 294,42 ✓CA (OR × R23,20 = R27 228,91)"),
        ("The same amount in Swiss francs (CHF)", 2, 1333.49, 4, "R27 294,42 ÷ R20,48 ✓MCA = CHF 1 332,74 ✓CA (OR R27 228,91 ÷ 20,48 = CHF 1 329,54; OR "
         "× 0,049 = CHF 1 337,43 / CHF 1 334,22; OR £1 = CHF 1,1328125)")],
          ["Convert pounds to rand first, then rand to Swiss francs.", "Use TABLE 9's factors."])]
INFL = {"head": ["MONTH", "INFLATION RATE (in %)"], "rows": [["Jul. 2024", "2,2"], ["Aug. 2024", "2,2"], ["Sep. 2024", "C"], ["Oct. 2024", "2,3"]]}
q52 = [
    steps("5.2.1", "The average inflation rate over the four-month period during 2024 was 2,1%. Calculate the missing value C.", 3, [
        ("Sum of the four inflation rates (%)", 2, 8.4, 0.005, "(2,2 + 2,2 + C + 2,3) ÷ 4 = 2,1 ✓MA ✓MA: the four rates add up to 2,1 × 4 = 8,4%"),
        ("Value of C (%)", 1, 1.7, 0.005, "C = 8,4% – 6,7% = 1,7% ✓CA")],
          ["Mean × number of values = their total.", "Subtract the three known rates."]),
    steps("5.2.2", "Candice stated that the difference in the cost of a full tank of petrol from Jul. 2024 to Aug. 2024, was £1,5. Verify, showing ALL "
          "calculations, whether her statement is VALID.", 5, [
        ("Petrol price in Jul. 2024 (£ per litre)", 1, 1.45, 0.005, "£1,45 ✓A"),
        ("Petrol price in Aug. 2024 (£ per litre)", 1, 1.42, 0.011, "£1,42 ✓RT (from the graph: 1,41–1,43)"),
        ("Difference in the cost of a full 40 ℓ tank (£)", 3, 1.20, 0.41, "(£1,45 – £1,42) × 40 ℓ ✓MA = £1,20 ✓CA: her statement is NOT VALID ✓O "
         "(OR £58 – £56,80)")],
          ["Read July and August from ANNEXURE B.", "The tank holds 40 litres."]),
    steps("5.2.3", "Calculate, in £ per litre, the cost of petrol during Jun. 2024, if the petrol price from Jun. 2024 to Jul. 2024 changed in line with inflation.", 3, [
        ("Petrol price in Jun. 2024 (£ per litre)", 3, 1.42, 0.006, "£1,45 ✓RT × 100/102,2 ✓MA = £1,42 ✓CA (CA from 5.2.2)")],
          ["July's price is June's price plus 2,2%.", "Divide July's price by 1,022."]),
    rub("5.2.4", "Describe the trend in the inflation rate for the period Jul. 2024 to Oct. 2024.", 3, [
        "It remains the same (constant) from July to August (1).", "It decreases from August to September (1).", "It increases from September to October (1)."],
        ["Read TABLE 10 month by month (C from 5.2.1).", "Same, down, then up?"])]

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
     "figure": fig("3.2", "ANSWER SHEET 3.2, a stacked bar graph, NUMBER OF LTE DEVICES PER PROVINCE, 0 to 60 000 000 in steps of 1 000 000 (hatched "
                   "2021, white 2022, black 2023). Each bar's tops: Gauteng 16 000 000 / 34 500 000 / 56 000 000; KwaZulu-Natal 9 000 000 / "
                   "20 500 000 (no 2023 part); Limpopo 4 000 000 / 11 000 000 / 18 500 000; Western Cape 5 500 000 / 12 000 000 / 19 500 000; "
                   "Mpumalanga 3 500 000 / 8 500 000 (no 2023 part); Eastern Cape 3 500 000 / 8 500 000 / 14 000 000; North West 4 000 000 / "
                   "8 000 000 / 12 500 000; Free State 1 000 000 / 5 000 000 / 7 500 000; Northern Cape 2 000 000 / 3 000 000 / 4 500 000."),
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
                   "litre from 1,2 to 1,5: Jul. 2024 1,45; Aug. 2024 1,42; Sep. 2024 1,37; Oct. 2024 1,34."), "items": q52},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P1", "sitting": "November 2025", "total_marks": 150, "time": "3 hours"},
    "sections": [{"title": "Mathematical Literacy", "total": 150, "missions": missions}],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper, hand-transcribed from the SCANNED question paper's page images, the memo and "
                                                           "the special answer book (ANNEXURE A typed; ANSWER SHEET 3.2 and ANNEXURE B cropped from it)."},
        {"n": "2.1.4(c)", "kind": "no_fit", "detail": "'Verify ... VALID' parts (2.1.4(c), 3.1.3(b), 4.1.3(a), 4.1.3(b), 5.2.2) play as steps: the conclusion "
                                                      "mark rides on the last number (the phone sees numbers, not the conclusion)."},
        {"n": "4.1.1", "kind": "no_fit", "detail": "A formula plays as a strict term listing the forms a learner types (all or nothing: the memo's 1 "
                                                   "for the deposit and 1 for the variable cost)."},
        {"n": "5.1.3", "kind": "no_fit", "detail": "The memo accepts several methods and answers (CHF 1 329,54 – 1 337,43; rand R27 228,91 or R27 294,42): "
                                                   "the tolerances span them. A learner converting £ to CHF directly leaves the rand step empty."},
        {"n": "3.2.3", "kind": "no_fit", "detail": "Completing the stacked bar graph is drawn on paper and self-checked against the memo's criteria."},
        {"n": "1.1.3", "kind": "memo_issue", "detail": "The memo's explanation reads '1RT 169,92' where the table and its working use R169,62."},
        {"n": "4.2.1", "kind": "memo_issue", "detail": "The paper asks for V 'rounded to the nearest thousand'; the memo rounds to three decimal places "
                                                       "(0,652, the nearest thousandth)."},
        {"n": "5.2.2", "kind": "memo_issue", "detail": "The August price is read from the graph (memo: 1,41 – 1,43): the full-tank difference is played as "
                                                       "£1,20 ± 0,41 to stay consistent with any reading in that range."},
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
print("total:", sum(i["marks"] for m in missions for i in m["items"]))
