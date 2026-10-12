"""Grade 11 Business Studies P1 November 2024 (Eastern Cape Department of Education), the whole paper (Sections A, B and C, 150 marks,
2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options, marks and memo points are
the paper's and the memo's own; clues are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2024_November_Gr_11_Exams, the question
paper zip (English PDF 'Final ENG', 9 pages, text layer) and the memo zip (English, 27 pages).

  python tools/ingest/transcribe_g11_bs_p1_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-bs-p1-2024-11-ec/BUSINESS STUDIES P1 GR 11 NOV Final ENG D_watermark.pdf" "uploads/provincial/g11-bs-p1-2024-11-ec/BUSINESS STUDIES P1 GR11 MEMO NOV2024 -English_watermark.pdf" --id g11-bs-p1-2024-11-ec --from-json

The Business Studies rulings, as in transcribe_bs_p1_2024_11.py (Murci 2026-10-10): every written part plays as statements to pick
(the memo's points and clearly wrong ones; a card is worth what the memo ticks for one point: √ 1, √√ 2, a name with its description
3); a quote from the scenario as picking its sentences; Section B answers any TWO, Section C any ONE; each essay as sections (one per
memo heading, scaled so the facts sum to the memo's cap of 32) and an insight part (LASO, 8)."""
from provincial import Paper, sentences

P = Paper("g11-bs-p1-2024-11-ec", 595.22, 842.0, {}, start=9)
answer, stmt, mcq, term, sort, essay = P.answer, P.stmt, P.mcq, P.term, P.sort, P.essay
pick = lambda n, q, opts, pool, clues: {"t": "pickn", "n": n, "marks": len(pool), "q": q, "clues": clues, "opts": opts, "pool": pool,
                                        "count": len(pool)}
INSIGHT_CLUES = ["Insight is earned from how you answered the sections.", "Right first time, every heading answered, and the examples picked."]

# ---- SECTION A, QUESTION 1, the question paper pages 3-5 and the memo page 7 ----
q11 = [
    mcq("1.1.1", "The … is an example of contemporary legislation that guard against discriminatory appointments in business operations.",
        ["Labour Relations Act (LRA), 1995 (Act 66 of 1995)", "Basic Conditions of Employment Act (BCEA), 1997 (Act 75 of 1997)",
         "Employment Equity Act (EEA), 1998 (Act 55 of 1998)", "Compensation for Occupational Injuries and Disease Act (COIDA), 1997 "
                                                                "(Act 61 of 1997)"], 2,
        ["Discrimination in appointments is about fairness and equity.", "Which Act's name says 'equity'?"]),
    mcq("1.1.2", "Paw Prints and Pet Food are two retailers combined to become one business. This is called a/an …",
        ["merger.", "takeover.", "acquisitions.", "alliances."], 0, ["Both agree to join.", "A takeover is one buying the other."]),
    mcq("1.1.3", "Goods enter South Africa from China at a price that is cheaper than the normal value of the goods in a domestic country. "
        "This is known as …", ["globalisation.", "dumping.", "economic crime.", "exports."], 1,
        ["Selling below normal value in another country.", "The goods are 'dumped' on the market."]),
    mcq("1.1.4", "The type of packaging where cooldrink cans have the flags of all the countries competing in the Olympic Games in Paris.",
        ["Speciality packaging", "Kaleidoscopic packaging", "Packaging for double use", "Combination packaging"], 1,
        ["The design changes for a special event.", "Many colourful designs."]),
    mcq("1.1.5", "The Human Resources activity where a new employee is placed where he/she will function optimally and add value.",
        ["Recruitment", "Selection", "Placement", "Induction"], 2, ["The word is in the question.", "Where the employee is put."])]
WORDS = ("demographics; penetration; lock-out; loading; go-slow; Unemployment Insurance Fund; psychographics; mark-up; routing; "
         "Compensation Fund")
