"""Grade 11 Business Studies P2 November 2025 (Eastern Cape Department of Education), the whole paper (Sections A, B and C, 150 marks,
2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options, marks and memo points are
the paper's and the memo's own; clues are ours. Source (PROVENANCE-g10-g11.md): ecexams.co.za, 2025 November Grade 11, the question
paper zip (English PDF, 9 pages, text layer) and the memo zip (English, 26 pages).

  python tools/ingest/transcribe_g11_bs_p2_2025_11_ec.py
  python tools/ingest/ingest.py "uploads/provincial/g11-bs-p2-2025-11-ec/BUSINESS STUDIES P2 GR11 QP NOV2025_English_watermark.pdf" "uploads/provincial/g11-bs-p2-2025-11-ec/BUSINESS STUDIES P2 GR11 MEMO NOV2025_English_watermark.pdf" --id g11-bs-p2-2025-11-ec --from-json

The Business Studies rulings, as in transcribe_g11_bs_p1_2024_11_ec.py."""
from provincial import Paper, sentences

P = Paper("g11-bs-p2-2025-11-ec", 595.32, 841.92, {}, start=1)
answer, stmt, mcq, term, sort, essay = P.answer, P.stmt, P.mcq, P.term, P.sort, P.essay
pick = lambda n, q, opts, pool, clues: {"t": "pickn", "n": n, "marks": len(pool), "q": q, "clues": clues, "opts": opts, "pool": pool,
                                        "count": len(pool)}
INSIGHT_CLUES = ["Insight is earned from how you answered the sections.", "Right first time, every heading answered, and the examples picked."]

# ---- SECTION A, QUESTION 1, the question paper pages 3-5 and the memo page 7 ----
q11 = [
    mcq("1.1.1", "The ... serves as the constitution of a company.", ["initial public offer", "memorandum of incorporation", "prospectus",
                                                                      "notice of incorporation"], 1,
        ["The company's rules.", "MOI."]),
    mcq("1.1.2", "Zonke sold the right to use the name and trademark of Fruit and Veg Delivery Company to Tiny in return for a/an … fee.",
        ["royalties", "rent", "franchising", "outsourcing"], 0, ["A franchise fee paid regularly.", "Paid for the use of a name."]),
    mcq("1.1.3", "A/an ... shows activities that must be completed.", ["business plan", "report", "action plan", "timelines"], 2,
        ["Activities to complete.", "A plan of actions."]),
    mcq("1.1.4", "Solutions that are not created as part of the norm and which do not follow what is generally done, are known as …",
        ["conventional.", "routine.", "non-conventional.", "creative thinking."], 2, ["Not the norm.", "Non-…"]),
    mcq("1.1.5", "One of the causes of stress in the workplace is …", ["serious illness of employees.", "consulting experts.",
                                                                       "evaluating the emergency plan of the business.",
                                                                       "unconducive working conditions."], 3,
        ["A cause, not a crisis or a response.", "The working environment."])]
WORDS = "flyer; public; crisis; slides; bad; equity capital; stress; good; angel funding; private"
q12 = [
    term("1.2.1", "Zanele traders may not offer shares to the general public. This refers to a ... company.", ["private"],
         ["Not public.", "(Pty) Ltd."], marks=2),
    term("1.2.2", "Mr Veejay, a wealthy entrepreneur, provided … in exchange for a share in the business.", ["angel funding"],
         ["A wealthy individual investor.", "Angel …"], marks=2),
    term("1.2.3", "Simcock Tech Wear Clothing used a thin sheet of paper to advertise their products. This is known as a …", ["flyer"],
         ["A thin sheet handed out.", "Not a poster."], marks=2),
    term("1.2.4", "The leader of M&M Financial Services has many tasks to do in a short space of time. This causes …", ["stress"],
         ["Too much to do.", "Pressure."], marks=2),
    term("1.2.5", "Sound ethical practice is part of … decision-making in business.", ["good"], ["Ethical decisions are …", "Not bad."],
         marks=2)]
