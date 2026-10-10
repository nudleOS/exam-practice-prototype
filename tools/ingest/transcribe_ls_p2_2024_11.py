"""Life Sciences P2 Nov 2024, the whole paper (Questions 1 to 3), hand-transcribed into the catalogue format (as if Claude had produced it), then run through
`ingest.py --from-json` like any ingested paper. Stems, options, marks and answers are the paper's and the memo's own; the clues and
the figure captions (alt text) are ours. No API call: the transcription is the source, kept in git (out/ is not).
Polished one subject at a time, every paper of it (Murci, 2026-10-09): Life Sciences first, 2025 and 2024, P1 and P2.
Learner rollout (Murci, 2026-10-10): every written answer plays as statements (STATEMENTS) or a sort (SORTS, 3.4.3); the parts whose
cards show an earlier part's answer open after it (GATES).

  python tools/ingest/transcribe_ls_p2_2024_11.py
  python tools/ingest/ingest.py "<...>/Life Sciences P2 Nov 2024 Eng.pdf" "<...>/Life Sciences P2 Nov 2024 MG Eng.pdf" --id ls-p2-2024-11 --from-json
  then open Exam Practice.dc.html?ingested=ls-p2-2024-11&paper=ls-p2-2024-11&play=0

Figure boxes are measured in PDF points on the A4 page (595 x 842) and stored as fractions."""
import json
from pathlib import Path

W, H = 595.0, 842.0
box = lambda x0, y0, x1, y1: [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4), round(y1 / H, 4)]
fig = lambda page, b, caption: {"page": page, "bbox": box(*b), "caption": caption}
mcq = lambda n, q, opts, a, clues, **kw: {"t": "mcq", "n": n, "marks": 2, "q": q, "clues": clues, "opts": opts, "a": a, **kw}
mcq1 = lambda n, q, opts, a, clues: {"t": "mcq", "n": n, "marks": 1, "q": q, "clues": clues, "opts": opts, "a": a}
term = lambda n, q, a, clues, marks=1, **kw: {"t": "term", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, **kw}
lst = lambda n, q, count, marks, pool, clues: {"t": "list", "n": n, "marks": marks, "q": q, "clues": clues, "count": count, "pool": pool}
rub = lambda n, q, marks, bullets, clues, **kw: {"t": "rubric", "n": n, "marks": marks, "q": q, "clues": clues, "bullets": bullets, **kw}
num = lambda n, q, a, tol, unit, clues, marks=1: {"t": "num", "n": n, "marks": marks, "q": q, "clues": clues, "a": a, "tol": tol, "unit": unit}
AB = ["A only", "B only", "Both A and B", "None"]
# Column I / Column II (1.3): the description is the stem, COLUMN II's two items are `ab` (the Venn layout draws them as its two circles)
abq = lambda n, q, a_item, b_item, a, clues: mcq(n, q, AB, a, clues, ab={"a": a_item, "b": b_item})
# the butterfly's alleles (1.5.3) and muscular dystrophy's (2.4), built from a tray: typed, the case-folding matcher took RREE for RRee
WING = ["R", "r", "E", "e"]
MD = ["Xᴰ", "Xᵈ", "Y"]