q12 = [
    term("1.2.1", "A form of industrial action where employers refuse employees entry during a strike action is called a …", ["lock-out",
                                                                                                                             "lockout"],
         ["The employer's weapon.", "The gates are locked."], marks=2),
    term("1.2.2", "Tasco Manufacturers studied the attitudes and tastes of their target market. This is an example of …", ["psychographics"],
         ["Attitudes and tastes, not age and income.", "Psycho- means the mind."], marks=2),
    term("1.2.3", "The … pricing is where products are sold at a very low price, to attract customers to a new product in the market.",
         ["penetration"], ["Entering a market.", "The opposite of skimming."], marks=2),
    term("1.2.4", "The production process where tasks are allocated to the responsible employee, is known as …", ["loading"],
         ["Production planning: routing, scheduling, …", "Work is 'loaded' onto workers."], marks=2),
    term("1.2.5", "It is compulsory for Liozzi Ltd to contribute 1% of employees' salary towards the …", ["Unemployment Insurance Fund", "UIF"],
         ["For workers who lose their jobs.", "Employer 1% and employee 1%."], marks=2)]
DESC = ["these are low priced goods purchased by consumers without much thought",
        "identify the most suitable candidate for the vacancy",
        "granting of mortgage bonds to people who cannot obtain credit from banks",
        "refers to what the business wants to achieve in the long term",
        "granting of small loans to people who cannot obtain credit from banks",
        "refers to what the business provides/produces",
        "identify vacancies to attract suitable candidates",
        "quality checks that are done after the production process",
        "these are high priced goods and require time and effort to be purchase by consumers",
        "quality checks are done during and after the production process"]
q13 = [
    {"t": "match", "n": "1.3", "marks": 10, "q": "Choose a description from COLUMN B that matches a term in COLUMN A (1.3.1 Vision, 1.3.2 "
     "Micro-lending, 1.3.3 Quality assurance, 1.3.4 Shopping goods, 1.3.5 Recruitment).",
     "clues": ["Vision looks to the long term; micro-lending gives small loans.", "Quality assurance checks during AND after production."],
     "left": ["1.3.1 Vision", "1.3.2 Micro-lending", "1.3.3 Quality assurance", "1.3.4 Shopping goods", "1.3.5 Recruitment"], "right": DESC,
     "a": [3, 4, 9, 8, 6], "each": 2, "heads": ["COLUMN A", "COLUMN B (A–J)"]}]

# ---- SECTION B, QUESTION 2: BUSINESS ENVIRONMENTS, the question paper page 6 and the memo pages 8-12 ----
HS = ("Happy Sticks sells sport equipment at reasonable prices. All Sports is a new sport shop, and is becoming popular among HS customers. "
      "Some of HS employees are regularly absent from work. Happy Sticks' main supplier sometimes deliver orders late.")
GS = ("Good Supermarket is a general dealer in a rural town in the Eastern Cape. They are struggling to find employees that are trained to "
      "perform their duties. Most of the community members cannot read or write. There was a decline in their profitability during the past "
      "financial year.")
