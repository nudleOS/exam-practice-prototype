"""Business Studies P1 Nov 2025, the whole paper (Sections A, B and C), hand-transcribed into the catalogue format (as if Claude had
produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks and memo points are the
paper's and the memo's own; the clues are ours. No API call: the transcription is the source, kept in git (out/ is not).
2025 papers first (Murci, 2026-10-06).

  python tools/ingest/transcribe_bs_p1_2025_11.py
  python tools/ingest/ingest.py "<...>/Business Studies P1 Nov 2025 Eng.pdf" "<...>/Business Studies P1 Nov 2025 MG Eng.pdf" --id bs-p1-2025-11 --from-json

How the memo's shapes map (the same for every Business Studies paper):
  1.1 multiple choice -> mcq; 1.2 a word from the printed list -> term (the list is the block's lead); 1.3 COLUMN A to COLUMN B
  (ten descriptions, A-J) -> match (each 2); "Name/Give any N" -> list; "Quote TWO ... from the scenario" -> pickn over the
  scenario's own sentences (the memo: "only award marks for responses that are quoted from the scenario"); "Classify" -> match
  (each item to its environment); one fixed answer -> term; explain/discuss/outline/advise/describe -> rubric, its points the
  memo's (each 2 where every point is worth two ticks); the essays -> one rubric each, the memo's points under its own headings
  and sub-maxima, plus insight (LASO). Section B is "answer any TWO" and Section C "answer any ONE" (answer_any).

Then (Murci 2026-10-10, the same shape as bs-p2-2025-11), see the bottom block: every written (rubric) part plays as STATEMENTS
(pick the memo's points among clearly wrong ones) or, where the memo weighs two sides, a SORT (4.4); both essays play as SECTIONS
(one part per memo heading, facts summing to 32) plus an INSIGHT part (8). The rubric parts above stay as the memo source."""
import json
from pathlib import Path

mcq = lambda n, q, opts, a, clues: {"t": "mcq", "n": n, "marks": 2, "q": q, "clues": clues, "opts": opts, "a": a}
term = lambda n, q, a, clues, marks=2: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a}
lst = lambda n, q, count, pool, clues: {"t": "list", "n": n, "marks": count, "q": q, "clues": clues, "count": count, "pool": pool}
pick = lambda n, q, opts, pool, clues: {"t": "pickn", "n": n, "marks": len(pool), "q": q, "clues": clues, "opts": opts, "pool": pool, "count": len(pool)}
match = lambda n, q, left, right, a, each, clues, **kw: {"t": "match", "n": n, "marks": len(left) * each, "q": q, "clues": clues, "left": left,
                                                         "right": right, "a": a, **({"each": each} if each > 1 else {}), **kw}


# notes: the memo's marking instructions that are NOT points ("Mark the first TWO only ..."): never scored, never shown (2026-10-10)
# worth: each point's own marks where they differ ("Force (2) + Motivation (1)": the name and its quote, [2, 1]) (2026-10-10)
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


# ---- Section A: Question 1, the question paper pages 3-5 and the memo page 7 ----
q11 = [
    mcq("1.1.1", "This Act requires businesses to display information of their products on packaging:",
        ["Employment Equity Act (EEA), 1998 (Act 55 of 1998)", "Labour Relations Act (LRA), 1995 (Act 66 of 1995)",
         "Consumer Protection Act (CPA), 2008 (Act 68 of 2008)", "National Credit Act (NCA), 2005 (Act 34 of 2005)"], 2,
        ["Which Act is about the rights of the people who BUY products?", "Labelling tells a buyer what is inside the packaging."]),
    mcq("1.1.2", "Smith Stores uses outdated computers which prevent access to online transactions. This challenge is classified as a … "
        "factor of the PESTLE analysis.", ["technological", "political", "legal", "social"], 0,
        ["PESTLE: political, economic, social, technological, legal, environmental.", "What kind of problem is an old computer?"]),
    mcq("1.1.3", "Highway Manufacturing operate in the ... sector as they produce office chairs from timber and steel.",
        ["tertiary", "primary", "economic", "secondary"], 3,
        ["Primary takes from nature, secondary makes things, tertiary provides services.", "Turning timber and steel into chairs is ..."]),
    mcq("1.1.4", "The role of the interviewer during an interview is to …",
        ["make the interviewee feel at ease.", "ask clarity-seeking questions about the position.", "assist candidates in responding to questions.",
         "be inquisitive and show interest in the business."], 0,
        ["Two of the options describe what a CANDIDATE should do, not the interviewer.",
         "An interviewer must be fair to every candidate: no one gets help that the others do not."]),
    mcq("1.1.5", "Top Limited implemented the … step of the PDCA model by monitoring processes to determine whether they are functioning "
        "effectively.", ["do", "check", "plan", "act"], 1,
        ["Plan, Do, Check, Act: which step looks at results?", "Monitoring whether something works is ..."]),
]
WORDS = "selection;  job specification;  National Skills;  management;  threat;  placement;  weakness;  performance;  job description;  Human Resources"
q12 = [
    term("1.2.1", "The … Development Strategy aims to increase access to programmes that train people.", ["National Skills"],
         ["Its goals are what the SETAs and the training levy work towards.", "Think of the Act that created the SETAs."]),
    term("1.2.2", "Eezy Electronics are losing customers due to the high crime rate in the area. This is classified as a … in the SWOT "
         "analysis.", ["threat"], ["Is crime in the area inside or outside the business?", "Is losing customers good or bad for the business?"]),
    term("1.2.3", "The component of the job analysis that outlines the duties and responsibilities of the position is known as …",
         ["job description"], ["A job analysis has two parts: one is about the work itself, one about the person who will do it.",
                               "Duties and responsibilities belong to the work, not the person."]),
    term("1.2.4", "Themba, the human resources manager, conducts background checks of applicants who qualify for the job during the … "
         "procedure.", ["selection"], ["Recruitment attracts applicants; what comes next?", "Checking applicants before choosing one is part of ..."]),
    term("1.2.5", "Blue Manufacturer developed new methods and techniques to improve the quality of their products. This is known as "
         "quality …", ["management"], ["Not one product check, but the whole way a business runs its quality.",
                                       "Which word in the list names the work of planning, organising, leading and controlling?"]),
]
COL_B = ["an agreement between the employer and the employee that is legally binding",
         "responsible for producing goods at the lowest possible cost",
         "focuses on the ability of a product to satisfy the needs of customers",
         "distributes the wealth of the country to a few previously disadvantaged individuals",
         "aims at reducing the business' dependency on suppliers",
         "an agreement between the employer and the trade union that is legally binding",
         "responsible for buying raw materials in bulk at lower prices",
         "focuses on achieving customer satisfaction and continuous improvement in all business processes",
         "distributes the wealth of the country across a broader spectrum of society",
         "aims at reducing the threat of competition"]
q13 = [match("1.3", "Choose a description from COLUMN B that matches a term in COLUMN A.",
             ["Black Economic Empowerment", "Horizontal integration", "Employment contract", "Purchasing function", "Total quality management"],
             COL_B, [3, 9, 0, 6, 7], 2,
             ["Two descriptions are close for several terms: read the small words (employee or trade union, a few or broader).",
              "Horizontal integration buys a business at the same level: what does that remove?"])]
missions_a = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 10,
     "lead": "Various options are provided as possible answers to the following questions. Choose the answer.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Words from a list", "marks": 10,
     "lead": "Complete the following statements by using the word(s) provided in the list below.\n\n" + WORDS, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Matching columns", "marks": 10, "items": q13},
]

# ---- Section B: Question 2 (Business Environments), the question paper page 6 and the memo pages 8-13 ----
BF = ("Bona Frames are well-known for their quality sunglasses and reading spectacles. BF sales have decreased as Bright Eyewear sells "
      "unique sunglasses at reasonable prices.")
MF = ("Meyer Furniture provides customers with facilities to buy goods on credit. MF conducts credit checks with the credit bureau before "
      "the granting of credit. They allow customers a five-day cooling-off period to return goods. MF also ensures that their procedures "
      "adhere to the provisions of the Financial Intelligence Centre Act (FICA).")
