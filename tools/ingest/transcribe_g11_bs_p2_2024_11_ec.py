"""Grade 11 Business Studies P2 November 2024 (Eastern Cape Department of Education), the whole paper (Sections A, B and C, 150 marks,
2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options, marks and memo points are
the paper's and the memo's own; clues are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2024_November_Gr_11_Exams, the question
paper zip (English PDF, 8 pages, text layer) and the memo zip (English, 29 pages).

  python tools/ingest/transcribe_g11_bs_p2_2024_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-bs-p2-2024-11-ec/BUSINESS STUDIES gr 11 P2 QP ENG D_watermark.pdf" "uploads/provincial/g11-bs-p2-2024-11-ec/BUSINESS STUDIES GR 11 P2 MG_ENG_watermark.pdf" --id g11-bs-p2-2024-11-ec --from-json

The Business Studies rulings, as in transcribe_g11_bs_p1_2024_11_ec.py: written parts as statements (a card worth what the memo ticks
for one point), a quote as picking the scenario's sentences, a difference as a sort, each essay as sections scaled to the memo's 32
plus insight; Section B answers any TWO, Section C any ONE."""
from provincial import Paper, sentences

P = Paper("g11-bs-p2-2024-11-ec", 595.22, 842.0, {}, start=10)
answer, stmt, mcq, term, sort, essay = P.answer, P.stmt, P.mcq, P.term, P.sort, P.essay
pick = lambda n, q, opts, pool, clues: {"t": "pickn", "n": n, "marks": len(pool), "q": q, "clues": clues, "opts": opts, "pool": pool,
                                        "count": len(pool)}
INSIGHT_CLUES = ["Insight is earned from how you answered the sections.", "Right first time, every heading answered, and the examples picked."]

# ---- SECTION A, QUESTION 1, the question paper pages 3-4 and the memo page 7 ----
q11 = [
    mcq("1.1.1", "A company in which the directors are jointly and separately liable for all the debts and liabilities of the business:",
        ["Private company", "Public company", "State-owned company", "Personal liability company"], 3,
        ["The directors are personally liable.", "The name says it."]),
    mcq("1.1.2", "Vusi sold the right to use the name and trademark of VS Foods to Tony in return for a royalty fee. Vusi is known as the …",
        ["franchisor.", "franchisee.", "lessor.", "lessee."], 0, ["Vusi owns the name.", "-or is the one who gives."]),
    mcq("1.1.3", "A business hiring temporary employees or using independent contractors considers … as a factor that must be considered "
        "before start-up.", ["the culture of the organisation", "business growth", "cost saving", "customer service"], 2,
        ["Temporary staff are cheaper.", "Why not hire permanently?"]),
    mcq("1.1.4", "Zonke Construction uses … when alternative solutions are generated and evaluated in response to problems.",
        ["problem-solving", "force-field analysis", "Delphi technique", "routine thinking"], 0,
        ["Generating and evaluating solutions.", "The general process, not one technique."]),
    mcq("1.1.5", "The way the body reacts to situations that a person finds difficult to control, is known as …", ["crisis.", "stress.",
                                                                                                                   "change.", "conflict."], 1,
        ["A reaction of the body.", "Not a disagreement."])]
WORDS = "norming; passion; grievance; performing; partnership; hand-outs; conflict; close corporation; posters; perseverance"
q12 = [
    term("1.2.1", "A … has no legal entity and therefore has no continuity.", ["partnership"], ["Two or more owners, no legal personality.",
                                                                                            "Not a close corporation."], marks=2),
    term("1.2.2", "Dlamini showed … as an entrepreneurial quality when she did not give up despite the challenges she faced in her business.",
         ["perseverance"], ["Not giving up.", "Persevere."], marks=2),
    term("1.2.3", "Nico provided ... as a type of visual aid to the audience after his presentation to remind them of the key points.",
         ["hand-outs", "handouts"], ["Given to the audience to keep.", "Paper."], marks=2),
    term("1.2.4", "A disagreement between two parties is known as …", ["conflict"], ["Not a grievance: that is a complaint.", "A clash."],
         marks=2),
    term("1.2.5", "During the ... stage of team development, team members come to an agreement and reach a consensus.", ["norming"],
         ["After storming.", "They agree on norms."], marks=2)]
