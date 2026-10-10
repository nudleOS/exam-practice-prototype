"""Business Studies P2 Nov 2025, the whole paper (Sections A, B and C), hand-transcribed into the catalogue format (as if Claude had
produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks and memo points are the
paper's and the memo's own; the clues are ours. No API call: the transcription is the source, kept in git (out/ is not).

  python tools/ingest/transcribe_bs_p2_2025_11.py
  python tools/ingest/ingest.py "<...>/Business Studies P2 Nov 2025 Eng.pdf" "<...>/Business Studies P2 Nov 2025 MG Eng.pdf" --id bs-p2-2025-11 --from-json

The memo's shapes map as for P1 (transcribe_bs_p1_2025_11.py's docstring): mcq, a word from the list as term, COLUMN A to B as
match (2 a pair), Name/Give/List any N as list, "Quote ... from the scenario" as pickn over its sentences, "Identify ... and
motivate by quoting" as rubric (the force/style/principle 2, the quote 1), explain/discuss/describe/advise/evaluate as rubric with
the memo's points, the essays as one rubric each (headings, sub-maxima, insight). Section B answer any TWO, C any ONE.
Those rubrics are the source only: the bottom block plays every written part as statements (STATEMENTS) or a sort (SORTS), and
both essays (5 and 6) as sections, one per memo heading, plus an insight part (2026-10-10)."""
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


READ = "Read the scenario below and answer the questions that follow."

# ---- Section A: Question 1, the question paper pages 3-5 and the memo ----
q11 = [
    mcq("1.1.1", "Adriaan earned … interest when he invested an amount of R30 000 in a fixed deposit for three years, at 12% simple interest per "
        "annum, with Axis Bank.", ["R40 800", "R44 691", "R10 800", "R14 691"], 2,
        ["Simple interest is paid on the amount invested only, every year the same.", "Interest = amount x rate x years. The question asks for the INTEREST, not the total."]),
    mcq("1.1.2", "The term 'unlimited liability' means that the owner's …",
        ["losses are restricted to the amount invested in the business.", "personal assets are protected against the debts of the business.",
         "personal debts need to be replaced by the business.", "personal assets may be seized to pay the debts of the business."], 3,
        ["Unlimited: there is no limit on what the owner can lose.", "If the business cannot pay its debts, where does the money come from?"]),
    mcq("1.1.3", "Jobe Bookkeeping educated their staff on the impact of fraud when dealing with … as a type of unprofessional business practice.",
        ["the unauthorised use of workplace funds and resources", "the abuse of work time", "unfair advertising", "sexual harassment"], 0,
        ["Fraud is about money and property.", "A bookkeeper looks after the books, not the adverts or the staff's conduct."]),
    mcq("1.1.4", "Team members often experience power struggles for the position of team leader during the … stage of team development.",
        ["forming", "storming", "performing", "adjourning"], 1,
        ["Forming, storming, norming, performing, adjourning.", "Which stage is about conflict?"]),
    mcq("1.1.5", "Catherine Textiles deals with HIV/Aids as a socio-economic issue by …",
        ["offering the best volunteering programmes to identify and attract potential employees.",
         "supporting poverty alleviation programmes that are offered by the government.",
         "rolling out antiretroviral treatment programmes for all infected employees.",
         "creating job opportunities for unemployed community members."], 2,
        ["Several options are good deeds, but only one deals with this particular issue.",
         "Think about what employees living with the virus need from their employer."]),
]
WORDS = "force-field analysis;  non-profit;  situational;  flip charts;  planet;  transformational;  Delphi technique;  posters;  state-owned;  people"
q12 = [
    term("1.2.1", "Willem applies different leadership styles based on different circumstances. This is known as the … leadership theory.",
         ["situational"], ["The leader reads what is happening around him and adjusts his style.", "Which word in the list describes circumstances?"]),
    term("1.2.2", "A … company creates job opportunities and offers essential services to the majority of citizens.", ["state-owned", "state owned"],
         ["Who provides essential services such as electricity and transport?",
          "Which kind of company belongs to the government rather than to private shareholders?"]),
    term("1.2.3", "Qama Electronics strategically places … in the business as a visual aid to attract customers.", ["posters"],
         ["Visual aids hang on walls to be seen by passing customers.", "Which visual aid works without a presenter standing next to it?"]),
    term("1.2.4", "Businesses implement the necessary changes after considering the driving and restraining aspects. This refers to … as a "
         "problem-solving technique.", ["force-field analysis", "force field analysis"],
         ["Picture two sides pushing against each other: one for the change, one against it.",
          "Which technique from the list weighs the pushes for and against before deciding?"]),
    term("1.2.5", "Highway Stores focuses on … as a triple bottom-line element when they support eco-friendly production methods.", ["planet"],
         ["The triple bottom line has three parts; one of them is about the natural world.", "Eco-friendly is about the environment."]),
]
COL_B = ["occur when employees lodge complaints with management in the workplace",
         "applies when assets are insured for more than their market value",
         "focuses on developing a moral compass for decision-making",
         "has limited continuity as the business ceases to exist upon resignation of the owner",
         "occur when there are clashes of opinions between two or more parties in the workplace",
         "focuses on upholding the reputation of the business",
         "investors receive higher dividends when the company makes profits",
         "applies when assets are insured for less than their market value",
         "has unlimited continuity as the business can exist beyond the resignation of the owner",
         "investors receive payments for dividends that were not paid out in previous years"]
q13 = [match("1.3", "Choose a description from COLUMN B that matches a term in COLUMN A.",
             ["Sole trader", "Cumulative preference shares", "Average clause", "Professional behaviour", "Grievances"],
             COL_B, [3, 9, 7, 5, 0], 2,
             ["Several descriptions come in pairs (more or less, limited or unlimited, complaints or clashes): read the small words.",
              "Cumulative means it adds up from year to year."])]
missions_a = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 10,
     "lead": "Various options are provided as possible answers to the following questions. Choose the answer.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Words from a list", "marks": 10,
     "lead": "Complete the following statements by using the word(s) provided in the list below.\n\n" + WORDS, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Matching columns", "marks": 10, "items": q13},
]

# ---- Section B: Question 2 (Business Ventures), the question paper page 6 and the memo pages 8-12 ----
MT = ("The managers of Mabizela Technologies apply different leadership styles in the workplace. Rachel takes all decisions alone, without "
      "consulting her staff members. Zaid, however, offers rewards to hardworking employees, which increases productivity.")
SM = ("Zintle, the financial manager of Starlight Marketing, considered various aspects when she designed her multimedia presentation. She kept "
      "the graphs simple by not mixing different styles. She conducted background checks on some of the audience members. Zintle also used key "
      "words to limit the information on each slide.")
q21 = [lst("2.1", "Name any TWO factors that should be considered when making investment decisions.", 2,
           [["Return on investment", "ROI"], ["Risk"], ["Investment term", "Investment period", "Term", "Period"], ["Inflation rate", "Inflation"],
            ["Taxation", "Tax"], ["Liquidity"]],
           ["What would you ask before putting your money somewhere?",
            "Some factors are about the investment itself, others about the economy around it."])]
q22 = [rub("2.2", "Elaborate on the meaning of excess as an insurance concept.", 4, [
    "Excess is the amount that the insured agrees to pay upfront when he/she takes out an insurance policy/the amount the insured agrees to "
    "pay upfront as stipulated in the insurance policy.",
    "A portion of the insurance claim that the insured will have to pay towards the cost of replacing/repairing goods/property concerned.",
    "Excess payments protect the insurer against fraudulent claims as the insured is less likely to submit a false claim when he/she needs to pay the amount upfront.",
    "It is the amount paid to the insurer when a claim for damages is lodged/in the event of a claim.",
    "It is not paid out to the insured when a claim is settled, but is recovered from the liable party by the insurer.",
    "Higher excess amounts keep the insurance premium lower and discourage fraud.",
    "Excess payment prevents the insured from claiming for minor damages.",
    "Any other relevant answer related to the meaning of excess as an insurance concept. A maximum of 2 for an example used as an explanation."],
    ["When you claim, who pays the first part of the cost?", "Why would an insurer want the insured to pay something too?"], each=2)]
q23 = [rub("2.3", "Explain the functions of the Johannesburg Securities Exchange (JSE).", 6, [
    "Gives opportunities to financial institutions such as insurance companies investing their surplus funds in shares.",
    "Serves as a barometer/indicator of economic conditions in South Africa.", "Keeps investors informed by publishing share prices daily.",
    "Acts as a link between investors and public companies.", "Shares are valued and assessed by experts.",
    "Small investors are invited to take part in the economy of the country through the buying/selling of shares.",
    "Venture capital market is made possible on the open market.", "Strict investment rules ensure a disciplined/orderly market for securities.",
    "Raises primary capital by encouraging new investments in listed companies.", "Mobilises the funds of insurance companies and other institutions.",
    "Regulates the market for trading in shares.", "Plans, researches and advises on investment possibilities.",
    "Ensures that the market operates in a transparent manner.", "Provides protection for investors through strict rules/legislation.",
    "Encourages short-term investment as shares can be sold at any time.",
    "Facilitates the electronic trading of shares/STRATE/Channels financial resources into productive economic activities.",
    "Enhances job creation and increases economic growth/development.",
    "Any other relevant answer related to the functions of the JSE."],
    ["The JSE is where shares in public companies are bought and sold.", "What does it do for investors, for companies and for the economy?"], each=2)]
q24 = [rub("2.4", "Identify the leadership styles applicable to MT. Motivate your answer by quoting from the scenario above.", 6, [
    "Autocratic leadership style.",
    "(Its motivation, quoted from the scenario:) 'Rachel takes all decisions alone, without consulting her staff members.'",
    "Transactional leadership style.",
    "(Its motivation, quoted from the scenario:) 'Zaid, however, offers rewards to hardworking employees, which increases productivity.'"],
    ["One manager decides alone; the other trades rewards for hard work.", "Name each style, then quote the sentence that shows it."],
    worth=[2, 1, 2, 1],
    notes=["Mark the first TWO only. Marks for a style even if its quote is incomplete; no marks for a motivation if its style is wrong."])]