q2 = [
    lst("2.1", "Name any FOUR types of leave provisions as stipulated in the Basic Conditions of Employment Act (BCEA), 1997 (Act 75 of 1997).", 4,
        [["Annual", "annual leave"], ["Sick", "sick leave"], ["Maternity", "maternity leave"],
         ["Parental", "Adoption", "Commissioning parental", "Paternity", "parental leave", "adoption leave", "paternity leave"],
         ["Family responsibility", "family responsibility leave"]],
        ["Think of the reasons a worker may be away with the BCEA's protection.", "Holidays, illness, a new baby, a family crisis ..."]),
    rub("2.2", "Outline the role of SETAs in supporting the Skills Development Act (SDA), 1998 (Act 97 of 1998).", 4, [
        "Report to the Director General.", "Promote and establish learnerships.", "Collect levies and pay out grants as required.",
        "Provide accreditation for skills development facilitators.", "Register learnership agreements/learning programmes.",
        "Approve workplace skills plans and annual training reports.", "Monitor/Evaluate the actual training by service providers.",
        "Allocate grants to employers/education/training providers.", "Oversee training in different sectors of the South African economy.",
        "Develop sector skills plans in line with the National Skills Development Strategy.",
        "Draw up skills development plans for their specific economic sectors.",
        "Provide training material/programmes for skills development facilitators.",
        "Pay out grants to businesses that are complying with the requirements of the Skills Development Act.",
        "Identify suitable workplaces for practical work experience.",
        "Any other relevant answer related to the role of SETAs in supporting the SDA."],
        ["SETA: Sector Education and Training Authority. One sector, its training.",
         "Ask of each card: is it about training and skills in a sector?"], each=2),
]
q23 = [
    rub("2.3.1", "Identify the force of Porter's Five Forces model that is applicable to BF. Motivate your answer by quoting from the scenario "
        "above.", 3, [
            "Competitive rivalry/Power of competitors.",
            "(Its motivation, quoted from the scenario:) 'BF sales have decreased as Bright Eyewear sells unique sunglasses at reasonable prices.'"],
        ["Who is taking BF's sales away?", "Check both halves of each card: the force AND the sentence that proves it."], worth=[2, 1],
        notes=["No marks for the motivation if the force is wrong; the force earns its marks even if the motivation is incomplete."]),
    rub("2.3.2", "Describe how businesses could apply ONE other force of Porter's Five Forces model to analyse their position in the market "
        "environment.", 3, [
            "Bargaining power of suppliers OR Power of suppliers.",
        "(Bargaining power of suppliers/Power of suppliers, described:) assess the power of the suppliers in influencing "
            "prices; suppliers that deliver high quality/unique/scarce products may have power over the business; the more powerful the "
            "suppliers, the less control the business has over them; the smaller the number of suppliers, the more powerful they may be as the "
            "choice of suppliers may be limited; identify the kind of power suppliers have in terms of the quality of products/services/"
            "reliability/ability to make prompt deliveries.",
            "OR — Bargaining power of buyers OR Power of buyers.",
        "(Bargaining power of buyers/Power of buyers, described:) assess how easy it is for buyers/customers to drive "
            "prices down; determine the number of buyers/the importance of each buyer to the business and the cost of switching to other "
            "products; a few powerful buyers are often able to dictate their terms to the business; buyers buying in bulk can bargain for "
            "prices in their favour; if buyers can do without the business's products then they have more power to determine the prices and "
            "terms of sale; conduct market research to gather more information about its buyers.",
            "OR — Threat of substitution/substitutes.",
        "(Threat of substitution/substitutes, described:) business's products that can be easily substituted weakens the "
            "power of the business in the market; establish whether the sellers of substitute products have improved their product/sell lower "
            "quality goods at lower prices; if the business sells unique products it will not be threatened by substitute products; assess if "
            "customers are using substitute products/services and determine reasons for using substitutes.",
            "OR — Threat/Barriers of new entrants to the market.",
        "(Threat/Barriers of new entrants to the market, described:) if the barriers to enter the market are low, then it is "
            "easy for new businesses to enter the market/industry; if the business is highly profitable, it will attract potential competitors "
            "that want to benefit from high profits; new competitors can quickly/easily enter the market, if it takes little time/money to "
            "enter the market; if there are a few suppliers of a product/service but many buyers, it may be easy to enter the market."],
        ["The force from 2.3.1 does not count here.",
         "Check each description against how the force really works: does it give the business more control or less?"], worth=[2, 1, 2, 1, 2, 1, 2, 1],
        notes=["Mark the first ONE force only. No marks for competitive rivalry/power of competitors (2.3.1's force)."]),
]
q24 = [rub("2.4", "Explain the steps in strategy evaluation.", 4, [
    "Examine the underlying basis of a business strategy.", "Look forward and backwards into the implementation process.",
    "Compare the expected performance with the actual performance.", "Determine the reasons for deviations and analyse these reasons.",
    "Take corrective action so that deviations may be corrected.", "Set specific dates for control and follow up.",
    "Draw up a table of the advantages and disadvantages of a strategy.",
    "Decide on the desired outcome as envisaged when strategies were implemented.",
    "Consider the impact of the strategic implementation in the internal and external environments of the business.",
    "Any other relevant answer related to the steps in strategy evaluation (in any order)."],
    ["Evaluation looks back at a strategy already in use.",
     "Ask of each card: does it help the business learn whether its strategy is working?"], each=2)]
q25 = [rub("2.5", "Discuss any TWO types of intensive strategies.", 6, [
    "Market penetration.",
        "(Market penetration, discussed:) new products penetrate an existing market at a low price, until it is well "
    "known to the customers and then the price increases; businesses focus on selling existing products into existing markets to increase "
    "their market share; businesses use market research on existing clients to decide on how to improve their marketing mix; aggressive "
    "marketing campaigns such as lowering/reducing prices are used to attract potential/existing clients; embark on an intensive advertising "
    "campaign to increase awareness and customer loyalty; employ more sales staff to improve sales/services.",
    "Market development.",
        "(Market development, discussed:) a growth strategy where businesses aim to sell their existing products in new "
    "markets; businesses target consumers in a potential market that is outside of its normal target market; increasing sales of existing "
    "products by finding new ways to develop new markets; prices are restructured/reviewed to cater for customers/consumers of all income levels.",
    "Product development.",
        "(Product development, discussed:) a growth strategy where businesses aim to introduce new products into existing "
    "markets/modifies an existing product; businesses generate new ideas/develop new products/services for existing/current markets; "
    "businesses conduct test marketing/market research to establish whether new products will be accepted by existing customers; new "
    "products may be different/of a higher quality than those of competitors."],
    ["Intensive strategies work harder with existing products or markets.",
     "Ask of each card: is the product new or existing, and is the market new or existing?"], worth=[2, 1, 2, 1, 2, 1],
    notes=["Mark the first TWO only (3 marks each: the strategy 2, its discussion 1)."])]
q26 = [
    pick("2.6.1", "Quote TWO ways in which MF complies with the National Credit Act (NCA), 2005 (Act 34 of 2005) from the scenario above.",
         sentences(MF), [1, 3], ["Offering credit is not, by itself, obeying the Act: look for what MF DOES to follow the rules on credit.",
                                 "The five-day period to return goods is a consumer right from another Act."]),
    rub("2.6.2", "Recommend other ways in which businesses can comply with the National Credit Act.", 4, [
        "Offer applicants pre-agreement statements.", "Disclose all costs of the loan/No hidden costs should be charged/added.",
        "Businesses should be registered with the National Credit Regulator.",
        "Submit an annual compliance report to the National Credit Regulator.",
        "Conduct affordability assessment to ensure that consumers have the ability to meet their obligations.",
        "Verify the identity of clients and report suspicious transactions/train staff on their obligations in terms of FICA.",
        "Any other relevant answer related to other ways in which businesses can comply with the NCA."],
        ["Think about what a lender must do BEFORE it gives credit.", "Ask of each card: does it protect the consumer who borrows?"], each=2,
        notes=["No marks for the ways quoted from the scenario in 2.6.1."]),
]
q27 = [rub("2.7", "Explain ways in which businesses can apply ownership as a pillar of the Broad-Based Black Economic Empowerment Act (BBBEE), "
           "2003 (Act 53 of 2003).", 6, [
    "Businesses should include black people in shareholding/partnerships/franchises.",
    "Encourage small black investors to invest in big companies and share ownership.",
    "Exempted Micro Enterprises (EMEs) with an ownership of 50% or more of black people are promoted to level 3 of the BEE scorecard.",
    "More opportunities are created for black people to become owners/entrepreneurs.",
    "Large businesses should form joint ventures with small black owned businesses and share business risks.",
    "Businesses sometimes find it difficult to locate suitable black business partners/shareholders who can afford shares.",
    "Many black people cannot afford shares in companies/contributions to partnerships.",
    "Any other relevant answer related to ways in which businesses can apply ownership as a pillar of BBBEE."],
    ["Ownership is about who holds a stake in the business.", "How can black people become part-owners of a business?"], each=2)]
q28 = [rub("2.8", "Advise businesses on the advantages of diversification strategies.", 4, [
    "Increases sales/revenue/income and business growth.", "Improves the business brand/image/brand awareness of the business.",
    "Reduces the risk of relying only on one product for sales/revenue/income.",
    "Businesses gain more technological capabilities through product modification.",
    "Sustained profitability from different product lines during times of fluctuating economic activities.",
    "Businesses produce more output using less inputs as one factory may be used to manufacture more products.",
    "Enables businesses to retain their competitive advantage by meeting the needs of current/new customers/expanding into new unexplored markets.",
    "Allow businesses to remain relevant/functional/operational in a dynamic business environment.",
    "Enable businesses to establish additional markets in unrelated markets/industries.",
    "Any other relevant answer related to the advantages of diversification strategies."],
    ["Diversifying means adding new products or new markets.", "What does a business gain from selling more than one kind of product?"], each=2)]
missions_q2 = [
    {"id": "2.1", "title": "Question 2.1", "kind": "Leave in the BCEA", "marks": 4, "items": q2[:1]},
    {"id": "2.2", "title": "Question 2.2", "kind": "SETAs", "marks": 4, "items": q2[1:]},
    {"id": "2.3", "title": "Question 2.3", "kind": "Porter's Five Forces", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "BONA FRAMES (BF)\n\n" + BF, "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Strategy evaluation", "marks": 4, "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Intensive strategies", "marks": 6, "items": q25},
    {"id": "2.6", "title": "Question 2.6", "kind": "National Credit Act", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "MEYER FURNITURE (MF)\n\n" + MF, "items": q26},
    {"id": "2.7", "title": "Question 2.7", "kind": "BBBEE ownership", "marks": 6, "items": q27},
    {"id": "2.8", "title": "Question 2.8", "kind": "Diversification", "marks": 4, "items": q28},
]

# ---- Section B: Question 3 (Business Operations), the question paper page 7 and the memo pages 14-18 ----
FW = ("Fabric Wholesalers sell different types of material. FW pay their employees according to the number of rolls of material they sell. "
      "They have a sound knowledge of the Labour Relations Act (LRA), 1995 (Act 66 of 1995) and its implications on the human resources function.")
BM = ("Bilon Manufacturers produce sport cars. BM schedule their activities to avoid the duplication of tasks. The management of BM shares "
      "the responsibility for quality output with employees. BM is also aware of the impact of total quality management (TQM) if it is "
      "poorly implemented.")
