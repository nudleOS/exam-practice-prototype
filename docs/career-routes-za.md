# Career routes: South Africa (researched 2026-10-28)

**Purpose.** The data behind the industry page's course field and its clickable career pills. A learner picks a career or a
course; the page then offers only the levels and subjects that course uses, and so only those subjects' past papers.
Facts are per country; South Africa first (Murci 2026-10-27).

**Rules for this file.**
- Every fact comes from a page a research agent opened (WebFetch) on 2026-10-28. The source number is in brackets.
- An empty cell means not verified. It is never filled from memory, and APS scores and subject levels are never guessed.
- "L5" means NSC achievement level 5 (60-69%).
- Requirements are one example institution's, for its current intake. Other institutions differ: e.g. BPharm Maths is L3 at
  UKZN but L5 at NWU.
- A minimum does not guarantee a place (most of the pages say so).

**How it was checked.** Three parallel research agents covered three industries each. I re-opened three of their sources
myself and all three matched exactly:
- Wits Mechanical Engineering: APS 42+, English / Maths / Physical Sciences each at L5.
- UMP Diploma in Nature Conservation: APS 28; English L4; Maths L2 (30%) or Maths Literacy L4; Life Sciences L4.
- False Bay College NC(V) IT and Computer Science: its level 2-4 subject lists.

A gap-filling round filled 13 of the 17 open careers; what is left is under "Open after the gap round".

**Blocked while researching:**
- These sites returned 403: up.ac.za, uj.ac.za, su.ac.za, irba.co.za.
- These failed with a certificate error or 403: hpcsa.co.za, sanc.co.za, samsa.org.za.
- DHET's "NC(V) Matrix of Subjects" PDF is unreadable. NC(V) subject lists therefore come from the DBE NC(V) guideline pages
  or from a college's programme page.

**In the page (2026-10-28, Murci picked direction A).** `COURSES` in `Exam Practice.dc.html` holds one entry per route
below. On the industry page:
- **Tapping a career pill** picks its course; the one that fits the saved level comes first. Tapping it again lets go.
- **The Course field** (step 1) lists the industry's courses, plus "All courses".
- **A course narrows the fields below it.**
  - Level: only its kind of school. Picking a course of the other kind saves Grade 12 or NC(V) Level 4.
  - Subject: a school course's named subjects, or an NC(V) programme's subjects at that level.
  - Paper follows the subject.
- **Under the fields:** the requirement as the source states it and what follows after study. The source link is not shown on the card (Murci 2026-10-28); the sources stay in `COURSES` and below.
- **"After school" is gone.** Finance's Finance-only box (RE5 / RE1) is now part of the Financial adviser and Insurance broker
  courses.
- **When a course names no subject with papers here,** the industry's subjects show, and the hint says so.

**Routes by level, as the app will use them:**
- **School (NSC, Grades 10-12).** A course is the learner's *target*. Its required subjects are the ones to practise.
- **TVET NC(V) L2-L4.** The course *is* the programme. It has 3 fundamentals (a language; Mathematics or Mathematical
  Literacy; Life Orientation, now Life Skills and Computer Literacy) plus its vocational subjects. Those subjects are the
  ones to practise.
- **NATED N4-N6.** In teach-out to about 2027/28 (project_tvet_curriculum_facts). None is listed here.
- **University.** A degree's modules. No past papers yet, so the course is shown without papers.

## Engineering & Manufacturing

| Career | Route | School subjects (minimum) | After study |
|---|---|---|---|
| Mechanical engineer | BSc (Eng) Mechanical, Wits (APS 42+) [1] | English L5, Maths L5, Physical Sciences L5 [1] | ECSA Pr Eng: accredited degree, then training, reports, review interview [2] |
| | NC(V) Engineering and Related Design [3] | Vocational: Automotive Repair and Maintenance; Engineering Fabrication; Engineering Fundamentals; Engineering Systems; Engineering Technology; Fitting and Turning; Welding [3] | |
| Electrical engineer | BSc (Eng) Electrical, Wits (APS 42+) [4] | English L5, Maths L5, Physical Sciences L5 [4] | ECSA Pr Eng [2] |
| | NC(V) Electrical Infrastructure Construction [3] | Vocational: Electrical Principles and Practice; Electrical Systems and Construction; Electronic Control and Digital Electronics; Workshop Practice [3] | |
| Mechatronics engineer | BIng Mechatronic, NWU (APS 34) [5] | Maths L6, Physical Sciences L6, English L5 [5] | ECSA Pr Eng [2] |
| Chemical engineer | BSc (Eng) Chemical, Wits (APS 42+) [6] | English L5, Maths L5, Physical Sciences L5 [6] | ECSA Pr Eng [2] |
| Industrial engineer | BSc (Eng) Industrial, Wits (APS 42+) [7] | English L5, Maths L5, Physical Sciences L5 [7] | ECSA Pr Eng [2] |
| Engineering technician | Accredited National Diploma (institution not verified) | | ECSA Pr Techni Eng: accredited diploma, workplace experience, reports, review [8] |
| | NC(V) Engineering and Related Design [3] | as above | |
| Fitter and turner | NC(V) Engineering and Related Design (has Fitting and Turning) [3] | as above | Trade test at a QCTO-accredited centre; QCTO issues the trade certificate [9] |

