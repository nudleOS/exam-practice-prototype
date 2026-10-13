"""Grade 10 Business Studies P2 November 2024 (North West Department of Education, provincial assessment), the whole paper (Sections
A, B and C, 150 marks, 2 hours), hand-transcribed into the catalogue format, then run through `ingest.py --from-json`. Stems, options,
marks and memo points are the paper's and the memo's own; clues are ours. Source (PROVENANCE-g10-g11.md): education.nwpg.gov.za,
Examination > Assessment, the question paper PDF (English, 10 pages, text layer) and the marking guidelines PDF (English, 33 pages).

  python tools/ingest/transcribe_g10_bs_p2_2024_11_nw.py
  python tools/ingest/ingest.py "uploads/provincial/g10-bs-p2-2024-11-nw/21-NOVEMBER-2024-NW-GR-10-S2-BUSINESS-STUDIES-QP-ENG.pdf" "uploads/provincial/g10-bs-p2-2024-11-nw/21-NOVEMBER-2024-NW-GR-10-S2-BUSINESS-STUDIES-MG-ENG.pdf" --id g10-bs-p2-2024-11-nw --from-json

The Business Studies rulings, as in transcribe_g10_bs_p1_2024_11_nw.py: every written part plays as statements to pick (a card is worth
what the memo ticks for one point: √ 1, √√ 2, a technique with its quote 3); 'differentiate/distinguish' and the SWOT analysis as
sorts; Section B answers any TWO, Section C any ONE; each essay as sections scaled to the memo's cap of 32, then insight (LASO, 8).
3.6 ('define social responsibility and give practical examples') plays as two parts, the memo's sub-maxima (2 and 4)."""
from provincial import Paper

P = Paper("g10-bs-p2-2024-11-nw", 595.2, 841.92, {}, start=12)
answer, stmt, mcq, term, sort, essay = P.answer, P.stmt, P.mcq, P.term, P.sort, P.essay
INSIGHT_CLUES = ["Insight is earned from how you answered the sections.", "Right first time, every heading answered, and the examples picked."]

# ---- SECTION A, QUESTION 1, the question paper pages 3-5 and the memo page 8 ----
q11 = [
    mcq("1.1.1", "The name of a state-owned company ends with the letters …", ["(Pty) Ltd.", "Ltd.", "Inc.", "SOC Ltd"], 3,
        ["It is owned by the state.", "SOC: state-owned company."]),
    mcq("1.1.2", "… are designed to collect information from people, in writing, about their attitudes, preferences, level of knowledge, "
        "personalities and/or beliefs.", ["Interviews", "Questionnaires", "Focus groups", "Observations"], 1,
        ["The key words are 'in writing'.", "People fill in a list of questions."]),
    mcq("1.1.3", "An example of a verbal presentation.", ["Delivering a speech in front of an audience.", "Sending a business report via email.",
        "Giving handouts at the start of a meeting.", "Putting up a poster with the newly updated laws on the wall."], 0,
        ["Verbal means spoken.", "Which one uses the voice?"]),
    mcq("1.1.4", "The … technique links key concepts using images and lines to a central concept.", ["Delphi", "Brainstorming",
        "Nominal group", "Mind-mapping"], 3, ["Lines and images branch out from the centre.", "It is a kind of map."]),
    mcq("1.1.5", "An initiative to address inclusivity in the workplace.", ["Provide sick workers with ARVs.",
        "Woolworths is donating food parcels to schools.", "Management should educate workers on the benefits of diversity in the workplace.",
        "Businesses should start recycling glass and paper."], 2, ["Inclusivity means including everyone.", "Which option is about diversity?"])]
WORDS = "gambling; shareholders; vision; potential market; mission; target market; flip chart; crime; data projector; directors"
q12 = [
    term("1.2.1", "… refers to where the business sees itself in the future.", ["vision"], ["It looks ahead.", "Not the mission."], marks=2),
    term("1.2.2", "A non-profit company's managers are called …", ["directors", "board of directors"],
         ["They manage a company.", "Not shareholders: a non-profit company has none."], marks=2),
    term("1.2.3", "Offering financial literacy to your workers is a possible initiative to address …", ["gambling"],
         ["A socio-economic issue about losing money.", "Betting and the lottery."], marks=2),
    term("1.2.4", "… can be used when presenting to a small group of people.", ["flip chart"], ["It needs no electricity.", "Large sheets of "
                                                                                                                      "paper on a stand."],
         marks=2),
    term("1.2.5", "The … is a specific group of customers at which a company aims to sell its products and services.", ["target market"],
         ["The business aims at them.", "Not the potential market."], marks=2)]