q31 = [lst("3.1", "Give any FOUR examples of fringe benefits.", 4,
           [["Pension fund"], ["Medical aid fund", "Health insurance fund", "Medical aid"], ["Funeral benefit"], ["Provident fund"],
            ["Allowances", "Car allowance", "Travel allowance", "Housing allowance", "Cell phone allowance", "Clothing allowance"],
            ["Performance based incentives", "Performance incentives"], ["Issuing of bonus shares", "Bonus shares"],
            ["Staff discount", "Free or low-cost meal", "Canteen facilities"]],
           ["Fringe benefits come on top of the salary.", "Think retirement, health, a car, a discount on what the business sells."])]
q32 = [rub("3.2", "Outline the placement procedure as a human resources activity.", 6, [
    "Businesses should outline the specific responsibilities/expectations/skills of the new position.",
    "Determine the successful candidate's strengths/weaknesses/interests/skills by subjecting him/her to a range of psychometric tests.",
    "Determine the relationship between the position and the competencies of the new employee.",
    "Any other relevant answer related to the placement procedure as a human resources activity."],
    ["Placement puts the new employee in the right position.",
     "It happens after selection: the person is chosen; now, where do they fit best?"], each=2)]
q33 = [
    term("3.3.1", "Name the salary determination method applied by FW in the scenario above.", ["Piecemeal", "Piece meal", "Piece-meal"],
         ["FW pays by how much each worker sells.",
          "There are two methods: pay for time worked, or pay for output produced. Which does FW use?"]),
    rub("3.3.2", "Explain the implications of the Labour Relations Act on the human resources function.", 4, [
        "Promotes resolution of labour disputes between employer and employees.",
        "Protects the rights of employees/employers as outlined in the Constitution.",
        "Advances economic development and social justice/labour peace.",
        "Provides for unresolved disputes to be referred to Labour Courts/Labour Appeal Courts.",
        "Promotes orderly negotiations and employee participation in decision making in the workplace.",
        "Workers cannot be easily dismissed as bargaining council/Commission for Conciliation, Mediation and Arbitration (CCMA) processes need to be followed.",
        "Provides a framework for bilateral meetings where employees, trade unions and employers discuss matters relating to employment.",
        "The human resource manager should allow workers to form/establish workplace forums/trade unions/collective bargaining/bargaining "
        "councils to promote the interests of all employees.",
        "Clarify the transfer of contracts of employment./If a business is transferred to another owner then the employee contracts are also transferred.",
        "Any other relevant answer related to the implications of the LRA on the human resources function."],
        ["The LRA is about labour relations: disputes, unions, dismissals.", "What must the HR manager now do differently?"], each=2),
]
q34 = [rub("3.4", "Advise businesses on the reasons for the termination of an employment contract.", 4, [
    "The employer may dismiss an employee for a valid reason(s) such as unsatisfactory job performance/misconduct.",
    "Employer may no longer have work for redundant employees/cannot fulfil the contract/is restructuring.",
    "The employer may retrench some employees due to insolvency/may not be able to pay the employees.",
    "Employees may decide to leave/resign voluntarily for better job opportunities.",
    "An employee may have reached the pre-determined age for retirement.", "Incapacity of an employee to work due to illness/injuries.",
    "By a mutual agreement between the employer and employee.", "The duration of the employment contract expires/comes to an end.",
    "Any other relevant answer related to the reasons for the termination of an employment contract."],
    ["A contract can end because of the employer, the employee, or time.",
     "A fair reason is about the work, the business's situation or the contract itself, never about a worker's rights."], each=2)]
q35 = [rub("3.5", "Outline the difference between quality control and quality assurance.", 4, [
    "Quality control (submax 2): a system that ensures the desired quality is met by inspecting the final product; ensure that finished "
    "products meet the required standards; the process of ensuring that products are consistently manufactured to high standards; checking "
    "raw materials/employees/machinery/workmanship/products to ensure that high standards "
    "are maintained; includes setting targets/measuring performance and taking corrective measures.",
    "Quality assurance (submax 2): checks carried out during and after the production process; ensure that required standards have been met "
    "at every stage of the process; processes put in place to ensure that the quality of products/services/systems adhere to pre-set "
    "standards with minimal defects/delays/short-comings; ensuring that every process is aimed to get the product 'right the first time' "
    "and prevent mistakes from happening; the 'building in' of quality as opposed to 'checking of' quality."],
    ["One checks the finished product; the other builds quality in at every step.", "Inspecting at the end vs preventing mistakes along the way."], each=2,
    notes=["The answer need not be a table and the two sides need not link, but the difference must be clear: a maximum of 2 if it is not, or "
           "if only one of the two is given."])]
q36 = [
    pick("3.6.1", "Quote TWO ways from the scenario above in which BM apply total quality management (TQM) to reduce the cost of quality.",
         sentences(BM), [1, 2], ["Which sentences describe what BM DOES?",
                                 "Cost of quality falls when a business organises its work and its people well: which sentences show BM doing that on purpose?"]),
    rub("3.6.2", "Discuss the impact of total quality management (TQM) if poorly implemented by businesses.", 4, [
        "Setting unrealistic deadlines that may not be achieved.", "Employees may not be adequately trained resulting in poor quality products.",
        "Decline in productivity, because of stoppages.",
        "Businesses may not be able to make necessary changes of products/services to satisfy the needs of customers.",
        "Businesses' reputation/image may suffer because of poor quality/defective goods.",
        "Customers will have many alternatives to choose from and the impact could be devastating to businesses.",
        "Investors might withdraw investment, if there is a decline in profits.", "Decline in sales as more goods are returned by unhappy customers.",
        "High staff turnover, because of poor skills development.",
        "Undocumented/Uncontrolled quality control processes/systems could result in errors/deviations from pre-set quality standards.",
        "Any other relevant answer related to the impact of TQM if it is poorly implemented by businesses."],
        ["What goes wrong for customers, staff and investors when quality slips?", "Each true card names a problem and what it leads to."], each=2),
]
q37 = [rub("3.7", "Describe the advantages of monitoring and evaluation of quality processes as a total quality management (TQM) element for "
           "large businesses.", 6, [
    "Prevents product defects and minimises wastage/customer complaints.",
    "Good quality checks/procedures minimise the replacement/breakdown of equipment/machinery on a regular basis.",
    "May be equipped to get things done right the first time.", "Improve performance and maintain high quality standards.",
    "Improve current and future management of quality outputs/outcomes/impact.",
    "Provide clear indication about quality aspects that are contributing to the achievement of goals/targets.",
    "Modify interventions that may improve the efficient use of resources.",
    "Support management to acquire information needed to make informed decision about processes.",
    "Cost of production is reduced as deviations from set standards can be corrected.",
    "Strategies are revised in order to improve the quality of the product and services/business image.",
    "Allows for quality control checks and procedures at key points.",
    "Key performance indicators are carefully selected to monitor and evaluate the outcome.",
    "Benchmarking is used to find best practices in order to determine the competitive position of the business.",
    "Quality circles meet on regular basis to evaluate the progress in terms of quality.",
    "Continuous research is conducted on latest developments to ensure that TQM planning is up to date.",
    "Any other relevant answer related to the advantages of monitoring and evaluation of quality processes as a TQM element on large businesses."],
    ["Monitoring finds problems early; evaluating decides what to change.", "Ask of each card: would it make quality better or worse?"], each=2)]
q38 = [rub("3.8", "Advise businesses on the quality indicators of the public relations function.", 4, [
    "Dealing quickly with negative publicity./Less/little/no incidents of negative publicity.", "Providing regular/positive press releases.",
    "Implement sustainable corporate social investment (CSI) programmes.",
    "Good/positive results of feedback from public surveys on business image.",
    "High standard of internal publicity/appearance of buildings/professional telephone etiquette.",
    "Deliver quality goods/services that promote the brand/image with key stakeholders/customers/suppliers/government/service providers.",
    "Compliance with recent legislation, such as BEE compliant.",
    "Any other relevant answer related to quality indicators of the public relations function."],
    ["Public relations looks after the business's image.", "How would you SEE that the image is in good hands?"], each=2)]
missions_q3 = [
    {"id": "3.1", "title": "Question 3.1", "kind": "Fringe benefits", "marks": 4, "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Placement", "marks": 6, "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Salaries and the LRA", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "FABRIC WHOLESALERS (FW)\n\n" + FW, "items": q33},
    {"id": "3.4", "title": "Question 3.4", "kind": "Ending a contract", "marks": 4, "items": q34},
    {"id": "3.5", "title": "Question 3.5", "kind": "Control and assurance", "marks": 4, "items": q35},
    {"id": "3.6", "title": "Question 3.6", "kind": "Total quality management", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "BILON MANUFACTURERS (BM)\n\n" + BM, "items": q36},
    {"id": "3.7", "title": "Question 3.7", "kind": "Monitoring quality", "marks": 6, "items": q37},
    {"id": "3.8", "title": "Question 3.8", "kind": "Public relations quality", "marks": 4, "items": q38},
]

# ---- Section B: Question 4 (Miscellaneous topics), the question paper pages 8-9 and the memo pages 19-23 ----
GF = ("Global Farms distribute their fruit locally and internationally. Their exports have decreased due to unfavourable exchange rates. "
      "The workers of GF are also not meeting their deadlines because they are often late for work.")
FL = ("Fibernet Limited supply Wi-Fi routers to businesses and they apply total quality management (TQM) in their operations. FL can afford "
      "to conduct research to gather information on the quality of their products. They also benefit from a good quality management system.")
GF_CH = sentences(GF)[1:]
q41 = [lst("4.1", "Name any TWO types of defensive strategies.", 2, [["Divestiture"], ["Retrenchment"], ["Liquidation"]],
           ["Defensive strategies protect a business that is struggling.", "Selling off, cutting back, closing down."])]