DESC = ["using routine methods to solve problems", "occurs when a business reduces the number of workers in the business or organisation",
        "shows the duration of the task/element", "a set of values that are morally acceptable within a business organisation",
        "communicate information by means of printed material",
        "a set of rules and responsibilities of an organisation or business that the employees must comply with",
        "shows all the tasks that need to be done", "communicate information by means of oral presentations",
        "using non-routine methods to solve problems", "occurs when employees lose their jobs due to resignation or retrenchment"]
q13 = [
    {"t": "match", "n": "1.3", "marks": 10, "q": "Choose a description from COLUMN B that matches a term in COLUMN A (1.3.1 Gantt chart, 1.3.2 "
     "Non-verbal presentation, 1.3.3 Creative thinking, 1.3.4 Code of conduct, 1.3.5 Unemployment).",
     "clues": ["A Gantt chart shows how long each task takes.", "Non-verbal means printed, not spoken."],
     "left": ["1.3.1 Gantt chart", "1.3.2 Non-verbal presentation", "1.3.3 Creative thinking", "1.3.4 Code of conduct", "1.3.5 Unemployment"],
     "right": DESC, "a": [2, 4, 8, 5, 9], "each": 2, "heads": ["COLUMN A", "COLUMN B (A–J)"]}]

# ---- SECTION B, QUESTION 2: BUSINESS VENTURES, the question paper page 6 and the memo pages 8-11 ----
EQ = ["Perseverance", "Creativity", "Risk-taking", "Leadership"]
q2 = [
    stmt("2.1", "Name any FOUR stages of an action plan.", 4,
         ["Define the vision, mission and goals.", "Define the steps to get there.", "Arrange the steps in logical order.",
          "Identify the end point for each step.", "Review progress regularly."],
         ["Skip the planning and start working.", "Keep the plan secret from the team.", "Never check progress."],
         ["Goals, steps, order, review.", "An action plan."], 1),
    stmt("2.2", "Outline aspects that must be included in the prospectus.", 6,
         ["Name of the company", "Company overview, including its vision, mission and goals", "Management team",
          "The risks and potential of the business", "Financial position and share information"],
         ["The directors' home addresses", "The staff's leave records", "The canteen menu"], ["A prospectus invites investors.",
                                                                                              "What would an investor want to know?"], 2),
    answer("2.3.1", "Identify the entrepreneurial quality: The manager of GM steel manufacturer did not lose hope when the global tariffs "
           "threatened the local businesses.", 2, [EQ[0], EQ[1], EQ[2], EQ[3]], ["Did not lose hope.", "Kept going."]),
    answer("2.3.2", "Identify the entrepreneurial quality: Zuko provides special material like fiber glass for the clients who were not able to "
           "afford the original material amid market uncertainty.", 2, [EQ[1], EQ[0], EQ[2], EQ[3]], ["A new solution.", "Thinking of "
                                                                                                                         "something new."]),
    stmt("2.4", "Explain the purpose of a business plan.", 6,
         ["Gain insight into the market and competition.", "Offer direction for a proposed business.", "Check the performance of the business "
                                                                                                         "against set goals.",
          "Convince others of the business's profitability, such as when applying for finance."],
         ["Keep the business's goals hidden from investors.", "Replace the need for a budget."], ["Direction and funding.",
                                                                                                "Why write a plan?"], 2),
    stmt("2.5.1", "Telly Gadgets is a newly established business that specialises in manufacturing TV gadgets. Ntombi, the owner of TG, "
         "conducted research to identify her target market. She also changed some of her original business plans, due to new technology. "
         "Identify TWO factors from the scenario that need to be considered before starting the business. Motivate your answer by quoting "
         "from the scenario.", 6,
         ["Customer service: 'Ntombi, the owner of TG, conducted research to identify her target market.'",
          "Environmental change: 'She also changed some of her original business plans, due to new technology.'"],
         ["Customer service: 'She also changed some of her original business plans, due to new technology.'",
          "Environmental change: 'Ntombi … conducted research to identify her target market.'",
          "Cost saving: 'Telly Gadgets is a newly established business.'"], ["Customers and change.", "Match each factor to its quote."], 3),
    stmt("2.6.1", "Discuss how the presenter must prepare slides.", 4,
         ["Use keywords instead of full sentences.", "Use a legible font and font size.", "Limit the amount of information on each slide.",
          "Make sure there are no spelling errors."],
         ["Fill every slide with long paragraphs.", "Use tiny fonts to fit more in."], ["Simple and readable.", "Keywords."], 2),
    stmt("2.6.2", "Discuss how the presenter must prepare posters.", 4,
         ["Use a title to draw the reader's attention.", "Design the poster to be attractive and eye-catching.",
          "Keep it simple, with few words.", "Use a big, bold font."],
         ["Use small print for all the details.", "Avoid any pictures."], ["Seen from a distance.", "Simple and bold."], 2),
    stmt("2.7", "Advise the business on the legal requirements of the name of the company.", 6,
         ["A name reserved at the CIPC cannot be used by another company.", "The name of a company is subject to approval by the CIPC.",
          "The name must be original and may not be misleading.", "The name must show the type of company, e.g. a private company ends with "
                                                                  "(Pty) Ltd."],
         ["Any name may be used, even one already registered.", "The name may be offensive if it attracts attention."],
         ["The CIPC approves names.", "Original, and shows the type."], 2)]