DESC = ["A technique used to look at the driving and restraining forces of a change.",
        "Part of middle management, the link between the top and lower levels of the team.",
        "The business should provide skills development programmes through learnerships.",
        "An expensive type of visual aid that requires the use of electricity.",
        "Shareholders' personal assets may be seized to pay for the debts of the business.",
        "The business should develop strategies to deal with stigma and discrimination.",
        "Shareholders may only lose the capital they invested to pay for the debts of the business.",
        "A technique used to make a choice by having a discussion in your head.",
        "Part of top management, the highest level of a hierarchy in a team.", "A cheap type of visual aid that does not require any electricity."]
q13 = [
    {"t": "match", "n": "1.3", "marks": 10, "q": "Choose a description from COLUMN B that matches a term in COLUMN A (1.3.1 Chief Executive "
     "Officer, 1.3.2 Initiative to address unemployment, 1.3.3 Limited liability, 1.3.4 Interactive whiteboard, 1.3.5 Force field analysis).",
     "clues": ["The CEO is top management.", "Limited liability: shareholders lose only what they invested."],
     "left": ["1.3.1 Chief Executive Officer", "1.3.2 Initiative to address unemployment", "1.3.3 Limited liability",
              "1.3.4 Interactive whiteboard", "1.3.5 Force field analysis"], "right": DESC, "a": [8, 2, 6, 3, 0], "each": 2,
     "heads": ["COLUMN A", "COLUMN B (A–J)"]}]

# ---- SECTION B, QUESTION 2: BUSINESS VENTURES, the question paper page 6 and the memo pages 9-12 ----
PS = ("Susan is marketing manager at Primax Stores. She made a presentation to the board of directors. She distributed hard copies of the "
      "sales figures to them before the start of her presentation.")
