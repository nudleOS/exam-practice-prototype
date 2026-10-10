"""Business Studies P2 Nov 2024, the whole paper (Sections A, B and C), hand-transcribed into the catalogue format (as if Claude had
produced it), then run through `ingest.py --from-json` like any ingested paper. Stems, options, marks and memo points are the
paper's and the memo's own; the clues are ours. No API call: the transcription is the source, kept in git (out/ is not).

  python tools/ingest/transcribe_bs_p2_2024_11.py
  python tools/ingest/ingest.py "<...>/Business Studies P2 Nov 2024  Eng.pdf" "<...>/Business Studies P2 Nov 2024 MG Eng.pdf" --id bs-p2-2024-11 --from-json

(The question paper's file name has TWO spaces before "Eng", as the DBE named it.) The memo's shapes map as in Business Studies P1
Nov 2024 (transcribe_bs_p1_2024_11.py): marking instructions are `notes`; a name and its explanation or quote are two points,
`worth` [2, 1]; only an alternative answer's FIRST point starts with "OR" (2.5.2: one theory, either of two).

Since Murci's rulings of 2026-10-10 (as in transcribe_bs_p2_2025_11.py): every written answer of Section B plays as STATEMENTS to pick
(the memo's own points and clearly wrong ones) or, where the memo weighs two sides (2.6, 4.4), as a SORT; both essays play as
SECTIONS (one per memo heading, the facts summing to 32) plus an insight part; 2.3.2, the average-clause calculation, plays as a
whole-working multiple choice (the memo's working and three built from common errors, all or nothing, as in
transcribe_ml_p2_2025_11.py). The rubrics below stay as the source of the memo's points."""
import json
import re
from pathlib import Path


def mcq(n, q, opts, a, clues, marks=2):
    return {"t": "mcq", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts, "a": a}


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


WORK = "\n\nChoose the correct working."
AUTHORED = []   # the typed calculations played as authored multiple choice, in paper order


def shape(o):
    """An option's layout: its line count and how many lines end in a [reason]."""
    lines = o.split("\n")
    return len(lines), sum(1 for ln in lines if re.search(r"\[[^\[\]]+\]\s*$", ln))


