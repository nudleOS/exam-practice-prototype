"""Grade 10 Business Studies P1 November 2024 (North West Department of Education, provincial assessment), the whole paper (Sections
A, B and C, 150 marks, 2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options,
marks and memo points are the paper's and the memo's own; clues are ours. Source (PROVENANCE-g10-g11.md): education.nwpg.gov.za,
Examination > Assessment, the question paper PDF (English, 9 pages, text layer) and the marking guidelines PDF (English, 27 pages).

  python tools/ingest/transcribe_g10_bs_p1_2024_11_nw.py
  python tools/ingest/ingest.py "uploads/provincial/g10-bs-p1-2024-11-nw/12-November-24-NW-GR10-S2-BUSINESS-STUDIES-QP-P1-ENG.pdf" "uploads/provincial/g10-bs-p1-2024-11-nw/12-November-2024-NW-GR10-S2-Business-Studies-MG-P1-ENG.pdf" --id g10-bs-p1-2024-11-nw --from-json

The Business Studies rulings, as in transcribe_g11_bs_p1_2024_11_ec.py (Murci 2026-10-10): every written part plays as statements to
pick (the memo's points and clearly wrong ones; a card is worth what the memo ticks for one point: √ 1, √√ 2, a name with its quote 3);
a quote from the scenario as picking its sentences; 'distinguish' as a sort; Section B answers any TWO, Section C any ONE; each essay as
sections (one per memo heading, scaled so the facts sum to the memo's cap of 32) and an insight part (LASO, 8). The paper's marks are
used where the memo's breakdown differs (2.6: 4, 3.7: 6; the paper's questions then total 40)."""
from provincial import Paper, sentences

P = Paper("g10-bs-p1-2024-11-nw", 595.2, 841.92, {}, start=11)
answer, stmt, mcq, term, sort, essay = P.answer, P.stmt, P.mcq, P.term, P.sort, P.essay
pick = lambda n, q, opts, pool, clues: {"t": "pickn", "n": n, "marks": len(pool), "q": q, "clues": clues, "opts": opts, "pool": pool,
                                        "count": len(pool)}
INSIGHT_CLUES = ["Insight is earned from how you answered the sections.", "Right first time, every heading answered, and the examples picked."]

# ---- SECTION A, QUESTION 1, the question paper pages 3-5 and the memo page 8 ----
q11 = [
    mcq("1.1.1", "The business has full control over the … environment.", ["micro", "macro", "market", "external"], 0,
        ["It is the business's own internal environment.", "Vision, mission, resources, culture."]),
    mcq("1.1.2", "Finah Supermarket operates in the … sector because they sell groceries to customers.",
        ["secondary", "tertiary", "primary", "public"], 1, ["Selling to customers is trade.", "Trade and services are the third sector."]),
    mcq("1.1.3", "This level of management is responsible for high productivity, technical assistance and motivating employees.",
        ["General level management", "Lower level management", "Top level management", "Middle level management"], 1,
        ["This level works closest to the workers.", "Supervisors and foremen."]),
    mcq("1.1.4", "The process of setting goals and developing strategies is known as …", ["organising.", "controlling.", "planning.",
        "leading."], 2, ["It comes first among the management tasks.", "Deciding what to do and how."]),
    mcq("1.1.5", "… includes setting targets, measuring performance and taking corrective measures.",
        ["Quality", "Quality control", "Quality circles", "Quality assurance"], 1,
        ["It checks the work against targets.", "It corrects what does not meet the standard."])]