MP = ("Maria wants to start her new pizzeria business. She does not know where to start and friends advised her to draw up a business plan.")
q2 = [
    stmt("2.1", "Name any FOUR types of co-operatives.", 4,
         ["Housing co-operative", "Worker co-operative", "Agricultural co-operative", "Consumer co-operative", "Financial services co-operative"],
         ["Public company", "Close corporation", "Sole trader"], ["A co-operative is owned by its members.", "Housing, workers, farmers …"], 1),
    stmt("2.2", "Outline the characteristics of a sole trader.", 6,
         ["The owner can sell the business to anyone at any time.", "It is easy to establish, with no legal formalities.",
          "The owner has unlimited liability for the debts of the business.", "The business has no legal personality, so no continuity.",
          "Profit is added to the rest of the owner's taxable income."],
         ["The owner has limited liability for the business's debts.", "It must have at least seven shareholders.",
          "Its financial statements must be audited by law."],
         ["A sole trader is one owner.", "Who pays the debts?"], 2),
    sort("2.3", "Differentiate between a private company and a personal liability company.",
         ["Private company", "Personal liability company"],
         [("The name ends with (Pty) Ltd", 0), ("The directors are not personally liable for the debts of the business", 0),
          ("The name ends with Inc.", 1), ("The directors are personally liable for the debts of the business", 1)],
         ["Look at the name endings.", "Who is liable for the debts?"]),
    term("2.4.1", "Identify the visual aid that Susan used during her presentation.", ["hand-outs", "handouts", "hand outs", "handout"],
         ["She gave the directors copies before she started.", "Paper copies to hold."], marks=2),
    stmt("2.4.2", "Advise PS on the importance of graphs, diagrams, symbols and pictures.", 4,
         ["They help the audience see what you are talking about.", "Graphs present data in a form that is easy to understand.",
          "They make a presentation more interesting for the audience.", "They help to organise information more clearly."],
         ["They make the presentation longer and harder to follow.", "They replace the need to prepare.", "They hide the data from the audience."],
         ["Visual aids support the spoken word.", "What do they do for the audience?"], 2),
    stmt("2.5", "Discuss factors that must be considered when preparing for a verbal presentation.", 6,
         ["Write down the purpose of the presentation and list the objectives.", "Consider the audience: who they are and what they know.",
          "Prepare the structure: introduction, body and conclusion.", "Practise the presentation and time it.",
          "Visit the venue and check the equipment, with a back-up for load shedding."],
         ["Do not prepare, so the talk sounds natural.", "Ignore the audience's level of knowledge.", "Use as many slides as possible."],
         ["Purpose, audience, structure, practice, venue.", "Plan before you speak."], 2),
    stmt("2.6.1", "State any FOUR components of the business plan.", 4,
         ["Executive summary", "SWOT analysis", "Marketing plan", "Financial plan", "Operational plan"],
         ["The owner's bank statement", "A staff birthday list", "A customer complaints register"],
         ["A business plan describes the whole business.", "Summary, analysis, plans."], 1),
    stmt("2.7", "Describe the protocol for conducting research.", 6,
         ["The researcher must obtain consent from the participants before the interview.",
          "The researcher should not influence the opinions of the participants.",
          "Participants must be told the purpose of the interview.", "Information collected must be kept confidential.",
          "Research findings must be reported accurately and not used to mislead."],
         ["The researcher may share participants' names without asking.", "Participants must answer every question.",
          "Results may be changed to suit the business."],
         ["Protocol is the correct, ethical way of doing research.", "Consent, honesty, confidentiality."], 2),
    stmt("2.8", "Advise businesses on the importance of assessing needs and desires in identifying a business opportunity.", 4,
         ["Needs and desires are the key to successful business opportunities.", "Needs and desires guarantee a possible market.",
          "Unfulfilled needs or desires present a business opportunity.", "An entrepreneur can create a desire through advertising and marketing."],
         ["Needs and desires have nothing to do with business opportunities.", "A business should ignore what customers want.",
          "Fulfilled needs create the most opportunities."],
         ["What do customers want that they do not have?", "Unmet needs are opportunities."], 2)]

# ---- QUESTION 3: BUSINESS ROLES, the question paper page 7 and the memo pages 13-17 ----
SS = ("Sunshine Sweets want to change some of their products. The marketing team asked the employees to suggest new ideas aloud in a large "
      "group. The manager of SS also asked experts to make suggestions by means of a questionnaire. These ideas were used to inspire new "
      "thoughts.")
