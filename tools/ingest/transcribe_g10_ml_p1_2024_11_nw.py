"""Grade 10 Mathematical Literacy P1 November 2024 (North West Department of Education, provincial assessment), the whole paper
(Questions 1 to 4, 75 marks), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, marks,
answers and the memo's working are the paper's and the memo's own (its English); clues and figure captions are ours. Source
(PROVENANCE-g10-g11.md): education.nwpg.gov.za, Examination > Assessment, the question paper PDF (English, 8 pages with Annexure
A, text layer; the pie chart and bar graph are images) and the marking guidelines PDF (English, 7 pages), read from their text and
page images (100 dpi).

  python tools/ingest/transcribe_g10_ml_p1_2024_11_nw.py
  python tools/ingest/ingest.py "uploads/provincial/g10-ml-p1-2024-11-nw/15-NOVEMBER-2024-NW-S2-GR10-MATHEMATICAL-LITERACY-P1-ENG-QP.pdf" "uploads/provincial/g10-ml-p1-2024-11-nw/15-NOVEMBER-2024-NW-S2-GR10-MATHEMATICAL-LITERACY-P1-ENG-MG.pdf" --id g10-ml-p1-2024-11-nw --from-json

The Mathematical Literacy rulings, as in transcribe_g11_ml_p1_2024_11_ec.py: a calculation, a 'verify' and a number worked from a
table -> four whole workings (provincial.work), the memo's first method and three real errors; a word read off -> term or an MCQ of
answers; a definition or an explanation -> statements. The budget, the bank statement (Annexure A) and the water tariffs are typed
as tables, the statement as printed (its 20/10/2025 date included); the bank's fee structure is typed in the lead.
Figure boxes in PDF points (page 595 x 842), measured on the page images (100 dpi, scale 1.3889)."""
from provincial import Paper

P = Paper("g10-ml-p1-2024-11-nw", 595.32, 841.92, {"Q3.1": [5, 100, 208, 470, 506], "Q4.2": [7, 105, 182, 475, 548]}, start=1)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term

BUDGET = {"head": ["INCOME ITEMS", "AMOUNT IN RAND", "EXPENDITURE ITEMS", "AMOUNT IN RAND"],
          "rows": [["Dad income", "28 000", "Municipality account", "3 600"],
                   ["Mom income (½ day = 4 hours per day)", "5 500", "Cell phone usage", "850"],
                   ["", "", "Insurance", "2 700"],
                   ["Savings pay-out", "24 000", "Rent payment", "5 500"],
                   ["", "", "Car payment", "4 700"],
                   ["", "", "Christmas gifts", "4 000"],
                   ["TOTAL INCOME", "57 500", "TOTAL EXPENDITURE", "21 350"]]}
STATEMENT = {"head": ["DATE", "TRANSACTION DETAILS", "DEBIT", "CREDIT", "BALANCE"],
             "rows": [["01/10/2024", "Opening balance", "", "", "R14 680,00"],
                      ["01/10/2024", "Interest on credit balance", "", "R57,00", ""],
                      ["02/10/2024", "Stop order – NW Insurance", "R2 700,00", "", "2.1.2"],
                      ["05/10/2024", "PnP debit card purchase", "R940,00", "", ""],
                      ["10/10/2024", "Debit order – Municipality", "R3 860,00", "", ""],
                      ["14/10/2024", "Cash withdrawal (branch)", "R1 300,00", "", ""],
                      ["15/10/2024", "Stop order – Toyota SA", "R4 700,00", "", ""],
                      ["17/10/2024", "Checkers debit card purchase", "R1 660,00", "", ""],
                      ["20/10/2025", "Stop order – NW properties", "R5 500,00", "", ""],
                      ["25/10/2024", "Salary – EFT deposit", "", "R28 000,00", ""],
                      ["30/10/2024", "Bank charges", "R577,50", "", ""],
                      ["", "Closing balance", "", "", "?"]]}
WATER = {"head": ["CONSUMPTION", "TARIFF IN RANDS (VAT INCLUDED)"],
         "rows": [["0 kℓ – 6 kℓ", "R27,80"], ["6 kℓ – 20 kℓ", "R34,06"], ["20 kℓ – 50 kℓ", "R35,14"], ["50 kℓ – 100 kℓ", "R36,34"],
                  ["100 kℓ – 200 kℓ", "R38,34"], ["200 kℓ – 300 kℓ", "R40,62"], ["300 kℓ +", "R51,16"]]}

