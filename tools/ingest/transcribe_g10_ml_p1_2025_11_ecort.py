"""Grade 10 Mathematical Literacy P1 November 2025 (Eastern Cape Department of Education, O.R. Tambo Coastal District), the whole paper
(Questions 1 to 4, 75 marks), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, marks,
answers and the memo's working are the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md):
re-published by Stanmore Secondary (stanmorephysics.com) as one scanned PDF, the question paper (pages 1-8) then the marking guidelines
(pages 9-16), no text layer: read from its page images (100 dpi). Split into '<id> QP.pdf' and '<id> MG.pdf'.

  python tools/ingest/transcribe_g10_ml_p1_2025_11_ecort.py
  python tools/ingest/ingest.py "uploads/provincial/g10-ml-p1-2025-11-ecort/g10-ml-p1-2025-11-ecort QP.pdf" "uploads/provincial/g10-ml-p1-2025-11-ecort/g10-ml-p1-2025-11-ecort MG.pdf" --id g10-ml-p1-2025-11-ecort --from-json

The Mathematical Literacy rulings, as in transcribe_g10_ml_p1_2024_11_nw.py: a calculation or a 'verify' -> four whole workings
(provincial.work); a word read off -> term or an MCQ of answers; a definition or an explanation -> statements; fixed and variable
expenses (2.1.2) and interest versus interest rate (3.2.1) -> sorts. The till slip, the budget, the water tariff, the bank fees and the car
lengths are typed as tables. Question 2.2 and Question 4 repeat items of the North West Grade 10 P1 of 2024 (the water tariff, the car colours and
lengths); the workings are the same. Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-ml-p1-2025-11-ecort", 595.44, 841.92, {
    "1.2": [4, 63, 65, 494, 301], "4.1": [7, 97, 216, 472, 504]}, start=3)
work, answer, num, draw, stmt, mcq, term, sort = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term, P.sort

BUDGET = {"head": ["INCOME", "AMOUNT", "EXPENDITURE", "AMOUNT"],
          "rows": [["Allowance", "R3 800", "Rent", "R1 500"], ["Salary", "R1 800", "Food", "R1 700"], ["", "", "Clothes", "R300"],
                   ["", "", "Entertainment", "R250"], ["", "", "Others", "R700"], ["Total", "", "", "R4 450"]]}
WATER = {"head": ["CONSUMPTION", "TARIFF IN RANDS (VAT INCLUDED)"],
         "rows": [["0 kℓ – 6 kℓ", "R27,80"], ["6 kℓ – 20 kℓ", "R34,06"], ["20 kℓ – 50 kℓ", "R35,14"], ["50 kℓ – 100 kℓ", "R36,34"],
                  ["100 kℓ – 200 kℓ", "R38,34"], ["200 kℓ – 300 kℓ", "R40,62"], ["300 kℓ +", "R51,16"]]}
FEES = {"head": ["FNB BANK ACCOUNT FEES", ""],
        "rows": [["Monthly account fee", "R65,00"], ["Cellphone banking", "R0,00"], ["Cash withdrawals (FNB Bank ATM): first R1 500", "R0,00"],
                 ["Cash withdrawals (FNB Bank ATM): more than R1 500", "R12,00 + R1,20 per R100 (or part thereof)"],
                 ["Cash withdrawals (other bank ATM)", "R15,00"]]}

# the till slip, typed (Murci 2026-10-13: "that pick'n'pay receipt is not clearly visible": a 461 x 946 scan drawn 161 px wide in the
# frame; typed, it is crisp at any size and a screen reader reads it)
SLIP = {"head": ["PICK N PAY (cashier: Mihlali)", "QUANTITY @ PRICE", "AMOUNT"],
        "rows": [["Hamburger buns (6 each)", "8 @ 10.99", "(1.1.2)"], ["Fruit jellybeans", "5 @ 25.00", "125.00"],
                 ["Maynards wine gum roll", "20 @ 7.99", "159.80"], ["Tomatoes 1 kg", "", "17.99 #"], ["Simba chips", "10 @ 15.00", "150.00"],
                 ["Crisp lettuce", "4 @ 12.99", "51.96 #"], ["Large carrier bag", "3 @ 0.50", "1.50"],
                 ["Dairy Milk Oreo slab 120 g", "10 @ 25.99", "259.90"], ["Coke Light 2 L", "10 @ 16.49", "164.90"],
                 ["DUE VAT INCL", "", "1 018.97"], ["TENDER: Mastercard", "", "1 018.97"], ["TOTAL ITEMS", "", "71"],
                 ["TAX INVOICE: VAT incl / VAT value", "1 018.97", "123.79"], ["# ZERO-RATED", "", "69.95"],
                 ["VAT reg no. 4090105588", "24.02.2020 18:54", ""]]}

# ---- QUESTION 1, the question paper pages 3-4 and the memo pages 12-13 ----
NOVAT = "R1 018,97 − R69,95 = R949,02\n"
q11 = [
    stmt("1.1.1", "What is the meaning of the hashtag symbol (#) that is found next to certain prices?", 2,
         ["Those are the items that are excluded from VAT (zero-rated).", "The items marked # are zero-rated: no VAT is charged on them."],
         ["Those items are on special.", "Those items were returned.", "Those items cost more than R50.", "Those items were paid in cash."],
         ["Look at '# ZERO-RATED' near the bottom of the slip.", "Tomatoes and lettuce are basic foods."], 2),
    work("1.1.2", "Calculate the total cost of the hamburger buns.", 2, [
        "Total = R10,99 × 8\n= R87,92",     # the memo
        "Total = R10,99 × 6\n= R65,94",     # the buns per pack as the quantity
        "Total = R10,99 + 8\n= R18,99",     # added
        "Total = R10,99 × 48\n= R527,52"],  # every bun priced
        ["8 packs at R10,99 each.", "Multiply."]),
    answer("1.1.3", "Write the cost of one bag of jelly beans as a ratio to the cost of one bag of chips. Give your answer as a simplified ratio.", 2,
           ["5 : 3", "3 : 5", "25 : 15", "125 : 150"], ["R25 : R15.", "Divide both by 5; keep the order."]),
    work("1.1.4", "Show how the VAT amount of R123,79 has been calculated.", 3, [
        NOVAT + "R949,02 ÷ 1,15 = R825,23\nVAT = R949,02 − R825,23 = R123,79",       # the memo
        "R1 018,97 ÷ 1,15 = R886,06\nVAT = R1 018,97 − R886,06\n= R132,91",          # the zero-rated items taxed
        NOVAT + "R949,02 × 15% = R142,35\nVAT = R142,35",                            # 15% of the VAT-inclusive amount
        NOVAT + "R949,02 × 1,15 = R1 091,37\nVAT = R1 091,37 − R949,02 = R142,35"],  # VAT added again
        ["Take the zero-rated items out first.", "The amount includes VAT: divide by 1,15."])]
q12 = [
    term("1.2.1", "Name the type of graph that Mrs Magadi used.", ["bar graph", "vertical bar graph", "column graph", "bar chart",
                                                                     "single bar graph"],
         ["Each month has a bar.", "The bars stand up from the axis."], marks=2),
    work("1.2.2", "How many learners does Mrs Magadi teach in total?", 2, [
        "Total = 3 + 4 + 2 + 3 + 8 + 10 + 6 + 1 + 7 + 8 + 4 + 7\n= 63 learners",      # the memo
        "Total = 3 + 4 + 2 + 3 + 8 + 10 + 6 + 7 + 8 + 4 + 7\n= 62 learners",          # August left out
        "Total = 12 months × 10\n= 120 learners",                                     # the tallest bar for every month
        "Total = 3 + 4 + 2 + 3 + 8 + 10 + 6 + 1 + 7 + 8 + 4 + 8\n= 64 learners"],     # December misread
        ["Read every bar's height.", "Add all twelve."]),
    answer("1.2.3", "Write down the month(s) in which the second-most birthdays are celebrated.", 2,
           ["May and October", "June", "May only", "September and December"], ["June has the most.", "Which months come next?"]),
    work("1.2.4", "Determine the probability of randomly selecting a month with fewer than 4 students, as a decimal rounded to two decimal places.", 3, [
        "Months with fewer than 4: Jan, Mar, Apr, Aug\nP = {4}/{12}\n= 0,33",      # the memo
        "Months with fewer than 4: Jan, Mar, Apr, Aug, Nov\nP = {5}/{12}\n= 0,42", # 4 counted as fewer than 4
        "Learners in those months: 3 + 2 + 3 + 1 = 9\nP = {9}/{63}\n= 0,14",       # learners, not months
        "Months with fewer than 4: Jan, Mar, Apr, Aug\nP = {12}/{4}\n= 3"],        # upside down
        ["Count the months whose bar is below 4.", "Out of 12 months."])]

# ---- QUESTION 2, the question paper pages 4-5 and the memo page 13 ----
q21 = [
    answer("2.1.1", "How much does Mavis spend on entertainment?", 2, ["R250", "R300", "R700", "R4 450"],
           ["Read the expenditure column.", "Entertainment's row."]),
    sort("2.1.2", "List Mavis's expenses as either variable or fixed expenses.", ["Fixed expenses", "Variable expenses"],
         [("Rent: R1 500", 0), ("Food: R1 700", 1), ("Clothes: R300", 1), ("Entertainment: R250", 1), ("Others: R700", 1),
          ("Total: R1 500", 0), ("Total: R2 950", 1)],
         ["A fixed expense is the same every month.", "Which amount does not change?"]),
    work("2.1.3", "Calculate her total monthly income.", 2, [
        "R3 800 + R1 800\n= R5 600",      # the memo
        "R3 800 − R1 800\n= R2 000",      # subtracted
        "R3 800 + R1 800 − R4 450\n= R1 150",   # the expenditure taken off
        "R3 800\n= R3 800"],              # the allowance only
        ["Income is the allowance and the salary.", "Add them."]),
    work("2.1.4", "Calculate the rent as a percentage of the total expenditure.", 2, [
        "{R1 500}/{R4 450} × 100\n= 33,71%",      # the memo
        "{R1 500}/{R5 600} × 100\n= 26,79%",      # the income as the total
        "{R4 450}/{R1 500} × 100\n= 296,67%",     # upside down
        "{R1 500}/{R4 450}\n= 0,34%"],            # not × 100
        ["Part ÷ whole × 100.", "The whole is the total expenditure."])]
B6 = "0 to 6 kℓ: 6 × R27,80 = R166,80\n"
q22 = [
    stmt("2.2.1", "Define the term tariff.", 2,
         ["A tariff is a charge per unit for a service rendered.", "A fixed rate charged for each unit of a service such as water."],
         ["The total of a monthly bill.", "A tax added to goods.", "The amount of water used in a month.", "A fine for late payment."],
         ["Water is charged per kilolitre.", "Per unit."], 2),
    term("2.2.2", "Write VAT in full.", ["value added tax", "value-added tax"], ["V, A, T.", "A tax added to the value of goods."], marks=2),
    answer("2.2.3", "What is the current VAT % in South Africa?", 2, ["15%", "14%", "10%", "16%"], ["It has been the rate since 2018.",
                                                                                                    "One and a half tens."]),
    work("2.2.4", "Mr Sibiya claims that 18 kℓ of water will cost more than R550 for 2024/2025. Verify, by calculating the cost of 18 kℓ, if his "
         "statement is CORRECT.", 5, [
        B6 + "6 to 18 kℓ: 12 × R34,06 = R408,72\nTotal = R166,80 + R408,72\n= R575,52\nMore than R550: his statement is CORRECT",       # the memo
        "0 to 18 kℓ: 18 × R27,80 = R500,40\n6 to 18 kℓ: none\nTotal = R500,40 + R0\n= R500,40\nLess than R550: his statement is NOT CORRECT",  # one tariff
        B6 + "6 to 18 kℓ: 18 × R34,06 = R613,08\nTotal = R166,80 + R613,08\n= R779,88\nMore than R550: his statement is CORRECT",       # all 18 kℓ again
        B6 + "6 to 18 kℓ: 12 × R35,14 = R421,68\nTotal = R166,80 + R421,68\n= R588,48\nMore than R550: his statement is CORRECT"],      # the next band's tariff
        ["The first 6 kℓ cost one tariff; the next 12 kℓ another.", "Which band does 6 kℓ to 18 kℓ fall in?"])]

# ---- QUESTION 3, the question paper page 6 and the memo page 14 ----
q3 = [
    answer("3.1.1", "What is the monthly fee of having this account?", 2, ["R65,00", "R0,00", "R12,00", "R15,00"],
           ["Read the first row of the table.", "Monthly account fee."]),
    work("3.1.2", "Endinako withdraws R1 700 at an FNB Bank ATM. Calculate what this withdrawal will cost her.", 3, [
        "R1 700 − R1 500 = R200 over R1 500\nCost = R12,00 + (R1,20 × 2)\n= R14,40",       # the memo
        "R1 700 − R1 500 = R200 over R1 500\nCost = R1,20 × 2\n= R2,40",                   # the R12,00 left out
        "R1 700 ÷ 100 = 17\nCost = R12,00 + (R1,20 × 17)\n= R32,40",                       # the free R1 500 charged
        "R1 700 − R1 500 = R200 over R1 500\nCost = R15,00\n= R15,00"],                    # the other bank's fee
        ["The first R1 500 is free.", "How many R100s over R1 500?"]),
    answer("3.1.3", "Endinako had to transfer R500 to her mother's account. She decided to use her cellphone banking to do this. How much did this "
                    "transaction cost her?", 2, ["R0,00", "R12,00", "R65,00", "R15,00"], ["Read the cellphone banking row.", "It costs nothing."]),
    sort("3.2.1", "Differentiate between interest and interest rate.", ["Interest", "Interest rate"],
         [("The actual amount of money earned on an investment or paid on a loan", 0), ("Measured in rands", 0),
          ("The percentage at which interest is calculated on a loan or investment", 1), ("Written as a percentage, e.g. 9,5% p.a.", 1)],
         ["One is an amount, the other a percentage.", "Which is in rands?"]),
    work("3.2.2", "Endinako invests R2 000 into a fixed deposit account for a period of two years. The bank offers her simple interest at a rate of "
         "9,5% p.a. Calculate the value of her investment after two years.", 4, [
        "Interest per year = R2 000 × 0,095 = R190\nTotal interest = R190 × 2 = R380\nTotal value = R2 000 + R380\n= R2 380",       # the memo
        "Interest per year = R2 000 × 0,095 = R190\nTotal interest = R190 × 2 = R380\nTotal value = R380\n= R380",                 # the interest only
        "Interest per year = R2 000 × 0,95 = R1 900\nTotal interest = R1 900 × 2 = R3 800\nTotal value = R2 000 + R3 800\n= R5 800",  # 9,5% as 0,95
        "Year 1: R2 000 × 1,095 = R2 190\nYear 2: R2 190 × 1,095 = R2 398,05\nTotal value = R2 398,05\n= R2 398,05"],              # compounded
        ["Simple interest is on R2 000 each year.", "Add the interest to the R2 000."])]

# ---- QUESTION 4, the question paper pages 7-8 and the memo pages 15-16 ----
SUM = "Sum = 4,1 + 4,3 + 5,8 + 4,1 + 2,9 + 5,1 + 3,6 + 2,5 + 4,7 + 4,4 + 4,2 + 5,0 = 50,7\n"
SORT = "2,5 ; 2,9 ; 3,6 ; 4,1 ; 4,1 ; 4,2 ; 4,3 ; 4,4 ; 4,7 ; 5,0 ; 5,1 ; 5,8\n"
q41 = [
    term("4.1.1", "Name the type of chart shown above.", ["pie chart", "pie graph", "pie diagram"],
         ["The chart is a circle cut into slices.", "Each slice is a percentage."], marks=2),
    mcq("4.1.2", "State whether the above data is categorical or numerical.", ["Categorical", "Numerical"], 0,
        ["Are the colours numbers or groups?", "Named groups are categorical."], marks=2),
    work("4.1.3", "Calculate the percentage of red cars.", 3, [
        "35% + 9% + 6% + 15% + 24% + 3% = 92%\nRed = 100% − 92%\n= 8%",     # the memo
        "35% + 9% + 6% + 15% + 24% = 89%\nRed = 100% − 89%\n= 11%",         # Other left out
        "7 colours and Other share 100%\nRed = 100% ÷ 8\n= 12,5%",           # shared equally
        "35% + 9% + 6% + 15% + 24% + 3% = 82%\nRed = 100% − 82%\n= 18%"],   # an addition slip
        ["What do all the slices add up to?", "Add every labelled percentage, Other included."]),
    work("4.1.4", "During this specific month, 350 cars were sold. Calculate the number of beige cars sold.", 2, [
        "350 × 24%\n= 84 cars", "350 × 35%\n= 122,5 cars", "350 ÷ 24\n= 14,58 cars", "350 × 24\n= 8 400 cars"],
        ["What percentage of the cars were beige?", "Find that percentage of 350."]),
    stmt("4.1.5", "Mr Bernard claims that a white car doesn't attract dirt easily. Give another valid reason why a white car might be a better "
                  "option to buy.", 2,
         ["A white car is more visible on the road, so it is easier to spot.", "White paint hides imperfections well.",
          "A white car can improve the car's resale value.", "White car paint is cheaper than colourful paint."],
         ["A white car uses less fuel than other cars.", "A white car does not need to be insured.", "A white car can go faster than other cars."],
         ["Think of safety, repairs and selling the car later.", "White is the most popular colour in the chart."], 2)]
LENGTHS = {"head": ["CAR LENGTHS (m)", "", "", "", "", ""],
           "rows": [["4,1", "4,3", "5,8", "4,1", "2,9", "5,1"], ["3,6", "2,5", "4,7", "4,4", "4,2", "5,0"]]}
q42 = [
    work("4.2.1", "Calculate the mean length of the given data in the set.", 3, [
        SUM + "Mean = {50,7}/{12}\n= 4,23 m", SUM + "Mean = {50,7}/{11}\n= 4,61 m", SUM + "Mean = {12}/{50,7}\n= 0,24 m",
        SUM + "Mean = {2,5 + 5,8}/{2}\n= 4,15 m"],
        ["Add all the lengths.", "Divide by how many lengths there are."]),
    work("4.2.2", "Calculate the median of the data.", 4, [
        SORT + "Middle values: 4,2 and 4,3\nMedian = {4,2 + 4,3}/{2}\n= 4,25 m",
        "4,1 ; 4,3 ; 5,8 ; 4,1 ; 2,9 ; 5,1 ; 3,6 ; 2,5 ; 4,7 ; 4,4 ; 4,2 ; 5,0\nMiddle values: 5,1 and 3,6\nMedian = {5,1 + 3,6}/{2}\n= 4,35 m",
        SORT + "Middle values: 4,1 and 4,2\nMedian = {4,1 + 4,2}/{2}\n= 4,15 m",
        SORT + "Middle values: 4,2 and 4,3\nMedian = 4,2 + 4,3\n= 8,5 m"],
        ["Put the lengths in order first.", "With 12 values, which two are in the middle?"])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Till slips and VAT", "marks": 9, "table": SLIP,
     "lead": "Mr Mpoba is a Grade 10 teacher. He decided to have one big party to celebrate all the learners in his class register for birthdays. "
             "Given below is the till slip received after doing some of the shopping for the party.",
     "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Bar graphs and probability", "marks": 9,
     "lead": "Mrs Magadi decided to display the birthdays of every child that she teaches in a graph.",
     "figure": P.fig("1.2", "A bar graph, Birthday of Students by Month: Jan 3, Feb 4, Mar 2, Apr 3, May 8, Jun 10, Jul 6, Aug 1, Sep 7, Oct 8, "
                            "Nov 4, Dec 7."), "items": q12},
    {"id": "2.1", "title": "Question 2.1", "kind": "Budgets", "marks": 13, "table": BUDGET,
     "lead": "Mavis is a third-year college student. She receives R3 800 from her parents as a monthly allowance. She also works at the supermarket "
             "on weekends and receives a monthly salary of R1 800. TABLE 1 below shows Mavis's budget.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Tariffs", "marks": 11, "table": WATER,
     "lead": "Mr Sibiya compared the water tariffs of his own town to those of Port St Johns. He got the following water tariffs for the 2024/2025 "
             "book year (adapted from www.matlosana.gov.za).", "items": q22},
    {"id": "3", "title": "Question 3", "kind": "Banking and interest", "marks": 15, "table": FEES,
     "lead": "Study TABLE 1 regarding bank fees at FNB Bank.", "items": q3},
    {"id": "4.1", "title": "Question 4.1", "kind": "Pie charts", "marks": 11,
     "lead": "Mr Bernard planned to buy a new car. He is uncertain about the colour and the model of the car. He decided to do some research before "
             "he makes a decision. He came across the following chart that showed the different colour cars sold in the previous month.",
     "figure": P.fig("4.1", "A pie chart, CAR SALES DURING A SPECIFIC MONTH: White 35%, Beige 24%, Silver 15%, Blue 9%, Black 6%, Other 3%, and a "
                            "Red slice with no percentage."), "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Measures of central tendency", "marks": 7, "table": LENGTHS,
     "lead": "Mr Bernard came across the different lengths of cars in South Africa. The different lengths, in metres, are as follows.", "items": q42}]

P.finish(missions,
         {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P1", "sitting": "November 2025", "total_marks": 75,
          "time": "1 hour 30 minutes"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "2.1.2", "kind": "no_fit", "detail": "Fixed and variable expenses (2.1.2) and interest versus interest rate (3.2.1) play as sorts; "
                                                     "the memo's totals for 2.1.2 (R1 500 fixed, R2 950 variable) follow from the sort."},
          {"n": "1.1", "kind": "low_confidence", "detail": "The stem names Mr Mpoba and then says 'she received'; the till slip is dated 24.02.2020. "
                                                           "Both kept as printed."}],
         {"1": 18, "2": 24, "3": 15, "4": 18}, 75, {}, "Questions 1 to 4 (the whole paper)")