q3 = [
    stmt("3.1", "Name any FOUR steps of the problem-solving cycle.", 4,
         ["Identify the problem", "Define the problem", "Formulate a strategy", "Allocate resources", "Implement the strategy"],
         ["Ignore the problem", "Blame an employee", "Close the business"], ["The cycle starts with spotting the problem.",
                                                                              "Then plan, act and check."], 1),
    stmt("3.2", "Outline the advantages of creative thinking.", 6,
         ["Creative thinking improves the quality of solutions to business problems.", "Products and services can be marketed creatively.",
          "It motivates employees and improves their skills.", "It helps businesses respond to the threat of competition.",
          "New products and services can be designed to meet customers' changing needs."],
         ["It makes every employee do the same thing.", "It stops new ideas from being tested.", "It increases production costs every time."],
         ["New ideas give a business an edge.", "Solutions, marketing, staff, competition."], 2),
    stmt("3.3.1", "Identify the problem-solving techniques used by SS in the scenario above. Motivate your answer by quoting from the scenario.", 6,
         ["Brainstorming: 'The marketing team asked the employees to suggest new ideas aloud in a large group.'",
          "Delphi technique: 'The manager of SS also asked experts to make suggestions by means of a questionnaire.'"],
         ["Nominal group technique: 'The marketing team asked the employees to suggest new ideas aloud in a large group.'",
          "Mind-mapping: 'These ideas were used to inspire new thoughts.'",
          "Force field analysis: 'Sunshine Sweets want to change some of their products.'"],
         ["Ideas aloud in a group; experts by questionnaire.", "Name each technique with its quote."], 3),
    stmt("3.3.2", "Describe to SS how to apply ONE of the problem-solving techniques identified in QUESTION 3.3.1 above (brainstorming).", 6,
         ["The problem must be defined clearly.", "All ideas are written on a flip chart.",
          "The facilitator encourages everyone to take part and no-one criticises any suggestion.",
          "Similar ideas are grouped together.", "The group evaluates and rates the ideas, then plans to put the best into practice."],
         ["Criticise each idea as soon as it is suggested.", "Only the manager may suggest ideas.", "Choose the first idea without evaluating it."],
         ["Brainstorming generates many ideas first.", "Judge the ideas only at the end."], 2, after=["3.3.1"]),
    stmt("3.4", "Suggest ways in which creative business opportunities can realistically be implemented.", 4,
         ["There has to be a demand for the product or service.", "Develop a realistic plan with reasonable deadlines and resources.",
          "Give people in the business tasks and activities of the plan.", "Put control measures in place to check the plan is implemented."],
         ["Start without any plan.", "Ignore whether customers want the product.", "Never check whether the plan is working."],
         ["Is there a market for it?", "Plan, assign, control."], 2),
    stmt("3.5", "Elaborate on the meaning of interpersonal relationships in the workplace.", 4,
         ["A strong association among individuals working together.", "Team members share a special relationship.",
          "Team members build trust, openness, understanding and effective communication.",
          "Everyone in the business plays a role in achieving the business objectives."],
         ["Employees who never speak to each other.", "Relationships between the business and its competitors only.",
          "Each employee working alone without contact."],
         ["Inter means between people.", "Trust and communication."], 2),
    stmt("3.6(a)", "Define the term social responsibility.", 2,
         ["Individuals take responsibility for the effects of their behaviour and lifestyle on the environment and on others.",
          "Every individual and organisation can contribute towards the well-being of the community and the environment."],
         ["Making as much profit as possible, whatever the cost to others.", "Paying tax only.", "Ignoring the community's needs.",
          "Avoiding all contact with the public."],
         ["Responsibility towards society.", "Acting in the best interests of the environment and others."], 2),
    stmt("3.6(b)", "Give practical examples of social responsibility (business opportunities that serve the community).", 4,
         ["Home care services for senior citizens", "Online education programmes", "Catering and ready-made meals"],
         ["Selling stolen goods", "Dumping waste in a river", "Charging the poor higher prices"],
         ["Services that meet community needs.", "Care, education, food."], 2),
    stmt("3.7", "Recommend initiatives the business can take to address poverty as a socio-economic issue.", 4,
         ["Provide bursaries, learnerships or apprenticeships.", "Invest in young small and medium enterprises.",
          "Encourage entrepreneurial programmes for start-ups.", "Support the government's poverty alleviation programmes.",
          "Donate money or food parcels to local NGOs."],
         ["Cut wages to increase profit.", "Close the business's training programmes.", "Raise prices in poor communities."],
         ["Skills, jobs and support.", "How can a business help people earn?"], 2)]

# ---- QUESTION 4: MISCELLANEOUS TOPICS, the question paper pages 8-9 and the memo pages 17-21 ----
NETFLIX = ("Netflix is a popular American media services provider and production company founded in 1997. The marketing team of Netflix "
           "completed their environmental scanning and found the following:\n• Netflix is available in over 190 countries, giving it a "
           "global reach.\n• Netflix can partner with internet service providers to offer a combo service which will include both internet "
           "and Netflix subscriptions.\n• Streaming services such as Disney+ and Showmax compete for viewers' subscriptions.\n• Netflix still "
           "relies heavily on licensing agreements with studios to offer popular TV shows and movies.\n• To help the company diversify and "
           "attract more customers, it could explore video games and virtual reality.\n• Netflix has over 222 million subscribers worldwide, "
           "giving it a strong financial foundation and allows it to invest in more content.\n• Netflix does not show any traditional adverts "
           "on its platform, limiting its advertising income potential.\n• Online piracy impacts Netflix significantly, as users can access "
           "pirated content for free.")
