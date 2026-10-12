"""Grade 11 Mathematical Literacy P1 November 2024 (Eastern Cape Department of Education), the whole paper (Questions 1 to 4, 100 marks,
2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, marks, answers and the memo's
working are the paper's and the memo's own; clues and figure captions are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za,
2024_November_Gr_11_Exams, the question paper zip (English PDF, 16 pages with its ANSWER SHEET, text layer) and the memo (English,
6 pages; its last page is an image, read from the page image).

  python tools/ingest/transcribe_g11_ml_p1_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-ml-p1-2024-11-ec/MATHS LIT P1 GR11 QP NOV 2024 ENG DD_watermark.pdf" "uploads/provincial/g11-ml-p1-2024-11-ec/MATHS LIT P1 MEMO GR 11 NOV2024_English_watermark.pdf" --id g11-ml-p1-2024-11-ec --from-json

The Mathematical Literacy rulings, as in transcribe_ml_p1_2025_11.py: a calculation, a 'verify' and a number worked from a table ->
four whole workings (provincial.work), the memo's first method and three real errors; a word read off -> term or an MCQ of answers;
a definition or an explanation -> statements; 'arrange in order' -> order; the graph on the answer sheet (4.1.3, 4.1.4) -> pick the
drawing (pictures_lower.py: breakeven). The tables are typed. The figure box is in PDF points (scratch figbox.py)."""
from provincial import Paper

P = Paper("g11-ml-p1-2024-11-ec", 595.2, 842.0, {"1.3": [4, 111.6, 454.0, 486.0, 658.9]}, start=7)
work, answer, num, draw, stmt, mcq, term = P.work, P.answer, P.num, P.draw, P.stmt, P.mcq, P.term

INVOICE = {"head": ["ITEM", "UNIT PRICE", "QUANTITY", "PRICE"],
           "rows": [["White camisole top", "$123", "1", "$123"], ["Cuban collar shirt", "$127", "4", "A"], ["Floral cotton dress", "$123", "B", "$369"],
                    ["Subtotal", "", "", "$1 000"], ["Tax (0%)", "", "", "$0"], ["TOTAL", "", "", "$1 000"]]}
RESORT = {"head": ["Number of people", "0", "1", "C", "4", "8", "10"],
          "rows": [["Cost for Mt View Resort", "1 200", "1 200", "1 200", "1 200", "1 200", "1 200"],
                   ["Cost for Forest Resort", "950", "950", "950", "950", "950", "D"]]}
BUDGET = {"head": ["SECTORS", "2024/2025 (in Rand)", "2025/2026 (in Rand)"],
          "rows": [["Education", "42 441 422", "44 104 248"], ["Health", "30 106 843", "31 029 965"], ["Social Development", "2 972 172", "3 100 547"],
                   ["Sports, Recreation, Arts and Culture", "1 043 363", "1 074 493"], ["Community Safety", "144 840", "150 179"],
                   ["Total", "76 708 640", "79 459 432"]]}
FEES = {"head": ["TABLE 3: SCHOOL FEE STRUCTURE FOR 2024", ""],
        "rows": [["SCHOOL FEES", "R48 800,00"], ["HOSTEL FEES", "R66 800,00"], ["TOTAL", "R115 600,00"]]}
CRYPTO = {"head": ["No.", "COUNTRY", "VALUES", "PERCENTAGES (%)"],
          "rows": [["1.", "Indonesia", "12 615 365", "4,55"], ["2.", "Colombia", "2 505 605", "4,81"], ["3.", "Morocco", "1 854 162", "4,90"],
                   ["4.", "Kenya", "2 713 117", "4,92"], ["5.", "Turkey", "4 684 727", "5,54"], ["6.", "United Kingdom", "3 740 280", "5,52"],
                   ["7.", "Argentina", "2 544 102", "5,56"], ["8.", "Nigeria", "12 862 740", "5,75"], ["9.", "Russia", "8 485 749", "5,87"],
                   ["10.", "Pakistan", "15 400 547", "6,40"], ["11.", "Brazil", "15 400 547", "6,40"], ["12.", "India", "103 317 638", "7,23"],
                   ["13.", "Thailand", "6 692 796", "9,32"], ["TOTAL", "", "", ""]]}
