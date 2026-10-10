"""Business Studies P2 Nov 2024, the whole paper (Sections A, B and C), hand-transcribed into the catalogue format (as if Claude had
produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks and memo points are the
paper's and the memo's own; the clues are ours. No API call: the transcription is the source, kept in git (out/ is not).

  python tools/ingest/transcribe_bs_p2_2024_11.py
  python tools/ingest/ingest.py "<...>/Business Studies P2 Nov 2024  Eng.pdf" "<...>/Business Studies P2 Nov 2024 MG Eng.pdf" --id bs-p2-2024-11 --from-json

(The question paper's file name has TWO spaces before "Eng", as the DBE named it.) The memo's shapes map as in Business Studies P1
Nov 2024 (transcribe_bs_p1_2024_11.py): marking instructions are `notes`; a name and its explanation or quote are two points,
`worth` [2, 1]; only an alternative answer's FIRST point starts with "OR" (2.5.2: one theory, either of two). One shape is new here:
2.3.2, the average-clause calculation, is two `steps` that follow the memo's four ticks (insured amount over market value 2, the
compensation 2)."""
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


def steps(n, q, marks, sts, clues):
    """sts: (label, marks, answer, tolerance, the memo's working)."""
    s = [{"id": "s%d" % (i + 1), "label": lab, "marks": m, "a": a, "tol": tol, "memo": memo} for i, (lab, m, a, tol, memo) in enumerate(sts)]
    assert sum(x["marks"] for x in s) == marks, n
    return {"t": "steps", "n": n, "marks": marks, "q": q, "clues": clues, "steps": s}


def sentences(text):
    """A scenario's sentences, as printed (each ends with a full stop)."""
    return [s.strip().rstrip(".") + "." for s in text.split(". ") if s.strip()]


QUOTE = "(Its motivation, quoted from the scenario:) "

# ---- Section A: Question 1, the question paper pages 3-5 and the memo page 7 ----
q11 = [
    mcq("1.1.1", "The leadership style in which subordinates are experts and take full responsibility for their actions:",
        ["Transactional", "Democratic", "Laissez-faire", "Charismatic"], 2,
        ["Which leader hands the work over and steps back?", "Experts who need no supervision suit a hands-off style."]),
    mcq("1.1.2", "The main objective of a ... is to create mutual benefit for its members.",
        ["partnership", "cooperative", "state-owned company", "private company"], 1,
        ["Which form of ownership exists to serve its own members?", "Members work together, or co-operate, for a shared benefit."]),
    mcq("1.1.3", "Chidere Enterprise uses fine print to hide misleading information when promoting their products. This is known as ..., "
        "a type of unethical business practice.", ["taxation", "pricing of goods in rural areas", "fair advertising", "unfair advertising"], 3,
        ["Hiding misleading information is part of how a product is promoted.", "Is hiding information fair to the customer?"]),
    mcq("1.1.4", "The role of health and safety representatives is to ...",
        ["ensure that protective clothing is available.", "provide safety clothes to employees.", "use prescribed safety equipment.",
         "maintain equipment regularly."], 0,
        ["A representative checks on behalf of the workers; the employer provides and maintains.", "Workers USE the equipment; who makes sure it is there?"]),
    mcq("1.1.5", "Amajuba team members implement ... as a criterion for successful team performance by agreeing on methods to get the job "
        "done, without wasting time on conflict resolution.",
        ["shared values", "communication", "collaboration", "interpersonal attitudes and behaviour"], 2,
        ["Agreeing on how to get the job done together.", "Working together on the methods is ..."]),
]
WORDS = "bonus;  limited;  conflict;  cultural;  posters;  grievance;  social;  hand-outs;  unlimited;  founders'"
q12 = [
    term("1.2.1", "Visco Limited issued ... shares to the promoters of the company.", ["founders'", "founders", "founder's"],
         ["The promoters started the company.", "Shares for the people who founded it."]),
    term("1.2.2", "Ben distributed ... at the start of the presentation to attract the attention of the audience.", ["hand-outs", "handouts", "hand outs"],
         ["Something each person in the audience holds.", "Ben hands them out."]),
    term("1.2.3", "The shareholders at Blake Ltd have ... liability and can only lose the amount that they invested in the company.", ["limited"],
         ["Ltd stands for this word.", "They cannot lose more than they invested."]),
    term("1.2.4", "A disagreement between two or more parties in the workplace is known as a ...", ["conflict"],
         ["Not a formal complaint by one employee: a clash between parties.", "Two sides that do not agree are in ..."]),
    term("1.2.5", "Employees at Mawethu Traders are allowed to use their own language during their lunch breaks; this promotes their ... right "
         "in the workplace.", ["cultural"], ["Language is part of a person's culture.", "Which right protects language and traditions?"]),
]
COL_B = ["allows employees to silently generate many ideas on their own",
         "managers must know their facts when dealing with this type of personality",
         "business decisions must be clear to all stakeholders",
         "based on the principle of indemnity",
         "can be bought back at the option of the issuing company",
         "managers must restrict the time of the discussion when dealing with this type of personality",
         "based on the principle of certainty",
         "allows employees to randomly generate suggestions aloud",
         "business should take responsibility for their decisions",
         "can only be bought back when the company closes down"]
q13 = [match("1.3", "Choose a description from COLUMN B that matches a term in COLUMN A.",
             ["Security", "Redeemable preference shares", "Nominal group technique", "Accountability", "Expert"],
             COL_B, [6, 4, 0, 8, 1], 2,
             ["Several descriptions come in pairs: read the small words (indemnity or certainty; silently or aloud; clear or responsible).",
              "Security (assurance) pays out for an event that is certain to happen."])]
missions_a = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 10,
     "lead": "Various options are provided as possible answers to the following questions. Choose the answer.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Words from a list", "marks": 10,
     "lead": "Complete the following statements by using the word(s) provided in the list below.\n\n" + WORDS, "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "Matching columns", "marks": 10, "items": q13},
]

# ---- Section B: Question 2 (Business Ventures), the question paper page 6 and the memo pages 8-11 ----
AT = ("Akhona Traders bought stock to the value of R400 000 but only insured it for R200 000. A fire broke out in the warehouse and destroyed "
      "stock to the value of R80 000.")
EA = ("Exclusive Architects operate in a competitive environment and had to improve the designs of their housing plans. The management of EA "
      "provide emotional support for employees through coaching so that they can share their ideas more freely.")