WORDS = "culture; global; working capital; structure; mission; planning; vision; organising; economic; fixed capital"
q12 = [
    term("1.2.1", "The … is used to finance long-term capital needs of the business.", ["fixed capital"],
         ["Long term: buildings and machinery.", "The opposite of working capital."], marks=2),
    term("1.2.2", "A process of breaking a plan into action is known as …", ["organising"], ["It follows planning.",
                                                                                          "Tasks, people and resources are arranged."],
         marks=2),
    term("1.2.3", "The … explains what the business aims to achieve.", ["vision"], ["It looks to the long-term future.",
                                                                                 "Not the mission, which says how."], marks=2),
    term("1.2.4", "Norms, values and expectations are examples of organisational …", ["culture"],
         ["The 'personality' of the business.", "How things are done here."], marks=2),
    term("1.2.5", "The … environment refers to an increase in trade and investment between countries.", ["global"],
         ["Countries trading with each other.", "Globalisation."], marks=2)]
DESC = ["ensures that there is good communication between the business and its stakeholders",
        "all designated race groups should have the same opportunities despite their colour, belief and gender",
        "establishes the sources for acquiring the capital", "protects the economic welfare of the consumers",
        "promotes the development of a credit market that is accessible to all South Africans",
        "takes into account other expenses of the customers",
        "a degree to which people do not have the same opportunities and are treated differently because of their social status",
        "a plan of action taken by top management to achieve their objectives", "a mechanism used to execute a plan",
        "buy in bulk and negotiate for discount"]
q13 = [
    {"t": "match", "n": "1.3", "marks": 10, "q": "Choose a description from COLUMN B that matches a term in COLUMN A (1.3.1 Financial function, "
     "1.3.2 National Consumer Commission, 1.3.3 Public relations, 1.3.4 Inclusive, 1.3.5 Strategy).",
     "clues": ["The financial function finds capital; public relations communicates.", "Inclusive means equal opportunities for all."],
     "left": ["1.3.1 Financial function", "1.3.2 National Consumer Commission", "1.3.3 Public relations", "1.3.4 Inclusive", "1.3.5 Strategy"],
     "right": DESC, "a": [2, 3, 0, 1, 7], "each": 2, "heads": ["COLUMN A", "COLUMN B (A–J)"]}]

# ---- SECTION B, QUESTION 2: BUSINESS ENVIRONMENTS, the question paper pages 6-7 and the memo pages 9-11 ----
HM = ("Handa Manufacturers specialises in manufacturing ladies clothing and handbags. HM is located in an area where there is high rate of "
      "crime. Peter, one of the employees is not productive due to an illness that compromises his immune system.")
JFP = ("Jacob is the founder of Jay Forestry Plantation. He is the main supplier of timber in Zeerust. JFP borrowed capital from Cazet Bank "
       "to finance their expenses.")