DESC = ["tax returns submitted on time and making regular tax payments", "comply with the South African Bureau of Standards",
        "tax payments are adjusted to avoid paying high tax payments", "money and assets of the owners invested in a business",
        "information communicated by means of printed material", "there are diverse solutions to a problem",
        "money made available by the government for small developing businesses", "information communicated by means of an oral presentation",
        "there is only one solution to a problem", "comply with international standards of quality"]
q13 = [
    {"t": "match", "n": "1.3", "marks": 10, "q": "Choose a description from COLUMN B that matches a term in COLUMN A (1.3.1 Verbal presentation, "
     "1.3.2 Equity capital, 1.3.3 Non-conventional solutions, 1.3.4 Globalisation, 1.3.5 Good decision).",
     "clues": ["Verbal means spoken; equity is the owners' money.", "Globalisation means meeting international standards."],
     "left": ["1.3.1 Verbal presentation", "1.3.2 Equity capital", "1.3.3 Non-conventional solutions", "1.3.4 Globalisation",
              "1.3.5 Good decision"], "right": DESC, "a": [7, 3, 5, 9, 0], "each": 2, "heads": ["COLUMN A", "COLUMN B (A–J)"]}]

# ---- SECTION B, QUESTION 2: BUSINESS VENTURES, the question paper page 5 and the memo pages 8-10 ----
VA = ["Table", "Graph", "Flip chart", "Hand-out"]
q2 = [
    stmt("2.1", "Name any FOUR key success factors in a business.", 4,
         ["Sustainability", "Strategic focus", "Profitability", "A strong customer base", "Market knowledge", "Good leadership"],
         ["High staff turnover", "Unclear goals"], ["What makes a business succeed?", "Customers, leadership, profit."], 1),
    stmt("2.2", "Outline the aspects that must be considered when initiating a business.", 6,
         ["Strategies such as marketing, management and public relations are implemented and reviewed.",
          "Operations are implemented, and staff are employed and trained.", "Productivity: the rate of output per unit of input.",
          "The most appropriate size of the business must be decided."],
         ["The owner's favourite colour for the logo.", "Whether competitors will close down.", "The weather on the opening day."],
         ["Strategy, operations, productivity, size.", "What must be in place to start?"], 2),
    answer("2.3.1", "Identify the type of visual aid used by Thandi: He used columns and rows to compare the different options available to "
           "investors.", 2, [VA[0], VA[1], VA[2], VA[3]], ["Columns and rows.", "A grid of cells."]),
    answer("2.3.2", "Identify the type of visual aid used by Thandi: He showed the relationship between two variables over a period of time.",
           2, [VA[1], VA[0], VA[2], VA[3]], ["Two variables over time.", "Lines or bars on axes."]),
    stmt("2.4", "Explain the procedure for the formation of companies.", 6,
         ["Determine the people establishing the company.", "Reserve a company name with the Registrar of Companies.",
          "Prepare a memorandum of incorporation.", "File a notice of incorporation and obtain a registration number.",
          "Register the company at the CIPC and pay the prescribed fees."],
         ["Ask SARS to choose the company's name.", "Sell shares before the company is registered.", "Skip the MOI for small companies."],
         ["Name, MOI, notice, registration.", "With the CIPC."], 2),
    stmt("2.5", "Real Estate owns properties around the country. They allow businesses to enter into an agreement and make a monthly payment "
         "for the use of these properties. RE also offers information technology services to these businesses to allow them to focus on "
         "important business activities. Identify TWO avenues of acquiring businesses used by RE. Motivate your answer by quoting from the "
         "scenario.", 6,
         ["Leasing: 'They allow businesses to enter into an agreement and make a monthly payment for the use of these properties.'",
          "Outsourcing: 'RE also offers information technology services to these businesses to allow them to focus on important business "
          "activities.'"],
         ["Leasing: 'RE also offers information technology services to these businesses.'",
          "Outsourcing: 'They allow businesses to … make a monthly payment for the use of these properties.'",
          "Franchising: 'Real Estate owns properties around the country.'"],
         ["Paying monthly to use property.", "Another business does the IT."], 3),
    stmt("2.6.1", "Discuss the following benefit of establishing a company versus other forms of ownership: Legal status and liability.", 4,
         ["A company has its own legal status, trading name and owns its assets.", "Shareholders' private assets are protected, as they have "
                                                                                   "limited liability.",
          "Companies have their own names, and these are protected."],
         ["Shareholders must pay the company's debts from their private assets.", "A company has no legal status of its own."],
         ["A company is a legal person.", "Limited liability."], 2),
    stmt("2.6.2", "Discuss the following benefit of establishing a company versus other forms of ownership: Ownership and management.", 4,
         ["Shareholders can buy and sell shares freely in a public company.", "The company is managed by a qualified and competent board of "
                                                                              "directors.",
          "A company has a larger pool of skills and expertise, so it is less likely to use consultants."],
         ["One owner must manage a company alone.", "Shares in a public company can never be sold."],
         ["Shareholders own, directors manage.", "Skills and transferable shares."], 2),
    stmt("2.7", "Suggest reasons why entrepreneurs may decide to purchase an existing business.", 6,
         ["It is easier to raise financing if the business has a good history.", "There is immediate cash flow from established customers.",
          "Supply links, staff and networks are already established.", "The business may come with goodwill from a good reputation."],
         ["There is no customer base to rely on.", "Everything must be built from nothing."],
         ["Buying something already running.", "Customers, cash, networks."], 2)]