# ---- Section A: Question 1, from the question paper pages 3-7 and the memo page 4 ----
q11 = [
    mcq("1.1.1", "Which ONE of the following organelles is the site of protein synthesis?", ["Ribosomes", "Chloroplasts", "Mitochondria", "Centrosomes"], 0,
        ["The mRNA attaches to this organelle.", "Which organelle reads the codons and joins the amino acids?"]),
    # options printed as a TABLE: optTable carries it; opts read each row as a line (the medal card, the memo)
    mcq("1.1.2", "In humans, the gonosomes determine the gender. Which combination below shows the CORRECT gonosomes for males and females?",
        ["Male: XY · female: YY", "Male: YY · female: XY", "Male: XY · female: XX", "Male: XX · female: XY"], 2,
        ["Every person gets an X chromosome from the mother.", "A Y chromosome makes a male: can anyone have two of them?"],
        optTable={"head": ["MALE GONOSOMES", "FEMALE GONOSOMES"], "rows": [["XY", "YY"], ["YY", "XY"], ["XY", "XX"], ["XX", "XY"]]}),
    mcq("1.1.3", "An organism has the genotype TT. The CORRECT term which describes this organism's genotype is …",
        ["heterozygous dominant.", "heterozygous recessive.", "homozygous dominant.", "homozygous recessive."], 2,
        ["Are the two alleles the same or different?", "A capital letter stands for which kind of allele?"]),
    mcq("1.1.4", "Down syndrome is a genetic disorder where an individual has an extra copy of chromosome 21. Which ONE of the following may lead to Down syndrome?",
        ["Failure of chromosomes to replicate during mitosis", "Failure of chromosome pairs to separate during meiosis",
         "Failure of chromosomes to form pairs during fertilisation", "Failure of chromosome pairs to cross over during meiosis"], 1,
        ["The extra chromosome came in a gamete.", "Which division makes gametes, and what must the pairs do in it?"]),
    mcq("1.1.5", "A gradual change in the characteristics of a species over time is known as …",
        ["punctuated equilibrium.", "genetic engineering.", "speciation.", "biological evolution."], 3,
        ["Is the change in the stem sudden or slow? Does the stem say that a new species forms?", "Which term is the change itself, slow and over time?"]),
    mcq("1.1.6", "Which ONE of the following is a reproductive isolation mechanism?",
        ["Adaptation to the same pollinator", "Species-specific courtship behaviour", "Production of fertile offspring", "Breeding at the same time of the year"], 1,
        ["An isolation mechanism STOPS two species from interbreeding.", "Three of the options would help them interbreed."]),
    mcq("1.1.7", "Analysis of mitochondrial DNA is an example of this line of evidence:",
        ["Fossil evidence", "Modification by descent", "Biogeography", "Genetic evidence"], 3,
        ["mtDNA is studied in a laboratory, not dug up or mapped.", "What kind of molecule is DNA?"]),
    mcq("1.1.8", "Which option in the table below shows the CORRECT comparison between mitosis and meiosis?",
        ["Mitosis: produces four daughter cells · meiosis: produces two daughter cells",
         "Mitosis: produces genetically different cells · meiosis: produces genetically identical cells",
         "Mitosis: the chromosome number remains the same · meiosis: the chromosome number is halved",
         "Mitosis: two divisions occur · meiosis: four divisions occur"], 2,
        ["Mitosis makes body cells; meiosis makes gametes.", "What must happen to the chromosome number so that fertilisation restores it?"],
        optTable={"head": ["MITOSIS", "MEIOSIS"], "rows": [["Produces four daughter cells", "Produces two daughter cells"],
                                                       ["Produces genetically different cells", "Produces genetically identical cells"],
                                                       ["The chromosome number remains the same", "The chromosome number is halved"],
                                                       ["Two divisions occur", "Four divisions occur"]]}),
    mcq("1.1.9", "Which ONE of the following scientists discovered the fossil Taung Child?", ["Lee Berger", "Ron Clarke", "Raymond Dart", "Robert Broom"], 2,
        ["The skull was found in 1924 in a lime quarry.", "The scientist who described it in 1925 named a new genus for it, Australopithecus."]),
    mcq("1.1.10", "Which ONE of the following is produced at the end of translation?", ["A DNA molecule", "A messenger RNA molecule", "A protein", "An amino acid"], 2,
        ["Translation is the second stage of protein synthesis.", "Amino acids go IN at the ribosome: what comes OUT?"]),
]
q12 = [
    term("1.2.1", "A nucleic acid that carries hereditary information", ["DNA", "deoxyribonucleic acid"],
         ["It is found in the nucleus, the mitochondria and the chloroplasts.", "Genes are made of it."]),
    term("1.2.2", "The chromosome condition of a cell that has a single set of chromosomes", ["haploid"],
         ["Gametes are in this condition.", "It is written as n, the opposite of 2n."]),
    term("1.2.3", "The structure that holds the two chromatids of a chromosome together", ["centromere"],
         ["Spindle fibres attach to it.", "It splits in anaphase II."]),
    term("1.2.4", "The type of RNA that carries specific amino acids to the site of protein synthesis", ["tRNA", "transfer RNA", "t-RNA"],
         ["It carries an anticodon.", "Its name says what it does: it moves amino acids across."]),
    term("1.2.5", "The analysis of DNA samples to identify individuals or relationships between individuals", ["DNA profiling"],
         ["It is used in paternity tests and at crime scenes.", "The bands look like a barcode."]),
    term("1.2.6", "A representation of the number and structure of all the chromosomes that occur in the nucleus of a somatic cell", ["karyotype", "karyogram"],
         ["The chromosomes are photographed and arranged in pairs.", "It shows Down syndrome as three copies of chromosome 21."]),
    term("1.2.7", "A group of similar organisms that are able to interbreed to produce fertile offspring", ["species"],
         ["A horse and a donkey are two of these: a mule is infertile.", "It is the second word of a scientific name."]),
    term("1.2.8", "The phase of meiosis where paired chromosomes are arranged at the equator", ["metaphase I", "metaphase 1"],
         ["Chromosomes line up at the equator in this phase.", "They are still PAIRED: which division of meiosis is it?"],
         reject=["metaphase II", "metaphase 2", "metaphase"]),
    term("1.2.9", "The biotechnological process that produces genetically identical organisms", ["cloning"],
         ["Dolly the sheep was made this way.", "The offspring is a copy of one parent."]),
]
q13 = [
    abq("1.3.1", "A source of variation in populations", "Random fertilisation", "Random mating", 2,
        ["Variation comes from new combinations of alleles.", "Does each item give new combinations: which sperm meets which egg, and which parents meet?"]),
    abq("1.3.2", "Discovery of the structure of the DNA molecule", "Franklin and Wilkins", "Lamarck and Darwin", 0,
        ["The structure was found in the 1950s, with X-ray pictures.", "Two of these scientists lived long before DNA was known."]),
    abq("1.3.3", "Occurs during meiosis", "Karyokinesis", "Cytokinesis", 2,
        ["Karyokinesis is the division of the nucleus, cytokinesis of the cytoplasm.", "Meiosis makes new cells: which of the two must happen?"]),
]
q14 = [
    term("1.4.1(a)", "Identify the process shown in the diagram", ["DNA replication", "replication"],
         ["The two strands have come apart, and each strand is pairing with new units.", "The process makes a copy of the molecule."]),
    term("1.4.1(b)", "Identify the chemical bond labelled 1", ["hydrogen bond", "hydrogen bonds", "hydrogen"],
         ["It joins a base to the base it pairs with.", "It is a weak bond, broken when the strands unzip."]),
    term("1.4.2(a)", "Give the collective name for the parts labelled 2, 3 and 4", ["nucleotide", "nucleotides"],
         ["2 is a phosphate, 3 a sugar and 4 a base.", "It is the building unit of a DNA strand."]),
    term("1.4.2(b)", "Give the full name of the nitrogenous base labelled 5", ["thymine"],
         ["Find the base on the other strand at the same level as 5.", "Write the name, not the letter: A pairs with which base in DNA?"]),
    term("1.4.3", "During which phase of the cell cycle does this process take place?", ["interphase"],
         ["It happens before the cell divides.", "It is the phase between divisions."]),
    term("1.4.4", "Where in the cell does this process occur?", ["nucleus"], ["Where is most of a cell's DNA?", "It is the control centre of the cell."]),
]
q15 = [
    term("1.5.1", "Name the type of cross represented above.", ["dihybrid cross", "dihybrid"],
         ["How many genes are followed in this cross?", "A cross of one gene is monohybrid."], reject=["monohybrid cross", "monohybrid"]),
    lst("1.5.2", "Give the dominant characteristic of EACH gene.", 2, 2, [["red (spots)"], ["black (eyes)"]],
        ["The dominant allele is written with a capital letter.", "Give the characteristic in words, not the letter, for the wing spots AND for the eyes."]),
    # four alleles a genotype (catalogue `genotype` per 4, 2026-10-09): the memo's RRee and Rree, 2 marks each
    {"t": "genotype", "n": "1.5.3(a)", "marks": 4, "q": "Give ALL the possible genotypes at X", "alleles": WING, "count": 2, "per": 4,
     "pool": [["R", "R", "e", "e"], ["R", "r", "e", "e"]],
     "clues": ["Brown eyes is recessive: what must the eye-colour alleles be?", "Red spots is dominant: it can be shown by two alleles or by one."]},
    term("1.5.3(b)", "Give the phenotype at Y",
         ["red spots, black eyes", "red spots and black eyes", "red spots with black eyes", "black eyes, red spots", "black eyes and red spots",
          "red wing spots, black eyes", "red wing spots and black eyes"],
         ["RrEe has a dominant allele for each gene.", "Give the wing spots AND the eyes."]),
    # a gamete carries one allele of each gene: built from the same tray (typed, "RE" folded to "re")
    {"t": "genotype", "n": "1.5.3(c)", "marks": 1, "q": "Give the genotype of the gametes produced by a butterfly with grey spots and brown eyes",
     "alleles": WING, "count": 1, "pool": [["r", "e"]],
     "clues": ["Grey spots and brown eyes are both recessive: what is this butterfly's genotype?", "A gamete gets ONE allele of each gene."]},
]
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Biological terms", "marks": 9,
     "lead": "Give the correct biological term for EACH of the following descriptions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "A, B, both or none", "marks": 6,
     "lead": "Indicate whether each of the descriptions in COLUMN I apply to A ONLY, B ONLY, BOTH A AND B or NONE of the items in COLUMN II.", "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "A DNA molecule", "marks": 6,
     "lead": "The diagram below represents a DNA molecule undergoing an important biological process.", "items": q14,
     "figure": fig(6, (101, 129, 518, 479), "A DNA molecule whose two strands have come apart into a V shape. Each strand is a chain of units: a circle "
                   "joined to a pentagon, the pentagon carrying a small shape (a base). Lower down, the bases are unpaired. On the left-hand strand, "
                   "from top to bottom: the circle labelled 2 joined to the pentagon labelled 3, which carries the pointed base labelled 4; then a "
                   "pointed base A; then a rounded base G. On the right-hand strand, from top to bottom: a notched base, the notched base labelled 5 "
                   "(level with A), and a hollow rounded base. Higher up, each strand's bases are paired with the bases of a second strand of units "
                   "alongside it, each pair joined by short lines; 1 points to the short lines between one pair on the left.")},
    {"id": "1.5", "title": "Question 1.5", "kind": "Butterfly cross", "marks": 9,
     "lead": "In a certain species of butterfly, one gene controls wing-spot colour and another controls eye colour. The wing-spot colour can be "
             "red spots (R) or grey spots (r), while eye colour can be black (E) or brown (e). Butterflies that are heterozygous for both genes were "
             "crossed. For QUESTION 1.5.3, the table below shows the phenotypes and all the possible genotypes of the offspring.", "items": q15,
     "table": {"head": ["PHENOTYPES", "ALL POSSIBLE GENOTYPES"],
               "rows": [["Red spots, brown eyes", "(X)"], ["(Y)", "RrEe"], ["Grey spots, brown eyes", "rree"]]}},
]