q21 = [lst("2.1", "List any FOUR types of investment opportunities.", 4,
           [["Mutual funds", "Mutual fund", "Stokvel", "Stokvels"], ["Managed portfolio", "Managed portfolios"], ["Venture capital"],
            ["32-day notice account", "32 day notice account", "Notice account"], ["Debentures", "Debenture"],
            ["Endowment", "Endowment policy", "Retirement annuities", "Retirement annuity"]],
           ["Places where a business can put money to grow.", "Funds, portfolios, notice accounts, debentures, annuities."])]
q22 = [rub("2.2", "Outline the advantages of a state-owned company.", 6, [
    "Profits may be used to finance other state departments.", "Offer essential services which may not be offered by the private sector.",
    "Prices are kept reasonable/Create sound competition to make services affordable to more citizens.",
    "Wasteful duplication of services is eliminated.", "Planning can be coordinated through central control.",
    "Generates income/Receive government funds to finance social programmes.", "Jobs are created for all skills levels.",
    "Any other relevant answer related to the advantages of a state-owned company."],
    ["The state owns it and runs it for the public.", "Essential services, fair prices, jobs, money for the state."], each=2)]
q23 = [
    term("2.3.1", "Name the insurance clause that is applicable to AT in the scenario above.", ["Average clause", "Average", "The average clause"],
         ["AT insured its stock for less than it is worth.", "Under-insured: the insurer pays only part of the loss."]),
    steps("2.3.2", "Calculate the amount that AT will receive as compensation from the insurer. Show ALL the calculations.", 4, [
        ("Insured amount ÷ market value of the stock", 2, 0.5, 0.001,
         "Insured amount ÷ market value × loss: R200 000 ÷ R400 000 = ½ (0,5)"),
        ("Compensation from the insurer (R)", 2, 40000, 0.5, "½ × R80 000 = R40 000")],
        ["Under-insured by half: what share of the stock's value is insured?", "The insurer pays that share of the R80 000 loss."]),
]
q24 = [rub("2.4", "Explain aspects that should be considered when designing a multimedia presentation.", 6, [
    "Start with the heading/text which forms the basis of the presentation.", "Select the background to complement/enhance the text.",
    "Choose images that may help to communicate the message.", "Include/Create graphics to assist the information which is conveyed.",
    "Add special effects/sound/pictures/animation to make it interesting for the audience.",
    "Create hyperlinks to allow quick access to other files/documents/video clips.",
    "Use legible font and font size so that it is easy to see/read.",
    "Keep slides/images/graphs/font simple by not mixing different styles/colours.", "Make sure there are no language and spelling errors.",
    "Use bright colours to increase visibility.",
    "Structure information in a logical sequence so that the audience can easily follow the content of the presentation.",
    "Limit the information on each slide by using key words and not full sentences.",
    "Any other relevant answer related to aspects that should be considered when designing a multimedia presentation."],
    ["Think of a slide: heading, background, images, font, colour, order.", "Each aspect, then why it helps the audience."], each=2)]
q25 = [
    rub("2.5.1", "Identify the leadership theory used by EA. Motivate your answer by quoting from the scenario above.", 3, [
        "Transformational/Transitional theory.",
        QUOTE + "'The management of EA provide emotional support for employees through coaching so that they can share their ideas more freely.'"],
        ["EA's managers support and coach their people so that they change and grow.", "Which theory is about leaders who transform their followers?"],
        worth=[2, 1], notes=["Do not award marks for the motivation if the leadership theory was incorrectly identified."]),
    rub("2.5.2", "Explain ONE other leadership theory.", 3, [
        "Leaders and followers theory.",
        "(Leaders and followers, explained:) teams achieve great results/set out organisational goals when there is a sense of understanding "
        "between the leader and the team of followers/employees; followers listen to what is expected of them/follow the instructions of the "
        "leader and are willing to work as a team towards the organisation goals; followers easily accept/take responsibility when something "
        "doesn't work out/targets are not achieved; leaders lead by example and reward/provide incentives for positive behaviour; leaders "
        "motivate employees to devise alternative strategies/to be creative and innovative/to find more efficient ways to use available "
        "resources/increase productivity; followers might just trail along/stifle innovation and creativity/by depending on leaders and other "
        "followers to pull them through the task.",
        "OR — Situational theory.",
        "(Situational, explained:) different leadership characteristics/styles are needed for different situations/prevailing circumstances; "
        "the task/situation dictates the leadership style that should be applied, so leaders are adaptable/flexible/self-assured; effective "
        "application/adoption of this theory may enable leaders to accomplish/achieve their organisational goals; relationships between leaders "
        "and employees are based on mutual trust/respect/loyalty/integrity/honesty; leaders have the ability to analyse the situation/get the "
        "most suitable people in the right positions to complete tasks successfully; leaders analyse group members/objectives/time constraints, "
        "to adopt a suitable/relevant leadership style; may lead to conflict when leaders use different leadership styles/when managing employees "
        "in different situations; the success of this theory depends on the kind of relationship that exists between the leader and "
        "followers/subordinates/employees."],
        ["Not the theory in 2.5.1. Two others: one about leaders and the people who follow them, one about the situation.",
         "Name the theory, then explain how it works."],
        worth=[2, 1, 2, 1],
        notes=["Mark the first ONE only (3 marks: the theory 2, its explanation 1). Do not award marks for transformational/transitional theory. "
               "Any other relevant answer related to each theory is accepted."]),
]
q26 = [rub("2.6", "Discuss the impact of the autocratic leadership style on businesses.", 6, [
    "Positive: quick decisions can be taken without consulting/considering followers/employees.",
    "Positive: work gets done in time/on schedule as targets are clearly specified.",
    "Positive: line of command/communication is clear as it is top-down/followers know exactly what to do.",
    "Positive: direct supervision/strict control ensure high quality products/services.",
    "Positive: provides strong leadership which makes new employees feel confident/safe.",
    "Positive: works well in large companies where consultation with every employee is impractical.",
    "Positive: clear guidance can be given to low-skilled/inexperienced/new staff.",
    "Negative: leaders and followers may become divided as tension arise and may not agree on ways to solve problems.",
    "Negative: workers can become demotivated if their opinions/ideas are not considered.",
    "Negative: de-motivated workers impact negatively on productivity.",
    "Negative: new/innovative/creative/cost reducing ideas and solutions may not be used/considered/implemented.",
    "Negative: followers may feel that they are not valued resulting in high absenteeism/employee turnover.",
    "Negative: experienced/highly skilled workers may experience resistance resulting in slow growth/low participation/less creativity.",
    "Any other relevant answer related to the positive and/or negative impact of the autocratic leadership style on businesses."],
    ["An autocratic leader decides alone and tells others what to do.", "Impact can be positive, negative, or both: say what happens, then why."],
    each=2)]