q42 = [rub("4.2", "Outline the strategic management process.", 4, [
    "Have a clear vision/mission statement/measurable/realistic objective in place.",
    "Identify opportunities/weaknesses/strengths/threats by conducting environmental scanning/situational analysis.",
    "Tools available for environmental scanning may include a SWOT analysis/Porter's Five Forces model/PESTLE analysis/industrial analysis tools.",
    "Formulate alternative strategies to respond to the challenges.",
    "Develop (an) action plan(s), including the tasks to be done/deadlines to be met/resources to be procured.",
    "Implement selected strategies by communicating it to all stakeholders/organising business resources/motivating staff.",
    "Continuously evaluate/monitor/measure strategies in order to take corrective action.",
    "OR — (option 2) Review/Analyse/Re-examine their vision/mission statement.",
    "(option 2) Conduct an environmental analysis using models such as SWOT/PESTLE/Porter's Five Forces.",
    "(option 2) Formulate a strategy, such as defensive/retrenchment strategy.",
    "(option 2) Implement a strategy, using a template such as an action plan.",
    "(option 2) Control/Evaluate/Monitor the implemented strategy to identify gaps/deviations in implementation.",
    "(option 2) Take corrective action to ensure goals/objectives are met.",
    "Any other relevant answer related to the strategic management process."],
    ["It starts with where the business wants to go.",
     "Where does the business want to go, where is it now, how will it get there, and how will it know it worked?"], each=2)]
q43 = [
    pick("4.3.1", "Quote TWO challenges for GF from the scenario above.", sentences(GF), [1, 2],
         ["A challenge is a problem GF faces.", "One comes from outside the business, one from inside."]),
    match("4.3.2", "Classify GF's challenges according to the business environments.", GF_CH,
          ["Micro environment", "Market environment", "Macro environment"], [2, 0], 1,
          ["The three environments differ in how much control the business has.",
           "Ask of each challenge: who causes it, and can GF control it?"],
          heads=["CHALLENGES", "BUSINESS ENVIRONMENTS"], groups=True, after=["4.3.1"]),   # (its rows are 4.3.1's answers: it opens after 4.3.1)
]
q44 = [rub("4.4", "Discuss the impact of the Compensation for Occupational Injuries and Diseases Amendment Act (COIDA),1997 (Act 61 of 1997) "
           "on businesses.", 6, [
    "Positive: promotes safety in the workplace.",
    "Positive: domestic workers can now claim compensation for work related injuries/illnesses.",
    "Positive: employees do not contribute towards this fund.", "Positive: claiming processes are relatively simple.",
    "Positive: eliminates time and costs spent on lengthy civil court proceedings.",
    "Positive: any compensation to an employee/the family is exempt from income tax.",
    "Positive: employers are protected from financial burden should an accident occur in the workplace provided that the employer was not negligent.",
    "Positive: makes businesses more socially responsible as they cannot just employ workers at random in dangerous working conditions.",
    "Positive: workers are treated with dignity and respect as businesses view them as valuable assets and not just as workers.",
    "Positive: covers all employees at the workplace if both parties meet all the necessary safety provisions in the Act.",
    "Positive: creates a framework for acceptable employment practices and safety regulations.",
    "Positive: supply administrative guidelines/mechanisms for dealing with/processing claims.",
    "Positive: employees are compensated financially for any injury/disability resulting from performing their duties at their workplace.",
    "Positive: in the event of the death of an employee as a result of a work-related accident/disease, his/her dependent(s) will receive financial support.",
    "Positive: employees receive medical assistance provided there is no other medical assistance option/cannot claim medical assistance from the fund and medical aid.",
    "Positive: medical expenses/other types of compensation are paid to employees and/or their families depending on the type/severity of the injuries.",
    "Positive: employers have to pay a monthly amount to the Compensation Fund depending on the number of employees/the level of risk they are exposed to.",
    "Negative: claiming processes can be time consuming.", "Negative: military workers are not covered.",
    "Negative: workers who are temporarily/permanently employed in foreign countries are not covered.",
    "Negative: employers may be forced to pay heavy penalties if they are found guilty of negligence/not enforcing safety measures.",
    "Negative: implementation processes/procedures required by the Act may be expensive.",
    "Negative: procedures required by this Act may be costly as paperwork places an extra administrative burden on businesses.",
    "Negative: employers make annual contributions to COIDA, which may result in cash flow problems.",
    "Any other relevant answer related to the positive and/or negative impact of COIDA on businesses."],
    ["COIDA compensates workers injured or made ill by their work.",
     "Ask of each card: does it help the business, cost the business, or is it simply false?"], each=2)]
q45 = [rub("4.5", "Recommend ways in which businesses can deal with the challenges posed by the social factor of the PESTLE analysis.", 4, [
    "Sell substitute products at lower prices due to low levels of income distribution/Employ people from local community.",
    "Learn local languages/indigenous languages/Hire employees who are well conversant with the local language.",
    "Work together with community police forums and improve security in the business.",
    "Businesses must be well conversant with the demands/trends of their customers.",
    "Develop/produce/incorporate/innovate new products that aim to address the lifestyle attitude/trends of customers.",
    "Any other relevant answer related to the ways in which businesses can deal with the challenges posed by the social factor of the PESTLE analysis."],
    ["Social factors: income, language, crime, lifestyle and trends.", "For each challenge, what could the business do about it?"], each=2)]
q46 = [rub("4.6", "Outline the purpose of induction.", 4, [
    "Introduce new employees to management/colleagues to establish relationships with fellow colleagues at different levels.",
    "Give new employees a tour/information about the layout of the building/office.",
    "Make new employees feel welcome by introducing them to their physical workspace.", "Improve skills through in-service training.",
    "Familiarise new employees with the organisational structure/their supervisors.",
    "Allow new employees the opportunity to ask questions that will put them at ease/reduce insecurity/anxiety/fear.",
    "Create opportunities for new employees to experience/explore different departments.",
    "Explain safety regulations and rules, so that new employees will understand their roles/responsibilities in this regard.",
    "Ensure that employees understand their roles/responsibilities so that they will be more efficient/productive.",
    "Communicate information about the products/services offered by the business.",
    "Communicate business policies regarding ethical/professional conduct/procedures/employment contract/conditions of employment.",
    "Any other relevant answer related to the purpose of induction."],
    ["Induction is a new employee's first days.", "Ask of each card: does it help a new employee settle in?"], each=2)]
q47 = [rub("4.7", "Explain the Unemployment Insurance Fund (UIF) as a benefit required by law.", 6, [
    "Employees are required to contribute 1% of their basic salary towards UIF.",
    "Employers are required to contribute 1% of an employee's basic salary towards UIF.",
    "Employers must pay unemployment insurance contributions of 2% directly to UIF of the value of each worker's salary per month.",
    "The fund also assists the dependants of a contributing worker who has died.",
    "The fund offers short-term financial assistance to workers when they become unemployed or are unable to work due to illness, maternity or adoption leave.",
    "Contributions are paid to the Unemployment Insurance Fund (UIF)/South African Revenue Services (SARS).",
    "Any other relevant answer related to UIF as a benefit required by law."],
    ["Who pays into UIF, how much, and to whom?", "Who can be paid out, and when?"], each=2)]