# ---- QUESTION 1, the question paper page 3 and the memo page 2 ----
q1 = [
    stmt("1.1", "Define the term budget.", 2,
         ["A budget is a summary of the expected income and expenditure for a period such as a month.",
          "A budget is a plan of the money you expect to earn and to spend over a period."],
         ["A budget is a record of the money already spent last month.", "A budget is a bank statement of the income received.",
          "A budget is a list of the items you want to buy on holiday.", "A budget is the total of all your savings."],
         ["Is a budget about the past or a plan for the future?", "Does it show income, expenditure or both?"], 2),
    answer("1.2", "Write down the amount of the total expenditure in words (without numerals).", 2,
           ["Twenty-one thousand three hundred and fifty rand", "Twenty-one thousand three hundred and five rand",
            "Two hundred and thirteen thousand five hundred rand", "Fifty-seven thousand five hundred rand"],
           ["Find TOTAL EXPENDITURE in the table.", "Read 21 350 as thousands, then hundreds, then the rest."]),
    term("1.3", "Name one item that is an occasional expenditure.", ["christmas gifts", "christmas gift", "christmas presents"],
         ["Occasional expenditure does not happen every month.", "Which item is only paid at a certain time of the year?"], marks=2),
    work("1.4", "Determine the mom's monthly salary if she works for 8 hours per day.", 2, [
        "R5 500 × 2\n= R11 000",      # the memo
        "R5 500 × 8\n= R44 000",      # × the hours
        "R5 500 ÷ 2\n= R2 750",       # divided, not multiplied
        "R5 500 × 4\n= R22 000"],     # × the half-day's hours
        ["She earns R5 500 for 4 hours a day.", "How many times longer is an 8-hour day?"]),
    term("1.5", "Write down the name of the most expensive expenditure.", ["rent payment", "rent", "the rent payment"],
         ["Which expenditure amount is the largest?", "Give the item's name, not its amount."], marks=2),
    answer("1.6", "Determine the minimum value (in rand) in the expenditure column.", 2, ["R850", "R5 500", "R2 700", "R21 350"],
           ["Look at the expenditure amounts only.", "Which is the smallest?"]),
    term("1.7", "During the planning phase of the holiday, the family came across a document with questions which they had to complete. "
                "In this document a travel agency wanted to determine certain likes and dislikes of clients when travelling. Name the type "
                "of data collecting instrument described above.", ["questionnaire", "a questionnaire"],
         ["It is a document of questions that people fill in.", "Its name starts with 'question'."], marks=2)]