q27 = [rub("2.7", "Recommend ways in which presenters can handle feedback in a non-aggressive and professional manner.", 6, [
    "The presenter should stand throughout the feedback session.", "Be polite/confident/courteous/calm when responding to questions.",
    "Ensure that each question/comment is clearly understood before responding/rephrase questions if uncertain.",
    "The presenter should first listen and then respond.",
    "Provide feedback as soon as possible after the question was asked or after the session.",
    "Be direct/honest/sincere when responding to questions.", "Use simple language to support the examples used in the presentation.",
    "Keep answers short and to the point.", "Apologise/Acknowledge errors/mistakes if pointed out by the audience.",
    "Encourage questions from the audience.", "Always address the question and not the person.",
    "Acknowledge good questions to motivate the audience to ask more questions.",
    "The presenter should not be involved in a debate when responding to questions.",
    "The presenter should not avoid the questions if he/she does not know the answer, but rather promise feedback on it.",
    "Address the full audience and not only the person who posed the question.",
    "Any other relevant answer related to ways in which presenters can handle feedback in a non-aggressive and professional manner."],
    ["Questions come after a presentation: how do you answer them well?", "Listen, stay calm, be honest, keep it short, address the question."],
    each=2)]
missions_q2 = [
    {"id": "2.1", "title": "Question 2.1", "kind": "Investment opportunities", "marks": 4, "items": q21},
    {"id": "2.2", "title": "Question 2.2", "kind": "State-owned companies", "marks": 6, "items": q22},
    {"id": "2.3", "title": "Question 2.3", "kind": "The average clause", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "AKHONA TRADERS (AT)\n\n" + AT, "items": q23},
    {"id": "2.4", "title": "Question 2.4", "kind": "Multimedia presentations", "marks": 6, "items": q24},
    {"id": "2.5", "title": "Question 2.5", "kind": "Leadership theories", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "EXCLUSIVE ARCHITECTS (EA)\n\n" + EA, "items": q25},
    {"id": "2.6", "title": "Question 2.6", "kind": "Autocratic leadership", "marks": 6, "items": q26},
    {"id": "2.7", "title": "Question 2.7", "kind": "Handling feedback", "marks": 6, "items": q27},
]

# ---- Section B: Question 3 (Business Roles), the question paper page 7 and the memo pages 12-14 ----
TF = ("Tornado Furniture specialises in the manufacturing of lounge suites. They monitor their employees on an hourly basis to ensure that tasks "
      "are completed on time. The management allows only certain employees access to the business funds. TF also strengthens the team spirit "
      "among the employees so that they feel responsible for what needs to be achieved.")
MD = ("Medal Designers gave Pumla the responsibility to manage a team of experienced and highly competent members. Team members are able to "
      "handle the decision-making process without Pumla supervising them. They are also aware of the importance of team dynamic theories in "
      "improving team performance.")
q31 = [lst("3.1", "Name any TWO corporate social investment (CSI) focus areas.", 2,
           [["Community", "Communities"], ["Rural development"], ["Employees", "Staff"], ["Environment"]],
           ["Where does a business spend its CSI money and time?", "People around it, its own people, rural areas, nature."])]
q32 = [rub("3.2", "Outline the responsibilities of workers in promoting human health and safety in the workplace.", 6, [
    "Use prescribed safety equipment.", "Report accidents to the employer by the end of the shift.",
    "Report unsafe/unhealthy working conditions to the relevant authorities/management.",
    "Inform the employer of any illness that may affect the ability to work.", "Take care of their own health and safety in the workplace.",
    "Co-operate and comply with the rules and procedures, such as wear prescribed safety clothing.",
    "Any other relevant answer related to the responsibilities of workers in promoting human health and safety in the workplace."],
    ["The WORKERS' duties, not the employer's.", "Use the equipment, report accidents and dangers, follow the rules."], each=2)]
q33 = [
    pick("3.3.1", "Quote TWO ways in which TF is dealing with the abuse of work time as a type of unprofessional business practice from the "
         "scenario above.", sentences(TF), [1, 3],
         ["Which sentences are about using work time well?", "Access to business funds is a different problem."]),
    rub("3.3.2", "Explain other ways in which TF can deal with abuse of work time as a type of unprofessional business practice in the workplace.", 4, [
        "Speak directly to those employees who abuse work time.",
        "Make employees aware that profit will decrease resulting in less incentives/bonus pay-outs.",
        "The code of conduct/ethics should contain clear rules about abuse of work time.",
        "TF/A business should conduct training on the contents of the code of conduct/ethics.",
        "The code of conduct/ethics should be signed by all employees so that they are aware of its contents.",
        "Structure working hours in such a way that employees have free/flexible time for personal matters.",
        "Any other relevant answer related to other ways in which TF/a business can deal with abuse of work time as a type of unprofessional "
        "business practice in the workplace."],
        ["Abuse of work time: personal matters, long breaks, idling on the job.", "Talk to them, a code of conduct, training, flexible hours."],
        each=2, notes=["Do not award marks for responses that were quoted in QUESTION 3.3.1."]),
]
q34 = [rub("3.4", "Recommend ways in which businesses can create an environment that promotes creative thinking in the workplace.", 6, [
    "Emphasise the importance of creative thinking to ensure that all staff know that management wants to hear their ideas.",
    "Make time for brainstorming sessions to generate new ideas such as regular workshops/build on one another's ideas.",
    "Place suggestion boxes around the workplace and keep communication channels open for new ideas.",
    "Train staff in innovative techniques/creative problem-solving skills/mind-mapping/lateral thinking.",
    "Encourage job swops within the organisation/Study how other businesses are doing things.",
    "Encourage employees to develop/come up with new/unique ideas/alternative ways of working/doing things.",
    "Reward creativity by offering reward schemes to employees/Introduce incentives for staff members who came up with useful creative ideas.",
    "Respond enthusiastically to all ideas and never let anyone feel less important.",
    "Make the working environment conducive to creativity/free from distraction/high noise levels.",
    "Any other relevant answer related to ways in which businesses can create an environment that promotes creative thinking in the workplace."],
    ["How can a business show that it wants new ideas?", "Brainstorming, suggestion boxes, training, rewards, a quiet place to think."], each=2)]