q48 = [
    term("4.8.1", "Name the total quality management (TQM) element applied by FL in the scenario above.",
         ["Adequate financing and capacity", "Adequate financing"],
         ["FL can AFFORD to do something.",
          "Which TQM element depends on the business's resources rather than its people or its processes?"]),
    rub("4.8.2", "Explain the benefits of a good quality management system.", 4, [
        "Effective customer services are rendered, resulting in increased customer satisfaction.", "Time and resources are used efficiently.",
        "Productivity increases through proper time management/using high quality resources.",
        "Products/Services are constantly improved resulting in increased levels of customer satisfaction.",
        "Vision/Mission/Business goals may be achieved.", "A business has a competitive advantage over its competitors.",
        "Regular training will continuously improve the quality of employees' skills/knowledge/competencies.",
        "Employers and employees will have a healthy working relationship resulting in happy/productive workers/improved employee morale/productivity.",
        "Increased market share/financial stability as more customers improve profitability.",
        "Improves business image as there are less defects/returns.",
        "Any other relevant answer related to the benefits of a good quality management system."],
        ["A system that keeps quality high helps customers, staff and profits.",
         "Ask of each card: is it something a good system really delivers?"], each=2),
]
q49 = [rub("4.9", "Advise businesses on the role of quality circles as part of continuous improvement to processes and systems.", 4, [
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
    ["A quality circle is a small group of workers who meet about quality.",
     "Ask of each card: does it make the work better and the team stronger?"], each=2)]
missions_q4 = [
    {"id": "4.1", "title": "Question 4.1", "kind": "Defensive strategies", "marks": 2, "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Strategic management", "marks": 4, "items": q42},
    {"id": "4.3", "title": "Question 4.3", "kind": "Business environments", "marks": 4,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "GLOBAL FARMS (GF)\n\n" + GF,
     "table": {"title": "Use the table below as a GUIDE to answer QUESTIONS 4.3.1 and 4.3.2.", "head": ["CHALLENGES (4.3.1)", "BUSINESS ENVIRONMENTS (4.3.2)"],
               "rows": [["1.", ""], ["2.", ""]]}, "items": q43},
    {"id": "4.4", "title": "Question 4.4", "kind": "COIDA", "marks": 6, "items": q44},
    {"id": "4.5", "title": "Question 4.5", "kind": "Social challenges", "marks": 4, "items": q45},
    {"id": "4.6", "title": "Question 4.6", "kind": "Induction", "marks": 4, "items": q46},
    {"id": "4.7", "title": "Question 4.7", "kind": "UIF", "marks": 6, "items": q47},
    {"id": "4.8", "title": "Question 4.8", "kind": "Quality management", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "FIBERNET LIMITED (FL)\n\n" + FL, "items": q48},
    {"id": "4.9", "title": "Question 4.9", "kind": "Quality circles", "marks": 4, "items": q49},
]

# ---- Section C: the essays (answer any ONE), the question paper page 10 and the memo pages 24-31 ----
# Each essay is one rubric part (as printed: one question of 40): the memo's points under its own headings and sub-maxima (facts
# capped at 32), and insight (8). Every point earns 1 here: the keyword stand-in cannot judge sub-maxima, repetition or insight, so an
# essay's mark waits for model marking.
INSIGHT = ["Insight (8), 2 each: Layout (an introduction, paragraphs and a conclusion, the words INTRODUCTION and CONCLUSION stated and "
           "explained); Analysis and interpretation (all headings addressed; interpreted correctly); Synthesis (only relevant facts); "
           "Originality (an example in any TWO of the four aspects, based on recent information, current trends and developments, not "
           "older than two years).",
           ]
ESSAY_NOTES = ["Facts are capped at 32 of the 40; no marks for content repeated from the introduction or the conclusion."]
Q5_STEM = ("The Employment Equity Act (EEA), 1998 (Act 55 of 1998) was established to facilitate the transformation process in the workplace. "
           "The implementation of the EEA may have an impact on business operations. Businesses are compelled to comply with the requirements of "
           "this Act to avoid facing penalties for non-compliance.\n\nWrite an essay on the Employment Equity Act in which you include the following "
           "aspects:\n• Outline the purpose of the Employment Equity Act.\n• Discuss the impact of the Employment Equity Act on businesses.\n"
           "• Explain ways in which businesses can comply with the Employment Equity Act.\n• Advise businesses on penalties they may face for "
           "non-compliance with this Act.")
Q6_STEM = ("Businesses following the correct recruitment procedures will attract the best applicants. The human resources manager could use "
           "the internal recruitment method to fill the available vacancies. The interviewer must be well prepared before conducting the interview. "
           "Both employers and employees should be aware of the legal requirements of an employment contract.\n\nWrite an essay on the human "
           "resources function in which you include the following aspects:\n• Outline the recruitment procedure as a human resources activity.\n"
           "• Discuss the impact of internal recruitment on businesses.\n• Explain the role of the interviewer before the interview.\n"
           "• Advise businesses on the legal requirements of an employment contract.")
q5 = [rub("5", Q5_STEM, 40, [
    "Introduction (any 2 x 1): the EEA gives businesses the opportunity to create acceptable employment practices to correct inequalities of "
    "the past; businesses that implement the EEA will benefit from improved and greater transformation processes in the workplace; the "
    "requirements stated in the EEA compel businesses to align all the employment policies and procedures appropriately; the Act stipulates "
    "bodies that are responsible for monitoring of compliance and impose punitive measures for non-compliance.",
    "Purpose of the EEA (max 10, 2 each): the EEA allows employees who do the same work to be paid equally.",
    "Purpose of the EEA: eliminates discrimination on grounds of gender/race/disability in the workplace.",
    "Purpose of the EEA: promotes equal opportunity and fair treatment in the workplace.",
    "Purpose of the EEA: promotes diversity in the workplace by ensuring that people of diverse backgrounds are appointed.",
    "Purpose of the EEA: protects employees from victimisation if they exercise the rights given to them by the EEA.",
    "Purpose of the EEA: ensures equal representation in the workplace through the implementation of affirmative action.",
    "Impact of the EEA (max 14, 2 each), positive: encourages consultation between employer and employees.",
    "Impact, positive: treat employees fairly and promote/provide equal opportunities in the workplace.",
    "Impact, positive: impacts positively on BEE ratings for businesses.",
    "Impact, positive: appointment process is clearly defined, so all parties are well informed.",
    "Impact, positive: motivates employees because the workforce is more diverse/representative/inclusive.",
    "Impact, positive: motivates employees because everyone has the same employment opportunities.",
    "Impact, positive: promotes the implementation of affirmative action measures to redress the imbalances in employment.",
    "Impact, positive: provides employees with legal recourse if they have been unfairly discriminated against.",
    "Impact, positive: provides all employees with an equal opportunity to be selected/appointed/promoted in a position.",
    "Impact, positive: prevents unfair discrimination as it ensures that the workforce represents the demographics of the country.",
    "Impact, positive: creates a framework of acceptable employment practices/affirmative action measures.",
    "Impact, positive: encourages diversity in business by employing people from various racial backgrounds.",
    "Impact, positive: businesses are in a better position to negotiate contracts with the government.",
    "Impact, positive: certified psychometric tests may be used to assess applicants/employees to ensure that they are suitable for the vacancy.",
    "Impact, negative: increased administration burden, as businesses must compile/submit employment equity reports every two years.",
    "Impact, negative: expensive to train/employ someone who knows little about the Act.",
    "Impact, negative: other groups may not respect the knowledge/skills/experience of an EEA appointment and may lead to conflict.",
    "Impact, negative: fines/penalties for non-compliant businesses may be expensive for the business.",
    "Impact, negative: employers have to appoint one or more senior managers to ensure the implementation of the plan, which increases salary expenditure.",
    "Impact, negative: skilled people from designated groups may demand higher salaries which increase salary expenses.",
    "Impact, negative: job hopping of skilled/trained EEA appointees may increase staff turnover.",
    "Impact, negative: diversity in the workplace may lead to conflict/unhappiness.",
    "Impact, negative: businesses must submit a compliance certificate before they can conduct business with state businesses.",
    "Impact, negative: businesses are sometimes pressurised to appoint an unsuitable person to meet EEA requirements.",
    "Impact, negative: often positions go unfilled because there are no suitable EEA candidates.",
    "Complying with the EEA (max 12, 2 each): businesses should guard against discriminatory appointments.",
    "Complying: assess the racial composition of all employees, including senior management.",
    "Complying: ensure that there is equal representation of all racial groups in every level of employment.",
    "Complying: clearly define the appointment process, so that all parties are well informed.",
    "Complying: ensure that diversity/inclusivity in the workplace is achieved.",
    "Complying: prepare an employment equity plan in consultation with employees.",
    "Complying: compile employment equity plans that indicate how they will implement affirmative action.",
    "Complying: ensure that affirmative action measures promote diversity in the workplace.",
    "Complying: implement the employment equity plan as required by the Act.",
    "Complying: implement affirmative action measures to redress disadvantages experienced by designated groups/accommodate people from different designated groups.",
    "Complying: submit the employment equity plan to the Department of Labour.",
    "Complying: assign one or more senior managers to ensure implementation and monitoring of the employment equity plan.",
    "Complying: eliminate barriers that have an adverse impact on designated groups.",
    "Complying: regularly report to the Department of Labour on progress in implementing the plan.",
    "Complying: display a summary of the Act where employees can clearly see/have access to the document.",
    "Complying: conduct medical/psychological tests fairly to employees/when deemed necessary/use certified psychometric tests to assess "
    "applicants/employees to ensure that suitable candidates are appointed.",
    "Complying: ensure that the workplace represents the demographics of the country at all levels.",
    "Complying: restructure/analyse current employment policies/practices/procedures to accommodate designated groups.",
    "Complying: retrain/develop/train designated groups through skills development programmes.",
    "Complying: employees must be paid equal for work of equal value.",
    "Penalties for non-compliance (max 10, 2 each): labour inspectors may conduct onsite visits, to interview employees which can create a bad image for the business.",
    "Penalties: a compliance order may be issued to businesses that do not comply with the EEA.",
    "Penalties: businesses may be brought before the Labour Court if compliance orders are not adhered to/no efforts made to reach targets.",
    "Penalties: labour inspectors may investigate/inspect/ask questions about complaints.",
    "Penalties: businesses may face heavy fines for non-compliance.",
    "Penalties: they can be ordered to pay compensation and damages to the employee.",
    "Penalties: the Department of Labour may block non-compliant companies from doing business with the government.",
    "Penalties: the labour inspector could issue a compliance order to businesses to stop operating should they be found guilty of illegal practices.",
    "Conclusion (any 1 x 2): businesses that implement the EEA enjoy a balanced workforce and fair representation which portrays the demographics "
    "of the community in which the business operates; the EEA affords businesses access to the skills and expertise by employing people from "
    "various backgrounds; businesses that comply with the EEA have preferential treatment by government institutions regarding the awarding of "
    "tenders; penalties for non-compliance with the Act may have a negative financial implication for businesses.",
    "Any other relevant answer under each heading."] + INSIGHT,
    ["Plan four headings, one per bullet in the question, between an introduction and a conclusion.",
     "Purpose: what the Act sets out to do. Impact: good AND bad for a business. Compliance: what a business must do. Penalties: what happens if it does not."],
    notes=ESSAY_NOTES)]
q6 = [rub("6", Q6_STEM, 40, [
    "Introduction (any 2 x 1): an accurate recruitment procedure enables businesses to appoint suitable candidates who meet the needs of the "
    "identified position; businesses prefer internal recruitment methods as they provide existing employees with the opportunity to grow and "
    "showcase the skills they have acquired; the interviewer should have a comprehensive understanding of the interview process to ensure the "
    "necessary planning arrangements before the interview; businesses are guided by laws on drawing up the legal requirements of the employment contract.",
    "Recruitment procedure (max 10, 2 each, any order): the human resource manager should evaluate the job/prepare a job analysis, that includes "
    "the job specification/job description in order to identify recruitment needs.",
    "Recruitment: the HRM should prepare the job description in order to determine the responsibility/key performance areas related to the nature of the job.",
    "Recruitment: the HRM should indicate the job specification/description/key performance areas to attract suitable candidates.",
    "Recruitment: choose the method of recruitment, such as internal/external, to reach/target the suitable applicants/candidates.",
    "Recruitment: vacancies can be internally advertised via internal email/word of mouth/staff notices.",
    "Recruitment: if internal recruitment is unsuccessful, external recruitment should be considered.",
    "Recruitment: if the external recruitment is chosen/done, the relevant recruitment sources should be selected, such as recruitment "
    "agencies/tertiary institutions/newspapers.",
    "Recruitment: an advertisement should be prepared with the relevant information, such as the name of the company, contact details, contact person.",
    "Recruitment: place the advertisement in the appropriate media that will ensure that the best candidates apply.",
    "Impact of internal recruitment (max 14, 2 each), positive: cheaper/quicker to fill the post as this method focuses on promoting existing employees.",
    "Impact, positive: placement is easy, as management knows the employees' skills/personality/experience/strengths.",
    "Impact, positive: provides opportunities for career paths within the business.",
    "Impact, positive: the employee already understands how the business operates, induction/training is not always necessary.",
    "Impact, positive: reduces the chances of losing employees, as future career prospects are available.",
    "Impact, positive: detailed, reliable information can be obtained from the supervisors/employee records.",
    "Impact, negative: current employees may not bring/close the door to new ideas into the business/from outsiders.",
    "Impact, negative: promoting a current employee may cause resentment amongst other employees.",
    "Impact, negative: promotion may disrupt business operations as it creates open vacancies that need to be filled.",
    "Impact, negative: the number of applicants is limited to current staff only.",
    "Impact, negative: employees who do not really have the required skills for the new job may be promoted.",
    "Impact, negative: current employees may need to be trained/developed before they can be promoted, which can be expensive.",
    "Impact, negative: staff that is not promoted may feel demotivated which may hamper productivity.",
    "Role of the interviewer before the interview (max 10, 2 each): book and prepare the venue for the interview.",
    "Interviewer: inform all shortlisted candidates about the date and place of the interview.",
    "Interviewer: set the interview date and ensure that all interviews take place on the same date, if possible.",
    "Interviewer: notify all panel members conducting the interview about the date and place of the interview.",
    "Interviewer: develop a core set of questions based on the skills/knowledge/ability required.",
    "Interviewer: check/read the application/verify the CV of every candidate for anything that may need to be explained.",
    "Interviewer: plan the programme for the interview and determine the time that should be allocated to each candidate.",
    "Interviewer: allocate the same amount of time to interview each candidate on the programme.",
    "Legal requirements of an employment contract (max 12, 2 each): the employer and employee/both parties must sign the contract.",
    "Contract: employer and employee must agree to any changes to the contract.",
    "Contract: no party may unilaterally change aspects of the employment contract.",
    "Contract: the remuneration package/including benefits must be clearly indicated.",
    "Contract: the employment contract may not contain any requirements that are in conflict with the BCEA.",
    "Contract: aspects of the employment contract can be renegotiated during the course of employment.",
    "Contract: the employer must explain the terms and conditions of the employment contract to the employee.",
    "Contract: conditions of employment/duties/responsibilities of the employees must be stipulated clearly.",
    "Contract: all business policies/procedures/disciplinary codes/rules must form part of the employment contract.",
    "Contract: the employer must allow the employee to thoroughly read through the contract before it is signed.",
    "Contract: the employment contract should include a code of conduct and code of ethics.",
    "Conclusion (any 1 x 2): the correct recruitment procedure enables businesses to compile a proper job analysis that will be used to identify "
    "suitable candidates for the vacancy; internal recruitment may result in existing employees feeling valued when they are considered for "
    "promotions; the success of the interview depends on the manner in which the interviewer properly planned before the interview; businesses "
    "can avoid legal actions by aligning their employment contracts according to recent legislation.",
    "Any other relevant answer under each heading."] + INSIGHT,
    ["Plan four headings, one per bullet in the question, between an introduction and a conclusion.",
     "Recruitment: the steps in order. Internal recruitment: good AND bad. Before the interview: what the interviewer arranges. Contract: what the law requires."],
    notes=ESSAY_NOTES)]
missions_c = [
    {"id": "5", "title": "Question 5", "kind": "Essay: the Employment Equity Act", "marks": 40, "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Essay: the human resources function", "marks": 40, "items": q6},
]

# ---- Written answers as STATEMENTS (Murci 2026-10-10, the same shape as bs-p2-2025-11) ----
# A written part plays as picking statements: the memo's own points (right, tidied to one reading of its "/" alternatives) and
# CLEARLY wrong ones (never a true point the memo leaves out: its "any other relevant answer" would make that right). The learner
# picks marks/each of them, any right one counts (the memo's "any N"), each right pick earns `each`; the cards are shuffled the same
# way every run. The memo points above stay as the source. "Identify/Discuss a force or strategy + its quote or discussion" parts
# (2.3.1, 2.3.2, 2.5: the name 2 + its motivation/description 1) play as one card per name + its half, each 3.
import random


def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random("bs-p1-2025-11:" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts,
            "pool": sorted(k for k, i in enumerate(order) if i < len(right)), "count": count}


BF_Q = "'BF sales have decreased as Bright Eyewear sells unique sunglasses at reasonable prices.'"
BF_0 = "'Bona Frames are well-known for their quality sunglasses and reading spectacles.'"
STATEMENTS = {
    "2.2": (2, ["Promote and establish learnerships.", "Collect levies and pay out grants as required.",
                "Approve workplace skills plans and annual training reports.", "Monitor and evaluate the actual training by service providers."],
               ["Collect income tax from employees on behalf of SARS.", "Set the minimum wage that every sector must pay.",
                "Register trade unions and settle labour disputes between employers and employees."]),
    "2.3.1": (3, ["Competitive rivalry: " + BF_Q],
                 ["Bargaining power of suppliers: " + BF_Q, "Bargaining power of buyers: " + BF_0,
                  "Threat of new entrants: " + BF_0, "Threat of substitutes: " + BF_0]),
    "2.3.2": (3, ["Bargaining power of suppliers: the smaller the number of suppliers, the more powerful they may be, as the choice of suppliers "
                  "may be limited.",
                  "Threat of substitutes: if the business sells unique products, it will not be threatened by substitute products."],
                 ["Bargaining power of buyers: buyers who buy in bulk have less power to bargain for prices in their favour.",
                  "Threat of new entrants: if the barriers to enter the market are low, it is difficult for new businesses to enter the market.",
                  "Competitive rivalry: the more competitors there are in a market, the more control the business has over its prices."]),
    "2.4": (2, ["Examine the underlying basis of a business strategy.", "Compare the expected performance with the actual performance.",
                "Determine the reasons for deviations and analyse these reasons.", "Take corrective action so that deviations may be corrected."],
               ["Ignore any deviations, as the strategy has already been implemented.",
                "Evaluate a strategy only once, before it is implemented, and never again.",
                "Keep the strategy unchanged even when the results are poor."]),
    "2.5": (3, ["Market penetration: businesses focus on selling existing products into existing markets to increase their market share.",
                "Market development: businesses aim to sell their existing products in new markets.",
                "Product development: businesses aim to introduce new products into existing markets."],
               ["Market penetration: businesses sell new products in new markets that are unrelated to their current business.",
                "Market development: businesses take over their suppliers to control the supply of raw materials.",
                "Product development: businesses sell their existing products, unchanged, in new markets."]),
    "2.6.2": (2, ["Offer applicants pre-agreement statements.", "Disclose all costs of the loan.",
                  "Businesses should be registered with the National Credit Regulator.",
                  "Conduct an affordability assessment to ensure that consumers have the ability to meet their obligations."],
                 ["Add hidden costs to the loan after the agreement has been signed.",
                  "Grant credit to every applicant without checking whether they can afford it.",
                  "Refuse to tell consumers how much interest they will be charged."]),
    "2.7": (2, ["Businesses should include black people in shareholding, partnerships or franchises.",
                "Encourage small black investors to invest in big companies and share ownership.",
                "Large businesses should form joint ventures with small black-owned businesses and share business risks.",
                "More opportunities are created for black people to become owners or entrepreneurs."],
               ["Black shareholders may not vote at shareholders' meetings.",
                "Ownership is applied by paying black employees higher salaries than other employees.",
                "Businesses should sell shares only to people who already own large companies."]),
    "2.8": (2, ["Increases sales, revenue and business growth.", "Reduces the risk of relying on only one product for sales.",
                "Improves the business brand and image.",
                "Enables businesses to retain their competitive advantage by expanding into new, unexplored markets."],
               ["Guarantees that the business will never make a loss.", "Increases the risk, as the business relies on only one product.",
                "Allows the business to stop meeting the needs of its current customers."]),
    "3.2": (2, ["Businesses should outline the specific responsibilities, expectations and skills of the new position.",
                "Determine the successful candidate's strengths, weaknesses, interests and skills by subjecting the candidate to a range of "
                "psychometric tests.",
                "Determine the relationship between the position and the competencies of the new employee."],
               ["Place the new employee in any vacant position, regardless of his or her skills.",
                "Placement means dismissing new employees who do not perform in their first week.",
                "Placement is done before the vacancy is advertised."]),
    "3.3.2": (2, ["Promotes the resolution of labour disputes between employer and employees.",
                  "Protects the rights of employees and employers as outlined in the Constitution.",
                  "Workers cannot be easily dismissed, as bargaining council or CCMA processes need to be followed.",
                  "Provides for unresolved disputes to be referred to the Labour Courts."],
                 ["Employers may dismiss workers at any time without following any procedure.",
                  "The LRA prevents workers from joining trade unions.",
                  "The LRA sets the number of annual leave days that employees must receive."]),
    "3.4": (2, ["The employer may dismiss an employee for a valid reason, such as unsatisfactory job performance or misconduct.",
                "The employer may retrench some employees due to insolvency.",
                "Employees may decide to resign voluntarily for better job opportunities.",
                "The duration of the employment contract expires."],
               ["An employer may end a contract because the employee joined a trade union.",
                "An employer may end a contract because the employee is pregnant.",
                "A contract ends automatically every time the employee takes annual leave."]),
    "3.5": (2, ["Quality control inspects the final product, whereas quality assurance carries out checks during and after the production process.",
                "Quality control ensures that finished products meet the required standards, whereas quality assurance ensures that the required "
                "standards are met at every stage of the process.",
                "Quality control checks raw materials, machinery and products to maintain high standards, whereas quality assurance is the "
                "'building in' of quality as opposed to the 'checking of' quality."],
               ["Quality control builds quality into every stage of the process, whereas quality assurance only inspects the final product.",
                "Quality control aims to get the product 'right the first time', whereas quality assurance checks finished products for defects.",
                "Quality control and quality assurance both take place only after products have been sold to customers."]),
    "3.6.2": (2, ["Employees may not be adequately trained, resulting in poor quality products.",
                  "Decline in productivity because of stoppages.",
                  "The business's reputation may suffer because of poor quality or defective goods.",
                  "Decline in sales as more goods are returned by unhappy customers."],
                 ["Sales always increase, because customers prefer poor quality goods.",
                  "Productivity increases because there are more stoppages.",
                  "Staff turnover falls because employees receive less skills development."]),
    "3.7": (2, ["Prevents product defects and minimises wastage and customer complaints.",
                "Cost of production is reduced, as deviations from set standards can be corrected.",
                "Supports management to acquire the information needed to make informed decisions about processes.",
                "Benchmarking is used to find best practices in order to determine the competitive position of the business.",
                "Improves performance and maintains high quality standards."],
               ["Increases product defects and wastage, as fewer checks are done.", "Removes the need for quality control checks at key points.",
                "Strategies never need to be revised once quality has been checked once."]),
    "3.8": (2, ["Dealing quickly with negative publicity.", "Providing regular, positive press releases.",
                "Implementing sustainable corporate social investment (CSI) programmes.",
                "Good results of feedback from public surveys on the business's image."],
               ["Frequent incidents of negative publicity that are never answered.",
                "Refusing to speak to the media or the community about the business.",
                "Many customer complaints about rude telephone manners and untidy buildings."]),
    "4.2": (2, ["Have a clear vision, mission statement and measurable, realistic objectives in place.",
                "Identify strengths, weaknesses, opportunities and threats by conducting environmental scanning.",
                "Formulate alternative strategies to respond to the challenges.",
                "Implement selected strategies by communicating them to all stakeholders."],
               ["Skip the environmental scan, as the business already knows its market.",
                "Stop the process once the strategy has been implemented, without evaluating it.",
                "Keep the strategy secret from staff so that they cannot resist it."]),
    "4.5": (2, ["Employ people from the local community.", "Hire employees who are well conversant with the local language.",
                "Work together with community police forums and improve security in the business.",
                "Develop new products that address the lifestyle trends of customers."],
               ["Ignore the language spoken by the local community.", "Raise prices sharply in areas where incomes are low.",
                "Close the business whenever crime is reported in the area."]),
    "4.6": (2, ["Introduce new employees to management and colleagues to establish relationships.",
                "Give new employees a tour of the building.",
                "Familiarise new employees with the organisational structure and their supervisors.",
                "Explain safety regulations and rules, so that new employees understand their responsibilities."],
               ["Decide which of the applicants will be appointed.",
                "Keep new employees away from their colleagues until their probation ends.",
                "Dismiss new employees who make mistakes in their first week."]),
    "4.7": (2, ["Employees are required to contribute 1% of their basic salary towards UIF.",
                "Employers are required to contribute 1% of an employee's basic salary towards UIF.",
                "The fund also assists the dependants of a contributing worker who has died.",
                "The fund offers short-term financial assistance to workers when they become unemployed or are unable to work due to illness, "
                "maternity or adoption leave.",
                "Contributions are paid to the Unemployment Insurance Fund or SARS."],
               ["Employees contribute 10% of their basic salary towards UIF.", "Only employers contribute to UIF; employees pay nothing.",
                "The fund pays a monthly pension to all workers once they retire."]),
    "4.8.2": (2, ["Effective customer services are rendered, resulting in increased customer satisfaction.",
                  "Time and resources are used efficiently.", "A business has a competitive advantage over its competitors.",
                  "Improves the business image, as there are fewer defects and returns."],
                 ["Increases the number of defects and returns.", "Removes the need for any training of employees.",
                  "Guarantees that the business will have no competitors."]),
    "4.9": (2, ["Solve problems related to quality and implement improvements.", "Investigate problems and suggest solutions to management.",
                "Ensure that there is no duplication of activities in the workplace.",
                "Increase employees' morale and motivation to boost team spirit."],
               ["Decide on the salaries of all employees in the business.", "Replace the managers of the business.",
                "Increase the duplication of tasks in the workplace."]),
}
# A written part whose memo weighs two sides (positive / negative impact) plays as a SORT instead (variety, Murci 2026-10-10): each
# statement dragged to its side, or to "Not true" (the clearly wrong ones), 1 mark a statement; a grouped match.
SORTS = {
    "4.4": (["Positive impact", "Negative impact", "Not true"], [
        ("It eliminates the time and costs spent on lengthy civil court proceedings.", 0),
        ("Employers are protected from financial burden should an accident occur in the workplace, provided that the employer was not negligent.", 0),
        ("Claiming processes can be time consuming.", 1),
        ("Procedures required by the Act may be costly, as paperwork places an extra administrative burden on businesses.", 1),
        ("Employees must pay a monthly contribution to the Compensation Fund from their wages.", 2),
        ("COIDA allows employers to ignore safety measures, as every accident is covered anyway.", 2)]),
}


def sort_(n, q, marks, bins, rows, clues):
    order = list(range(len(rows)))
    random.Random("bs-p1-2025-11:sort:" + n).shuffle(order)
    rows = [rows[i] for i in order]
    assert marks == len(rows) and len(set(b for _, b in rows)) == len(bins), n
    return {"t": "match", "n": n, "marks": marks, "q": q + " Sort each statement.", "clues": clues, "left": [r for r, _ in rows],
            "right": bins, "a": [b for _, b in rows], "heads": ["STATEMENTS", "SORT INTO"], "groups": True}


for _m in missions_q2 + missions_q3 + missions_q4:
    for _k, _it in enumerate(_m["items"]):
        if _it["t"] == "rubric" and _it["n"] in SORTS:
            _bins, _rows = SORTS[_it["n"]]
            _m["items"][_k] = sort_(_it["n"], _it["q"], _it["marks"], _bins, _rows, _it["clues"])
        elif _it["t"] == "rubric" and _it["n"] in STATEMENTS:
            _each, _right, _wrong = STATEMENTS[_it["n"]]
            _m["items"][_k] = stmt(_it["n"], _it["q"], _it["marks"], _right, _wrong, _it["clues"], _each)
assert not [i["n"] for m in missions_q2 + missions_q3 + missions_q4 for i in m["items"] if i["t"] == "rubric"], "a written part left as rubric"


# ---- The essays as SECTIONS (Murci 2026-10-10): the memo's headings, each played as statements or a sort, their facts summing to the
# memo's cap of 32 (the memo's sub-maxima 10/14/12/10 scaled to 6/8/8/6 here, 10/14/10/12 to 6/8/6/8: the facts are capped at 32), then
# an INSIGHT part (LASO, 8) worked out from the picks (Layout: introduction + conclusion right; Analysis: every heading answered;
# Synthesis: every section right first time; Originality: the example statements picked). The essay's own wording goes to the
# mission's extract; the memo points above stay as the source.
def essay(nums, parts, examples, insight_clues):
    ex = [[n, next(p for p in parts if p["n"] == n)["opts"].index(t)] for n, t in examples]
    assert sum(p["marks"] for p in parts) == 32, [p["marks"] for p in parts]
    return parts + [{"t": "insight", "n": nums, "marks": 8, "q": "Insight: your essay's layout, analysis, synthesis and originality, worked out "
                     "from your picks.", "clues": insight_clues, "of": [p["n"] for p in parts], "intro": parts[0]["n"], "conclusion": parts[-1]["n"],
                     "examples": ex}]


INSIGHT_CLUES = ["Insight is earned from how you answered the sections.", "Right first time, every heading answered, and the examples picked."]
Q5_EX = ["For example, a construction company that ignores a compliance order is taken to the Labour Court.",
         "For example, an employee who was unfairly passed over for promotion because of her race is awarded compensation."]
q5_parts = essay("5.7", [
    stmt("5.1", "Introduction: pick the TWO statements that introduce this essay on the Employment Equity Act.", 2,
         ["The Employment Equity Act gives businesses the opportunity to create acceptable employment practices to correct inequalities of the past.",
          "Businesses that implement the EEA will benefit from improved and greater transformation processes in the workplace.",
          "The Act stipulates bodies that are responsible for monitoring compliance and imposing punitive measures for non-compliance."],
         ["The EEA allows businesses to choose whether or not to follow fair employment practices.",
          "The EEA applies only to businesses that are owned by the government.",
          "Businesses that ignore the EEA face no consequences."],
         ["An introduction says what the Act sets out to do and why it matters to a business.", "Check each card against what the Act requires."], 1),
    stmt("5.2", "Outline the purpose of the Employment Equity Act.", 6,
         ["It allows employees who do the same work to be paid equally.",
          "It eliminates discrimination on grounds of gender, race or disability in the workplace.",
          "It promotes equal opportunity and fair treatment in the workplace.",
          "It promotes diversity in the workplace by ensuring that people of diverse backgrounds are appointed.",
          "It protects employees from victimisation if they exercise the rights given to them by the EEA."],
         ["It allows employers to pay employees differently for the same work, based on their race.",
          "It requires businesses to appoint people from only one race group.",
          "It sets the number of annual leave days that employees must receive."],
         ["The Act's purpose is about fairness at work.", "Ask of each card: does it make the workplace fairer, and is it this Act's job?"], 2),
    sort_("5.3", "Discuss the impact of the Employment Equity Act on businesses.", 8, ["Positive impact", "Negative impact", "Not true"], [
        ("It encourages consultation between employer and employees.", 0),
        ("It provides employees with legal recourse if they have been unfairly discriminated against.", 0),
        ("Businesses are in a better position to negotiate contracts with the government.", 0),
        ("It increases the administration burden, as businesses must compile and submit employment equity reports.", 1),
        ("Skilled people from designated groups may demand higher salaries, which increases salary expenses.", 1),
        ("Positions often go unfilled because there are no suitable EEA candidates.", 1),
        ("It allows businesses to pay women less than men for the same work.", 2),
        ("It removes the need for businesses to report anything to the Department of Labour.", 2)],
        ["A positive helps the business or its staff; a negative costs the business time or money.",
         "A 'Not true' card says something the Act does not do."]),
    stmt("5.4", "Explain ways in which businesses can comply with the Employment Equity Act.", 8,
         ["Prepare an employment equity plan in consultation with employees.",
          "Submit the employment equity plan to the Department of Labour.",
          "Assign one or more senior managers to ensure implementation and monitoring of the employment equity plan.",
          "Display a summary of the Act where employees can clearly see it.",
          "Eliminate barriers that have an adverse impact on designated groups."],
         ["Keep the employment equity plan secret from employees and the Department of Labour.",
          "Pay designated groups less than other employees for work of equal value.",
          "Use appointment tests that favour one race group."],
         ["Complying means acting openly and fairly, and being able to prove it to the Department of Labour.",
          "Ask of each card: would a labour inspector be satisfied?"], 2),
    stmt("5.5", "Advise businesses on penalties they may face for non-compliance with this Act.", 6,
         ["A compliance order may be issued to businesses that do not comply with the EEA.",
          "Businesses may face heavy fines for non-compliance.",
          "The Department of Labour may block non-compliant companies from doing business with the government."] + Q5_EX,
         ["Non-compliant businesses are rewarded with extra government tenders.",
          "Labour inspectors are not allowed to visit a business or interview its employees.",
          "Penalties for non-compliance are paid by the employees, not the business."],
         ["What can the Department of Labour and the courts do to a business that ignores the Act?",
          "Ask of each card: does it punish the business, or reward it?"], 2),
    stmt("5.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["Businesses that implement the EEA enjoy a balanced workforce that represents the demographics of the community in which they operate.",
          "Penalties for non-compliance with the Act may have a negative financial implication for businesses."],
         ["The EEA has no effect on how businesses employ people.",
          "Businesses that comply with the EEA lose all their government contracts.",
          "It is cheaper for businesses to ignore the EEA, as there are no penalties."],
         ["A conclusion sums up why the Act matters to a business.", "The benefits of complying, the cost of not complying."], 2),
], [("5.5", Q5_EX[0]), ("5.5", Q5_EX[1])], INSIGHT_CLUES)