# ---- QUESTION 3: BUSINESS ROLES, the question paper page 7 and the memo pages 11-14 ----
q3 = [
    stmt("3.1", "Mention any FOUR external causes of change.", 4,
         ["Political factors", "Social factors", "Legal factors", "Economic factors", "Technological factors"],
         ["New management", "High staff turnover", "Restructuring"], ["External: outside the business.", "PESTLE."], 1),
    stmt("3.2", "Outline the causes of conflict in the business.", 6,
         ["Lack of proper communication between management and workers.", "Different personalities and backgrounds.",
          "Lack of recognition for good work.", "Unfair disciplinary procedures, such as favouritism."],
         ["Clear roles and good communication.", "Fair treatment of all workers."], ["Why do people disagree at work?",
                                                                                     "Communication and fairness."], 2),
    stmt("3.3.1", "Macros Manufacturer encountered severe challenges, including the breakdown of machinery, managers who are not competent or "
         "efficient, along with power outages. Name the TWO examples of crises from the scenario.", 2,
         ["Breakdown of machinery", "Power outages"], ["Manufacturing chocolates", "A newly established business", "Selling to retailers"],
         ["A crisis is a sudden event.", "Machines and electricity."], 1),
    stmt("3.3.2", "Discuss the importance of stress management in the workplace.", 4,
         ["Unmanaged stress can cause staff health issues.", "Managing stress curbs absenteeism and maintains productivity.",
          "Stressed workers display poor judgement in a crisis.", "Conflict can be avoided if stress is managed."],
         ["Stress always improves decisions.", "Stress management increases absenteeism."], ["What does stress cost?", "Health, absence, "
                                                                                                                        "errors."], 2),
    stmt("3.4.1", "Eugene Creatives wants to change the structure of the business to introduce digital services. They called for all the opposing "
         "and supporting ideas for this development. They also decided to invite experts to help them deal with their challenge. Identify TWO "
         "problem-solving techniques used by EC. Motivate by quoting from the scenario.", 6,
         ["Force field analysis: 'They called for all the opposing and supporting ideas for this development.'",
          "Delphi technique: 'They also decided to invite experts to help them deal with their challenge.'"],
         ["Delphi technique: 'They called for all the opposing and supporting ideas.'", "Force field analysis: 'They also decided to invite "
                                                                                       "experts.'",
          "Brainstorming: 'Eugene Creatives specialises in producing art and creations.'"], ["For and against: forces.", "Experts: Delphi."],
         3),
    stmt("3.4.2", "Explain the advantages of creative thinking in the workplace.", 6,
         ["Better, unique solutions are generated.", "It may give the business a competitive advantage.", "Complex problems may be solved.",
          "It improves motivation amongst staff."],
         ["It stops all new ideas.", "It makes employees resist change."], ["New ideas.", "Solutions and motivation."], 2),
    stmt("3.5", "Discuss the functions of work forums.", 6,
         ["Prevent unilateral decisions by employers on issues affecting employees.", "Encourage workers' participation in decision-making.",
          "Promote the interests of all employees.", "Promote efficiency through co-operation."],
         ["Set the business's prices.", "Discipline managers."], ["A voice for workers.", "Participation."], 2),
    stmt("3.6", "Recommend ways to deal with crisis in the workplace.", 6,
         ["Respond appropriately and quickly to lessen the effects of the crisis.", "Identify the real nature of the crisis by assessing it.",
          "Provide accurate and correct information.", "Communicate with all stakeholders."],
         ["Ignore the crisis until it passes.", "Hide information from stakeholders."], ["Calm, quick, informed.", "Assess and communicate."],
         2)]