q35 = [
    term("3.5.1", "Name the stage of team development applicable in the scenario above.", ["Performing", "Performing stage"],
         ["Forming, storming, norming, performing, adjourning.", "The team works well on its own, without supervision."]),
    rub("3.5.2", "Discuss the importance of team dynamic theories in improving team performance.", 6, [
        "Team dynamic theories explain how effective teams work/operate.",
        "Businesses are able to allocate tasks according to the roles of team members.",
        "Team members can optimise/maximise performance as tasks are allocated according to their abilities/skills/attributes/personalities.",
        "Team members with similar strengths may compete for team tasks/responsibilities that best suit their abilities/competencies.",
        "Theories assist team leaders to understand the personality types of team members so that tasks are assigned more effectively.",
        "Conflict may be minimised when team members perform different roles.",
        "Any other relevant answer related to the importance of team dynamic theories in improving team performance."],
        ["Team dynamic theories describe the roles people play in a team.", "Knowing the roles: better task allocation, less conflict."], each=2),
]
q36 = [rub("3.6", "Explain how businesses should handle conflict in the workplace.", 6, [
    "Acknowledge that there is conflict between employers/employees/parties in the workplace.",
    "Identify the cause of the conflict to get clarity on its nature.",
    "Arrange time and place for negotiations where all employees involved are present.",
    "Arrange a meeting between conflicting employers and employees.",
    "Make the intentions/purpose for intervention/meeting clear so that parties involved may feel at ease.",
    "Arrange a pre-negotiation meeting where workers/complainants will be allowed to state their case/views separately.",
    "Each party has the opportunity to express his/her own opinions/feelings.",
    "Conflicting parties may recognise that their views are different during the meeting.",
    "Analyse the cause(s) of conflict by breaking it down into different parts.", "Evaluate the views expressed and make an objective decision.",
    "Blame shifting should be avoided and a joint effort should be made.", "Direct conflicting parties towards finding/focusing on solutions.",
    "Devise/Brainstorm possible ways of resolving the conflict.", "Conflicting parties agree on criteria to evaluate the alternatives.",
    "Select/Implement the best solution that will deal with the conflict.", "Provide opportunities for parties to agree on the best solution.",
    "Evaluate/Follow up on the implementation of the solution(s).", "Monitor progress to ensure that the conflict has been resolved.",
    "Source experts on handling conflict from outside the business.",
    "Any other relevant answer related to how businesses should handle conflict in the workplace."],
    ["Handling conflict is a process: acknowledge it, find its cause, meet, solve it, follow up.",
     "Each step: what the business does, then why."], each=2)]
q37 = [rub("3.7", "Suggest ways in which businesses could deal with gender as a diversity issue in the workplace.", 6, [
    "Males and females should be offered equal employment opportunities.",
    "Business directors should promote both men and women in managerial positions.", "Women should be employed to comply with the EEA.",
    "Targets may be set for gender equity in the business.", "New appointments should be based on skills and ability.",
    "Introduce affirmative action by ensuring that male and female employees are remunerated fairly/equally.",
    "Any other relevant answer related to ways in which businesses could deal with gender as a diversity issue in the workplace."],
    ["Gender: treating men and women fairly at work.", "Opportunities, promotion, pay, targets, the EEA."], each=2)]
missions_q3 = [
    {"id": "3.1", "title": "Question 3.1", "kind": "CSI focus areas", "marks": 2, "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Health and safety", "marks": 6, "items": q32},
    {"id": "3.3", "title": "Question 3.3", "kind": "Abuse of work time", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "TORNADO FURNITURE (TF)\n\n" + TF, "items": q33},
    {"id": "3.4", "title": "Question 3.4", "kind": "Creative thinking", "marks": 6, "items": q34},
    {"id": "3.5", "title": "Question 3.5", "kind": "Team performance", "marks": 8,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "MEDAL DESIGNERS (MD)\n\n" + MD, "items": q35},
    {"id": "3.6", "title": "Question 3.6", "kind": "Handling conflict", "marks": 6, "items": q36},
    {"id": "3.7", "title": "Question 3.7", "kind": "Gender diversity", "marks": 6, "items": q37},
]

# ---- Section B: Question 4 (Miscellaneous topics), the question paper page 8 and the memo pages 15-19 ----
EL = ("The management of Elange Limited presented their future plans for expansion to the shareholders. They used PowerPoint, smart pens and "
      "flip charts to make their presentation interesting. Management also considered comments from the shareholders in order to improve "
      "their next presentation.")
BT = ("Barrows Traders sell bicycles to different outlets. They treat all employees with respect regardless of their socio-economic status. "
      "The management of BT encourages open communication channels between them and employees.")
q41 = [lst("4.1", "Name any TWO types of compulsory insurance.", 2,
           [["Unemployment Insurance Fund", "UIF"], ["Road Accident Fund", "RAF", "Road Accident Benefit Scheme", "RABS"],
            ["Compensation for Occupational Injuries and Diseases Fund", "COIDA", "Compensation Fund", "COID"]],
           ["Compulsory insurance is required by law.", "Losing a job, a road accident, an injury at work."])]
q42 = [rub("4.2", "Outline the advantages of insurance for businesses.", 6, [
    "Transfers the risk from businesses/insured to insurance companies/an insurer.",
    "Transfer of risk is subject to the terms and conditions of the insurance contract.",
    "Protects businesses against theft/loss of stock and/or damages caused by natural disasters such as floods/storm damage.",
    "Businesses will be compensated for insurable losses, such as the destruction of property through fire.",
    "Business' assets such as vehicles/equipment/buildings need to be insured against damage and/or theft.",
    "Businesses are protected against the loss of earnings, such as strikes by employees which may result in losses worth millions.",
    "Protects businesses against dishonest employees.",
    "Life insurance can be taken on the life of partners in a partnership to prevent unexpected loss of capital.",
    "Should the services of key personnel be lost due to accidents/death, the proceeds of an insurance policy can be paid out to the "
    "business/beneficiaries.",
    "Replacement costs for damaged machinery/equipment are very high therefore insurance can reduce/cover such costs.",
    "Protects businesses from claims made by members of the public for damages that businesses are responsible for.",
    "Protects businesses against losses due to death of a debtor.",
    "Any other relevant answer related to the advantages of insurance for businesses."],
    ["Insurance moves the risk of a loss to the insurer.", "Theft, fire, disasters, dishonest staff, losing key people, claims by the public."],
    each=2)]