## Built Environment & Construction

| Career | Route | School subjects (minimum) | After study |
|---|---|---|---|
| Civil engineer | BSc (Eng) Civil, Wits (APS 42+) [10] | English L5, Maths L5, Physical Sciences L5 [10] | ECSA Pr Eng [2] |
| | NC(V) Civil Engineering and Building Construction [3] | Vocational: Construction Carpentry and Roof Work; Concrete Structures; Construction Masonry and Tiling; Construction Materials; Construction Plant and Equipment; Construction Plumbing; Drawings and setting out, quantities and costing; Roads [3] | |
| Construction manager | BSc Construction Economics Management, UFS (3 years; AP 30) [59] | Maths L5; English L4; one of Physical Science / Accounting / Economics / Business L4 [59] | SACPCMP PrCM: an NQF 8 qualification (e.g. BSc Hons Construction Management) plus 5 years' experience [60] |
| Land surveyor | Geomatics degree, UCT [11] | English, Maths, Physical Science (no levels stated; Geography not required) [11] | SAGC: candidate, mentored training, Law exam(s), then Professional [12] |
| Architect | BAS, then Honours and MArch (Prof), UCT [13] | English 50%, Maths 50% (Maths Literacy not accepted; Physics not required); portfolio [13] | SACAP registration, required to practise [13][14] |
| Quantity surveyor | BSc Construction Economics Management, UFS (AP 30) [59] | Maths L5; English L4; one of Physical Science / Accounting / Economics / Business L4 [59] | SACQSP: accredited degree, 33+ months in-service training, interview [15] |
| Town planner | BSc (URP), Wits (APS 36+) [16] | English L5, Maths L5 [16] | |
| Electrician | NC(V) Electrical Infrastructure Construction [3] | as under Engineering | |

## Mining & Energy

| Career | Route | School subjects (minimum) | After study |
|---|---|---|---|
| Mining engineer | BSc (Eng) Mining, Wits (APS 42+) [17] | English L5, Maths L5, Physical Sciences L5 [17] | ECSA Pr Eng [2] |
| Geologist | BSc Geological Sciences, Wits (APS 42+) [18] | English L5, Maths L6, Physical Science L5 [18] | |
| Power engineer | BSc (Eng) Electrical, Wits (nearest verified; no "power" degree found) [4] | English L5, Maths L5, Physical Sciences L5 [4] | ECSA Pr Eng [2] |
| Metallurgist | BSc (Eng) Metallurgy and Materials, Wits (APS 42+) [19] | English L5, Maths L5, Physical Sciences L5 [19] | ECSA Pr Eng [2] |
| Renewable energy technician | National Occupational Certificate: Solar PV Standalone Systems Installer, NQF 4 (MERSETA) [61] | Entry: an NQF 3 qualification with Maths (level not stated) [61] | |
| Mine surveyor | Mine Surveyor's Certificate of Competency under the Mine Health and Safety Act regulations [62] | *exam, experience and entry open* | |

## Health & Life Sciences

