"""Grade 11 Business Studies P1 November 2025 (Eastern Cape Department of Education), the whole paper (Sections A, B and C, 150 marks,
2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options, marks and memo points are
the paper's and the memo's own; clues are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2025 November Grade 11, the question
paper zip (English PDF 'BSTD P1 ... ENG', 10 pages, text layer) and the marking-guideline zip (English, 29 pages).

  python tools/ingest/transcribe_g11_bs_p1_2025_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-bs-p1-2025-11-ec/BSTD P1 GRADE 11 Nov 2025 ENG_watermark.pdf" "uploads/provincial/g11-bs-p1-2025-11-ec/BUSINESS STUDIES GRADE 11 NOV 2025 MARKING GUIDELINE_watermark.pdf" --id g11-bs-p1-2025-11-ec --from-json

The Business Studies rulings, as in transcribe_g11_bs_p1_2024_11_ec.py."""
from provincial import Paper, sentences

P = Paper("g11-bs-p1-2025-11-ec", 595.32, 842.04, {}, start=11)
answer, stmt, mcq, term, sort, essay = P.answer, P.stmt, P.mcq, P.term, P.sort, P.essay
pick = lambda n, q, opts, pool, clues: {"t": "pickn", "n": n, "marks": len(pool), "q": q, "clues": clues, "opts": opts, "pool": pool,
                                        "count": len(pool)}
INSIGHT_CLUES = ["Insight is earned from how you answered the sections.", "Right first time, every heading answered, and the examples picked."]

# ---- SECTION A, QUESTION 1, the question paper pages 3-5 and the memo page 8 ----
q11 = [
    mcq("1.1.1", "A component of the macro environment is:", ["Competitors", "Unions", "Legal environment", "Vision and mission"], 2,
        ["The macro environment is outside the business's control.", "Competitors and unions are in the market environment."]),
    mcq("1.1.2", "This Act makes provision for the establishment of the CCMA and bargaining councils.",
        ["Labour Relations Act (LRA), 1995 (Act 66 of 1995)", "Employment Equity Act (EEA), 1998 (Act 55 of 1998)",
         "Compensation for Occupational Injuries and Disease Act (COIDA), 1997 (Act 61 of 1997)",
         "Consumer Protection Act (CPA), 2008 (Act 68 of 2008)"], 0, ["Disputes and bargaining.", "Labour relations."]),
    mcq("1.1.3", "Telecom combines with Vuka mobile to become one business. This is known as a/an …", ["takeover.", "merger.", "acquisition.",
                                                                                                     "alliance."], 1,
        ["Both combine by agreement.", "Into one business."]),
    mcq("1.1.4", "Packaging where the container can be used for something else once the content is finished is called …",
        ["unit packaging.", "packaging for resale.", "speciality packaging.", "packaging for double use."], 3,
        ["Used again.", "Two uses."]),
    mcq("1.1.5", "Tau (Pty) Ltd is required by law to contribute to the … fund as a compulsory employee benefit.",
        ["unemployment insurance", "medical aid", "provident", "pension"], 0, ["Required by law.", "UIF."])]
WORDS = "limited; time-related; control; economic; piecemeal; internal; assurance; no; external; industrial"
q12 = [
    term("1.2.1", "King Traders has … control over the social environment.", ["no"], ["The social environment is part of the macro "
                                                                                     "environment.", "How much control?"], marks=2),
    term("1.2.2", "Money laundering is a/an … crime.", ["economic"], ["A crime involving money.", "Not industrial."], marks=2),
    term("1.2.3", "Phila and Philane used the … recruitment method when they advertised a vacancy on their business noticeboard.",
         ["internal"], ["A noticeboard is seen by current staff.", "Inside."], marks=2),
    term("1.2.4", "Samuel gets paid for the hours spent at work. It is known as the … salary determination method.", ["time-related",
                                                                                                                    "time related"],
         ["Paid for hours.", "Not piecemeal."], marks=2),
    term("1.2.5", "Inspecting the products during and after production to ensure that it meet the required standards is called quality …",
         ["assurance"], ["During AND after.", "Quality control is only after."], marks=2)]