q2 = [
    stmt("2.1", "Name TWO types of business sectors.", 2, ["Primary sector", "Secondary sector", "Tertiary sector"],
         ["Private sector of the stock exchange", "Informal environment", "Market sector of the micro environment"],
         ["Nature, manufacturing, services.", "First, second, third."], 1),
    stmt("2.2", "Outline the advantages of networking.", 6,
         ["Businesses can attract new customers, resulting in increased market share and profitability.",
          "Networking can be an excellent source of new perspectives and business ideas.",
          "It allows managers to build new business relationships and generate new business opportunities.",
          "It plays a role in the marketing and expansion of a business.", "It assists businesses in making future business decisions."],
         ["Networking means the business never has to advertise again.", "Networking guarantees that the business will make a profit.",
          "Networking lets businesses avoid paying tax."], ["Networking builds relationships with other businesses.",
                                                           "What can those contacts bring?"], 2),
    pick("2.3.1", "Quote TWO challenges of the market environment in the scenario above.", sentences(HS), [1, 3],
         ["The market environment: competitors, suppliers, customers.", "Employees are in the micro environment."]),
    stmt("2.3.2", "Suggest ways in which businesses can overcome competition in the market.", 4,
         ["Produce unique (differentiated) goods or services that satisfy the target market's needs.",
          "Price goods and services lower than competitors' goods and services.",
          "Improve customer service and ensure client satisfaction.",
          "Undertake good marketing campaigns, such as posters or social media campaigns."],
         ["Copy the competitor's brand name exactly.", "Raise prices so that customers think the goods are better.",
          "Stop advertising to save money."], ["How can HS win customers back?", "Price, quality, service, marketing."], 2),
    stmt("2.4", "Describe projects that can be undertaken by businesses as part of their social responsibility.", 6,
         ["Allow employees to get involved in social development programmes.", "Engage in environmentally friendly campaigns, such as "
                                                                              "recycling.",
          "Support less fortunate people by donating to charity organisations.", "Build schools or offer bursaries to needy students.",
          "Sponsor art and cultural programmes, such as school choirs."],
         ["Pay employees less to fund the business's own projects.", "Dump waste in the community to save costs.",
          "Sell products at higher prices to the poor."], ["Social responsibility gives back to the community.",
                                                           "Education, environment, charity."], 2),
    stmt("2.5.1", "Identify TWO socio-economic issues from the scenario above.", 4, ["Lack of skills", "Illiteracy"],
         ["Inflation", "HIV/Aids", "Crime"], ["Read the scenario: training, reading and writing.", "Which issues does GS face?"], 2),
    stmt("2.5.2", "Explain the negative impact of ONE of the socio-economic issues identified in QUESTION 2.5.1.", 4,
         ["Businesses cannot find candidates with adequate skills and experience.",
          "Unskilled employees spend considerable time seeking assistance to perform their work.",
          "Training employees is expensive, and productivity is affected while they learn.",
          "Unskilled employees make errors and have to repeat tasks."],
         ["Unskilled employees make the business more productive.", "A lack of skills lowers the cost of training."],
         ["Take lack of skills.", "What does it cost the business?"], 2)]
q26 = [
    stmt("2.6.1", "Discuss the following type of lobbying: Hedging against inflation.", 4,
         ["Businesses use hedging to protect their financial investments by spreading the risk.",
          "Businesses invest surplus funds so that their value grows faster than inflation.",
          "Businesses buy bonds, shares, property or gold to protect capital from inflation.",
          "It is a way to reduce risk when unsure about possible price fluctuations."],
         ["Hedging means keeping all surplus money in cash.", "Hedging increases the effect of inflation on capital."],
         ["Inflation lowers money's value.", "Invest where value grows."], 2),
    stmt("2.6.2", "Discuss the following type of lobbying: Influencing supervisory body/regulators.", 4,
         ["Through membership and submissions, businesses may influence changes to existing regulations.",
          "Businesses take an active role in professional bodies.", "Business managers take part in debates that shape public policies.",
          "Businesses negotiate with regulators to protect their own sustainability."],
         ["Businesses ignore regulators to save time.", "Regulators are owned by the businesses they supervise."],
         ["Regulators set the rules.", "How can a business have a say?"], 2),
    stmt("2.7", "Suggest ways in which businesses can have a direct influence on the environment.", 4,
         ["Get involved in research and development so that they can continue to operate.",
          "Influence suppliers by signing long-term contracts for raw materials at fixed prices.",
          "Influence customers by creating new uses for a product.", "Influence regulators through lobbying and bargaining."],
         ["Wait for the environment to change on its own.", "Refuse to deal with suppliers and customers."],
         ["Suppliers, customers, regulators.", "Act on them."], 2)]

# ---- QUESTION 3: BUSINESS OPERATIONS, the question paper page 7 and the memo pages 13-16 ----
AS = ("Amazing Snacks (AS) is a catering business that provides platters for business functions. The management of AS uses a sales "
      "promotion strategy to increase sales. AS conducts personal selling of their products to add value to customers. The business has "
      "established strong brand recognition around Gqeberha.")