STADIUM = {"head": ["Number of learners", "0", "10", "20", "40", "50", "100"],
           "rows": [["TABLE 5: Cost in Rand", "2 400", "2 900", "3 400", "4 400", "4 900", "7 400"],
                    ["TABLE 6: Income in Rand (t-shirts)", "0", "1 500", "3 000", "6 000", "7 500", "15 000"]]}
MARKS = ("43 ; 32 ; 86 ; 39 ; 30 ; 26 ; 62 ; 39 ; 40 ; 41 ; 50 ; 21 ; 18 ; 38 ; 26 ; 33 ; 69 ; 17 ; 22 ; 51 ; 21 ; 37 ; 24 ; 12 ; 24 ; 41 ; "
         "54 ; 41 ; E ; 14 ; 15 ; 55 ; 49 ; 64 ; 60 ; 49 ; 15 ; 40 ; 44 ; 53 ; 31 ; 13 ; 23 ; 26")

# ---- QUESTION 1, the question paper pages 3-4 and the memo page 2 ----
q11 = [
    term("1.1.1", "Write down the name of the service provider.", ["Canva", "Samira Hadid"], ["Whose name is at the top of the invoice?",
                                                                                              "Who sent the bill?"], marks=2),
    work("1.1.2", "Calculate the value of A.", 2, [
        "A = $127 × 4\n= $508",      # the memo
        "A = $127 + 4\n= $131",      # added
        "A = $123 × 4\n= $492",      # the wrong row's unit price
        "A = $127 ÷ 4\n= $31,75"],   # divided
        ["Price = unit price × quantity.", "Which unit price is the shirt's?"]),
    stmt("1.1.3", "Define the term invoice.", 2, ["An invoice is a list of goods or services provided, with a statement of the amount due."],
         ["An invoice is a receipt showing that the account has been paid.", "An invoice is a bank statement of a month's transactions.",
          "An invoice is a quotation for work that has not been done yet.", "An invoice is a list of a shop's opening hours."],
         ["When do you get an invoice: before or after paying?", "What does it list?"], 2),
    work("1.1.4", "Determine the value of B.", 2, [
        "B = $369 ÷ $123\n= 3",          # the memo
        "B = $369 − $123\n= 246",        # subtracted
        "B = $1 000 ÷ $123\n= 8,13",     # the subtotal used
        "B = $369 ÷ $127\n= 2,91"],      # the shirt's unit price
        ["Quantity = price ÷ unit price.", "Which unit price is the dress's?"]),
    answer("1.1.5", "Write down the due date?", 2, ["5 March 2024", "16 February 2024", "5 February 2024", "16 March 2024"],
           ["Look under PAYMENT INFORMATION.", "'Pay by' gives the due date."]),
    work("1.1.6", "Convert the total amount in dollars to rand, if R1,00 = $0,053.", 2, [
        "R1,00 = $0,053\nTotal = {$1 000 × R1,00}/{$0,053}\n= R18 867,92",       # the memo
        "R1,00 = $0,053\nTotal = $1 000 × 0,053\n= R53,00",                      # multiplied
        "R1,00 = $0,053\nTotal = {$1 000}/{0,53}\n= R1 886,79",                  # the rate misread
        "R1,00 = $0,053\nTotal = {$0,053}/{$1 000}\n= R0,000053"],               # upside down
        ["How many dollars is one rand?", "To change dollars into rand, multiply or divide by 0,053?"])]
q12 = [
    answer("1.2.1", "Identify the type of relationship illustrated in the table above.", 2,
           ["Constant (fixed) relationship", "Direct proportion", "Inverse proportion", "An increasing linear relationship"],
           ["Does the cost change as the number of people changes?", "What do you call a cost that stays the same?"]),
    answer("1.2.2", "Calculate how much the church members will pay if only five members attend the service at Mt View Resort.", 2,
           ["R1 200,00", "R6 000,00", "R240,00", "R950,00"], ["Is the price per person or per night?", "Does the number of people change it?"]),
    term("1.2.3(a)", "Determine the following missing value in the table: C", ["2", "3"], ["C lies between 1 and 4 people.", "Any number of "
                                                                                                                        "people from 1 to 4."],
         marks=2),
    answer("1.2.3(b)", "Determine the following missing value in the table: D", 2, ["R950", "R1 200", "R9 500", "R1 900"],
           ["Forest Resort's cost is the same for every number of people.", "Read along its row."])]