DESC = ["prices are attached to a new innovative, unique product", "an organisation which helps to promote the business's products",
        "action taken by employers to keep employees from entering the workplace", "imported goods sold at a higher-than-normal price",
        "employees' qualifications and skills are matched with the requirements of the job",
        "action taken by employees in an attempt to have their demands met", "imported goods sold at a lower-than-normal price",
        "an organisation with official power to control an activity",
        "employees are familiarised with the physical work environment and organisational structure",
        "prices use the customers' emotional response to encourage sales"]
q13 = [
    {"t": "match", "n": "1.3", "marks": 10, "q": "Choose a description from COLUMN B that matches a term in COLUMN A (1.3.1 Lockout, 1.3.2 "
     "Dumping, 1.3.3 Regulator, 1.3.4 Placement, 1.3.5 Price skimming).",
     "clues": ["A lockout is the employer's action; dumping is selling cheap imports.", "Skimming prices a new, unique product high."],
     "left": ["1.3.1 Lockout", "1.3.2 Dumping", "1.3.3 Regulator", "1.3.4 Placement", "1.3.5 Price skimming"], "right": DESC,
     "a": [2, 6, 7, 4, 0], "each": 2, "heads": ["COLUMN A", "COLUMN B (A–J)"]}]

# ---- SECTION B, QUESTION 2: BUSINESS ENVIRONMENTS, the question paper pages 6-7 and the memo pages 9-13 ----
SE = ["Illiteracy", "Demographic issues", "Piracy", "Inclusivity"]
q2 = [
    stmt("2.1", "Name THREE types of power relationships.", 3, ["Strategic alliance agreements", "Persuasion of large investors",
                                                                "Company representatives' influence"],
         ["Hostile price wars", "Dumping", "Retrenchments"], ["How a business gains influence.", "Alliances, investors, representatives."], 1),
    stmt("2.2", "Outline the negative impact of strikes on businesses.", 6,
         ["Strikes can jeopardise relations between management and employees.", "Businesses suffer financial losses from low productivity.",
          "Strikes may lead to production losses and a decline in sales.", "Business property may be looted or destroyed.",
          "The business's image and reputation might be damaged."],
         ["Strikes always increase production.", "Strikes improve relations between employers and employees.",
          "Customers become more loyal during strikes."], ["What does a strike cost?", "Relations, money, image."], 2),
    answer("2.3.1", "Games More (GM) duplicate computer games without permission from the creators and sell it to the public. Identify the "
           "socio-economic issue in the scenario.", 2, [SE[2], SE[0], SE[1], SE[3]], ["Copying without permission.", "Pirated games."]),
    stmt("2.3.2", "Advise businesses on ONE solution to the socio-economic issue identified in QUESTION 2.3.1.", 4,
         ["Patent: a registered patent stops others from producing and selling the same product.",
          "Trademarks: a registered trademark identifies the business, and its owner can claim damages from infringers.",
          "Copyright: businesses can sue anyone who infringes their copyright."],
         ["Lower prices until the pirates stop.", "Give the software away free.", "Stop creating new games."],
         ["Protect intellectual property by law.", "Each card gives a solution and how it works."], 4),
    stmt("2.4", "Discuss political change as a challenge of the macro environment.", 4,
         ["A change in government laws forces businesses to adapt to new laws and policies.",
          "A change in government can cause political instability, which scares away investors and tourists.",
          "In some countries political instability makes it very difficult to operate profitably."],
         ["Political change never affects businesses.", "Businesses control the government's laws."],
         ["New government, new laws.", "Instability and investors."], 2),
    answer("2.5.1", "Identify the socio-economic issue applicable to Zonke Enterprise: Some employees of Zonke Enterprise cannot read and write.",
           2, [SE[0], SE[1], SE[2], SE[3]], ["Cannot read or write.", "Literacy."]),
    answer("2.5.2", "Identify the socio-economic issue applicable to Zonke Enterprise: Zonke Enterprise employ people from different races, "
           "ages and genders.", 2, [SE[1], SE[0], SE[2], SE[3]], ["Race, age and gender.", "The make-up of a population."]),
    stmt("2.6", "Explain the link between the primary, secondary and tertiary sectors.", 6,
         ["The three sectors work together to create an economic chain of production.",
          "The primary sector extracts raw materials, which the secondary sector processes into products.",
          "The secondary sector needs the tertiary sector to sell its goods and for services such as banks and transport.",
          "The primary sector depends on the secondary sector for machinery and equipment."],
         ["The sectors never depend on one another.", "The tertiary sector extracts raw materials from nature."],
         ["Raw materials, manufacturing, services.", "Each needs the others."], 2),
    stmt("2.7.1", "Purr-fect Foods produces various kinds of pet food. The production manager does not have the necessary skills to lead his "
         "department. Some clients prefer to buy cheaper brands because of low-income levels. Identify the challenge from the "
         "micro-environment applicable to PF. Motivate your answer by quoting from the scenario.", 3,
         ["Lack of adequate management skills: 'The production manager does not have the necessary skills to lead his department.'"],
         ["Lack of adequate management skills: 'Some clients prefer to buy cheaper brands because of low-income levels.'",
          "Competition: 'The production manager does not have the necessary skills to lead his department.'",
          "Low income levels: 'Some clients prefer to buy cheaper brands.'", "Inflation: 'Purr-fect Foods produces various kinds of pet "
                                                                             "food.'"],
         ["The micro environment is inside the business.", "Management."], 3),
    stmt("2.7.2", "Explain ways in which business can have a direct influence on the environment.", 4,
         ["Get involved in research and development so that they can continue to operate.",
          "Influence suppliers by signing long-term contracts at fixed prices.", "Influence customers by creating new uses for a product.",
          "Influence regulators through lobbying and bargaining."],
         ["Wait for the environment to change on its own.", "Refuse to deal with suppliers and customers."],
         ["Suppliers, customers, regulators.", "Act on them."], 2),
    stmt("2.8", "Suggest ways in which businesses can overcome competition in the market.", 4,
         ["Produce unique (differentiated) goods or services for the target market.", "Price goods lower than competitors' goods.",
          "Improve customer service and ensure client satisfaction.", "Run good marketing campaigns, such as on social media."],
         ["Copy the competitor's brand name exactly.", "Stop advertising to save money."], ["Price, quality, service, marketing.",
                                                                                           "How to win customers."], 2)]