q3 = [
    stmt("3.1", "Name TWO aspects that must be considered during production control.", 2, ["Dispatching", "Following up", "Inspection",
                                                                                          "Corrective action"],
         ["Recruitment", "Advertising", "Budgeting for tax"], ["Control checks production as it happens.", "Send, follow, inspect, correct."],
         1),
    stmt("3.2", "Outline the importance of pricing.", 4,
         ["Pricing affects the number of products sold, which affects profitability.",
          "The price can influence consumers' attitude towards the product or brand.",
          "If the price is too high, fewer consumers may buy the product.",
          "If the price is too low, consumers may think the goods are of poor quality."],
         ["Price has no effect on how many products are sold.", "A low price always shows high quality."],
         ["Price, sales and profit.", "What do customers think of a price?"], 2),
    pick("3.3.1", "Quote TWO components of the marketing communication policy in the scenario above.", sentences(AS), [1, 2],
         ["Marketing communication: advertising, sales promotion, personal selling …", "Which sentences name one?"]),
    stmt("3.3.2", "Explain the role of public relations in publicity.", 4,
         ["Public relations presents a favourable image of the business and its products.",
          "The public relations department builds good relationships with the media and the press.",
          "It keeps the media informed of product launches and new shops.",
          "It supports marketing efforts to build a brand identity."],
         ["Public relations hides bad news by paying the press.", "Public relations sets the prices of products."],
         ["Image and the media.", "Free coverage."], 2),
    stmt("3.4", "Recommend precautionary measures that businesses should take when handling machinery.", 4,
         ["Familiarise employees with safety procedures.", "Install all machinery correctly and make sure it is safe to use.",
          "Train workers properly on how to use the machinery and inform them of the risks.",
          "Carry out regular safety checks and service the machinery regularly.",
          "Workers must wear protective clothing, such as hard hats and safety boots."],
         ["Remove safety guards to speed up production.", "Let untrained workers learn by trial and error."],
         ["Train, maintain, protect.", "Prevent accidents."], 2),
    stmt("3.5", "Explain Total Quality Management (TQM) as part of the quality management system.", 4,
         ["It is a management philosophy that integrates all organisational functions.",
          "It focuses on improving the quality of products and services to satisfy customers.",
          "It is the responsibility of everyone in the organisation, from top management to general workers.",
          "Businesses strive to get it right the first time."],
         ["Only the quality controller is responsible for quality.", "TQM checks quality once a year only."],
         ["Total: the whole business.", "Everyone, all the time."], 2),
    stmt("3.6.1", "Tasker's Fashion placed an advert on the business's notice board for a new secretary. TF also advertised the vacancy in the "
         "local newspaper. Identify TWO methods of recruitment applicable to TF in the scenario above. Quote from the scenario above to "
         "motivate your answer.", 6,
         ["Internal recruitment: 'They placed an advert on the business's notice board for a new secretary.'",
          "External recruitment: 'TF also advertised the vacancy in the local newspaper.'"],
         ["External recruitment: 'They placed an advert on the business's notice board for a new secretary.'",
          "Internal recruitment: 'TF also advertised the vacancy in the local newspaper.'",
          "Recruitment agency: 'TF calculates the salaries of employees.'"],
         ["A notice board is seen by staff already there.", "A newspaper reaches people outside."], 3),
    stmt("3.6.2", "Discuss TWO salary determination methods.", 6,
         ["Piecemeal: workers are paid according to the number of items (units) produced.",
          "Time-related: workers are paid for the amount of time they spend at work."],
         ["Piecemeal: workers are paid for the hours they spend at work.", "Time-related: workers are paid per item they produce.",
          "Profit-sharing: workers pay the business a share of their wages."],
         ["Paid per item, or per hour.", "Each card gives a method and what it means."], 3),
    stmt("3.7", "Explain the purpose of induction.", 4,
         ["Introduce new employees to management and colleagues, to build relationships.",
          "Explain safety regulations and rules, so that new employees understand their responsibilities.",
          "Give new employees a tour of the layout of the building.", "Familiarise new employees with the organisational structure."],
         ["Decide whether to employ the applicant.", "Advertise the vacancy to the public."],
         ["Induction happens after appointment.", "Welcome and inform."], 2),
    stmt("3.8", "Advise businesses on the requirements of a good trademark.", 4,
         ["It must be attractive and promote the product.", "It must be easy to recognise, remember and pronounce.",
          "It must be different from its competitors'.", "It must promote the image of the enterprise."],
         ["It should look like a competitor's trademark.", "It should be changed every month."],
         ["A trademark identifies a brand.", "Recognisable and unique."], 2)]