# ---- QUESTION 3: BUSINESS ROLES, the question paper page 6 and the memo pages 11-15 ----
AM = ("Assop Manufacturer specialises in manufacturing electric cars and they apply the principles of professionalism and ethics. They focus "
      "on using resources responsibly to ensure that the environment is looked after. AM also practises social responsibility by giving "
      "back to poor communities. The management of AM is also aware of the differences between professionalism and ethics.")
q3 = [
    stmt("3.1", "Name any FOUR internal causes of change.", 4,
         ["New business objectives or goals", "High employee turnover", "New policies and procedures", "New management", "Restructuring"],
         ["Changes in interest rates", "New government legislation", "Competitors' new products"],
         ["Internal: inside the business.", "Goals, people, policies."], 1),
    stmt("3.2", "Outline the importance of stress management in the workplace.", 6,
         ["Unmanaged stress results in absenteeism, poor performance and conflict.", "Managing stress minimises absenteeism and keeps "
                                                                                     "productivity up.",
          "Stressed workers make poor decisions and errors of judgement.", "Stressed staff give poor service, leading to unhappy customers."],
         ["Stress always improves employees' decisions.", "Stress management increases absenteeism."],
         ["What does stress cost a business?", "Absence, errors, service."], 2),
    pick("3.3.1", "Quote TWO principles of professionalism and ethics that AM is displaying in the scenario above.", sentences(AM), [1, 2],
         ["Principles: responsible use of resources, social responsibility …", "Which sentences show them?"]),
    sort("3.3.2", "Explain the difference between professionalism and ethics.", ["Professionalism", "Ethics"],
         [("A person acquires knowledge and skills to practise a specific job", 0), ("Applies a code of conduct of a profession or business", 0),
          ("The principles of right and wrong and what is acceptable in society", 1), ("Values that are morally acceptable within a business", 1)],
         ["Professionalism: standards of a job.", "Ethics: right and wrong."]),
    stmt("3.4", "Discuss the functions of workplace forums.", 6,
         ["Prevent unilateral decisions by employers on issues affecting employees.", "Encourage workers' participation in decision-making.",
          "Promote the interests of all employees in the workplace.", "Promote efficiency in the workplace through co-operation."],
         ["Set the business's prices.", "Replace trade unions by law.", "Discipline managers."], ["Forums give workers a voice.",
                                                                                                 "Participation and consultation."], 2),
    stmt("3.5", "Eastern Hotel reduced the number of employees at the hotel to decrease their costs. EH also offers equal opportunities to people "
         "from previously disadvantaged groups as a legal stipulation. Identify TWO major changes that people and businesses have to deal "
         "with in the scenario above. Motivate your answer by quoting from the scenario.", 6,
         ["Retrenchment: 'They reduced the number of employees at the hotel to decrease their costs.'",
          "Affirmative action: 'EH also offers equal opportunities to people from previously disadvantaged groups as a legal stipulation.'"],
         ["Affirmative action: 'They reduced the number of employees at the hotel.'", "Retrenchment: 'EH also offers equal opportunities.'",
          "Globalisation: 'Eastern Hotel is exposed to difficult economic conditions.'"], ["Fewer staff.", "Equal opportunities."], 3),
    stmt("3.6", "Discuss the importance of teamwork.", 6,
         ["Teamwork gives a sense of unity, with shared interests and responsibilities.", "It reduces stress as members work towards a common "
                                                                                          "goal.",
          "The combined efforts of members are more than the sum of individual efforts.", "It produces creative solutions through "
                                                                                          "brainstorming."],
         ["Teamwork removes all responsibility from members.", "Teams always take longer and achieve less."],
         ["Together is stronger.", "Unity, stress, creativity."], 2),
    stmt("3.7", "Recommend ways in which professional, responsible, ethical and effective business practices should be conducted.", 6,
         ["Treat all employees equally, regardless of race, gender, age or disability.", "Pay fair wages that meet the requirements of the "
                                                                                         "BCEA.",
          "Make business decisions transparent to all stakeholders.", "Draw up a code of ethics (conduct)."],
         ["Use other businesses' trademarks to save time.", "Pay taxes only when audited.", "Dispose of toxic waste in rivers."],
         ["Fairness, honesty, accountability.", "What would a good business do?"], 2)]