# ---- QUESTION 2, the question paper page 4, Annexure A and the memo pages 3-4 ----
DEB = "Debits: R2 700 ; R940 ; R3 860 ; R1 300 ; R4 700 ; R1 660 ; R5 500 ; R577,50\n"
LT = "Less than R2 500: R940 ; R1 300 ; R1 660 ; R577,50\n"
N13 = "Number of R100s: {1 300}/{100} = 13\n"
YR = "1st year: R2 000 × 7,5% × 1 = R150\n"
q21 = [
    answer("2.1.1", "Write down the branch number as indicated on the statement.", 2, ["179462", "236892389275", "Orkney", "31 October 2024"],
           ["Look at the top of the statement.", "The branch number is in brackets after the branch's name."]),
    work("2.1.2", "Calculate the balance on the 2nd of October 2024.", 4, [
        "R14 680,00 + R57,00 − R2 700,00\n= R12 037,00",     # the memo
        "R14 680,00 − R57,00 − R2 700,00\n= R11 923,00",     # the interest subtracted
        "R14 680,00 + R57,00 + R2 700,00\n= R17 437,00",     # the stop order added
        "R14 680,00 − R2 700,00\n= R11 980,00"],             # the interest left out
        ["Start from the opening balance.", "Add the credits and subtract the debits up to 2 October."]),
    work("2.1.3", "Calculate the total amount spent by paying with the debit card for October 2024.", 3, [
        "R940,00 + R1 660,00\n= R2 600,00",                  # the memo
        "R940,00 + R1 300,00 + R1 660,00\n= R3 900,00",      # the cash withdrawal included
        "R940,00 + R3 860,00 + R1 660,00\n= R6 460,00",      # the debit order included
        "R1 660,00 − R940,00\n= R720,00"],                   # subtracted, not added
        ["Which entries say 'debit card purchase'?", "A debit order is not a debit card payment."]),
    work("2.1.4", "Calculate the bank charges as a percentage of the salary.", 3, [
        "{R577,50}/{R28 000} × 100\n= 2,06 %",               # the statement's bank charges (the memo writes 557,50)
        "{R28 000}/{R577,50} × 100\n= 4 848,48 %",           # upside down
        "{R577,50}/{R14 680} × 100\n= 3,93 %",               # the opening balance for the salary
        "{R577,50}/{R28 000}\n= 0,02 %"],                    # not × 100
        ["What are the bank charges and the salary on the statement?", "Percentage = part ÷ whole × 100."]),
    work("2.1.5", "By using the debit entries only, calculate the probability to randomly select a debit amount less than R2 500. Give your "
         "answer as a decimal number.", 3, [
        DEB + LT + "P = {4}/{8} = 0,5",                                                                      # the memo
        "Debits: R2 700 ; R940 ; R3 860 ; R1 300 ; R4 700 ; R1 660 ; R5 500\nLess than R2 500: R940 ; R1 300 ; R1 660\n"
        "P = {3}/{7} = 0,43",                                                                                # the bank charges left out
        "Entries: 8 debits and 2 credits\n" + LT + "P = {4}/{10} = 0,4",                                     # the credits counted too
        DEB + LT + "P = {8}/{4} = 2"],                                                                       # upside down
        ["How many debit entries are there, the bank charges included?", "How many of them are less than R2 500?"]),
    work("2.1.6", "Bernard claims that his bank charge on the cash withdrawal will be less than R20,00. Verify, showing ALL calculations, if "
         "his statement is VALID.", 4, [
        N13 + "Fee = R3,50 + (R1,50 × 13)\n= R3,50 + R19,50 = R23,00\nMore than R20,00: his statement is NOT VALID",   # the memo
        N13 + "Fee = R1,45 × 13\n= R18,85\nLess than R20,00: his statement is VALID",                                    # the own bank ATM fee
        N13 + "Fee = R3,50 + R1,50\n= R5,00\nLess than R20,00: his statement is VALID",                                  # 'per R100' left out
        N13 + "Fee = (R3,50 + R1,50) × 13\n= R65,00\nMore than R20,00: his statement is NOT VALID"],                     # the fixed fee × 13 too
        ["The withdrawal was made at the branch: which fee applies?", "How many R100s are in R1 300?"])]
q22 = [
    work("2.2", "Jessica is planning to save R2 000 for 18 months at a simple interest rate of 7,5% per year interest. Calculate the amount "
         "that she will receive at the end of the 18 months period.", 4, [
        YR + "Half year: R2 000 × 7,5% × 0,5 = R75\nInterest = R150 + R75 = R225\nTotal = R2 000 + R225 = R2 225",       # the memo
        YR + "Half year: R2 000 × 7,5% × 1 = R150\nInterest = R150 + R150 = R300\nTotal = R2 000 + R300 = R2 300",       # the half year as a year
        YR + "Half year: R2 000 × 7,5% × 0,5 = R75\nInterest = R150 + R75 = R225\nTotal = R225",                         # the interest only
        "1st year: R2 000 × 1,075 = R2 150\nHalf year: R2 150 × 7,5% × 0,5 = R80,63\nInterest = R150 + R80,63 = R230,63\n"
        "Total = R2 000 + R230,63 = R2 230,63"],                                                                       # compounded
        ["How many years is 18 months?", "Simple interest is worked out on the R2 000 only."])]
q23 = [
    work("2.3", "The price of fishing gear is R2 400 VAT exclusive. It is expected that the fishing gear will increase by 10% this coming "
         "December. John wishes to buy the fishing gear in December after receiving his savings pay-out of R3 000. He claims that he will "
         "have enough money to buy this fishing gear with his savings amount. Verify, showing ALL calculations, whether his claim is VALID "
         "or NOT.", 4, [
        "VAT included: R2 400 × 1,15 = R2 760\nPrice increase: R2 760 × 1,1\n= R3 036\nMore than R3 000: his claim is NOT VALID",   # the memo
        "VAT included: none added\nPrice increase: R2 400 × 1,1\n= R2 640\nLess than R3 000: his claim is VALID",                   # VAT left out
        "VAT and increase: 15% + 10% = 25%\nPrice: R2 400 × 1,25\n= R3 000\nExactly R3 000: his claim is VALID",                    # the percentages added
        "VAT included: R2 400 × 0,15 = R360\nPrice increase: R360 × 1,1\n= R396\nLess than R3 000: his claim is VALID"],            # the VAT taken as the price
        ["The price is VAT exclusive: what must be added first?", "Then increase that price by 10%."])]