| Career | Route | School subjects (minimum) | After study |
|---|---|---|---|
| Doctor | MBBCh, Wits (6 years; NSC 75% + NBT 25%) [20] | English L5, Maths L5, Life and/or Physical Sciences L5 [20] | HPCSA, after internship and community service [21] |
| Physiotherapist | BSc Physiotherapy, Wits [22] | English L5, Maths L5, Life and/or Physical Sciences L5; 16 h observing a physio [22] | HPCSA: community service, then independent [23] |
| Pharmacist | BPharm, UKZN [24] | English L4, Life Sciences L4, Life Orientation L4, Maths L3, Physical Sciences L4 [24] | SAPC (intern steps not verified) [25] |
| | BPharm, NWU (APS 32) [26] | Maths L5, Physical Sciences L5, English or Afrikaans L4 [26] | SAPC [25] |
| Nurse | BNurs, Wits [27] | English L4, Maths L4, Life and/or Physical Sciences L4 [27] | |
| | BNurs, NWU (APS 25) [28] | Physical Science, Life Sciences or Maths L4; English or Afrikaans L4 [28] | SANC General Nursing and Midwifery, after 1 year community service [28] |
| Radiographer | BRad Diagnostics, CUT (APS 30) [29] | Life Sciences L4, Physical Sciences L4, Maths L4, Life Orientation L3 [29] | HPCSA Diagnostic Radiographer [29] |
| Occupational therapist | BSc OT, UWC (33 points) [63] | English L4; another language L3; Maths L3 or Maths Literacy L5; Life Sciences L4 [63] | |
| | BOT, UKZN (30 points excl. LO) [64] | Maths L3; Life Sciences or Physical Science L3; LO L4; English L4 (the two UKZN pages differ on English) [64] | |
| Paramedic | Bachelor of Emergency Medical Care (SAQA 91791) [31] | *levels open* | HPCSA Independent Emergency Care Practitioner [31] |
| | Higher Certificate in Emergency Medical Care, NQF 5 (DUT per SAQA) [65] | Entry: NSC or NC(V) L4 with higher-certificate access (no subjects stated) [65] | entry-level emergency care |

## Environment, Agriculture & Natural Resources

| Career | Route | School subjects (minimum) | After study |
|---|---|---|---|
| Agricultural scientist | BSc Agric (Agribusiness), UKZN (APS 28) [32] | English L4, Maths L4, one of Agricultural / Life / Physical Sciences L4 [32] | SACNASP, Agricultural Science field [33] |
| Environmental scientist | BSc Environmental Science, UKZN (APS 28) [34] | Maths L4, one of Physical / Life / Agricultural Sciences L4 [34] | SACNASP, Environmental Science field [33] |
| Forester | BSc Forestry, UMP (requirements not on page) [35] | | SACNASP (Forestry sits in Agricultural Science) [33] |
| Farm manager | NC(V) Primary Agriculture, Nkangala TVET [36] | Vocational: Soil Science; Plant Production; Animal Production; Farm Planning and Mechanization; Agribusiness; Agricultural Management Practices; Sustainable Agricultural Practices [36] | |
| | BSc Agric (Agribusiness), UKZN (nearest degree) [32] | as Agricultural scientist | |
| Conservation officer | Diploma in Nature Conservation, UMP (APS 28) [37] | English L4; Maths L2 or Maths Literacy L4; Life Sciences L4 [37] | |
| | Diploma in Nature Conservation, UNISA [38] | English 50%, Maths 50%, one of Physical / Life / Agricultural Science 40% [38] | |
| Soil scientist | BSc Agric (Agribusiness), UKZN (nearest degree; not soil-specific) [32] | as Agricultural scientist | SACNASP, Soil Science field [33] |

## Finance, Insurance & Business

| Career | Route | School subjects (minimum) | After study |
|---|---|---|---|
| Financial adviser | BCom Financial Planning, NMU (FPI-accredited) [39] | Maths 50% (extended programme 45%) [39] | FPI Financial Services Associate [39]; FAIS RE5 for representatives, RE1 for key individuals [40] |
| | NC(V) Finance, Economics and Accounting [41] | Vocational: Applied Accounting; Economic Environment; Financial Management; Project Management [41] | |
| Insurance broker | BCom Economics with Risk Management, NWU (APS 26; nearest: not a broking qualification) [66] | Maths L4, English L4 (extended programme: Maths L3 or Maths Literacy L6, English L3) [66] | FAIS RE5 [40] |
| Accountant | BCom Accounting, Wits (APS 38+) [42] | English L5, Maths L5 [42] | SAICA CA(SA): endorsed degree and PGDA, ITC, training contract, APC [43] |
| | NC(V) Finance, Economics and Accounting [41] | as above | |
| Actuary | BSc Actuarial Science, Wits (APS 44+; NBT) [44] | English L7, Maths L7, Physical Science L7 [44] | ASSA Fellowship (FASSA): exams plus work experience; degree exemptions [45] |
| Auditor | BCom Accounting, Wits (APS 38+) [42] | English L5, Maths L5 [42] | IRBA Public Practice Exam admission: CTA, SAICA Qualifying Exam Part I, 18 months' training, an auditing specialism course (reproduced text; may be dated) [67] |
| Economist | BCom (Economics), Wits (APS 38+) [46] | English L5, Maths L5 [46] | |