q25 = [rub("2.5", "Describe the role of personal attitude in successful leadership.", 4, [
    "Positive attitude releases leadership potential for personal growth.", "A leader's good attitude can influence the success of the business.",
    "Leaders must know their strengths and weaknesses to apply their leadership styles effectively.",
    "Great leaders understand that the right attitude will set the right atmosphere.",
    "Leaders' attitude may influence employees'/teams' thoughts/behaviour.", "Leaders should model the behaviour that they want to see in team members.",
    "Successful leaders consider the abilities/skills of team members to allocate tasks/roles effectively.",
    "Enthusiasm produces confidence in a leader and inspires them to work even harder.",
    "A positive attitude is critical for good leadership because good leaders will stay with the task regardless of difficulties/challenges.",
    "Successful leaders have a constant desire to work and achieve personal/professional success.",
    "Leaders with a positive attitude know that there is always more to learn/space to grow.",
    "Any other relevant answer related to the role of personal attitude in successful leadership."],
    ["How does a leader's attitude spread to the team?", "Think about what the team sees in its leader, and what follows from it."], each=2)]
q26 = [
    pick("2.6.1", "Quote TWO aspects from the scenario above that Zintle considered when she designed her multimedia presentation.",
         sentences(SM), [1, 3], ["Which sentences are about the SLIDES themselves?",
                                 "Design aspects are choices about how the slides look and what is on them."]),
    rub("2.6.2", "Explain other aspects that must be considered when designing a multimedia presentation.", 4, [
        "Start with the heading/text which forms the basis of the presentation.", "Select the background to complement/enhance the text.",
        "Choose images that may help to communicate the message.", "Include/Create graphics to assist the information which is conveyed.",
        "Add special effects/sound/pictures/animation to make it interesting for the audience.",
        "Create hyperlinks to allow quick access to other files/documents/video clips.",
        "Use legible font and font size so that it is easy to see/read.", "Make sure there are no language and spelling errors.",
        "Use bright colours to increase visibility.",
        "Structure information in a logical sequence so that the audience can easily follow the content of the presentation.",
        "Any other relevant answer related to aspects that should be considered when designing a multimedia presentation."],
        ["Think about what helps an audience take in a slide at a glance.", "Each aspect, then why it helps the audience."], each=2,
        notes=["No marks for the aspects quoted in 2.6.1."]),
]
q27 = [rub("2.7", "Discuss the impact of government/RSA Retail Savings Bonds as a form of investment.", 6, [
    "Positive: guaranteed returns, as interest rate is fixed for the whole investment period.",
    "Positive: interest rates are market related and attract more investors.",
    "Positive: interest can be received twice a year making it a viable investment option.",
    "Positive: investment may be easily accessible, as cash may be withdrawn after the first twelve months.",
    "Positive: low risk/safe investment, as it is invested with the South African Government which cannot be liquidated.",
    "Positive: it is an affordable type of investment for all levels of income earners including pensioners.",
    "Positive: retail bonds are easily/conveniently obtained electronically/from any Post Office/directly from the National Treasury.",
    "Positive: no charges/costs/commissions payable on this type of investment.", "Positive: interest is usually higher than on fixed deposits.",
    "Positive: retail bonds are listed on the capital bond markets/on the JSE.",
    "Positive: investors younger than 18 years/minors may invest with the help of a legal guardian, which encourages saving from a young age.",
    "Negative: retail bonds cannot be ceded to banks/financial institutions as security for obtaining loans.",
    "Negative: a minimum of R500 for RSA Retail Savings Top Up Bonds/R1 000 for Fixed Rate Retail Savings Bonds must be invested, which may be "
    "difficult for some small investors to accumulate.",
    "Negative: retail bonds are not freely transferable amongst investors.",
    "Negative: investors need to have valid SA identification/should be older than 18 years which may discourage foreigners/young people to invest.",
    "Negative: penalties are charged for early withdrawals, if the savings is less than 12 months old.",
    "Any other relevant answer related to the positive and/or negative impact of Government/RSA Retail Savings Bonds as a form of investment."],
    ["You lend the government money and it pays you interest.",
     "Weigh how safe and how flexible this investment is, and what it costs to get in and out."], each=2)]
q28 = [rub("2.8", "Advise businesses on how management as a criterion could contribute to the success and/or failure of a public company.", 6, [
    "Success: managed by a board of competent highly skilled directors, which results in better decision-making.",
    "Success: the management of the company can improve since directors are accountable to shareholders.",
    "Success: shareholders can vote for/appoint the most capable directors to manage their company.",
    "Success: directors bring creative ideas, which encourages efficiency in the company.",
    "Failure: directors may not have a direct interest in the company, which can hamper growth and profit maximisation.",
    "Failure: large management structure can result in decision making taking time.",
    "Failure: directors' fees increase the company's expenses which reduces net profit.",
    "Failure: management may be open to legal challenges if their reports do not comply with the King Code.",
    "Failure: some shareholders may not exercise their voting rights resulting in choosing the wrong person as a director.",
    "Failure: directors may not be motivated to work very hard because shareholders decide on the directors' remuneration.",
    "Any other relevant answer related to how management as a criterion could contribute to the success and/or failure of a public company "
    "(success and/or failure; not necessarily a table)."],
    ["A public company is run by a board of directors chosen by shareholders.", "How can the board help the company, and how can it hold it back?"], each=2)]
missions_q2 = [
    {"id": "2.1", "title": "Question 2.1", "kind": "Investment decisions", "marks": 2, "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "Excess", "marks": 4, "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "The JSE", "marks": 6, "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Leadership styles", "marks": 6, "lead": "Read the scenario below and answer the question that follows.",
     "extract": "MABIZELA TECHNOLOGIES (MT)\n\n" + MT,
     "table": {"title": "Use the table below as a GUIDE to answer QUESTION 2.4.", "head": ["LEADERSHIP STYLES", "MOTIVATIONS"], "rows": [["1.", ""], ["2.", ""]]},
     "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Personal attitude", "marks": 4, "items": q25},
    {"id": "2.6", "title": "Question 2.6", "kind": "Multimedia presentations", "marks": 6, "lead": READ,
     "extract": "STARLIGHT MARKETING (SM)\n\n" + SM, "items": q26},
    {"id": "2.7", "title": "Question 2.7", "kind": "Retail Savings Bonds", "marks": 6, "items": q27},
    {"id": "2.8", "title": "Question 2.8", "kind": "Public companies", "marks": 6, "items": q28},
]

# ---- Section B: Question 3 (Business Roles), the question paper page 7 and the memo pages 12-17 ----
JP = ("The board of directors of Jaleel Pharmacy regularly applies the King Code principles in their business operations. JP developed a remedial "
      "programme to reduce air pollution levels and to protect the environment.")
KH = ("Klipland Hardware is experiencing conflict in the workplace. Some employees of KH display a lack of cooperation which causes delays in "
      "production. The management of KH sets unrealistic deadlines that increase the stress levels of employees. The employees of KH have "
      "difficulty with paying their own debt timeously.")
q31 = [lst("3.1", "List any FOUR problem-solving steps.", 4,
           [["Identify the problem"], ["Define the problem"], ["Identify possible solutions to the problem", "Identify possible solutions", "generate (possible solutions)", "brainstorm (possible solutions)"],
            ["Evaluate alternative solutions"], ["Choose the most appropriate solution", "Select the most appropriate alternative", "Choose the best solution"],
            ["Develop an action plan"], ["Implement the suggested solution", "Implement the action plan"],
            ["Monitor the implementation of the solution", "Monitor the action plan"], ["Evaluate the implemented solution"]],
           ["Start where a problem starts: noticing it.",
            "What must happen before a problem can be solved, and what comes after a solution is picked?"])]
q32 = [rub("3.2", "Outline the benefits of diversity in the workplace.", 6, [
    "Diversity in the workforce improves morale/motivation amongst employees.",
    "Businesses with a diverse workforce are more likely to have a good public image and attract more customers.",
    "Diversified workforce can give businesses a competitive advantage, as they can render better services.",
    "Workforce diversity improves the ability of a business to solve problems/innovate/cultivate diverse markets.",
    "A diversified workforce stimulates debate on new/improved ways of getting things done.",
    "Employees demonstrate greater loyalty to the business because they feel respected/accepted/understood.",
    "Employees value each other's diversity and learn to connect/communicate across lines of difference.",
    "Employees from different backgrounds can bring different perspectives to the business.",
    "Employees represent various groups and are therefore better able to recognise customer needs and satisfy consumers.",
    "Being respectful of differences/Demonstrating diversity makes good business sense/improves profitability.",
    "Diverse businesses ensure that their policies/practices empower every employee to perform at his/her full potential.",
    "Stakeholders increasingly evaluate businesses on how they manage diversity in the workplace.",
    "Any other relevant answer related to the benefits of diversity in the workplace."],
    ["How does a mix of people help the business, inside and in the market?",
     "Weigh each card: does it describe diversity correctly, and is the benefit real?"], each=2)]