def work(n, q, marks, opts, a, clues):
    """A typed calculation as authored multiple choice (Murci, 2026-10-10): opts are the memo's FIRST working and three workings
    built from common errors, one step a line, a fraction {numerator}/{denominator}; the part keeps its marks, all or nothing."""
    assert len(opts) == 4 and len(set(opts)) == 4, (n, "four distinct options")
    assert len({shape(o) for o in opts}) == 1 and shape(opts[0])[0] >= 2, (n, [shape(o) for o in opts])
    assert 0 <= a <= 3, (n, a)
    AUTHORED.append(n)
    return mcq(n, q + WORK, opts, a, clues, marks=marks)


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
        ["Which form of ownership exists to serve its own members?", "Members pool their resources and share the benefit among themselves."]),
    mcq("1.1.3", "Chidere Enterprise uses fine print to hide misleading information when promoting their products. This is known as ..., "
        "a type of unethical business practice.", ["taxation", "pricing of goods in rural areas", "fair advertising", "unfair advertising"], 3,
        ["Hiding misleading information is part of how a product is promoted.", "Is hiding information fair to the customer?"]),
    mcq("1.1.4", "The role of health and safety representatives is to ...",
        ["ensure that protective clothing is available.", "provide safety clothes to employees.", "use prescribed safety equipment.",
         "maintain equipment regularly."], 0,
        ["A health and safety representative is a worker chosen to look after the other workers' safety.",
         "Think about what someone who inspects the workplace on the workers' behalf would do."]),
    mcq("1.1.5", "Amajuba team members implement ... as a criterion for successful team performance by agreeing on methods to get the job "
        "done, without wasting time on conflict resolution.",
        ["shared values", "communication", "collaboration", "interpersonal attitudes and behaviour"], 2,
        ["Agreeing on how to get the job done together.", "Working together on the methods is ..."]),
]
WORDS = "bonus;  limited;  conflict;  cultural;  posters;  grievance;  social;  hand-outs;  unlimited;  founders'"
q12 = [
    term("1.2.1", "Visco Limited issued ... shares to the promoters of the company.", ["founders'", "founders", "founder's"],
         ["The promoters started the company.", "Special shares for the people who started the company and did the work to set it up."]),
    term("1.2.2", "Ben distributed ... at the start of the presentation to attract the attention of the audience.", ["hand-outs", "handouts", "hand outs"],
         ["Something each person in the audience holds.", "Printed sheets that each person in the audience gets to keep."]),
    term("1.2.3", "The shareholders at Blake Ltd have ... liability and can only lose the amount that they invested in the company.", ["limited"],
         ["There is a ceiling on what a shareholder can lose.", "They cannot lose more than they invested."]),
    term("1.2.4", "A disagreement between two or more parties in the workplace is known as a ...", ["conflict"],
         ["Not a formal complaint by one employee: a clash between parties.", "Two sides that do not agree are in ..."]),
    term("1.2.5", "Employees at Mawethu Traders are allowed to use their own language during their lunch breaks; this promotes their ... right "
         "in the workplace.", ["cultural"], ["Language, customs and traditions belong to a group's way of life.",
                                             "Which right protects language and traditions?"]),
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
              "Sort the terms first: a kind of cover, a kind of share, a technique, a King Code principle and a personality type."])]
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
           ["Places where a business can put money to grow.",
            "Think of what banks, insurers and fund managers offer people who want their money to grow."])]
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
    work("2.3.2", "Calculate the amount that AT will receive as compensation from the insurer. Show ALL the calculations.", 4, [
        "Compensation = {Market value}/{Insured amount} × Loss\n= {R400 000}/{R200 000} × R80 000\n= R160 000",          # the fraction inverted
        "Compensation = {Insured amount}/{Market value} × Market value\n= {R200 000}/{R400 000} × R400 000\n= R200 000",  # times the stock's value, not the loss
        "Compensation = {Insured amount}/{Market value} × Loss\n= {R200 000}/{R400 000} × R80 000\n= R40 000",            # the memo
        "Compensation = {Insured amount}/{Market value} × Loss\n= {R200 000}/{R400 000} × R80 000\n= R4 000"],            # a zero dropped
        2, ["Compare the amount insured with the stock's market value: what fraction is that?",
            "The insurer pays that fraction of the loss caused by the fire."]),
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
        ["EA's managers support and coach their people so that they change and grow.",
         "Which theory is about leaders who inspire and develop people to grow beyond what they thought they could do?"],
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
        ["Not the theory in 2.5.1: one theory looks at the bond between a leader and the team, another says the circumstances decide the style.",
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
    {"id": "2.3", "title": "Question 2.3", "kind": "Insurance", "marks": 6,
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
           ["Where does a business spend its CSI money and time?",
            "Think of who or what, outside the business's own profits, it chooses to support."])]
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
         ["Which sentences are about using work time well?",
          "Abuse of work time: personal matters, long breaks, idling. Which actions keep people working?"]),
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
         ["Five stages run from a team first meeting to a team breaking up.", "The team works well on its own, without supervision."]),
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
    {"id": "3.5", "title": "Question 3.5", "kind": "Team development", "marks": 8,
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
           ["Compulsory insurance is required by law.", "Think of the state funds that pay out when people cannot work or are hurt."])]
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
        ["A visual aid is something the audience looks at.", "Find the items in the scenario that show information to the shareholders."]),
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
           ["Solving a problem goes step by step, from the problem to checking the result.",
            "Picture a machine that keeps breaking: what would you do first, next and last?"])]
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
    ["One sentence is about respect; the other is about how management and staff talk to each other.",
     "Which human right protects a person's worth? Which one protects sharing your views and opinions openly?"],
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
# Each essay as printed (one question of 40): the memo's points under its own headings and sub-maxima (facts capped at 32), and
# insight (8). These rubrics are the SOURCE only: below, each essay's items are replaced by its sections and the insight part.
INSIGHT = ["Insight (8), 2 each: Layout (an introduction, paragraphs and a conclusion, the words INTRODUCTION and CONCLUSION stated and "
           "explained); Analysis and interpretation (all headings addressed; interpreted correctly); Synthesis (only relevant facts); "
           "Originality (an example in any TWO of the four aspects, based on recent information, current trends and developments, not "
           "older than two years)."]