# ---- Section B: Questions 2 and 3, from the question paper pages 8-14 and the memo pages 5-11 ----
# (a list scores an answer that holds the LEAD word of an accepted answer: each accepted answer leads with a word only that point uses)
q21 = [
    term("2.1.1", "Identify molecule Y.", ["mRNA", "messenger RNA", "m-RNA"],
         ["It is a single strand built along the template strand.", "It carries the code out of the nucleus to the ribosome."]),
    rub("2.1.2", "Describe the process that resulted in the formation of molecule Y.", 6,
        ["The DNA double helix unwinds and", "(the double strand) unzips / (weak) hydrogen bonds break", "to form two separate strands",
         "One strand is used as a template", "to form mRNA", "using free RNA nucleotides from the nucleoplasm",
         "The mRNA is complementary to the DNA / A complements U, G complements C"],
        ["Start with what happens to the DNA molecule.", "Then say how molecule Y is built along one strand, and how its bases pair."]),
    rub("2.1.3", "Give ONE structural difference between molecule X and molecule Y.", 2,
        ["Molecule X (DNA) is double stranded (double helix)", "Molecule Y (RNA) is single stranded",
         "OR — Molecule X (DNA) has hydrogen bonds", "Molecule Y (RNA) has no hydrogen bonds",
         "OR — Molecule X (DNA) contains deoxyribose sugar", "Molecule Y (RNA) contains ribose sugar",
         "OR — Molecule X (DNA) has thymine / T as a nitrogenous base", "Molecule Y (RNA) has uracil / U as a nitrogenous base",
         "OR — Molecule X (DNA) is longer", "Molecule Y (RNA) is shorter"],
        ["Compare the number of strands, the sugar or the bases.", "Say it for BOTH molecules: X is …, while Y is …"]),
    term("2.1.4", "Give the sequence of bases at triplet Z on strand 2.", ["TAC"],
         ["Strand 2 is not the template: it has the same bases as molecule Y, except one.", "DNA has T where RNA has U."]),
    lst("2.1.5", "Identify the first and last amino acids coded for by this section of molecule Y.", 2, 2, [["arginine"], ["proline"]],
        ["Read molecule Y from left to right, three bases at a time.", "Find its first and last codons in the table."]),
]
q22 = [
    term("2.2.1", "Identify the phase of meiosis shown.", ["anaphase II", "anaphase 2"],
         ["The chromatids are being pulled to the poles.", "It is a phase of the second division."], reject=["anaphase I", "anaphase 1", "anaphase"]),
    rub("2.2.2", "State ONE difference between the phase shown in the diagram above and the same phase in meiosis I.", 2,
        ["Chromosome pairs separate during anaphase I / chromosomes move to the poles",
         "A chromosome separates during anaphase II / chromatids move to the poles",
         "OR — Centromeres do not split during anaphase I", "Centromeres split during anaphase II"],
        ["What is pulled apart in each phase: pairs of chromosomes, or the two halves of one chromosome?",
         "Think of the centromere in each phase. Say it for both phases."]),
    term("2.2.3(a)", "Identify structure A", ["centriole", "centrosome", "centrioles"],
         ["It sits at the pole of the cell.", "The spindle fibres run from it; plant cells do not have it."]),
    term("2.2.3(b)", "Identify structure B", ["spindle fibre", "spindle fibres", "spindle fiber", "spindle fibers"],
         ["The dashed lines run from pole to pole.", "The chromatids hang on them."]),
    rub("2.2.4", "Describe the role of structure B during cell division.", 2,
        ["Attaches to the centromere", "to pull chromatids / chromosomes towards the (opposite) poles",
         "OR — It contracts / shortens", "to pull chromatids / chromosomes towards the (opposite) poles"],
        ["Where on a chromosome does it attach?", "What does it do to move the chromatids?"]),
    # a drawing on paper: self-marked against the memo's grid (P N S L), not marked online
    {"t": "draw", "n": "2.2.5", "marks": 5,
     "q": "Draw a labelled diagram representing the cell above as it would have appeared in metaphase II. NOTE: The diagram should show the correct "
          "shading and include labels (exclude labels for A and B).",
     "clues": ["Before anaphase II, each pair of chromatids was still one chromosome: put the halves back together.",
               "Where do the chromosomes lie in metaphase? Keep each chromatid's shading as it is in the diagram."],
     "criteria": [{"text": "Position: chromosomes in a single row at the equator (P)", "marks": 1},
                  {"text": "Number: 2 unpaired chromosomes drawn (N)", "marks": 1},
                  {"text": "Shading: 1 shaded chromosome with an unshaded tip and 1 unshaded chromosome with a shaded tip (S)", "marks": 1},
                  {"text": "Any TWO correct labels, except centriole and spindle fibre (L)", "marks": 2}],
     "memo": "Labels the memo accepts (any two): cell membrane, cytoplasm, chromosome, chromatid, centromere."},
]
GROUPS = ["A", "B", "AB", "O"]
q23 = [
    mcq1("2.3.1", "According to the data, which is the most common blood group among the donors?", GROUPS, 3,
         ["Find the largest percentage in the table.", "Read across to its blood group."]),
    term("2.3.2", "Name the type of dominance shown by the inheritance of blood group A.", ["complete dominance", "complete"],
         ["Blood group A can have the genotype Iᴬi.", "Is the i allele shown at all when Iᴬ is there?"],
         reject=["incomplete dominance", "incomplete", "co-dominance", "codominance"]),
    rub("2.3.3", "Explain how it is possible for a man with blood group A and a woman with blood group AB to have a child with blood group B.", 5,
        ["The man is heterozygous / is Iᴬi for blood group A", "The woman has an allele for blood group B / is IᴬIᴮ",
         "The child inherits the Iᴮ allele from the mother", "and the i allele from the father",
         "Therefore, the child will be heterozygous for blood group B / the genotype will be Iᴮi"],
        ["The child cannot have Iᴬ: so which allele must the father have besides Iᴬ?", "Say which allele the child gets from each parent, and the child's genotype."]),
    {"t": "draw", "n": "2.3.4", "marks": 6, "q": "Plot a bar graph to represent the data in the table.",
     "clues": ["Each blood group is its own bar: a bar graph's bars stand apart.", "The blood groups go along the bottom, the percentage up the side."],
     "criteria": [{"text": "Type of graph: a bar graph is drawn", "marks": 1}, {"text": "Caption includes both variables, SA and 2018", "marks": 1},
                  {"text": "X-axis and Y-axis correctly labelled, with the unit", "marks": 1},
                  {"text": "Equal space and width of bars on the X-axis, and a correct scale for the Y-axis", "marks": 1},
                  {"text": "Plotting: 1–3 co-ordinates correct (1), all 4 correct (2)", "marks": 2}],
     # built step by step, one memo criterion a step (T C L S P), as LS P1 Nov 2025 2.3.4
     "build": {"kind": "hist", "want": "bar", "groups": ["O", "A", "B", "AB"], "answers": [48, 38, 10, 4], "tol": 0.5, "top": 50,
               "steps": [2, 5, 10, 25], "okSteps": [2, 5, 10], "snap": 1, "unit": "blood group",
               "x": ["Blood group", "Percentage of donors (%)", "Number of donors"],
               "y": ["Percentage of donors (%)", "Blood group", "Number of donors"],
               # the memo's caption: both variables, SA and 2018 ("sa " ends a word: " sa" alone took "same", "sample")
               "capWords": [["blood", "group"], ["donor", "percent"], ["south", "sa "], ["2018"]],
               "typeQ": "Which graph shows separate blood groups against a percentage?",
               "typeHint": "A histogram's bars touch for groups that run on; a bar graph's stand apart."}},
]
q24 = [
    num("2.4.1", "How many offspring do individuals 1 and 2 have?", 3, 0, "", ["Find the line that joins 1 and 2.", "Follow it down and count their children."]),
    term("2.4.2(a)", "Give the phenotype of individual 1",
         ["male without muscular dystrophy", "a male without muscular dystrophy", "male with no muscular dystrophy",
          "male who does not have muscular dystrophy", "male that does not have muscular dystrophy", "normal male", "unaffected male"],
         ["Use the key.", "Is 1 a square or a circle, open or shaded?"]),
    {"t": "genotype", "n": "2.4.2(b)", "marks": 1, "q": "Give the genotype of individual 2", "alleles": MD, "count": 1, "pool": [["Xᴰ", "Xᵈ"]],
     "clues": ["2 does not have muscular dystrophy, but one of her sons does.", "A son gets his X chromosome from his mother: what must she carry?"]},
    rub("2.4.3", "Explain why more males than females are likely to have muscular dystrophy.", 4,
        ["Males only have one X chromosome / XY and", "need only one recessive allele to have muscular dystrophy",
         "The Xᵈ allele on a male cannot be masked by a dominant allele", "Females have two X chromosomes and",
         "need two recessive alleles to have muscular dystrophy / XᵈXᵈ",
         "In females, a dominant allele on one X chromosome would mask the effect of the recessive allele / Xᴰ masks Xᵈ"],
        ["Count the X chromosomes in a male and in a female.", "How many recessive alleles does each need to show the condition?"]),
    # a SEX-LINKED cross BUILT on the Punnett square (draw.build cross): parents 5 and 6 are the second generation, so the memo marks
    # "P2 and F2" (`gens`). The memo's compulsory mark is the 25% chance; the builder takes the offspring's proportions, which give it
    {"t": "draw", "n": "2.4.4", "marks": 6,
     "build": {"kind": "cross", "alleles": MD, "gens": ["P2", "F2"],
               "phenos": ["female without muscular dystrophy", "male without muscular dystrophy", "male with muscular dystrophy",
                          "female with muscular dystrophy"],
               "parents": [{"pheno": "female without muscular dystrophy", "geno": ["Xᴰ", "Xᵈ"]},
                           {"pheno": "male without muscular dystrophy", "geno": ["Xᴰ", "Y"]}],
               "offspring": [{"geno": ["Xᴰ", "Xᴰ"], "pheno": "female without muscular dystrophy"},
                             {"geno": ["Xᴰ", "Xᵈ"], "pheno": "female without muscular dystrophy"},
                             {"geno": ["Xᴰ", "Y"], "pheno": "male without muscular dystrophy"},
                             {"geno": ["Xᵈ", "Y"], "pheno": "male with muscular dystrophy"}]},
     "q": "Parents 5 and 6 plan to have another child. Use a genetic cross to show the percentage chance of having a child with muscular dystrophy.",
     "clues": ["5 does not have muscular dystrophy, but her sons do: what is her genotype? 6 is a male without it.",
               "Lay it out: P2, meiosis, gametes, fertilisation, F2, then the chance."],
     "criteria": [{"text": "P2 phenotypes: female without muscular dystrophy x male without muscular dystrophy", "marks": 1},
                  {"text": "P2 genotypes: XᴰXᵈ x XᴰY", "marks": 1},
                  {"text": "Gametes: Xᴰ, Xᵈ x Xᴰ, Y (in a Punnett square: the correct gametes)", "marks": 1},
                  {"text": "F2 genotypes: XᴰXᴰ, XᴰY, XᴰXᵈ, XᵈY (in a Punnett square: the correct genotypes)", "marks": 1},
                  {"text": "F2 phenotypes: (50%) females without muscular dystrophy, (25%) males without, (25%) males with muscular dystrophy", "marks": 1},
                  {"text": "25% chance of a child with muscular dystrophy, compulsory", "marks": 1},
                  {"text": "P2 and F2 shown", "marks": 1},
                  {"text": "Meiosis and fertilisation shown", "marks": 1}],
     "memo": "*1 compulsory mark (25% chance of a child with muscular dystrophy) + any 5. P2: female without muscular dystrophy (XᴰXᵈ) x male "
             "without muscular dystrophy (XᴰY); meiosis; gametes Xᴰ, Xᵈ x Xᴰ, Y; fertilisation; F2: XᴰXᴰ, XᴰY, XᴰXᵈ, XᵈY; (50%) females without, "
             "(25%) males without, (25%) males with muscular dystrophy; 25% chance. A Punnett square may replace the gamete and fertilisation "
             "lines: 1 mark for the correct gametes, 1 mark for the correct genotypes."},
]
q31 = [
    rub("3.1.1", "Describe how the Bt maize is genetically modified to be insect resistant.", 3,
        ["The Bt producing gene is cut from the bacterial DNA and", "inserted into maize DNA", "This recombinant DNA",
         "causes the maize plant to produce the Bt toxin"],
        ["Which part of the bacterium's DNA is wanted?", "Where is it put, and what does the maize then make?"]),
    rub("3.1.2", "Explain TWO reasons why farmers might want to grow Bt maize.", 4,
        ["Fewer crops are damaged", "which leads to increased yield / more food for people / increased food security / healthier crops / more profit",
         "Reduced need for pesticides", "so farmers save money / fewer toxins reach consumers / the environment"],
        ["What do the insects stop doing to the maize?", "What would the farmer no longer need to spray? Give the result of each reason."]),
]
LETTERS = ["P", "Q", "R", "S", "T", "U", "V"]
q32 = [
    mcq1("3.2.1", "Give the LETTER representing the common ancestor for ALL the species shown in the phylogenetic tree.", LETTERS, 6,
         ["A common ancestor is where branches meet.", "Follow every branch down: where do they ALL meet?"]),
    term("3.2.2", "Identify the species that is most closely related to Old-world monkeys.", ["gibbons", "gibbon", "U"],
         ["Follow the Old-world monkeys' branch down to where it first meets another branch.", "Which group's branch runs straight on to that point?"]),
    rub("3.2.3", "Give a reason for your answer to QUESTION 3.2.2.", 1,
        ["They share the most recent common ancestor U", "OR — Old-world monkeys are directly descended from U"],
        ["Closely related species meet at a branch point soon.", "Find the branch point that the two groups share."]),
    lst("3.2.4", "Identify THREE species that share the common ancestor R.", 3, 3,
        [["humans", "human"], ["chimpanzees", "chimp"], ["gorillas", "gorilla"], ["Q"]],
        ["Start at R and follow every branch above it up to the top.", "Which groups can you reach from R?"]),
    lst("3.2.5", "State THREE characteristics of the upper limbs that humans share with group P.", 3, 3,
        [["freely (rotating arms)", "rotating", "rotate"], ["long (upper arms)"], ["elbow (rotation around the elbow joints)"],
         ["wrist (rotation around the wrist)"], ["bare (fingertips)", "fingertips"], ["nails (instead of claws)", "nail"],
         ["fingerprints", "prints"], ["opposable (thumb)", "precision (grip)", "thumb"],
         ["pentadactyl (five digits per limb)", "digits"]],
        ["Group P are the great apes: think of the arm, the hand and the fingers.", "How do the arms move, and what is on the fingertips?"]),
]
q33 = [
    lst("3.3.1(a)", "Identify the independent variable", 1, 1, [["type (of milk)", "kind (of milk)"]],
        ["What did the researchers change between the two groups?", "It is the factor they set up on purpose before anything was measured."]),
    lst("3.3.1(b)", "Identify the dependent variable", 1, 1, [["height (of the children)"]],
        ["What did the researchers measure at the end?", "It was measured in cm."]),
    term("3.3.2", "Name the type of variation displayed by the height of a person.", ["continuous variation", "continuous"],
         ["Can height take any value in a range, or only a few set values?", "The values form a smooth range with no clear groups."],
         reject=["discontinuous variation", "discontinuous"]),
    lst("3.3.3", "State TWO planning steps that the researchers had to consider at the beginning of this investigation.", 2, 2,
        [["diet (ensure the same additional diet)"], ["activities (ensure similar daily activities)", "activity"],
         ["living (conditions: ensure they are similar)", "conditions"], ["date (time or venue for measuring)", "time", "venue"],
         ["sample (size)", "size"], ["consent (ask for parental consent)", "permission"], ["train (the research assistants)", "assistants"],
         ["recruit (parents willing to participate)", "willing"], ["target (group)"], ["recording (sheet)", "record"],
         ["source (of milk)", "supplier"], ["apparatus (or equipment, or method of measuring)", "equipment", "method"],
         ["duration (of the investigation)", "period"], ["type (of milk)", "kind"], ["amount (of milk)", "quantity", "volume", "litre"]],
        ["Think of what had to be decided before the first day.", "Who takes part, what they get, and how and when you measure?"]),
    lst("3.3.4", "State THREE ways in which the validity of this investigation was ensured.", 3, 3,
        [["healthy (only healthy children chosen)"], ["age (the same age)"], ["race (the same race)"], ["gender (the same gender)", "sex"],
         ["quantity (of milk: the same)", "amount", "litre", "volume"], ["diet (the same additional diet)"], ["supplier (of milk: the same)"],
         ["number (of children in each group: the same)", "equal"], ["duration (the same)", "years"],
         ["activities (similar daily activities)", "activity"], ["living (conditions: similar)", "conditions", "environment"]],
        ["Validity: only the type of milk may differ between the groups.", "Read the method: what was kept the same or similar?"]),
    lst("3.3.5", "State ONE factor that could have negatively affected the validity of this investigation.", 1, 1,
        [["genetic (or hormonal influence not considered)", "hormon", "genes", "inherit"],
         ["difficult (to keep the same conditions over 7 years)", "maintain"], ["baseline (height not measured)", "starting", "initial"]],
        ["What else decides how tall a child grows?", "Could everything stay the same for 7 years? Was the height at age 3 known?"]),
    lst("3.3.6", "How did the researchers ensure the reliability of the results?", 1, 1,
        [["large (sample: 4 146 children in two equal groups)", "4146", "2073", "4 146", "2 073", "sample"],
         ["7 (years)", "seven", "years", "long"]],
        ["Reliability: would you get the same results again?", "Think of how many children took part, and for how long."]),
    rub("3.3.7", "State the conclusion for this investigation.", 2,
        ["Cow milk consumption leads to better growth / increased height compared to soy milk",
         "OR — Soy milk consumption by children leads to decreased height / below average height",
         "OR — Cow milk consumption by children leads to increased height / above average height"],
        ["A conclusion answers the aim: the influence of the type of milk on height.", "Compare each group's average with the expected height."], each=2),
]
q34 = [
    rub("3.4.1", "Describe how the fossils of Homo erectus are used to support the 'Out-of-Africa' hypothesis.", 3,
        ["The oldest fossils of Homo erectus were found in Africa", "while the younger fossils were found in other parts of the world / Asia",
         "indicating that Homo erectus migrated out of Africa"],
        ["Where are the oldest Homo erectus fossils, and where the younger ones?", "What does that order tell us about where they went?"]),
    rub("3.4.2", "Describe how all OTHER fossil evidence is used to support the 'Out-of-Africa' hypothesis.", 4,
        ["Ardipithecus fossils were found in Africa only", "Australopithecus fossils were found in Africa only",
         "Fossils of Homo habilis were found in Africa only", "The oldest fossils of Homo sapiens were found in Africa",
         "The younger fossils of Homo sapiens were found in other parts of the world"],
        ["Name the other hominid genera and species.", "Say where each one's fossils have been found."]),
    # a TABLE the memo marks (1) for the table + (2 x 2) for two differences, each with both sides: played as a SORT into the two
    # species' columns (SORTS below), the source points kept here
    rub("3.4.3", "Use the information in the passage regarding Homo erectus and tabulate TWO differences between the features of Homo erectus and Homo sapiens.", 5,
        ["Table with the two species as column headings", "Homo erectus: a smaller brain", "Homo sapiens: a larger brain / bigger brain",
         "Homo erectus: a prominent brow ridge", "Homo sapiens: a reduced brow ridge"],
        ["Read the passage for two features of Homo erectus.", "For each feature, ask how it compares in humans today."],
        table=["Homo erectus", "Homo sapiens"]),
    rub("3.4.4", "What observation of the skull of Homo erectus would have led scientists to conclude that Homo erectus was bipedal?", 1,
        ["The foramen magnum was in a (more) forward position"],
        ["Look for the opening where the spinal cord leaves the skull.", "Where is it when the head balances on an upright spine?"]),
]
q35 = [
    rub("3.5.1", "What is a mutation?", 1, ["Changes in the genetic composition / genetic material of organisms"],
        ["Think of what high radiation does to the DNA in a cell.", "A mutation is a source of new alleles: what has changed?"]),
    lst("3.5.2", "What effect does exposure to high radiation have on animals?", 1, 1,
        [["cancer"], ["death", "die", "dies", "kill"], ["mutations", "mutate"]],
        ["Read the passage.", "What happened to the animals exposed to the radiation?"]),
    rub("3.5.3", "Use Darwin's theory of natural selection to explain the development of immunity to cancer in these wolves.", 7,
        ["There was variation amongst (the population of) the wolves", "Some had the mutation which made them immune to cancer and some did not",
         "When exposed to radiation", "the wolves without the mutation / immunity died", "Those with the mutation / immunity survived",
         "and reproduced", "passing the allele for the mutation / immunity to their offspring",
         "The next generation had a higher proportion of wolves with the mutation / immunity to cancer"],
        ["Start with variation in the population.", "Who survives the radiation, who breeds, and what do the offspring inherit?"]),
]
missions_b = [
    {"id": "2.1", "title": "Question 2.1", "kind": "Protein synthesis", "marks": 12,
     "lead": "The diagram below represents a certain stage of protein synthesis. (The sequence of bases is read from left to right.) The table "
             "below shows some amino acids coded for by codons on molecule Y.", "items": q21,
     "figure": fig(8, (102, 187, 518, 362), "A DNA double helix, Molecule X, whose two strands are opened in the middle into a long bubble. The upper "
                   "strand of the bubble is Strand 1 (template), the lower is Strand 2; short ticks along each stand for bases, without letters. "
                   "Inside the bubble, along Strand 1, lies a single strand, Molecule Y, with the bases A G A U A C, a gap, then C C A, read from "
                   "left to right. Z is a bracket under three ticks of Strand 2, below U A C."),
     "table": {"head": ["CODON", "AMINO ACID"], "rows": [["AGA", "Arginine"], ["UCU", "Serine"], ["CCA", "Proline"], ["UAC", "Tyrosine"], ["GGU", "Glycine"]]}},
    {"id": "2.2", "title": "Question 2.2", "kind": "Meiosis II", "marks": 12, "lead": "The diagram below represents a phase of meiosis II.", "items": q22,
     "figure": fig(9, (193, 118, 437, 346), "A round cell. Dashed lines run from a small dot at the top to a small dot at the bottom, bowing out left "
                   "and right like a diamond. Four V-shaped single chromatids lie on the dashed lines, two near each dot, their bends towards that "
                   "dot. Near the top: on the left a black chromatid with a white tip, on the right a white chromatid with a black tip. Near the "
                   "bottom: on the left an all-black chromatid, on the right an all-white one. A labels the dot at the top; B labels the dashed line "
                   "near the bottom right.")},
    {"id": "2.3", "title": "Question 2.3", "kind": "Blood donors", "marks": 13,
     "lead": "The table below shows the percentage of blood donors for each of the blood groups in South Africa for 2018.", "items": q23,
     "table": {"head": ["BLOOD GROUP", "% DONORS"], "rows": [["O", "48"], ["A", "38"], ["B", "10"], ["AB", "4"]]}},
    {"id": "2.4", "title": "Question 2.4", "kind": "Muscular dystrophy", "marks": 13,
     "lead": "Muscular dystrophy is a genetic condition that causes muscles to weaken over time. It is caused by a recessive allele on the X "
             "chromosome (Xᵈ). The dominant allele (Xᴰ) results in normal muscle formation. The pedigree diagram below shows the inheritance of "
             "muscular dystrophy in a family.", "items": q24,
     "figure": fig(11, (102, 170, 498, 499), "A family over three generations, with a key: an open square is a male without muscular dystrophy, a shaded "
                   "square a male with muscular dystrophy, an open circle a female without muscular dystrophy and a shaded circle a female with "
                   "muscular dystrophy. Top row: 1 (open square) and 2 (open circle) are joined as parents. Their children, in the second row, are 3 "
                   "(open square), 4 (shaded square) and 5 (open circle). 5 is joined as a parent with 6 (open square); their children, in the third "
                   "row, are 7 (shaded square) and 8 (shaded square).")},
    {"id": "3.1", "title": "Question 3.1", "kind": "Bt maize", "marks": 7, "lead": "Read the passage below.", "items": q31,
     "extract": "GENETICALLY MODIFIED MAIZE\n\nThe bacterium Bacillus thuringiensis produces a toxin, called Bt, that kills insects. This bacterium "
                "is used to genetically modify maize to contain the Bt toxin. This Bt maize is toxic to insects."},
    {"id": "3.2", "title": "Question 3.2", "kind": "Phylogenetic tree", "marks": 9,
     "lead": "The phylogenetic tree below shows the evolutionary relationship between some species.", "items": q32,
     "figure": fig(12, (163, 317, 463, 593), "A tree with seven groups along the top, each drawn as a silhouette, from left to right: New-world "
                   "monkeys, gibbons, humans, chimpanzees, gorillas, orangutans and Old-world monkeys. A bracket labelled P spans chimpanzees, gorillas "
                   "and orangutans. The humans' branch runs down to the right: the chimpanzees' branch joins it at Q and the gorillas' at R, and it "
                   "ends at S on the orangutans' branch. The orangutans' branch runs on down to the left and ends at T on the gibbons' branch. The "
                   "gibbons' branch runs on down to the right and ends at U on the Old-world monkeys' branch, which runs on down to the left and ends "
                   "at V, the foot of the tree, on the New-world monkeys' branch.")},
    {"id": "3.3", "title": "Question 3.3", "kind": "Milk and height", "marks": 12,
     "lead": "A group of researchers conducted an investigation to determine the influence of the type of milk on the height of children drinking "
             "the milk. (The investigation was conducted over a period of 7 years from age 3 to age 10.)", "items": q33,
     "extract": "They:\n• Selected 4 146 healthy 3-year-old children of the same race and gender\n• Divided the children into two equal groups: one "
                "group was given 1 litre of cow's milk to drink daily; the other group was given 1 litre of soy milk to drink daily\n• Ensured that "
                "each group had the same additional diet, similar daily activities and similar living conditions\n• Provided the milk from the same "
                "supplier\n• Measured the children's height at the end of the investigation and calculated the average\n\nThe table below shows the "
                "results at the end of the investigation compared to the expected average height of 10-year-olds.",
     "table": {"head": ["EXPECTED AVERAGE HEIGHT OF CHILD (cm)", "AVERAGE HEIGHT OF A CHILD ON COW'S MILK (cm)", "AVERAGE HEIGHT OF A CHILD ON SOY MILK (cm)"],
               "rows": [["149,86", "151,4", "147,4"]]}},
    {"id": "3.4", "title": "Question 3.4", "kind": "Homo erectus", "marks": 13, "lead": "The passage below describes Homo erectus fossils.", "items": q34,
     "extract": "Evidence from fossils of Homo erectus shows that they appeared in Africa about 2 million years ago. They spread to many parts of Asia. "
                "Homo erectus is the oldest known species to be fully bipedal and have a human-like body. Their brain size was smaller than that of "
                "humans today. A prominent brow ridge was present over their eye sockets."},
    {"id": "3.5", "title": "Question 3.5", "kind": "Wolves of Chernobyl", "marks": 9, "lead": "Read the passage below.", "items": q35,
     "extract": "NATURAL SELECTION IN WOLVES\n\nIn 1986 there was a huge radioactive disaster in Chernobyl and all humans immediately left the area "
                "because of the deadly high radiation. Animals exposed to this high radiation developed cancer or died. Almost 40 years later, "
                "scientists have been studying the wolves that live in this highly radioactive environment where they are exposed to high radiation. "
                "They found that these wolves have a mutation that makes them immune to cancer."},
]

