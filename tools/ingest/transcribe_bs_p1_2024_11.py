"""Business Studies P1 Nov 2024, the whole paper (Sections A, B and C), hand-transcribed into the catalogue format (as if Claude had
produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks and memo points are the
paper's and the memo's own; the clues are ours. No API call: the transcription is the source, kept in git (out/ is not).

  python tools/ingest/transcribe_bs_p1_2024_11.py
  python tools/ingest/ingest.py "<...>/Business Studies P1 Nov 2024 Eng.pdf" "<...>/Business Studies P1 Nov 2024 MG Eng.pdf" --id bs-p1-2024-11 --from-json

The memo's shapes map as in Business Studies P1 Nov 2025 (transcribe_bs_p1_2025_11.py), with what that paper taught (2026-10-10):
  - the memo's marking instructions ("Mark the first TWO only", "No marks for ...", "Accept ... even if ...") are a rubric's `notes`,
    never bullets (a bullet is a point a learner earns);
  - a name and what goes with it ("Strategy (2) + Discussion (1)", "Component (Sub max 4) + Motivation (Sub max 2)") are two points,
    `worth` [2, 1]: the name alone earns its 2, the discussion or quote its 1; the second point's label is in brackets, which the
    marker never requires;
  - only an alternative answer's FIRST point starts with "OR" (each "OR" opens a new alternative, and only the best one counts);
  - in an essay the memo's "OPTION 1 ... OR ... OPTION 2" for one aspect is the same steps worded twice: each option-2 wording is an
    "ACCEPT:" of its option-1 step (an "OR" inside an essay would make the rest of the essay the alternative)."""
import json
from pathlib import Path

mcq = lambda n, q, opts, a, clues: {"t": "mcq", "n": n, "marks": 2, "q": q, "clues": clues, "opts": opts, "a": a}
term = lambda n, q, a, clues, marks=2: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a}
lst = lambda n, q, count, pool, clues: {"t": "list", "n": n, "marks": count, "q": q, "clues": clues, "count": count, "pool": pool}
pick = lambda n, q, opts, pool, clues: {"t": "pickn", "n": n, "marks": len(pool), "q": q, "clues": clues, "opts": opts, "pool": pool, "count": len(pool)}
match = lambda n, q, left, right, a, each, clues, **kw: {"t": "match", "n": n, "marks": len(left) * each, "q": q, "clues": clues, "left": left,
                                                         "right": right, "a": a, **({"each": each} if each > 1 else {}), **kw}


# notes: the memo's marking instructions that are NOT points: never scored, never shown. worth: each point's own marks where they differ.
def rub(n, q, marks, bullets, clues, each=None, notes=None, worth=None):
    r = {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets}
    if each:
        r["each"] = each
    if worth:
        r["worth"] = worth
    if notes:
        r["notes"] = notes
    return r


def sentences(text):
    """A scenario's sentences, as printed (each ends with a full stop)."""
    return [s.strip().rstrip(".") + "." for s in text.split(". ") if s.strip()]


QUOTE = "(Its motivation, quoted from the scenario:) "

# ---- Section A: Question 1, the question paper pages 3-5 and the memo page 7 ----
q11 = [
    mcq("1.1.1", "This Act prevents discrimination on the grounds of race, gender and disability in the workplace:",
        ["Consumer Protection Act (CPA), 2008 (Act 68 of 2008)", "Employment Equity Act (EEA), 1998 (Act 55 of 1998)",
         "Basic Conditions of Employment Act (BCEA), 1997 (Act 75 of 1997)", "Labour Relations Act (LRA), 1995 (Act 66 of 1995)"], 1,
        ["One Act protects consumers, one sets working hours and leave, one deals with unions and disputes.",
         "Which is left: the one about fair treatment of every group at work?"]),
    mcq("1.1.2", "Niemand Traders is experiencing a high employee turnover. This is classified as a/an ... in the SWOT analysis.",
        ["weakness", "threat", "opportunity", "strength"], 0,
        ["SWOT: strengths and weaknesses are inside the business; opportunities and threats come from outside.",
         "Is losing staff an inside or an outside problem? Good or bad?"]),
    mcq("1.1.3", "Mabasa Enterprise has ... control over suppliers who increase the prices of their products.",
        ["full", "no", "limited", "complete"], 2,
        ["A business can negotiate with suppliers or change them, but it cannot set their prices.", "So how much control does it have?"]),
    mcq("1.1.4", "The role of the interviewee during an interview is to ...",
        ["make the interviewer feel at ease.", "explain the purpose of the interview to the panel.", "prepare responses for possible questions.",
         "ask clarity-seeking questions about the position."], 3,
        ["Two options are the interviewer's job; one happens BEFORE the interview.", "What does a candidate do DURING the interview?"]),
    mcq("1.1.5", "Businesses utilise machinery and equipment optimally in the ... function.",
        ["purchasing", "production", "marketing", "administration"], 1,
        ["Which function turns inputs into goods?", "Machines and equipment are used most where things are made."]),
]
WORDS = "employer;  secondary;  placement;  backward vertical;  plan;  selection;  forward vertical;  act;  employee;  tertiary"
q12 = [
    term("1.2.1", "The ... has the right to embark on a legal strike as a remedy for grievances.", ["employee"],
         ["A strike and a lockout are the two sides' weapons in a dispute.", "Which side downs tools?"]),
    term("1.2.2", "Sizwe Bakery applied the ... integration strategy when they bought a wheat farm.", ["backward vertical"],
         ["Is the wheat farm before or after the bakery in the chain from raw material to customer?", "Two words from the list: a direction, then ... vertical."]),
    term("1.2.3", "Fazzel Hairdressing Salon operates in the ... sector as they specialise in the selling of hair products.", ["tertiary"],
         ["Primary takes from nature, secondary makes things, the third sector ...", "Selling to customers is a service."]),
    term("1.2.4", "The employee's qualifications and skills are matched with the requirements of the job during the ... procedure.", ["placement"],
         ["Selection chooses the person; what puts them in the right position?", "Skills matched with the job's requirements."]),
    term("1.2.5", "Monwa Plastics continuously revise their processes to improve the quality of their products. This is known as the ... step "
         "in the PDCA model.", ["act"], ["Plan, Do, Check, Act.", "Revising processes to improve them comes last."]),
]
COL_B = ["process of finding potential candidates for available vacancies",
         "large businesses may prevent effective training due to poor communication",
         "ensures that the features of goods satisfy a specific need",
         "provides protection to employees who become disabled due to a workplace accident",
         "practical training opportunities that lead to a recognised qualification",
         "process of determining a candidate's suitability for the position",
         "provides protection to employees who are unfairly dismissed in the workplace",
         "practical training opportunities for ongoing professional development",
         "large businesses can afford to put systems in place to prevent defects in products",
         "ensures that finished products meet the required standards"]