LFF = ("Linda's Fashion Factory offers top international and national brands in fashion wear, sportswear, luggage and accessories at "
       "unbeatable prices. LFF realised that HIV/Aids impacts both their clients and their workers and decided that their business wants to "
       "be involved in CSR programmes.")
q4 = [
    stmt("4.1", "State any FOUR types of legal requirements of a business.", 4,
         ["Trading licences and permits", "Taxation regulations", "Registration", "The Basic Conditions of Employment Act",
          "The National Credit Act"],
         ["A logo design", "Office furniture", "A company song"], ["What does the law require of a business?", "Licences, tax, labour laws."], 1),
    stmt("4.2", "Outline factors that must be considered when designing a presentation.", 4,
         ["Use large, clear fonts that are easy to read.", "Limit each slide to five or six lines.", "Make sure the grammar is correct.",
          "Select a suitable background.", "Avoid long sentences and keep it simple."],
         ["Fill each slide with long paragraphs.", "Use tiny fonts to fit more in.", "Add as many fancy decorations as possible."],
         ["Slides must be easy to read.", "Keep it short and clear."], 2),
    sort("4.3.1", "Compile a SWOT analysis from the given scenario.", ["Strength", "Weakness", "Opportunity", "Threat"],
         [("Netflix is available in over 190 countries, giving it a global reach", 0),
          ("Netflix has over 222 million subscribers worldwide, giving it a strong financial foundation", 0),
          ("Netflix still relies heavily on licensing agreements with studios", 1),
          ("Netflix does not show traditional adverts, limiting its advertising income", 1),
          ("Netflix can partner with internet service providers to offer a combo service", 2),
          ("Netflix could explore video games and virtual reality to diversify", 2),
          ("Streaming services such as Disney+ and Showmax compete for viewers' subscriptions", 3),
          ("Online piracy lets users access content for free", 3)],
         ["Strengths and weaknesses are inside Netflix.", "Opportunities and threats come from outside."]),
    stmt("4.4", "Advise businesses on the advantages of a public company.", 4,
         ["The business has its own legal identity and can own assets.", "Shareholders can sell or transfer their shares freely.",
          "It is easy to raise funds for growth through the sale of shares.", "Shareholders have limited liability for the company's debts.",
          "There is no limit on the number of shareholders."],
         ["Shareholders are personally liable for all debts.", "Shares can never be transferred.", "It may have only one shareholder."],
         ["Public companies sell shares to the public.", "Identity, shares, funds, liability."], 2),
    stmt("4.5", "Elaborate on the meaning of creative thinking.", 4,
         ["The ability to think of original, varied and innovative ideas.", "It focuses on exploring ideas and generating possibilities.",
          "Thinking in a way that is unconventional and original.", "Producing new ideas and making them real."],
         ["Always doing things the way they were done before.", "Copying a competitor's ideas exactly.", "Refusing to consider new ideas."],
         ["Creative means new.", "Many possible answers."], 2),
    sort("4.6", "Distinguish between problem-solving and decision-making.", ["Decision-making", "Problem-solving"],
         [("The process of choosing from several alternatives", 0), ("Decisions are usually made by one person", 0),
          ("The process of finding a solution to a problem", 1), ("It usually involves a group or team", 1)],
         ["Deciding is choosing.", "Solving finds a solution."]),
    stmt("4.7", "Explain how businesses can use creative thinking to generate entrepreneurial opportunities.", 6,
         ["Design environments that stimulate creative thinking.", "Encourage staff to come up with new ideas and solutions.",
          "Make time for brainstorming sessions, for example regular workshops.",
          "Place suggestion boxes around the workplace and keep communication open.",
          "Train staff in creative problem-solving, mind-mapping and lateral thinking."],
         ["Punish employees who suggest new ideas.", "Close all communication channels.", "Never allow time for new ideas."],
         ["How can a business make new ideas happen?", "Environment, time, training."], 2),
    stmt("4.8.1", "Define the meaning of Corporate Social Responsibility.", 2,
         ["Businesses taking responsibility for their impact on society and the environment.",
          "A business makes sure its actions protect the environment and improve the quality of life of citizens."],
         ["Making the most profit regardless of society.", "Paying shareholders their dividends.", "Ignoring the community's needs.",
          "Selling products at the highest price."],
         ["Corporate means business.", "Responsibility towards society."], 2),
    stmt("4.8.2", "Recommend initiatives that can be used to address HIV/Aids as a socio-economic issue.", 4,
         ["Train counsellors to support infected and affected employees.",
          "Hold regular workshops and information sessions on the effects of HIV/Aids.",
          "Encourage employees to join HIV/Aids support groups.", "Support NGOs that work with people affected by HIV/Aids."],
         ["Dismiss employees who are HIV positive.", "Keep HIV/Aids information away from staff.", "Stop all medical aid for employees."],
         ["Support, education and prevention.", "Help workers and the community."], 2)]