# ---- QUESTION 3, the question paper pages 5-6 and the memo pages 5-6 ----
SUM = "Sum = 4,1 + 4,3 + 5,8 + 4,1 + 2,9 + 5,1 + 3,6 + 2,5 + 4,7 + 4,4 + 4,2 + 5,0 = 50,7\n"
SORT = "2,5 ; 2,9 ; 3,6 ; 4,1 ; 4,1 ; 4,2 ; 4,3 ; 4,4 ; 4,7 ; 5,0 ; 5,1 ; 5,8\n"
q31 = [
    term("3.1.1", "Name the type of chart shown above.", ["pie chart", "pie graph", "pie diagram"],
         ["The chart is a circle cut into slices.", "Each slice is a percentage of the whole."], marks=2),
    mcq("3.1.2", "State whether the above data is categorical or numerical.", ["Categorical", "Numerical"], 0,
        ["Are the colours numbers or groups?", "Data in named groups is categorical."], marks=2),
    work("3.1.3", "Calculate the percentage of red cars.", 3, [
        "35% + 9% + 6% + 15% + 24% + 3% = 92%\nRed = 100% − 92%\n= 8%",     # the memo
        "35% + 9% + 6% + 15% + 24% = 89%\nRed = 100% − 89%\n= 11%",         # Other left out
        "7 colours and Other share 100%\nRed = 100% ÷ 8\n= 12,5%",           # shared equally
        "35% + 9% + 6% + 15% + 24% + 3% = 82%\nRed = 100% − 82%\n= 18%"],   # an addition slip
        ["What do all the slices add up to?", "Add every labelled percentage, Other included."]),
    work("3.1.4", "During this specific month, 350 cars were sold. Calculate the number of beige cars sold.", 2, [
        "350 × 24%\n= 84 cars",          # the memo
        "350 × 35%\n= 122,5 cars",       # the white slice
        "350 ÷ 24\n= 14,58 cars",        # divided by 24
        "350 × 24\n= 8 400 cars"],       # 24, not 24%
        ["What percentage of the cars were beige?", "Find that percentage of 350."]),
    stmt("3.1.5", "Mr Bernard claims that a white car doesn't attract dirt easily. Give another valid reason why a white car might be a better "
                  "option to buy.", 2,
         ["A white car is more visible on the road, so it is easier to spot.", "White paint hides small imperfections such as scratches well.",
          "A white car can improve the car's resale value.", "White paint keeps the car cooler in the sun."],
         ["A white car uses less fuel than other cars.", "A white car does not need to be insured.", "A white car can go faster than other cars."],
         ["Think of safety, heat and selling the car later.", "White is the most popular colour in the chart."], 2)]
q32 = [
    work("3.2.1", "Calculate the mean length of the given data in the set.", 3, [
        SUM + "Mean = {50,7}/{12}\n= 4,23 m",           # the memo
        SUM + "Mean = {50,7}/{11}\n= 4,61 m",           # ÷ 11
        SUM + "Mean = {12}/{50,7}\n= 0,24 m",           # upside down
        SUM + "Mean = {2,5 + 5,8}/{2}\n= 4,15 m"],      # the middle of the smallest and largest
        ["Add all the lengths.", "Divide by how many lengths there are."]),
    work("3.2.2", "Calculate the median of the data.", 4, [
        SORT + "Middle values: 4,2 and 4,3\nMedian = {4,2 + 4,3}/{2}\n= 4,25 m",                                                       # the memo
        "4,1 ; 4,3 ; 5,8 ; 4,1 ; 2,9 ; 5,1 ; 3,6 ; 2,5 ; 4,7 ; 4,4 ; 4,2 ; 5,0\nMiddle values: 5,1 and 3,6\n"
        "Median = {5,1 + 3,6}/{2}\n= 4,35 m",                                                                                           # not put in order
        SORT + "Middle values: 4,1 and 4,2\nMedian = {4,1 + 4,2}/{2}\n= 4,15 m",                                                       # the 5th and 6th values
        SORT + "Middle values: 4,2 and 4,3\nMedian = 4,2 + 4,3\n= 8,5 m"],                                                             # not halved
        ["Put the lengths in order first.", "With 12 values, which two are in the middle?"])]

