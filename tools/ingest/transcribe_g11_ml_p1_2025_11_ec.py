"""Grade 11 Mathematical Literacy P1 November 2025 (Eastern Cape Department of Education), the whole paper (Questions 1 to 4, 100 marks,
2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, marks, answers and the memo's
working are the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za,
2025 November Grade 11, the question paper zip (English PDF, 10 pages with its two ANSWER SHEETS, text layer) and the memo (English,
8 pages, text layer).

  python tools/ingest/transcribe_g11_ml_p1_2025_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-ml-p1-2025-11-ec/MATHS LITERACY P1 GR11 QP NOV2025_English_watermark.pdf" "uploads/provincial/g11-ml-p1-2025-11-ec/MATHS LITERACY P1 GR11 MEMO NOV2025_English_watermark.pdf" --id g11-ml-p1-2025-11-ec --from-json

The Mathematical Literacy rulings, as in transcribe_ml_p1_2025_11.py: a calculation and a 'verify' -> four whole workings
(provincial.work), the memo's first method and three real errors; a value read off -> num, term or an MCQ of answers; a printed choice
-> mcq as printed; column A to column B -> match; the graphs drawn on the answer sheets (2.2.3, 3.2) -> pick the drawing
(pictures_lower.py: plot); the table completed on the answer sheet (2.2.2) -> one number a cell. The tables are typed. Figure boxes are
in PDF points (scratch figbox.py), each 1% of the page inside its neighbours (ingest pads every crop by 1%)."""
from provincial import Paper

P = Paper("g11-ml-p1-2025-11-ec", 595.32, 841.92, {
    "1.1": [3, 83.8, 152.0, 504.0, 311.0], "3.1": [6, 116.5, 135.5, 470.0, 339.5], "4.1.3": [7, 113.2, 405.8, 518.4, 689.0]}, start=11)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term

GOALS = {"head": ["TEAMS", "SFC", "ORP", "SUN", "AMA", "TSG", "KAC", "CHI", "MGE", "CTC"],
         "rows": [["GOALS SCORED", "73", "60", "46", "35", "35", "32", "31", "30", "27"]]}
BUILDERS = {"head": ["Number of builders", "3", "4", "6", "9", "12"], "rows": [["Number of days", "12", "", "", "", "3"]]}
TB = {"head": ["Classes", "A", "B", "C", "D", "E", "F", "G", "H", "I"],
      "rows": [["Number of antibiotics", "35", "30", "10", "50", "45", "35", "20", "55", "10"],
               ["Number of learners contracted TB", "40", "45", "50", "5", "20", "25", "50", "10", "55"]]}
INVOICE = {"head": ["DESCRIPTION", "QUANTITY", "LITRES", "PRICE PER LITRE", "COST"],
           "rows": [["1. Water-based general purpose cleaner", "2", "25", "R99,00", "R4 950"],
                    ["2. Pine fragrance disinfectant cleaner", "2", "25", "R95,00", "R4 750"],
                    ["Sub Total", "", "", "", "…"], ["VAT (15%)", "", "", "", "R1 455"], ["Total Due", "", "", "", "…"]]}
TARIFF = {"head": ["SIZE", "", "TARIFF (R/kWh) (Excluding VAT)"],
          "rows": [["Block 1", "0 – 350 kWh", "2,216"], ["Block 2", "> 350 – 500 kWh", "2,711"], ["Block 3", "> 500 kWh", "3,226"]]}