# ---- SECTION C, QUESTION 5: the essay, the question paper page 10 and the memo pages 22-27 ----
Q5_STEM = ("A business plan is a plan to turn an idea into a workable plan. Entrepreneurs know the importance of a business plan when "
           "starting a business. It is of utmost importance to do proper market research and to determine who your competitors are so that "
           "the business can develop strategies to overcome competition.\n\nWrite an essay on the business plan in which you include the "
           "following aspects:\n• Outline the importance of a marketing plan and market research.\n• Explain the meaning of a marketing mix "
           "with specific reference to any FOUR of the 7 P's.\n• Explain the importance of a business plan.\n• Recommend strategies to "
           "overcome competition in the market.")
Q5_EX = ["For example, a new pizzeria shows its business plan to a bank to get a loan for its oven.",
         "For example, a corner café starts a loyalty card to keep its customers when a new chain store opens nearby."]
q5 = essay("5.7", [
    stmt("5.1", "Introduction: pick the TWO statements that introduce this essay on the business plan.", 2,
         ["Once an entrepreneur has identified a business opportunity, the next step is to turn the idea into a workable plan.",
          "A business plan is a written description of a prospective business.",
          "The business plan describes how the business will deal with threats and market its goods and services."],
         ["A business plan is only needed after the business closes.", "Market research is a waste of time.",
          "Competition has no effect on a new business."],
         ["An introduction says what the essay is about.", "Which cards say something true?"], 1),
    stmt("5.2", "Outline the importance of a marketing plan and market research.", 6,
         ["The marketing plan analyses the target market, customers and competition.",
          "The marketing plan guides the business on how to advertise and price its products.",
          "Market research helps the business understand more about customers' needs.",
          "Market research shows whether the target market is interested in the goods and services.",
          "Surveys, interviews and questionnaires are methods of market research."],
         ["The marketing plan sets the employees' salaries.", "Market research tells the owner how to pay tax."],
         ["Who are the customers and what do they want?", "Plan and research."], 2),
    stmt("5.3", "Explain the meaning of a marketing mix with specific reference to any FOUR of the 7 P's.", 8,
         ["Product: a description of the product, its appearance and usage, different from competitors' products.",
          "Price: the amount the consumer pays; it must cover costs and appeal to the target market.",
          "Place: where goods and services are sold or reached, e.g. direct selling or online shopping.",
          "Promotion: making the target market aware of the product, e.g. adverts, special offers and social media.",
          "People: the employees, managers and owners whose skills and attitudes affect sales."],
         ["Profit: the money the owner takes home each month.", "Pollution: the waste the business produces."],
         ["The 7 P's: product, price, place, promotion, people, process, physical environment.", "Name each P and explain it."], 2),
    stmt("5.4", "Explain the importance of a business plan.", 8,
         ["It helps entrepreneurs set goals and objectives.", "It can be used to attract investors and prospective employees.",
          "It guides the entrepreneur on the viability of the business idea.", "It helps identify problems that may arise and how to avoid them.",
          "It is essential when applying for financial assistance from investors or lenders.", Q5_EX[0]],
         ["A business plan stops the business from growing.", "A business plan is only for large companies."],
         ["Why plan before starting?", "Goals, investors, viability, problems, finance."], 2),
    stmt("5.5", "Recommend strategies to overcome competition in the market.", 6,
         ["Produce unique (differentiated) goods or services for the target market.",
          "Price goods and services lower than competitors' goods and services.",
          "Improve customer service and keep customers happy.", "Offer low-cost extras such as improved credit terms or loyalty schemes.",
          Q5_EX[1]],
         ["Copy the competitor's product exactly.", "Raise prices above the competitors' without improving quality."],
         ["What makes customers choose you?", "Unique, cheaper, better service."], 2),
    stmt("5.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["The business plan provides details on where the business would like to go with its idea and how it will get there.",
          "The business plan explains how the prospective business owner will obtain funding."],
         ["A business plan is not needed if the idea is good.", "Market research should be skipped.", "Competition can be ignored."],
         ["A conclusion sums up why it all matters.", "Which card would an entrepreneur agree with?"], 2),
], [("5.4", Q5_EX[0]), ("5.5", Q5_EX[1])], INSIGHT_CLUES)