# ---- QUESTION 3: BUSINESS OPERATIONS, the question paper page 7 and the memo pages 14-18 ----
SE7 = ("Softy's Electronics is looking for an experienced supervisor to fill a vacant position. They conducted preliminary interviews as there "
       "were many applicants. SE gave a written offer for the job to the successful candidate.")
CG = ["Convenience goods", "Speciality goods", "Shopping goods", "Unsought goods"]
q3 = [
    stmt("3.1", "Name FOUR requirements for a safe work environment.", 4,
         ["Safety policy", "Visible warning signs", "First aid kit", "Precautionary measures when handling machinery"],
         ["Locked fire exits", "Untrained machine operators", "Wet floors without warning"], ["What keeps workers safe?",
                                                                                              "Policy, signs, first aid."], 1),
    stmt("3.2", "Outline the advantages of production planning.", 4,
         ["Every machine and worker is used to full capacity.", "The business has the correct amount of supplies and stock.",
          "It prevents time from being wasted and increases output.", "Improved inventory control reduces wastage and storage costs."],
         ["It leaves machines idle.", "It increases storage costs."], ["Use resources well.", "Time, stock, output."], 2),
    answer("3.3.1", "Identify the type of consumer goods sold by Gerrie Stores: GS sells low-cost goods which customers will purchase without "
           "much thought.", 2, [CG[0], CG[1], CG[2], CG[3]], ["Little thought.", "Bought often and quickly."]),
    answer("3.3.2", "Identify the type of consumer goods sold by Gerrie Stores: GS sells specific brand name clothing and customers require time "
           "and effort to purchase.", 2, [CG[1], CG[0], CG[2], CG[3]], ["A specific brand.", "Customers go out of their way."]),
    stmt("3.4", "Explain the reasons why manufacturers may prefer to make use of indirect distribution methods.", 4,
         ["Experienced intermediaries deal with customers, so the business can focus on core issues.", "Intermediaries take care of transport "
                                                                                                       "and storage.",
          "Better market coverage is achieved through intermediaries.", "Businesses enjoy the benefit of bulk orders from wholesalers."],
         ["The manufacturer must deliver to every consumer itself.", "Intermediaries increase the manufacturer's control."],
         ["Using middlemen.", "Coverage, storage, transport."], 2),
    stmt("3.5", "Discuss the requirements of a good trademark.", 4,
         ["Trademarks must be attractive and promote the product.", "Easy to recognise, remember and pronounce.", "Must be different from "
                                                                                                                  "its competitors'.",
          "A good trademark can be registered under the Trade Marks Act."],
         ["It should copy a competitor's trademark.", "It should be changed every month."], ["Recognisable and unique.", "Registered."], 2),
    stmt("3.6", "Advise businesses on the purpose of sales promotion.", 4,
         ["Increase the sales of the business's products.", "Inform existing and potential customers about products.",
          "Persuade potential customers to buy immediately.", "Improve customer loyalty."],
         ["Reduce the number of customers.", "Hide new products from the market."], ["Promotions sell more.", "Inform, persuade, keep."],
         2),
    pick("3.7.1", "Quote TWO steps of the selection procedure from the scenario.", sentences(SE7), [1, 2],
         ["Selection: screening, interviews, the offer …", "Which sentences describe them?"]),
    stmt("3.7.2", "Explain other steps in the selection procedure.", 6,
         ["Determine fair assessment criteria on which selection will be based.", "Sort the received CVs according to the selection criteria.",
          "Check references to verify the content of CVs.", "Compile a shortlist of potential candidates.",
          "Invite shortlisted candidates for an interview."],
         ["Appoint the first applicant without checking documents.", "Destroy the CVs before screening."],
         ["Other than preliminary interviews and the offer.", "Screen, check, shortlist."], 2),
    sort("3.8", "Discuss the difference between job description and job specification.", ["Job description", "Job specification"],
         [("Describes the duties and responsibilities of a specific job", 0), ("A written description of the job and its requirements", 0),
          ("Describes the minimum personal qualities, skills and qualifications needed", 1), ("Describes the requirements for the person, "
                                                                                              "e.g. qualifications", 1)],
         ["The job, or the person for the job?", "Sort each card."]),
    stmt("3.9", "Advise businesses on the purpose of induction.", 4,
         ["Introduce new employees to management and colleagues.", "Explain safety regulations and rules.",
          "Give new employees a tour of the building.", "Familiarise new employees with the organisational structure."],
         ["Decide whether to employ the applicant.", "Advertise the vacancy."], ["After appointment.", "Welcome and inform."], 2)]