# ---- QUESTION 4: MISCELLANEOUS TOPICS, the question paper page 8 and the memo pages 15-18 ----
DCD = ("Sandra the owner of DCD wants to improve customer service in the city of Johannesburg. She considers acquiring funding from wealthy "
       "business people to cover the start-up cost of buying premises. DCD also hires temporary employees so as to save costs. Pay costs of "
       "input such as wages, telephone and other expenses.")
PE = ["Competence", "Confidentiality", "Accountability", "Transparency"]
q4 = [
    stmt("4.1", "Name any FOUR key success factors.", 4,
         ["Profitability", "Sustainability", "Market knowledge", "A strong customer base", "Good leadership"],
         ["High staff turnover", "Unclear goals", "Poor customer service"], ["What makes a business succeed?", "Profit, customers, "
                                                                                                               "leaders."], 1),
    stmt("4.2", "Outline the reasons why entrepreneurs may decide to purchase an existing business.", 6,
         ["An established business takes little time to set up.", "It has an existing customer base.",
          "Market research has already been done.", "It already has customers and continued cash flow."],
         ["It has no customers yet.", "Everything must be built from nothing."], ["Buying something already running.", "Customers and "
                                                                                                                       "cash."], 2),
    pick("4.3.1", "Quote TWO reasons why the business needs to acquire funding.", sentences(DCD), [1, 3],
         ["Funding pays for start-up and running costs.", "Premises and inputs."]),
    stmt("4.3.2", "Explain grants as a source of funding.", 4,
         ["A business may qualify for government support to get started.", "A grant is funding from the government.",
          "Grants are normally cheaper than other sources of funding."],
         ["A grant must be repaid with high interest.", "A grant is a loan from a friend."], ["Government money.", "Not repaid."], 2),
    stmt("4.4", "Recommend areas for improvement on key success factors.", 4,
         ["Regularly evaluate the price of every product.", "Keep business expenses to a minimum.", "Set goals with reasonable milestones.",
          "Know the needs of customers, e.g. through surveys."],
         ["Ignore customers' feedback.", "Never review the business's structure."], ["Price, costs, goals, customers.", "Improve."], 2),
    stmt("4.5", "Outline the THREE stages of development.", 6, ["Forming", "Storming", "Norming", "Performing"],
         ["Recruiting", "Retrenching", "Advertising"], ["Team development.", "Forming, …"], 2),
    answer("4.6.1", "Identify the principle of professionalism and ethics: Nomsa always demonstrates a combination of technical skill and the "
           "ability to communicate effectively.", 2, [PE[0], PE[1], PE[2], PE[3]], ["Skill and ability.", "Competent."]),
    answer("4.6.2", "Identify the principle of professionalism and ethics: Ahmad, the team leader, never shares the employees' details with "
           "another team member.", 2, [PE[1], PE[0], PE[2], PE[3]], ["Keeps details private.", "Confidential."]),
    stmt("4.7", "Discuss strategies businesses can use to deal with globalisation.", 6,
         ["Stay attentive to changes and trends in their industry.", "Stay up to date with new technology to keep a competitive edge.",
          "Explore overseas markets for their products.", "Ensure products meet international standards of quality."],
         ["Ignore foreign competitors.", "Avoid new technology."], ["Compete worldwide.", "Technology, markets, standards."], 2),
    stmt("4.8", "Recommend ways in which businesses can create an environment that stimulates creative thinking in the workplace.", 4,
         ["Encourage alternative ways of working.", "Respond enthusiastically to all ideas.", "Place suggestion boxes around the workplace.",
          "Train staff in creative problem-solving skills."],
         ["Punish employees whose ideas fail.", "Close all communication channels."], ["Welcome ideas.", "Encourage and train."], 2)]