# ---- QUESTION 4: MISCELLANEOUS TOPICS, the question paper page 7 and the memo pages 16-21 ----
TS = ["Forming", "Storming", "Norming", "Adjourning (mourning)"]
q4 = [
    stmt("4.1", "Name any FOUR stages of action plan/steps to follow when drawing up an action plan.", 4,
         ["Define the vision, mission and goals.", "Define the steps to get there.", "Arrange the steps in logical order.",
          "Identify the end point for each step.", "Review progress regularly."],
         ["Skip the planning and start working.", "Keep the plan secret from the team.", "Never check progress."],
         ["Goals, steps, order, review.", "An action plan turns plans into tasks."], 1),
    stmt("4.2", "Elaborate on the meaning of memorandum of incorporation.", 4,
         ["The MOI serves as the constitution of a company.", "Companies are governed according to the rules in the MOI.",
          "It describes the rights and duties of the shareholders and directors.", "It gives details about the company's name and share "
                                                                                   "capital."],
         ["The MOI is the company's annual tax return.", "The MOI lists the company's customers."],
         ["A founding document.", "The company's rules."], 2),
    answer("4.3.1", "Ronald Warehousing received funding from a wealthy entrepreneur in exchange for a share in the business. Identify the "
           "source of funding that RW received in the scenario.", 2, ["Angel funding", "A bank loan", "A government grant", "An overdraft"],
           ["A wealthy individual.", "In exchange for a share."]),
    stmt("4.3.2", "Explain the reasons why businesses need funding.", 6,
         ["To cover start-up costs, including premises, machinery and raw materials.", "To run the business and pay employees and suppliers.",
          "To pay for the cost of inputs, such as wages and telephone costs.", "To expand the business as sales increase."],
         ["To avoid paying suppliers.", "To pay the owner's private debts."], ["Start, run, grow.", "What must be paid for?"], 2),
    stmt("4.4", "Recommend factors that the presenter must consider when preparing a presentation.", 4,
         ["Be clear about the purpose of the presentation.", "Know the background of the audience.", "Include visual aids that enhance the "
                                                                                                     "presentation.",
          "Practise the delivery so that the time is not exceeded."],
         ["Read the slides word for word without preparation.", "Use difficult jargon to impress."],
         ["Purpose, audience, practice.", "Prepare before."], 2),
    stmt("4.5", "Outline the causes of conflict in the workplace.", 6,
         ["Lack of proper communication between leaders and members.", "Differences in backgrounds, cultures, values and beliefs.",
          "Limited business resources.", "Unfair workload among employees."],
         ["Clear roles and good communication.", "Fair treatment of all workers."], ["Why do people disagree at work?",
                                                                                     "Communication, resources, differences."], 2),
    answer("4.6.1", "Identify the stage of team development: The newly appointed members of the marketing team were comfortable with each other "
           "during their first meeting.", 2, [TS[0], TS[1], TS[2], TS[3]], ["A new team.", "The first stage."]),
    answer("4.6.2", "Identify the stage of team development: Rowena, the team leader of the cleaning team, ensured that all tasks are completed "
           "before the team finally part ways.", 2, [TS[3], TS[0], TS[1], TS[2]], ["The team parts ways.", "The last stage."]),
    stmt("4.7", "Discuss any TWO theories of ethics that are applicable in the workplace.", 6,
         ["Consequential theory: an action is good or bad depending on its outcome.",
          "The common good approach: business values are in line with the society in which it operates.",
          "The rights approach: individuals' rights are respected and people are treated with dignity."],
         ["Consequential theory: the outcome of an action never matters.", "The rights approach: employees have no rights at work."],
         ["Outcomes, society, rights.", "Each card gives a theory and what it means."], 3),
    stmt("4.8", "Recommend ways in which businesses could deal with crisis in the workplace.", 4,
         ["Assess and evaluate the nature of the crisis.", "Intervene swiftly, without panicking or overreacting.",
          "Provide accurate and correct information.", "Obtain expert advice if the crisis is outside the business's expertise."],
         ["Ignore the crisis until it goes away.", "Hide information from stakeholders."], ["Calm, quick, informed.", "Assess, act, "
                                                                                                                    "communicate."], 2)]