q13 = [match("1.3", "Choose a description from COLUMN B that matches a term in COLUMN A.",
             ["Learnership", "Compensation for Occupational Injuries and Diseases Amendment Act, 1997 (Act 61 of 1997)", "Recruitment",
              "Quality control", "Adequate financing and capacity"],
             COL_B, [4, 3, 0, 9, 8], 2,
             ["Several descriptions come in pairs: read the small words (a qualification or ongoing development; disabled or dismissed).",
              "Quality control checks what is already finished."])]
missions_a = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 10,
     "lead": "Various options are provided as possible answers to the following questions. Choose the answer.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Words from a list", "marks": 10,
     "lead": "Complete the following statements by using the word(s) provided in the list below.\n\n" + WORDS, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Matching columns", "marks": 10, "items": q13},
]

# ---- Section B: Question 2 (Business Environments), the question paper page 6 and the memo pages 8-12 ----
MM = ("Mondo Manufacturers specialise in the production of winter blankets. MM disposes of their chemical waste from the manufacturing "
      "process into the local river in order to save costs.")
LS = ("Lass Suppliers implemented the Broad-Based Black Economic Empowerment Act (BBBEE), 2003 (Act 53 of 2003). They promoted Sandile to a "
      "senior executive position to serve on their board of directors.")
q21 = [lst("2.1", "Name any TWO types of diversification strategies.", 2,
           [["Concentric diversification", "Concentric"], ["Horizontal diversification", "Horizontal"], ["Conglomerate diversification", "Conglomerate"]],
           ["Diversification adds new products or new markets.", "Three kinds: related products, new products for the same customers, unrelated products."])]
q22 = [rub("2.2", "Outline the advantages of intensive strategies.", 6, [
    "Increase in sales/income/profitability due to a variety of advertising campaigns.", "Regular sales to existing customers may increase.",
    "Gain customer loyalty through effective promotion campaigns.", "Improved service delivery may positively impact/increase sales.",
    "Eliminate competitors and dominate market prices.", "Decrease in price could influence customers to buy more products.",
    "Businesses can have more control over the prices of products/services.",
    "Enables the business to focus on markets/well-researched quality products that satisfy the needs of consumers.",
    "Increased market share reduces the business's vulnerability to actions of competitors.",
    "Any other relevant answer related to the advantages of intensive strategies."],
    ["Intensive strategies push harder with the products and markets a business already has.",
     "What does the business gain: sales, loyalty, market share, control over prices?"], each=2)]
q23 = [
    term("2.3.1", "Name the PESTLE factor that is applicable to MM in the scenario above.", ["Environmental", "Environmental factor", "Environment"],
         ["What is MM doing to the river?", "PESTLE: political, economic, social, technological, legal, environmental."]),
    rub("2.3.2", "Recommend ways in which MM can deal with the challenges posed by the PESTLE factor named in QUESTION 2.3.1.", 4, [
        "Chemicals/Ingredients should be clearly indicated on labels/packaging to inform customers about possible side effects/correct use of products.",
        "MM/Businesses implemented cost effective measures to dispose of waste.",
        "Implement recycling measures to prevent pollution of the environment/Use packaging that is re-usable/recyclable.",
        "Engage in environmentally sustainable practices such as the conservation/preservation of natural resources.",
        "Any other relevant answer related to ways in which MM/businesses can deal with the challenges posed by environmental as a PESTLE factor."],
        ["How could MM stop harming the river and the environment?", "Waste disposal, recycling, labelling, conserving resources."], each=2,
        notes=["Accept relevant facts even if the PESTLE factor was incorrectly identified as an answer in QUESTION 2.3.1."]),
]
q24 = [rub("2.4", "Discuss any TWO types of defensive strategies.", 6, [
    "Divestiture.",
    "(Divestiture, discussed:) disposing/selling some assets/divisions that are no longer profitable/productive; selling off divisions/product "
    "lines with slow growth potential; decreasing the number of shareholders by selling ownership; paying off debts by selling unproductive "
    "assets; withdrawing/divesting their investment share in another business.",
    "Retrenchment.",
    "(Retrenchment, discussed:) terminating employment contracts/letting go of employees for operational reasons/to reduce costs/expenses; "
    "decreasing the number of product lines/closing certain departments may result in some workers becoming redundant.",
    "Liquidation.",
    "(Liquidation, discussed:) selling all assets/bringing the business activities to an end to pay creditors due to lack of capital; selling "
    "the entire business in order to pay shareholders a fair price for their shares; allowing creditors to apply for forced liquidation in "
    "order to have their claims settled."],
    ["Defensive strategies protect a business that is struggling.", "Selling off parts, cutting staff, closing down: name each, then explain it."],
    worth=[2, 1, 2, 1, 2, 1],
    notes=["Mark the first TWO only (3 marks each: the strategy 2, its discussion 1). Any other relevant answer related to each type of "
           "defensive strategy is accepted."])]
q25 = [
    term("2.5.1", "Name the pillar of the Broad-Based Black Economic Empowerment Act (BBBEE), 2003 (Act 53 of 2003) applied by LS in the "
         "scenario above.", ["Management control", "Management and control"],
         ["Sandile now sits on the board of directors.", "BBBEE pillars: ownership, management control, skills development, ..."]),
    rub("2.5.2", "Describe the purpose of the Broad-Based Black Economic Empowerment Act (BBBEE), 2003 (Act 53 of 2003).", 4, [
        "BBBEE Act enables wealth to be spread more broadly across all population groups.",
        "Outlines areas that would give the government a platform for bringing equitable spread of wealth.",
        "Allows for the development of Codes of Good Practice.",
        "Empowers the Minister to issue Codes of Good Practice and publish transformation charters.",
        "Establishes the Black Economic Empowerment Advisory Council, which addresses matters related to black empowerment.",
        "Creates capacity within the broader economic landscape at all levels through the implementation of the BBBEE pillars.",
        "BBBEE Act aims at targeting inequality in the South African economy.",
        "Increases the number of black people that manage/control South African businesses.",
        "Any other relevant answer related to the purpose of the BBBEE Act."],
        ["BBBEE aims to spread the economy's wealth more broadly.", "Codes of Good Practice, an advisory council, more black people in control."], each=2),
]
q26 = [rub("2.6", "Explain ways in which businesses can comply with the Consumer Protection Act (CPA), 2008 (Act 68 of 2008).", 4, [
    "Disclose prices of all products on sale.", "Provide/Conduct adequate training to staff/stakeholders on the CPA.",
    "All agreements must provide for a five-day cooling off period.", "Ensure that goods/services offered are standardised/of the same quality.",
    "Comply with the requirements regarding promotional competitions.",
    "Comply with requirements regarding the display of information on labels/packaging.",
    "Display the name of the business on all business documents, such as invoices/contracts.",
    "Bundling of goods/services should benefit consumers, such as offering a cell phone and a tablet at a special price.",
    "Implement measures that will facilitate complaints by using suggestion boxes.",
    "Any other relevant answer related to ways in which businesses can comply with the CPA."],
    ["The CPA protects people who buy goods and services.", "Prices, labels, cooling-off periods, trained staff, complaints."], each=2)]