q2 = [
    stmt("2.1", "List any FOUR components of the micro environment.", 4,
         ["Vision", "Mission", "Objectives", "Organisational resources", "Leadership and management"], ["Competitors", "Suppliers", "Inflation"],
         ["The micro environment is inside the business.", "The business controls it."], 1),
    stmt("2.2", "Outline the purpose of organisational culture.", 6,
         ["It influences people's actions and attitudes.", "It determines how things are done.", "It is the 'personality' of the business.",
          "It gives a shared understanding of how things are done."],
         ["It sets the prices of the business's products.", "It decides the exchange rate.", "It is the legal registration of the business."],
         ["Culture is about values and behaviour.", "What does it shape in the people?"], 2),
    pick("2.3.1", "Quote TWO examples of socio-economic issues from the scenario above.", sentences(HM), [1, 2],
         ["Look for crime and illness.", "What the business makes is not a socio-economic issue."]),
    stmt("2.3.2", "Explain the negative impact of the examples of socio-economic issues identified in QUESTION 2.3.1.", 6,
         ["Loss of skilled staff due to HIV/Aids-related illnesses.", "High absenteeism from illness decreases productivity.",
          "Insurance and security costs become expensive.", "Loss of profits due to stolen goods."],
         ["Crime increases the business's sales.", "HIV/Aids lowers the cost of medical benefits.", "Illness among staff improves productivity."],
         ["Crime and illness both cost the business.", "Think of staff, production and costs."], 2, after=["2.3.1"]),
    stmt("2.4", "Discuss possible solutions to unemployment.", 6,
         ["Improve skills through better education and training.", "Businesses provide skills development programmes through learnerships.",
          "Offer bursaries to the community to improve the level of education.", "Provide entrepreneurial programmes that promote "
                                                                               "self-employment.",
          "Support existing small businesses to create more employment opportunities."],
         ["Close small businesses so that big ones can hire.", "Stop all training to save money.", "Raise taxes on new businesses."],
         ["How can people become employable?", "How can more jobs be created?"], 2),
    stmt("2.5", "Identify TWO business sectors represented by JFP. Motivate your answer by quoting from the scenario above.", 6,
         ["Primary sector: 'He is the main supplier of timber in Zeerust.'",
          "Tertiary sector: 'JFP borrowed capital from Cazet Bank to finance their expenses.'"],
         ["Secondary sector: 'He is the main supplier of timber in Zeerust.'", "Public sector: 'Jacob is the founder of Jay Forestry "
                                                                               "Plantation.'",
          "Informal sector: 'JFP borrowed capital from Cazet Bank to finance their expenses.'"],
         ["Timber comes from nature; banking is a service.", "Name each sector with its quote."], 3),
    stmt("2.6", "Explain the interrelation between business and consumers.", 4,
         ["Consumers depend on businesses for goods and services, and businesses depend on consumers for income.",
          "Without consumers a business cannot survive, so it must produce goods of consistently high quality.",
          "The public relations department keeps a positive image so that customers remain loyal.",
          "The marketing department researches the target market to satisfy consumers' changing needs."],
         ["Businesses do not need consumers if their products are good.", "Consumers have no influence on what businesses make.",
          "Only the government decides what consumers buy."],
         ["Who depends on whom?", "What must the business do to keep its customers?"], 2),
    stmt("2.7", "Advise businesses on the importance of the formal sector.", 6,
         ["They supply legal products.", "They employ many people with different skills and qualifications.",
          "Their products are guaranteed, so faulty goods can be returned.", "They pay taxes that the government uses for services."],
         ["They avoid paying tax.", "They sell goods without any guarantee.", "They are not registered with the government."],
         ["The formal sector is registered and regulated.", "What do customers and workers gain?"], 2)]

# ---- QUESTION 3: BUSINESS OPERATIONS, the question paper page 7 and the memo pages 12-14 ----
MHS = ("Mercy is the owner of Mercy's Hair Studio. She recently appointed Gontse to assist her at the salon. Gontse ensures that reliable "
       "information is available for decision making.")