# ---- QUESTION 6: the essay, the question paper page 10 and the memo pages 27-33 ----
Q6_STEM = ("Teamwork, when two or more people work together for a common goal, can be advantageous for any business. To set up a successful "
           "team, the manager needs to consider the criteria for successful team performance. Managers need to be aware of the factors that "
           "can influence team relationships and need to create an environment that enables teams to work effectively.\n\nWrite an essay on "
           "relationships and team performance in which you include the following aspects:\n• Outline the benefits of teamwork.\n• Explain "
           "any THREE criteria for successful team performance.\n• Describe any THREE factors that can influence team relationships.\n• "
           "Suggest ways in which businesses can create an environment that enables teams to work effectively.")
Q6_EX = ["For example, a mixed team of young and older shop assistants learns to respect each other's ways of serving customers.",
         "For example, a call centre sets clear weekly targets and holds a short team meeting every Monday."]
q6 = essay("6.7", [
    stmt("6.1", "Introduction: pick the TWO statements that introduce this essay on relationships and team performance.", 2,
         ["Successful teams communicate frequently and openly, and team members are flexible to ensure the team's success.",
          "Teamwork can be natural for some people, but difficult for others.",
          "Poor relationships in a team can create distress, anger and withdrawal."],
         ["Teams always perform worse than individuals.", "Team relationships have no effect on performance.",
          "Managers should never set up teams."],
         ["An introduction says what the essay is about.", "Which cards say something true?"], 1),
    stmt("6.2", "Outline the benefits of teamwork.", 6,
         ["The team achieves more than the individual.", "Good teamwork helps the business achieve its objectives.",
          "Teamwork improves effective communication.", "Team members learn from each other and grow.",
          "Teamwork promotes creativity and learning."],
         ["Teamwork always slows the business down.", "Team members compete instead of supporting each other.",
          "Teamwork lowers job satisfaction."],
         ["Together more is achieved.", "Communication, learning, objectives."], 2),
    stmt("6.3", "Explain any THREE criteria for successful team performance.", 8,
         ["Clear objectives and agreed goals: members who agree on goals are more committed.",
          "Interpersonal attitudes and behaviour: members support and motivate each other.",
          "Shared values and mutual respect: members respect each other's skills and act with integrity.",
          "Communication: open discussion leads to quick decisions and effective problem solving.",
          "Co-operation: members work together as a unit to achieve the team's objectives."],
         ["Secret goals: members do not know what the team must achieve.", "Each member works alone without telling the others."],
         ["What makes a team succeed?", "Goals, attitudes, respect, communication, co-operation."], 2),
    stmt("6.4", "Describe any THREE factors that can influence team relationships.", 8,
         ["Prejudice: a negative attitude towards a person based on differences such as culture.",
          "Discrimination: negative action against a person because of gender, race or religion.",
          "Diversity: including people of different backgrounds, genders and orientations.",
          "Beliefs: convictions tied to culture and religion that shape attitudes.",
          "Equity: fair, respectful and dignified treatment of every person.", Q6_EX[0]],
         ["The colour of the office walls.", "The brand of the team's computers."],
         ["Attitudes, actions and differences between people.", "Prejudice, discrimination, diversity, beliefs, equity."], 2),
    stmt("6.5", "Suggest ways in which businesses can create an environment that enables teams to work effectively.", 6,
         ["Make sure the team clearly understands the business objectives.", "Set ground rules for the team.",
          "Encourage trust, respect and co-operation among team members.", "Consider each employee's ideas as valuable.", Q6_EX[1]],
         ["Keep the team's goals secret.", "Allow members to ignore each other's ideas.", "Punish every mistake in front of the team."],
         ["What helps a team work well together?", "Objectives, rules, trust, respect."], 2),
    stmt("6.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["Successful teams communicate frequently and openly, so that the team succeeds overall.",
          "Businesses that build good team relationships and an enabling environment perform better."],
         ["Teams should not be used in business.", "Team relationships do not matter.", "Managers should ignore team performance."],
         ["A conclusion sums up why it all matters.", "Which card would a manager agree with?"], 2),
], [("6.4", Q6_EX[0]), ("6.5", Q6_EX[1])], INSIGHT_CLUES)

missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 10,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Complete the statements", "marks": 10,
     "lead": "Complete the following statements by using the word(s) provided in the list below.\n" + WORDS, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Column A and Column B", "marks": 10,
     "lead": "Choose a description from COLUMN B that matches a term in COLUMN A.", "items": q13},
    {"id": "2.1", "title": "Question 2", "kind": "Business ventures", "marks": 40,
     "lead": "QUESTION 2: BUSINESS VENTURES\n2.4 PRIMAX STORES (PS)\n" + PS + "\n2.6 MARIA'S PIZZA (MP)\n" + MP, "items": q2},
    {"id": "3.1", "title": "Question 3", "kind": "Business roles", "marks": 40,
     "lead": "QUESTION 3: BUSINESS ROLES\n3.3 SUNSHINE SWEETS (SS)\n" + SS, "items": q3},
    {"id": "4.1", "title": "Question 4", "kind": "Miscellaneous topics", "marks": 40,
     "lead": "QUESTION 4: MISCELLANEOUS TOPICS\n4.3 NETFLIX (N)\n" + NETFLIX + "\n4.8 LINDA'S FASHION FACTORY (LFF)\n" + LFF, "items": q4},
    {"id": "5", "title": "Question 5", "kind": "Essay: the business plan", "marks": 40,
     "lead": "Build the essay section by section, then see your insight.", "extract": "QUESTION 5: THE ESSAY\n\n" + Q5_STEM, "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Essay: relationships and teams", "marks": 40,
     "lead": "Build the essay section by section, then see your insight.", "extract": "QUESTION 6: THE ESSAY\n\n" + Q6_STEM, "items": q6},
]
P.finish(missions,
         {"subject": "Business Studies", "title": "Business Studies P2", "sitting": "November 2024", "total_marks": 150, "time": "2 hours"},
         [{"n": "3.3.1", "kind": "no_fit", "detail": "A technique with its quote is one card (3 marks: the memo's 2 + 1); the SWOT analysis "
                                                     "(4.3.1) and the 'differentiate/distinguish' parts (2.3, 4.6) are sorts."},
          {"n": "5.7", "kind": "no_fit", "detail": "Each essay plays as sections, one per memo heading, their facts scaled to sum to the memo's "
                                                   "cap of 32 (Question 5: 2 + 6 + 8 + 8 + 6 + 2 of the memo's 2 + 8 + 16 + 12 + 10 + 2; "
                                                   "Question 6: 2 + 6 + 8 + 8 + 6 + 2 of 2 + 10 + 12 + 12 + 12 + 2), then insight (8)."},
          {"n": "3.6(a)", "kind": "no_fit", "detail": "3.6 ('define social responsibility and give practical examples', 6) plays as two parts "
                                                      "with the memo's sub-maxima: the definition (2) and the examples (2 × 2)."}],
         {"1": 30, "2": 40, "3": 40, "4": 40, "5": 40, "6": 40}, 150, {"3.3.2": ["3.3.1"]}, "Sections A, B and C (the whole paper)",
         sections=[("Section A", 30, None, ["1"]), ("Section B", 80, 2, ["2", "3", "4"]), ("Section C", 40, 1, ["5", "6"])])