# ---- QUESTION 4: MISCELLANEOUS TOPICS, the question paper page 8 and the memo pages 17-19 ----
PT = ["Promotional pricing", "Price skimming", "Penetration pricing", "Cost-plus pricing"]
q4 = [
    stmt("4.1", "Name any FOUR components of the macro environment.", 4,
         ["Physical (natural) environment", "Economic environment", "Social (cultural, demographic) environment", "Technological environment",
          "Legal environment", "Political environment"], ["Management", "Suppliers"],
         ["The macro environment is outside the business's control.", "PESTLE."], 1),
    stmt("4.2", "Outline the reasons why businesses lobby.", 4,
         ["To change laws, such as child labour laws and municipal regulations.",
          "Lobby groups' views make a difference by giving solutions to business challenges.",
          "Lobbying helps to find solutions to emerging challenges.",
          "To influence the prices, policies and regulations of their regulator or supervisory body."],
         ["To avoid paying their suppliers.", "To keep the public uninformed."], ["Lobbying tries to influence decision-makers.",
                                                                                 "Laws, regulators and solutions."], 2),
    answer("4.3.1", "Winning Ways helps businesses to work together to build on the expertise of one another. Identify from the scenario the way "
           "in which businesses can form a power relationship.", 2,
           ["Strategic alliance (partnership agreement)", "Persuasion of large investors", "Company representatives' influence", "Lobbying"],
           ["Working together.", "An agreement between businesses."]),
    stmt("4.3.2", "Discuss TWO other ways in which businesses can form power relationships.", 6,
         ["Persuasion of large investors: a powerful investor helps the business gain credit and better deals.",
          "Company representatives' influence: a representative persuades investors to invest in the business."],
         ["Persuasion of large investors: the business refuses all outside investors.",
          "Company representatives' influence: representatives keep the business's image hidden from investors.",
          "Hostile takeover: the business forces its suppliers to close."],
         ["Other than a strategic alliance.", "Each card gives a way and what it means."], 3),
    stmt("4.4", "Advise businesses on information management as a way to adapt to challenges in the business environments.", 4,
         ["Information must be recorded, stored, easily retrieved and used effectively.",
          "Implement an effective information management system that is accessible to all staff.",
          "Invest capital in information technology systems to update business operations.",
          "Modern IT solutions help businesses satisfy customer needs more efficiently."],
         ["Keep information away from staff.", "Store records only on paper in one office."],
         ["Information helps decisions.", "Systems and technology."], 2),
    answer("4.5.1", "Identify the pricing technique: Fashions Ltd sold winter clothing at the end of the winter season at low prices.", 2,
           [PT[0], PT[1], PT[2], PT[3]], ["End-of-season sale.", "A promotion."]),
    answer("4.5.2", "Identify the pricing technique: Prestige Cellphones sells their new cell phone models at higher prices because of their "
           "prestige value.", 2, [PT[1], PT[0], PT[2], PT[3]], ["A high price for a new product.", "Skim the top of the market."]),
    stmt("4.6", "Explain the importance of product development.", 6,
         ["Products are designed to suit the needs of the customers.", "Without a suitable design there will be very little demand.",
          "New products replace older products when their sales decline.", "Businesses remain competitive by improving their products.",
          "Products become different from those of the competitors."],
         ["Product development stops all competition by law.", "Old products sell more as they age.",
          "Customers' needs never change."], ["Products have a life cycle.", "Stay competitive."], 2),
    stmt("4.7", "Discuss the reasons why manufacturers may prefer to make use of direct distribution methods.", 6,
         ["Manufacturers have control over the product and its marketing.", "They achieve better end-user prices, with no intermediary costs.",
          "They do not share their profit margin with intermediaries.", "There is direct contact with the target market for feedback."],
         ["Intermediaries reduce the manufacturer's control costs to zero.", "Direct distribution needs many wholesalers."],
         ["No middlemen.", "Control, price, profit, feedback."], 2),
    stmt("4.8", "Advise businesses on the reasons why they must manage safety in the workplace.", 4,
         ["Accidents can cause injuries and deaths, and financial trouble for the business.",
          "Publicity of accidents harms the business's image.", "Serious accidents may cause investors to withdraw their money.",
          "Employees may leave to join safer companies."],
         ["Accidents improve the business's reputation.", "Safety laws do not apply to businesses."],
         ["People, image, investors.", "What does an accident cost?"], 2)]