q3 = [
    stmt("3.1", "Name any THREE factors that influence the organisational structure.", 3,
         ["The size of the company", "Technology", "Resources", "The strategic goals of the company"],
         ["The weather", "The colour of the logo", "The owner's age"],
         ["What decides how many levels and departments a business needs?", "Size, goals, resources."], 1),
    stmt("3.2", "Outline the quality indicators of the human resources function.", 6,
         ["A low rate of staff turnover in the business.", "Motivate and reward employees.", "Provide good working conditions.",
          "Offer performance incentives to enhance productivity.", "Maintain a healthy relationship between employees and employer."],
         ["A high rate of staff turnover.", "Pay employees late.", "Keep the business goals secret from employees."],
         ["Quality HR keeps good staff.", "How are employees treated?"], 2),
    stmt("3.3.1", "Identify the business function that is applied by MHS. Motivate your answer by quoting from the scenario above.", 3,
         ["Administration: 'Gontse ensures that reliable information is available for decision making.'"],
         ["Marketing: 'Gontse ensures that reliable information is available for decision making.'",
          "Human resources: 'She recently appointed Gontse to assist her at the salon.'",
          "Financial: 'Mercy is the owner of Mercy's Hair Studio.'",
          "Production: 'She recently appointed Gontse to assist her at the salon.'"],
         ["Which function handles information?", "Name the function with its quote."], 3),
    stmt("3.3.2", "Explain the purpose of the business function identified in QUESTION 3.3.1.", 6,
         ["It handles information and data.", "It collects, processes and distributes information that management uses for decisions.",
          "It stores and records information using recent technology.", "It does general office work such as filing."],
         ["It manufactures the business's products.", "It sets the selling prices.", "It recruits new employees."],
         ["The function is administration.", "What does it do with information?"], 2, after=["3.3.1"]),
    stmt("3.4", "Discuss the quality indicators of the financial function.", 6,
         ["Financial records are kept up to date.", "Cash is managed effectively by cash budgeting.",
          "There is accountability through tight financial processes.", "Better interest rates are negotiated to keep financial costs down.",
          "Accurate financial statements are drawn up regularly."],
         ["Financial records are updated once every five years.", "Surplus funds are left idle.", "Loans are taken at the highest interest rates."],
         ["Quality finance is accurate and controlled.", "Records, cash, statements, costs."], 2),
    sort("3.5", "Distinguish between external and internal public relations.", ["External public relations", "Internal public relations"],
         [("Creates a good company image and awareness among people outside the business", 0),
          ("Builds relationships with customers, suppliers and the community", 0),
          ("Creates a good company image and awareness among the employees in the business", 1),
          ("Keeps employees informed through newsletters and staff meetings", 1)],
         ["External is outside the business; internal is inside.", "Who is the audience?"]),
    stmt("3.6", "Explain the quality indicators of the general management function.", 6,
         ["Develop, implement and monitor effective strategic plans.", "Set direction and establish priorities for the business.",
          "Effectively communicate a shared vision, mission and values.", "Ensure that all departments meet their deadlines and targets.",
          "Set an example of the ethics and productivity expected from employees."],
         ["Keep the vision and mission secret.", "Let each department ignore deadlines.", "Avoid learning about changes in the environment."],
         ["General management leads the whole business.", "Plans, direction, communication, example."], 2),
    stmt("3.7", "Evaluate the correlation between management and the success of the business in achieving its objectives.", 6,
         ["Management makes the correct decisions and motivates employees to be productive.",
          "Poor management can result in ineffective employees and lost productivity.",
          "Businesses require ongoing decision-making and problem solving.",
          "Problems not solved and decisions not made appropriately can decrease productivity."],
         ["Management has no effect on whether objectives are achieved.", "Good management always lowers productivity.",
          "Businesses succeed without making decisions."],
         ["Good management leads to success; poor management to failure.", "Decisions and motivation."], 2)]

# ---- QUESTION 4: MISCELLANEOUS TOPICS, the question paper pages 7-8 and the memo pages 14-17 ----
NFH = ("Naidoo Fresh Hub is known for selling fresh fruits and vegetables. NFH buy their stock from Zakes Farm. Naidoo Fresh Hub lost many "
       "of their customers to People's Market who also sell fruits and vegetables at lower prices.")
RE = ("Rolex Electronics is known for selling quality products. Rolly the owner of RE mentioned that quality enables his business to have a "
      "good reputation and promotes brand awareness. RE has also gained goodwill and support from the community.")