# ---- SECTION C, the essays (answer any ONE), the question paper page 9 and the memo pages 19-26 ----
Q5_STEM = ("Entrepreneurs who enter into franchise should understand the meaning of franchise. They also need to understand both the "
           "advantages and the disadvantages of the franchise. Businesses who want to downscale and focus on the core aspect of the business, "
           "outsource the less critical operations. The lease agreement outlines the main responsibilities and contractual rights of the "
           "lessee.\n\nWrite an essay on avenues of acquiring a business in which you include the following aspects:\n• Elaborate on the "
           "meaning of franchise as a type of avenue for acquiring business.\n• Explain the advantages and disadvantages of franchises.\n• "
           "Discuss the advantages of outsourcing.\n• Advise businesses on the contractual implications of leasing.")
Q5_EX = ["For example, many restaurant chains in South Africa, such as Debonairs, KFC and Wimpy, run as franchises.",
         "For example, a mining company outsources its security to a specialist firm and its staff focus on mining."]
q5 = essay("5.8", [
    stmt("5.1", "Introduction: pick the TWO statements that introduce this essay on avenues of acquiring a business.", 2,
         ["A franchise agreement legally outlines the terms of the relationship between a franchisor and a franchisee.",
          "Outsourcing allows businesses to focus on important business activities.",
          "The lease agreement indicates whether the lessee becomes the owner of the asset after the lease period."],
         ["A franchise is a loan from a bank.", "Outsourcing means closing the business.", "A lease transfers ownership immediately."],
         ["An introduction says what the essay is about.", "Which cards are true?"], 1),
    stmt("5.2", "Elaborate on the meaning of franchise as a type of avenue for acquiring business.", 6,
         ["A franchise is a licence to use the idea, name and processes of an existing business in a specific area.",
          "It is an agreement between a franchisor and a franchisee.", "The franchisor sells the right to trade in the product.",
          "The franchisee buys the right to offer the same products or services.", Q5_EX[0]],
         ["The franchisee owns the brand's trademark.", "A franchise is a government grant."], ["Two parties and a licence.",
                                                                                               "Franchisor and franchisee."], 2),
    stmt("5.3", "Explain the advantages of franchises.", 6,
         ["The business is based on a proven idea, and the product is tried and tested.", "Management advice and training are provided.",
          "Marketing and advertising costs can be shared.", "Banks are more likely to finance an established business."],
         ["Franchisees never pay any fees.", "Franchises have a lower success rate than start-ups."], ["A proven model.", "Support and "
                                                                                                                        "lower risk."], 2),
    stmt("5.4", "Explain the disadvantages of franchises.", 4,
         ["The high initial franchise cost can make it difficult to buy in.", "There are restrictions on how the business can be run.",
          "Franchisees must pay royalties or a share of the profit.", "One poor outlet may risk the reputation of the whole franchise."],
         ["Franchisees may change the brand freely.", "Franchises never pay royalties."], ["Costs and restrictions.", "Royalties."], 2),
    stmt("5.5", "Discuss the advantages of outsourcing.", 6,
         ["It provides continuity during high staff turnover.", "A company can reduce costs.", "It gives access to skilled people without "
                                                                                              "employing them.",
          "Fixed and overhead costs are lower.", Q5_EX[1]],
         ["It always increases staff costs.", "It removes access to specialists."], ["Someone else does the work.", "Costs and skills."],
         2),
    stmt("5.6", "Advise businesses on the contractual implications of leasing.", 6,
         ["The lessee has the right to occupy or use the asset.", "The lessee must keep the asset in good condition.",
          "The lessee must pay the rent on time.", "No alterations may be made without the lessor's consent."],
         ["The lessee may sell the asset.", "The lessee need not pay rent if busy."], ["Rights and responsibilities.", "Use, care, pay."], 2),
    stmt("5.7", "Conclusion: pick the statement that concludes this essay.", 2,
         ["Outsourcing allows the business to focus on its vision and core business.",
          "Acquiring a franchise can be an expensive initial outlay."],
         ["Leasing has no contractual implications.", "Franchises never have any disadvantages.", "Outsourcing always harms a business."],
         ["A conclusion sums up why it all matters.", "Which card would a business agree with?"], 2),
], [("5.2", Q5_EX[0]), ("5.5", Q5_EX[1])], INSIGHT_CLUES)
Q6_STEM = ("Businesses are required to conduct their operations in an ethical and professional manner. Businesses must know how effective "
           "business practice should be conducted. Theories of ethics guide businesses and individuals when they need to make morally correct "
           "decisions. When establishing a business, one needs to understand the benefits of ethical business ventures.\n\nWrite an essay on "
           "professionalism and ethics in which you must include the following aspects:\n• Outline the differences between professionalism and "
           "ethics.\n• Discuss ways in which professional, responsible, ethical and effective business practice should be conducted.\n• "
           "Briefly explain the THREE theories of ethics that are applicable to the workplace.\n• Advise businesses on the benefits of ethical "
           "business ventures.")