# ---- QUESTION 4, the question paper pages 6-7 and the memo page 7 ----
B6 = "0 to 6 kℓ: 6 × R27,80 = R166,80\n"
q41 = [
    answer("4.1.1", "The amounts in Table 1 above included VAT. What is the current VAT % in South Africa?", 2, ["15%", "14%", "10%", "6%"],
           ["VAT is added to most goods and services in South Africa.", "It has been the same rate since 2018."]),
    work("4.1.2", "The tariffs increased from 2022/2023 to 2023/2024 by 6%. Calculate the previous tariff for the 0 kℓ – 6 kℓ category in "
         "2022/2023.", 3, [
        "R27,80 ÷ 1,06\n= R26,23",       # the memo
        "R27,80 × 0,94\n= R26,13",       # 6% taken off the new tariff
        "R27,80 × 1,06\n= R29,47",       # increased again
        "R27,80 − 6\n= R21,80"],         # R6, not 6%
        ["The 2023/2024 tariff is 106% of the old tariff.", "To undo an increase of 6%, divide by 1,06."]),
    work("4.1.3", "Mr Bernard claims that 18 kℓ of water will cost more than R550 for 2023/2024. Verify, by calculating the cost of 18 kℓ, if his "
         "statement is CORRECT.", 5, [
        B6 + "6 to 18 kℓ: 12 × R34,06 = R408,72\nTotal = R166,80 + R408,72\n= R575,52\nMore than R550: his statement is CORRECT",       # the memo
        "0 to 18 kℓ: 18 × R27,80 = R500,40\n6 to 18 kℓ: none\nTotal = R500,40 + R0\n= R500,40\nLess than R550: his statement is NOT CORRECT",  # one tariff
        B6 + "6 to 18 kℓ: 18 × R34,06 = R613,08\nTotal = R166,80 + R613,08\n= R779,88\nMore than R550: his statement is CORRECT",       # all 18 kℓ again
        B6 + "6 to 18 kℓ: 12 × R35,14 = R421,68\nTotal = R166,80 + R421,68\n= R588,48\nMore than R550: his statement is CORRECT"],      # the next band's tariff
        ["The first 6 kℓ cost one tariff; the next 12 kℓ another.", "Which band does 6 kℓ to 18 kℓ fall in?"])]
q42 = [
    answer("4.2.1", "Determine the probability of randomly selecting a month with a water usage of less than 12 kilolitre.", 2,
           ["0", "{1}/{12}", "1", "0,5"], ["Which months used less than 12 kℓ?", "Is any bar below 12?"]),
    work("4.2.2", "List all the values for water usage over 12 months from the graph and then determine the mode of the data set.", 4, [
        "16 ; 14 ; 19 ; 17 ; 19 ; 17 ; 22 ; 15 ; 20 ; 17 ; 19 ; 18\nIn order: 14 ; 15 ; 16 ; 17 ; 17 ; 17 ; 18 ; 19 ; 19 ; 19 ; 20 ; 22\n"
        "Mode = 17 kℓ and 19 kℓ",                                                                                                    # the memo
        "16 ; 14 ; 19 ; 17 ; 19 ; 17 ; 22 ; 15 ; 20 ; 17 ; 19 ; 18\nIn order: 14 ; 15 ; 16 ; 17 ; 17 ; 17 ; 18 ; 19 ; 19 ; 19 ; 20 ; 22\n"
        "Mode = 17 kℓ",                                                                                                               # one mode only
        "16 ; 14 ; 19 ; 17 ; 19 ; 17 ; 22 ; 15 ; 20 ; 17 ; 19 ; 18\nIn order: 14 ; 15 ; 16 ; 17 ; 17 ; 17 ; 18 ; 19 ; 19 ; 19 ; 20 ; 22\n"
        "Mode = 17,75 kℓ",                                                                                                            # the mean
        "16 ; 14 ; 19 ; 17 ; 19 ; 17 ; 22 ; 15 ; 20 ; 17 ; 19 ; 18\nIn order: 14 ; 15 ; 16 ; 17 ; 17 ; 17 ; 18 ; 19 ; 19 ; 19 ; 20 ; 22\n"
        "Mode = 17,5 kℓ"],                                                                                                            # the median
        ["Read each bar's height.", "The mode is the value that appears most often: can there be two?"])]