q13 = [
    num("1.3.1", "Determine the number of learners that wrote the cycle test.", 59, 0, "", ["Add the heights of all four bars.",
                                                                                        "29 + 23 + 3 + 4."], marks=2),
    work("1.3.2", "Calculate the percentage of learners who failed the cycle test.", 2, [
        "% fail = {29}/{59} × 100\n= 49,15%",            # the memo
        "% fail = {29}/{100} × 100\n= 29%",              # out of 100, not 59
        "% fail = {59}/{29} × 100\n= 203,45%",           # upside down
        "% fail = {29 + 23}/{59} × 100\n= 88,14%"],      # 30 – 49 counted as failing
        ["Which bar shows the learners who failed?", "Percentage = part ÷ total × 100."], after=["1.3.1"]),
    answer("1.3.3", "Write down the modal class percentage levels.", 2, ["0 – 29", "30 – 49", "50 – 69", "70 – 100"],
           ["The mode is the most frequent.", "Which bar is the tallest?"])]

# ---- QUESTION 2, the question paper pages 5-6 and the memo pages 3-4 ----
D2 = "Daniel: R50 + R12 × (80 − 3)\n= R50 + R924\n= R974,00\n"
q21 = [
    stmt("2.1.1", "Explain the meaning of the term budget.", 2,
         ["A budget is a financial plan outlining income and expenses over a period of time.",
          "A budget is a tool to help manage finances, reach financial goals and make informed decisions about spending and saving."],
         ["A budget is the money left over at the end of a month.", "A budget is a loan from a bank.", "A budget is a list of goods bought.",
          "A budget is the tax paid to the government."], ["Is a budget a plan or a record?", "Of what?"], 2),
    answer("2.1.2", "Write down the amount allocated for health in 2025/2026 in words.", 2, [
        "Thirty-one million and twenty-nine thousand, nine hundred and sixty-five", "Thirty-one million, two hundred and nine thousand, nine "
                                                                                    "hundred and sixty-five",
        "Thirty million, one hundred and six thousand, eight hundred and forty-three", "Three million, one hundred and two thousand, nine "
                                                                                       "hundred and sixty-five"],
        ["Find Health in the 2025/2026 column: 31 029 965.", "Read it in groups of three digits."]),
    work("2.1.3", "Calculate the percentage increase of the Education sector for the 2024/2025 and 2025/2026 financial year. Give your answer to "
         "the nearest percentage. You may use the following formula: Percentage increase = (new value − old value)/old value × 100%", 4, [
        "% increase = {44 104 248 − 42 441 422}/{42 441 422} × 100\n= 3,92\n= 4%",       # the memo
        "% increase = {31 029 965 − 30 106 843}/{30 106 843} × 100\n= 3,07\n= 3%",       # the Health row
        "% increase = {44 104 248}/{42 441 422} × 100\n= 103,92\n= 104%",                # the old value not subtracted
        "% increase = {42 441 422 − 44 104 248}/{42 441 422} × 100\n= −3,92\n= −4%"],    # old minus new
        ["Which row is Education, and which value is new?", "Use the formula, then round to a whole percentage."])]
q22 = [
    answer("2.2.1", "Write down the formula for calculating the cost for Daniel's company in the form of: Cost =", 2, [
        "Cost = R50 + R12 × (number of km − 3)", "Cost = R50 + R12 × number of km", "Cost = (R50 + R12) × (number of km − 3)",
        "Cost = R12 + R50 × (number of km − 3)"],
        ["The first 3 km are free.", "The R50 is paid once per trip."]),
    work("2.2.2", "The distance for a single trip to the meeting is 80 km. Mr Paul makes the statement that Jerry's taxi company will be the "
         "cheapest. Verify, showing ALL calculations, that his statement is correct.", 6, [
        D2 + "Jerry: R14,50 × 80 = R1 160,00\nDaniel's is cheaper: the statement is NOT correct",                                    # the memo
        "Daniel: R50 + R12 × 80\n= R50 + R960\n= R1 010,00\nJerry: R14,50 × 80 = R1 160,00\nDaniel's is cheaper: the statement is NOT "
        "correct",                                                                                                                     # the 3 free km ignored
        D2 + "Jerry: R14,50 + 80 = R94,50\nJerry's is cheaper: the statement is correct",                                            # added, not multiplied
        "Daniel: (R50 + R12) × (80 − 3)\n= R62 × 77\n= R4 774,00\nJerry: R14,50 × 80 = R1 160,00\nJerry's is cheaper: the statement is "
        "correct"],                                                                                                                    # the call-out fee per km
        ["Work out both prices for 80 km.", "Which is cheaper, and was Mr Paul right?"], after=["2.2.1"]),
    work("2.2.3", "Mr Paul had another trip. He paid Daniel R1 214 for a single trip. Determine the distance travelled during this trip.", 4, [
        "R1 214 = R50 + R12 × (D − 3)\nR1 164 = R12 × (D − 3)\n97 = D − 3\nD = 100 km",        # the memo
        "R1 214 = R50 + R12 × (D − 3)\nR1 164 = R12 × (D − 3)\n97 = D − 3\nD = 94 km",         # 3 subtracted, not added
        "R1 214 = R12 × (D − 3)\n101,17 = D − 3\nD = 104,17\nD = 104,17 km",                     # the call-out fee forgotten
        "R1 214 + R50 = R12 × (D − 3)\nR1 264 = R12 × (D − 3)\n105,33 = D − 3\nD = 108,33 km"],  # R50 added
        ["Put R1 214 into Daniel's formula.", "Undo each step in reverse order."], after=["2.2.1"])]