q43 = [
    lst("4.3.1", "Name TWO visual aids used by EL in the scenario above.", 2,
        [["PowerPoint", "Power Point", "PowerPoint presentation", "PowerPoint slides"], ["Flip charts", "Flip chart", "Flipcharts", "Flipchart"]],
        ["A visual aid is something the audience looks at.", "Of the three things EL used, a pen is not something the audience looks at."]),
    rub("4.3.2", "Suggest the areas of improvement that the management should consider for their next presentation.", 4, [
        "The presenter should revise objectives that were not achieved.", "Use humour appropriately.",
        "Always be prepared to update/keep the information relevant.", "Reflect on any problem/criticism and avoid it in future presentations.",
        "Reflect on the time/length of the presentation to add/remove content.",
        "Reflect on the logical flow of the format/slides/application of visual aids.",
        "Increase/Decrease the use of visual aids/replace or remove aids that do not work well.",
        "Information that the presenter receives as feedback from a presentation should be analysed and where relevant incorporated/used to "
        "update/amend his/her presentation.",
        "Any other relevant answer related to the areas of improvement that the management should consider for their next presentation."],
        ["Look back at the presentation: what could be better next time?", "Objectives, time, flow, visual aids, the feedback received."], each=2),
]
q44 = [rub("4.4", "Explain how capital as a criterion can contribute to the success and/or failure of a private company.", 6, [
    "Success: large amount of capital can be raised since there is no limit on the number of shareholders.",
    "Success: the company can access long term capital and therefore has good long term growth opportunities.",
    "Success: even though shares are not freely transferable, large private companies can raise a considerable amount of capital.",
    "Failure: it cannot grow into a very large business since it cannot invite the public to buy shares.",
    "Failure: restrictions on transferability of shares may not attract financially strong investors.",
    "Failure: large amount of capital cannot be obtained as capital contribution is only limited to private shareholders.",
    "Any other relevant answer related to the contribution of capital to the success and/or failure of a private company."],
    ["A private company's capital comes from its shareholders, not from the public.", "How does that help it grow, and how does it hold it back?"],
    each=2, notes=["The answer does not have to be in tabular format. Mark either success AND/OR failure."])]
q45 = [lst("4.5", "State any FOUR problem-solving steps.", 4,
           [["Identify the problem"], ["Define the problem"],
            ["Identify possible solutions", "Identify alternatives", "Identify possible alternatives"],
            ["Evaluate alternative solutions", "Evaluate alternatives", "Evaluate the alternative solutions"],
            ["Choose the most appropriate alternative", "Select the most appropriate solution", "Choose the best solution", "Select the best alternative"],
            ["Develop an action plan"], ["Implement the suggested solution", "Implement the action plan", "Implement the solution"],
            ["Monitor the implementation of the solution", "Monitor the implementation", "Monitor the action plan"],
            ["Evaluate the implemented solution", "Evaluate the action plan"]],
           ["Solving a problem goes step by step, from the problem to checking the result.", "Identify, define, find options, choose, plan, implement, monitor."])]
q46 = [rub("4.6", "Explain ways in which businesses can contribute time and effort to improve the well-being of employees.", 6, [
    "Pay fair wages/salaries to the workers based on the nature of their work/the prevailing economic conditions in the market.",
    "Provide transport for employees who work unusually long hours.",
    "Pay fair bonuses based on business earnings, as acknowledgement for hard work and commitment.",
    "Working conditions should include safety/medical/canteen facilities/benefits like housing/leave/retirement.",
    "Provide for employees' participation in decision making that affects them.",
    "Provide employees with recreational facilities to socialise and strengthen work relations.",
    "Offer annual physical/medical assessments to workers to promote health awareness.",
    "Encourage employees to stay fit and healthy by getting them involved in health activities to minimize stress/substance abuse/obesity.",
    "Make trauma debriefing/counselling/therapy available to any employee who requires these services.",
    "Offer financial assistance in the case of any hardship caused by unexpected medical costs.",
    "Allow flexible working hours to enhance productivity.", "Offer support programmes for employees infected and affected by HIV/Aids.",
    "Make childcare facilities available on the premises for working mothers in the business.",
    "Start a nutritional programme so that employees can enjoy one meal per day to keep them in a healthy condition.",
    "Give time to the staff to get involved in projects they choose/Allow staff to use some of the working hours to participate in the "
    "projects of their choice.",
    "Establish coaching and mentoring programmes for junior employees.", "Conduct team-building sessions to improve employees' morale.",
    "Encourage employees to attend capacity-building workshops/training programmes/staff-development programmes/team-development programmes.",
    "Any other relevant answer related to ways in which businesses can contribute time and effort in improving the well-being of employees."],
    ["Well-being: employees' health, money worries, family and growth.", "Fair pay, health checks, counselling, flexible hours, childcare, training."],
    each=2)]
q47 = [rub("4.7", "Identify TWO human rights that are promoted by BT. Motivate your answer by quoting from the scenario above.", 6, [
    "Dignity.", QUOTE + "'They treat all employees with respect regardless of their socio-economic status.'",
    "Freedom of speech and expression.", QUOTE + "'The management of BT encourages open communication channels between them and employees.'"],
    ["One sentence is about respect; the other is about speaking openly.", "Which human right protects a person's worth? Which one protects speaking freely?"],
    worth=[2, 1, 2, 1],
    notes=["Mark the first TWO only. The answer does not have to be in tabular format. Award marks for the human rights even if the quotes "
           "are incomplete; no marks for a motivation if its human right is wrong."])]
q48 = [rub("4.8", "Recommend ways in which professional, responsible, ethical and effective business practice should be conducted by businesses.", 4, [
    "Mission statement should include the values of equality/respect.",
    "Businesses should develop equity programmes/promotes strategies to ensure that all employees are treated equally regardless of status/rank/power.",
    "Treat workers with respect/dignity by recognising work well done/the value of human capital.",
    "Plan properly and put preventative measures in place.",
    "Pay fair wages/salaries which are in line with the minimum requirements of the BCEA/Remunerate employees for working overtime/during public holidays.",
    "Engage in environmental awareness programmes/Refrain from polluting the environment such as legally disposing of toxic waste.",
    "Refrain from starting a venture using other businesses' ideas that are protected by law.",
    "Business decisions and actions must be clear/transparent to all stakeholders.",
    "Businesses should be accountable/responsible for their decisions and actions/patent rights.",
    "Hire honest/trustworthy accountants/financial officers with good credentials.", "Regular/Timeous payment of taxes.",
    "All workers should have access to equal opportunities/positions/resources.",
    "Ensure that employees work in a work environment that is conducive to safety/fairness/free of embarrassment.",
    "Employers and employees need to comply with legislation with regard to equal opportunities/human rights in the workplace.",
    "Training/Information/Business policies should include issues such as diversity/discrimination/harassment.",
    "Employers should respond swiftly and fairly to reported incidents of discrimination in the workplace.",
    "Orders/Tasks should be given respectfully and allow the recipient/employee to have a say in the way that task should be performed.",
    "Draw up a code of ethics/conduct.", "On-going development and training for all employees.",
    "Performance management systems/Appraisals should be in place.", "Adequate internal controls/monitoring/evaluation.",
    "Any other relevant answer related to ways in which professional, responsible, ethical and effective business practice should be "
    "conducted by businesses."],
    ["Professional, responsible, ethical, effective: how a business treats people, money and the environment.",
     "Respect, fair pay, transparency, taxes, a code of ethics, training."], each=2)]