Q6_EX = ["For example, a retailer pays its cashiers overtime for public holidays, as the BCEA requires.",
         "For example, a clothing brand that pays workers fairly gains loyal customers on social media."]
q6 = essay("6.7", [
    stmt("6.1", "Introduction: pick the TWO statements that introduce this essay on professionalism and ethics.", 2,
         ["Businesses have a code of conduct that outlines the expected behaviour of their employees.",
          "Unethical business practices can have a negative impact on a business.",
          "Businesses that adopt ethical practices remain sustainable over a long period."],
         ["Ethics are only for government departments.", "Professionalism means wearing expensive clothes.",
          "Ethical businesses always make losses."], ["An introduction says what the essay is about.", "Which cards are true?"], 1),
    sort("6.2", "Outline the differences between professionalism and ethics.", ["Professionalism", "Ethics", "Not true"],
         [("A set of standards of expected behaviour", 0), ("Focuses on upholding the reputation of a business or profession", 0),
          ("Conforms to a set of values that is morally acceptable", 1), ("Focuses on developing a moral compass for decisions", 1),
          ("Allows employees to ignore the code of conduct", 2), ("Means following no rules at all", 2)],
         ["Standards of a job, or right and wrong?", "Sort each card."]),
    stmt("6.3", "Discuss ways in which professional, responsible, ethical and effective business practice should be conducted.", 8,
         ["Treat all employees equally, regardless of race, gender or disability.", "Pay fair wages in line with the BCEA.",
          "Ensure a safe and fair work environment.", "Refrain from using other businesses' protected ideas.", Q6_EX[0]],
         ["Pollute the environment to save costs.", "Discriminate when promoting staff."], ["Fairness and respect.", "Laws and ethics."],
         2),
    stmt("6.4", "Briefly explain the THREE theories of ethics that are applicable to the workplace.", 6,
         ["Consequential theory: an act is judged by its effect on others.",
          "Common good approach: the business's values are in line with the society in which it operates.",
          "The rights approach: people's basic rights are identified and protected."],
         ["Consequential theory: the outcome of an act never matters.", "The rights approach: employees have no rights at work."],
         ["Outcomes, society, rights.", "Each card gives a theory and what it means."], 2),
    stmt("6.5", "Advise businesses on the benefits of ethical business ventures.", 8,
         ["Customer loyalty is created and a positive image is built.", "Staff morale is built by paying employees fairly.",
          "Positive relationships between co-workers improve productivity.", "Compliance with environmental regulations avoids fees.",
          Q6_EX[1]],
         ["Ethical businesses lose all their customers.", "Ethics lower staff morale."], ["What does doing right bring?", "Loyalty and "
                                                                                                                       "morale."], 2),
    stmt("6.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["A code of ethics should improve relationships and eliminate unethical business practice.",
          "Good corporate governance can address issues that challenge ethical behaviour."],
         ["Ethics have no place in business.", "Professionalism is only about appearance.", "Unethical practice has no consequences."],
         ["A conclusion sums up why it all matters.", "Which card would a business agree with?"], 2),
], [("6.3", Q6_EX[0]), ("6.5", Q6_EX[1])], INSIGHT_CLUES)

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 10,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Complete the statements", "marks": 10,
     "lead": "Complete the following statements by using the words provided in the list below.\n" + WORDS, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column A and Column B", "marks": 10,
     "lead": "Choose a description from COLUMN B that matches a term in COLUMN A.", "items": q13},
    {"id": "2", "title": "Question 2", "kind": "Business ventures", "marks": 40, "lead": "QUESTION 2: BUSINESS VENTURES", "items": q2},
    {"id": "3", "title": "Question 3", "kind": "Business roles", "marks": 40, "lead": "QUESTION 3: BUSINESS ROLES", "items": q3},
    {"id": "4", "title": "Question 4", "kind": "Miscellaneous topics", "marks": 40,
     "lead": "QUESTION 4: MISCELLANEOUS TOPICS\n4.3 DEEP CHAT DESIGN (DCD)\n" + DCD, "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Essay: avenues of acquiring a business", "marks": 40,
     "lead": "Build the essay section by section, then see your insight.", "extract": "QUESTION 5: THE ESSAY\n\n" + Q5_STEM, "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Essay: professionalism and ethics", "marks": 40,
     "lead": "Build the essay section by section, then see your insight.", "extract": "QUESTION 6: THE ESSAY\n\n" + Q6_STEM, "items": q6},
]
P.finish(missions,
         {"subject": "Business Studies", "title": "Business Studies P2", "sitting": "November 2025", "total_marks": 150, "time": "2 hours"},
         [P.flag_answers(),
          {"n": "4.3.1", "kind": "no_fit", "detail": "The quote item is played by picking the scenario's sentences, as Grade 12."},
          {"n": "5.8", "kind": "no_fit", "detail": "Each essay plays as sections, one per memo heading, their facts scaled to the memo's cap of 32 "
                                                   "(Question 5: 2 + 6 + 6 + 4 + 6 + 6 + 2 of 2 + 8 + 16 + 14 + 8 + 2, the franchise's "
                                                   "advantages and disadvantages each a section; Question 6: 2 + 6 + 8 + 6 + 8 + 2 of 2 + 8 + "
                                                   "12 + 18 + 8 + 2), then insight (8)."},
          {"n": "2.5.1", "kind": "no_fit", "detail": "A factor (or technique) and its quote are one card (3 marks: the memo's 2 + 1): 2.5.1, "
                                                     "3.4.1."}],
         {"1": 30, "2": 40, "3": 40, "4": 40, "5": 40, "6": 40}, 150, {}, "Sections A, B and C (the whole paper)",
         sections=[("Section A", 30, None, ["1"]), ("Section B", 80, 2, ["2", "3", "4"]), ("Section C", 40, 1, ["5", "6"])])