# ---- SECTION C, the essays (answer any ONE), the question paper page 9 and the memo pages 20-27 ----
Q5_STEM = ("Trade unions play an important role to assist businesses on any illegal activities in the workplace. Piracy can have a negative "
           "impact on businesses and must be reported to find solutions. The Labour Relations Act protects the rights of the employer and "
           "employee.\n\nWrite an essay on contemporary socio-economic issues in which you include the following aspects:\n• Outline the "
           "functions of trade unions.\n• Explain the negative impact of piracy on businesses.\n• Discuss solutions to piracy.\n• Advise "
           "businesses on the purpose of the Labour Relations Act.")
Q5_EX = ["For example, a music label loses sales when its new album is copied and streamed illegally online.",
         "For example, a clothing brand registers its logo as a trademark and sues a seller of fake copies."]
q5 = essay("5.7", [
    stmt("5.1", "Introduction: pick the TWO statements that introduce this essay on contemporary socio-economic issues.", 2,
         ["A trade union is a group of employees who associate to protect the rights of their members.",
          "Piracy is the unauthorised use or reproduction of another person's original work.",
          "The LRA puts structures in place with which disputes in the workplace can be settled."],
         ["Piracy is a legal way to share music and films.", "Trade unions are owned by employers to control workers.",
          "The LRA allows employers to dismiss workers without reason."],
         ["An introduction says what the essay is about.", "Which cards say something true?"], 1),
    stmt("5.2", "Outline the functions of trade unions.", 6,
         ["Protecting the interests of workers.", "Influencing management for better working conditions, salaries and benefits.",
          "Providing legal and financial advice to members.", "Protecting members during retrenchments and disciplinary hearings."],
         ["Setting the prices of the business's products.", "Hiring and firing employees for management.",
          "Collecting income tax for SARS."], ["Unions act for workers.", "Pay, conditions, protection."], 2),
    stmt("5.3", "Explain the negative impact of piracy on businesses.", 8,
         ["It undermines the music and movie industry, as they lose money.", "It drives up prices to make up for the lost sales.",
          "It leads to job losses in the industry.", "The industry is reluctant to develop new talent, as the risk is too high.",
          "Businesses lose sales and income."] + [Q5_EX[0]],
         ["Piracy increases the original producer's sales."], ["Copied goods replace paid ones.", "Who loses?"], 2),
    stmt("5.4", "Discuss solutions to piracy.", 8,
         ["Patent: a registered patent stops others from producing and selling the same invention.",
          "Trademarks: a registered trademark identifies the business and its products, and its owner can claim damages.",
          "Copyright: businesses can sue anyone who infringes their copyright.", Q5_EX[1]],
         ["Lower the price until pirates stop.", "Stop producing original work.", "Share all designs freely."],
         ["Protect intellectual property by law.", "Patent, trademark, copyright."], 2),
    stmt("5.5", "Advise businesses on the purpose of the Labour Relations Act.", 6,
         ["It promotes the resolution of labour disputes through the CCMA.", "It regulates the rights of trade unions and facilitates "
                                                                             "collective bargaining.",
          "It promotes fair labour practices between employer and employee.", "It establishes workplace forums where employees take part in "
                                                                              "decision-making."],
         ["It sets the prices of consumer goods.", "It forbids trade unions.", "It allows employers to pay below the minimum wage."],
         ["The LRA governs labour relations.", "Disputes, unions, fairness."], 2),
    stmt("5.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["Trade unions play an important role in protecting the rights of employees.",
          "Businesses should find effective solutions to illegal reproduction of goods that harms artists, owners and businesses."],
         ["Piracy is harmless, so businesses can ignore it.", "Labour legislation only benefits employers.",
          "Trade unions should be banned to end disputes."],
         ["A conclusion sums up why it all matters.", "Which card would a business agree with?"], 2),
], [("5.3", Q5_EX[0]), ("5.4", Q5_EX[1])], INSIGHT_CLUES)
Q6_STEM = ("The Human Resources manager draw up a job analysis in order to determine the job description and job specification. The "
           "selection procedure is implemented thereafter. The interviewer invites prospective candidates for interviews. The successful "
           "candidate must sign an employment contract.\n\nWrite an essay on Human Resources in which you include the following aspects:\n"
           "• Distinguish between a job description and job specification as components of a job analysis.\n• Explain the selection "
           "procedure.\n• Discuss the role of the interviewer during the interview.\n• Advise businesses on the legal requirements of an "
           "employment contract.")