q27 = [rub("2.7", "Discuss the impact of the Labour Relations Act (LRA), 1995 (Act 66 of 1995) on businesses.", 6, [
    "Positive: promotes a healthy relationship between the employer and employees.",
    "Positive: protects the rights of businesses in labour relations issues.",
    "Positive: labour disputes are settled quicker and are less expensive.",
    "Positive: workplace forums can add value to businesses if it functions properly.",
    "Positive: protects employers who embark on lawful lockouts when negotiations between parties fail.",
    "Positive: LRA provides for the principles of collective bargaining and puts structures in place with which disputes in the workplace can be settled.",
    "Positive: provides sound dispute resolution processes through consensus between organised labour, businesses, and the state.",
    "Positive: provides specific guidelines for employers on correct and fair disciplinary procedures.",
    "Positive: employers and employees have guidelines regarding correct and fair dismissal procedures.",
    "Positive: provides a mechanism/framework such as statutory councils/collective bargaining/CCMA.",
    "Positive: employers are entitled to compensation from the Labour Court if they suffered damages as a result of unprotected strikes.",
    "Negative: reduced global competitiveness due to lower productivity.",
    "Negative: productivity may decrease if employees are allowed to participate in the activities of trade unions during work time.",
    "Negative: costs of labour increases because of legal strikes.", "Negative: employers may not get a court interdict to stop a strike.",
    "Negative: employers may have to disclose information about workplace issues to union representatives that could be the core of their "
    "competitive advantage.",
    "Negative: employers may not dismiss employees at will, as procedures have to be followed.",
    "Negative: many employees take advantage of the right to strike without acknowledging their responsibilities.",
    "Negative: many employees and employers do not understand/respect the Labour Relations Act.",
    "Negative: strike actions always result in loss of production for which employers may not claim.",
    "Negative: some trade unions may not promote the mandate of their members but embark on industrial action, which is harmful to labour "
    "relations between employers and employees.",
    "Negative: some businesses may feel that the LRA gives employees too much power as it creates lengthy procedures such as consulting with "
    "workplace forums.",
    "Negative: labour disputes and bargaining council processes become disruptive/time-consuming and can lead to a decrease in productivity/"
    "profitability in businesses.",
    "Any other relevant answer related to the positive and/or negative impact of the LRA on businesses."],
    ["The LRA deals with unions, strikes, lockouts, disputes and dismissals.", "Impact can be positive, negative, or both: say what happens, then why."],
    each=2)]
q28 = [rub("2.8", "Advise businesses on the strategic management process.", 4, [
    "Have a clear vision/mission statement/measurable/realistic objective in place.",
    "Identify opportunities/weaknesses/strengths/threats by conducting environmental scanning/situational analysis.",
    "Tools available for environmental scanning may include a SWOT analysis/Porter's Five Forces model/PESTLE analysis/industrial analysis tools.",
    "Formulate alternative strategies to respond to the challenges.",
    "Develop (an) action plan(s), including the tasks to be done/deadlines to be met/resources to be procured.",
    "Implement selected strategies by communicating it to all stakeholders/organising business resources/motivating staff.",
    "Continuously evaluate/monitor/measure strategies in order to take corrective action.",
    "Any other relevant answer related to the strategic management process.",
    "OR — (option 2) Review/Analyse/Re-examine their vision/mission statement.",
    "(option 2) Conduct an environmental analysis using models such as SWOT/PESTLE/Porter's Five Forces.",
    "(option 2) Formulate a strategy, such as defensive/retrenchment strategy.",
    "(option 2) Implement a strategy, using a template such as an action plan.",
    "(option 2) Control/Evaluate/Monitor the implemented strategy to identify gaps/deviations in implementation.",
    "(option 2) Take corrective action to ensure goals/objectives are met."],
    ["It starts with where the business wants to go.", "Vision, scan the environment, formulate, implement, evaluate."], each=2)]
missions_q2 = [
    {"id": "2.1", "title": "Question 2.1", "kind": "Diversification", "marks": 2, "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Intensive strategies", "marks": 6, "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "The PESTLE analysis", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "MONDO MANUFACTURERS (MM)\n\n" + MM, "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Defensive strategies", "marks": 6, "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "BBBEE", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "LASS SUPPLIERS (LS)\n\n" + LS, "items": q25},
    {"id": "2.6", "title": "Question 2.6", "kind": "Consumer Protection Act", "marks": 4, "items": q26},
    {"id": "2.7", "title": "Question 2.7", "kind": "Labour Relations Act", "marks": 6, "items": q27},
    {"id": "2.8", "title": "Question 2.8", "kind": "Strategic management", "marks": 4, "items": q28},
]

# ---- Section B: Question 3 (Business Operations), the question paper page 7 and the memo pages 13-16 ----
TL = ("Tobbi Logistics drafted an employment contract for Thabo, a newly appointed transport supervisor. Management explained the terms and "
      "conditions of the employment contract to him. Thabo was given an opportunity to read the contract before signing it. TL also highlighted "
      "the reasons why an employment contract could be terminated.")
ML = ("Moosa Limited sells storage containers to small businesses. ML continuously updates their bookkeeping records to ensure that their tax "
      "payment to the South African Revenue Services (SARS) is timeous and accurate.")
q31 = [lst("3.1", "State any FOUR sources of internal recruitment.", 4,
           [["Internal e-mails", "Internal emails", "E-mails", "Emails", "Intranet", "Websites to staff", "Web sites to staff"],
            ["Word of mouth", "Staff meetings"], ["Business newsletter", "Newsletters", "Circulars to staff", "Circulars"],
            ["Internal referrals", "Management referrals", "Referrals"], ["Notice board of the business", "Notice board", "Noticeboard"],
            ["Internal bulletins", "Bulletins"], ["Recommendation of current employees", "Recommendations from employees", "Recommendations"],
            ["Head hunting within the business", "Head hunting", "Headhunting", "Organisational database"]],
           ["Internal recruitment looks for candidates among the people already working there.", "How would staff hear about a vacancy?"])]