# ---- Written answers as STATEMENTS (Murci 2026-10-10, as Business Studies P2 Nov 2025): a written part plays as picking statements:
# the memo's own points (right, tidied to one reading of its "/" alternatives) and CLEARLY wrong ones (never a true point the memo
# leaves out: its "any other relevant answer" would make that right). The learner picks marks/each of them, any right one counts (the
# memo's "any N"), each right pick earns `each` (Life Sciences: 1 a tick; a difference with both sides ticked, 2); the cards are
# shuffled the same way every run. The memo points above (rub) stay as the source. No Section C essay in this paper (Section B is
# Questions 2 and 3) and no calculation with a working (2.4.4's cross is built on the Punnett square), so no essay sections and no
# whole-working MCQs.
import random

PID = "ls-p2-2024-11"


def stmt(n, q, marks, right, wrong, clues, each):
    count = marks // each
    assert marks % each == 0 and 1 <= count <= len(right) and 5 <= len(right) + len(wrong) <= 8, n
    assert len(set(right + wrong)) == len(right + wrong), n + ": a statement twice"
    order = list(range(len(right) + len(wrong)))
    random.Random(PID + ":" + n).shuffle(order)
    opts = [(right + wrong)[i] for i in order]
    return {"t": "pickn", "n": n, "marks": marks, "q": q, "clues": clues, "opts": opts,
            "pool": sorted(k for k, i in enumerate(order) if i < len(right)), "count": count}