Q6_EX = ["For example, a retailer checks a cashier applicant's references with her previous employer before the interview.",
         "For example, the panel chair thanks each candidate and explains when the outcome will be known."]
q6 = essay("6.7", [
    stmt("6.1", "Introduction: pick the TWO statements that introduce this essay on Human Resources.", 2,
         ["The employer must be clear about the nature of the work so that a job description and job specification can be prepared.",
          "The purpose of the selection process is to choose the applicants most likely to succeed.",
          "An employment contract is a legal document that regulates the terms and conditions of employment."],
         ["An interview is a meeting to set the business's prices.", "An employment contract is signed only by the employer.",
          "A job analysis describes the business's competitors."], ["An introduction says what the essay is about.",
                                                                    "Which cards say something true?"], 1),
    sort("6.2", "Distinguish between a job description and job specification as components of a job analysis.",
         ["Job description", "Job specification", "Not true"],
         [("Describes the duties and responsibilities of a specific job", 0), ("Describes key performance areas, e.g. job title and working "
                                                                               "conditions", 0),
          ("Describes the minimum qualities, skills and qualifications needed", 1), ("Describes the requirements for the person, e.g. "
                                                                                     "formal qualifications", 1),
          ("Describes the business's annual profit", 2), ("Lists the competitors' salaries", 2)],
         ["The job, or the person for the job?", "Ask of each card: about the job, the person, or neither?"]),
    stmt("6.3", "Explain the selection procedure.", 8,
         ["Determine fair assessment criteria on which selection will be based.", "Sort the received CVs according to the selection criteria.",
          "Check references to verify the content of CVs.", "Compile a shortlist of potential candidates.",
          "Invite shortlisted candidates for an interview.", Q6_EX[0]],
         ["Appoint the first applicant without checking documents.", "Destroy the CVs before screening."],
         ["From applications to an offer.", "Screen, check, shortlist, interview."], 2),
    stmt("6.4", "Discuss the role of the interviewer during the interview.", 8,
         ["Introduce the members of the panel to the interviewee.", "Make the interviewee feel at ease.",
          "Avoid discriminatory questions, such as asking about family planning.", "Give the interviewee an opportunity to ask questions.",
          Q6_EX[1]],
         ["Ask the interviewee personal questions about her children.", "Mislead the interviewee about the job.",
          "End the interview without thanking the candidate."], ["The interviewer runs the interview fairly.", "Welcome, record, close."],
         2),
    stmt("6.5", "Advise businesses on the legal requirements of an employment contract.", 6,
         ["It may not contain requirements that conflict with the BCEA.", "Both the employer and the employee must sign it.",
          "Neither party may change it on their own.", "The remuneration package, including benefits, must be clearly stated."],
         ["The employer may change it whenever he wants.", "Only the employee signs it.", "It may pay less than the BCEA allows."],
         ["A contract binds both parties.", "The BCEA sets the minimum."], 2),
    stmt("6.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["Appointing the right person can help the business reach its objectives and be profitable.",
          "The employer is not allowed to offer the employee less than what the BCEA stipulates."],
         ["Selection procedures waste time, as anyone can do any job.", "Employment contracts are optional for big businesses.",
          "Interviews should be skipped to save money."], ["A conclusion sums up why it all matters.", "Which card would a business "
                                                                                                      "agree with?"], 2),
], [("6.3", Q6_EX[0]), ("6.4", Q6_EX[1])], INSIGHT_CLUES)

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 10,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Complete the statements", "marks": 10,
     "lead": "Complete the following statements by using the word(s) provided in the list below.\n" + WORDS, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column A and Column B", "marks": 10,
     "lead": "Choose a description from COLUMN B that matches a term in COLUMN A.", "items": q13},
    {"id": "2.1", "title": "Question 2", "kind": "Business environments", "marks": 28,
     "lead": "QUESTION 2: BUSINESS ENVIRONMENTS\n2.3 HAPPY STICKS (HS)\n" + HS + "\n2.5 GOOD SUPERMARKET (GS)\n" + GS, "items": q2},
    {"id": "2.6", "title": "Question 2.6 – 2.7", "kind": "Business environments", "marks": 12, "lead": "Lobbying and the environment.",
     "items": q26},
    {"id": "3.1", "title": "Question 3", "kind": "Business operations", "marks": 40,
     "lead": "QUESTION 3: BUSINESS OPERATIONS\n3.3 AMAZING SNACKS (AS)\n" + AS + "\n3.6 TASKER'S FASHION (TF)\nTasker's Fashion is a clothing "
             "store in Makhanda. They placed an advert on the business's notice board for a new secretary. TF also advertised the vacancy "
             "in the local newspaper. TF calculates the salaries of employees by using different salary determination methods.",
     "items": q3},
    {"id": "4.1", "title": "Question 4", "kind": "Miscellaneous topics", "marks": 40,
     "lead": "QUESTION 4: MISCELLANEOUS TOPICS\n4.3 WINNING WAYS (WW)\nWinning Ways is a consulting business that helps businesses to overcome "
             "challenges in the business environments. WW helps businesses to work together to build on the expertise of one another. "
             "Winning Ways also assists businesses in identifying Corporate Social Responsibility projects to be involved in.", "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Essay: socio-economic issues", "marks": 40,
     "lead": "Build the essay section by section, then see your insight.", "extract": "QUESTION 5: THE ESSAY\n\n" + Q5_STEM, "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Essay: human resources", "marks": 40,
     "lead": "Build the essay section by section, then see your insight.", "extract": "QUESTION 6: THE ESSAY\n\n" + Q6_STEM, "items": q6},
]
P.finish(missions,
         {"subject": "Business Studies", "title": "Business Studies P1", "sitting": "November 2024", "total_marks": 150, "time": "2 hours"},
         [P.flag_answers(),
          {"n": "2.3.1", "kind": "no_fit", "detail": "Quote items (2.3.1, 3.3.1) are played by picking the scenario's sentences, as Grade 12."},
          {"n": "5.7", "kind": "no_fit", "detail": "Each essay plays as sections, one per memo heading, their facts scaled to sum to the memo's "
                                                   "cap of 32 (Question 5: 2 + 6 + 8 + 8 + 6 + 2 of the memo's 2 + 10 + 12 + 12 + 12 + 2; "
                                                   "Question 6: 2 + 6 + 8 + 8 + 6 + 2 of 2 + 8 + 12 + 14 + 12 + 2), then insight (8)."},
          {"n": "3.6.1", "kind": "no_fit", "detail": "A method and its quote are one card (3 marks: the memo's 2 + 1)."}],
         {"1": 30, "2": 40, "3": 40, "4": 40, "5": 40, "6": 40}, 150, {}, "Sections A, B and C (the whole paper)",
         sections=[("Section A", 30, None, ["1"]), ("Section B", 80, 2, ["2", "3", "4"]), ("Section C", 40, 1, ["5", "6"])])