q4 = [
    stmt("4.1", "Elaborate on the meaning of the macro environment.", 4,
         ["Conditions that exist in the economy as a whole, rather than in a particular sector or region.",
          "The interaction of businesses with forces outside themselves.", "It is also known as the external environment.",
          "The business has no control over this environment."],
         ["The business has full control over the macro environment.", "It consists only of the business's own employees.",
          "It never changes."],
         ["Macro means large and outside.", "Can the business control it?"], 2),
    stmt("4.2", "Explain the reasons why the economic component poses a challenge to businesses.", 4,
         ["High inflation means consumers have less money to spend on goods and services.",
          "Higher taxes mean businesses are charged more and people have less to spend.",
          "Exchange rates make raw materials and machinery from overseas expensive.",
          "Higher interest rates mean higher monthly instalments on loans."],
         ["Inflation gives consumers more money to spend.", "Lower interest rates increase loan instalments.",
          "Taxes have no effect on businesses."],
         ["Inflation, taxes, exchange rates, interest rates.", "How does each affect costs or spending?"], 2),
    stmt("4.3.1", "Identify TWO components of the market environment that are applicable to NFH. Motivate your answer by quoting from the "
                  "scenario above.", 6,
         ["Suppliers: 'NFH buy their stock from Zakes Farm.'",
          "Competitors: 'Naidoo Fresh Hub lost many of their customers to People's Market who also sell fruits and vegetables at lower "
          "prices.'"],
         ["Consumers: 'NFH buy their stock from Zakes Farm.'", "Intermediaries: 'Naidoo Fresh Hub is known for selling fresh fruits and "
                                                                "vegetables.'",
          "Regulators: 'NFH buy their stock from Zakes Farm.'"],
         ["Who sells to NFH, and who takes its customers?", "Name each component with its quote."], 3),
    stmt("4.4", "Evaluate the reasons why competition poses a challenge to businesses.", 6,
         ["Competition keeps prices down and reduces the business's profitability.",
          "It forces businesses to find new ways to produce existing products or develop new ones.",
          "A business may close down if it is unable to compete.", "Competition reduces the business's market share."],
         ["Competition always raises the business's prices.", "Competition increases the business's market share.",
          "Competitors have no effect on a business."],
         ["What happens to prices and customers?", "What must the business do to keep up?"], 2),
    stmt("4.5", "Name any TWO activities of the administration function.", 2,
         ["Management of information", "Handling of information", "Office practice", "Information technology"],
         ["Recruiting employees", "Manufacturing products", "Advertising"],
         ["Administration deals with information.", "Office work."], 1),
    stmt("4.6", "Outline the importance of public relations.", 6,
         ["The business gets publicity for promotional events through the media.",
          "News conferences release information that helps the business survive.", "Businesses can sponsor community events.",
          "Annual reports show the business's activities and achievements.",
          "Corporate social responsibility gives the business positive exposure in communities."],
         ["Public relations hides information from the public.", "It is only used to collect debts.", "It replaces the business's products."],
         ["Public relations builds the business's image.", "Media, events, reports, community."], 2),
    pick("4.7.1", "Quote the importance of quality in the business.", sentences(RE), [1, 2],
         ["Look for what quality does for RE.", "Reputation, brand, goodwill."]),
    stmt("4.7.2", "Explain other importance of quality in businesses.", 6,
         ["Customers associate the image of the business with the quality of its products.",
          "Quality products increase sales, profits and business growth, and attract investors.",
          "The vision, mission and business goals may be achieved.", "Quality products lead to fewer returns and complaints, saving costs."],
         ["Quality products always lower sales.", "Quality has no link to the business's image.", "Poor quality attracts investors."],
         ["What does quality do for sales and image?", "Do not repeat the scenario's points."], 2, after=["4.7.1"]),
    sort("4.8", "Distinguish between quality control and quality assurance.", ["Quality control", "Quality assurance"],
         [("Inspection of the final product to make sure it meets the required standards", 0),
          ("Includes setting targets, measuring performance and taking corrective measures", 0),
          ("Carried out during and after production, so standards are met at every stage", 1),
          ("Building quality in, rather than checking for it", 1)],
         ["Control checks after; assurance builds in all the way.", "Which happens at every stage?"])]

# ---- SECTION C, QUESTION 5: the essay, the question paper page 9 and the memo pages 18-21 ----
Q5_STEM = ("Socio-economic issues such as strikes and political disturbances have a negative impact on businesses. It is crucial that "
           "management understand why socio-economic issues pose a challenge in their operations and they must also put measures in place "
           "to respond to those challenges. Businesses should employ people from different designated groups.\n\nBearing the above "
           "statement in mind, write a detailed essay on the following aspects:\n• Explain the meaning of strikes.\n• Discuss the negative "
           "impacts of strikes and political disturbances on businesses.\n• Outline the purpose of inclusivity in the workplace.\n• Advise "
           "management on reasons why socio-economic issues pose a challenge to businesses.")