STATEMENTS = {
    # 6 of the memo's 7 points ("Any"): all 7 fill the 8 cards with one wrong (the 8-card limit)
    "2.1.2": (1, ["The DNA double helix unwinds.", "The weak hydrogen bonds break, so the double strand unzips.",
                  "Two separate strands are formed.", "One strand is used as a template.", "An mRNA molecule is formed on the template strand.",
                  "Free RNA nucleotides from the nucleoplasm are used.", "The mRNA is complementary to the DNA template strand."],
              ["Molecule Y is formed at a ribosome in the cytoplasm."]),
    # (1 x 2): a difference, its two sides ticked, is worth the whole 2
    "2.1.3": (2, ["Molecule X (DNA) is double stranded, while molecule Y (RNA) is single stranded.",
                  "Molecule X (DNA) contains deoxyribose sugar, while molecule Y (RNA) contains ribose sugar.",
                  "Molecule X (DNA) has thymine as a nitrogenous base, while molecule Y (RNA) has uracil."],
              ["Molecule X (DNA) is single stranded, while molecule Y (RNA) is double stranded.",
               "Molecule X (DNA) contains ribose sugar, while molecule Y (RNA) contains deoxyribose sugar.",
               "Molecule X (DNA) has uracil as a nitrogenous base, while molecule Y (RNA) has thymine.",
               "Molecule X (DNA) is shorter, while molecule Y (RNA) is longer."]),
    "2.2.2": (2, ["Whole chromosomes move to the poles during anaphase I, while chromatids move to the poles during anaphase II.",
                  "Centromeres do not split during anaphase I, while centromeres split during anaphase II."],
              ["Chromatids move to the poles during anaphase I, while whole chromosomes move to the poles during anaphase II.",
               "Centromeres split during anaphase I, while centromeres do not split during anaphase II.",
               "Crossing over takes place during anaphase I, while it does not take place during anaphase II."]),
    "2.2.4": (1, ["It attaches to the centromere.", "It pulls the chromatids towards the opposite poles.", "It contracts and shortens."],
              ["It copies the DNA before the cell divides.", "It forms a new nuclear membrane around each set of chromosomes.",
               "It holds the two chromatids of a chromosome together."]),
    "2.3.3": (1, ["The man is heterozygous for blood group A: he is Iᴬi.", "The woman has an allele for blood group B: she is IᴬIᴮ.",
                  "The child inherits the Iᴮ allele from the mother.", "The child inherits the i allele from the father.",
                  "The child is heterozygous for blood group B: the genotype is Iᴮi."],
              ["The man is homozygous for blood group A: he is IᴬIᴬ.", "The father passes the Iᴮ allele on to the child.",
               "The child is homozygous for blood group B: the genotype is IᴮIᴮ."]),
    "2.4.3": (1, ["Males have only one X chromosome (XY).", "Males need only one recessive allele to have muscular dystrophy.",
                  "Females have two X chromosomes.", "Females need two recessive alleles (XᵈXᵈ) to have muscular dystrophy.",
                  "In females, a dominant allele on one X chromosome masks the effect of the recessive allele."],
              ["The allele for muscular dystrophy is carried on the Y chromosome.",
               "Males have two X chromosomes, so they inherit two recessive alleles.",
               "Females need only one recessive allele to have muscular dystrophy."]),
    "3.1.1": (1, ["The Bt-producing gene is cut from the bacterial DNA.", "The Bt-producing gene is inserted into the maize DNA.",
                  "The maize DNA carrying the bacterial gene is recombinant DNA.",
                  "The recombinant DNA causes the maize plant to produce the Bt toxin."],
              ["A maize gene is inserted into the DNA of the bacterium.", "The maize is cross-pollinated with the bacterium.",
               "The Bt toxin gene is removed from the maize DNA."]),
    # (2 x 2): a reason and its result; the memo has exactly TWO reasons (its "/" results are one reading each)
    "3.1.2": (2, ["Fewer crops are damaged by insects, which leads to an increased yield.",
                  "There is a reduced need for pesticides, so farmers save money."],
              ["More pesticide must be sprayed on Bt maize, so farmers spend more money.",
               "Bt maize attracts more insects, which pollinate it and increase the yield.",
               "Bt maize needs no water or fertiliser, so it costs nothing to grow."]),
    # the memo's reason for 'gibbons' and its reason for 'U' (both answers it accepts at 3.2.2)
    "3.2.3": (1, ["Gibbons and Old-world monkeys share the most recent common ancestor, U.", "Old-world monkeys are directly descended from U."],
              ["Gibbons and Old-world monkeys share the most recent common ancestor, T.", "Old-world monkeys are directly descended from the gibbons.",
               "Gibbons and Old-world monkeys both belong to group P."]),
    "3.3.7": (2, ["Cow's milk consumption leads to increased height compared to soy milk.",
                  "Soy milk consumption by children leads to below-average height.",
                  "Cow's milk consumption by children leads to above-average height."],
              ["Soy milk consumption leads to increased height compared to cow's milk.",
               "The type of milk has no influence on the height of children.",
               "Cow's milk consumption by children leads to below-average height."]),
    "3.4.1": (1, ["The oldest fossils of Homo erectus were found in Africa.",
                  "The younger fossils of Homo erectus were found in other parts of the world, such as Asia.",
                  "The ages and places of the fossils indicate that Homo erectus migrated out of Africa."],
              ["The oldest fossils of Homo erectus were found in Asia.", "Homo erectus fossils were found in Africa only.",
               "The ages and places of the fossils indicate that Homo erectus migrated from Asia into Africa."]),
    "3.4.2": (1, ["Ardipithecus fossils were found in Africa only.", "Australopithecus fossils were found in Africa only.",
                  "Fossils of Homo habilis were found in Africa only.", "The oldest fossils of Homo sapiens were found in Africa.",
                  "The younger fossils of Homo sapiens were found in other parts of the world."],
              ["The oldest fossils of Homo sapiens were found in Europe.", "Australopithecus fossils were found on every continent.",
               "Fossils of Homo habilis were found only outside Africa."]),
    "3.4.4": (1, ["The foramen magnum was in a more forward position."],
              ["The foramen magnum was in a more backward position.", "The skull had no foramen magnum.",
               "The brain case was smaller than that of a chimpanzee.", "The canine teeth were large and pointed, like those of a gorilla."]),
    "3.5.1": (1, ["A change in the genetic composition of an organism."],
              ["The process by which organisms with favourable characteristics survive and reproduce.",
               "The exchange of genetic material between homologous chromosomes during meiosis.",
               "The movement of alleles from one population to another.", "The formation of a new species from an existing one."]),
    # 7 of the memo's 8 points ("Any"): its "When exposed to radiation" opens the point after it, so the two play as one statement and
    # the 8 ticks as 7 cards + one wrong (the Lamarckian slip: a mutation arising because it is needed)
    "3.5.3": (1, ["There was variation amongst the wolves in the population.",
                  "Some wolves had the mutation which made them immune to cancer and some did not.",
                  "When exposed to the radiation, the wolves without the mutation died.", "The wolves with the mutation survived.",
                  "The wolves that survived reproduced.", "The survivors passed the allele for the mutation on to their offspring.",
                  "The next generation had a higher proportion of wolves with the mutation."],
              ["The wolves developed the mutation because they needed to survive the radiation."]),
}
# A written part whose memo weighs two sides plays as a SORT (variety): 3.4.3's tabulated differences, each feature sorted into its
# species' column (the memo's table), or "Not true" (true of neither: both species walk upright). 1 mark a row: the memo's 4 entries +
# 1 false row = 5; the memo's mark for drawing a table is the sort's own two-column layout.
SORTS = {
    "3.4.3": (["Homo erectus", "Homo sapiens", "Not true"], [
        ("Small brain", 0), ("Prominent brow ridges", 0), ("Large brain", 1), ("Reduced brow ridges", 1), ("Walks on all four limbs", 2)]),
}