Q6_EX = ["For example, the HR manager of a supermarket books the boardroom for the interview day and sends every shortlisted candidate an SMS "
         "with the date and venue.",
         "For example, before interviewing applicants for an accountant post, the panel agrees on the same core questions about bookkeeping "
         "skills for every candidate."]
q6_parts = essay("6.7", [
    stmt("6.1", "Introduction: pick the TWO statements that introduce this essay on the human resources function.", 2,
         ["An accurate recruitment procedure enables businesses to appoint suitable candidates who meet the needs of the identified position.",
          "Businesses prefer internal recruitment methods as they give existing employees the opportunity to grow and showcase their skills.",
          "Businesses are guided by laws when drawing up the legal requirements of the employment contract."],
         ["Recruitment is only needed when a business is about to close down.",
          "An employment contract does not need to follow any law.",
          "Interviews work best when the interviewer does no planning beforehand."],
         ["An introduction says why the topic matters to a business.", "Check each card against how a careful HR manager works."], 1),
    stmt("6.2", "Outline the recruitment procedure as a human resources activity.", 6,
         ["The human resources manager should prepare a job analysis, including the job specification and job description, to identify "
          "recruitment needs.",
          "Choose the method of recruitment, such as internal or external, to reach suitable candidates.",
          "Vacancies can be advertised internally via internal email, word of mouth or staff notices.",
          "If internal recruitment is unsuccessful, external recruitment should be considered.",
          "Place the advertisement in the appropriate media that will ensure that the best candidates apply."],
         ["Appoint the first person who applies, without advertising the post.",
          "Leave the company's name and contact details out of the advertisement.",
          "Only ever recruit from outside the business, never from current staff."],
         ["Recruitment attracts suitable applicants to a vacancy.", "Ask of each card: would it bring in the best candidates?"], 2),
    sort_("6.3", "Discuss the impact of internal recruitment on businesses.", 8, ["Positive impact", "Negative impact", "Not true"], [
        ("It is cheaper and quicker to fill the post, as this method focuses on promoting existing employees.", 0),
        ("Placement is easy, as management knows the employees' skills and strengths.", 0),
        ("It provides opportunities for career paths within the business.", 0),
        ("Current employees may not bring new ideas into the business.", 1),
        ("Promoting a current employee may cause resentment amongst other employees.", 1),
        ("The number of applicants is limited to current staff only.", 1),
        ("It attracts more applicants than external recruitment, as anyone may apply.", 2),
        ("Promoted employees know nothing about how the business operates.", 2)],
        ["Internal recruitment fills a post from the business's own staff.",
         "A 'Not true' card says something that cannot happen when only current staff apply."]),
    stmt("6.4", "Explain the role of the interviewer before the interview.", 6,
         ["Book and prepare the venue for the interview.",
          "Develop a core set of questions based on the skills, knowledge and ability required.",
          "Read the application and verify the CV of every candidate for anything that may need to be explained."] + Q6_EX,
         ["Give each candidate a different set of questions so that no two interviews are the same.",
          "Tell only some of the shortlisted candidates where the interview will be held.",
          "Decide who will get the job before reading any of the applications."],
         ["Before the interview, the interviewer plans so that every candidate gets a fair chance.",
          "Ask of each card: would it make the interview fair and well organised?"], 2),
    stmt("6.5", "Advise businesses on the legal requirements of an employment contract.", 8,
         ["Both the employer and the employee must sign the contract.",
          "The employer and employee must agree to any changes to the contract.",
          "The remuneration package, including benefits, must be clearly indicated.",
          "The employment contract may not contain any requirements that are in conflict with the BCEA.",
          "The employer must allow the employee to read through the contract thoroughly before it is signed."],
         ["The employer may change the contract at any time without telling the employee.",
          "The contract may set working conditions below the minimum required by the BCEA.",
          "Only the employee needs to sign the contract."],
         ["A contract binds both parties, and the law sets its minimum terms.", "Ask of each card: is it fair to BOTH parties?"], 2),
    stmt("6.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["The correct recruitment procedure enables businesses to compile a proper job analysis that is used to identify suitable candidates "
          "for the vacancy.",
          "Businesses can avoid legal action by aligning their employment contracts with recent legislation."],
         ["Internal recruitment always makes existing employees feel unwanted.",
          "The success of an interview does not depend on any planning before the interview.",
          "Employment contracts do not need to follow the law, as long as both parties agree."],
         ["A conclusion sums up why the topic matters to a business.", "Good procedure, careful planning and the law."], 2),
], [("6.4", Q6_EX[0]), ("6.4", Q6_EX[1])], INSIGHT_CLUES)