# ---- SECTION C, the essays (answer any ONE), the question paper page 8 and the memo pages 22-29 ----
Q5_STEM = ("Businesses that follow the project planning steps will ensure the completion of their tasks. A business plan is essential to "
           "ensure that the proposed business goals are achieved. Planning tools provide guidelines on how to transform a business plan into "
           "an action plan and businesses use action plans to organise their activities.\n\nWrite an essay on transforming a business plan "
           "into an action plan in which you include the following aspects:\n• Outline the project planning steps.\n• Explain the purpose of a "
           "business plan.\n• Discuss the importance of timelines and Gantt charts/Work Breakdown Structure (WBS).\n• Advise businesses on the "
           "importance of an action plan.")
Q5_EX = ["For example, a bakery opening a second shop plots each task, from fitting ovens to hiring staff, on a Gantt chart.",
         "For example, a start-up shows its business plan to a bank to apply for a loan."]
q5 = essay("5.7", [
    stmt("5.1", "Introduction: pick the TWO statements that introduce this essay on transforming a business plan into an action plan.", 2,
         ["Project planning steps ensure that business projects are completed successfully.",
          "A business plan is a written document that gives a comprehensive overview of a proposed business.",
          "An action plan is a checklist of steps or tasks needed to reach the business goals."],
         ["A business plan is a receipt for goods bought.", "An action plan replaces the need for any goals.",
          "Gantt charts are used to pay employees."], ["An introduction says what the essay is about.", "Which cards are true?"], 1),
    stmt("5.2", "Outline the project planning steps.", 8,
         ["Define the scope of the plan.", "Identify the resources (people, budget and time) needed.", "Break the project down into activities.",
          "Set time frames and milestones.", "Plot the activity schedule on a Gantt chart.", "Monitor progress regularly."],
         ["Start the project before defining it.", "Never record the activities."], ["Scope, resources, time, monitor.",
                                                                                    "From start to finish."], 2),
    stmt("5.3", "Explain the purpose of a business plan.", 8,
         ["Gain insight into the market and competition.", "Obtain funding from investors.", "Set realistic goals and objectives.",
          "Check the performance of the business against set goals.", Q5_EX[1]],
         ["Keep the business's goals hidden from investors.", "Replace the need for a budget.", "Avoid market research."],
         ["Direction and funding.", "Why write it down?"], 2),
    stmt("5.4", "Discuss the importance of timelines and Gantt charts/Work Breakdown Structure (WBS).", 6,
         ["Timelines indicate the due date for each task.", "Gantt charts show progress on an activity so managers can monitor it.",
          "Team members can see who is responsible for each activity.", Q5_EX[0]],
         ["Gantt charts hide which activities run at the same time.", "Timelines remove the need for deadlines."],
         ["Planning tools show time.", "Who, what, when."], 2),
    stmt("5.5", "Advise businesses on the importance of an action plan.", 6,
         ["An action plan helps projects to be achieved within a specific time.", "Businesses can prioritise activities by importance.",
          "It is a control measure against which performance can be measured.", "It turns plans into actions."],
         ["An action plan makes monitoring impossible.", "It removes accountability."], ["Plans into actions.", "Priorities and control."],
         2),
    stmt("5.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["The business plan serves as a roadmap that provides direction to the business.",
          "The action plan clarifies the objective and identifies areas that need change."],
         ["Planning tools waste a business's time.", "Businesses succeed best without any plan.", "Gantt charts should be avoided."],
         ["A conclusion sums up why it all matters.", "Which card would a business agree with?"], 2),
], [("5.3", Q5_EX[1]), ("5.4", Q5_EX[0])], INSIGHT_CLUES)
Q6_STEM = ("Businesses use routine thinking and creative thinking to solve their problems. Creative thinking has many advantages and "
           "businesses can also apply the Delphi technique and the Force field analysis as problem-solving techniques. Businesses should "
           "create an environment that stimulates creative thinking in the workplace.\n\nWrite an essay on creative thinking and "
           "problem-solving in which you include the following aspects:\n• Outline the differences between routine thinking and creative "
           "thinking.\n• Explain the advantages of creative thinking in the workplace.\n• Discuss how the businesses can apply the following "
           "problem-solving techniques: Delphi technique; Force field analysis.\n• Recommend ways in which businesses can create an environment "
           "that stimulates creative thinking in the workplace.")