missions_q4 = [
    {"id": "4.1", "title": "Question 4.1", "kind": "Compulsory insurance", "marks": 2, "items": q41},
    {"id": "4.2", "title": "Question 4.2", "kind": "Advantages of insurance", "marks": 6, "items": q42},
    {"id": "4.3", "title": "Question 4.3", "kind": "Presentations", "marks": 6,
     "lead": "Read the scenario below and answer the questions that follow.", "extract": "ELANGE LIMITED (EL)\n\n" + EL, "items": q43},
    {"id": "4.4", "title": "Question 4.4", "kind": "Capital and a private company", "marks": 6, "items": q44},
    {"id": "4.5", "title": "Question 4.5", "kind": "Problem-solving steps", "marks": 4, "items": q45},
    {"id": "4.6", "title": "Question 4.6", "kind": "Employee well-being", "marks": 6, "items": q46},
    {"id": "4.7", "title": "Question 4.7", "kind": "Human rights", "marks": 6,
     "lead": "Read the scenario below and answer the question that follows.", "extract": "BARROWS TRADERS (BT)\n\n" + BT,
     "table": {"title": "Use the table below as a GUIDE to answer QUESTION 4.7.", "head": ["HUMAN RIGHTS", "MOTIVATIONS"],
               "rows": [["1.", ""], ["2.", ""]]}, "items": q47},
    {"id": "4.8", "title": "Question 4.8", "kind": "Professional business practice", "marks": 4, "items": q48},
]

# ---- Section C: the essays (answer any ONE), the question paper page 9 and the memo pages 20-29 ----
# Each essay is one rubric part (as printed: one question of 40): the memo's points under its own headings and sub-maxima (facts
# capped at 32), and insight (8). Every point earns 1 here, as in the other Business Studies essays: the keyword stand-in cannot
# judge sub-maxima, repetition or insight, so an essay's mark waits for model marking.
INSIGHT = ["Insight (8), 2 each: Layout (an introduction, paragraphs and a conclusion, the words INTRODUCTION and CONCLUSION stated and "
           "explained); Analysis and interpretation (all headings addressed; interpreted correctly); Synthesis (only relevant facts); "
           "Originality (an example in any TWO of the four aspects, based on recent information, current trends and developments, not "
           "older than two years)."]