## ICT & Digital

| Career | Route | School subjects (minimum) | After study |
|---|---|---|---|
| Software developer | BSc Computer Science, Wits (APS 44+) [47] | English L5, Maths L6 [47] | |
| | NC(V) Information Technology and Computer Science [48] | Vocational: L2 Introduction to Information Systems, Electronics, Introduction to Systems Development, Multimedia Basics; L3 Systems Analysis and Design, Computer Hardware and Software, Principles of Computer Programming, Multimedia Content; L4 Data Communication and Networking, Computer Programming, Multimedia Service, Systems Analysis and Design [48] | |
| Data analyst | BSc Statistics and Computer Science, UKZN (APS 30) [68] | Maths L4, English L4, LO L4, one of Agricultural / Life / Physical Science L4 [68] | |
| | Diploma in IT, VUT (APS 26) [69] | English L4; Maths or Technical Maths L4 (or Maths Literacy L6) [69] | |
| Cybersecurity analyst | Diploma in IT, VUT (nearest: general IT, no security specialism) [69] | as above [69] | |
| Network engineer | NC(V) IT and Computer Science (L4 Data Communication and Networking) [48] | as above | |
| IT technician | NC(V) IT and Computer Science (L3 Computer Hardware and Software) [48] | as above | |
| UX designer | Diploma: Fashion, Photography, Graphic Design and Fine Art, VUT (APS 21; portfolio + interview; nearest: not UX) [70] | English L4; Maths L2 or Maths Literacy L3 [70] | |

## Transport, Logistics & Aviation