# ---- QUESTION 4: MISCELLANEOUS TOPICS, the question paper pages 8-9 and the memo pages 19-22 ----
BS = ("Bongi Sneakers manufactures a variety of casual and training shoes. BS lost customers to Tekkie Trainers, which opened two weeks ago. "
      "The profitability of BS decreased due to a shortage of skilled employees.")
q4 = [
    stmt("4.1", "State any TWO types of lobbying.", 2,
         ["Hedging against inflation", "Bargaining sessions between management and unions", "Influencing supervisory bodies (regulators)"],
         ["Price skimming", "Dumping", "Recruitment"], ["Lobbying influences decision-makers.", "Inflation, bargaining, regulators."], 1),
    pick("4.2.1", "Quote TWO challenges from the scenario above.", sentences(BS), [1, 2], ["Challenges are problems.", "Customers lost, "
                                                                                                                       "skills short."]),
    {"t": "match", "n": "4.2.2", "marks": 2, "q": "Classify BS's challenges according to the business environments.",
     "clues": ["Competitors are in the market environment.", "Employees and skills are inside the business."],
     "left": ["BS lost customers to Tekkie Trainers, which opened two weeks ago.", "The profitability of BS decreased due to a shortage of "
                                                                                   "skilled employees."],
     "right": ["Micro environment", "Market environment", "Macro environment"], "a": [1, 0], "heads": ["CHALLENGE", "BUSINESS ENVIRONMENT"],
     "after": ["4.2.1"]},
    stmt("4.3", "Explain the advantages of networking for the business.", 4,
         ["Businesses can attract new customers, increasing market share and profitability.", "Networking is a source of new perspectives "
                                                                                              "and business ideas.",
          "Managers build new business relationships and opportunities.", "It assists businesses in making future decisions."],
         ["Networking means the business never has to advertise.", "Networking guarantees a profit."],
         ["Relationships with other businesses.", "Customers and ideas."], 2),
    stmt("4.4", "Discuss the functions of trade unions.", 6,
         ["Trade unions represent and protect their members against unfair labour practices.",
          "They empower employees about their rights in the workplace.", "They represent employees in grievances and disputes.",
          "They negotiate for better working conditions, wages and benefits.", "They may take legal action on behalf of their members."],
         ["They set the business's prices.", "They hire and fire for management.", "They collect income tax for SARS."],
         ["Unions act for workers.", "Protect, represent, negotiate."], 2),
    stmt("4.5", "Advise businesses on the purpose of the Labour Relations Act.", 4,
         ["It promotes the resolution of labour disputes through the CCMA.", "It regulates the rights of trade unions and facilitates "
                                                                             "collective bargaining.",
          "It promotes fair labour practices.", "It allows workplace forums where employees take part in decision-making."],
         ["It sets the prices of consumer goods.", "It forbids trade unions."], ["Labour relations.", "Disputes, unions, fairness."], 2),
    stmt("4.6", "Name TWO marketing activities.", 2, ["Standardisation and grading", "Storage", "Transport", "Financing", "Risk-bearing",
                                                      "Buying and selling"],
         ["Recruitment", "Payroll"], ["Activities that move goods to the market.", "Store, transport, sell."], 1),
    stmt("4.7", "Outline the importance of product development.", 4,
         ["Products are designed to suit the needs of customers.", "New products replace older products when sales decline.",
          "Businesses remain competitive by improving their products.", "Products become different from competitors' products."],
         ["Customers' needs never change.", "Old products sell more as they age."], ["Products have a life cycle.", "Stay competitive."], 2),
    stmt("4.8.1", "Tasco's Fresh Market sells fresh fruit and vegetables. The demand for the product, the mark-up they want to achieve and the "
         "input cost influence their prices. Name TWO factors that will influence TF's pricing in the scenario.", 2,
         ["Demand for the product", "Input cost"], ["The weather", "The number of employees", "The colour of the packaging"],
         ["Read the scenario.", "What influences their prices?"], 1),
    stmt("4.8.2", "Explain the importance of pricing.", 4,
         ["Pricing affects the number of products sold, which affects profitability.", "The price influences consumers' attitude towards "
                                                                                       "the brand.",
          "If the price is too high, fewer consumers may buy.", "If the price is too low, consumers may think the quality is poor."],
         ["Price has no effect on sales.", "A low price always shows high quality."], ["Price, sales and profit.", "Customers' view."], 2),
    stmt("4.9", "Discuss the role of the interviewer during the interview.", 4,
         ["Introduce the members of the panel to the interviewee.", "Make the interviewee feel at ease.",
          "Avoid discriminatory questions, such as about family planning.", "Give the interviewee an opportunity to ask questions."],
         ["Ask about the candidate's plans to have children.", "Mislead the interviewee about the job."],
         ["Run a fair interview.", "Welcome, record, close."], 2),
    stmt("4.10", "Advise businesses on the legal requirements of an employment contract.", 4,
         ["It may not conflict with the BCEA.", "Both the employer and the employee must sign it.", "Neither party may change it on their own.",
          "The remuneration package must be clearly stated."],
         ["The employer may change it at will.", "Only the employee signs it."], ["Binds both parties.", "The BCEA is the minimum."], 2)]