q32 = [rub("3.2", "Outline the role of the interviewer before the interview.", 4, [
    "Book and prepare the venue for the interview.", "Inform all shortlisted candidates about the date and place of the interview.",
    "Set the interview date and ensure that all interviews take place on the same date, if possible.",
    "Notify all panel members conducting the interview about the date and place of the interview.",
    "The interviewer should develop a core set of questions based on the skills/knowledge/ability required.",
    "Check/read the application/verify the CV of every candidate for anything that may need to be explained.",
    "Plan the programme for the interview and determine the time that should be allocated to each candidate.",
    "Any other relevant answer related to the role of the interviewer before the interview."],
    ["Before the interview: arrangements and preparation.", "Venue, dates, candidates, the panel, questions, CVs."], each=2)]
q33 = [
    pick("3.3.1", "Quote TWO legal requirements of an employment contract from the scenario above.", sentences(TL), [1, 2],
         ["A legal requirement protects both sides when the contract is signed.", "What did TL make sure Thabo understood before he signed?"]),
    rub("3.3.2", "Advise businesses on the reasons for the termination of an employment contract.", 4, [
        "The employer may dismiss an employee for a valid reason(s) such as unsatisfactory job performance/misconduct.",
        "Employer may no longer have work for redundant employees/cannot fulfil the contract/is restructuring.",
        "The employer may retrench some employees due to insolvency/may not be able to pay the employees.",
        "Employees may decide to leave/resign voluntarily for better job opportunities.",
        "An employee may have reached the pre-determined age for retirement.", "Incapacity of an employee to work due to illness/injuries.",
        "By a mutual agreement between the employer and employee.", "The duration of the employment contract expires/comes to an end.",
        "Any other relevant answer related to the reasons for the termination of an employment contract."],
        ["A contract can end because of the employer, the employee, or time.", "Dismissal, retrenchment, resignation, retirement ..."], each=2),
]
q34 = [rub("3.4", "Discuss the implications of the Employment Equity Act (EEA), 1998 (Act 55 of 1998) on the human resources function.", 6, [
    "Offer equal pay for work of equal value.", "Compile employment equity plans that indicate how they will implement affirmative action.",
    "Ensures that affirmative action promotes diversity in the workplace.",
    "The human resources manager must treat employees fairly and promote/provide equal opportunities in the workplace.",
    "Retrain/Develop/Train designated groups through skills development programmes.",
    "Define the appointment process clearly to ensure all parties are well informed.",
    "Display a summary of the Act where employees can clearly see it/have access to it.",
    "Assign a manager to ensure that the employment equity plan will be implemented/regularly monitored.",
    "Report to the Department of Labour on the progress in the implementation of the equity plan.",
    "Conduct medical/psychological tests fairly to employees/when deemed necessary.",
    "Ensures that the workplace represents the demographics of the country at all levels.",
    "Restructure/Analyse current employment policies/practices/procedures to accommodate designated groups.",
    "Any other relevant answer related to the implications of the EEA on the human resources function."],
    ["The EEA is about fair treatment and fair representation at work.", "What must the HR manager now do: plans, reports, training, fair pay?"], each=2)]
q35 = [rub("3.5", "Outline the benefits of a good quality management system.", 4, [
    "Effective customer services are rendered, resulting in increased customer satisfaction.", "Time and resources are used efficiently.",
    "Productivity increases through proper time management/using high quality resources.",
    "Products/Services are constantly improved resulting in increased levels of customer satisfaction.",
    "Vision/Mission/Business goals may be achieved.", "A business has a competitive advantage over its competitors.",
    "Regular training will continuously improve the quality of employees' skills/knowledge.",
    "Employers and employees will have a healthy working relationship resulting in happy/productive workers.",
    "Increased market share/Financial sustainability as more customers improves profitability.",
    "Improves business image as there are less defects/returns.",
    "Any other relevant answer related to the benefits of a good quality management system."],
    ["A system that keeps quality high helps customers, staff and profits.", "Each point: a benefit, then what it leads to."], each=2)]
q36 = [
    term("3.6.1", "Identify the business function that is applicable to ML in the scenario above.",
         ["Financial function", "Financial", "Finance function", "Finance"],
         ["Bookkeeping records and tax payments belong to which function?", "Money in, money out, money owed to SARS."]),
    rub("3.6.2", "Explain other quality indicators of the business function identified in QUESTION 3.6.1.", 4, [
        "Obtain capital from the most suitable/available/reliable sources.", "Negotiate better interest rates in order to keep financial cost down.",
        "Draw up budgets to ensure sufficient application of monetary resources.", "Analyse strategies to increase profitability.",
        "Invest surplus funds to create sources of passive income.", "Implement financial control measures/systems to prevent fraud.",
        "Implement credit granting/debt collecting policies to monitor cash flow.", "Draw up accurate financial statements timeously/regularly.",
        "Accurately analyse and interpret financial information.", "Invest in strategies that will assist the business to remain profitable.",
        "Avoid over/under-capitalisation so that financial resources will be utilised effectively.",
        "Any other relevant answer related to other quality indicators of the financial function."],
        ["How would you SEE that a finance function is working well?", "Capital, interest rates, budgets, investments, controls, statements."], each=2,
        notes=["Do not award marks for a response that is quoted from the scenario.",
               "Accept relevant facts even if the financial function was incorrectly identified as an answer in QUESTION 3.6.1 (the memo prints 3.6.2)."]),
]
q37 = [rub("3.7", "Discuss the impact of total client/customer satisfaction as a total quality management (TQM) element on large businesses.", 6, [
    "Positive: large businesses use market research/customer surveys to measure/monitor customer satisfaction/reaction time to changing "
    "consumer demand/analyse customers' needs.",
    "Positive: continuously promote a positive business image.",
    "Positive: may achieve a state of total client/customer satisfaction, if businesses follow sound business practices that incorporates all stakeholders.",
    "Positive: strive to understand/fulfil customer expectations by aligning cross-functional teams across critical processes.",
    "Positive: ensures that cross-functional teams understand their core competencies and develop/strengthen it.",
    "Positive: may lead to higher customer retention/loyalty and businesses may be able to charge higher prices.",
    "Positive: large businesses may be able to gain access to the global market.", "Positive: may lead to increased competitiveness/profitability.",
    "Negative: large businesses that become complacent with the existing customer satisfaction/target market may experience limited long term "
    "growth potential.",
    "Negative: employees who seldom come into contact with customers often do not have a clear idea of what will satisfy their needs.",
    "Negative: monopolistic businesses have an increased bargaining power so they do not necessarily have to please customers.",
    "Negative: not all employees may be involved/committed to total client/customer satisfaction.",
    "Any other relevant answer related to the positive and/or negative impact of total client/customer satisfaction as a TQM element on large businesses."],
    ["Total client satisfaction: knowing what customers need and meeting it.", "The impact on a large business can be positive, negative, or both."],
    each=2)]