# ---- QUESTION 1, the question paper pages 3-4 and the memo page 3 ----
CASH = "Total = R260,00 + R16,70"
q11 = [
    term("1.1.1", "Write down Cynthia's account number.", ["2 457 164 834", "2457164834"], ["Find the Account no. row.", "Ten digits."],
         marks=2),
    num("1.1.2", "Determine how many transfers were from other banks.", 2, 0, "", ["Look at the Drawer's name and Bank rows.",
                                                                                  "How many cheques are listed?"], marks=2),
    answer("1.1.3", "Write down the total amount of cash that she deposited.", 2, ["R276,70", "R260,00", "R1 097,50", "R16,70"],
           ["Cash is notes and coins.", "Find their subtotal."]),
    work("1.1.4", "Calculate the total of the amount deposited.", 2, [
        CASH + " + R340,00 + R480,80\n= R1 097,50",                # the memo's sum, with the slip's R480,80
        CASH + "\n= R276,70",                                      # the cash only
        "Total = R340,00 + R480,80\n= R820,80",                    # the cheques only
        CASH + " + R276,70 + R340,00 + R480,80\n= R1 374,20"],     # the subtotal counted again
        ["The deposit is the cash AND the two cheques.", "Count the cash once."])]
q12 = [
    mcq("1.2.1", "Choose the correct word to make the statement TRUE. The above data is numerical / categorical.", ["numerical", "categorical"],
        0, ["Goals are counted.", "Numbers or names?"]),
    num("1.2.2", "Write down the highest number of goals scored in the league.", 73, 0, "", ["Read the GOALS SCORED row.",
                                                                                            "Which number is the biggest?"], marks=2),
    answer("1.2.3", "List the teams that have the same number of goals scored.", 2, ["AMA and TSG", "KAC and CHI", "CHI and MGE",
                                                                                     "SUN and AMA"],
           ["Look for a number that appears twice.", "35 appears twice."])]
DEFS = ["the likelihood of something happening or not happening", "a record of income and expenditure", "instrument used to collect data",
        "payment made into the bank account", "the difference between the debits and credits", "unemployment insurance fund"]
q13 = [
    {"t": "match", "n": "1.3", "marks": 8, "q": "Choose a definition from COLUMN B that matches the term in COLUMN A (1.3.1 Questionnaire, "
     "1.3.2 Balance, 1.3.3 Probability, 1.3.4 UIF).", "clues": ["A questionnaire is a tool; probability is a chance.",
                                                                "Balance compares debits and credits; UIF is an abbreviation."],
     "left": ["1.3.1 Questionnaire", "1.3.2 Balance", "1.3.3 Probability", "1.3.4 UIF"], "right": DEFS, "a": [2, 4, 0, 5], "each": 2,
     "heads": ["COLUMN A", "COLUMN B (A–F)"]}]

# ---- QUESTION 2, the question paper page 5, the answer sheet page 9 and the memo pages 4-5 ----
B2 = "Balance = R499 900 − R79 984\n= R419 916\n"
q21 = [
    work("2.1.1", "Calculate the amount Rowe saved for the deposit.", 2, [
        "Deposit = {16}/{100} × R499 900\n= R79 984",       # the memo
        "Deposit = 16 × R499 900\n= R7 998 400",            # the % not divided by 100
        "Deposit = {84}/{100} × R499 900\n= R419 916",      # the balance, not the deposit
        "Deposit = {R499 900}/{16}\n= R31 243,75"],         # divided by 16
        ["16% of the price.", "Percent means out of 100."]),
    work("2.1.2", "Rowe secured a loan for the outstanding balance from the bank, agreeing to repay it over 36 months with a 9,5% annual simple "
         "interest rate. Calculate how much Rowe will pay if it takes him exactly 36 months to pay the loan.", 5, [
        B2 + "Interest = {9,5}/{100} × R419 916 × 3\n= R119 676,06\nTotal = R419 916 + R119 676,06\n= R539 592,06",           # the memo
        B2 + "Interest = {9,5}/{100} × R419 916 × 1\n= R39 892,02\nTotal = R419 916 + R39 892,02\n= R459 808,02",             # one year
        B2 + "Interest = {9,5}/{100} × R499 900 × 3\n= R142 471,50\nTotal = R419 916 + R142 471,50\n= R562 387,50",           # on the price
        B2 + "Interest = {9,5}/{100} × R419 916 × 36\n= R1 436 112,72\nTotal = R419 916 + R1 436 112,72\n= R1 856 028,72"],  # 36 years
        ["The loan is the price minus the deposit.", "Simple interest: the same interest each YEAR; 36 months is 3 years."], after=["2.1.1"]),
    work("2.1.3", "Determine the monthly instalment Rowe will pay on the loan.", 2, [
        "Instalment = {R539 592,06}/{36}\n= R14 988,67",    # the memo
        "Instalment = {R539 592,06}/{3}\n= R179 864,02",    # per year
        "Instalment = {R419 916}/{36}\n= R11 664,33",       # the interest left out
        "Instalment = {R539 592,06}/{12}\n= R44 966,01"],   # 12 months
        ["Share the total from 2.1.2 over the months.", "How many months?"], after=["2.1.2"]),
    work("2.1.4", "In the showroom there were different colours of the car Rowe wants to buy (2 red, 3 silver, 4 grey and 5 black). Calculate "
         "the probability, as a decimal, that Rowe will choose a silver car.", 3, [
        "P = {3}/{14}\n= 0,214…\n≈ 0,21",      # the memo
        "P = {3}/{4}\n= 0,75\n≈ 0,75",          # the four colours as the total
        "P = {3}/{11}\n= 0,272…\n≈ 0,27",      # the silver cars left out of the total
        "P = {1}/{14}\n= 0,071…\n≈ 0,07"],     # one silver car
        ["How many cars are there altogether?", "How many are silver?"])]