for _m, _parts, _stem, _q in ((missions_c[0], q5_parts, Q5_STEM, "5"), (missions_c[1], q6_parts, Q6_STEM, "6")):
    _m["items"] = _parts
    _m["lead"] = "Build the essay section by section, then see your insight."
    _m["extract"] = "QUESTION " + _q + ": THE ESSAY\n\n" + _stem   # (the essay's wording in the shared-information card: on a phone it folds away)

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Business Studies", "title": "Business Studies P1", "sitting": "November 2025", "total_marks": 150, "time": "2 hours"},
    "sections": [
        {"title": "Section A", "total": 30, "missions": missions_a},
        {"title": "Section B", "total": 80, "answer_any": 2, "missions": missions_q2 + missions_q3 + missions_q4},
        {"title": "Section C", "total": 40, "answer_any": 1, "missions": missions_c},
    ],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 6), hand-transcribed from the paper and memo PDFs; no API call."},
        {"n": "2.6.1", "kind": "memo_issue", "detail": "The memo's second quote reads 'Financial Intelligent Centre Act'; the scenario prints 'Financial "
                                                       "Intelligence Centre Act', transcribed as printed in the scenario (the option is the scenario's sentence)."},
        {"n": "2.6.1", "kind": "no_fit", "detail": "Quote items (2.6.1, 3.6.1, 4.3.1) are played by picking the scenario's sentences: the memo awards "
                                                   "marks only for responses quoted from the scenario, so picking the right sentences is the same skill."},
        {"n": "2.7", "kind": "memo_issue", "detail": "The memo lists two challenges as ways to apply ownership ('Businesses sometimes find it difficult to "
                                                     "locate suitable black business partners...', 'Many black people cannot afford shares...') and an EME "
                                                     "scorecard rule (50% black ownership -> level 3); none of the three is used as a statement."},
        {"n": "4.4", "kind": "memo_issue", "detail": "The memo lists 'Employers have to pay a monthly amount to the Compensation Fund' under the "
                                                     "positives; not used as a sort row."},
        {"n": "4.3.2", "kind": "no_fit", "detail": "4.3.2's rows are 4.3.1's two challenges (as the paper's own table pairs them), so it is GATED "
                                                   "(after: 4.3.1): the player opens it only once 4.3.1 is answered."},
    ],
}
out = Path(__file__).parent / "out" / "bs-p1-2025-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs (no API call)",
                                                        "scope": "Questions 1 to 6 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for sec in paper["sections"]:
    print(sec["title"], "parts:", sum(len(m["items"]) for m in sec["missions"]), "marks:", sum(i["marks"] for m in sec["missions"] for i in m["items"]),
          "answer any:", sec.get("answer_any", "all"))