Q5_EX = ["For example, a factory loses a month's production and misses its delivery contracts when its workers strike over wages.",
         "For example, a township spaza shop faces higher costs after rising crime forces it to install burglar bars and alarms."]
q5 = essay("5.7", [
    stmt("5.1", "Introduction: pick the TWO statements that introduce this essay on socio-economic issues.", 2,
         ["Businesses can grow into successful enterprises if they take socio-economic issues into consideration.",
          "Socio-economic issues present both challenges and opportunities for entrepreneurs.",
          "A diverse workforce allows businesses to address inequality as a socio-economic issue."],
         ["Socio-economic issues never affect businesses.", "Strikes always increase a business's profits.",
          "Businesses should employ people from one group only."],
         ["An introduction says what the essay is about.", "Which cards say something true?"], 1),
    stmt("5.2", "Explain the meaning of strikes.", 6,
         ["A strike is a collective refusal of employees to work because of an issue in the workplace.",
          "It is collective action by unhappy employees to force employers to accept their demands.",
          "Strikes may take the form of a go-slow or a sympathy strike.",
          "It is a dispute when employer and employees cannot agree on wages or working conditions, even after negotiations."],
         ["A strike is when the employer closes the business for a holiday.", "A strike is one employee resigning.",
          "A strike is a meeting to celebrate good results."],
         ["Who refuses to work, and why?", "It is collective."], 2),
    stmt("5.3", "Discuss the negative impacts of strikes and political disturbances on businesses.", 8,
         ["The business may be unable to meet its contractual obligations and lose contracts.",
          "Production is lost as employees stay away from work.", "Strikes can be violent when strikers intimidate other employees.",
          "Political disturbances may scare off potential investors.", "Businesses suffer losses from damage to property during riots."]
         + [Q5_EX[0]],
         ["Strikes increase the business's production."], ["Who loses when work stops?", "Contracts, production, investors, property."], 2),
    stmt("5.4", "Outline the purpose of inclusivity in the workplace.", 8,
         ["Inclusivity enables businesses to make the best use of all human resources.", "It increases tolerance of each other's ideas and "
                                                                                       "beliefs.",
          "Businesses can use a variety of talents and skills.", "It promotes respect for each person and their contribution.",
          "It promotes a happy working environment, which increases job satisfaction and productivity."],
         ["Inclusivity means employing people from one group only.", "It reduces communication in the workplace.",
          "It lowers job satisfaction."],
         ["Inclusivity includes everyone.", "What does a business gain from diverse staff?"], 2),
    stmt("5.5", "Advise management on reasons why socio-economic issues pose a challenge to businesses.", 6,
         ["Poverty and unemployment reduce consumer spending.",
          "Businesses must spend on policies and programmes to address these issues.",
          "Counterfeiting, bootlegging and crime may lead to a loss of profits.", Q5_EX[1]],
         ["Socio-economic issues increase consumers' disposable income.", "Crime lowers the business's security costs.",
          "These issues never affect productivity."],
         ["What do these issues do to customers and costs?", "Spending, costs, profits."], 2),
    stmt("5.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["Businesses that develop strategies to deal with socio-economic issues survive long enough to achieve long-term goals.",
          "Businesses must be aware of these challenges so that they can put strategies in place to overcome them."],
         ["Socio-economic issues can be ignored by businesses.", "Strikes are good for every business.",
          "Inclusivity should be avoided in the workplace."],
         ["A conclusion sums up why it all matters.", "Which card would a business agree with?"], 2),
], [("5.3", Q5_EX[0]), ("5.5", Q5_EX[1])], INSIGHT_CLUES)