def sort_(n, q, marks, bins, rows, clues):
    order = list(range(len(rows)))
    random.Random(PID + ":sort:" + n).shuffle(order)
    rows = [rows[i] for i in order]
    assert marks == len(rows) and len(set(b for _, b in rows)) == len(bins), n
    return {"t": "match", "n": n, "marks": marks, "q": q + " Sort each statement.", "clues": clues, "left": [r for r, _ in rows],
            "right": bins, "a": [b for _, b in rows], "heads": ["STATEMENTS", "SORT INTO"], "groups": True}


# GATES: a part whose statements show an earlier part's answer opens only once that part is answered (2.1.2-2.1.3 name molecule Y as
# mRNA/RNA, 2.2.2 names anaphase II, 2.2.4 describes structure B's role, 3.2.3 names the gibbons)
GATES = {"2.1.2": ["2.1.1"], "2.1.3": ["2.1.1"], "2.2.2": ["2.2.1"], "2.2.4": ["2.2.3(b)"], "3.2.3": ["3.2.2"]}
for _m in missions + missions_b:
    for _k, _it in enumerate(_m["items"]):
        if _it["t"] == "rubric" and _it["n"] in SORTS:
            _bins, _rows = SORTS[_it["n"]]
            _m["items"][_k] = sort_(_it["n"], _it["q"], _it["marks"], _bins, _rows, _it["clues"])
        elif _it["t"] == "rubric" and _it["n"] in STATEMENTS:
            _each, _right, _wrong = STATEMENTS[_it["n"]]
            _m["items"][_k] = stmt(_it["n"], _it["q"], _it["marks"], _right, _wrong, _it["clues"], _each)
        if _it["n"] in GATES:
            _m["items"][_k]["after"] = GATES[_it["n"]]