q23 = [
    work("2.3", "Calculate the total discount amount that Mr Mnotho and his wife will get from the school.", 6, [
        "School fee discount = R48 800 × 10% = R4 880\nHostel fee discount = R66 800 × 5% = R3 340\nTotal discount = R4 880 + R3 340\n= R8 220,00",
        # (above) the memo
        "School fee discount = R48 800 × 15% = R7 320\nHostel fee discount = R66 800 × 10% = R6 680\nTotal discount = R7 320 + R6 680\n"
        "= R14 000,00",                                                                                                         # the third child's rates
        "School fee discount = R115 600 × 10% = R11 560\nHostel fee discount = R115 600 × 5% = R5 780\nTotal discount = R11 560 + R5 780\n"
        "= R17 340,00",                                                                                                         # % of the total fees
        "School fee discount = R48 800 × 10% × 2 = R9 760\nHostel fee discount = R66 800 × 5% × 2 = R6 680\nTotal discount = R9 760 + R6 680\n"
        "= R16 440,00"],                                                                                                        # both sons discounted
        ["Only the second child gets a discount.", "Work out each discount, then add."])]

# ---- QUESTION 3, the question paper page 7 and the memo page 4 ----
DESC = ["103 317 638", "15 400 547 (Pakistan and Brazil)", "12 862 740", "12 615 365", "8 485 749", "6 692 796", "4 684 727", "3 740 280",
        "2 713 117", "2 544 102", "2 505 605", "1 854 162"]
SHOW = [DESC[i] for i in (3, 10, 11, 8, 6, 7, 9, 2, 4, 1, 0, 5)]   # the table's order, the two equal values one card
q3 = [
    answer("3.1", "Write down the country with the highest value of crypto currency.", 2, ["India", "Pakistan", "Thailand", "Brazil"],
           ["Read the VALUES column.", "Which value is the biggest?"]),
    {"t": "order", "n": "3.2", "marks": 2, "q": "Arrange the values owned by the countries in descending order. (Pakistan and Brazil both own "
     "15 400 547: one card.)", "clues": ["Descending: biggest first.", "Twelve different values."], "opts": SHOW,
     "a": [SHOW.index(v) for v in DESC]},
    work("3.3", "Calculate the difference between the maximum value and the minimum value.", 2, [
        "Difference = 103 317 638 − 1 854 162\n= 101 463 478",      # the memo
        "Difference = 103 317 638 − 2 505 605\n= 100 812 033",      # Colombia taken as the minimum
        "Difference = 15 400 547 − 1 854 162\n= 13 546 385",        # the second value as the maximum
        "Difference = 103 317 638 + 1 854 162\n= 105 171 800"],     # added
        ["Which is the biggest value, and which the smallest?", "Difference = maximum − minimum."]),
    num("3.4", "Determine the number of countries with a percentage between 5% and 6%.", 5, 0, "",
        ["Look down the PERCENTAGES column.", "Count the ones from 5,00 to 5,99."], marks=2),
    answer("3.5", "Determine the median country of the top 13 countries.", 2, ["Thailand", "Russia", "Turkey", "United Kingdom"],
           ["With 13 values in order, which position is the middle?", "Which country owns that 7th value?"], after=["3.2"]),
    answer("3.6", "Name the type of graph that would best display the above information.", 2, ["Bar graph", "Pie chart", "Histogram",
                                                                                               "Scatter plot"],
           ["The data are values for separate countries.", "Which graph compares separate categories?"]),
    work("3.7", "Calculate the probability, as a decimal, of randomly selecting a percentage between 3% and 6%.", 3, [
        "P = {9}/{13}\n= 0,69",      # the memo
        "P = {5}/{13}\n= 0,38",      # only 5% to 6%
        "P = {9}/{100}\n= 0,09",     # out of 100
        "P = {13}/{9}\n= 1,44"],     # upside down
        ["How many percentages are below 6%?", "Out of how many countries?"]),
    num("3.8", "Write down the number of countries from the list of top 13 countries with crypto currency that are found in Africa.", 3, 0, "",
        ["Which countries in the list are in Africa?", "Morocco, Kenya and …?"], marks=2)]