q22 = [
    answer("2.2.1", "Derive a mathematical formula that represents the information given in the table.", 2, [
        "Number of builders × number of days = 36", "Number of builders + number of days = 15", "Number of days = 4 × number of builders",
        "Number of days = 36 × number of builders"],
        ["3 × 12 and 12 × 3: what stays the same?", "More builders, fewer days."]),
    num("2.2.2(a)", "Complete TABLE 3: the number of days for 4 builders.", 9, 0, "days", ["Builders × days = 36.", "36 ÷ 4."]),
    num("2.2.2(b)", "Complete TABLE 3: the number of days for 6 builders.", 6, 0, "days", ["Builders × days = 36.", "36 ÷ 6."]),
    num("2.2.2(c)", "Complete TABLE 3: the number of days for 9 builders.", 4, 0, "days", ["Builders × days = 36.", "36 ÷ 9."]),
    draw("2.2.3", "Use the ANSWER SHEET to draw a graph to represent the data in TABLE 3.", 4,
         [["All the points plotted: (3 ; 12), (4 ; 9), (6 ; 6), (9 ; 4), (12 ; 3)", 3], ["The points joined with a smooth curve", 1]],
         ["Plot builders across and days up.", "Inverse proportion makes a curve, not a straight line."],
         memo="The memo's graph: the five points joined by a smooth curve.", after=["2.2.2(a)", "2.2.2(b)", "2.2.2(c)"]),
    mcq("2.2.4", "Choose the correct word to make the statement false. The relationship represented by the graph in QUESTION 2.2.3 is direct / "
        "indirect proportion.", ["direct", "indirect"], 0, ["More builders, fewer days: which proportion is that?",
                                                            "The statement must be FALSE."])]
q23 = [
    work("2.3", "Joyce's salary is R20 600,00 per month. Last year her monthly salary was R20 000,00. Calculate the inflation rate.", 4, [
        "Inflation rate = {R20 600 − R20 000}/{R20 000} × 100\n= 3%",        # the memo
        "Inflation rate = {R20 600 − R20 000}/{R20 600} × 100\n= 2,91%",     # divided by the new salary
        "Inflation rate = {R20 600}/{R20 000} × 100\n= 103%",                # the old salary not subtracted
        "Inflation rate = {R20 600 − R20 000}/{100}\n= 6%"],                 # divided by 100
        ["The increase as a percentage of LAST year's salary.", "Increase ÷ old × 100."])]