q33 = [
    rub("3.3.1", "Identify the King Code principle applied by JP. Motivate your answer by quoting from the scenario above.", 3, [
        "Responsibility.",
        "(Its motivation, quoted from the scenario:) 'JP developed a remedial programme to reduce air pollution levels and to protect the environment.'"],
        ["Who is JP caring for by reducing pollution?", "The King Code principles: responsibility, accountability, transparency, fairness ..."],
        worth=[2, 1],
        notes=["No marks for the motivation if the principle is wrong; responsibility earns its marks even if the motivation is incomplete."]),
    rub("3.3.2", "Describe any ONE other King Code principle that businesses can apply to improve their ethical business conduct.", 3, [
        "Transparency.",
        "(Transparency, described:) decisions/actions must be clear to all stakeholders; staffing and other processes should be open "
        "and transparent; employees/shareholders/directors should be aware of the employment policies of the business; auditing and other reports must "
        "be accurate/available to shareholders/employees; regular audits should be done to determine the effectiveness of the business; business deals "
        "should be conducted openly so that there is no hint/sign of dishonesty/corruption; businesses should give details of shareholders' voting "
        "rights to them before/at the Annual General Meeting (AGM); the board of directors must report on both the negative and positive impacts of "
        "the business on the community/environment; the board should ensure that the company's ethics on information are reliable/relevant and "
        "implemented effectively.",
        "OR — Accountability.",
        "(Accountability, described:) there must be regular communication between management and stakeholders such as shareholders; "
        "the company should appoint internal and external auditors to audit financial statements; the board should ensure that the company's ethics on "
        "disclosure are motivated/proper/accurate and implemented effectively; businesses should be accountable/responsible for their "
        "decisions/actions; businesses should present accurate annual reports to shareholders at the AGM; top management should ensure that other "
        "levels of management are clear about their roles and responsibilities to improve accountability."],
        ["Choose a principle different from the one JP applied in 3.3.1.", "Name the principle, then describe what a business does to apply it."],
        worth=[2, 1, 2, 1],
        notes=["Mark the first ONE only; no marks for responsibility (3.3.1's principle)."]),
]
q34 = [rub("3.4", "Discuss communication as a criterion for successful team performance.", 6, [
    "A clear set of processes/procedures for teamwork ensures that every team member understands his/her role.",
    "Efficient/Good communication between team members may result in quick decisions.", "Quality feedback improves the morale of the team.",
    "Open/Honest discussions lead to effective solutions of problems.",
    "Continuous review of team progress ensures that team members can rectify mistakes/act pro-actively to ensure that goals/targets are reached.",
    "Any other relevant answer related to communication as a criterion for successful team performance."],
    ["How does talking well together help a team work well together?",
     "Think about what a team gains when everyone knows what is going on and can speak up."], each=2)]
q35 = [
    pick("3.5.1", "Quote TWO causes of conflict at KH from the scenario above.", sentences(KH), [1, 2],
         ["Conflict at work comes from how people work together.",
          "Ask of each sentence: does it describe a cause, and is that cause in the workplace?"]),
    rub("3.5.2", "Explain how businesses should handle conflict in the workplace.", 4, [
        "Acknowledge that there is conflict between employers/employees/parties in the workplace.",
        "Identify the cause of the conflict to get clarity on its nature.",
        "Arrange time and place for negotiations where all employees involved are present.", "Arrange a meeting between conflicting employers/employees.",
        "Make intentions for intervention clear so that parties involved may feel at ease.",
        "Arrange a pre-negotiation meeting where workers/complainants will be allowed to state their case/views separately.",
        "Each party has the opportunity to express his/her own opinions/feelings.",
        "Conflicting parties may recognise that their views are different during the meeting.",
        "Analyse/Evaluate the cause(s) of conflict by breaking it down into different parts.",
        "Evaluate the views expressed and make an objective decision.", "Blame shifting should be avoided and a joint effort should be made.",
        "Direct conflicting parties towards finding/focusing on solutions.", "Devise/Brainstorm possible ways of resolving the conflict.",
        "Conflicting parties agree on criteria to evaluate the alternatives.", "Select/Implement the best solution that will deal with the conflict.",
        "Provide opportunities for parties to agree on the best solution.", "Evaluate/Follow up on the implementation of the solution(s).",
        "Monitor progress to ensure that the conflict has been resolved.", "Source experts on handling conflict from outside the business.",
        "Any other relevant answer related to how businesses should handle conflict in the workplace."],
        ["Handling conflict is a process: which cards move it toward a fair solution?",
         "Would each step make the conflict smaller, or bigger?"], each=2),
]
q36 = [rub("3.6", "Discuss the advantages of corporate social responsibility (CSR) on businesses.", 6, [
    "May attract experienced employees/increase the pool of skilled labour which could increase productivity.",
    "Positive/Improved image as the business looks after employees/conducts itself in a responsible way.",
    "Businesses may have a competitive advantage, resulting in good publicity/an improved reputation.",
    "Promotes customer loyalty resulting in more sales.", "CSR projects may be used as a marketing strategy to promote their products.",
    "Businesses enjoy the goodwill/support of communities.", "CSR projects promote teamwork within businesses.",
    "CSR helps to attract investors because of increased profits/income/growth.", "Gives businesses tax advantages such as tax reduction/-rebates.",
    "The government is less likely to enforce issues through legislation to businesses that voluntarily participate in CSR projects.",
    "Employees feel as if they are making a difference in working for the business.",
    "It helps to retain staff/lower staff turnover as employees' health and safety are considered.",
    "Improves the health of its employees through focused CSR projects.", "Attracts investors when the business is included in the JSE SRI.",
    "Any other relevant answer related to the advantages of CSR on businesses."],
    ["CSR: a business looking after its people and its community.",
     "Ask of each card: is it a real gain, or a promise too good to be true?"], each=2)]
q37 = [rub("3.7", "Evaluate the impact of the nominal group technique.", 6, [
    "Positive: it provides time to think about the question in silence before responding.",
    "Positive: voting on the ideas is anonymous and may be more reliable/honest.", "Positive: strong technique for preventing conformity to group pressure.",
    "Positive: each team member/director has a chance to participate without interference from other team members.",
    "Positive: everyone in the group is given an opportunity to contribute to the discussion, while avoiding the likelihood of one person dominating the group process.",
    "Positive: enables the group to generate and clarifies a large amount of ideas quickly, and democratically prioritises them.",
    "Positive: it encourages participants to confront issues through constructive problem solving.",
    "Negative: small groups limit participation and are pre-selected.", "Negative: it is time consuming, as each member must make a presentation.",
    "Negative: suggestions may not be as creative as when a group throws ideas around.",
    "Negative: good ideas can be voted out because its potential cannot be developed further.",
    "Negative: it minimises discussion, and thus does not allow the full development of ideas.",
    "Negative: ideas/inputs made by members may not converge and cannot lead to the same solution(s).",
    "Negative: it is hard to implement it effectively with large groups unless very carefully planned beforehand.",
    "Negative: requires extended advance preparation, which means that it cannot be a spontaneous technique.",
    "Any other relevant answer related to the positive and/or negative impact of the nominal group technique."],
    ["Members write ideas alone, share them, then vote.", "Evaluate: say what is good, what is not, and why."], each=2)]