| Career | Route | School subjects (minimum) | After study |
|---|---|---|---|
| Logistics planner | NC(V) Transport and Logistics (DHET NC(V) Matrix of Subjects 2015, the source of the page's NC(V) data; no public link) | Its subjects per level as in the page's `NCV_COMPULSORY` | |
| Commercial pilot | CPL(A) under Civil Aviation Regulations 2011, Part 61; training at a Part 141 school [49][71] | No school subjects in the regulation. Age 18+, Part 67 medical, theory exam, skills test, night rating; 200 h total (150 integrated), 100 h PIC (reproduced text) [71] | SACAA licence [49] |
| Aircraft maintenance engineer | AME licence, Part 66 (licence route) [49][72] | No school subjects in the regulation. Age 21+, employed by an approved maintenance organisation, training, theory exam, experience (reproduced text) [72] | SACAA licence [49] |
| Air traffic controller | ATNS training (2015 bursary notice; current intake not verified) [50] | Maths L4, English L4 (2015 notice) [50] | |
| Supply chain manager | NC(V) Transport and Logistics (as above) | as above | |
| Ship's officer | Bachelor of Nautical Science, NQF 7 (CPUT per SAQA) [73] | English, Maths, Physical Science (no levels stated); or NC(V) L4 with the same [73] | |
| | Diploma in Nautical Studies, NQF 6 (DUT per SAQA) [74] | Entry: NSC with bachelor access or NC(V) L4 (no subjects stated); SAMSA eyesight + medical [74] | Underpins SAMSA deck officer certificates [74] |
| | SAMTRA Mates and Masters (STCW A-II/2) [51] | *entry open* | |

## Education & Social Services

| Career | Route | School subjects (minimum) | After study |
|---|---|---|---|
| Foundation phase teacher | BEd Foundation Phase, Wits (APS 37) [52] | English L5; Maths L4 or Maths Literacy L5 or Technical Maths L5 [52] | SACE registration [53] |
| Maths teacher | BEd SP and FET, Wits (APS 37) [54] | English L5 (no Maths needed for entry; Maths is a 2nd-year option) [54] | SACE [53] |
| Science teacher | BEd SP and FET, Wits (APS 37) [54] | English L5 (science specialisation from 2nd year) [54] | SACE [53] |
| Early childhood practitioner | NC(V) Education and Development, eThekwini TVET [55] | Vocational: Arts & Science of Teaching; Human and Social Development; Learning Psychology; Early Childhood Development [55] | |
| Social worker | BSW, UFS (top 50 selected) [56] | English L5; five academic subjects L5, one more L4 [56] | SACSSP social worker; police clearance [57] |
| Educational psychologist | *university route open* | | HPCSA Psychology board exam (secondary source only) [58] |

## Open after the gap round (2026-10-28)

**No sourced route yet.** Every source sat behind a blocked site; the snippets were not opened, so they were not used.
- Educational psychologist: every university page was blocked.
- Logistics planner and Supply chain manager have only the NC(V) route. The public diplomas (e.g. TUT, VUT) 404'd.

**Partial.**
- Mine surveyor: the exam, experience and entry rules.
- Paramedic: the bachelor's subject levels.
- The FAIS RE5 rule: only a training provider stated it.
- "Nearest route" rows (Cybersecurity, UX, Insurance broker, Soil scientist, Power engineer, Farm manager): the closest
  verified programme, labelled as not specific to the career.

**Reproduced text.** The regulation rows for pilot, AME, auditor (IRBA) and construction manager (SACPCMP) come from
acts.co.za, a third-party reproduction of the regulations. Re-check against the official text before learners see them.

## Flag: NC(V) business programmes, new intake from 2027 (UNVERIFIED, material)

- **What the sources say.** Search results say some colleges take **no new Level 2 students from January 2027** in
  Finance, Economics and Accounting, Management, Marketing and Office Administration.
- **The circular number conflicts.** Sedibeng TVET College's 2027 prospectus cites DHET circular **T0132**; other college
  notices cite **TC 0153**.
- **Not confirmed.** The prospectus PDF could not be read here, and the circular itself was not found. If true, it affects
  the Finance industry's NC(V) route (above) and the TVET market plan (project_tvet_curriculum_facts). Confirm it with DHET
  or a college before relying on it.
- Sources: https://www.mysedcol.co.za/_CollegeCirculars/Sedcol_Prospectus_2027.pdf (unreadable here);
  https://varsitywise.com/posts/umalusi-phasing-out-nated-n1-n3-exams-internalizing-ncv-levels-2-3 (secondary).

## Sources

1. https://www.wits.ac.za/course-finder/undergraduate/ebe/mechanical-engineering/
2. https://www.ecsa.co.za/ecsa-registration/professional-engineer/
3. https://www.education.gov.za/Curriculum/CurriculumStatements/NationalCertificates(Vocational)NQFLevel2/NC(Vocational)AssessmentGuidelinesLevel2.aspx
4. https://www.wits.ac.za/course-finder/undergraduate/ebe/electrical-engineering/
5. https://studies.nwu.ac.za/undergraduate-studies/fields-study-engineering
6. https://www.wits.ac.za/course-finder/undergraduate/ebe/chemical-engineering/
7. https://www.wits.ac.za/course-finder/undergraduate/ebe/industrial-engineering/
8. https://www.ecsa.co.za/ecsa-registration/professional-engineering-technician/
9. https://www.qcto.org.za/for-learners.html
10. https://www.wits.ac.za/course-finder/undergraduate/ebe/civil-engineering/
11. https://ebe.uct.ac.za/apply-ebe-faqs/frequently-asked-questions-geomatics
12. https://sagc.org.za/registration-process/
13. https://ebe.uct.ac.za/apply-ebe-faqs/frequently-asked-questions-architecture
14. https://www.sacapsa.com/registration/categories
15. SACQSP registration route (agent-reported; the URL was not returned)
16. https://www.wits.ac.za/course-finder/undergraduate/ebe/urban-and-regional-planning/
17. https://www.wits.ac.za/course-finder/undergraduate/ebe/mining-engineering/
18. https://www.wits.ac.za/course-finder/undergraduate/science/geological-sciences/
19. https://www.wits.ac.za/course-finder/undergraduate/ebe/metallurgy-and-materials-engineering/
20. https://www.wits.ac.za/course-finder/undergraduate/health/medicine-and-surgery
21. https://medicalschool.mandela.ac.za/Frequently-Asked-Questions/Prospective-Students/What-happens-after-I-receive-my-MBChB-degree
22. https://www.wits.ac.za/course-finder/undergraduate/health/physiotherapy
23. https://allqs.saqa.org.za/showQualification.php?id=121046
24. https://health-sciences.ukzn.ac.za/degrees/bachelor-of-pharmacy/
25. https://www.pharmcouncil.co.za/
26. https://health-sciences.nwu.ac.za/pharmacy/apply-study-pharmacy
27. https://www.wits.ac.za/course-finder/undergraduate/health/nursing/
28. https://health-sciences.nwu.ac.za/nursing/bnursing
29. https://www.cut.ac.za/Programmes/radiography-in-diagnostics
30. https://www.wits.ac.za/therapeuticsciences/occupational-therapy/academic-programmes/undergraduate/admissions/
31. https://allqs.saqa.org.za/showQualification.php?id=91791
32. https://agriculture-science.ukzn.ac.za/qualification/bachelor-of-science-in-agriculture/
33. https://www.sacnasp.org.za/fields-of-practice and https://www.sacnasp.org.za/requirements-for-registration
34. https://agriculture-science.ukzn.ac.za/qualification/bachelor-of-science-in-environmental-science/
35. https://www.ump.ac.za/Study-with-us/Faculties-and-Schools/Faculty-of-Agriculture-and-Natural-Sciences
36. https://ntc.edu.za/primary-agriculture.html
37. https://www.ump.ac.za/Study-with-us/Faculties-and-Schools/Faculty-of-Agriculture-and-Natural-Sciences/School-of-Biology-and-Environmental-Sciences/Diploma-in-Nature-Conservation.aspx
38. https://w2.unisa.ac.za/CW/SITES/CORPORAT/DEFAULT/APPLY_FO/UNDERGRA/QUALIFIC/ALL_QUAL/DIPLOM-4.HTM
39. https://busman.mandela.ac.za/Undergraduate-Studies/BCom-Financial-Planning-(40126)
40. https://www.moonstone.co.za/study-material-for-the-res/ (a training provider; no FSCA page stating RE5/RE1 loaded)
41. https://ewc.edu.za/programmes/business-studies/finance-economics-accounting-l4.html
42. https://www.wits.ac.za/course-finder/undergraduate/clm/accounting/
43. https://www.saica.org.za/become-a-member/how-to-become-a-member/chartered-accountant-casa/how-to-become-a-chartered-accountant-casa
44. https://www.wits.ac.za/course-finder/undergraduate/science/actuarial-science/
45. https://www0.sun.ac.za/programmes/undergraduate-programmes/economic-and-management-sciences/broad-degree-programmes-for-professional-registration/bcomm-actuarial-sciences.html
46. https://www.wits.ac.za/course-finder/undergraduate/clm/economics/
47. https://www.wits.ac.za/course-finder/undergraduate/science/computer-science/
48. https://falsebaycollege.co.za/ict/ncv-information-technology-and-computer-science-level-2-4/
49. https://www.caa.co.za/industry-information/personnel-licensing/licensing/
50. https://www.sanews.gov.za/node/26440
51. https://www.samtra.co.za
52. https://www.wits.ac.za/course-finder/undergraduate/humanities/bed-foundation-phase-teaching/
53. https://www.sace.org.za/pages/registration-requirements
54. https://www.wits.ac.za/course-finder/undergraduate/humanities/bed-senior-phase-teaching
55. https://thekwini.edu.za/campuses
56. https://www.ufs.ac.za/humanities/departments-and-divisions/social-work-home/prospective-students
57. https://www.sacssp.co.za/social-work
58. https://www.sacap.edu.za/blog/psychology/educational-psychologist/ (a private college's career guide: secondary)
59. https://www.ufs.ac.za/natagri/departments-and-divisions/quantity-surveying-and-construction-management-home/unlisted-pages/all/bsc-quantity-surveying-bsc-hons-quantity-surveying-208
60. https://shop.acts.co.za/project-and-construction-management-professions-act-2000/rules_for_reg_4_4__registratio.php (reproduced rules)
61. https://allqs.saqa.org.za/showQualification.php?id=120883
62. https://www.gov.za/node/819951 (title only; the regulations PDF was not read)
63. https://www.uwc.ac.za/study/all-areas-of-study/departments/department-of-occupational-therapy-2/undergraduate
64. https://ot.ukzn.ac.za/undergraduate-programmes/ and https://health-sciences.ukzn.ac.za/degrees/b-occupational-therapy/
65. https://allqs.saqa.org.za/showQualification.php?id=119803
66. https://commerce.nwu.ac.za/es/riskmanagement
67. https://source.acts.co.za/auditing-profession-act-2005/bn93_3__admission_requirements.php (reproduced; may be dated)
68. https://statistics.ukzn.ac.za/data-science/qualification/bachelor-of-science-statistics-computer-science
69. https://vut.ac.za/?p=33848
70. https://vut.ac.za/?p=33757
71. https://source.acts.co.za/civil-aviation-act-2009/nr425_61_05_1_requirement.php (reproduced Part 61)
72. https://source.acts.co.za/civil-aviation-act-2009/nr425_66_02_1_requirement.php (reproduced Part 66)
73. https://allqs.saqa.org.za/showQualification.php?id=110050
74. https://allqs.saqa.org.za/showQualification.php?id=94831