ESSAY_NOTES = ["Facts are capped at 32 of the 40; no marks for content repeated from the introduction or the conclusion."]
q5 = [rub("5", "Investors can acquire shares of companies that are listed on the Johannesburg Securities Exchange (JSE). They consider various "
          "factors when making investment decisions to choose the best option. Businesses prefer investing in unit trusts and they also compare "
          "simple and compound interest offered by financial institutions.\n\nWrite an essay on investment securities in which you include the "
          "following aspects:\n• Outline the functions of the Johannesburg Securities Exchange (JSE).\n• Explain any FOUR factors that should be "
          "considered when making investment decisions.\n• Discuss the impact of unit trusts as a form of investment.\n• Advise businesses on the "
          "differences between simple interest and compound interest.", 40, [
    "Introduction (any 2 x 1): the JSE serves as a financial market that regulates the activities of trading of securities in an orderly "
    "manner; sound knowledge of the factors to be considered when making investment decisions enables the investors to receive better returns "
    "on investment; unit trusts are a popular form of investment as investors from lower income groups can afford the minimum contributions "
    "needed; investors need to do research on the returns on investment by comparing the differences between the simple interest and compound interest.",
    "Functions of the JSE (max 10, 2 each): gives opportunities to financial institutions such as insurance companies investing their surplus "
    "funds in shares.",
    "JSE: serves as a barometer/indicator of economic conditions in South Africa.", "JSE: keeps investors informed by publishing share prices daily.",
    "JSE: acts as a link between investors and public companies.", "JSE: shares are valued and assessed by experts.",
    "JSE: small investors are invited to take part in the economy of the country through the buying/selling of shares.",
    "JSE: venture capital market is made possible on the open market.",
    "JSE: strict investment rules ensure a disciplined/orderly market for securities.",
    "JSE: raises primary capital by encouraging new investments in listed companies.",
    "JSE: mobilises the funds of insurance companies and other institutions.", "JSE: regulates the market for trading in shares.",
    "JSE: plans, researches and advises on investment possibilities.", "JSE: ensures that the market operates in a transparent manner.",
    "JSE: provides protection for investors through strict rules/legislation.",
    "JSE: encourages short-term investment as shares can be sold at any time.",
    "JSE: facilitates electronic trading of shares/STRATE/channels financial resources into productive economic activities.",
    "JSE: enhances job creation and increases economic growth/development.",
    "Factors for investment decisions (max 16; the first FOUR, each the factor 2 + explanation 2, submax 4): Return on investment/ROI.",
    "ROI: refers to income from the investment, namely interest/dividends/increased capital growth on the original amount invested.",
    "ROI: high/low risk investments yield higher/lower returns.", "ROI: the return should be expressed as net after-tax gains on the investment.",
    "ROI: generally, there will be a direct link between the risk and the return.",
    "ROI: returns can be in the form of capital gains where the asset appreciates in value over time.",
    "ROI: the return on investment after the deduction of tax should be higher than the general increase in the initial cost of investment.",
    "Risk (factor 2 + explanation 2).",
    "Risk: refers to the chance that the invested amount may be reduced in value/lost in total over a period of time, due to unforeseen circumstances.",
    "Risk: different risks are linked to different investment opportunities.",
    "Risk: the higher/lower the potential return, the higher/lower the risk of a potential loss.",
    "Risk: investing in shares has a higher risk than investing in a fixed deposit.", "Risk: shares have low/medium risk over a longer investment period.",
    "Risk: shares with higher risks have a greater potential for higher returns.",
    "Risk: ordinary shares have the highest risk as the investor may lose the full/part of the investment when the company is dissolved/bankrupt/liquidated.",
    "Risk: preference shareholders' risk is lower, as they have preferential claims on the assets of the liquidated company/may receive some "
    "compensation before ordinary shareholders.",
    "Risk: share prices are linked to factors which investors cannot always control, such as economic conditions/operational success of the company.",
    "Risk: share prices are volatile/unstable/unpredictable/may increase/decrease sharply within hours which contribute to the uncertainty of "
    "the value of an investment in shares on the short term.",
    "Investment term/period (factor 2 + explanation 2).",
    "Term: this refers to the duration of the investment which may influence the return on investment.",
    "Term: the investment period can be short/medium/long term depending on the nature of an investment option.",
    "Term: the investment period will depend on an investor's personal needs/goals.", "Term: the longer the investment period the higher the returns.",
    "Term: short term investments enable investors to access their money on a short period if needed.",
    "Inflation rate (factor 2 + explanation 2).",
    "Inflation: refers to a general increase in the price of goods/services over a period of time, resulting in a decrease in the value of money.",
    "Inflation: investors/people are affected by a high inflation rate, because their money/purchasing power decreases.",
    "Inflation: the return on investment should be higher than the inflation rate.",
    "Inflation: inflation has a positive effect on some investments such as property/shares where the income will increase as inflation increases.",
    "Taxation (factor 2 + explanation 2).", "Taxation: refers to a compulsory payment made by citizens to the government.",
    "Taxation: a good investment will yield good after-tax returns.",
    "Taxation: income tax implications must be considered in order to ensure a high net after-tax return.",
    "Taxation: tax rates are not necessarily the same for different investments.",
    "Liquidity (factor 2 + explanation 2).", "Liquidity: refers to the ease and speed with which investors can convert an investment into cash.",
    "Liquidity: an amount could be invested in a type of investment that can easily be converted to cash/is more liquid.",
    "Liquidity: an investment in a savings account/unit trust will be easier to convert into cash than an investment in a fixed deposit which "
    "is usually deposited for a fixed period of time.",
    "Impact of unit trusts (max 12, 2 each), positive: managed by a fund manager who buys shares on the stock exchange/JSE.",
    "Impact, positive: easy to cash in as there are no penalties for withdrawals when an investor needs all or part of the money at any time.",
    "Impact, positive: a small amount can be invested per month.", "Impact, positive: generally, beats inflation on the medium/long term.",
    "Impact, positive: safe investment, as it is managed according to rules and regulations.",
    "Impact, positive: the investor has a variety to choose from/a wider range of shares from lower to higher degrees of risk.",
    "Impact, positive: easy to invest in, as investors simply complete a few relevant forms or invest online.",
    "Impact, positive: fluctuations in unit trust rates of return are often not so severe because of diversity of the investment fund.",
    "Impact, positive: offer competitive returns in the form of capital growth and dividend distribution.",
    "Impact, positive: fund managers are knowledgeable/experts/reliable/trustworthy as they are required to be accredited to sell unit trusts.",
    "Impact, positive: lowers the potential risk allowing more people to invest in the fund.",
    "Impact, negative: share prices may fluctuate due to the volatility of the market.",
    "Impact, negative: unit trusts are not suitable for people who want to invest for a short period.",
    "Impact, negative: it is not a good option for people who want to avoid risks at all costs.",
    "Impact, negative: unit trusts are not allowed to borrow, therefore reducing potential returns.",
    "Impact, negative: if blue-chip companies do not continue on their growth path, the growth of unit trusts will also be affected/it will "
    "not render the expected returns.",
    "Impact, negative: bid prices that are usually higher than the ask price, making the investment less liquid.",
    "Simple and compound interest (max 8: simple submax 4, compound submax 4), simple interest: interest earned on the original amount and "
    "not on the interest accrued.",
    "Simple interest: the principal amount remains the same over the entire period of investment.",
    "Simple interest: the interest is kept separate unless it is reinvested.", "Simple interest: yields less return on investment.",
    "Simple interest: total amount of interest earned on investment is less.",
    "Compound interest: interest earned on the original amount invested, as well as interest earned in previous period(s).",
    "Compound interest: the principal amount grows with the addition of interest to it.",
    "Compound interest: interest is calculated on the higher principal amount and again added to it.",
    "Compound interest: yields high return on investment.", "Compound interest: total amount of interest earned on investment is high.",
    "Conclusion (any 1 x 2): JSE creates opportunities for the general public to participate in the economy of the country; choosing an "
    "investment opportunity should be informed by research findings gathered on various decision factors made; investing in unit trusts "
    "encourages small investors to invest in this form of investment due to its liquidity; a better understanding of how simple and compound "
    "interest is calculated will enable an investor to choose suitable and appropriate investment options.",
    "Any other relevant answer under each heading."] + INSIGHT,
    ["Plan four headings, one per bullet in the question, between an introduction and a conclusion.",
     "JSE: what it does. Factors: name four, explain each. Unit trusts: good AND bad. Interest: simple vs compound, both sides."],
    notes=["Factors for investment decisions: mark the first FOUR only.",
           "Simple and compound interest: the answer does not have to be a table and the differences need not link, but must be clear; a maximum "
           "of 4 if the differences are not clear or only one side is given."] + ESSAY_NOTES)]