ESSAY_NOTES = ["Facts are capped at 32 of the 40; no marks for content repeated from the introduction or the conclusion."]
Q5_STEM = ("Investors can acquire shares of companies that are listed on the Johannesburg Securities Exchange (JSE). They consider various "
           "factors when making investment decisions to choose the best option. Businesses prefer investing in unit trusts and they also compare "
           "simple and compound interest offered by financial institutions.\n\nWrite an essay on investment securities in which you include the "
           "following aspects:\n• Outline the functions of the Johannesburg Securities Exchange (JSE).\n• Explain any FOUR factors that should be "
           "considered when making investment decisions.\n• Discuss the impact of unit trusts as a form of investment.\n• Advise businesses on the "
           "differences between simple interest and compound interest.")
q5 = [rub("5", Q5_STEM, 40, [
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
Q6_STEM = ("Corporate social responsibility and corporate social investment allow businesses to be actively involved in the projects that are "
           "positively benefiting the community. Successful businesses strive to maintain the relationship between social responsibility and "
           "triple bottom line and to find ways to deal with unemployment as a socio-economic issue.\n\nWrite an essay on social responsibility "
           "and corporate social responsibility in which you include the following aspects:\n• Outline the purpose of corporate social investment "
           "(CSI).\n• Discuss the impact of corporate social responsibility (CSR) on communities.\n• Explain the relationship between social "
           "responsibility and triple bottom line.\n• Suggest ways in which businesses can deal with unemployment as a socio-economic issue.")
q6 = [rub("6", Q6_STEM, 40, [
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

# ---- Written answers as STATEMENTS (Murci 2026-10-10, as in transcribe_bs_p2_2025_11.py) ----
# A written part plays as picking statements: the memo's own points (right, tidied to one reading of its "/" alternatives) and
# CLEARLY wrong ones (never a true point the memo leaves out: its "any other relevant answer" would make that right). The learner
# picks marks/each of them, any right one counts (the memo's "any N"), each right pick earns `each`; the cards are shuffled the same
# way every run. The memo points above stay as the source. "Identify and motivate by quoting" (2.5.1, 4.7) pairs the name with its
# quote in one card worth 3 (name 2 + quote 1); 2.5.2 pairs a theory with one line of its explanation (theory 2 + explanation 1).
import random


def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random("bs-p2-2024-11:" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts,
            "pool": sorted(k for k, i in enumerate(order) if i < len(right)), "count": count}


EA2 = "'The management of EA provide emotional support for employees through coaching so that they can share their ideas more freely.'"
EA1 = "'Exclusive Architects operate in a competitive environment and had to improve the designs of their housing plans.'"
BT1 = "'They treat all employees with respect regardless of their socio-economic status.'"
BT2 = "'The management of BT encourages open communication channels between them and employees.'"
STATEMENTS = {
    "2.2": (2, ["Profits may be used to finance other state departments.",
                "It offers essential services which may not be offered by the private sector.",
                "Prices are kept reasonable to make services affordable to more citizens.",
                "Wasteful duplication of services is eliminated.", "Jobs are created for all skills levels."],
               ["It never needs funds from the government, because it always makes a profit.",
                "Its main aim is to make the highest possible profit for private shareholders.",
                "It is free from any government control or regulation."]),
    "2.4": (2, ["Select a background that complements the text.", "Use a legible font and font size so that the slides are easy to read.",
                "Make sure there are no language and spelling errors.",
                "Structure the information in a logical sequence so that the audience can follow the presentation.",
                "Limit the information on each slide by using key words and not full sentences."],
               ["Fill each slide with full paragraphs so that nothing is left out.",
                "Mix as many font styles and colours as possible on each slide.",
                "Use the smallest possible font so that more information fits on each slide."]),
    "2.5.1": (3, ["Transformational theory: " + EA2],
                 ["Situational theory: " + EA2, "Leaders and followers theory: " + EA2, "Transactional theory: " + EA1,
                  "Situational theory: " + EA1]),
    "2.5.2": (3, ["Leaders and followers theory: teams achieve great results when there is a sense of understanding between the leader and "
                  "the followers.",
                  "Situational theory: different leadership styles are needed for different situations, so leaders are adaptable and flexible.",
                  "Situational theory: leaders analyse the situation to get the most suitable people in the right positions to complete tasks."],
                 ["Situational theory: a leader uses the same leadership style in every situation.",
                  "Leaders and followers theory: followers make all the decisions and the leader simply carries them out.",
                  "Leaders and followers theory: leaders never reward positive behaviour, so that followers do not expect incentives."]),
    "2.7": (2, ["Be polite, confident and calm when responding to questions.",
                "Ensure that each question is clearly understood before responding.", "Keep answers short and to the point.",
                "Always address the question and not the person.", "Acknowledge mistakes if they are pointed out by the audience."],
               ["Argue with audience members until they agree with the presenter.",
                "Ignore questions that the presenter cannot answer and move on quickly.",
                "Answer only the person who asked, with your back to the rest of the audience."]),
    "3.2": (2, ["Use prescribed safety equipment.", "Report accidents to the employer by the end of the shift.",
                "Report unsafe or unhealthy working conditions to management.",
                "Inform the employer of any illness that may affect the ability to work.",
                "Take care of their own health and safety in the workplace."],
               ["Remove the safety guards from machines so that they can work faster.",
                "Keep accidents to themselves so that the employer is not bothered.",
                "Buy the safety equipment for all the other workers with their own money."]),
    "3.3.2": (2, ["Speak directly to those employees who abuse work time.",
                  "The code of conduct should contain clear rules about abuse of work time.",
                  "Conduct training on the contents of the code of conduct.",
                  "Structure working hours so that employees have flexible time for personal matters."],
                 ["Allow employees to run personal errands during working hours whenever they like.",
                  "Remove the rules about work time from the code of conduct.",
                  "Pay higher bonuses to the employees who take the longest breaks."]),
    "3.4": (2, ["Make time for brainstorming sessions to generate new ideas.",
                "Place suggestion boxes around the workplace and keep communication channels open for new ideas.",
                "Train staff in creative problem-solving skills, such as mind-mapping and lateral thinking.",
                "Reward creativity with incentives for staff members who come up with useful ideas.",
                "Respond enthusiastically to all ideas and never let anyone feel less important."],
               ["Criticise new ideas in front of other staff so that only the best ones are shared.",
                "Keep the workplace noisy and busy so that staff have no time to think.",
                "Allow only senior managers to suggest new ideas."]),
    "3.5.2": (2, ["Team dynamic theories explain how effective teams work.",
                  "Businesses are able to allocate tasks according to the roles of team members.",
                  "Team members can maximise performance, as tasks are allocated according to their abilities.",
                  "Theories help team leaders to understand the personality types of team members, so that tasks are assigned more effectively.",
                  "Conflict may be minimised when team members perform different roles."],
                 ["Team dynamic theories require every team member to perform the same role.",
                  "The theories guarantee that team members will never disagree.",
                  "Team dynamic theories are used to set the prices of a business's products."]),
    "3.6": (2, ["Acknowledge that there is conflict between the parties in the workplace.",
                "Identify the cause of the conflict to get clarity on its nature.",
                "Give each party the opportunity to express his or her own opinions and feelings.",
                "Brainstorm possible ways of resolving the conflict.", "Monitor progress to ensure that the conflict has been resolved."],
               ["Ignore the conflict, as it will resolve itself over time.",
                "Decide who is to blame and punish that party in front of the other staff.",
                "Dismiss everyone involved without hearing their side."]),
    "3.7": (2, ["Males and females should be offered equal employment opportunities.",
                "Business directors should promote both men and women to managerial positions.",
                "Targets may be set for gender equity in the business.", "New appointments should be based on skills and ability.",
                "Ensure that male and female employees are remunerated fairly and equally."],
               ["Pay men more than women for the same work.", "Appoint only men to managerial positions.",
                "Keep women out of training programmes to save costs."]),
    "4.2": (2, ["It transfers the risk from the business to the insurer.",
                "It protects businesses against theft and against damage caused by natural disasters such as floods.",
                "Businesses are compensated for insurable losses, such as the destruction of property through fire.",
                "It protects businesses against dishonest employees.",
                "It protects businesses from claims by members of the public for damages that the business is responsible for."],
               ["It allows a business to claim more than the value of its loss.",
                "The premiums are paid back to the business in full at the end of every year.",
                "It removes the need for the business to look after its assets."]),
    "4.3.2": (2, ["Revise the objectives that were not achieved.",
                  "Reflect on the time and length of the presentation to add or remove content.",
                  "Replace or remove visual aids that do not work well.",
                  "Analyse the feedback received and use it to update the presentation."],
                 ["Ignore the shareholders' comments, as the presentation is already over.",
                  "Add as much text as possible to every slide next time.",
                  "Read every slide word for word with your back to the audience."]),
    "4.6": (2, ["Pay fair wages to the workers, based on the nature of their work.",
                "Offer annual medical assessments to workers to promote health awareness.",
                "Make counselling available to any employee who requires it.", "Allow flexible working hours to enhance productivity.",
                "Make childcare facilities available on the premises for working mothers."],
               ["Cancel all leave so that employees spend more time at work.",
                "Make employees work longer hours without extra pay.",
                "Stop all training so that employees are not distracted from their work."]),
    "4.7": (3, ["Dignity: " + BT1, "Freedom of speech and expression: " + BT2],
               ["Privacy: " + BT2, "Safety, security and protection of life: " + BT1,
                "Access to information: 'Barrows Traders sell bicycles to different outlets.'"]),
    "4.8": (2, ["Draw up a code of ethics.", "Business decisions and actions must be transparent to all stakeholders.",
                "Pay fair wages in line with the minimum requirements of the BCEA.", "Pay taxes regularly and on time."],
               ["Hide the business's financial records from its stakeholders.",
                "Use other businesses' patented ideas without permission to save costs.",
                "Dump toxic waste wherever it is cheapest."]),
}
# A written part whose memo weighs two sides (positive / negative impact, success / failure) plays as a SORT instead (variety,
# Murci 2026-10-10): each statement dragged to its side, or to "Not true" (the clearly wrong ones), 1 mark a statement; a grouped
# match (the cards are reusable), so the platform and the service play it as they play a classification.
SORTS = {
    "2.6": (["Positive impact", "Negative impact", "Not true"], [
        ("Quick decisions can be taken without consulting employees.", 0),
        ("Clear guidance can be given to low-skilled, inexperienced or new staff.", 0),
        ("Workers can become demotivated if their opinions and ideas are not considered.", 1),
        ("New, creative or cost-reducing ideas may not be considered or implemented.", 1),
        ("Employees take all the decisions, so the leader has no control over the work.", 2),
        ("Every employee is consulted before any decision is taken.", 2)]),
    # (the memo's success point 'large amount of capital can be raised' and its failure point 'large amount of capital cannot be
    # obtained' contradict each other: only the first of the two is a row)
    "4.4": (["Success", "Failure", "Not true"], [
        ("A large amount of capital can be raised, since there is no limit on the number of shareholders.", 0),
        ("The company can access long-term capital and therefore has good long-term growth opportunities.", 0),
        ("It cannot grow into a very large business, since it cannot invite the public to buy shares.", 1),
        ("Restrictions on the transferability of shares may not attract financially strong investors.", 1),
        ("It raises capital by selling its shares to the public on the JSE.", 2),
        ("Its shareholders are personally liable for all of the company's debts.", 2)]),
}


def sort_(n, q, marks, bins, rows, clues):
    order = list(range(len(rows)))
    random.Random("bs-p2-2024-11:sort:" + n).shuffle(order)
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
assert tuple(AUTHORED) == ("2.3.2",), AUTHORED


# ---- The essays as SECTIONS (Murci 2026-10-10): the memo's headings, each played as statements or a sort, their facts summing to the
# memo's cap of 32, then an INSIGHT part (LASO, 8) worked out from the picks (Layout: introduction + conclusion right; Analysis: every
# heading answered; Synthesis: every section right first time; Originality: the example statements picked). The essay's own wording
# goes to the mission's extract; the memo points above stay as the source.
def essay(nums, parts, examples, insight_clues):
    ex = [[n, next(p for p in parts if p["n"] == n)["opts"].index(t)] for n, t in examples]
    assert sum(p["marks"] for p in parts) == 32, [p["marks"] for p in parts]
    return parts + [{"t": "insight", "n": nums, "marks": 8, "q": "Insight: your essay's layout, analysis, synthesis and originality, worked out "
                     "from your picks.", "clues": insight_clues, "of": [p["n"] for p in parts], "intro": parts[0]["n"], "conclusion": parts[-1]["n"],
                     "examples": ex}]


INSIGHT_CLUES = ["Insight is earned from how you answered the sections.", "Right first time, every heading answered, and the examples picked."]
Q5_EX = ["For example, a pension fund invests its members' surplus money in shares that are listed on the JSE.",
         "For example, a young worker buys a few shares in a listed retailer through an online share-trading account."]
q5_parts = essay("5.7", [
    stmt("5.1", "Introduction: pick the TWO statements that introduce this essay on investment securities.", 2,
         ["The JSE serves as a financial market that regulates the trading of securities in an orderly manner.",
          "Sound knowledge of the factors to consider when making investment decisions enables investors to receive better returns.",
          "Unit trusts are a popular form of investment, as investors from lower income groups can afford the minimum contributions."],
         ["The JSE guarantees that every investor makes a profit on the shares that he or she buys.",
          "Unit trusts are only available to very wealthy investors.",
          "Simple and compound interest always give an investor exactly the same return."],
         ["An introduction says what the essay is about and why it matters to investors.", "The JSE, investment decisions, unit trusts, interest."], 1),
    stmt("5.2", "Outline the functions of the Johannesburg Securities Exchange (JSE).", 6,
         ["Serves as an indicator of economic conditions in South Africa.", "Keeps investors informed by publishing share prices daily.",
          "Acts as a link between investors and public companies.", "Provides protection for investors through strict rules and legislation."] + Q5_EX,
         ["Prints the banknotes and coins used in the South African economy.",
          "Guarantees that the price of every listed share rises each year."],
         ["The JSE is where shares in listed companies are bought and sold.", "What does it do for investors, for companies and for the economy?"], 2),
    sort_("5.3", "Explain any FOUR factors that should be considered when making investment decisions.", 8,
          ["Return on investment", "Risk", "Inflation rate", "Liquidity", "Not true"], [
        ("It is the income from an investment, such as interest, dividends or capital growth.", 0),
        ("Returns can come as capital gains, when the asset increases in value over time.", 0),
        ("It is the chance that the amount invested may lose value or be lost completely.", 1),
        ("Ordinary shareholders may lose all or part of their investment if the company is liquidated.", 1),
        ("Investors are affected when prices rise quickly, because their purchasing power decreases.", 2),
        ("It is the ease and speed with which an investment can be converted into cash.", 3),
        ("A higher potential return always comes with a lower chance of a loss.", 4),
        ("A fixed deposit can be converted into cash more easily than a savings account.", 4)],
        ["Each factor answers a different question: what will I earn, what could I lose, what will my money buy, how fast can I get it?",
         "Read what each statement describes, not only its words."]),
    sort_("5.4", "Discuss the impact of unit trusts as a form of investment.", 8, ["Positive impact", "Negative impact", "Not true"], [
        ("A small amount can be invested every month.", 0),
        ("It generally beats inflation over the medium to long term.", 0),
        ("Fluctuations in returns are often less severe, because the fund is diversified.", 0),
        ("Unit trusts are not suitable for people who want to invest for a short period.", 1),
        ("It is not a good option for people who want to avoid risk at all costs.", 1),
        ("Unit trusts are not allowed to borrow, which reduces potential returns.", 1),
        ("Returns are guaranteed, because the government pays a fixed interest rate on unit trusts.", 2),
        ("Investors can never withdraw their money before the fund closes down.", 2)],
        ["A unit trust pools many investors' money in a fund run by a fund manager.", "Good AND bad: who gains from it, and who should avoid it?"]),
    sort_("5.5", "Advise businesses on the differences between simple interest and compound interest.", 6,
          ["Simple interest", "Compound interest", "Not true"], [
        ("Interest is earned on the original amount only, and not on the interest accrued.", 0),
        ("The principal amount remains the same over the entire investment period.", 0),
        ("Interest is earned on the original amount as well as on the interest of previous periods.", 1),
        ("The principal amount grows as interest is added to it.", 1),
        ("The interest earned gets smaller every year, even though nothing is withdrawn.", 2),
        ("The investor pays interest to the bank on the money that he or she has invested.", 2)],
        ["Ask of each statement: is interest ever earned on interest?", "Over many years, which kind of interest earns more?"]),
    stmt("5.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["The JSE creates opportunities for the general public to participate in the economy of the country.",
          "A better understanding of how simple and compound interest is calculated enables an investor to choose suitable investment options."],
         ["Investors should choose an investment without doing any research.",
          "Small investors should avoid unit trusts, as they can never afford the contributions.",
          "The JSE should be closed to small investors to protect the economy."],
         ["A conclusion sums up why the topic matters.", "Participation, research and informed choices."], 2),
], [("5.2", Q5_EX[0]), ("5.2", Q5_EX[1])], INSIGHT_CLUES)

Q6_EX = ["For example, a mining company offers bursaries to learners from the towns near its mines.",
         "For example, a supermarket chain buys fresh produce from small local farmers, so that they can employ more people."]
q6_parts = essay("6.7", [
    stmt("6.1", "Introduction: pick the TWO statements that introduce this essay on social responsibility.", 2,
         ["CSI is when a business commits money, resources and time to a specific project that will improve the lives of people.",
          "Triple bottom line expects businesses to measure their social and environmental impact in addition to financial performance.",
          "Businesses have the responsibility to address unemployment as a socio-economic issue to avoid the risk of reduced sales."],
         ["CSI means that a business focuses only on making a profit for its shareholders.",
          "Unemployment is only the government's problem, so businesses can ignore it.",
          "CSR projects benefit only the owners of the business and never the community."],
         ["An introduction says what the essay is about and why it matters.", "CSI, CSR, the triple bottom line, unemployment."], 1),
    stmt("6.2", "Outline the purpose of corporate social investment (CSI).", 6,
         ["CSI aims at contributing towards the sustainable development of its immediate communities.",
          "CSI projects play a positive role in the development of communities.",
          "CSI reveals a business's attitude towards the community in which it operates.", "CSI projects are a long-term investment.",
          "It is relevant to the South African context, where socio-economic upliftment is a priority."],
         ["CSI is used to replace the salaries that a business pays its own employees.",
          "The purpose of CSI is to avoid paying any company tax.",
          "CSI money is spent only on the business's own shareholders."],
         ["CSI: a business investing money, time and resources in its community.",
          "What does it aim to achieve, and what does it show about the business?"], 2),
    sort_("6.3", "Discuss the impact of corporate social responsibility (CSR) on communities.", 8,
          ["Positive impact", "Negative impact", "Not true"], [
        ("Community skills can be improved through the provision of bursaries.", 0),
        ("Better educational facilities are established in poor communities.", 0),
        ("Investing in medical infrastructure improves the health of communities.", 0),
        ("Communities tend to depend on CSR programmes and struggle to take their own initiatives.", 1),
        ("Communities may not sustain the infrastructure provided, due to a lack of financial resources.", 1),
        ("The benefits of the programmes may not filter through to the intended people in the community.", 1),
        ("Community members must pay the business back for every CSR project.", 2),
        ("A business that runs CSR programmes no longer has to obey labour laws.", 2)],
        ["CSR is a business looking after the community around it.", "Good AND bad: what improves, and what can go wrong?"]),
    sort_("6.4", "Explain the relationship between social responsibility and triple bottom line.", 8, ["Profit", "People", "Planet", "Not true"], [
        ("A business should not focus only on profit or charge high prices, but should also invest in CSI projects.", 0),
        ("A business should not make a profit at the expense of its community.", 0),
        ("Business operations should not exploit employees or customers.", 1),
        ("Businesses should improve the quality of life of their employees.", 1),
        ("Businesses may support energy-efficient and eco-friendly production methods.", 2),
        ("Businesses should recycle and re-use waste, such as packaging.", 2),
        ("The triple bottom line measures only a business's financial performance.", 3),
        ("Businesses should use up natural resources quickly while they are still cheap.", 3)],
        ["Three Ps: one about money, one about people, one about the environment.",
         "Which part of the business's impact does each statement look after?"]),
    stmt("6.5", "Suggest ways in which businesses can deal with unemployment as a socio-economic issue.", 6,
         ["Provide skills development programmes through learnerships.", "Create jobs for members of the community.",
          "Provide entrepreneurial programmes that can promote self-employment.",
          "Use members of the community to implement CSI projects in the community."] + Q6_EX,
         ["Replace local workers with imported labour wherever it is cheaper.",
          "Stop hiring young people until they have many years of work experience."],
         ["Unemployment: people who want work but cannot find it.", "Skills, jobs, self-employment, small businesses."], 2),
    stmt("6.6", "Conclusion: pick the statement that concludes this essay.", 2,
         ["CSI projects have a strong developmental approach and use company resources to benefit and uplift communities.",
          "Businesses that maintain a sound relationship between social responsibility and the triple bottom line remain sustainable in the long run."],
         ["Businesses should avoid CSR, as it never benefits communities.",
          "Dealing with unemployment makes a business less profitable in every case.",
          "Social responsibility is a cost that no successful business should carry."],
         ["A conclusion sums up why it all matters.", "Development, sustainability and profit in the long run."], 2),
], [("6.5", Q6_EX[0]), ("6.5", Q6_EX[1])], INSIGHT_CLUES)

for _m, _parts, _stem, _q in ((missions_c[0], q5_parts, Q5_STEM, "5"), (missions_c[1], q6_parts, Q6_STEM, "6")):
    _m["items"] = _parts
    _m["lead"] = "Build the essay section by section, then see your insight."
    _m["extract"] = "QUESTION " + _q + ": THE ESSAY\n\n" + _stem   # (the essay's wording in the shared-information card: on a phone it folds away)

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
        {"n": "2.3.2", "kind": "no_fit", "detail": "Authored multiple choice (Murci, 2026-10-10): the average-clause calculation plays as the "
                                                   "memo's working plus three built from common errors (the fraction inverted, multiplied by "
                                                   "the stock's market value instead of the loss, a zero dropped), 0 or 4 marks; the memo's part "
                                                   "marks (3 for a right working with a wrong answer, 1 for the formula alone) are not given."},
        {"n": "4.4", "kind": "memo_issue", "detail": "The memo's success point 'Large amount of capital can be raised since there is no limit on "
                                                     "the number of shareholders' and its failure point 'Large amount of capital cannot be "
                                                     "obtained as capital contribution is only limited to private shareholders' contradict each "
                                                     "other; the sort uses only the first."},
        {"n": "5.4", "kind": "memo_issue", "detail": "The memo's negative point 'Bid prices that are usually higher than the ask price, making the "
                                                     "investment less liquid' has the two prices the wrong way round (a bid is normally below the "
                                                     "ask); it is not used as a statement. The memo's heading 5.2 prints 'Johannesburg Security "
                                                     "Exchange' (the paper: Securities)."},
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