missions = [
    {"id": "1", "title": "Question 1", "kind": "Budgets", "marks": 14, "table": BUDGET,
     "lead": "Jessica and her family are planning to go on holiday to a nearby holiday resort during the December holiday. The table below "
             "shows their budget presented to her dad: JESSICA'S FAMILY BUDGET FOR DECEMBER 2024.", "items": q1},
    {"id": "2.1", "title": "Question 2.1", "kind": "Bank statements", "marks": 19, "table": STATEMENT,
     "lead": "Jessica's dad, Bernard, showed his bank statement for October 2024 to her (Annexure A), with an extract of his bank's bank "
             "charges structure. All bank charges will be debited at the end of the month.\nRSA BANK, current account statement. Account "
             "name: Mr B Jantjies. Account number: 236892389275. Branch: Orkney (179462). Statement date: 31 October 2024. Statement "
             "period: 1 Oct 2024 to 31 Oct 2024.\nTransaction fees: stop order (internal) R6,50 + 1,2% of the amount; stop order "
             "(external) R7,50 + 1,35% of the amount; debit order (internal) R4,85; debit order (external) R16,75; cash withdrawal at own "
             "bank ATM R1,45 per R100 or part of; at another bank's ATM R6,80 + R2,60 per R100 or part of; at own bank branch R3,50 + "
             "R1,50 per R100 or part of; debit card payment (swipe at counter) R0,50 per R100 or part of.", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Simple interest", "marks": 4, "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "VAT and price increases", "marks": 4, "items": q23},
    {"id": "3.1", "title": "Question 3.1", "kind": "Pie charts", "marks": 11,
     "lead": "Mr Bernard planned to buy a new car. He is uncertain about the colour and the model of the car. He decided to do some research "
             "before he makes a decision. He came across the following chart that showed the different colour cars sold in the previous "
             "month.",
     "figure": P.fig("Q3.1", "A pie chart, CAR SALES DURING A SPECIFIC MONTH: White 35%, Beige 24%, Silver 15%, Blue 9%, Black 6%, "
                             "Other 3%, and a Red slice with no percentage."), "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Measures of central tendency", "marks": 7,
     "lead": "Mr Bernard came across the different lengths of cars in South Africa. The different lengths, in metres, are as follows:\n"
             "4,1 ; 4,3 ; 5,8 ; 4,1 ; 2,9 ; 5,1 ; 3,6 ; 2,5 ; 4,7 ; 4,4 ; 4,2 ; 5,0", "items": q32},
    {"id": "4.1", "title": "Question 4.1", "kind": "Tariffs", "marks": 10, "table": WATER,
     "lead": "Mr Bernard compared the water tariffs of his own town to that of Matlosana. He got the following water tariffs for Matlosana "
             "for the 2023/2024 book year (TABLE 1: WATER TARIFF FOR MATLOSANA FOR 2023/2024, adapted from www.matlosana.gov.za).",
     "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Bar graphs and probability", "marks": 6,
     "lead": "Over a year's time Mr Bernard kept a record of his family's water usage. He drew a graph of these records. Note: the water "
             "usage is rounded each month to the nearest whole number.",
     "figure": P.fig("Q4.2", "A bar graph, WATER USAGE OVER 12 MONTHS, usage in kilolitres from 0 to 24: month 1 16, month 2 14, month 3 "
                             "19, month 4 17, month 5 19, month 6 17, month 7 22, month 8 15, month 9 20, month 10 17, month 11 19, "
                             "month 12 18."), "items": q42}]

P.finish(missions,
         {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P1", "sitting": "November 2024", "total_marks": 75,
          "time": "1 hour 30 minutes"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "2.1.4", "kind": "memo_issue", "detail": "The memo divides R557,50 by R28 000 (1,99 %); the statement's bank charges are "
                                                         "R577,50, which gives 2,06 %. The right option uses the statement's R577,50."}],
         {"1": 14, "2": 27, "3": 18, "4": 16}, 75, {}, "Questions 1 to 4 (the whole paper)")