# ---- QUESTION 3, the question paper page 6, the answer sheet page 10 and the memo page 6 ----
q31 = [
    work("3.1.1", "Determine the percentage of bachelor passes obtained by the Sarah Baartman District.", 3, [
        "% = 100 − (20 + 8 + 26 + 12 + 27)\n= 100 − 93\n= 7%",          # the memo, without its slip (it lists 7 in the bracket)
        "% = 100 − (20 + 8 + 26 + 12)\n= 100 − 66\n= 34%",              # Nelson Mandela missed
        "% = 100 ÷ 6\n= 16,666…\n= 16,67%",                              # equal shares
        "% = (20 + 8 + 26 + 12 + 27) − 100\n= 93 − 100\n= −7%"],        # subtracted the wrong way round
        ["A pie chart adds up to 100%.", "Subtract the five given percentages."]),
    work("3.1.2", "Calculate the number of candidates with bachelor passes in Buffalo City.", 3, [
        "Buffalo City = {26}/{100} × 20 910\n= 5 436,6\n≈ 5 437 learners",     # the memo
        "Buffalo City = {26}/{100} × 20 910\n= 5 436,6\n≈ 5 436 learners",     # rounded down
        "Buffalo City = 26 × 20 910\n= 543 660\n≈ 543 660 learners",           # the % not divided by 100
        "Buffalo City = {20 910}/{26}\n= 804,23\n≈ 804 learners"],             # divided by 26
        ["26% of 20 910.", "People are whole numbers: round properly."]),
    work("3.1.3", "Determine the median percentage of bachelors passes.", 3, [
        "In order: 7 ; 8 ; 12 ; 20 ; 26 ; 27\nMedian = {12 + 20}/{2}\n= 16%",               # the memo
        "In the chart's order: 20 ; 8 ; 26 ; 12 ; 27 ; 7\nMedian = {26 + 12}/{2}\n= 19%",    # not arranged
        "In order: 7 ; 8 ; 12 ; 20 ; 26 ; 27\nMedian = 12 + 20\n= 32%",                     # not halved
        "In order: 8 ; 12 ; 20 ; 26 ; 27\nMedian = the 3rd value\n= 20%"],                   # Sarah Baartman left out
        ["Arrange all six percentages first.", "With six values the median lies between the 3rd and the 4th."], after=["3.1.1"]),
    answer("3.1.4", "Write down the district that has the least percentage of bachelor passes.", 2,
           ["Sarah Baartman", "Amathole West", "Chris Hani West", "Nelson Mandela"],
           ["Which slice is the smallest?", "Your answer to 3.1.1 helps."]),
    work("3.1.5", "Calculate the mean percentage of bachelor passes in Cluster B.", 3, [
        "Mean = {7 + 8 + 12 + 20 + 26 + 27}/{6}\n= {100}/{6}\n= 16,67%",     # the memo
        "Mean = {8 + 12 + 20 + 26 + 27}/{5}\n= {93}/{5}\n= 18,6%",           # Sarah Baartman left out
        "Mean = {7 + 8 + 12 + 20 + 26 + 27}/{5}\n= {100}/{5}\n= 20%",        # divided by 5
        "Mean = {12 + 20}/{2}\n= {32}/{2}\n= 16%"],                           # the median's middle pair
        ["Mean = sum ÷ number of districts.", "There are six districts."], after=["3.1.1"]),
    work("3.1.6", "Determine the probability of randomly selecting a district with a bachelor pass of less than 10%. Write your answer as a "
         "simplified fraction.", 3, [
        "P = {2}/{6}\n= {1}/{3}",      # the memo
        "P = {2}/{100}\n= {1}/{50}",   # out of 100
        "P = {4}/{6}\n= {2}/{3}",      # the districts of 10% or more
        "P = {6}/{2}\n= 3"],           # upside down
        ["Which districts have less than 10%?", "Out of how many districts?"])]
q32 = [
    draw("3.2", "Draw a scatter plot to illustrate the data in TABLE 4. Use the ANSWER SHEET provided for QUESTION 3.2.", 6,
         [["Every three points plotted correctly", 3], ["A title", 1], ["The x- and y-axes labelled", 2]],
         ["Antibiotics across, learners with TB up.", "A scatter plot's points are not joined."],
         memo="The memo's scatter plot: the nine points, its title and both axes labelled.")]