missions_q3 = [
    {"id": "3.1", "title": "Question 3.1", "kind": "Problem-solving steps", "marks": 4, "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Diversity", "marks": 6, "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "The King Code", "marks": 6, "lead": READ, "extract": "JALEEL PHARMACY (JP)\n\n" + JP, "items": q33},
    {"id": "3.4", "title": "Question 3.4", "kind": "Team communication", "marks": 6, "items": q34},
    {"id": "3.5", "title": "Question 3.5", "kind": "Conflict", "marks": 6, "lead": READ, "extract": "KLIPLAND HARDWARE (KH)\n\n" + KH, "items": q35},
    {"id": "3.6", "title": "Question 3.6", "kind": "Corporate social responsibility", "marks": 6, "items": q36},
    {"id": "3.7", "title": "Question 3.7", "kind": "Nominal group technique", "marks": 6, "items": q37},
]

# ---- Section B: Question 4 (Miscellaneous topics), the question paper page 8 and the memo pages 17-21 ----
TA = ("Thandokazi Attorneys strive to promote creative thinking in the workplace. They ensure that the work environment is free from high noise "
      "levels and distractions. The management of TA provides employees with fewer breaks to optimise workplace productivity. TA also encourage "
      "employees to come up with new ways of performing their duties.")
q41 = [lst("4.1", "Give any TWO examples of non-insurable risks.", 2,
           [["Nuclear weapons", "War", "Earthquakes"], ["Changes in fashion and trends", "Changes in fashion"], ["Changes in technology", "Improvement in technology"],
            ["Irrecoverable debts", "Bad debts"], ["High rate of inflation", "Inflation"], ["Financial loss due to bad management", "Bad management"],
            ["Possible failure of a business", "Business failure"], ["Shoplifting during business hours", "Shoplifting"],
            ["Loss of income if stock is not received in time", "Time that elapses between the ordering and delivery of goods"],
            ["Losses/damages incurred because of illegal marketing malpractices", "Illegal marketing activities"]],
           ["An insurer will not cover a risk it cannot measure or one the business causes itself.",
            "Think of losses no insurer can predict or price, or losses caused by the market or by the business's own decisions."])]
q42 = [
    term("4.2.1", "PL raised additional capital by borrowing money from the public.", ["Debentures", "Debenture"],
         ["Borrowing from the public, not selling shares.", "A long-term loan certificate a company issues."]),
    term("4.2.2", "Employees of PL make monthly contributions to an informal savings scheme from which they will be able to make future withdrawals.",
         ["Stokvels", "Stokvel", "Mutual funds", "Mutual fund"],
         ["An informal savings club.", "Members pay in each month and take turns or withdraw later."]),
]
q43 = [rub("4.3", "Explain the difference between management and leadership.", 4, [
    "Management (submax 2): guides human behaviour; communicates through management functions, such as line function; administers "
    "plans/programs/tasks to reach targets; controls systems and procedures to get the job done; focuses on the bottom line/short/medium term; a "
    "person becomes a manager because of the position in which he/she is appointed; manages the process of getting things done by exercising "
    "responsibility; managers have power because of the position of authority into which they are appointed; enforce rules on subordinates/ensure "
    "that tasks are completed; management is instructional in their approach by guiding/training/directing employees; management is task "
    "orientated and focuses on completing goals/deadlines/processes; manages by planning/organising/leading/control; management 'does things right' "
    "by focusing on efficiency and execution of tasks; manages the 'how' and 'when' regarding processes/timelines of a task.",
    "Leadership (submax 2): influences human behaviour; communicates by means of interaction/behaviour/vision/values/charisma; innovates/encourages "
    "new ideas to increase productivity; inspires staff to trust and support each other; focuses on the horizon/long term; leaders are born with "
    "natural/instinctive leadership skills; guides/leads people to become active participants; leaders have power/influence because of his/her "
    "knowledge/skills/intelligence; always trying to find more efficient ways of completing tasks; leadership is inspirational in their approach by "
    "energizing/motivating/encouraging employees; leadership is people orientated and focuses on building relationships/morale/development; leads "
    "by example/trust/respect; leadership 'does the right things' by focusing on the vision and strategies; leadership asks 'what' and 'why' to "
    "foster a deeper understanding for improvement."],
    ["Think about what each one focuses on, and how each one gets people to act.",
     "A difference is only right when BOTH halves are right: check each side."], each=2,
    notes=["Not necessarily a table, and the two need not link, but the difference must be clear: a maximum of 2 if it is not, or if only one "
           "side is given."])]
q44 = [rub("4.4", "Discuss the advantages of a personal liability company.", 6, [
    "Has its own legal identity and shareholders have no direct legal implications/limited liability.", "Has the potential for good long-term growth.",
    "Pays tax at a fixed tax rate to the South African Revenue Services (SARS).",
    "Appoints a board of directors with the required expertise/experience/knowledge to make business decisions.",
    "Is not required to file annual financial statements with the Companies and Intellectual Property Commission (CIPC).",
    "Is a legal person and can sign contracts in its own name.", "Is not required to publish private financial statements for the general public.",
    "Has continuity of existence/perpetual/unlimited lifespan as the lifespan of the business is not dependent on the lifespan of the owners.",
    "Is managed by at least one competent/highly skilled director.", "Can be sold as it is a separate legal entity in its own right.",
    "Can easily raise capital by issuing shares to their shareholders.",
    "Can raise large amounts of capital since there is no limit on the number of shareholders.",
    "Can improve their management since directors are accountable to shareholders.",
    "Directors are personally liable if they knowingly participate in carrying out business in a reckless/fraudulent manner.",
    "Any other relevant answer related to the advantages of a personal liability company."],
    ["A personal liability company (Inc.) is a company, often of professionals.",
     "Compare it with a sole trader: what does being a registered company give it?"], each=2)]
q45 = [rub("4.5", "Advise presenters on the factors that they should consider during a presentation.", 4, [
    "Establish credibility by introducing yourself as the presenter at the start.", "Mention/Show the most important information first.",
    "Make the purpose/main points of the presentation clear at the start of the presentation.", "Use suitable section titles/headings/sub-headings/bullets.",
    "Summarise the main points of the presentation to conclude the presentation.",
    "Stand in a good position/upright, where the audience can clearly see the presenter/presentation.", "Avoid/Refrain from hiding behind equipment.",
    "Do not ramble on at the start to avoid losing the audience/their interest.",
    "Capture listeners' attention/Involve the audience with a variety of methods such as short video clips/sound effects/humour.",
    "Maintain eye contact with the audience.", "Be audible/loud and clear to all listeners/audience.",
    "Vary the tone of voice/tempo within certain sections to prevent monotony.",
    "Make the presentation interesting with visual aids/anecdotes/examples/Use visual aids effectively.",
    "Use appropriate gestures to emphasize certain points.", "Speak with energy and enthusiasm.", "Pace yourself by not rushing or talking too slowly.",
    "Keep the presentation short and simple.", "Conclude/End with a strong/striking ending that will be remembered.",
    "Ensure that the audience will leave with specific information.", "Manage time effectively to allow time for questions.",
    "Any other relevant answer related to the factors to be considered by the presenter while presenting."],
    ["DURING the presentation: how you stand, speak and hold the audience.",
     "Ask of each card: would it keep the audience with you, or lose them?"], each=2)]
q46 = [lst("4.6", "Name the FOUR corporate social investment (CSI) focus areas.", 4,
           [["Community"], ["Rural development"], ["Employees"], ["Environment"]],
           ["Where does a business invest to do good?",
            "Think of who and what a business's social investment can benefit, inside and outside the business."])]
q47 = [rub("4.7", "Describe the importance of team dynamic theories in improving team performance.", 6, [
    "Team dynamic theories explain how effective teams work/operate.", "Businesses are able to allocate tasks according to the roles of team members.",
    "Team members can maximise performance as tasks are allocated according to their abilities/skills/attributes/personalities.",
    "Team members with similar strengths may compete for team tasks/responsibilities that best suit their abilities/competencies.",
    "Theories assist team leaders to understand the personality types of team members so that tasks are assigned more effectively.",
    "Conflict may be minimised when team members perform different roles.",
    "Any other relevant answer related to the importance of team dynamic theories in improving team performance."],
    ["Theories such as Belbin's describe the roles people play in a team.", "Knowing the roles, how can a leader use them?"], each=2)]
q48 = [
    pick("4.8.1", "Quote TWO ways from the scenario above in which TA creates an environment that promotes creative thinking.", sentences(TA), [1, 3],
         ["Which sentences help people think creatively?",
          "Ask of each sentence: is it something TA does, and would it help new ideas to flow?"]),
    rub("4.8.2", "Explain other ways in which businesses can create an environment that promotes creative thinking in the workplace.", 4, [
        "Emphasise the importance of creative thinking to ensure that all staff know that management wants to hear their ideas.",
        "Make time for brainstorming sessions to generate new ideas such as regular workshops/generate more ideas/build on one another's ideas.",
        "Place suggestion boxes around the workplace and keep communication channels open for new ideas.",
        "Train staff in innovative techniques such as creative problem-solving skills/mind-mapping/lateral thinking.",
        "Encourage job swops within the organisation/study how other businesses are doing things.",
        "Respond enthusiastically to all ideas and never let anyone feel less important.",
        "Reward creativity by offering employees reward schemes/introduce incentives for staff members who come up with useful creative ideas.",
        "Any other relevant answer related to other ways in which businesses can create an environment that promotes creative thinking."],
        ["How can a business show that it wants new ideas?",
         "Ask of each card: would staff feel safe and keen to share an idea?"], each=2,
        notes=["No marks for the ways quoted in 4.8.1."]),
]
q49 = [rub("4.9", "Recommend ways in which businesses can deal with the pricing of goods in rural areas as a type of unethical business practice in the workplace.", 4, [
    "Lobby with other businesses/suppliers in the area to convince the government to improve infrastructure in the rural area.",
    "Charge fair/market-related/affordable prices for goods and services.", "Be willing to avoid unethical business practices to attract customer loyalty.",
    "Investigate cost-effective ways of transporting products/Hire a large truck to combine deliveries to shop owners in the same area.",
    "Work together with suppliers to share delivery costs to remote rural area.", "Buy in bulk to get a discount to avoid charging high prices.",
    "Any other relevant answer related to ways in which businesses can deal with the pricing of goods in rural areas."],
    ["Rural prices are high mostly because of transport costs.", "How can a business cut those costs instead of passing them on?"], each=2)]
missions_q4 = [
    {"id": "4.1", "title": "Question 4.1", "kind": "Non-insurable risks", "marks": 2, "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Investment opportunities", "marks": 4,
     "lead": "Identify the type of investment opportunity applicable to Platinum Ltd (PL) in EACH of the following statements:", "items": q42},
    {"id": "4.3", "title": "Question 4.3", "kind": "Management and leadership", "marks": 4, "items": q43},
    {"id": "4.4", "title": "Question 4.4", "kind": "Personal liability companies", "marks": 6, "items": q44},
    {"id": "4.5", "title": "Question 4.5", "kind": "Presenting", "marks": 4, "items": q45},
    {"id": "4.6", "title": "Question 4.6", "kind": "CSI focus areas", "marks": 4, "items": q46},
    {"id": "4.7", "title": "Question 4.7", "kind": "Team dynamics", "marks": 6, "items": q47},
    {"id": "4.8", "title": "Question 4.8", "kind": "Creative thinking", "marks": 6, "lead": READ, "extract": "THANDOKAZI ATTORNEYS (TA)\n\n" + TA, "items": q48},
    {"id": "4.9", "title": "Question 4.9", "kind": "Rural pricing", "marks": 4, "items": q49},
]

# ---- Section C: the essays (answer any ONE), the question paper page 9 and the memo pages 22-32 ----
INSIGHT = ["Insight (8), 2 each: Layout (an introduction, paragraphs and a conclusion, the words INTRODUCTION and CONCLUSION stated and "
           "explained); Analysis and interpretation (all headings addressed; interpreted correctly); Synthesis (only relevant facts); "
           "Originality (an example in any TWO of the four aspects, based on recent information, current trends and developments, not "
           "older than two years).",
           ]
ESSAY_NOTES = ["Facts are capped at 32 of the 40; no marks for content repeated from the introduction or the conclusion."]
Q5_STEM = ("Businesses are required to make a clear distinction between insurance and assurance for future financial planning. A sound knowledge "
           "of compulsory insurance is beneficial for businesses. Businesses receive the benefits of insurance when they successfully apply the "
           "insurance principles.\n\nWrite an essay on investment: insurance in which you include the following aspects:\n• Outline the differences "
           "between insurance and assurance.\n• Explain the THREE types of compulsory insurance.\n• Discuss the advantages of insurance.\n• Advise "
           "businesses on the following principles of insurance:\n  o Utmost good faith\n  o Insurable interest")
q5 = [rub("5", Q5_STEM, 40, [
    "Introduction (any 2 x 1): the value of insurance and assurance for both businesses and individual are indispensable to insure against "
    "unforeseen eventualities.",
    "Introduction: businesses are required by law to take out the relevant compulsory insurance.",
    "Introduction: businesses are exposed to many risks during their business operations, so they need to take out insurance in order to protect "
    "themselves against these risks.",
    "Introduction: breach of any insurance principles could invalidate any claims that may arise should losses or damages occur.",
    "Insurance and assurance (max 12; insurance submax 6, assurance submax 6; 2 each, an example 1): insurance is based on the principle of indemnity.",
    "Insurance: the insured transfers the cost of potential loss to the insurer at a premium.",
    "Insurance: it covers a specified event that may occur.",
    "Insurance: applicable to short-term insurance.",
    "Insurance, examples (1): property insurance/cash in transit/theft/burglary/fire.",
    "Assurance: based on the principle of security/certainty.",
    "Assurance: the insurer undertakes to pay an agreed sum of money after a certain period has expired/on the death of the insured person, "
    "whichever occurred first.",
    "Assurance: specified event is a certainty, but the time of the event is uncertain.",
    "Assurance: applicable to long-term insurance.",
    "Assurance, examples (1): life insurance/endowment policy/retirement annuities.",
    "Compulsory insurance (max 16; the first THREE types, each the type 2 + explanation 4, submax 6): Unemployment Insurance Fund/UIF.",
    "UIF: the UIF provides short-term benefits to workers who have been working and become unemployed for various reasons.",
    "UIF: the UIF provides financial assistance for a limited period to the dependants of a deceased employee who was registered with/contributed to the UIF.",
    "UIF: businesses contribute 1% of basic wages towards UIF, therefore reducing the expense of providing UIF benefits themselves.",
    "UIF: employees contribute 1% of their basic wage to UIF as a financial safety net/back up funds.",
    "UIF: businesses are compelled to register their employees with the fund and pay the 2% levy contributions to SARS/UIF monthly.",
    "UIF: the contribution of businesses towards UIF increases the amount paid out to employees who become unemployed.",
    "UIF: all employees who work at least 24 hours per month are required to be registered for UIF/contribute to the UIF.",
    "UIF: employees who become unemployed must register with the Department of Labour, and all valid claims will be processed by the UIF.",
    "UIF: it is an affordable contribution that makes it possible for businesses to appoint substitute workers in some instances.",
    "UIF: businesses cannot be held responsible for unemployment cover as the UIF pays out to contributors directly/dependants of deceased contributors.",
    "UIF: employers will be held personally liable for unemployment cover if the UIF deductions are not made/paid timeously.",
    "UIF: employees who resigned/absconded or have been suspended from their jobs cannot claim from the UIF.",
    "Compensation Fund/Compensation for Occupational Injuries and Diseases Act/COIDA (type 2 + explanation 4).",
    "COIDA: the fund covers/compensates employees/domestic workers for occupational diseases and injuries incurred at work/the workplace.",
    "COIDA: compensation paid is determined by the degree of disablement.",
    "COIDA: the contribution payable is reviewed every few years according to the risk associated with that type of work.",
    "COIDA: all employers are obliged to register with the Compensation Fund so that employees may be compensated for accidents and diseases sustained in the workplace.",
    "COIDA: the fund covers employers for any legal claim that workers may bring against them.",
    "COIDA: employers are required to report all accidents within 7 days and occupational diseases within 14 days to the Compensation Commissioner.",
    "COIDA: employers are responsible for contributing towards the fund and may not claim money back from employees/deduct contributions from wages.",
    "COIDA: in the event of the death of an employee as a result of a work-related accident/disease, his/her dependant(s) will receive financial support.",
    "COIDA: employees do not have to contribute towards this fund.",
    "COIDA: employees receive medical assistance provided there is no other party/medical fund involved.",
    "Road Accident Fund/RAF/Road Accident Benefit Scheme/RABS (type 2 + explanation 4).",
    "RAF/RABS insures road-users against the negligence of other road users.",
    "RAF/RABS: provides compulsory cover for all road users in South Africa, which include South African businesses.",
    "RAF/RABS: drivers of business vehicles are indemnified against claims by persons injured in vehicle accidents.",
    "RAF/RABS: the social insurance cover, however, does not extend to drivers of motor vehicles that are found to be negligent.",
    "RAF/RABS is funded by a levy on the sale of fuel/diesel/petrol.",
    "RAF/RABS: the amount that can be claimed for loss of income is limited by legislation.",
    "RAF/RABS: the next of kin of workers/breadwinners who are injured/killed in road accidents, may claim directly from RAF/RABS.",
    "RAF/RABS: injured parties and negligent drivers are both covered by RAF/RABS.",
    "RAF/RABS: the injured party will be compensated, irrespective of whether the negligent driver is rich/poor/insured/uninsured.",
    "RABS aims to provide a benefit scheme that is reasonable/equitable/affordable/sustainable.",
    "RABS aims to simplify/speed up the claims process as victims of road accidents no longer have to prove who caused the accident.",
    "RABS enables road accident victims' speedy access to medical care as delays due to the investigation into accidents has been minimised.",
    "Advantages of insurance (max 10, 2 each): transfers the risk from businesses/insured to insurance companies/an insurer.",
    "Advantages: transfer of risk is subject to the terms and conditions of the insurance contract.",
    "Advantages: protects businesses against theft/loss of stock and/or damages caused by natural disasters such as floods/storm damage.",
    "Advantages: businesses will be compensated for insurable losses, such as the destruction of property through fire.",
    "Advantages: business' assets such as vehicles/equipment/buildings need to be insured against damage and/or theft.",
    "Advantages: businesses are protected against the loss of earnings, such as strikes by employees which may result in losses worth millions.",
    "Advantages: protects businesses against dishonest employees.",
    "Advantages: life insurance can be taken on the life of partners in a partnership to prevent unexpected loss of capital.",
    "Advantages: should the services of key personnel be lost due to accidents/death, the proceeds of an insurance policy can be paid out to the business/beneficiaries.",
    "Advantages: replacement costs for damaged machinery/equipment are very high therefore insurance can reduce/cover such costs.",
    "Advantages: protects businesses from claims made by members of the public for damages that businesses are responsible for.",
    "Advantages: protects businesses against losses due to death of a debtor.",
    "Principles of insurance (max 8): Utmost good faith (submax 4, 2 each): insured has to be honest in supplying details when entering in an insurance contract.",
    "Utmost good faith: both parties/insurer and insured must disclose all relevant facts.",
    "Utmost good faith: insured must disclose everything that may affect the extent of the risk.",
    "Utmost good faith: details/information supplied when claiming should be accurate/true.",
    "Insurable interest (submax 4, 2 each): insured must prove he/she will suffer a financial loss if the insured object is damaged/lost/ceases to exist.",
    "Insurable interest: an insurable interest must be expressed in financial terms.",
    "Insurable interest: insured must have a legal relationship with the insured object in the contract.",
    "Conclusion (any 1 x 2): insurance and assurance may differ as they describe the nature of the risk that may or may not occur for both individuals and businesses.",
    "Conclusion: compulsory insurance compels individuals/businesses to be clear about the legal implications and are regulated by the state.",
    "Conclusion: importance of insurance is to protect the business against the risks that they are exposed during business operations.",
    "Conclusion: it is therefore important that certain principles such as utmost good faith and insurable interest must be adhered to by both "
    "parties to ensure the validity of the contract.",
    "Any other relevant answer under each heading."] + INSIGHT,
    ["Plan the four aspects as headings between an introduction and a conclusion.",
     "Insurance vs assurance: indemnity vs certainty. Compulsory: UIF, COIDA, RAF. Then advantages, then the two principles."],
    notes=["Insurance and assurance: not necessarily a table; the differences need not link but must be clear; a maximum of 6 if the "
           "difference is not clear/only one side is given."] + ESSAY_NOTES)]
Q6_STEM = ("Employers are obligated to take care of the human health and safety of employees in the workplace. Businesses must be able to implement "
           "ways to deal with human rights and apply strategies to protect the environment and human health. They must also have knowledge of "
           "diversity issues in order to deal with them correctly.\n\nWrite an essay on human rights, inclusivity and environmental issues in which "
           "you include the following aspects:\n• Outline the responsibilities of employers in promoting human health and safety in the workplace.\n"
           "• Explain how businesses can deal with any THREE human rights in the workplace.\n• Discuss strategies businesses may use to protect the "
           "environment and human health.\n• Suggest ways in which businesses could deal with the following diversity issues:\n  o Age\n  o Disability")
q6 = [rub("6", Q6_STEM, 40, [
    "Introduction (any 2 x 1): businesses have a responsibility of ensuring that employees work in a safe and healthy environment.",
    "Introduction: policies and procedures used by businesses must include the rules on how to deal with human rights during their operations.",
    "Introduction: businesses that protect the environment and human health receive support from customers.",
    "Introduction: various strategies should be devised and applied by businesses to protect the environment and human health.",
    "Introduction: businesses are encouraged to promote diversity issues such as age and disability to improve productivity/sustainability.",
    "Employers' responsibilities for health and safety (max 12, 2 each): put systems in place to ensure that there is no harmful impact on the health and safety of workers.",
    "Responsibilities: reduce/remove dangers to workers and provide personal protective clothing.",
    "Responsibilities: employers must know where potential dangers might be and take measures to eliminate or limit the harm, such as, the surface of the floor must not be slippery.",
    "Responsibilities: provide and maintain equipment that is safe for employees to use in order to perform their work.",
    "Responsibilities: workers must be informed/instructed and supervised to limit potential dangers to them/emergency exit door signs should be visible to all employees.",
    "Responsibilities: provide a system where equipment is used only under the supervision of a designated trained worker.",
    "Responsibilities: comply with safety laws/protocols which seek to promote a healthy working environment.",
    "Responsibilities: provide a working environment where the workers' health is not damaged by hazards in the production/processing/storage/transportation of materials or equipment.",
    "Human rights (max 12; the first THREE, each the right 2 + explanation 2, submax 4): Privacy.",
    "Privacy: businesses may not violate the rights of the employees and clients.",
    "Privacy: they should not provide personal information about employees to anyone else.",
    "Privacy: information on employees who have disclosed their HIV/Aids status/any chronic illness must be kept confidential.",
    "Privacy: it is illegal to read other people's e-mails/record conversations unless stated clearly and upfront.",
    "Dignity (right 2 + explanation 2).",
    "Dignity: businesses must treat all employees with dignity/respect regardless of their socio-economic status.",
    "Dignity: they should not force workers to do embarrassing or degrading work.",
    "Dignity: the way in which the business communicates should also display respect and dignity towards the employees and customers.",
    "Equity (right 2 + explanation 2).",
    "Equity: the business must ensure that its workers receive equal pay for work of equal value.",
    "Equity: managers should ensure that no employee suffers because of discrimination, such as, paternity leave was implemented to give equal rights to fathers.",
    "Equity: businesses must not discriminate against their employees based on gender/race/religion/sexual orientation, but give equal opportunities to them.",
    "Equity: they should apply relevant legislation fairly on all levels of management, such as new appointments must adhere to the EEA regulations.",
    "Freedom of speech and expression (right 2 + explanation 2).",
    "Freedom of speech: businesses should allow open communication channels between management and employees by providing suggestion boxes for grievances.",
    "Freedom of speech: the employee has the right to express his/her opinion and should not be punished or discriminated against for voicing their opinion.",
    "Freedom of speech: they should give employees a platform to raise their grievances without any victimisation by appointing workplace representatives.",
    "Information (right 2 + explanation 2).",
    "Information: employees should be informed/updated as new information becomes available.",
    "Information: business needs to be transparent in their financial statements/employees may request to see these statements with motivation.",
    "Information: workers should have access to information, including all information held by the government, such as policies/work "
    "schedules/employment contracts/labour laws such as BCEA/EEA/SDA.",
    "Information: employees must receive information on the CSI projects of the business and how they will affect them.",
    "Safety, security and protection of life (right 2 + explanation 2).",
    "Safety: provide workers with protective clothing, such as gloves and footwear.",
    "Safety: comply with safety legislation such as COIDA/OHSA regarding the safety and health of their employees.",
    "Safety: employees should work in a safe working environment free from hazardous products/areas.",
    "Safety: employers should take precautionary measures to ensure employees and their belongings are safe in the workplace.",
    "Strategies to protect the environment and human health (max 10, 2 each): the business must take steps to become involved in environmental awareness programmes.",
    "Strategies: alter its production techniques in favour of cleaner and greener technologies to protect the environment.",
    "Strategies: test the water in the workplace in line with social rights of workers to ensure that it is safe for human consumption.",
    "Strategies: look after natural resources and promote nature conservation.",
    "Strategies: have a policy to minimise pollution and actively reuse, recycle and reduce waste.",
    "Strategies: reduce consumption of goods and services which are environmentally unfriendly, such as by investing in appropriate technology like clean solar or wind power.",
    "Strategies: register or engage with recognised institutions/bodies that promote green peace/renewable energy and green energy.",
    "Strategies: ensure that the physical working conditions is always worker friendly, safe and promotes occupational health.",
    "Strategies: evaluate the physical working conditions, to improve human health, such as by providing adequate lighting and ventilation to "
    "ensure optimal and functional working conditions.",
    "Strategies: service and maintain all machines regularly in order to reduce accidents in the workplace.",
    "Strategies: educate workers about hygiene issues, such as washing of hands.",
    "Strategies: encourage employees to do regular health check-ups to improve their health by regularly checking their blood pressure and temperature.",
    "Strategies: adhere to laws and regulations so that profits are not generated at the expense of the environment.",
    "Strategies: consider pollution and other environmental issues in all business activities, such as safe disposal of waste/dumping of toxic waste.",
    "Diversity issues (max 12): Age (submax 6, 2 each): businesses may not employ children who are under/below 15 years of age.",
    "Age: the age of permanent workers should vary from 18 to 65 years to include all age groups.",
    "Age: young employees must be advised to respect and learn from older employees.",
    "Age: businesses must encourage older employees to help young employees to develop their potential.",
    "Age: promotions should not be linked to age, but rather to a specific set of skills.",
    "Age: businesses may employ a person who is older than the normal retirement age, provided that person is the most suitable candidate.",
    "Age: the business should encourage employees to be sensitive to different perspectives of various age groups.",
    "Disability (submax 6, 2 each): provide employment opportunities for people who are physically challenged in jobs that they can handle.",
    "Disability: train employees on how to deal with colleagues with disabilities.",
    "Disability: businesses should be informed on how to deal with physically challenged employees.",
    "Disability: accommodate people who are physically challenged by providing facilities/ramps for wheelchairs/assistive devices.",
    "Disability: ensure that workers with special needs are not marginalised/feel excluded from workplace activities.",
    "Disability: policies and programmes should accommodate the needs of people with disabilities.",
    "Disability: create an organisational culture/climate that is conducive for people with disabilities.",
    "Disability: bring in external experts to help with disability and accommodation issues.",
    "Disability: do not discriminate against employees who have disabilities/they should treat them fairly.",
    "Disability: focus on the skills and work performance of the disabled worker, rather than his/her disability and possible problems that may occur/arise in the future.",
    "Conclusion (any 1 x 2): businesses that adhere to their responsibilities are able to create a safe and healthy work environment for their employees.",
    "Conclusion: businesses which allow their employees to practice their basic rights enables them to contribute positively to the business operations.",
    "Conclusion: environmental laws assist businesses to come up with the required strategies to protect and prevent exploitation of the environment and human health.",
    "Conclusion: businesses that address diversity issues create a more inclusive environment that enables the prevention of discrimination within the workplace.",
    "Conclusion: the workplace consists of diverse backgrounds and therefore requires businesses to develop ways to deal with the diversity issues in the workplace.",
    "Any other relevant answer under each heading."] + INSIGHT,
    ["Plan the four aspects as headings between an introduction and a conclusion.",
     "Health and safety: what the employer must provide. Rights: name three, then how to respect each. Environment: strategies. Age and disability: ways to include."],
    notes=ESSAY_NOTES)]

missions_c = [
    {"id": "5", "title": "Question 5", "kind": "Essay: investment, insurance", "marks": 40, "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Essay: human rights, inclusivity, environment", "marks": 40, "items": q6},
]

# ---- Written answers as STATEMENTS (Murci 2026-10-10, option C of three mocks; the design approved the same night) ----
# A written part plays as picking statements: the memo's own points (right, tidied to one reading of its "/" alternatives) and
# CLEARLY wrong ones (never a true point the memo leaves out: its "any other relevant answer" would make that right). The learner
# picks marks/each of them, any right one counts (the memo's "any N"), each right pick earns `each`; the cards are shuffled the same
# way every run. The memo points above stay as the source. A part worth more than 1 per point (BS "explain": 2) says so in play.
import random


def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random("bs-p2-2025-11:" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts,
            "pool": sorted(k for k, i in enumerate(order) if i < len(right)), "count": count}


STATEMENTS = {
    "2.2": (2, ["Excess is the amount that the insured agrees to pay upfront, as set out in the insurance policy.",
                "It is the portion of a claim that the insured pays towards repairing or replacing the damaged property.",
                "Excess protects the insurer against fraudulent claims, as the insured is less likely to claim falsely when part must be paid upfront."],
               ["Excess is the extra amount the insurer pays out on top of the full value of the claim.",
                "Excess is the monthly premium the insured pays to keep the policy active.",
                "Excess allows the insured to claim more than the value of the property that was damaged."]),
    "2.3": (2, ["Serves as an indicator of economic conditions in South Africa.", "Keeps investors informed by publishing share prices daily.",
                "Acts as a link between investors and public companies.", "Provides protection for investors through strict rules and legislation."],
               ["Sets the repo rate that commercial banks use to charge interest.",
                "Collects company tax from listed companies on behalf of SARS.",
                "Guarantees that the price of every listed share will rise each year."]),
    "2.4": (3, ["Autocratic leadership style: 'Rachel takes all decisions alone, without consulting her staff members.'",
                "Transactional leadership style: 'Zaid, however, offers rewards to hardworking employees, which increases productivity.'"],
               ["Democratic leadership style: 'Rachel takes all decisions alone, without consulting her staff members.'",
                "Laissez-faire leadership style: 'Zaid, however, offers rewards to hardworking employees, which increases productivity.'",
                "Charismatic leadership style: 'Rachel takes all decisions alone, without consulting her staff members.'"]),
    "2.5": (2, ["A leader's positive attitude can influence the success of the business.",
                "Leaders should model the behaviour that they want to see in team members.",
                "A leader's attitude may influence the thoughts and behaviour of employees."],
               ["A leader's attitude has no effect on the team, because only the leadership style matters.",
                "Successful leaders avoid learning from others, as they already know everything they need.",
                "A positive attitude means a leader gives up on a task as soon as it becomes difficult."]),
    "2.6.2": (2, ["Select a background that complements the text.", "Use a legible font and font size so that the slides are easy to read.",
                  "Structure the information in a logical sequence so that the audience can follow it."],
                 ["Fill each slide with as much text as possible so that nothing is left out.",
                  "Use a different font style on every slide to keep the audience guessing.",
                  "Use the smallest possible font so that more information fits on each slide."]),
    "3.2": (2, ["Diversity in the workforce improves morale and motivation amongst employees.",
                "Employees from different backgrounds bring different perspectives to the business.",
                "A diverse workforce can give the business a competitive advantage, as it can render better services.",
                "Employees show greater loyalty to the business because they feel respected and accepted."],
               ["Diversity means that every employee must think and act in exactly the same way.",
                "A diverse workforce allows the business to pay some groups lower wages.",
                "Diversity removes the need for the business to follow labour legislation."]),
    "3.3.1": (3, ["Responsibility: 'JP developed a remedial programme to reduce air pollution levels and to protect the environment.'"],
                 ["Transparency: 'JP developed a remedial programme to reduce air pollution levels and to protect the environment.'",
                  "Fairness: 'The board of directors of Jaleel Pharmacy regularly applies the King Code principles in their business operations.'",
                  "Accountability: 'The board of directors of Jaleel Pharmacy regularly applies the King Code principles in their business operations.'",
                  "Confidentiality: 'JP developed a remedial programme to reduce air pollution levels and to protect the environment.'"]),
    "3.3.2": (3, ["Transparency: decisions and actions must be clear to all stakeholders, and reports must be accurate and available to shareholders.",
                  "Accountability: businesses should be responsible for their decisions and actions, and present accurate annual reports to shareholders at the AGM."],
                 ["Accountability: directors do not have to explain their decisions to shareholders.",
                  "Secrecy: business deals should be kept hidden from shareholders to protect the directors.",
                  "Transparency: directors may leave the negative impacts on the community out of their reports."]),
    "3.4": (2, ["A clear set of procedures for teamwork ensures that every team member understands his/her role.",
                "Good communication between team members may result in quick decisions.", "Quality feedback improves the morale of the team.",
                "Open and honest discussions lead to effective solutions of problems."],
               ["Team members should avoid giving feedback so that nobody's feelings are hurt.",
                "Only the team leader should speak during meetings so that decisions are not delayed.",
                "Progress should never be reviewed, so that the team is not distracted from its tasks."]),
    "3.5.2": (2, ["Acknowledge that there is conflict in the workplace.", "Identify the cause of the conflict to get clarity on its nature.",
                  "Arrange a meeting where each party has the opportunity to express his/her own views."],
                 ["Ignore the conflict, as it will resolve itself over time.", "Dismiss the employees involved without hearing their side.",
                  "Decide who is to blame and punish that party in front of the other staff."]),
    "3.6": (2, ["It improves the business's image, as it conducts itself in a responsible way.",
                "It promotes customer loyalty, resulting in more sales.", "The business enjoys the goodwill and support of communities.",
                "It may give the business tax advantages, such as tax rebates."],
               ["CSR projects immediately double the business's profits.", "CSR allows the business to ignore labour legislation.",
                "CSR means the business no longer has to pay its employees' salaries."]),
    # 4 a difference: the memo's management submax 2 + leadership submax 2 make ONE clear difference worth the whole 4 (MG p17-18)
    "4.3": (4, ["Management guides human behaviour, whereas leadership influences human behaviour.",
                "Management focuses on the short to medium term, whereas leadership focuses on the long term.",
                "Management is task orientated, whereas leadership is people orientated."],
               ["Management inspires staff to trust each other, whereas leadership enforces rules on subordinates.",
                "Management focuses on the long term, whereas leadership focuses only on today's tasks.",
                "Management does the right things, whereas leadership does things right."]),
    "4.4": (2, ["It has its own legal identity and can sign contracts in its own name.",
                "It has continuity of existence, as its lifespan does not depend on the lifespan of its owners.",
                "It is not required to publish its financial statements for the general public.",
                "It pays tax at a fixed tax rate to SARS."],
               ["Its shares can be bought and sold by the public on the JSE.", "It has only one owner, who makes all the decisions alone.",
                "It does not need any directors to manage it."]),
    "4.5": (2, ["Maintain eye contact with the audience.", "Vary the tone of voice to prevent monotony.",
                "Manage time effectively to allow time for questions."],
               ["Read every slide word for word with your back to the audience.", "Speak as fast as possible to cover more information.",
                "Hide behind the equipment so that the audience focuses on the slides."]),
    "4.7": (2, ["Team dynamic theories explain how effective teams work.", "Businesses are able to allocate tasks according to the roles of team members.",
                "Theories help team leaders to understand the personality types of team members, so that tasks are assigned more effectively.",
                "Conflict may be minimised when team members perform different roles."],
               ["Team dynamic theories require every member to perform the same role.",
                "The theories ensure that team members never disagree about anything.",
                "Team dynamic theories are used to calculate employees' salaries."]),
    "4.8.2": (2, ["Make time for brainstorming sessions to generate new ideas.",
                  "Place suggestion boxes around the workplace and keep communication channels open for new ideas.",
                  "Reward creativity with incentives for staff members who come up with useful ideas."],
                 ["Criticise new ideas in public so that only the best people share them.", "Give employees fewer breaks to keep them focused.",
                  "Only allow managers to suggest new ideas."]),
    "4.9": (2, ["Charge fair and affordable prices for goods and services.",
                "Work together with suppliers to share delivery costs to remote rural areas.",
                "Buy in bulk to get a discount and avoid charging high prices."],
               ["Charge much higher prices because rural customers have few other shops to choose from.",
                "Stop supplying rural areas so that prices no longer matter.",
                "Add a hidden transport fee to the price without telling customers."]),
}
# A written part whose memo weighs two sides (positive / negative impact, success / failure) plays as a SORT instead (variety,
# Murci 2026-10-10: not only MCQ-style picks): each statement dragged to its side, or to "Not true" (the clearly wrong ones), 1 mark
# a statement; a grouped match (the cards are reusable), so the platform and the service play it as they play a classification.
SORTS = {
    "2.7": (["Positive impact", "Negative impact", "Not true"], [
        ("Returns are guaranteed, as the interest rate is fixed for the whole investment period.", 0),
        ("It is a low-risk investment, as the money is invested with the South African Government.", 0),
        ("Penalties are charged for early withdrawals if the savings are less than 12 months old.", 1),
        ("The bonds cannot be ceded to a bank as security for a loan.", 1),
        ("Investors can lose all their money if share prices fall on the JSE.", 2),
        ("Interest is paid only once, at the end of a 20-year period.", 2)]),
    "2.8": (["Success", "Failure", "Not true"], [
        ("It is managed by a board of skilled directors, which results in better decision-making.", 0),
        ("Shareholders can vote for the most capable directors to manage the company.", 0),
        ("A large management structure can make decision-making slow.", 1),
        ("Directors' fees increase the company's expenses, which reduces net profit.", 1),
        ("Directors have unlimited personal liability for all of the company's debts.", 2),
        ("A public company does not have to report to its shareholders at all.", 2)]),
    "3.7": (["Positive impact", "Negative impact", "Not true"], [
        ("Members have time to think about the question in silence before responding.", 0),
        ("Voting on the ideas is anonymous and may be more honest.", 0),
        ("It is time consuming, as each member must make a presentation.", 1),
        ("Good ideas can be voted out because their potential cannot be developed further.", 1),
        ("Members must vote openly, so nobody can be honest.", 2),
        ("One person dominates the group, so decisions are made faster.", 2)]),
}


def sort_(n, q, marks, bins, rows, clues):
    order = list(range(len(rows)))
    random.Random("bs-p2-2025-11:sort:" + n).shuffle(order)
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
# memo's cap of 32, then an INSIGHT part (LASO, 8) worked out from the picks (Layout: introduction + conclusion right; Analysis: every
# heading answered; Synthesis: every section right first time; Originality: the example statements picked). The essay's own wording
# stays as the mission's lead; the memo points above stay as the source.
def essay(nums, parts, examples, insight_clues):
    ex = [[n, next(p for p in parts if p["n"] == n)["opts"].index(t)] for n, t in examples]
    assert sum(p["marks"] for p in parts) == 32, [p["marks"] for p in parts]
    return parts + [{"t": "insight", "n": nums, "marks": 8, "q": "Insight: your essay's layout, analysis, synthesis and originality, worked out "
                     "from your picks.", "clues": insight_clues, "of": [p["n"] for p in parts], "intro": parts[0]["n"], "conclusion": parts[-1]["n"],
                     "examples": ex}]


Q5_EX = ["For example, a retailer insured against theft is paid out when its stock is stolen in a burglary.",
         "For example, if a key manager dies in an accident, the policy pays out to the business."]
q5_parts = essay("5.7", [
    stmt("5.1", "Introduction: pick the TWO statements that introduce this essay on insurance.", 2,
         ["Insurance and assurance are indispensable to businesses and individuals to insure against unforeseen events.",
          "Businesses are required by law to take out the relevant compulsory insurance.",
          "Businesses are exposed to many risks during their operations, so they take out insurance to protect themselves."],
         ["Insurance is only needed by businesses that have already suffered a loss.",
          "Businesses can choose to ignore compulsory insurance if they have enough savings.",
          "Insurance guarantees that a business will never suffer any loss at all."],
         ["An introduction says why the topic matters to a business.", "Pick statements that are true and set up the whole essay."], 1),
    sort_("5.2", "Outline the differences between insurance and assurance.", 8, ["Insurance", "Assurance", "Not true"], [
        ("It is based on the principle of indemnity.", 0),
        ("The insured transfers the cost of a possible loss to the insurer for a premium.", 0),
        ("It covers a specified event that may occur, such as fire, theft or burglary.", 0),
        ("It is based on the principle of security, as the event is certain but its time is not.", 1),
        ("The insurer pays an agreed sum after a set period or on the death of the insured, whichever comes first.", 1),
        ("It applies to long-term policies such as life insurance, endowments and retirement annuities.", 1),
        ("It pays out more than the value of the loss, so the insured makes a profit.", 2),
        ("It covers only events that happened before the policy was taken out.", 2)],
        ["Ask of each row: is the event only possible, or bound to happen sooner or later?",
         "Then think about how long each kind of policy usually runs."]),
    sort_("5.3", "Explain the THREE types of compulsory insurance.", 8, ["UIF", "COIDA", "RAF", "Not true"], [
        ("It provides short-term benefits to workers who become unemployed.", 0),
        ("Employers and employees each contribute 1% of the employee's basic wage every month.", 0),
        ("It compensates employees for injuries and diseases they get at work.", 1),
        ("Employers contribute to the fund and may not deduct the contributions from wages.", 1),
        ("It is funded by a levy on the sale of fuel.", 2),
        ("It insures road users against the negligence of other road users.", 2),
        ("Employees must pay for their own work injuries before any claim can be made.", 3),
        ("Only businesses with more than 1 000 employees have to register for it.", 3)],
        ["Spell out each fund's full name: it tells you what it covers.", "Who pays in: the employer, the worker, the fuel buyer?"]),
    stmt("5.4", "Discuss the advantages of insurance.", 6,
         ["It transfers the risk from the business to the insurer.",
          "The business is compensated for insurable losses, such as property destroyed by fire.",
          "It protects the business against claims by members of the public for damages it is responsible for."] + Q5_EX,
         ["Insurance allows a business to claim twice for the same loss.", "It removes the need for the business to look after its assets.",
          "Insurance premiums are paid back in full at the end of every year."],
         ["What does the business get for its premium?", "Think about who carries the cost when something goes wrong."], 2),
    sort_("5.5", "Advise businesses on the principles of insurance: utmost good faith and insurable interest.", 6,
          ["Utmost good faith", "Insurable interest", "Not true"], [
        ("The insured must be honest when giving details to take out the policy.", 0),
        ("Both the insurer and the insured must disclose all relevant facts.", 0),
        ("The insured must prove a financial loss if the insured object is damaged or lost.", 1),
        ("The insured must have a legal relationship with the insured object.", 1),
        ("The insured may hide facts that would make the premium higher.", 2),
        ("Anyone may insure any object, even one they have no link to.", 2)],
        ["Read each principle's name slowly: what does it ask of the insured?", "Ask of each row: would an insurer accept this?"]),
    stmt("5.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["Insurance protects a business against the risks it is exposed to during its operations.",
          "Principles such as utmost good faith and insurable interest must be kept so that the insurance contract stays valid."],
         ["Insurance is unnecessary for any business that is well managed.", "Compulsory insurance can be ignored once a business makes a profit.",
          "Breaking the principles of insurance makes a claim pay out faster."],
         ["A conclusion sums up why it all matters.", "Pick the statement that is true and ties the essay together."], 2),
], [("5.4", Q5_EX[0]), ("5.4", Q5_EX[1])],
    ["Insight is earned from how you answered the sections.", "Right first time, every heading answered, and the examples picked."])