q6 = [rub("6", "Corporate social responsibility and corporate social investment allow businesses to be actively involved in the projects that are "
          "positively benefiting the community. Successful businesses strive to maintain the relationship between social responsibility and "
          "triple bottom line and to find ways to deal with unemployment as a socio-economic issue.\n\nWrite an essay on social responsibility "
          "and corporate social responsibility in which you include the following aspects:\n• Outline the purpose of corporate social investment "
          "(CSI).\n• Discuss the impact of corporate social responsibility (CSR) on communities.\n• Explain the relationship between social "
          "responsibility and triple bottom line.\n• Suggest ways in which businesses can deal with unemployment as a socio-economic issue.", 40, [
    "Introduction (any 2 x 1): CSI is when a business commits money, resources and time to a specific project that will improve the lives of "
    "people; it is the responsibility of the business to ensure that the desired aims of corporate social responsibility (CSR) is filtered to "
    "the correct members of the community; triple bottom line expects businesses to commit to measuring their social and environmental impact "
    "in addition to financial performance; businesses have the responsibility to address unemployment as a socio-economic issue to avoid the "
    "risk of reduced sales.",
    "Purpose of CSI (max 8, 2 each): CSI aims at contributing towards sustainable growth/development of its immediate communities/new "
    "non-profit organisations/charities.",
    "Purpose: CSI is enforceable by law and government requires business to make CSI contributions.",
    "Purpose: CSI projects play a positive role in the development of communities.",
    "Purpose: CSI reveals a business's attitude towards the community in which it operates.", "Purpose: CSI projects are long-term investment.",
    "Purpose: it is relevant to the South African context where socio-economic upliftment is such a priority.",
    "Impact of CSR on communities (max 16, 2 each), positive: community skills can be improved through the provision of bursaries.",
    "Impact, positive: better educational facilities are established in poor communities.",
    "Impact, positive: the standard of living of the community is uplifted OR quality of life of communities is improved.",
    "Impact, positive: investing in the medical infrastructure, will improve the health of communities.",
    "Impact, positive: socio-economic issues are attended to/addressed which will improve the welfare of the community OR assists in solving "
    "socio-economic issues like poverty/unemployment.",
    "Impact, positive: training opportunities in the community increase the possibility of appointments of members of the community.",
    "Impact, positive: implementing developmental programmes in the community improves entrepreneurial skills of communities OR businesses "
    "become more community-based by working closely with the community to roll out skills development projects.",
    "Impact, negative: businesses are not always equipped to address social problems.",
    "Impact, negative: communities tend to be dependent on CSR programmes and struggle to take their own initiatives.",
    "Impact, negative: communities may not sustain infrastructure provided through CSR projects due to a lack of financial resources.",
    "Impact, negative: distribution of scarce resources to selected beneficiaries in the community may cause problems such as discrimination.",
    "Impact, negative: some businesses only participate in CSR initiatives to raise profit and do not really care for the community in which they operate.",
    "Impact, negative: businesses cannot meet the longer-term needs of the society OR businesses cannot deliver sustainable CSR programmes.",
    "Impact, negative: the benefits of the programmes may not filter to the intended persons within the community.",
    "Impact, negative: spending money on CSR programmes means the business has to recover expenses through higher prices which have a "
    "negative impact on the economy.",
    "Impact, negative: businesses tend to focus on CSR projects that do not directly benefit the community.",
    "Impact, negative: consumers are not easily convinced that the business is acting in the best interest of the community/environment.",
    "Impact, negative: less money is available for community projects during unfavourable economic conditions.",
    "Social responsibility and the triple bottom line (max 12; each element 2 + explanation 2, submax 4): Profit/Economic.",
    "Profit: triple bottom line means that businesses should not only focus on profit/charge high prices, but should also invest in CSI projects.",
    "Profit: businesses should not make a profit at the expense of its community.",
    "People/Social (element 2 + explanation 2).",
    "People: business operations should not exploit people/employees/customers which may have a negative impact/harm on the community.",
    "People: businesses should engage/invest in sustainable community programmes/projects that will benefit/uplift communities.",
    "People: improve the lifestyle/quality of life of their human resources/employees.",
    "Planet/Environment (element 2 + explanation 2).",
    "Planet: businesses should not exhaust resources/harm the environment for production/profit purposes.",
    "Planet: they may support energy-efficient/eco-friendly products/production methods.",
    "Planet: recycle/re-use waste, such as packaging from recycled material.",
    "Dealing with unemployment (max 10, 2 each): provide skills development programmes through learnerships.",
    "Unemployment: offer bursaries to the community to improve the level of education.", "Unemployment: create jobs for members of the community.",
    "Unemployment: provide entrepreneurial programmes that can promote self-employment.",
    "Unemployment: support existing small businesses to create more employment opportunities.",
    "Unemployment: use members of the community for implementing CSI projects in the community.",
    "Conclusion (any 1 x 2): corporate social investment projects have a strong developmental approach and utilise company resources to "
    "benefit and uplift communities; businesses must also take the challenges and problems of CSR into consideration, before deciding how to "
    "be involved in the community; businesses that maintain a sound relationship between social responsibility and triple bottom line remain "
    "sustainable in the long run; businesses that are able to deal with unemployment become profitable as the communities can afford to pay "
    "for goods and services.",
    "Any other relevant answer under each heading."] + INSIGHT,
    ["Plan four headings, one per bullet in the question, between an introduction and a conclusion.",
     "CSI: its purpose. CSR: good AND bad for communities. Triple bottom line: profit, people, planet. Unemployment: what a business can do."],
    notes=ESSAY_NOTES)]
missions_c = [
    {"id": "5", "title": "Question 5", "kind": "Essay: investment securities", "marks": 40, "items": q5},
    {"id": "6", "title": "Question 6", "kind": "Essay: social responsibility", "marks": 40, "items": q6},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Business Studies", "title": "Business Studies P2", "sitting": "November 2024", "total_marks": 150, "time": "2 hours"},
    "sections": [
        {"title": "Section A", "total": 30, "missions": missions_a},
        {"title": "Section B", "total": 80, "answer_any": 2, "missions": missions_q2 + missions_q3 + missions_q4},
        {"title": "Section C", "total": 40, "answer_any": 1, "missions": missions_c},
    ],
    "flags": [
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 6), hand-transcribed from the paper and memo PDFs; no API call."},
        {"n": "2.5.1", "kind": "low_confidence", "detail": "The keyword stand-in matches a word by its first five letters, so 'transformational' "
                                                           "and 'transactional' (a leadership style, wrong here) look the same to it; model "
                                                           "marking reads the memo point whole."},
        {"n": "2.3.2", "kind": "no_fit", "detail": "The memo's four ticks (formula, insured amount over market value, times the loss, the "
                                                   "answer) are played as two steps worth 2 each; the memo's 'full marks for the right answer "
                                                   "with no working' is met by filling both steps."},
        {"n": "3.3.1", "kind": "no_fit", "detail": "The quote item (3.3.1) is played by picking the scenario's sentences: the memo awards marks only "
                                                   "for responses quoted from the scenario, so picking the right sentences is the same skill."},
    ],
}
out = Path(__file__).parent / "out" / "bs-p2-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs (no API call)",
                                                        "scope": "Questions 1 to 6 (the whole paper)"}, "paper": paper}, indent=1, ensure_ascii=False),
                                   encoding="utf-8")
for sec in paper["sections"]:
    print(sec["title"], "parts:", sum(len(m["items"]) for m in sec["missions"]), "marks:", sum(i["marks"] for m in sec["missions"] for i in m["items"]),
          "answer any:", sec.get("answer_any", "all"))
