"""Life Sciences P2 Nov 2025, the whole paper (Questions 1 to 3), hand-transcribed into the catalogue format (as if Claude had produced it), then run through
`ingest.py --from-json` like any ingested paper. Stems, options, marks and answers are the paper's and the memo's own; the clues and
the figure captions (alt text) are ours. No API call: the transcription is the source, kept in git (out/ is not).
2025 papers first, 2024 stays playable (Murci, 2026-10-06).

  python tools/ingest/transcribe_ls_p2_2025_11.py
  python tools/ingest/ingest.py "<...>/Life Sciences P2 Nov 2025 Eng.pdf" "<...>/Life Sciences P2 Nov 2025 MG Eng.pdf" --id ls-p2-2025-11 --from-json
  then open Exam Practice.dc.html?ingested=ls-p2-2025-11&paper=ls-p2-2025-11&play=0

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

# ---- Section A: Question 1, from the question paper pages 3-8 and the memo page 4 ----
DNA = fig(4, (140, 125, 502, 492), "DNA replication, in a box. At the bottom the two strands are still paired: the left-hand strand's bases read "
          "G, A, T, T from top to bottom, their partners on the right blank boxes. Each unit on a strand is a box (a base) joined to a pentagon, "
          "the pentagons linked by small circles. Above, the strands have come apart. The left-hand strand runs up to the left with bases C, T, "
          "G, A (from the fork outwards); 4 points to the pentagon carrying T, and 5 to the small circle joining the pentagons carrying A and G. "
          "The right-hand strand runs up to the right with four bases: from the fork outwards a blank box, the box labelled 3, then two blank "
          "boxes. Beside it a new strand of three units is forming, the box labelled 2 at its outer end, opposite the right-hand strand's "
          "outermost box. Free units (a box, a pentagon and a small circle each) float between the strands; 1 points to a dashed circle round "
          "one of them in the middle.")
PLANTS = ("In a certain plant species, one gene controls stem colour and another controls plant height. The stem colour can be brown (B) or "
          "red (b), while the plant height can be tall (T) or short (t). Plant 1: stem colour brown, plant height short. Plant 2: stem colour "
          "red, plant height tall. When plant 1 was crossed with plant 2, some of their offspring were red and short. ")
q11 = [
    mcq("1.1.1", "A gene is …", ["the complete set of chromosomes of an organism.", "a segment on a chromosome, coding for a characteristic.",
                                 "the haploid number of chromosomes in a cell.", "a triplet of bases that codes for an amino acid."], 1,
        ["Think of the levels: genome, chromosome, gene, codon.", "A gene sits between a whole chromosome and a single triplet."]),
    mcq("1.1.2", "The significance of DNA replication is that the cells formed at the end of mitosis will …",
        ["be genetically identical.", "contain half the number of chromosomes.", "be genetically different.", "have double the number of chromosomes."], 0,
        ["Mitosis makes copies of a cell.", "What would the daughter cells get if the DNA were not copied first?"]),
    mcq("1.1.3", "Which ONE of the following statements is a feature of punctuated equilibrium?",
        ["Individual organisms adapt to changes in the environment.", "The inheritance of acquired characteristics",
         "There are long periods of little or no change in a population.", "The more a structure is used, the more it develops."], 2,
        ["The name has two halves: a long 'equilibrium', broken by sudden 'punctuation'.", "Two of the options are Lamarck's ideas, not this theory."]),
    mcq("1.1.4", "Haemophilia is …", ["characterised by the inability to distinguish between red and green.",
                                      "caused by a mutation of an allele on the X-chromosome.",
                                      "caused by non-disjunction of chromosomes during meiosis.", "caused by an allele carried on an autosome."], 1,
        ["Option A describes a different disorder.", "Haemophilia is far more common in boys: what does that say about where its allele sits?"]),
    mcq("1.1.5", "Which ONE of the following is an example of a heterozygous genotype?", ["XʳXʳ", "BB", "RW", "aa"], 2,
        ["Heterozygous means the two alleles are different.", "Look at the letters of each genotype: which pair is not the same?"]),
    # options printed as a TABLE: optTable carries it; opts read each row as a line (the medal card, the memo)
    mcq("1.1.6", "Which ONE of the following combinations CORRECTLY identifies molecules 1, 4 and 5?",
        ["1: nucleotide · 4: deoxyribose · 5: phosphate", "1: nitrogenous base · 4: phosphate · 5: deoxyribose",
         "1: nucleotide · 4: phosphate · 5: deoxyribose", "1: nitrogenous base · 4: deoxyribose · 5: phosphate"], 0,
        ["Molecule 1 is the whole circled unit, not just one part of it.",
         "Of the shapes on a strand, which is the five-carbon ring, and which links the units along the strand?"],
        figure=DNA, optTable={"head": ["Molecule 1", "Molecule 4", "Molecule 5"],
                              "rows": [["Nucleotide", "Deoxyribose", "Phosphate"], ["Nitrogenous base", "Phosphate", "Deoxyribose"],
                                       ["Nucleotide", "Phosphate", "Deoxyribose"], ["Nitrogenous base", "Deoxyribose", "Phosphate"]]}),
    mcq("1.1.7", "Which ONE of the following combinations is CORRECT for molecules 2 and 3?",
        ["2: T · 3: A", "2: A · 3: A", "2: T · 3: G", "2: A · 3: C"], 1,
        ["Bases pair A with T and G with C.", "Work out the right-hand strand from the left-hand one first, then the new strand that pairs with it."],
        figure=DNA, optTable={"head": ["Molecule 2", "Molecule 3"], "rows": [["T", "A"], ["A", "A"], ["T", "G"], ["A", "C"]]}),
    mcq("1.1.8", PLANTS + "Which ONE of the following represents the genotypes of plant 1 and plant 2?",
        ["Plant 1: bbtt · plant 2: BbTt", "Plant 1: Bbtt · plant 2: bbTt", "Plant 1: BbTt · plant 2: bbtt", "Plant 1: bbTt · plant 2: Bbtt"], 1,
        ["Red and short are both recessive: what genotype do those offspring have?",
         "Each parent must have passed on one of those recessive alleles for each gene; check the phenotypes too."],
        optTable={"head": ["PLANT 1", "PLANT 2"], "rows": [["bbtt", "BbTt"], ["Bbtt", "bbTt"], ["BbTt", "bbtt"], ["bbTt", "Bbtt"]]}),
    mcq("1.1.9", PLANTS + "The number of possible different genotypes expected in the offspring from this cross is …", ["4.", "8.", "9.", "16."], 0,
        ["Write the gametes of each parent first.", "Combine them in a grid and count only the genotypes that are different."]),
    mcq("1.1.10", "A rare form of rickets is caused by a dominant allele on the X-chromosome. Which ONE of the following statements is TRUE about "
        "the inheritance of this form of rickets?",
        ["If the father is affected, all his sons will be affected.",
         "It will be expressed more frequently in males than in females, since males have only one X-chromosome.",
         "If the father is affected, all his daughters will be affected.", "It will only be expressed in females, since they have two X-chromosomes."], 2,
        ["Which of his sex chromosomes does a father pass to a son, and which to a daughter?", "A dominant allele needs only one copy to show."]),
]
q12 = [
    term("1.2.1", "The bond formed between two amino acids during protein synthesis", ["peptide bond", "peptide", "peptide bonds"],
         ["It forms at the ribosome as the chain grows.", "A chain held together by many of these bonds is a protein."]),
    term("1.2.2", "An organelle that contains DNA which is used in tracing female ancestry", ["mitochondrion", "mitochondria"],
         ["It is the organelle of cellular respiration.", "It is passed on only through the mother's egg."]),
    term("1.2.3", "Undifferentiated cells in animals that have the potential to become any type of tissue", ["stem cells", "stem cell"],
         ["They are found in embryos and in bone marrow.", "They have not yet specialised."]),
    term("1.2.4", "A change in the sequence of nitrogenous bases resulting in the formation of a different protein",
         ["mutation", "gene mutation", "mutations"], ["It can happen by a substitution, an insertion or a deletion.", "It changes the genetic code."]),
    term("1.2.5", "The natural shape of a DNA molecule", ["double helix"], ["Watson and Crick described it in 1953.", "Think of a twisted ladder."]),
    term("1.2.6", "The permanent disappearance of a species from Earth", ["extinction"],
         ["The dodo is an example.", "Once it happens, the species is gone forever."]),
    term("1.2.7", "A type of variation with a range of intermediate phenotypes", ["continuous variation", "continuous"],
         ["Height and mass are examples.", "The values form a smooth range with no clear groups."]),
    term("1.2.8", "An allele that is expressed in a phenotype in the heterozygous condition", ["dominant allele", "dominant"],
         ["It masks the other allele.", "It is written with a capital letter."]),
    term("1.2.9", "The position of an allele on a chromosome", ["locus"],
         ["It is a gene's 'address' on a chromosome.", "Homologous chromosomes carry the alleles of a gene at the same one."]),
]
q13 = [
    abq("1.3.1", "The phase of meiosis during which non-disjunction can occur", "Anaphase I", "Anaphase II", 2,
        ["Non-disjunction is when chromosomes or chromatids fail to separate.", "Separation happens in both divisions of meiosis."]),
    abq("1.3.2", "A representation of the number, shape and arrangement of all the chromosomes in the nucleus", "Phylogenetic tree", "Karyotype", 1,
        ["One item shows how species are related; the other shows chromosomes.", "Which one is a picture of chromosomes arranged in pairs?"]),
    abq("1.3.3", "The alleles of a gene separate into different gametes during meiosis", "Law of independent assortment", "Law of segregation", 1,
        ["One of Mendel's laws is about one gene, the other about two genes at once.", "Which law deals with the two alleles of a single gene?"]),
]
CELLS = ["V", "W", "X", "Y", "Z"]
q14 = [
    term("1.4.1(a)", "Identify part A", ["cell membrane"], ["The line ends on the outline of the cell, not inside it.", "It is the boundary round the cytoplasm."]),
    term("1.4.1(b)", "Identify part B", ["spindle fibre", "spindle fibres", "spindle fiber", "spindle fibers"],
         ["These dashed lines run from one end of the cell to the other.", "Chromosomes attach to them by their centromeres."]),
    term("1.4.1(c)", "Identify part C", ["centriole", "centrosome", "centrioles"],
         ["It sits at the end (pole) of the cell.", "Animal cells have it; the dashed lines start from it."]),
    mcq1("1.4.2(a)", "Which diagram (V, W, X, Y or Z) represents a cell during prophase of mitosis", CELLS, 1,
         ["In prophase the nuclear membrane is still there and the chromosomes are visible.",
          "In mitosis homologous chromosomes do NOT pair up: look for six single chromosomes."]),
    mcq1("1.4.2(b)", "Which diagram (V, W, X, Y or Z) represents a cell during metaphase I", CELLS, 3,
         ["In metaphase the chromosomes lie at the equator.", "In meiosis I they line up in homologous pairs."]),
    mcq1("1.4.2(c)", "Which diagram (V, W, X, Y or Z) represents a cell during prophase I", CELLS, 0,
         ["In prophase the nucleus is still there.", "In meiosis I the homologous chromosomes pair up side by side."]),
    num("1.4.3(a)", "How many chromosomes will there be in each cell at the end of mitosis", 6, 0, "",
        ["Mitosis keeps the chromosome number the same.", "Count the chromosomes in a cell at the start, such as W."]),
    num("1.4.3(b)", "How many chromosomes will there be in each cell at the end of meiosis I", 3, 0, "",
        ["Meiosis I halves the chromosome number.", "Start from the number in a cell before it divides."]),
]
q15 = [
    term("1.5.1(a)", "Identify the stage of protein synthesis represented", ["translation"],
         ["The mRNA has left the nucleus and the amino acids are being brought to it.", "It is the second stage, after transcription."]),
    term("1.5.1(b)", "Identify molecule 1", ["tRNA", "transfer RNA", "t-RNA"],
         ["It carries an amino acid at one end.", "Its three bases at the other end are an anticodon."]),
    term("1.5.1(c)", "Identify organelle Z", ["ribosome", "ribosomes"], ["This organelle is where proteins are made.", "The mRNA attaches to it."]),
    term("1.5.2(a)", "State the sequence of nitrogenous bases on the DNA molecule for codon 3", ["CGT"],
         ["The codon is on mRNA: the DNA bases pair with it.", "DNA has T where it pairs with A, and no U."]),
    term("1.5.2(b)", "State the sequence of nitrogenous bases on the DNA molecule for codon 4", ["CTA"],
         ["Codon 4 pairs with the anticodon left over after codons 2, 3 and 5 are matched.",
          "Find codon 4's bases, then write the DNA bases that pair with them (T, not U, on DNA)."], marks=2),
    mcq1("1.5.3", "Which amino acid (P, Q, R or S) is coded for by codon 5?", ["P", "Q", "R", "S"], 0,
         ["Which three bases pair with C G A?", "Find the molecule carrying those three bases."]),
]
missions = [
    {"id": "1.1", "title": "Question 1.1", "kind": "Multiple choice", "marks": 20,
     "lead": "Various options are provided as possible answers to the following questions.", "items": q11},
    {"id": "1.2", "title": "Question 1.2", "kind": "Biological terms", "marks": 9,
     "lead": "Give the correct biological term for EACH of the following descriptions.", "items": q12},
    {"id": "1.3", "title": "Question 1.3", "kind": "A, B, both or none", "marks": 6,
     "lead": "Indicate whether each of the descriptions in COLUMN I apply to A ONLY, B ONLY, BOTH A AND B or NONE of the items in COLUMN II.", "items": q13},
    {"id": "1.4", "title": "Question 1.4", "kind": "Mitosis and meiosis", "marks": 8,
     "lead": "The diagrams below represent cells from the same organism during different phases of mitosis and meiosis.", "items": q14,
     "figure": fig(7, (104, 128, 535, 452), "Five cells: V, W and X in the top row, Y and Z below. V: inside a dotted nuclear outline, six "
                   "chromosomes of two chromatids each, lying in three pairs of matching shape, and a small dotted circle; outside the nucleus "
                   "at the bottom left, an oval of dashed lines between two small dark ends. W: inside a dotted nuclear outline, six chromosomes "
                   "of two chromatids each, scattered singly (not in pairs), and a small dotted circle; the dashed oval at the bottom right. X: no "
                   "nucleus; dashed lines from a dot at the top and a dot at the bottom pull three single-stranded chromosomes towards each end. "
                   "Y: no nucleus; dashed lines run from a dot at the top to a dot at the bottom, and six chromosomes of two chromatids each lie "
                   "across the middle in three pairs, the two of each pair one above the other. A is a line to the cell's outline near the top, B "
                   "a line to one of the dashed lines running down from the top dot, C a line to the dot at the bottom. Z: inside a dotted "
                   "nuclear outline, three chromosomes of two chromatids each and a small dotted circle; the dashed oval at the bottom right.")},
    {"id": "1.5", "title": "Question 1.5", "kind": "Protein synthesis", "marks": 7,
     "lead": "The diagram below represents a stage of protein synthesis. Each amino acid (P, Q, R and S) is coded for by a different codon on "
             "this mRNA molecule.", "items": q15,
     "figure": fig(8, (102, 129, 506, 432), "A horizontal strand with four brackets above it, numbered 2 to 5 from left to right, each over three "
                   "bases: 2 = U A C, 3 = G C A, 4 = three positions with no letters, 5 = C G A. A large circle, Z, sits under the strand below "
                   "brackets 3 and 4. Around it are four cross-shaped molecules, each with an oval holding a letter at one end and three bases at "
                   "the other (read left to right): R (top left) with C U A; S (top right) with A U G, 1 being a line to the middle of this "
                   "molecule; Q (bottom left) with C G U; P (bottom right) with G C U.")},
]

# ---- Section B: Questions 2 and 3, from the question paper pages 9-17 and the memo pages 5-9 ----
# (a list scores an answer that holds the FIRST WORD of an accepted answer: each accepted answer leads with a word only that point uses)
q21 = [
    term("2.1.1", "Identify structure A.", ["centromere"], ["It joins the two chromatids.", "Spindle fibres attach here."]),
    term("2.1.2", "Give the biological term for the sex chromosomes.", ["gonosomes", "gonosome"],
         ["The other 22 pairs are called autosomes.", "These are the 23rd pair, which decide a person's sex."]),
    rub("2.1.3", "Describe how these chromosomes would differ in the somatic cells of a male.", 1,
        ["There will be one X-chromosome and one Y-chromosome"],
        ["A male's sex chromosomes are not a matching pair.", "Which two sex chromosomes does a male have?"]),
    term("2.1.4(a)", "An exchange of genetic material takes place at region P. Name the process above.", ["crossing over", "crossing-over"],
         ["Chromatids of homologous chromosomes swap pieces.", "The points where they touch are chiasmata."]),
    term("2.1.4(b)", "Identify the phase during which the process named in QUESTION 2.1.4(a) takes place.", ["prophase I", "prophase 1"],
         ["It happens while the homologous chromosomes are paired.", "It is early in the first division of meiosis."],
         reject=["prophase II", "prophase 2", "prophase"]),
    rub("2.1.4(c)", "Give ONE reason why the process named in QUESTION 2.1.4(a) is important.", 1, ["Leads to (increased) genetic variation"],
        ["Why do the offspring of the same parents look different?", "New combinations of alleles: what do they add to a population?"]),
    rub("2.1.5", "Explain how the structure of the chromosomes would differ at the end of meiosis II.", 2,
        ["They will appear as chromatids", "due to the splitting of the centromere / the chromosome separating",
         "OR — Each chromosome will have some genetic material of the other chromosome", "because of crossing over"],
        ["In meiosis II, what splits so that the two halves separate?", "Think also of what crossing over did to each chromatid."]),
    rub("2.1.6", "Non-disjunction of these chromosomes occurred during meiosis and a gamete with an extra chromosome is formed. If this gamete is "
        "fertilised by normal gametes, the resulting zygotes will not be normal. Explain the genetic composition of these zygotes.", 3,
        ["The zygote will have XXY chromosomes / XXX chromosomes / an extra gonosome", "since the ovum with XX chromosomes",
         "fused with a sperm with a Y-chromosome / X-chromosome"],
        ["A gamete with an extra sex chromosome could be an ovum with two X-chromosomes.",
         "What does the zygote have if that ovum is fertilised by an X sperm, or by a Y sperm?"]),
]
q22 = [
    term("2.2.1", "Name the technique used in this criminal investigation.", ["DNA profiling"],
         ["The bands are like a barcode unique to each person.", "It is also used in paternity testing."]),
    mcq1("2.2.2", "Which ONE of the suspects (1 or 2) was at the crime scene?", ["1", "2"], 0,
         ["Compare each suspect's bands with the crime-scene sample.", "Look for the strip whose bands sit in the same places."]),
    rub("2.2.3", "Give ONE observable reason for your answer to QUESTION 2.2.2.", 1,
        ["The DNA profile / bands of suspect 1 is / are identical to the DNA profile of the sample from the crime scene"],
        ["Say what you compared.", "What do that suspect's bands and the crime scene's have in common?"]),
    lst("2.2.4", "Give TWO possible reasons why the suspect identified in QUESTION 2.2.2 might NOT be convicted if only this evidence is used.", 2, 2,
        [["twin (the suspect may have an identical twin)", "identical"], ["planted (evidence could have been planted at the crime scene)", "plant"],
         ["manipulation (of results can occur)", "manipulated"], ["contamination (of the DNA sample)", "contaminated"],
         ["human (error might occur during the procedure)", "error"], ["small (the DNA sample is too small)"],
         ["before (the suspect could have been at the crime scene before the crime was committed)"]],
        ["Being at the scene is not the same as committing the crime.", "Think of how the sample could have gone wrong, or who else shares the same DNA."]),
    rub("2.2.5", "Explain how the technique named in QUESTION 2.2.1 is used in paternity testing.", 4,
        ["The DNA profiles of the child, mother and possible father are compared", "since the child inherits 50% of their DNA from each parent",
         "All the DNA bands that are identical to the mother in the child's DNA profile are eliminated",
         "The remaining DNA bands are checked against the possible fathers'", "for possible matches with the child"],
        ["A child gets half of its DNA from each parent.", "Remove the bands that came from the mother: what is left to compare?"]),
]
q23 = [
    term("2.3.1", "Name the type of diagram represented above.", ["pedigree diagram", "pedigree"],
         ["It traces a characteristic through the generations of one family.", "Breeders of horses and dogs keep this kind of record too."]),
    num("2.3.2", "How many offspring do parents 3 and 4 have?", 1, 0, "", ["Find the line that joins 3 and 4.", "Follow it down to their children."]),
    term("2.3.3(a)", "Give the phenotype of individual 10", ["female with CADASIL"], ["Use the key.", "What does a filled circle stand for?"]),
    term("2.3.3(b)", "Give the genotype of individual 5", ["dd"],
         ["Individual 5 does not have CADASIL, and its allele is dominant.", "What genotype must a person without the disorder have?"]),
    rub("2.3.4", "Using evidence from the diagram, explain why individuals 1 and 2 are both heterozygous.", 4,
        ["Both individual 1 and 2 have CADASIL", "indicating they have a dominant allele / the (genotype) Dd",
         "but have children who do not have CADASIL / are homozygous recessive", "indicating that they inherited a recessive allele from each parent"],
        ["Look first at whether 1 and 2 have the disorder.", "Then at their children: what must a child without CADASIL have got from each parent?"]),
    num("2.3.5", "What is the percentage chance of parents 7 and 8 having another child with CADASIL?", 50, 0, "%",
        ["7 has CADASIL but a child without it; 8 does not have it: what are their genotypes?", "Cross the two and count the offspring with D."]),
]
GROUPS = ["A", "B", "AB", "O"]
q24 = [
    mcq1("2.4.1(a)", "Which blood group is most common in both ethnic groups", GROUPS, 3,
         ["Find the tallest bars.", "The group must be the highest for both ethnic groups."]),
    mcq1("2.4.1(b)", "Which blood group has a higher percentage in ethnic group 1 than in ethnic group 2", GROUPS, 0,
         ["Compare the black bar with the white bar for each blood group.", "Where is the black bar taller?"]),
    # superscripts: the matcher keeps only a-z and 0-9, so each answer LEADS with the typed form (IBIB) and shows the printed one after it
    lst("2.4.2", "State ALL the possible genotypes of 11% of the people in ethnic group 1.", 2, 2, [["IBIB (IᴮIᴮ)"], ["IBi (Iᴮi)"]],
        ["Which blood group is 11% in ethnic group 1?", "That group can be homozygous or heterozygous: write both, with the I alleles."]),
    mcq("2.4.3", "Ethnic group 1 had a population of 360 000 people in 2021. Which blood group (A, B, AB or O) had 39 600 people?", GROUPS, 1,
        ["Work out what percentage 39 600 is of 360 000.", "Find that percentage among ethnic group 1's bars."]),
    rub("2.4.4", "Explain the inheritance of blood group AB.", 3,
        ["Allele Iᴬ / the allele for blood group A is inherited from one parent", "and allele Iᴮ / the allele for blood group B from the other parent",
         "the alleles are co-dominant / equally dominant", "and are equally expressed in the phenotype / the child will have the genotype IᴬIᴮ"],
        ["Blood group AB needs two different alleles.", "Where does each allele come from, and how are both shown?"]),
]
q25 = [
    term("2.5.1", "Name the type of dominance displayed in the inheritance of coat colour in palomino horses.", ["incomplete dominance", "incomplete"],
         ["The offspring look like neither parent.", "Golden is a blend, in between cream and chestnut."],
         reject=["complete dominance", "complete"]),
    rub("2.5.2", "Explain your answer to QUESTION 2.5.1.", 2,
        ["Neither the allele of a cream-coloured coat and chestnut-coloured coat is dominant",
         "resulting in the intermediate phenotype which is the golden-coloured coat / palomino"],
        ["Is either allele dominant over the other?", "What kind of phenotype does the heterozygous horse show?"]),
    term("2.5.3(a)", "The breeding of horses with desired characteristics is a type of biotechnology. Name this type of biotechnology.",
         ["artificial selection", "selective breeding"], ["People choose which animals breed.", "It is the human counterpart of selection by nature."]),
    lst("2.5.3(b)", "Name the TWO phenotypes of the horses that must be interbred for a 100% chance of palomino offspring.", 2, 2,
        [["chestnut (coloured coat)"], ["cream (coloured coat)"]],
        ["A palomino has one allele of each colour.", "Which two homozygous horses always give one of each?"]),
    # a GENETIC CROSS: the memo marks 8 points, 1 compulsory (the ratio) + any 5; no catalogue type lays a cross out, so it is drawn on
    # paper and self-checked (flagged no_fit)
    {"t": "draw", "n": "2.5.4", "marks": 6,
     "q": "A horse with a cream-coloured coat was crossed with a palomino horse. Use a genetic cross to show the expected phenotypic ratio of the offspring.",
     "clues": ["Which genotype gives cream, and which gives the golden in-between colour?",
               "Lay it out: P1, meiosis, gametes, fertilisation, F1, then the ratio."],
     "criteria": [{"text": "P1 phenotypes: cream-coloured (coat) x palomino / golden-coloured (coat)", "marks": 1},
                  {"text": "P1 genotypes: AA x AG", "marks": 1},
                  {"text": "Gametes: A, A x A, G (in a Punnett square: the correct gametes)", "marks": 1},
                  {"text": "F1 genotypes: AA, AA, AG, AG (in a Punnett square: the correct genotypes)", "marks": 1},
                  {"text": "F1 phenotypes: cream-coloured, palomino / golden-coloured", "marks": 1},
                  {"text": "Ratio 1 : 1, compulsory (the phenotypes must be correct)", "marks": 1},
                  {"text": "P1 and F1 shown", "marks": 1},
                  {"text": "Meiosis and fertilisation shown", "marks": 1}],
     "memo": "*1 compulsory mark (the 1 : 1 ratio) + any 5. P1: cream-coloured (AA) x palomino (AG); meiosis; gametes A, A x A, G; "
             "fertilisation; F1: AA, AA, AG, AG, cream-coloured and palomino; 1 : 1. A Punnett square may replace the gamete and fertilisation "
             "lines: 1 mark for the correct gametes, 1 mark for the correct genotypes."},
]
q31 = [
    lst("3.1.1", "State TWO characteristics related to vision that humans share with African apes.", 2, 2,
        [["binocular (vision)"], ["stereoscopic (vision)"], ["colour (vision)", "color", "cones (presence of cones)"], ["front (eyes in front)"]],
        ["Where are the eyes on the face?", "Think of how the two eyes work together to see depth, and what colours they see."]),
    rub("3.1.2", "Describe TWO differences between the jaws of humans and African apes.", 4,
        ["Smaller jaws in humans", "and larger jaws in African apes", "Small teeth / canines in humans", "and large teeth / canines in African apes",
         "C-shaped palate in humans", "and a U-shaped palate in African apes", "Humans are non-prognathous", "and African apes are prognathous",
         "Humans do not have diastema", "and African apes have diastema", "There is a well-developed chin in humans",
         "and an underdeveloped chin in African apes"],
        ["Compare the size of the jaws and of the teeth.", "Think also of the palate's shape, the chin and how far the jaw sticks out."]),
    rub("3.1.3", "Explain the significance of the position of the foramen magnum, the shape of the spine and the size of the pelvis in bipedalism.", 6,
        ["The foramen magnum is in a more forward position", "to allow the vertebral column to attach below it", "The spine is S-shaped",
         "for better distribution of upper body weight / to absorb shock when walking upright / to allow flexibility", "The pelvis is short and wide",
         "to support the weight above the pelvis / upper body"],
        ["For each feature, say what it is like in humans and how it helps upright walking.",
         "Think of where the skull sits on the spine, the spine's curves and how the pelvis carries weight."]),
]
q32 = [
    num("3.2.1", "How many genera are represented in the table?", 3, 0, "",
        ["The genus is the first word of a scientific name.", "Count the different first words."]),
    lst("3.2.2", "Give TWO examples of fossils of Australopithecus africanus found in South Africa.", 2, 2,
        [["Taung child"], ["Mrs Ples", "Ples"], ["Little Foot", "Littlefoot"]],
        ["They come from the Cradle of Humankind and from a lime quarry in the North West.",
         "One is a child's skull, one an adult female's skull, one a nearly complete skeleton."]),
    num("3.2.3", "Give the average brain volume (mℓ) of the species that was the first to use tools.", 609, 0, "mℓ",
        ["Which species' name means 'handy man'?", "Read its brain volume from the table."]),
    {"t": "steps", "n": "3.2.4", "marks": 3,
     "q": "Calculate the percentage increase in the average brain volume between Homo habilis and Homo sapiens. Show ALL working and round off the answer to TWO decimal places.",
     "clues": ["Percentage increase = (new − old) ÷ old × 100.", "The old value is Homo habilis'; the new one is Homo sapiens'."],
     "steps": [{"id": "s1", "label": "Increase in average brain volume (mℓ)", "marks": 1, "a": 721, "tol": 0, "memo": "(1 330 − 609) / 609 ✓"},
               {"id": "s2", "label": "Percentage increase (%), to two decimal places", "marks": 2, "a": 118.39, "tol": 0.005,
                "memo": "× 100 ✓ = 118,39 ✓ %"}]},
    rub("3.2.5", "The brain decomposes after the organism dies. Explain how scientists are able to determine the brain volume of fossils.", 3,
        ["The cranium remains / becomes fossilised", "The cranium houses the brain, therefore", "measuring the cranial capacity gives brain volume"],
        ["What part of the skull survives as a fossil?", "The brain filled that space: what can be measured?"]),
    rub("3.2.6", "Explain the relationship between average brain volume and cultural evidence for human evolution.", 3,
        ["Brain volume increased", "leading to more intelligence and", "the development of (complex) tools"],
        ["Look at the trend of the brain volumes in the table.", "What does a larger brain allow, and what does it make?"]),
]
q33 = [
    rub("3.3.1(a)", "The ratites shown in the map are classified as different biological species. State what is meant by a biological species.", 2,
        ["A group of organisms with similar characteristics", "that can interbreed to produce fertile offspring"],
        ["Think of what members of one species share.", "What must come of their mating?"]),
    rub("3.3.1(b)", "Using the information in the extract, explain why the ostrich and emu are considered different species.", 2,
        ["They breed at different times of the year / ostriches lay their eggs mainly in September while emus lay their eggs from November to April",
         "therefore, they cannot interbreed"],
        ["Compare the months in which the ostrich and the emu lay eggs.", "Can they mate if they breed at different times?"]),
    lst("3.3.1(c)", "Name TWO other reproductive isolation mechanisms that would have prevented the rhea and ostrich from interbreeding if they "
        "were in the same habitat.", 2, 2,
        [["courtship (species-specific courtship behaviour)", "behaviour", "behavior"], ["infertile (offspring)"],
         ["prevention (of fertilisation)", "fertilisation", "fertilization"]],
        ["Breeding at different times is already used: think of behaviour, and of what happens after mating.",
         "What if mating happens but no zygote forms, or the offspring cannot breed?"]),
    term("3.3.2", "Identify the evidence for evolution represented in the diagram.", ["biogeography"],
         ["The diagram is a world map of where related species live.", "This evidence studies the distribution of organisms."]),
    rub("3.3.3", "Describe how the evidence identified in QUESTION 3.3.2 supports the theory of evolution.", 5,
        ["The ratites all had one common ancestor", "When continental drift occurred", "the (population) of ratites was separated",
         "The sub-populations were faced with different environmental conditions and", "underwent natural selection independently",
         "to form different species"],
        ["The ratites share one ancestor but live on continents far apart.", "How did the land split, and what did different conditions do to each group?"]),
]
q34 = [
    lst("3.4.1", "State the independent variable for this investigation.", 1, 1, [["availability (of food)", "available"]],
        ["What did the investigator change?", "The food was removed and returned."]),
    rub("3.4.2", "Describe how the dependent variable was measured.", 1,
        ["They measured the time it took for 80% of the flies to die from starvation"],
        ["What was recorded after the food was removed?", "It was a time, for a certain percentage of the flies."]),
    # a term, not a list: the list matcher takes any answer HOLDING the key word, and "age" is inside "average", "stage", "percentage"
    term("3.4.3", "State ONE controlled variable that was considered when selecting the fruit flies at the beginning of the investigation.",
         ["age", "same age", "the same age", "age of the flies", "age of the fruit flies"],
         ["Read the first point of the procedure.", "What did all 5 000 flies have in common?"]),
    rub("3.4.4", "Explain why the investigator gave the fruit flies the same type of food throughout the investigation.", 2,
        ["To improve the validity of the investigation", "by ensuring that the availability of food is the only independent variable",
         "so that any changes that occur are only due to the availability of food"],
        ["Only whether there was food was being tested, not which food.", "What would a different food do to the results?"]),
    rub("3.4.5", "Describe the results obtained in this investigation.", 2,
        ["The hours until death in the 1st generation was shorter / between 8 and 40 hours",
         "The hours until death in the 60th generation was longer / between 140 and 180 hours"],
        ["Compare where each peak sits on the time axis.", "Give the range of hours for each generation."]),
    rub("3.4.6", "Using Darwin's theory of natural selection, explain the increase in starvation resistance in fruit flies.", 6,
        ["There was variation in the population of fruit flies", "Some were starvation resistant while some were not starvation resistant",
         "When the food source was removed", "the fruit flies that were not starvation resistant died",
         "Those that were starvation resistant survived and reproduced and", "passed on the allele for starvation resistance to their offspring",
         "The next generation had a higher proportion of fruit flies that were starvation resistant"],
        ["Start with variation in the population.", "Who survives the starvation, who breeds, and what do the offspring inherit?"]),
]
missions_b = [
    {"id": "2.1", "title": "Question 2.1", "kind": "Sex chromosomes", "marks": 11, "lead": "The diagram below represents the sex chromosomes in a female.",
     "items": q21,
     "figure": fig(9, (207, 171, 388, 366), "Two X chromosomes side by side, each drawn as two long parallel strands joined by a black dot about "
                   "a third of the way down. A points to the black dot on the right-hand chromosome. P labels a dashed rectangle drawn across the "
                   "lower part of both chromosomes.")},
    {"id": "2.2", "title": "Question 2.2", "kind": "DNA evidence", "marks": 9,
     "lead": "The diagram below shows the DNA analysis of a sample obtained at a crime scene, a sample from the victim and samples from two "
             "suspects. In their investigation, police conducted a comparison of the DNA to identify the criminal.", "items": q22,
     "figure": fig(10, (105, 153, 523, 450), "Four strips of black bands, labelled on the right from top to bottom: sample from crime scene, "
                   "sample from the victim, sample from suspect 1, sample from suspect 2. The crime-scene strip has two clusters of bands at "
                   "the left, a single thin band, then three pairs of bands spread to the far right. Suspect 1's strip has the same bands in the "
                   "same places. The victim's and suspect 2's strips also have a single thin band near the middle left, but their other bands "
                   "form wide clusters in other places, and they have no bands in the right-hand third.")},
    {"id": "2.3", "title": "Question 2.3", "kind": "Inheritance of CADASIL", "marks": 9,
     "lead": "CADASIL is an autosomal genetic disorder caused by a dominant allele (D). It results in the thickening of the walls of blood vessels. "
             "The diagram below shows the inheritance of CADASIL in a family.", "items": q23,
     "figure": fig(11, (111, 155, 518, 507), "A diagram of a family over three generations, with a key: a filled circle is a female with CADASIL, a "
                   "filled square a male with CADASIL, an open circle a female without CADASIL and an open square a male without CADASIL. Top "
                   "row: 1 (filled circle) and 2 (filled square) are joined as parents; so are 3 (open square) and 4 (open circle). Second row: "
                   "the children of 1 and 2 are 5 (open circle), 6 (open square) and 7 (filled square); the child of 3 and 4 is 8 (open circle). "
                   "7 and 8 are joined as parents; their children, in the third row, are 9 (open circle), 10 (filled circle) and 11 (filled square).")},
    {"id": "2.4", "title": "Question 2.4", "kind": "Blood groups", "marks": 9,
     "lead": "The graph below shows the distribution of blood groups for two ethnic groups (1 and 2) in a certain country during 2021.", "items": q24,
     "figure": fig(12, (102, 127, 505, 410), "Bar graph 'Percentage of people with each blood group': percentage of people (0 to 60) against "
                   "blood groups A, B, AB and O, with a black bar for ethnic group 1 and a white bar for ethnic group 2 at each group. Values on "
                   "the bars: A, 40 (group 1) and 26 (group 2); B, 11 and 19; AB, 4 and 4; O, 45 and 51.")},
    {"id": "2.5", "title": "Question 2.5", "kind": "Palomino horses", "marks": 12,
     "lead": "Palomino horses are bred by horse breeders for their coat colour. A palomino has a golden-coloured coat. It is the offspring of a "
             "horse with a cream-coloured coat (A) and a horse with a chestnut-coloured coat (G).", "items": q25},
    {"id": "3.1", "title": "Question 3.1", "kind": "Humans and African apes", "marks": 12,
     "lead": "Theories of human evolution are based on the similarities between humans and African apes and also on the anatomical differences "
             "between them.", "items": q31},
    {"id": "3.2", "title": "Question 3.2", "kind": "Hominid brain volume", "marks": 13,
     "lead": "The table below shows the average brain volume of different hominid species.", "items": q32,
     "table": {"head": ["SPECIES", "AVERAGE BRAIN VOLUME (mℓ)"],
               "rows": [["Ardipithecus ramidus", "350"], ["Australopithecus africanus", "461"], ["Homo habilis", "609"], ["Homo erectus", "959"],
                        ["Homo sapiens", "1 330"]]}},
    {"id": "3.3", "title": "Question 3.3", "kind": "Ratites", "marks": 12, "lead": "The extract and diagram below are based on ratites.", "items": q33,
     "extract": "BREEDING MONTHS IN RATITES\n\nRatites are egg-laying flightless birds. The egg-laying months are influenced by many factors such as "
                "the temperature, length of the day and availability of food. Ostriches normally lay their eggs in September, rheas between "
                "October and March, while emus lay their eggs from November to April.",
     "figure": fig(15, (180, 210, 458, 459), "World map 'The present-day distribution of ratite species', the areas where each bird lives "
                   "shaded grey: the rhea across South America (darker in the east and south); the ostrich in a wide band across Africa north of "
                   "the equator, reaching down the east, and in a block in southern Africa; the emu over most of Australia. Oceans separate the "
                   "three areas.")},
    {"id": "3.4", "title": "Question 3.4", "kind": "Starvation resistance", "marks": 13,
     "lead": "Starvation resistance refers to the period for which an organism can go without food before it dies.", "items": q34,
     "extract": "An investigation was conducted to determine the effect of the availability of food on the starvation resistance in fruit flies.\n\n"
                "The procedure was as follows:\n• 5 000 fruit flies of the same age were used.\n• They were all placed in a container suitable for "
                "the growth of fruit flies and were given a maltose-based food source.\n• The food source was removed after an hour.\n• The time it "
                "took for 80% of the fruit flies to die from starvation was recorded.\n• The dead flies were removed from the container.\n• The food "
                "source was then returned to the container.\n• The remaining fruit flies were allowed to interbreed.\n• Their eggs were collected "
                "and transferred to a new container with a food source where they were allowed to hatch.\n• These fruit flies were allowed to grow "
                "to the same age as the 1st generation.\n• The food source was then removed again.\n• The time it took for 80% of the fruit flies "
                "to die from starvation was recorded again.\n• This procedure was repeated until the 60th generation of fruit flies was reached.\n\n"
                "The graphs below show the results obtained for the 1st generation and the 60th generation.",
     "figure": fig(17, (78, 169, 526, 334), "Two graphs of the number of flies (no scale) against hours until death from starvation (0 to 200). "
                   "Generation 1 (original population): one narrow peak from about 10 to 40 hours, highest near 20 hours. Generation 60: one "
                   "narrow peak from about 140 to 180 hours, highest near 160 hours.")},
]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Life Sciences", "title": "Life Sciences P2", "sitting": "November 2025", "total_marks": 150, "time": "2½ hours"},
    "sections": [{"title": "Section A", "total": 50, "missions": missions}, {"title": "Section B", "total": 100, "missions": missions_b}],
    "flags": [
        {"n": "2.3.3(b)", "kind": "no_fit", "detail": "A genotype (dd): the term matcher lowercases the answer, so DD and Dd are also marked right. A case-sensitive genotype input (or an allele picker) is the right layout."},
        {"n": "2.4.2", "kind": "no_fit", "detail": "Genotypes with superscript alleles (IᴮIᴮ, Iᴮi): the list matcher keeps only a-z and 0-9 and credits an answer that CONTAINS a key, so they are keyed as typed (IBIB, IBi), case is ignored, and a wrong IBIA also holds 'ibi'. An allele picker (Iᴬ / Iᴮ / i, two per genotype) is the right layout."},
        {"n": "2.5.4", "kind": "no_fit", "detail": "Genetic cross (P1 phenotypes and genotypes, meiosis, gametes, fertilisation, F1 genotypes and phenotypes, 1 : 1 ratio): the memo marks 8 points, 1 compulsory (the ratio) + any 5. Played as a drawing with self-check criteria (not marked online); a cross builder with a Punnett-grid option (the memo accepts either) is the right layout."},
        {"n": "3.4", "kind": "no_fit", "detail": "The question prints TWO figures: the procedure diagram (page 16: a container of flies, food removed, food returned, a new generation) and the results graphs (page 17). A mission holds one figure: the graphs are kept (3.4.5 reads them); the procedure diagram repeats the printed procedure and is left out."},
        {"n": "3.4.4", "kind": "memo_issue", "detail": "The memo's third point reads 'so that any changes that occur are only due to food availability ✓ of food' (a repeated 'of food'); transcribed as 'only due to the availability of food'."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 3), hand-transcribed from the paper and memo PDFs; no API call."},
    ],
}
out = Path(__file__).parent / "out" / "ls-p2-2025-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs (no API call)", "scope": "Questions 1 to 3 (the whole paper)"},
                                               "paper": paper}, indent=1, ensure_ascii=False), encoding="utf-8")
for sec in paper["sections"]:
    print(sec["title"], "parts:", sum(len(m["items"]) for m in sec["missions"]), "marks:", sum(i["marks"] for m in sec["missions"] for i in m["items"]))