Q6_EX = ["For example, a cellphone company asks a panel of experts by e-mail, in three rounds, how to improve battery life.",
         "For example, a retailer puts suggestion boxes in every store and rewards the best idea each month."]
q6 = essay("6.8", [
    stmt("6.1", "Introduction: pick the TWO statements that introduce this essay on creative thinking and problem-solving.", 2,
         ["The business environment is volatile and requires advanced problem-solving skills and creative thinking.",
          "A force field analysis is useful to overcome resistance to change.",
          "Creative thinking enables businesses to develop new ways of doing things."],
         ["Creative thinking means repeating what worked before.", "The Delphi technique needs all experts in one room.",
          "Problem-solving is only for managers."], ["An introduction says what the essay is about.", "Which cards are true?"], 1),
    sort("6.2", "Outline the differences between routine thinking and creative thinking.", ["Routine thinking", "Creative thinking"],
         [("Ordinary, conventional thinking with a logical, methodical way of doing things", 0), ("No new ideas or thought patterns are "
                                                                                                   "generated", 0),
          ("Looks at a problem in a new and different way, generating new ideas", 1), ("Explores innovative ideas to obtain better results",
                                                                                        1),
          ("Applies past decisions to current problems", 0), ("Uses imagination and insight to find solutions to unique challenges", 1)],
         ["Same old way, or a new way?", "Sort each card."]),
    stmt("6.3", "Explain the advantages of creative thinking in the workplace.", 8,
         ["Better, unique solutions are generated.", "It may give the business a competitive advantage.",
          "Complex business problems may be solved.", "It improves motivation amongst staff members."],
         ["It stops all new ideas.", "It makes employees resist change."], ["New ideas, new advantages.", "Solutions and motivation."], 2),
    stmt("6.4", "Discuss how businesses can apply the Delphi technique as a problem-solving technique.", 4,
         ["Invite a panel of experts, who are contacted individually.", "Send the experts a questionnaire on the problem.",
          "Summarise their responses in a feedback report and send a second questionnaire.", Q6_EX[0]],
         ["Bring all the experts together for one face-to-face vote.", "Use only the manager's own opinion."],
         ["Experts, rounds, consensus.", "Questionnaires, not a meeting."], 2),
    stmt("6.5", "Discuss how businesses can apply force field analysis as a problem-solving technique.", 4,
         ["Describe the current situation and the desired situation.", "List all driving and restraining forces.",
          "Allocate a score to each force, from 1 (weak) to 5 (strong).", "Weigh up the forces and decide if the change is viable."],
         ["Ignore the restraining forces.", "Choose the solution before listing any forces."], ["Forces for and against change.",
                                                                                               "Score and weigh them."], 2),
    stmt("6.6", "Recommend ways in which businesses can create an environment that stimulates creative thinking in the workplace.", 6,
         ["Inspire staff to come up with new ideas.", "Hold regular brainstorming workshops.", "Train staff in creative problem-solving skills.",
          Q6_EX[1]],
         ["Punish employees whose ideas fail.", "Close all communication channels."], ["Encourage, train, listen.", "Make ideas welcome."],
         2),
    stmt("6.7", "Conclusion: pick the statement that concludes this essay.", 2,
         ["Creative thinking lets businesses respond to challenges more successfully than routine thinking.",
          "A creative environment encourages staff to come up with new ideas and solutions."],
         ["Routine thinking always gives the best results.", "Creative thinking has no place in business.",
          "Problem-solving techniques waste time."], ["A conclusion sums up why it all matters.", "Which card would a business agree with?"],
         2),
], [("6.4", Q6_EX[0]), ("6.6", Q6_EX[1])], INSIGHT_CLUES)

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 10,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Complete the statements", "marks": 10,
     "lead": "Complete the following statements by using the word(s) provided in the list below.\n" + WORDS, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column A and Column B", "marks": 10,
     "lead": "Choose a description from COLUMN B that matches a term in COLUMN A.", "items": q13},
    {"id": "2", "title": "Question 2", "kind": "Business ventures", "marks": 40, "lead": "QUESTION 2: BUSINESS VENTURES", "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Business roles", "marks": 40,
     "lead": "QUESTION 3: BUSINESS ROLES\n3.3 ASSOP MANUFACTURER (AM)\n" + AM, "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Miscellaneous topics", "marks": 40, "lead": "QUESTION 4: MISCELLANEOUS TOPICS", "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Essay: business plan to action plan", "marks": 40,
     "lead": "Build the essay section by section, then see your insight.", "extract": "QUESTION 5: THE ESSAY\n\n" + Q5_STEM, "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Essay: creative thinking", "marks": 40,
     "lead": "Build the essay section by section, then see your insight.", "extract": "QUESTION 6: THE ESSAY\n\n" + Q6_STEM, "items": q6},
]
P.finish(missions,
         {"subject": "Business Studies", "title": "Business Studies P2", "sitting": "November 2024", "total_marks": 150, "time": "2 hours"},
         [P.flag_answers(),
          {"n": "3.3.1", "kind": "no_fit", "detail": "The quote item is played by picking the scenario's sentences, as Grade 12."},
          {"n": "5.7", "kind": "no_fit", "detail": "Each essay plays as sections, one per memo heading, their facts scaled to the memo's cap of 32 "
                                                   "(Question 5: 2 + 8 + 8 + 6 + 6 + 2 of 2 + 12 + 12 + 12 + 10 + 2; Question 6: 2 + 6 + 8 + 4 + "
                                                   "4 + 6 + 2 of 2 + 8 + 14 + 8 + 8 + 8 + 2, the Delphi technique and force field analysis "
                                                   "each its own section), then insight (8)."},
          {"n": "2.5", "kind": "no_fit", "detail": "An avenue (or change) and its quote are one card (3 marks: the memo's 2 + 1): 2.5, 3.5."}],
         {"1": 30, "2": 40, "3": 40, "4": 40, "5": 40, "6": 40}, 150, {}, "Sections A, B and C (the whole paper)",
         sections=[("Section A", 30, None, ["1"]), ("Section B", 80, 2, ["2", "3", "4"]), ("Section C", 40, 1, ["5", "6"])])