_ITEMS = [i for m in missions + missions_b for i in m["items"]]
assert not [i["n"] for i in _ITEMS if i["t"] in ("rubric", "steps")], "a written answer or typed steps left"
assert set(GATES) | set(n for g in GATES.values() for n in g) <= {i["n"] for i in _ITEMS}, "a gate names a missing part"
for _m in missions + missions_b:
    assert sum(i["marks"] for i in _m["items"]) == _m["marks"], _m["id"]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Life Sciences", "title": "Life Sciences P2", "sitting": "November 2024", "total_marks": 150, "time": "2½ hours"},
    "sections": [{"title": "Section A", "total": 50, "missions": missions}, {"title": "Section B", "total": 100, "missions": missions_b}],
    "flags": [
        {"n": "2.4.4", "kind": "no_fit", "detail": "The memo's compulsory mark is '25% chance of muscular dystrophy child'. The cross builder takes the offspring's phenotypes and their proportions (2 : 1 : 1, or 50 : 25 : 25), which give the 25%; the compulsory point is marked on those proportions."},
        {"n": "3.2.2", "kind": "memo_issue", "detail": "The question asks for a SPECIES, and the memo also accepts 'U' (a common ancestor); kept as the memo has it. 3.2.4 likewise accepts Q."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 3), hand-transcribed from the paper and memo PDFs; no API call."},
        {"n": "2.1.2", "kind": "no_fit", "detail": "Written answers play as statements (Murci, 2026-10-10): " + ", ".join(sorted(STATEMENTS)) + " pick the "
                                                   "memo's points among clearly wrong ones, 1 mark a tick (2.1.3, 2.2.2, 3.1.2 and 3.3.7: 2 a point, "
                                                   "as the memo ticks both halves). 2.1.2 (any 6 of 7) and 3.5.3 (any 7 of 8) fill the 8-card limit "
                                                   "with the memo's points and ONE wrong statement; 3.5.3 joins 'When exposed to radiation' to the "
                                                   "point it opens, so its 8 ticks play as 7 statements."},
        {"n": "3.4.3", "kind": "no_fit", "detail": "The tabulation plays as a sort into the two species' columns: the memo's 4 entries + 1 'Not true' "
                                                   "row, 5 marks. The memo's mark for drawing a table is the sort's own two-column layout, so the "
                                                   "fifth mark is earned on the false row."},
        {"n": "3.2.3", "kind": "memo_issue", "detail": "The memo's reason depends on the 3.2.2 answer it accepts (gibbons: they share the most "
                                                       "recent common ancestor U; 'U': Old-world monkeys are directly descended from U). Both "
                                                       "reasons are right statements; the part opens after 3.2.2, as its statements name the gibbons."},
    ],
}
out = Path(__file__).parent / "out" / "ls-p2-2024-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs (no API call)", "scope": "Questions 1 to 3 (the whole paper)"},
                                               "paper": paper}, indent=1, ensure_ascii=False), encoding="utf-8")
for sec in paper["sections"]:
    print(sec["title"], "parts:", sum(len(m["items"]) for m in sec["missions"]), "marks:", sum(i["marks"] for m in sec["missions"] for i in m["items"]))