# ---- SECTION C, the essays (answer any ONE), the question paper page 10 and the memo pages 23-29 ----
Q5_STEM = ("Businesses must get involved in social responsibility projects that are positively benefiting communities. These projects can "
           "have a positive impact for businesses. Business must be aware of the challenges in different business environments and how they "
           "have to adapt to these challenges in order to be sustainable. Lobbying can help to overcome challenges.\n\nWrite an essay on "
           "adapting to business challenges in which you include the following aspects:\n• Outline the projects that can be taken by "
           "businesses as part of social responsibility.\n• Explain the benefits of social responsibility projects for businesses.\n• Discuss "
           "the following ways in which businesses can adapt to challenges of the business environments: Information management; Strategic "
           "responses.\n• Advise businesses on the reasons why businesses lobby.")
Q5_EX = ["For example, a supermarket chain donates old computers to a rural school's computer lab.",
         "For example, a bank's customers stay loyal because it funds bursaries in their community."]
q5 = essay("5.8", [
    stmt("5.1", "Introduction: pick the TWO statements that introduce this essay on adapting to business challenges.", 2,
         ["Social responsibility is a business's obligation to protect its environment and improve the quality of life of its community.",
          "Businesses must adapt to challenges to stay ahead of competitors.",
          "Businesses lobby to have a voice in matters that affect their operations."],
         ["Social responsibility means maximising profit at any cost.", "Lobbying is illegal in South Africa.",
          "Businesses never face challenges."], ["An introduction says what the essay is about.", "Which cards are true?"], 1),
    stmt("5.2", "Outline the projects that can be taken by businesses as part of social responsibility.", 8,
         ["Allow employees to get involved in social development programmes.", "Engage in environmentally friendly campaigns, such as "
                                                                              "recycling.",
          "Support less fortunate people by donating to charities.", "Sponsor art and cultural programmes, such as school choirs.", Q5_EX[0]],
         ["Pay workers less to fund the owner's holidays.", "Dump waste in the community to save costs."],
         ["Give back to the community.", "Education, environment, charity."], 2),
    stmt("5.3", "Explain the benefits of social responsibility projects for businesses.", 8,
         ["It increases employees' morale and job satisfaction.", "It can be used as a marketing strategy.",
          "It promotes customer loyalty, resulting in more sales.", "It improves the business's image.", Q5_EX[1]],
         ["It always reduces the business's sales.", "It damages the business's reputation."], ["What does the business gain?",
                                                                                                "Image, loyalty, morale."], 2),
    stmt("5.4", "Discuss information management as a way in which businesses can adapt to challenges of the business environments.", 4,
         ["Information must be recorded, stored, easily retrieved and used effectively.", "Implement an information management system that "
                                                                                          "is accessible to all staff.",
          "Invest capital in IT systems to update business operations."],
         ["Keep information away from staff.", "Store records only on paper in one office."], ["Information helps decisions.",
                                                                                              "Systems and technology."], 2),
    stmt("5.5", "Discuss strategic responses as a way in which businesses can adapt to challenges of the business environments.", 4,
         ["Management designs strategic responses by analysing all information and the stakeholders involved.",
          "Get a clear picture of each stakeholder's viewpoints and requirements.", "Have a strategic plan to respond to changes in the "
                                                                                    "environment."],
         ["Ignore stakeholders' views.", "Respond to every change without a plan."], ["Plan the response.", "Information and stakeholders."],
         2),
    stmt("5.6", "Advise businesses on the reasons why businesses lobby.", 4,
         ["To change laws, such as child labour laws and municipal regulations.", "Lobby groups' views give solutions to business challenges.",
          "To influence the prices, policies and regulations of their regulator."],
         ["To avoid paying their suppliers.", "To keep the public uninformed."], ["Influence decision-makers.", "Laws and regulators."], 2),
    stmt("5.7", "Conclusion: pick the statement that concludes this essay.", 2,
         ["The public image of the business can improve when it takes part in social responsibility projects.",
          "Lobbying can assist businesses to have a say in matters that influence their sustainability."],
         ["Businesses gain nothing from helping communities.", "Businesses should never adapt to change.", "Lobbying always harms businesses."],
         ["A conclusion sums up why it all matters.", "Which card would a business agree with?"], 2),
], [("5.2", Q5_EX[0]), ("5.3", Q5_EX[1])], INSIGHT_CLUES)
Q6_STEM = ("Businesses must be well informed of the purpose of the Occupational Health and Safety Act. For businesses to be successful, they "
           "must ensure that the production planning is done effectively. Total Quality Management (TQM) plays an important role in the "
           "success of the business. When handling machinery it is important to take the necessary precautions.\n\nWrite an essay on "
           "production in which you include the following aspects:\n• Outline the purpose of the Occupational Health and Safety Act.\n• "
           "Explain the following aspects that must be considered during production planning: Loading; Scheduling.\n• Discuss Total Quality "
           "Management (TQM) as part of the quality management system.\n• Recommend precautionary measures that businesses should take when "
           "handling machinery.")