# ---- QUESTION 6: the essay, the question paper page 9 and the memo pages 22-26 ----
Q6_STEM = ("The purchasing function plays an important role in purchasing quality raw materials and services for the business. The "
           "purchasing manager needs to ensure that the business has sufficient capital and follows the purchasing procedure to place an "
           "order. The National Credit Act impacts the business both positively and negatively.\n\nWrite an essay on the following "
           "aspects:\n• Outline the purpose of the purchasing function.\n• Explain the differences between credit payment and cash "
           "payment.\n• Discuss the purchasing procedure.\n• Advise businesses on the impact of the National Credit Act on businesses.")
Q6_EX = ["For example, a bakery compares quotes from three flour mills before choosing the cheapest reliable supplier.",
         "For example, a furniture store loses sales when fewer customers qualify for credit under the NCA."]
q6 = essay("6.7", [
    stmt("6.1", "Introduction: pick the TWO statements that introduce this essay on the purchasing function.", 2,
         ["The purchasing function is responsible for buying quality raw materials and services for the business.",
          "The purchasing function places orders with suppliers and follows them up so that products are delivered on time.",
          "The National Credit Act affects how businesses buy and sell on credit."],
         ["The purchasing function sells the business's products.", "Cash and credit payments are the same.",
          "The National Credit Act has no effect on businesses."],
         ["An introduction says what the essay is about.", "Which cards say something true?"], 1),
    stmt("6.2", "Outline the purpose of the purchasing function.", 6,
         ["Buy quality raw materials and services for the business.", "Continuously look for new and better suppliers.",
          "Place orders with suppliers and follow them up so that goods are delivered on time.",
          "Make sure goods arrive at the agreed price, in the right quantities and of the right quality."],
         ["Obtain capital from the most suitable sources.", "Draw up the business's financial statements.", "Advertise the business's products."],
         ["Purchasing buys what the business needs.", "Suppliers, orders, price, quality."], 2),
    sort("6.3", "Explain the differences between credit payment and cash payment.", ["Cash payment", "Credit payment"],
         [("All payments made in cash or by cheque for business purchases", 0),
          ("Enables businesses to budget for stock purchases and avoid delays", 0),
          ("Cash payers can qualify for cash discounts", 0),
          ("Payments made by credit card or on a future date for business purchases", 1),
          ("Allows the business to buy stock now and pay on a future date", 1),
          ("The payer can pay more for goods because interest is added", 1),
          ("No interest is paid on the purchase", 0), ("The business needs to qualify to buy this way", 1)],
         ["Cash is paid now; credit is paid later.", "Which one can carry interest?"]),
    stmt("6.4", "Discuss the purchasing procedure.", 8,
         ["Determine the need: liaise with the financial department to set the budget and the product needs.",
          "Determine the price: obtain quotes or tenders to find the best price.",
          "Select a suitable supplier based on quality, price and delivery time.",
          "Place the order in writing and confirm the prices.", "Receive the order and check its quality and quantity against the order.",
          "Pay the supplier after satisfactory delivery.", Q6_EX[0]],
         ["Pay the supplier before deciding what to buy."], ["Need, price, supplier, order, receive, pay.", "Follow the steps in order."], 2),
    stmt("6.5", "Advise businesses on the impact of the National Credit Act on businesses.", 6,
         ["Positive: lower bad debts result in better cash flow.", "Positive: it prevents reckless lending by financial institutions.",
          "Negative: businesses can no longer carry out credit marketing.",
          "Negative: the Act complicates purchasing with administration in the credit process.", Q6_EX[1]],
         ["The NCA allows reckless lending.", "The NCA forces businesses to sell poor quality goods.",
          "The NCA removes all paperwork from credit."],
         ["The NCA protects consumers and limits credit.", "Give positives and negatives."], 2),
    stmt("6.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["The business needs a sound understanding of the National Credit Act, as it can impact the business both positively and "
          "negatively.",
          "A business that follows the purchasing procedure buys the right goods at the right price and time."],
         ["The purchasing procedure can be skipped.", "Credit payments are always cheaper than cash.",
          "The NCA should be ignored by businesses."],
         ["A conclusion sums up why it all matters.", "Which card would a business agree with?"], 2),
], [("6.4", Q6_EX[0]), ("6.5", Q6_EX[1])], INSIGHT_CLUES)

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 10,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Complete the statements", "marks": 10,
     "lead": "Complete the following statements by using the word(s) provided in the list below.\n" + WORDS, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column A and Column B", "marks": 10,
     "lead": "Choose a description from COLUMN B that matches a term in COLUMN A.", "items": q13},
    {"id": "2.1", "title": "Question 2", "kind": "Business environments", "marks": 40,
     "lead": "QUESTION 2: BUSINESS ENVIRONMENTS\n2.3 HANDA MANUFACTURERS (HM)\n" + HM + "\n2.5 JAY FORESTRY PLANTATION (JFP)\n" + JFP,
     "items": q2},
    {"id": "3.1", "title": "Question 3", "kind": "Business operations", "marks": 40,
     "lead": "QUESTION 3: BUSINESS OPERATIONS\n3.3 MERCY'S HAIR STUDIO (MHS)\n" + MHS, "items": q3},
    {"id": "4.1", "title": "Question 4", "kind": "Miscellaneous topics", "marks": 40,
     "lead": "QUESTION 4: MISCELLANEOUS TOPICS\n4.3 NAIDOO FRESH HUB (NFH)\n" + NFH + "\n4.7 ROLEX ELECTRONICS (RE)\n" + RE, "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Essay: socio-economic issues", "marks": 40,
     "lead": "Build the essay section by section, then see your insight.", "extract": "QUESTION 5: THE ESSAY\n\n" + Q5_STEM, "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Essay: business functions", "marks": 40,
     "lead": "Build the essay section by section, then see your insight.", "extract": "QUESTION 6: THE ESSAY\n\n" + Q6_STEM, "items": q6},
]
P.finish(missions,
         {"subject": "Business Studies", "title": "Business Studies P1", "sitting": "November 2024", "total_marks": 150, "time": "2 hours"},
         [{"n": "2.3.1", "kind": "no_fit", "detail": "Quote items (2.3.1, 4.7.1) are played by picking the scenario's sentences, as Grade 12; "
                                                     "a sector, function or component with its quote is one card (3 marks: the memo's 2 + 1)."},
          {"n": "5.7", "kind": "no_fit", "detail": "Each essay plays as sections, one per memo heading, their facts scaled to sum to the memo's "
                                                   "cap of 32 (Question 5: 2 + 6 + 8 + 8 + 6 + 2 of the memo's 2 + 8 + 12 + 14 + 12 + 2; "
                                                   "Question 6: 2 + 6 + 8 + 8 + 6 + 2 of 2 + 10 + 12 + 12 + 12 + 2), then insight (8)."},
          {"n": "6.2", "kind": "memo_issue", "detail": "The memo's 6.2 'purpose of the purchasing function' lists the financial function's "
                                                       "quality indicators (capital, interest rates, financial records and statements, "
                                                       "surplus funds). The cards use the purchasing purposes the memo itself gives in 6.1 "
                                                       "(buying quality materials, finding suppliers, following up orders, right price, "
                                                       "quantity and quality); two financial points are wrong cards. For Murci to confirm."},
          {"n": "2.6", "kind": "low_confidence", "detail": "The memo's breakdown gives 2.6 (4) and 3.7 (4) while its answers show Max (6); the "
                                                           "paper prints 2.6 (4) and 3.7 (6), which total each question to 40. The paper's "
                                                           "marks are used."}],
         {"1": 30, "2": 40, "3": 40, "4": 40, "5": 40, "6": 40}, 150, {"2.3.2": ["2.3.1"], "3.3.2": ["3.3.1"], "4.7.2": ["4.7.1"]},
         "Sections A, B and C (the whole paper)",
         sections=[("Section A", 30, None, ["1"]), ("Section B", 80, 2, ["2", "3", "4"]), ("Section C", 40, 1, ["5", "6"])])