missions_c[0]["items"] = q5_parts
missions_c[0]["lead"] = "Build the essay section by section, then see your insight."
missions_c[0]["extract"] = "QUESTION 5: THE ESSAY\n\n" + Q5_STEM   # (the essay's wording in the shared-information card: on a phone it folds away)

# Essay 6 the same way: the memo's six headings (6.1-6.6, MG p27-32), the facts 2 + 6 + 8 + 6 + 8 + 2 = 32, then the insight (8).
# 6.3 sorts THREE of the memo's six rights (privacy, equity, freedom of speech and expression: their ways do not overlap 6.2's
# health-and-safety points the way 'safety, security and protection of life' would); the examples sit in 6.4 (strategies).
Q6_EX = ["For example, a factory that switches to solar power and recycles its packaging cuts its pollution and its waste.",
         "For example, a clothing factory that improves the lighting and ventilation on its floor protects its workers' health."]
q6_parts = essay("6.7", [
    stmt("6.1", "Introduction: pick the TWO statements that introduce this essay on human rights, inclusivity and environmental issues.", 2,
         ["Businesses have a responsibility to ensure that employees work in a safe and healthy environment.",
          "Businesses that protect the environment and human health receive support from customers.",
          "Businesses are encouraged to promote diversity issues such as age and disability to improve productivity."],
         ["Health and safety in the workplace is the responsibility of the employees alone.",
          "Human rights apply to employees only outside working hours.",
          "Protecting the environment is the government's job, so businesses need not be involved."],
         ["An introduction says why the topic matters to a business.", "Pick statements that are true and set up the whole essay."], 1),
    stmt("6.2", "Outline the responsibilities of employers in promoting human health and safety in the workplace.", 6,
         ["Provide and maintain equipment that is safe for employees to use in their work.",
          "Reduce or remove dangers to workers and provide personal protective clothing.",
          "Inform, instruct and supervise workers to limit potential dangers to them.",
          "Comply with safety laws and protocols that promote a healthy working environment."],
         ["Make workers buy their own protective clothing before they may start work.",
          "Leave machines unguarded, as workers are responsible for their own safety.",
          "Let untrained workers use dangerous equipment without supervision to save time."],
         ["What must an employer provide, check and enforce so that work does not harm workers?",
          "Think of the workplace, the equipment and the people who use it."], 2),
    sort_("6.3", "Explain how businesses can deal with any THREE human rights in the workplace.", 8,
          ["Privacy", "Equity", "Freedom of speech and expression", "Not true"], [
        ("Do not give employees' personal information to anyone else.", 0),
        ("Keep confidential the HIV/Aids status or chronic illness that an employee has disclosed.", 0),
        ("Ensure that workers receive equal pay for work of equal value.", 1),
        ("Do not discriminate against employees based on gender, race, religion or sexual orientation; give them equal opportunities.", 1),
        ("Allow employees to express their opinions without being punished for voicing them.", 2),
        ("Give employees a platform, such as workplace representatives, to raise grievances without victimisation.", 2),
        ("Managers may read employees' private e-mails whenever they like, without telling them.", 3),
        ("Pay women less than men for the same work if the women agree to it.", 3)],
        ["Read each row and ask which right it protects.", "Remember that some rows describe what a business must never do."]),
    stmt("6.4", "Discuss strategies businesses may use to protect the environment and human health.", 6,
         ["Have a policy to minimise pollution and actively reuse, recycle and reduce waste.",
          "Alter production techniques in favour of cleaner and greener technologies to protect the environment.",
          "Service and maintain all machines regularly to reduce accidents in the workplace."] + Q6_EX,
         ["Dump toxic waste in a nearby river to save on disposal costs.",
          "Ignore environmental laws as long as the business makes a profit.",
          "Stop health check-ups for employees, as they take time away from production."],
         ["Strategies look after the environment AND the people who work in it.", "Which actions would an inspector praise, not fine?"], 2),
    sort_("6.5", "Suggest ways in which businesses could deal with the following diversity issues: age and disability.", 8,
          ["Age", "Disability", "Not true"], [
        ("Link promotions to a specific set of skills, not to age.", 0),
        ("Encourage older employees to help young employees develop their potential.", 0),
        ("Advise young employees to respect and learn from older employees.", 0),
        ("Provide ramps for wheelchairs and other assistive devices.", 1),
        ("Train employees on how to deal with colleagues with disabilities.", 1),
        ("Focus on the skills and work performance of the worker rather than on the disability.", 1),
        ("Employ children under 15 years of age if their parents agree.", 2),
        ("Keep workers with special needs out of workplace activities for their own safety.", 2)],
        ["Sort by the issue each row deals with, then ask whether the way it suggests is fair and legal.",
         "Inclusion means adapting the workplace, never shutting people out."]),
    stmt("6.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["Businesses that adhere to their responsibilities are able to create a safe and healthy work environment for their employees.",
          "Businesses that address diversity issues create a more inclusive environment that helps to prevent discrimination in the workplace."],
         ["Human rights in the workplace become optional when a business is under financial pressure.",
          "Environmental laws stop businesses from making any profit at all.",
          "Diversity issues disappear on their own once a business employs enough people."],
         ["A conclusion sums up why it all matters.", "Pick the statement that is true and ties the essay together."], 2),
], [("6.4", Q6_EX[0]), ("6.4", Q6_EX[1])],
    ["Insight is earned from how you answered the sections.", "Right first time, every heading answered, and the examples picked."])