Q6_EX = ["For example, a car factory gives welders goggles and gloves and services its welding machines every month.",
         "For example, a furniture factory plans the start and finish time of each step so that orders leave on time."]
q6 = essay("6.8", [
    stmt("6.1", "Introduction: pick the TWO statements that introduce this essay on production.", 2,
         ["The OHSA was implemented to protect the health and safety of employees.",
          "TQM helps to design, produce and provide quality products and services to customers.",
          "Any machinery can cause serious injuries, so precautionary measures must be in place."],
         ["Production planning is only needed for small businesses.", "TQM is the responsibility of one employee.",
          "The OHSA protects only customers."], ["An introduction says what the essay is about.", "Which cards are true?"], 1),
    stmt("6.2", "Outline the purpose of the Occupational Health and Safety Act.", 8,
         ["Protects the health, safety and welfare of employees.", "Outlines the roles and responsibilities of employers and employees.",
          "Requires every business to maintain a safe work environment.", "Requires that the main dangers in the workplace be identified and "
                                                                          "eliminated.",
          "Clarifies the duties of the health and safety representative and committee."],
         ["Sets the minimum wage.", "Regulates trade union elections.", "Protects consumers against unfair prices."],
         ["Health and safety at work.", "Who is responsible for what?"], 2),
    stmt("6.3", "Explain loading as an aspect that must be considered during production planning.", 4,
         ["Loading plans who will be responsible for each activity.", "It allocates every person and machine to their task.",
          "It calculates how long each machine will operate during a day."],
         ["Loading decides the selling price.", "Loading is the transport of finished goods."], ["Who and what does each job?",
                                                                                                "People and machines."], 2),
    stmt("6.4", "Explain scheduling as an aspect that must be considered during production planning.", 4,
         ["Scheduling involves the timing of the production process.", "It determines which jobs must be completed before the next one.",
          "It calculates the time required for each activity.", Q6_EX[1]],
         ["Scheduling chooses the suppliers.", "Scheduling ignores the availability of staff."], ["When is each job done?", "Timing."], 2),
    stmt("6.5", "Discuss Total Quality Management (TQM) as part of the quality management system.", 6,
         ["It is a management philosophy that integrates all organisational functions.", "It improves quality to satisfy customers' needs.",
          "It is the responsibility of everyone in the organisation.", "Businesses strive to get it right the first time."],
         ["Only the quality controller is responsible for quality.", "TQM checks quality once a year."], ["Total: everyone.",
                                                                                                          "Quality all the time."], 2),
    stmt("6.6", "Recommend precautionary measures that businesses should take when handling machinery.", 6,
         ["Familiarise employees with safety procedures.", "Install machinery correctly and make sure it is safe.",
          "Train workers properly to use the machinery.", "Carry out regular safety checks and services.", Q6_EX[0]],
         ["Remove safety guards to speed up production.", "Let untrained workers learn by trial and error."], ["Train, maintain, protect.",
                                                                                                                "Prevent accidents."], 2),
    stmt("6.7", "Conclusion: pick the statement that concludes this essay.", 2,
         ["Complying with the OHSA protects businesses from huge legal claims.",
          "TQM enables businesses to continuously improve the delivery of products and services."],
         ["Safety measures waste production time.", "Production planning is unnecessary.", "Quality does not affect customers."],
         ["A conclusion sums up why it all matters.", "Which card would a business agree with?"], 2),
], [("6.6", Q6_EX[0]), ("6.4", Q6_EX[1])], INSIGHT_CLUES)

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 10,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Complete the statements", "marks": 10,
     "lead": "Complete the following statements by using the words provided in the list below.\n" + WORDS, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column A and Column B", "marks": 10,
     "lead": "Choose a description from COLUMN B that matches a term in COLUMN A.", "items": q13},
    {"id": "2", "title": "Question 2", "kind": "Business environments", "marks": 40, "lead": "QUESTION 2: BUSINESS ENVIRONMENTS", "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Business operations", "marks": 40,
     "lead": "QUESTION 3: BUSINESS OPERATIONS\n3.7 SOFTY'S ELECTRONICS (SE)\n" + SE7, "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Miscellaneous topics", "marks": 40,
     "lead": "QUESTION 4: MISCELLANEOUS TOPICS\n4.2 BONGI SNEAKERS (BS)\n" + BS, "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Essay: adapting to challenges", "marks": 40,
     "lead": "Build the essay section by section, then see your insight.", "extract": "QUESTION 5: THE ESSAY\n\n" + Q5_STEM, "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Essay: the production function", "marks": 40,
     "lead": "Build the essay section by section, then see your insight.", "extract": "QUESTION 6: THE ESSAY\n\n" + Q6_STEM, "items": q6},
]
P.finish(missions,
         {"subject": "Business Studies", "title": "Business Studies P1", "sitting": "November 2025", "total_marks": 150, "time": "2 hours"},
         [P.flag_answers(),
          {"n": "4.4", "kind": "memo_issue", "detail": "The memo writes 'Max. (4)' under 4.4; the paper and the memo's own breakdown give 6, and "
                                                       "Question 4 adds to 40 only with 6: the part plays 6."},
          {"n": "3.7.1", "kind": "no_fit", "detail": "Quote items (3.7.1, 4.2.1) are played by picking the scenario's sentences, as Grade 12; "
                                                     "4.2.2 classifies the two challenges by a match."},
          {"n": "5.8", "kind": "no_fit", "detail": "Each essay plays as sections, one per memo heading, their facts scaled to the memo's cap of 32 "
                                                   "(Question 5: 2 + 8 + 8 + 4 + 4 + 4 + 2; Question 6: 2 + 8 + 4 + 4 + 6 + 6 + 2), then insight "
                                                   "(8)."}],
         {"1": 30, "2": 40, "3": 40, "4": 40, "5": 40, "6": 40}, 150, {"4.2.2": ["4.2.1"]}, "Sections A, B and C (the whole paper)",
         sections=[("Section A", 30, None, ["1"]), ("Section B", 80, 2, ["2", "3", "4"]), ("Section C", 40, 1, ["5", "6"])])