# ---- QUESTION 4, the question paper pages 7-8 and the memo pages 7-8 ----
C4 = "Cost = R4 950 + R4 750\n= R9 700\n"
q41 = [
    work("4.1.1", "Calculate the total cost for ALL the material bought by Lily, including VAT.", 4, [
        C4 + "= R9 700 + R1 455\n= R11 155",                         # the memo
        C4 + "= R9 700 − R1 455\n= R8 245",                          # VAT subtracted
        C4 + "= R9 700 × 1,15 + R1 455\n= R12 610",                  # VAT added twice
        "Cost = R99 + R95\n= R194\n= R194 + R1 455\n= R1 649"],      # the prices per litre added
        ["Add the two costs for the sub total.", "Then add the VAT once."]),
    work("4.1.2", "Lily states that the profit she makes from selling ONE 25 litre (25 ℓ) Pine fragrance disinfectant cleaner is R450,00, if she "
         "sells a litre at R135,00. Verify, showing ALL calculations, if her statement is VALID.", 6, [
        "Profit per litre = R135 − R95\n= R40\nProfit = R40 × 25\n= R1 000\nR1 000, not R450: her statement is INVALID",        # the memo
        "Profit per litre = R135 − R99\n= R36\nProfit = R36 × 25\n= R900\nR900, not R450: her statement is INVALID",            # the other cleaner
        "Profit per litre = R135 − R95\n= R40\nProfit = R40 × 50\n= R2 000\nR2 000, not R450: her statement is INVALID",        # both containers
        "Profit per litre = R95 − R135\n= −R40\nProfit = −R40 × 25\n= −R1 000\nA loss, not R450: her statement is INVALID"],   # the wrong way round
        ["Profit per litre = selling price − cost price.", "One container holds 25 litres."]),
    answer("4.1.3(a)", "Give the value(s) of the point marked (W) on the graph and explain the meaning of that point.", 2, [
        "(5 ; 725): income equals expenses, the break-even point", "(725 ; 5): income equals expenses, the break-even point",
        "(5 ; 725): the point of the biggest profit", "(0 ; 250): the cost before any litre is sold"],
        ["Read the number of litres first, then the rands.", "What is true where the two lines cross?"]),
    answer("4.1.3(b)", "Write down the formula for Lily's expenses if she must pay rent of R200. Cost = … + …", 2, [
        "Cost = R200 + R95 × number of litres", "Cost = R95 + R200 × number of litres", "Cost = R200 + R135 × number of litres",
        "Cost = R200 × R95 × number of litres"],
        ["The rent is paid once.", "Each litre costs her R95."])]
q42 = [
    work("4.2", "A South African company imports goods worth €45 000 from Europe. The exchange rate is R1 = €0,049669. Calculate the cost of "
         "the goods in South African Rand.", 3, [
        "R1 = €0,049669\nCost = {€45 000}/{€0,049669}\n= R905 997,70",      # the memo
        "R1 = €0,049669\nCost = €45 000 × 0,049669\n= R2 235,11",           # multiplied
        "R1 = €0,049669\nCost = {€0,049669}/{€45 000}\n= R0,0000011",       # upside down
        "R1 = €0,049669\nCost = {€45 000}/{€0,49669}\n= R90 599,77"],       # the rate misread
        ["One rand buys only €0,05: will the rand amount be bigger or smaller?", "Divide the euros by 0,049669."])]
q43 = [
    work("4.3", "The March Test results for nine Grade 11 Mathematical Literacy learners, out of 75 marks: 15 ; 60 ; 75 ; 67 ; 68 ; 73 ; 60 ; "
         "75 ; 58. The teacher claimed that the range of the class is 80%. Show by means of calculations whether the teacher's claim is VALID or "
         "not.", 5, [
        "Range = 75 − 15\n= 60\nRange as a % = {60}/{75} × 100\n= 80%\nThe claim is VALID",          # the memo
        "Range = 75 − 58\n= 17\nRange as a % = {17}/{75} × 100\n= 22,67%\nThe claim is NOT VALID",   # 15 overlooked
        "Range = 75 − 15\n= 60\nRange as a % = {60}/{100} × 100\n= 60%\nThe claim is NOT VALID",     # out of 100
        "Range = 75 + 15\n= 90\nRange as a % = {90}/{75} × 100\n= 120%\nThe claim is NOT VALID"],    # added
        ["Range = highest − lowest.", "The test was out of 75."])]