missions_c[1]["items"] = q6_parts
missions_c[1]["lead"] = "Build the essay section by section, then see your insight."
missions_c[1]["extract"] = "QUESTION 6: THE ESSAY\n\n" + Q6_STEM
assert not [i["n"] for m in missions_c for i in m["items"] if i["t"] == "rubric"], "an essay left as rubric"

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Business Studies", "title": "Business Studies P2", "sitting": "November 2025", "total_marks": 150, "time": "2 hours"},
    "sections": [
        {"title": "Section A", "total": 30, "missions": missions_a},
        {"title": "Section B", "total": 80, "answer_any": 2, "missions": missions_q2 + missions_q3 + missions_q4},
        {"title": "Section C", "total": 40, "answer_any": 1, "missions": missions_c},
    ],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 6), hand-transcribed from the paper and memo PDFs; no API call."},
        {"n": "1.3", "kind": "memo_issue", "detail": "COLUMN B (D) prints 'the business seizes to exist'; transcribed 'ceases to exist' (the paper's typo)."},
        {"n": "5", "kind": "memo_issue", "detail": "5.5.2 prints 'if the ensured object is damaged'; transcribed 'insured object' (the memo's typo)."},
        {"n": "6", "kind": "memo_issue", "detail": "6.5.2 prints 'Businesses should bel informed'; transcribed 'be informed' (the memo's typo)."},
        {"n": "2.6.1", "kind": "no_fit", "detail": "Quote items (2.6.1, 3.5.1, 4.8.1) are played by picking the scenario's sentences: the memo awards "
                                                   "marks only for responses quoted from the scenario."},
    ],
}
out = Path(__file__).parent / "out" / "bs-p2-2025-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs (no API call)",
                                                        "scope": "Questions 1 to 6 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for sec in paper["sections"]:
    print(sec["title"], "parts:", sum(len(m["items"]) for m in sec["missions"]), "marks:", sum(i["marks"] for m in sec["missions"] for i in m["items"]),
          "answer any:", sec.get("answer_any", "all"))