q38 = [rub("3.8", "Recommend ways in which total quality management (TQM) can reduce the cost of quality.", 4, [
    "Introduce quality circles to discuss ways of improving the quality of their work/workmanship.",
    "Schedule activities to eliminate duplication of tasks.", "Share responsibilities for quality output amongst management and workers.",
    "Train employees at all levels, so that everyone understands their roles in quality management.",
    "Develop work systems that empower employees to find new ways of improving quality.",
    "Work closely with suppliers to improve the quality of raw materials/inputs.",
    "Improve communication about the quality challenges/deviations, so that everyone can learn from past experiences.",
    "Reduce investment on expensive, but ineffective inspection procedures in the production process.",
    "Implement pro-active maintenance programmes for equipment/machinery to reduce/eliminate breakdowns.",
    "Any other relevant answer related to ways in which TQM can reduce the cost of quality."],
    ["The cost of quality: inspections, waste, rework, breakdowns.", "Quality circles, training, suppliers, maintenance, sharing responsibility."], each=2)]
missions_q3 = [
    {"id": "3.1", "title": "Question 3.1", "kind": "Internal recruitment", "marks": 4, "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "The interviewer", "marks": 4, "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Employment contract", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "TOBBI LOGISTICS (TL)\n\n" + TL, "items": q33},
    {"id": "3.4", "title": "Question 3.4", "kind": "Employment Equity Act", "marks": 6, "items": q34},
    {"id": "3.5", "title": "Question 3.5", "kind": "Quality management", "marks": 4, "items": q35},
    {"id": "3.6", "title": "Question 3.6", "kind": "The financial function", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "MOOSA LIMITED (ML)\n\n" + ML, "items": q36},
    {"id": "3.7", "title": "Question 3.7", "kind": "Client satisfaction", "marks": 6, "items": q37},
    {"id": "3.8", "title": "Question 3.8", "kind": "Cost of quality", "marks": 4, "items": q38},
]

# ---- Section B: Question 4 (Miscellaneous topics), the question paper page 8 and the memo pages 17-20 ----
SB = ("Shoe Boutique implemented a strategy aimed at improving their customer service due to a decrease in sales. The management of SB evaluated "
      "if their strategy had been effective. SB examined the underlying basis of their strategy throughout the implementation process. They also "
      "analysed the impact of the implemented strategy on their internal and external environments.")
MC = ("Mphemba Construction compiled a job analysis for the vacant position of a project manager. MC indicated that applicants must have a "
      "diploma in construction. The successful candidate will compile progress reports on assigned projects.")
q41 = [lst("4.1", "Name any FOUR provisions of the Basic Conditions of Employment Act (BCEA), 1997 (Act 75 of 1997).", 4,
           [["Regulation of working time", "Working time", "Working hours", "Ordinary hours of work", "Hours of work", "Overtime", "Meal intervals",
             "Rest periods", "Sunday work", "Public holidays"],
            ["Leave", "Annual leave", "Sick leave", "Family responsibility leave", "Maternity leave", "Paternity leave", "Parental leave"],
            ["Particulars of employment and remuneration", "Particulars of employment", "Remuneration"],
            ["Termination of employment", "Termination"],
            ["Prohibition of employment of children and forced labour", "Prohibition of child labour", "Child labour", "Forced labour"]],
           ["The BCEA sets the minimum conditions of employment.", "Working time, leave, pay details, ending employment, child labour."])]
q42 = [rub("4.2", "Outline the rights of consumers in terms of the National Credit Act (NCA), 2005 (Act 34 of 2005).", 6, [
    "Apply for credit and to be free from discrimination.", "Obtain reasons for credit being refused.",
    "Receive pre-agreement documentation/credit quote that is valid for 7 days before concluding any credit transaction.",
    "Fair and responsible marketing by the credit provider.",
    "Surrender/Return goods to the credit provider in order to settle the outstanding amount/debt.",
    "Apply for debt review/counselling if the consumers cannot afford to repay their debts.",
    "Receive information in plain and understandable language.", "Receive documents/statements as required by the Act.",
    "Access and challenge credit records and information.", "Receive protection of their personal information.",
    "Receive protection from being held accountable for the use of their credit facility after they reported the loss/theft.",
    "Refuse a credit limit increase.", "Any other relevant answer related to the rights of consumers in terms of the NCA."],
    ["The NCA protects people who borrow money or buy on credit.", "Consumers have a right to ...: apply, get reasons, get information, be protected."],
    each=2)]
q43 = [
    pick("4.3.1", "Quote TWO steps in strategy evaluation implemented by SB from the scenario above.", sentences(SB), [2, 3],
         ["Which sentences describe how SB checked its strategy?", "The first sentences only set the scene."]),
    rub("4.3.2", "Explain other steps in strategy evaluation.", 4, [
        "Look forward and backwards into the implementation process.", "Compare the expected performance with the actual performance.",
        "Determine the reasons for deviations and analyse these reasons.", "Take corrective action so that deviations may be corrected.",
        "Set specific dates for control and follow up.", "Draw up a table of the advantages and disadvantages of a strategy.",
        "Decide on the desired outcome as envisaged/expected when strategies were implemented.",
        "Any other relevant answer related to other steps in strategy evaluation."],
        ["Evaluation compares what was planned with what happened.", "Deviations, corrective action, dates for follow-up."], each=2,
        notes=["Accept steps in any order.", "Do not award marks for responses that were quoted in QUESTION 4.3.1."]),
]
q44 = [rub("4.4", "Advise businesses on how they could apply the power of suppliers as a force of Porter's Five Forces model to analyse their "
           "position in the market environment.", 4, [
    "Assess the power of the suppliers in influencing prices.",
    "Suppliers that deliver high quality/unique/scarce product may have power over the business.",
    "The more powerful the suppliers, the less control the business has over them.",
    "The smaller the number of suppliers, the more powerful they may be as the choice of suppliers may be limited.",
    "Identify the kind of power suppliers' have in terms of the quality of products/services/reliability/ability to make prompt deliveries.",
    "Any other relevant answer related to how businesses could apply power of suppliers as a force of Porter's Five Forces model to analyse "
    "their position in the market environment."],
    ["Suppliers have power when a business depends on them.", "Prices, quality, how many suppliers there are, reliability."], each=2)]
q45 = [lst("4.5", "State any FOUR aspects that should be included in an employment contract.", 4,
           [["Personal details of the employee", "Personal details", "Employee details"],
            ["Details of the business", "Details of the employer", "Name and address of the employer", "Employer details"],
            ["Job title", "Position"], ["Job description", "Duties", "Responsibilities", "Working conditions"],
            ["Job specification", "Formal qualifications", "Qualifications"],
            ["Date of employment", "Commencement of employment", "Starting date"],
            ["Place of work", "Place where the employee will spend most working time", "Workplace"],
            ["Hours of work", "Working hours", "Normal time and overtime", "Overtime"],
            ["Remuneration", "Salary", "Wages", "Weekly or monthly pay"], ["Benefits", "Fringe benefits", "Perks", "Allowances"],
            ["Leave", "Sick leave", "Maternity leave", "Annual leave", "Adoption leave"], ["Employee deductions", "Deductions"],
            ["Duration of the employment contract", "Period of employment", "Details of termination", "Expiry date of the employment contract"],
            ["Probation period", "Probation"], ["Signatures of both the employer and employee", "Signatures"],
            ["List of documents that form part of the contract", "Code of conduct", "Code of ethics", "Appointment letter"],
            ["Disciplinary policy", "Disciplinary procedure", "Rules"]],
           ["An employment contract sets out who, what, where, when and for how much.", "The two parties, the job, pay, hours, leave, signatures."])]
q46 = [rub("4.6", "Identify TWO components of a job analysis used by MC. Motivate your answer by quoting from the scenario above.", 6, [
    "Job specification.", QUOTE + "'MC indicated that applicants must have a diploma in construction.'",
    "Job description.", QUOTE + "'The successful candidate will compile progress reports on assigned projects.'"],
    ["A job analysis has two parts: one describes the PERSON the job needs, one describes the JOB.",
     "Which sentence asks for a qualification? Which one lists a duty?"],
    worth=[2, 1, 2, 1],
    notes=["Mark the first TWO only. Award marks for the components even if the motivations are incomplete; no marks for a motivation if its "
           "component is wrong. Accept responses in any order."])]
q47 = [rub("4.7", "Explain the role of quality circles as part of continuous improvement to processes and systems.", 6, [
    "Solve problems related to quality and implement improvements.", "Investigate problems and suggest solutions to management.",
    "Ensure that there is no duplication of activities/tasks in the workplace.",
    "Make suggestions for improving processes and systems in the workplace.",
    "Improve the quality of products/services/productivity through regular reviews of quality processes.",
    "Monitor/Reinforce strategies to improve the smooth running of business operations.",
    "Increase employees' morale/motivation to boost the team spirit in achieving organisational goals.",
    "Contribute towards the improvement and development of the organisation.",
    "Reduce costs of redundancy and wasteful efforts in the long run.", "Increase the demand for products/services of the business.",
    "Create harmony and high performance in the workplace.", "Build a healthy workplace relationship between the employer and employee.",
    "Improve employees' loyalty/commitment to the organisational goals.", "Improve employees' communication at all levels of the business.",
    "Develop a positive attitude/sense of involvement in decision-making processes of the services offered.",
    "Any other relevant answer related to the role of quality circles as part of continuous improvement to processes and systems."],
    ["A quality circle is a small group of workers who meet about quality.", "What do they find, suggest and improve?"], each=2)]
q48 = [rub("4.8", "Advise businesses on the quality indicators of the general management function.", 4, [
    "Develop/Implement/Monitor effective strategic plans.",
    "Efficient organisation/allocation of business resources to provide for the successful achievement of long-term and short-term plans.",
    "Structured standards and norms should be in place so that control mechanisms can be implemented.",
    "Learn about/understand changes in the business environment on an on-going basis.",
    "Effectively communicate shared vision, mission and values.", "Set direction and establish priorities for their business.",
    "Be prepared to set an example of the behaviour that is expected from employees in terms of ethics as well as productivity.",
    "Be proactive and always seeks to improve competitive advantage over competitors.",
    "Ensure that all departments/the business meet their deadlines/targets.",
    "Any other relevant answer related to the quality indicators of the general management function."],
    ["General management sets the direction for the whole business.", "Plans, resources, standards, communication, setting an example, deadlines."],
    each=2)]
missions_q4 = [
    {"id": "4.1", "title": "Question 4.1", "kind": "The BCEA", "marks": 4, "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "National Credit Act", "marks": 6, "items": q42},
    {"id": "4.3", "title": "Question 4.3", "kind": "Strategy evaluation", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "SHOE BOUTIQUE (SB)\n\n" + SB, "items": q43},
    {"id": "4.4", "title": "Question 4.4", "kind": "Power of suppliers", "marks": 4, "items": q44},
    {"id": "4.5", "title": "Question 4.5", "kind": "Employment contract", "marks": 4, "items": q45},
    {"id": "4.6", "title": "Question 4.6", "kind": "Job analysis", "marks": 6,
     "lead": "Read the scenario below and answer the question that follows.", "extract": "MPHEMBA CONSTRUCTION (MC)\n\n" + MC,
     "table": {"title": "Use the table below as a GUIDE to answer QUESTION 4.6.", "head": ["COMPONENTS OF A JOB ANALYSIS", "MOTIVATIONS"],
               "rows": [["1.", ""], ["2.", ""]]}, "items": q46},
    {"id": "4.7", "title": "Question 4.7", "kind": "Quality circles", "marks": 6, "items": q47},
    {"id": "4.8", "title": "Question 4.8", "kind": "General management quality", "marks": 4, "items": q48},
]

# ---- Section C: the essays (answer any ONE), the question paper page 9 and the memo pages 21-28 ----
# Each essay is one rubric part (as printed: one question of 40): the memo's points under its own headings and sub-maxima (facts
# capped at 32), and insight (8). Every point earns 1 here, as in the Nov 2025 essays: the keyword stand-in cannot judge sub-maxima,
# repetition or insight, so an essay's mark waits for model marking.
INSIGHT = ["Insight (8), 2 each: Layout (an introduction, paragraphs and a conclusion, the words INTRODUCTION and CONCLUSION stated and "
           "explained); Analysis and interpretation (all headings addressed; interpreted correctly); Synthesis (only relevant facts); "
           "Originality (an example in any TWO of the four aspects, based on recent information, current trends and developments, not "
           "older than two years)."]
ESSAY_NOTES = ["Facts are capped at 32 of the 40; no marks for content repeated from the introduction or the conclusion."]
q5 = [rub("5", "The basic aim of the Skills Development Act (SDA), 1998 (Act 97 of 1998) is to expand on the knowledge and competencies of the "
          "labour force. SETAs were established to facilitate the implementation of the SDA. Businesses are expected to oblige with this Act and "
          "be fully conversant with its requirements.\n\nWrite an essay on the Skills Development Act in which you include the following aspects:\n"
          "• Outline the role of SETAs in supporting the Skills Development Act.\n• Explain the purpose of the Skills Development Act.\n"
          "• Discuss the impact of the Skills Development Act on businesses.\n• Recommend ways in which businesses can comply with this Act.", 40, [
    "Introduction (any 2 x 1): a SETA is a vocational skills training organisation that identifies skills shortages that are needed in "
    "different industries; the Skills Development Act was introduced to redress the imbalances of the past; the SDA enables South Africans to "
    "gain access to skills training opportunities that have long-term benefits; businesses that comply with the SDA are able to create a good "
    "public image and address skills shortages in the South African workplace.",
    "Role of SETAs (max 12, 2 each): report to the Director General.",
    "SETAs: promote and establish learnerships.", "SETAs: collect levies and pay out grants as required.",
    "SETAs: provide accreditation for skills development facilitators.", "SETAs: register learnership agreements/learning programmes.",
    "SETAs: approve workplace skills plans and annual training reports.", "SETAs: monitor/evaluate the actual training by service providers.",
    "SETAs: allocate grants to employers/education/training providers.", "SETAs: oversee training in different sectors of the South African economy.",
    "SETAs: develop sector skills plans in line with the National Skills Development Strategy.",
    "SETAs: draw up skills development plans for their specific economic sectors.",
    "SETAs: provide training material/programmes for skills development facilitators.",
    "SETAs: pay out grants to businesses that are complying with the requirements of the Skills Development Act.",
    "SETAs: identify suitable workplaces for practical work experience.",
    "Purpose of the SDA (max 10, 2 each): develops the skills of people in South Africa in order to improve productivity.",
    "Purpose: invests in education and training of the South African workforce.",
    "Purpose: improves the chances of getting a job for previously disadvantaged people.",
    "Purpose: encourages workers to participate in learning programmes.", "Purpose: redresses imbalances of the past through education and training.",
    "Purpose: encourages businesses to improve the skills of their workers.",
    "Purpose: provides the systematic implementation of strategies on a national, sector and workplace basis.",
    "Impact of the SDA (max 12, 2 each), positive: increases the number of skilled employees in areas where these skills are scarce.",
    "Impact, positive: trains employees to improve productivity in the workplace.", "Impact, positive: businesses could become globally more competitive.",
    "Impact, positive: on-going skills development/learning/acquisition of new skills are encouraged to sustain the improvement of skills development.",
    "Impact, positive: increases investment in education and training in the labour market.",
    "Impact, positive: increases the return on investment in education and training.",
    "Impact, positive: improves employment opportunities and labour movement.", "Impact, positive: self-employment and entrepreneurship are promoted.",
    "Impact, positive: workplace discrimination can be addressed through training.",
    "Impact, positive: workplace is used as an active learning environment where employees can gain practical job experience.",
    "Impact, positive: businesses may claim back some of the costs of training as a refund from relevant SETAs.",
    "Impact, positive: improves quality of products/service delivery as the business employs more skilled workers.",
    "Impact, negative: the SDA process is prescriptive/requires a large amount of paperwork/administration, that can cost time/money.",
    "Impact, negative: Skills Development Levy could be an extra burden to financially struggling businesses.",
    "Impact, negative: it may be monitored/controlled by government departments that do not have education/training as their key priorities.",
    "Impact, negative: many courses offered by companies may not have unit standards that relate to the course content.",
    "Impact, negative: skills programmes may not always address the training needs of employees.",
    "Impact, negative: many service providers that offer training services are not SAQA accredited.",
    "Impact, negative: many businesses may not support this government initiative.",
    "Impact, negative: implementation of the SDA can be difficult to monitor and control.",
    "Impact, negative: employees are expected to attend learnerships during work hours that could affect the production process/productivity.",
    "Impact, negative: costly for businesses to employ a person to implement/manage/control learnerships.",
    "Impact, negative: the time/money spent on improving employee skills is wasted if they leave the business.",
    "Impact, negative: only companies with a staff payroll over R500 000 per annum can claim the Skills Development levy.",
    "Complying with the SDA (max 12, 2 each): businesses/employers who collect PAYE should register with the relevant SETAs.",
    "Complying: one per cent (1%) of an employer's payroll must be paid over to the SETA through SARS.",
    "Complying: businesses should register with SARS in the area in which their business is classified (in terms of the SETA).",
    "Complying: employers should submit a workplace skills plan and provide evidence that it was implemented.",
    "Complying: businesses with more than 50 employees must appoint a skills development facilitator.",
    "Complying: assess the skills of employees to determine areas in which skills development is needed.",
    "Complying: encourage employees to participate in learnerships and other training programmes.",
    "Complying: provide all employees with the opportunity to improve their skills.",
    "Complying: display a summary of the SDA in the business where it is visible to all employees.",
    "Conclusion (any 1 x 2): businesses should register with SETAs for training programmes that are accredited with the South African "
    "Qualification Authorities (SAQA); the SDA makes provisions for the establishment and the effective functioning of SETAs; the Skills "
    "Development Act plays an important role in ensuring that the South African workforce is skilled and encourage employee participation in "
    "lifelong learning; businesses are encouraged to comply with this Act in order to avoid penalties and an increased financial burden on businesses.",
    "Any other relevant answer under each heading."] + INSIGHT,
    ["Plan four headings, one per bullet in the question, between an introduction and a conclusion.",
     "SETAs: what they do. Purpose: what the Act sets out to do. Impact: good AND bad for a business. Compliance: what a business must do."],
    notes=ESSAY_NOTES)]
q6 = [rub("6", "Businesses that follow the correct selection procedures are able to identify suitable and qualified candidates for vacant positions. "
          "They also use different salary determination methods to ensure that their employees are remunerated correctly. Businesses offering "
          "fringe benefits and inducting new employees are more likely to have a productive workforce.\n\nWrite an essay on the human resources "
          "function in which you include the following aspects:\n• Outline the selection procedure as a human resources activity.\n"
          "• Explain the TWO salary determination methods.\n• Discuss the impact of fringe benefits on businesses.\n"
          "• Advise businesses on the benefits of induction.", 40, [
    "Introduction (any 2 x 1): the human resources manager is responsible for selecting and appointing qualified and competent employees to "
    "avoid fruitless expenditure; businesses use different salary determination methods to appropriately compensate their employees according "
    "to the kind of work done or tasks they perform; employees receive fringe benefits over and above their normal salaries and wages, which "
    "often improves their overall job satisfaction; the induction of new employees into the work environment provides introductory training to "
    "allow for a smooth transition into the new work environment.",
    "Selection procedure (max 12, 2 each, in any order): determine fair assessment criteria on which selection will be based.",
    "Selection: applicants must submit the application forms/curriculum vitae and certified copies of personal documents/IDs/proof of qualifications.",
    "Selection: sort the received documents/CVs according to the assessment/selection criteria. ACCEPT: receive documentation such as "
    "application forms and sort it according to the criteria of the job.",
    "Selection: screen/determine which applications meet the minimum job requirements and separate these from the rest. ACCEPT: evaluate CVs "
    "and create a shortlist/screen the applicants.",
    "Selection: preliminary interviews are conducted if many suitable applications were received/to identify suitable applicants. ACCEPT: conduct "
    "preliminary sifting interviews to identify applicants who are not suitable for the job, although they meet all requirements.",
    "Selection: reference checks/vetting process should be made/followed to verify work experience/criminal records/credit records/qualifications "
    "on the CV. ACCEPT: check information in the CVs and contact references.",
    "Selection: compile a shortlist of potential candidates identified.",
    "Selection: shortlisted candidates may be subjected to various types of selection tests such as skills tests. ACCEPT: assess/test candidates "
    "who have applied for senior positions/to ensure the best candidate is chosen.",
    "Selection: invite shortlisted candidates for an interview. ACCEPT: conduct interviews with shortlisted candidates.",
    "Selection: a written offer is made to the selected candidate. ACCEPT: offer employment in writing to the selected candidate(s).",
    "Selection: inform unsuccessful applicants about the outcome of their application/some advertisements indicate the deadline for informing "
    "only successful candidates.",
    "Salary determination methods (max 12; the TWO methods, each the method 2 + explanation 4, submax 6): Piecemeal.",
    "Piecemeal: workers are paid according to the number of items/units produced/action performed.",
    "Piecemeal: workers are not remunerated for the number of hours worked, regardless of how long it takes them to make the items.",
    "Piecemeal: mostly used in factories particularly in the textile/technology industries.",
    "Time-related (method 2 + explanation 4).",
    "Time-related: workers are paid according to the amount of time/hours they spend at work/on a task.",
    "Time-related: workers with the same experience/qualifications are paid on salary scales regardless of the amount of work done.",
    "Time-related: many private and public sector businesses use this method.",
    "Impact of fringe benefits (max 12, 2 each), positive: attractive fringe benefit packages may result in higher employee retention/reduces "
    "employee turnover.",
    "Impact, positive: attracts qualified/skilled/experienced employees who may positively contribute towards the business goals/objectives.",
    "Impact, positive: improves productivity resulting in higher profitability.",
    "Impact, positive: it increases employee satisfaction/loyalty as they may be willing to go the extra mile.",
    "Impact, positive: businesses save money as benefits are tax deductible.",
    "Impact, positive: fringe benefits can be used as leverage for salary negotiations.",
    "Impact, negative: businesses which cannot offer fringe benefits fail to attract skilled workers.",
    "Impact, negative: businesses which offer employees different benefit plans may create resentment to those who receive less benefit "
    "resulting in lower productivity.",
    "Impact, negative: it can create conflict/lead to corruption if allocated unfairly.",
    "Impact, negative: fringe benefits are additional costs that may result in cash flow problems.",
    "Impact, negative: decreases business profits, as incentive/package/remuneration costs are higher.",
    "Impact, negative: administrative costs increase as benefits need to be correctly recorded for tax purposes.",
    "Impact, negative: workers only stay with the business for fringe benefits, and may not be committed/loyal to the tasks/business.",
    "Impact, negative: businesses have to pay advisors/attorneys to help them create benefit plans that comply with legislation.",
    "Impact, negative: errors in benefit plans may lead to costly lawsuits/regulatory fines.",
    "Benefits of induction (max 10, 2 each): allows new employees to settle in quickly and work effectively.",
    "Induction: ensures that new employees understand rules and restrictions in the business.",
    "Induction: new employees may establish relationships with fellow employees at different levels.",
    "Induction: make new employees feel at ease in the workplace, which reduces anxiety/insecurity/fear.",
    "Induction: the results obtained during the induction process provide a base for focussed training.",
    "Induction: increases quality of performance/productivity which promotes the effective use of working methods/resources.",
    "Induction: minimises/decreases the need for on-going training and development.",
    "Induction: employees will be familiar with organisational structures, such as who are their supervisors/low level managers.",
    "Induction: opportunities are created for new employees to experience/explore different departments.",
    "Induction: new employees will understand their role/responsibilities concerning safety regulations and rules.",
    "Induction: new employees will know the layout of the building/factory/offices which saves production time.",
    "Induction: learn more about the business so that new employees understand their roles/responsibilities to be more efficient.",
    "Induction: company policies are communicated regarding conduct and procedures/safety and security/employment contract/conditions of "
    "employment/working hours/leave.",
    "Induction: realistic expectations for new employees as well as the business are created.",
    "Induction: new employees may feel part of the team resulting in positive morale and motivation.",
    "Induction: employees may have a better understanding of business policies regarding ethical/professional conduct/procedures/CSR.",
    "Induction: reduces the staff turnover as new employees have been inducted properly.",
    "Conclusion (any 1 x 2): competent employees who have been selected with the use of prescribed requirements and criteria will add value to "
    "businesses; businesses can avoid unnecessary disputes by paying the employees according to the appropriate salary determination methods; "
    "attractive fringe benefits encourage employees to work hard towards achieving business goals; a well-designed induction programme allows "
    "for new employees to gain a better understanding of the requirements of the new job.",
    "Any other relevant answer under each heading."] + INSIGHT,
    ["Plan four headings, one per bullet in the question, between an introduction and a conclusion.",
     "Selection: the steps in order. Salary: piecemeal and time-related. Fringe benefits: good AND bad. Induction: what it gives the business."],
    notes=["The selection procedure may be in any order; the memo's two options are the same steps worded differently.",
           "Salary determination methods: mark the first TWO only."] + ESSAY_NOTES)]
missions_c = [
    {"id": "5", "title": "Question 5", "kind": "Essay: the Skills Development Act", "marks": 40, "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Essay: the human resources function", "marks": 40, "items": q6},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Business Studies", "title": "Business Studies P1", "sitting": "November 2024", "total_marks": 150, "time": "2 hours"},
    "sections": [
        {"title": "Section A", "total": 30, "missions": missions_a},
        {"title": "Section B", "total": 80, "answer_any": 2, "missions": missions_q2 + missions_q3 + missions_q4},
        {"title": "Section C", "total": 40, "answer_any": 1, "missions": missions_c},
    ],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 6), hand-transcribed from the paper and memo PDFs; no API call."},
        {"n": "3.6.2", "kind": "memo_issue", "detail": "The memo's note reads 'Accept relevant facts even if the financial function was incorrectly "
                                                       "identified as an answer in QUESTION 3.6.2'; the function is identified in 3.6.1, and the "
                                                       "note is transcribed with 3.6.1."},
        {"n": "3.3.1", "kind": "no_fit", "detail": "Quote items (3.3.1, 4.3.1) are played by picking the scenario's sentences: the memo awards marks "
                                                   "only for responses quoted from the scenario, so picking the right sentences is the same skill."},
    ],
}
out = Path(__file__).parent / "out" / "bs-p1-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs (no API call)",
                                                        "scope": "Questions 1 to 6 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for sec in paper["sections"]:
    print(sec["title"], "parts:", sum(len(m["items"]) for m in sec["missions"]), "marks:", sum(i["marks"] for m in sec["missions"] for i in m["items"]),
          "answer any:", sec.get("answer_any", "all"))