# ---- QUESTION 4, the question paper pages 8-9 and the memo pages 5-6 ----
q41 = [
    term("4.1.1", "The cost of using the stadium is expected to increase in 2025. Write down the term used to explain the yearly general increase "
         "of goods or services.", ["Inflation"], ["Prices rise in general every year.", "The rate is published as a percentage, the CPI."], marks=2),
    work("4.1.2", "Show how the total cost of using the stadium when 100 learners booked to attend the session, is calculated.", 3, [
        "Cost = R2 400 + R50 × number of learners\n= R2 400 + R50 × 100\n= R2 400 + R5 000\n= R7 400",          # the memo
        "Cost = (R2 400 + R50) × number of learners\n= (R2 400 + R50) × 100\n= R2 450 × 100\n= R245 000",      # the decorations per learner
        "Cost = R2 400 + R150 × number of learners\n= R2 400 + R150 × 100\n= R2 400 + R15 000\n= R17 400",     # the t-shirt price
        "Cost = R2 400 × number of learners + R50\n= R2 400 × 100 + R50\n= R240 000 + R50\n= R240 050"],      # the amounts swapped
        ["The decorations cost R2 400 once; the stadium R50 per learner.", "Multiply first, then add."]),
    draw("4.1.3", "Use TABLE 6 to draw a line graph of the income from selling t-shirts, on the axis provided on the ANSWER SHEET.", 3,
         [["Starting point (0 ; 0)", 1], ["End point (100 ; 15 000)", 1], ["A straight line", 1]],
         ["Where does the income start when no t-shirts are sold?", "What is the income for 100 learners?"],
         memo="The memo's graph: a straight line from (0 ; 0) to (100 ; 15 000), on the answer sheet with the cost line already drawn."),
    draw("4.1.4", "Indicate on the graph with a letter B, a point that will determine the number of t-shirts the SCA learners must sell to break "
         "even.", 2, [["B where the income and cost lines meet: 24 learners", 2]],
         ["Breaking even means income = cost.", "Where do the two lines cross?"], memo="The memo's B: 24 learners (24 t-shirts), on both lines.",
         after=["4.1.3"]),
    work("4.1.5", "After the fundraiser the learners made a profit of R7 500 and they deposited it in an investment account, earning interest of "
         "10,5% p.a. compounded annually. The student body claims that after 3 years they will have more than R10 000 in the account. Verify, "
         "showing ALL calculations, whether the statement is valid.", 5, [
        "Year 1: R7 500 + R7 500 × 10,5% = R8 287,50\nYear 2: R8 287,50 + R8 287,50 × 10,5% = R9 157,69\nYear 3: R9 157,69 + R9 157,69 × 10,5% = "
        "R10 119,24\nMore than R10 000: the statement is valid",                                                                  # the memo
        "Year 1: R7 500 + R7 500 × 10,5% = R8 287,50\nYear 2: R8 287,50 + R7 500 × 10,5% = R9 075,00\nYear 3: R9 075,00 + R7 500 × 10,5% = "
        "R9 862,50\nLess than R10 000: the statement is not valid",                                                                # simple interest
        "Year 1: R7 500 + R7 500 × 1,05% = R7 578,75\nYear 2: R7 578,75 + R7 578,75 × 1,05% = R7 658,33\nYear 3: R7 658,33 + R7 658,33 × 1,05% = "
        "R7 738,74\nLess than R10 000: the statement is not valid",                                                                # the rate misread
        "Year 1: R7 500 − R7 500 × 10,5% = R6 712,50\nYear 2: R6 712,50 − R6 712,50 × 10,5% = R6 007,69\nYear 3: R6 007,69 − R6 007,69 × 10,5% = "
        "R5 376,88\nLess than R10 000: the statement is not valid"],                                                               # interest subtracted
        ["Compound interest: each year earns interest on the year before's balance.", "Work it out year by year."])]
