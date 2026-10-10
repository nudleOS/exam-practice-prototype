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
  and sub-maxima, plus insight (LASO). Section B is "answer any TWO" and Section C "answer any ONE" (answer_any)."""
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
        ["Which Act protects the people who BUY products?", "Labelling tells a buyer what is inside the packaging."]),
    mcq("1.1.2", "Smith Stores uses outdated computers which prevent access to online transactions. This challenge is classified as a … "
        "factor of the PESTLE analysis.", ["technological", "political", "legal", "social"], 0,
        ["PESTLE: political, economic, social, technological, legal, environmental.", "What kind of problem is an old computer?"]),
    mcq("1.1.3", "Highway Manufacturing operate in the ... sector as they produce office chairs from timber and steel.",
        ["tertiary", "primary", "economic", "secondary"], 3,
        ["Primary takes from nature, secondary makes things, tertiary provides services.", "Turning timber and steel into chairs is ..."]),
    mcq("1.1.4", "The role of the interviewer during an interview is to …",
        ["make the interviewee feel at ease.", "ask clarity-seeking questions about the position.", "assist candidates in responding to questions.",
         "be inquisitive and show interest in the business."], 0,
        ["Three options describe what a CANDIDATE does.", "The interviewer runs the interview: what helps the candidate do well?"]),
    mcq("1.1.5", "Top Limited implemented the … step of the PDCA model by monitoring processes to determine whether they are functioning "
        "effectively.", ["do", "check", "plan", "act"], 1,
        ["Plan, Do, Check, Act: which step looks at results?", "Monitoring whether something works is ..."]),
]
WORDS = "selection;  job specification;  National Skills;  management;  threat;  placement;  weakness;  performance;  job description;  Human Resources"
q12 = [
    term("1.2.1", "The … Development Strategy aims to increase access to programmes that train people.", ["National Skills"],
         ["A national strategy behind the Skills Development Act.", "Two words from the list; the strategy develops ..."]),
    term("1.2.2", "Eezy Electronics are losing customers due to the high crime rate in the area. This is classified as a … in the SWOT "
         "analysis.", ["threat"], ["Is crime in the area inside or outside the business?", "SWOT: the outside things are opportunities and ..."]),
    term("1.2.3", "The component of the job analysis that outlines the duties and responsibilities of the position is known as …",
         ["job description"], ["A job analysis has two parts: one describes the JOB, one the PERSON.", "Duties belong to the job, not the person."]),
    term("1.2.4", "Themba, the human resources manager, conducts background checks of applicants who qualify for the job during the … "
         "procedure.", ["selection"], ["Recruitment attracts applicants; what comes next?", "Checking applicants before choosing one is part of ..."]),
    term("1.2.5", "Blue Manufacturer developed new methods and techniques to improve the quality of their products. This is known as "
         "quality …", ["management"], ["Methods and techniques to improve quality are how quality is ...", "TQM: total quality ..."]),
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
        ["SETA: Sector Education and Training Authority. One sector, its training.", "Think levies, grants, learnerships, skills plans."], each=2),
]
q23 = [
    rub("2.3.1", "Identify the force of Porter's Five Forces model that is applicable to BF. Motivate your answer by quoting from the scenario "
        "above.", 3, [
            "Competitive rivalry/Power of competitors.",
            "(Its motivation, quoted from the scenario:) 'BF sales have decreased as Bright Eyewear sells unique sunglasses at reasonable prices.'"],
        ["Who is taking BF's sales away?", "Another business selling the same kind of product is a ..."], worth=[2, 1],
        notes=["No marks for the motivation if the force is wrong; the force earns its marks even if the motivation is incomplete."]),
    rub("2.3.2", "Describe how businesses could apply ONE other force of Porter's Five Forces model to analyse their position in the market "
        "environment.", 3, [
            "Bargaining power of suppliers/Power of suppliers (force 2, a description 1): assess the power of the suppliers in influencing "
            "prices; suppliers that deliver high quality/unique/scarce products may have power over the business; the more powerful the "
            "suppliers, the less control the business has over them; the smaller the number of suppliers, the more powerful they may be as the "
            "choice of suppliers may be limited; identify the kind of power suppliers have in terms of the quality of products/services/"
            "reliability/ability to make prompt deliveries.",
            "Bargaining power of buyers/Power of buyers (force 2, a description 1): assess how easy it is for buyers/customers to drive "
            "prices down; determine the number of buyers/the importance of each buyer to the business and the cost of switching to other "
            "products; a few powerful buyers are often able to dictate their terms to the business; buyers buying in bulk can bargain for "
            "prices in their favour; if buyers can do without the business's products then they have more power to determine the prices and "
            "terms of sale; conduct market research to gather more information about its buyers.",
            "Threat of substitution/substitutes (force 2, a description 1): business's products that can be easily substituted weakens the "
            "power of the business in the market; establish whether the sellers of substitute products have improved their product/sell lower "
            "quality goods at lower prices; if the business sells unique products it will not be threatened by substitute products; assess if "
            "customers are using substitute products/services and determine reasons for using substitutes.",
            "Threat/Barriers of new entrants to the market (force 2, a description 1): if the barriers to enter the market are low, then it is "
            "easy for new businesses to enter the market/industry; if the business is highly profitable, it will attract potential competitors "
            "that want to benefit from high profits; new competitors can quickly/easily enter the market, if it takes little time/money to "
            "enter the market; if there are a few suppliers of a product/service but many buyers, it may be easy to enter the market."],
        ["Five forces: rivalry, suppliers, buyers, substitutes, new entrants. Not the one in 2.3.1.",
         "Name the force, then say how a business would use it to judge its position."], each=3,
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
    ["Evaluation looks back at a strategy already in use.", "Compare what was planned with what happened, then act on the difference."], each=2)]
q25 = [rub("2.5", "Discuss any TWO types of intensive strategies.", 6, [
    "Market penetration (strategy 2, a discussion point 1): new products penetrate an existing market at a low price, until it is well "
    "known to the customers and then the price increases; businesses focus on selling existing products into existing markets to increase "
    "their market share; businesses use market research on existing clients to decide on how to improve their marketing mix; aggressive "
    "marketing campaigns such as lowering/reducing prices are used to attract potential/existing clients; embark on an intensive advertising "
    "campaign to increase awareness and customer loyalty; employ more sales staff to improve sales/services.",
    "Market development (strategy 2, a discussion point 1): a growth strategy where businesses aim to sell their existing products in new "
    "markets; businesses target consumers in a potential market that is outside of its normal target market; increasing sales of existing "
    "products by finding new ways to develop new markets; prices are restructured/reviewed to cater for customers/consumers of all income levels.",
    "Product development (strategy 2, a discussion point 1): a growth strategy where businesses aim to introduce new products into existing "
    "markets/modifies an existing product; businesses generate new ideas/develop new products/services for existing/current markets; "
    "businesses conduct test marketing/market research to establish whether new products will be accepted by existing customers; new "
    "products may be different/of a higher quality than those of competitors."],
    ["Intensive strategies work harder with existing products or markets.", "Three of them: penetrate, develop the market, develop the product."], each=3,
    notes=["Mark the first TWO only (3 marks each: the strategy 2, its discussion 1)."])]
q26 = [
    pick("2.6.1", "Quote TWO ways in which MF complies with the National Credit Act (NCA), 2005 (Act 34 of 2005) from the scenario above.",
         sentences(MF), [1, 3], ["The NCA is about lending money and selling on credit.", "A cooling-off period belongs to a different Act."]),
    rub("2.6.2", "Recommend other ways in which businesses can comply with the National Credit Act.", 4, [
        "Offer applicants pre-agreement statements.", "Disclose all costs of the loan/No hidden costs should be charged/added.",
        "Businesses should be registered with the National Credit Regulator.",
        "Submit an annual compliance report to the National Credit Regulator.",
        "Conduct affordability assessment to ensure that consumers have the ability to meet their obligations.",
        "Verify the identity of clients and report suspicious transactions/train staff on their obligations in terms of FICA.",
        "Any other relevant answer related to other ways in which businesses can comply with the NCA."],
        ["Think about what a lender must do BEFORE it gives credit.", "Registration, reporting, honest costs, checking a client can pay."], each=2,
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
    ["Ownership means who holds the shares or the partnership.", "How can black people become part-owners of a business?"], each=2)]
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
    ["Diversifying means not putting all your eggs in one basket.", "What does a business gain from selling more than one kind of product?"], each=2)]
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
    ["Placement puts the new employee in the right position.", "Match what the job needs with what the person can do."], each=2)]
q33 = [
    term("3.3.1", "Name the salary determination method applied by FW in the scenario above.", ["Piecemeal", "Piece meal", "Piece-meal"],
         ["FW pays by how much each worker sells.", "Paid per piece (per roll), not per hour."]),
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
    ["A contract can end because of the employer, the employee, or time.", "Dismissal, retrenchment, resignation, retirement ..."], each=2)]
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
         sentences(BM), [1, 2], ["Which sentences describe what BM DOES?", "Avoiding repeated work and sharing responsibility both cut costs."]),
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
        ["What goes wrong for customers, staff and investors when quality slips?", "Each point: a problem, then its result."], each=2),
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
    ["Monitoring finds problems early; evaluating decides what to change.", "Think defects, costs, decisions, benchmarks."], each=2)]
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
    "OR — (option 2) Conduct an environmental analysis using models such as SWOT/PESTLE/Porter's Five Forces.",
    "OR — (option 2) Formulate a strategy, such as defensive/retrenchment strategy.",
    "OR — (option 2) Implement a strategy, using a template such as an action plan.",
    "OR — (option 2) Control/Evaluate/Monitor the implemented strategy to identify gaps/deviations in implementation.",
    "OR — (option 2) Take corrective action to ensure goals/objectives are met.",
    "Any other relevant answer related to the strategic management process."],
    ["It starts with where the business wants to go.", "Vision, scan the environment, formulate, implement, evaluate."], each=2)]
q43 = [
    pick("4.3.1", "Quote TWO challenges for GF from the scenario above.", sentences(GF), [1, 2],
         ["A challenge is a problem GF faces.", "One comes from outside the business, one from inside."]),
    match("4.3.2", "Classify GF's challenges according to the business environments.", GF_CH,
          ["Micro environment", "Market environment", "Macro environment"], [2, 0], 1,
          ["Micro: inside the business. Market: its immediate surroundings. Macro: the wider economy.",
           "Can GF control exchange rates? Can it control its own workers?"],
          heads=["CHALLENGES", "BUSINESS ENVIRONMENTS"], groups=True),
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
    ["COIDA compensates workers injured or made ill by their work.", "Impact can be positive, negative, or both: say what happens, then why."], each=2)]
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
    ["Induction is a new employee's first days.", "People, place, rules and roles."], each=2)]
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
         ["FL can AFFORD to do something.", "Which TQM element is about having the money and means?"]),
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
        ["A system that keeps quality high helps customers, staff and profits.", "Each point: a benefit, then what it leads to."], each=2),
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
    ["A quality circle is a small group of workers who meet about quality.", "What do they find, suggest and improve?"], each=2)]
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
# capped at 32), and insight (8). An essay's points are marked as the memo's are: 2 each, the introduction's 1 each.
INSIGHT = ["Insight (8), 2 each: Layout (an introduction, paragraphs and a conclusion, the words INTRODUCTION and CONCLUSION stated and "
           "explained); Analysis and interpretation (all headings addressed; interpreted correctly); Synthesis (only relevant facts); "
           "Originality (an example in any TWO of the four aspects, based on recent information, current trends and developments, not "
           "older than two years).",
           ]
ESSAY_NOTES = ["Facts are capped at 32 of the 40; no marks for content repeated from the introduction or the conclusion."]
q5 = [rub("5", "The Employment Equity Act (EEA), 1998 (Act 55 of 1998) was established to facilitate the transformation process in the workplace. "
          "The implementation of the EEA may have an impact on business operations. Businesses are compelled to comply with the requirements of "
          "this Act to avoid facing penalties for non-compliance.\n\nWrite an essay on the Employment Equity Act in which you include the following "
          "aspects:\n• Outline the purpose of the Employment Equity Act.\n• Discuss the impact of the Employment Equity Act on businesses.\n"
          "• Explain ways in which businesses can comply with the Employment Equity Act.\n• Advise businesses on penalties they may face for "
          "non-compliance with this Act.", 40, [
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
q6 = [rub("6", "Businesses following the correct recruitment procedures will attract the best applicants. The human resources manager could use "
          "the internal recruitment method to fill the available vacancies. The interviewer must be well prepared before conducting the interview. "
          "Both employers and employees should be aware of the legal requirements of an employment contract.\n\nWrite an essay on the human "
          "resources function in which you include the following aspects:\n• Outline the recruitment procedure as a human resources activity.\n"
          "• Discuss the impact of internal recruitment on businesses.\n• Explain the role of the interviewer before the interview.\n"
          "• Advise businesses on the legal requirements of an employment contract.", 40, [
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