B1 = "Block 1 = 350 kWh × R2,216 = R775,60\n"
q44 = [
    work("4.4", "Use TABLE 5 to calculate how much a resident in this city pays a month, including VAT, when they use 374 kWh of electricity.", 6, [
        B1 + "Block 2 = 24 kWh × R2,711 = R65,064\nTotal = R775,60 + R65,064 = R840,664\nWith VAT = R840,664 × 1,15\n= R966,76",     # the memo
        "Block 1 = 374 kWh × R2,216 = R828,78\nBlock 2 = 0 kWh × R2,711 = R0\nTotal = R828,78 + R0 = R828,78\nWith VAT = R828,78 × 1,15\n"
        "= R953,10",                                                                                                                # one block
        B1 + "Block 2 = 150 kWh × R2,711 = R406,65\nTotal = R775,60 + R406,65 = R1 182,25\nWith VAT = R1 182,25 × 1,15\n= R1 359,59",  # all of block 2
        B1 + "Block 2 = 24 kWh × R2,711 = R65,064\nTotal = R775,60 + R65,064 = R840,664\nVAT not added\n= R840,66"],                 # no VAT
        ["The first 350 kWh at the Block 1 rate, the rest at Block 2.", "Then add 15% VAT."])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Banking", "marks": 8,
     "lead": "TABLE 1 presents the deposit slip details for funds to be credited to Cynthia Francis's account.",
     "figure": P.fig("1.1", "TABLE 1: Cynthia Francis's deposit slip, CFO Bank, 15 December 2024: notes R260,00, coins R16,70, subtotal "
                            "R276,70; cheques from 1. A Troyd (BBC, Jamestown) R340,00 and 2. Z Pasi (DBE, Bloemfontein) R480,80; the total "
                            "left blank; account no. 2 4 5 7 1 6 4 8 3 4."), "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Data", "marks": 6, "table": GOALS,
     "lead": "Zizo, a soccer fan, collected and analysed 2024/2025 goals scored for the Premium Soccer League. The goals scored for the league "
             "are indicated below.\nTABLE 2: 2024/2025 PREMIER SOCCER LEAGUE GOALS SCORED", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Terms", "marks": 8, "lead": "Choose a definition from COLUMN B that matches the term in "
                                                                                 "COLUMN A.", "items": q13},
    {"id": "2.1", "title": "Question 2.1", "kind": "Loans and probability", "marks": 12,
     "lead": "Rowe has been driving a demo car for the past four years. Over these four years he managed to save 16% as a deposit of the price "
             "of the brand new car he wants to buy. He is interested in buying a 2025 Cherry Tiggo 7 Pro Max.\nRowe visited the dealer to "
             "purchase the car. The price of the car is R499 900,00.\nNOTE: Focus will be on the price of the car only (no other initial "
             "costs).", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Inverse proportion", "marks": 11, "table": BUILDERS,
     "lead": "Waterfront High School wants to renovate their netball court. The school asked builders from the community to volunteer and "
             "assist with the renovations. The school estimated that it would take 3 builders 12 days to finish renovations, or it would take "
             "12 builders 3 days to finish renovations. The table below displays this information.\nTABLE 3: NUMBER OF BUILDERS AND DAYS TO "
             "RENOVATE THE NETBALL COURT", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Inflation", "marks": 4, "lead": "Joyce's salary has increased since last year.",
     "items": q23},
    {"id": "3.1", "title": "Question 3.1", "kind": "Data handling", "marks": 17,
     "lead": "The pie chart below shows the percentage of bachelor passes obtained by candidates in Cluster B Districts. The total number of "
             "bachelors passes in Cluster B Districts is 20 910.",
     "figure": P.fig("3.1", "A pie chart, BACHELOR PASS PER DISTRICT: Amathole East 20%, Amathole West 8%, Buffalo City 26%, Chris Hani West "
                            "12%, Nelson Mandela 27%, and Sarah Baartman's slice with no percentage."), "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Scatter plots", "marks": 6, "table": TB,
     "lead": "A clinic recorded the distribution of a few antibiotics to a sample group of learners at a school to see whether they contracted "
             "TB. The sample group was made up of nine classes. The results are shown in the table below.\nTABLE 4: THE RESULTS OF LEARNERS "
             "WHO CONTRACTED TB", "items": q32},
    {"id": "4.1", "title": "Question 4.1", "kind": "Income and expenditure", "marks": 14, "table": INVOICE,
     "lead": "The invoice given below lists cleaning materials bought by Lily.\nINCOME AND EXPENDITURE\nThe graph shows the cost and selling "
             "price of all-purpose cleaner material per litre.",
     "figure": P.fig("4.1.3", "A graph, COST AND SELLING PRICE OF ALL-PURPOSE CLEANER: Cost/Selling price (Rands) against Number of litres "
                              "(0 to 30); the INCOME line from (0 ; 0) and the EXPENSES line from about R250 cross at W, at 5 litres."),
     "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Exchange rates", "marks": 3, "lead": "Goods imported from Europe are paid for in rand.",
     "items": q42},
    {"id": "4.3", "title": "Question 4.3", "kind": "Data handling", "marks": 5,
     "lead": "Below are the March Test results for nine Grade 11 Mathematical Literacy learners. The test was out of 75 marks.\n15 ; 60 ; 75 ; "
             "67 ; 68 ; 73 ; 60 ; 75 ; 58", "items": q43},
    {"id": "4.4", "title": "Question 4.4", "kind": "Tariffs", "marks": 6, "table": TARIFF,
     "lead": "The City of FY2024/25 split the residential prepaid tariffs into Prepaid Low (indigent) and Prepaid High. Electricity tariffs for "
             "Prepaid Low are shown in TABLE 5.\nTABLE 5: RESIDENTIAL PREPAID LOW INDIGENT (FY 2024/25)", "items": q44},
]
P.finish(missions,
         {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P1", "sitting": "November 2025", "total_marks": 100,
          "time": "2 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "1.1.4", "kind": "memo_issue", "detail": "The memo adds R480,00 for Z Pasi's cheque; the slip shows R480,80, which gives the "
                                                         "memo's own total R1 097,50. The right option adds R480,80; R1 096,70 is in no "
                                                         "option."},
          {"n": "3.1.1", "kind": "memo_issue", "detail": "The memo's bracket lists 7 with the five printed percentages (12 + 26 + 8 + 20 + 27 + "
                                                         "7) yet writes 93; the right option subtracts the five printed ones."},
          {"n": "4.1.3(a)", "kind": "memo_issue", "detail": "The memo answers W(5 ; 675), from the text's R135 a litre and R200 rent; the graph "
                                                            "printed draws income at R145 a litre and expenses from R250, which cross at (5 ; "
                                                            "725), where W is marked. The question reads W off the graph: the right option is "
                                                            "(5 ; 725); 675 is in no option."},
          {"n": "2.2.2(a)", "kind": "no_fit", "detail": "The table completed on the answer sheet: one number a cell, one mark each, as the "
                                                        "memo's 1A + 1A + 1A. The answer sheet prints 7 builders where TABLE 3 and the memo "
                                                        "have 9; the parts follow TABLE 3."},
          {"n": "2.2.3", "kind": "no_fit", "detail": "The graph (2.2.3) and the scatter plot (3.2) drawn on the answer sheets play as pick the "
                                                     "drawing."}],
         {"1": 22, "2": 27, "3": 23, "4": 28}, 100,
         {"2.1.2": ["2.1.1"], "2.1.3": ["2.1.2"], "2.2.3": ["2.2.2(a)", "2.2.2(b)", "2.2.2(c)"], "3.1.3": ["3.1.1"], "3.1.5": ["3.1.1"]},
         "Questions 1 to 4 (the whole paper)")