q42 = [
    mcq("4.2.1", "Is the above data continuous or discrete?", ["Continuous", "Discrete"], 1,
        ["Marks out of 100 are counted whole numbers.", "Can a mark be 37,4 here?"]),
    work("4.2.2", "The mean of the above data is equal to 37. Calculate the value of E.", 5, [
        "37 = {1 588 + E}/{44}\n1 588 + E = 1 628\nE = 1 628 − 1 588\nE = 40",       # the memo
        "37 = {1 588 + E}/{43}\n1 588 + E = 1 591\nE = 1 591 − 1 588\nE = 3",        # 43 values counted
        "37 = {1 588}/{44} + E\n37 = 36,09 + E\nE = 37 − 36,09\nE = 0,91",          # E left out of the sum
        "37 = {1 588 + E}/{44}\n1 588 + E = 1 628\nE = 1 628 + 1 588\nE = 3 216"],  # 1 588 added, not subtracted
        ["Mean = sum ÷ number of values: how many values, E included?", "The 43 known marks add up to 1 588."]),
    work("4.2.3", "The Mathematical Literacy teacher, Mrs Lee, states that the results shown in the table above are more clustered together. "
         "Verify, with the necessary calculations, whether her statement is correct.", 4, [
        "In order: 12 ; 13 ; 14 ; … ; 64 ; 69 ; 86\nRange = 86 − 12\n= 74\nThe range is big: the marks are spread out, the statement is NOT "
        "correct",                                                                                                         # the memo
        "In order: 12 ; 13 ; 14 ; … ; 64 ; 69 ; 86\nRange = 86 − 12\n= 74\nThe range is small: the marks are clustered, the statement is "
        "correct",                                                                                                         # the wrong reading of 74
        "In the table's order: 43 ; 32 ; … ; 23 ; 26\nRange = 43 − 26\n= 17\nThe range is small: the marks are clustered, the statement is "
        "correct",                                                                                                         # first and last unsorted
        "In order: 12 ; 13 ; 14 ; … ; 64 ; 69 ; 86\nRange = 86 + 12\n= 98\nThe range is big: the marks are spread out, the statement is NOT "
        "correct"],                                                                                                        # added
        ["Arrange the marks first: what are the lowest and the highest?", "Is a range of 74 out of 100 clustered?"], after=["4.2.2"]),
    num("4.2.4", "Determine the number of learners who achieved 30% or more.", 28, 0, "", ["Count the marks of 30 or more, E = 40 included.",
                                                                                           "Sorting the marks helps."], marks=2, after=["4.2.2"]),
    work("4.2.5", "Write down the probability of selecting learners who achieved more than 80% as a decimal. (Correct your answer to 3 decimal "
         "places.)", 3, [
        "P = {1}/{44}\n= 0,023",      # the memo
        "P = {86}/{100}\n= 0,860",    # the mark as the probability
        "P = {44}/{1}\n= 44,000",     # upside down
        "P = {2}/{44}\n= 0,045"],     # 69 counted as above 80
        ["How many learners scored above 80%?", "Out of how many learners?"])]

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Invoices", "marks": 12, "table": INVOICE,
     "lead": "Mrs Link ordered clothing items and received the invoice below.\nCANVA © INVOICE, billed to Ave Link, 093 753 8800, 6 Prince Road. "
             "Invoice No: 2468, 16 February 2024.\nPAYMENT INFORMATION: Briand Bank, Account number 123-456-8900, Pay by: 5 March 2024. "
             "Samira Hadid, 331 Anywhere St. Any City ST 32110.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Costs", "marks": 8, "table": RESORT,
     "lead": "Metro church members are planning to have a church service at a resort for a weekend. They received quotes from two different "
             "resorts, both which accommodate a maximum of 10 people per resort.\nMt View Resort costs R1 200 per night including breakfast.\n"
             "Forest Resort costs R950 per night.\nTABLE 1: COSTS FOR BOTH RESORTS", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Data", "marks": 6,
     "lead": "A Grade 11 Mathematical Literacy class wrote a March cycle test. The results of the cycle test are shown in the graph below.",
     "figure": P.fig("1.3", "A bar graph, 2024 Grade 11 March cycle test results: the number of learners per percentage level, 29 for 0 – 29, "
                            "23 for 30 – 49, 3 for 50 – 69 and 4 for 70 – 100."), "items": q13},
    {"id": "2.1", "title": "Question 2.1", "kind": "Budgets", "marks": 8, "table": BUDGET,
     "lead": "Study the Eastern Cape Provincial Budget 2024/2025 framework and its focus areas on sectors. The summary of payment and estimates "
             "per sector is shown in the table below.\nTABLE 2: EASTERN CAPE PROVINCIAL BUDGET 2024/2025", "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Tariffs", "marks": 12,
     "lead": "Mr Paul is a businessman. He wants to attend a meeting and searched a meter taxi online. He found the prices of two companies: "
             "Daniel's company and Jerry's company.\nDaniel's company charges the following for a single trip:\n• A minimum call-out fee of R50 "
             "per trip and the first three kilometres are free\n• Thereafter, R12,00 for each additional kilometre or part thereof\nJerry's "
             "company charges a flat rate of R14,50 per kilometre.", "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "Discounts", "marks": 6, "table": FEES,
     "lead": "Mr Mnotho and his wife both secured new jobs overseas. They applied at a Boys High School for their two sons. The first son will be "
             "doing Grade 10 and the second son will be doing Grade 8. They will be staying at the hostel.\nSchool fees must be paid before end "
             "of January. Hostel fees must be paid at the beginning of each year.\nDiscount for siblings is offered as follows:\n• Second child "
             "gets 10% discount on school fees and 5% discount on hostel fees\n• Third child gets 15% discount on school fees and 10% discount "
             "on hostel fees", "items": q23},
    {"id": "3", "title": "Question 3", "kind": "Data handling", "marks": 17, "table": CRYPTO,
     "lead": "Study TABLE 4 below showing crypto ownership of the top 13 countries in 2023.\nTABLE 4: TOP 13 COUNTRIES WITH CRYPTO CURRENCY",
     "items": q3},
    {"id": "4.1", "title": "Question 4.1", "kind": "Break-even and interest", "marks": 15, "table": STADIUM,
     "lead": "The learners of the Student Christian Association (SCA) of South Africa are planning to celebrate the 128th year of existence of "
             "the organisation in October 2024. Celebrations will take place in the Eastern Cape, where the SCA learners are planning a "
             "fundraising event at one of the biggest stadiums in the province.\nTheir planning is as follows:\n• Stadium R50,00 per learner\n"
             "• Decorations R2 400,00\nThey decided to fundraise by selling t-shirts that will be worn during the celebrations, at R150,00 each.",
     "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Data handling", "marks": 16,
     "lead": "The 2023 Grade 11 Mathematical Literacy class of Zulu High School wrote an examination marked out of 100 marks. The results are "
             "shown below.\n" + MARKS, "items": q42},
]
P.finish(missions,
         {"subject": "Mathematical Literacy", "title": "Mathematical Literacy P1", "sitting": "November 2024", "total_marks": 100,
          "time": "2 hours"},
         [P.flag_workings(),
          P.flag_answers(),
          {"n": "3.2", "kind": "no_fit", "detail": "Pakistan and Brazil both own 15 400 547: an order of cards marks positions, so the two equal "
                                                   "values are one card (twelve cards), said in the stem."},
          {"n": "4.1.3", "kind": "no_fit", "detail": "The answer sheet's graph (4.1.3 the income line, 4.1.4 the point B) plays as pick the "
                                                     "drawing, each drawing with the sheet's printed cost line."},
          {"n": "1.2.3(a)", "kind": "no_fit", "detail": "C lies between 1 and 4 people: the memo takes 2 and accepts 3, both typed answers."},
          {"n": "2.2.2", "kind": "memo_issue", "detail": "The memo writes Jerry: R14,00 × R80,00 = R1 160,00; the rate is R14,50 a kilometre "
                                                         "and the trip 80 km, which give its R1 160,00. The right option writes R14,50 × 80."}],
         {"1": 26, "2": 26, "3": 17, "4": 31}, 100,
         {"1.3.2": ["1.3.1"], "2.2.2": ["2.2.1"], "2.2.3": ["2.2.1"], "3.5": ["3.2"], "4.1.4": ["4.1.3"], "4.2.3": ["4.2.2"], "4.2.4": ["4.2.2"]},
         "Questions 1 to 4 (the whole paper)")
