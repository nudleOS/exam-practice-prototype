"""Life Sciences P2 Nov 2025, the whole paper (Questions 1 to 3), hand-transcribed into the catalogue format (as if Claude had produced it), then run through
`ingest.py --from-json` like any ingested paper. Stems, options, marks and answers are the paper's and the memo's own; the clues and
the figure captions (alt text) are ours. No API call: the transcription is the source, kept in git (out/ is not).
2025 papers first, 2024 stays playable (Murci, 2026-10-06).

  python tools/ingest/transcribe_ls_p2_2025_11.py
  python tools/ingest/ingest.py "<...>/Life Sciences P2 Nov 2025 Eng.pdf" "<...>/Life Sciences P2 Nov 2025 MG Eng.pdf" --id ls-p2-2025-11 --from-json
  then open Exam Practice.dc.html?ingested=ls-p2-2025-11&paper=ls-p2-2025-11&play=0

Figure boxes are measured in PDF points on the A4 page (595 x 842) and stored as fractions.

Learner rollout (Murci, 2026-10-10): written answers play as statements (one as a sort), the typed calculation (3.2.4) as a
whole-working multiple choice, and a part whose statements show an earlier part's answer opens only after it (GATES, at the bottom).
This paper has no Section C essay (Section B is Questions 2 and 3)."""
import json
import random
import re
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

PID = "ls-p2-2025-11"
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
    return {"t": "mcq", "n": n, "marks": marks, "q": q + WORK, "clues": clues, "opts": opts, "a": a}


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
        ["Heterozygous means the two alleles of a gene are different.", "For a gene on the X-chromosome, compare the small letters, not the X's."]),
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
        ["Mitosis keeps the chromosome number the same.", "Count the chromosomes (not the chromatids) in a cell before it divides."]),
    num("1.4.3(b)", "How many chromosomes will there be in each cell at the end of meiosis I", 3, 0, "",
        ["Meiosis I halves the chromosome number.", "Start from the number in a cell before it divides."]),
]
q15 = [
    term("1.5.1(a)", "Identify the stage of protein synthesis represented", ["translation"],
         ["The mRNA has left the nucleus and the amino acids are being brought to it.", "Which stage takes place in the cytoplasm rather than in the nucleus?"]),
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
        ["This is a female's cell: what would her gamete carry if its sex chromosomes failed to separate?",
         "Then think about the two kinds of sperm that could fertilise it."]),
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
        ["Whose DNA profiles would the laboratory need for a paternity test?", "Which of the child's bands could have come only from the father?"]),
]
q23 = [
    term("2.3.1", "Name the type of diagram represented above.", ["pedigree diagram", "pedigree"],
         ["It traces a characteristic through the generations of one family.", "Breeders of horses and dogs keep this kind of record too."]),
    num("2.3.2", "How many offspring do parents 3 and 4 have?", 1, 0, "", ["Find the line that joins 3 and 4.", "Follow it down to their children."]),
    term("2.3.3(a)", "Give the phenotype of individual 10", ["female with CADASIL"],
         ["Use the key.", "Its shape gives the sex; its shading shows whether it has the disorder."]),
    # a genotype is BUILT from the alleles (catalogue `genotype`, 2026-10-06): typed, a case-folding matcher passed DD and Dd for dd
    {"t": "genotype", "n": "2.3.3(b)", "marks": 1, "q": "Give the genotype of individual 5", "alleles": ["D", "d"], "count": 1, "pool": [["d", "d"]],
     "clues": ["Find individual 5's phenotype from the key first.", "The CADASIL allele (D) is dominant: one copy is enough to show the disorder."]},
    rub("2.3.4", "Using evidence from the diagram, explain why individuals 1 and 2 are both heterozygous.", 4,
        ["Both individual 1 and 2 have CADASIL", "indicating they have a dominant allele / the (genotype) Dd",
         "but have children who do not have CADASIL / are homozygous recessive", "indicating that they inherited a recessive allele from each parent"],
        ["Look first at whether 1 and 2 have the disorder.", "Then look at their children: could two DD parents have a child without CADASIL?"]),
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
    # the paper prints no allele symbols here (a learner must know them); the tray offers the WHOLE ABO system (Iᴬ, Iᴮ, i), so it shows
    # the notation, not the answer. Typed, the superscripts were lost and a wrong IBIA held "ibi" (the list matcher's contains-check)
    {"t": "genotype", "n": "2.4.2", "marks": 2, "q": "State ALL the possible genotypes of 11% of the people in ethnic group 1.",
     "alleles": ["Iᴬ", "Iᴮ", "i"], "count": 2, "pool": [["Iᴮ", "Iᴮ"], ["Iᴮ", "i"]],
     "clues": ["Which blood group is 11% in ethnic group 1?", "That group can be homozygous or heterozygous: build both."]},
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
         ["artificial selection", "selective breeding"], ["People choose which animals breed.", "It has been used for thousands of years on crops and livestock."]),
    lst("2.5.3(b)", "Name the TWO phenotypes of the horses that must be interbred for a 100% chance of palomino offspring.", 2, 2,
        [["chestnut (coloured coat)"], ["cream (coloured coat)"]],
        ["A palomino has one allele of each colour.", "Which two homozygous horses always give one of each?"]),
    # a GENETIC CROSS: the memo marks 8 points, 1 compulsory (the ratio) + any 5; BUILT on a Punnett square (draw.build cross,
    # 2026-10-06): the parents and every offspring genotype's phenotype are the key, the marker derives the rest
    {"t": "draw", "n": "2.5.4", "marks": 6,
     "build": {"kind": "cross", "alleles": ["A", "G"], "phenos": ["cream-coloured", "palomino", "chestnut-coloured"],
               "parents": [{"pheno": "cream-coloured", "geno": ["A", "A"]}, {"pheno": "palomino", "geno": ["A", "G"]}],
               "offspring": [{"geno": ["A", "A"], "pheno": "cream-coloured"}, {"geno": ["A", "G"], "pheno": "palomino"},
                             {"geno": ["G", "G"], "pheno": "chestnut-coloured"}]},
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
        ["Think of where the eyes sit on the face.", "Think of how a primate judges distance when it moves through trees."]),
    rub("3.1.2", "Describe TWO differences between the jaws of humans and African apes.", 4,
        ["Smaller jaws in humans", "and larger jaws in African apes", "Small teeth / canines in humans", "and large teeth / canines in African apes",
         "C-shaped palate in humans", "and a U-shaped palate in African apes", "Humans are non-prognathous", "and African apes are prognathous",
         "Humans do not have diastema", "and African apes have diastema", "There is a well-developed chin in humans",
         "and an underdeveloped chin in African apes"],
        ["Picture a human skull beside a gorilla skull, seen from below.", "Each feature appears twice: one version is human, the other is an ape's."]),
    rub("3.1.3", "Explain the significance of the position of the foramen magnum, the shape of the spine and the size of the pelvis in bipedalism.", 6,
        ["The foramen magnum is in a more forward position", "to allow the vertebral column to attach below it", "The spine is S-shaped",
         "for better distribution of upper body weight / to absorb shock when walking upright / to allow flexibility", "The pelvis is short and wide",
         "to support the weight above the pelvis / upper body"],
        ["Each right statement names a feature AND says how it helps upright walking.",
         "Picture a human skeleton beside a gorilla's: the skull, the backbone and the hips."]),
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
    # (typed steps until 2026-10-10: the memo's working (1 330 − 609) / 609 ✓ × 100 ✓ = 118,39 ✓ %)
    work("3.2.4", "Calculate the percentage increase in the average brain volume between Homo habilis and Homo sapiens. Show ALL working and "
         "round off the answer to TWO decimal places.", 3, [
             "Percentage increase = {1 330 − 609}/{1 330} × 100\n= {721}/{1 330} × 100\n= 54,21%",   # divides by the NEW volume
             "Percentage increase = {959 − 609}/{609} × 100\n= {350}/{609} × 100\n= 57,47%",         # reads Homo erectus' 959 for Homo sapiens
             "Percentage increase = {1 330 − 609}/{609} × 100\n= {721}/{609} × 100\n= 118,39%",      # the memo
             "Percentage increase = {1 330 − 609}/{609} × 100\n= 1,18 × 100\n= 118,00%"], 2,         # rounds the fraction too early
         ["Check which two species the question compares, and read their volumes from the table.",
          "A percentage increase compares the change with the starting value."]),
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
        ["Compare the months in which the ostrich and the emu lay eggs.", "What has to happen at the same time for two birds to mate?"]),
    lst("3.3.1(c)", "Name TWO other reproductive isolation mechanisms that would have prevented the rhea and ostrich from interbreeding if they "
        "were in the same habitat.", 2, 2,
        [["courtship (species-specific courtship behaviour)", "behaviour", "behavior"], ["infertile (offspring)"],
         ["prevention (of fertilisation)", "fertilisation", "fertilization"]],
        ["Think of what could stop two species from mating, or make their mating fail.",
         "A mechanism can act before mating, on the gametes, or on the offspring."]),
    term("3.3.2", "Identify the evidence for evolution represented in the diagram.", ["biogeography"],
         ["The diagram is a world map of where related species live.", "This evidence studies the distribution of organisms."]),
    rub("3.3.3", "Describe how the evidence identified in QUESTION 3.3.2 supports the theory of evolution.", 5,
        ["The ratites all had one common ancestor", "When continental drift occurred", "the (population) of ratites was separated",
         "The sub-populations were faced with different environmental conditions and", "underwent natural selection independently",
         "to form different species"],
        ["Why would related flightless birds live on continents that oceans now separate?",
         "Think of what happened to the land over millions of years, and what each isolated group then faced."]),
]
q34 = [
    lst("3.4.1", "State the independent variable for this investigation.", 1, 1, [["availability (of food)", "available"]],
        ["What did the investigator change?", "The food was removed and returned."]),
    rub("3.4.2", "Describe how the dependent variable was measured.", 1,
        ["They measured the time it took for 80% of the flies to die from starvation"],
        ["What was recorded after the food was removed?", "Read the procedure: which measurement was repeated in every generation?"]),
    # a term, not a list: the list matcher takes any answer HOLDING the key word, and "age" is inside "average", "stage", "percentage"
    term("3.4.3", "State ONE controlled variable that was considered when selecting the fruit flies at the beginning of the investigation.",
         ["age", "same age", "the same age", "age of the flies", "age of the fruit flies"],
         ["Read the first point of the procedure.", "What did all 5 000 flies have in common?"]),
    rub("3.4.4", "Explain why the investigator gave the fruit flies the same type of food throughout the investigation.", 2,
        ["To improve the validity of the investigation", "by ensuring that the availability of food is the only independent variable",
         "so that any changes that occur are only due to the availability of food"],
        ["Recall what the independent variable of this investigation is.", "What would a different food do to the results?"]),
    rub("3.4.5", "Describe the results obtained in this investigation.", 2,
        ["The hours until death in the 1st generation was shorter / between 8 and 40 hours",
         "The hours until death in the 60th generation was longer / between 140 and 180 hours"],
        ["Compare where each peak sits on the time axis.", "Give the range of hours for each generation."]),
    rub("3.4.6", "Using Darwin's theory of natural selection, explain the increase in starvation resistance in fruit flies.", 6,
        ["There was variation in the population of fruit flies", "Some were starvation resistant while some were not starvation resistant",
         "When the food source was removed", "the fruit flies that were not starvation resistant died",
         "Those that were starvation resistant survived and reproduced and", "passed on the allele for starvation resistance to their offspring",
         "The next generation had a higher proportion of fruit flies that were starvation resistant"],
        ["Darwin's theory runs in a set order: where does it begin?", "Who survives the starvation, who breeds, and what do the offspring inherit?"]),
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
     # (the caption describes each strip on its own: it said "Suspect 1's strip has the same bands in the same places", 2.2.2's answer)
     "figure": fig(10, (105, 153, 523, 450), "Four strips of black bands, labelled on the right from top to bottom: sample from crime scene, "
                   "sample from the victim, sample from suspect 1, sample from suspect 2. Each strip read from left to right. Crime scene: a "
                   "thick and a thin band at the far left; three bands (thick, thin, thick) near the left; one thin band a third of the way "
                   "along; a thin and a thick band near the middle; a thick and a thin band two-thirds along; a thick and a thin band at the "
                   "far right. Victim: four thick bands side by side at the left, then two thin bands; one thin band a third of the way along; "
                   "three bands close together near the middle; four bands close together two-thirds along; nothing further right. Suspect 1: "
                   "a thick and a thin band at the far left; three bands (thick, thin, thick) near the left; one thin band a third of the way "
                   "along; a thin and a thick band near the middle; a thick and a thin band two-thirds along; a thick and a thin band at the "
                   "far right. Suspect 2: two thick bands at the far left; three bands (thick, thin, thick) near the left; one thin band a third "
                   "of the way along; three bands close together near the middle; three bands close together two-thirds along; nothing "
                   "further right.")},
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
                   "Generation 1 (original population): one narrow peak from about 8 to 40 hours, highest near 20 hours. Generation 60: one "
                   "narrow peak from about 140 to 180 hours, highest near 160 hours.")},
]

# ---- Written answers as STATEMENTS (Murci 2026-10-10, as Business Studies P2 Nov 2025): a written part plays as picking statements:
# the memo's own points (right, tidied to one reading of its "/" alternatives) and CLEARLY wrong ones (never a true point the memo
# leaves out: its "any other relevant answer" would make that right). The learner picks marks/each of them, any right one counts (the
# memo's "any N"), each right pick earns `each` (Life Sciences: 1 a tick; a point with its reason or explanation, both ticked, 2); the
# cards are shuffled the same way every run. Each card reads on its own (the cards are shuffled: no "This ..." pointing at another).
# The memo points above (rub) stay as the source.


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
    "2.1.3": (1, ["There will be one X-chromosome and one Y-chromosome."],
              ["There will be two Y-chromosomes.", "There will be two X-chromosomes, the same as in the female.",
               "There will be only one X-chromosome and no Y-chromosome.",
               "There will be three sex chromosomes: two X-chromosomes and one Y-chromosome."]),
    "2.1.4(c)": (1, ["It leads to increased genetic variation."],
                 ["It makes the gametes genetically identical to each other.", "It halves the number of chromosomes in the gametes.",
                  "It repairs damaged DNA before the cell divides.", "It ensures that every gamete receives a Y-chromosome."]),
    # the memo's two OR answers, each a point + its reason (2 ticks): either one is worth the whole 2
    "2.1.5": (2, ["The chromosomes will appear as single chromatids, due to the splitting of the centromere.",
                  "Each chromosome will have some genetic material of the other chromosome, because of crossing over."],
              ["Each chromosome will still have two chromatids, because the centromeres do not split in meiosis II.",
               "The chromosomes will be exactly as they were at the start, because no genetic material was exchanged.",
               "The number of chromatids will double, because the DNA replicates again before meiosis II."]),
    # the memo's "an extra gonosome" reading is left out: it would name 2.1.2's answer (XXY / XXX carry the same meaning)
    "2.1.6": (1, ["The zygote will have XXY or XXX sex chromosomes.", "The ovum carried two X-chromosomes (XX).",
                  "The ovum fused with a sperm carrying a Y-chromosome or an X-chromosome."],
              ["The zygote will have 45 chromosomes, as one sex chromosome is missing.",
               "The extra chromosome in the zygote is an autosome, such as an extra chromosome 21.",
               "The ovum carried no sex chromosome at all.", "Non-disjunction took place in the zygote, after fertilisation."]),
    "2.2.3": (1, ["The bands of suspect 1 are identical to the bands of the sample from the crime scene."],
              ["The bands of suspect 2 are identical to the bands of the sample from the crime scene.",
               "The bands of suspect 1 are identical to the bands of the victim's sample.",
               "Suspect 1's sample has no bands in common with the sample from the crime scene.",
               "The bands of suspect 1 are in the same places as the bands of suspect 2."]),
    "2.2.5": (1, ["The DNA profiles of the child, the mother and the possible father are compared.",
                  "The child inherits 50% of its DNA from each parent.",
                  "All the bands in the child's DNA profile that are identical to the mother's are eliminated.",
                  "The child's remaining bands are checked against the possible father's DNA profile.",
                  "A possible father whose bands match the child's remaining bands could be the father."],
              ["Only the child's DNA profile is needed to identify the father.",
               "The bands the child shares with the mother are the ones compared with the possible father.",
               "The child's DNA profile is identical to the father's DNA profile."]),
    "2.3.4": (1, ["Both individuals 1 and 2 have CADASIL.", "Individuals 1 and 2 each have a dominant allele (D).",
                  "Individuals 1 and 2 have children who do not have CADASIL (homozygous recessive).",
                  "The children without CADASIL inherited a recessive allele (d) from each parent."],
              ["Individuals 1 and 2 do not have CADASIL.", "All the children of individuals 1 and 2 have CADASIL.",
               "Individuals 1 and 2 must both be DD, since they have CADASIL.",
               "A child without CADASIL inherited a dominant allele from one parent."]),
    "2.4.4": (1, ["Allele Iᴬ is inherited from one parent.", "Allele Iᴮ is inherited from the other parent.",
                  "The alleles Iᴬ and Iᴮ are co-dominant.", "Both alleles are equally expressed in the phenotype."],
              ["Both alleles, Iᴬ and Iᴮ, are inherited from the same parent.",
               "Allele Iᴬ is dominant over allele Iᴮ, so only blood group A is expressed.",
               "Blood group AB is caused by a new mutation in every generation."]),
    "2.5.2": (1, ["Neither the allele for a cream-coloured coat nor the allele for a chestnut-coloured coat is dominant.",
                  "The heterozygous horse shows an intermediate phenotype, the golden-coloured (palomino) coat."],
              ["The allele for a cream-coloured coat is dominant over the allele for a chestnut-coloured coat.",
               "Both colours show at the same time, as patches of cream and chestnut hair.",
               "The golden coat is caused by a third allele that neither parent carries."]),
    # three features, each with its significance (2 ticks a feature): the memo has exactly three
    "3.1.3": (2, ["The foramen magnum is in a more forward position, to allow the vertebral column to attach below it.",
                  "The spine is S-shaped, for better distribution of the upper body weight.",
                  "The pelvis is short and wide, to support the weight of the upper body."],
              ["The foramen magnum is in a more backward position, to allow the vertebral column to attach behind the skull.",
               "The spine is C-shaped, to keep the upper body bent forward over the hips.",
               "The pelvis is long and narrow, to support the weight of the upper body."]),
    "3.2.5": (1, ["The cranium becomes fossilised.", "The cranium houses the brain.", "Measuring the cranial capacity gives the brain volume."],
              ["The brain itself becomes fossilised, so its volume can be measured directly.",
               "The brain volume is found from the size of the foramen magnum.",
               "The brain volume is calculated by counting the teeth in the jaw."]),
    "3.2.6": (1, ["Brain volume increased over time.", "A larger brain led to more intelligence.",
                  "More intelligence led to the development of complex tools."],
              ["Brain volume decreased over time.", "Larger brains led to the loss of tool use.",
               "Brain volume has no link with the development of tools."]),
    "3.3.1(a)": (1, ["A biological species is a group of organisms with similar characteristics.",
                     "The members of a biological species can interbreed to produce fertile offspring."],
                 ["A biological species is any group of organisms that live in the same habitat.",
                  "The members of a biological species can interbreed, but always produce infertile offspring.",
                  "The members of a biological species cannot interbreed with each other."]),
    "3.3.1(b)": (1, ["They breed at different times of the year: ostriches lay eggs mainly in September, emus from November to April.",
                     "The ostrich and the emu cannot interbreed."],
                 ["Ostriches and emus lay their eggs in the same months of the year.",
                  "Emus lay their eggs mainly in September, while ostriches lay theirs from November to April.",
                  "The ostrich and the emu produce fertile offspring when they mate."]),
    "3.3.3": (1, ["The ratites all had one common ancestor.", "The continents drifted apart (continental drift).",
                  "The population of ratites was separated.", "The sub-populations were faced with different environmental conditions.",
                  "The sub-populations underwent natural selection independently.", "The sub-populations formed different species."],
              ["Each ratite species arose separately, with no common ancestor.",
               "The ratites flew between the continents and kept interbreeding."]),
    "3.4.2": (1, ["They measured the time it took for 80% of the flies to die from starvation."],
              ["They counted the eggs laid by each generation.", "They measured the mass of food the flies ate every hour.",
               "They measured the time it took for the eggs to hatch.", "They counted how many flies were still alive after one hour."]),
    "3.4.4": (1, ["To improve the validity of the investigation.",
                  "To ensure that the availability of food is the only independent variable.",
                  "So that any changes are only due to the availability of food."],
              ["So that the type of food becomes the independent variable.", "To make sure that the flies never run out of food.",
               "To test which type of food the flies prefer."]),
    "3.4.5": (1, ["In the 1st generation the hours until death were shorter: between 8 and 40 hours.",
                  "In the 60th generation the hours until death were longer: between 140 and 180 hours."],
              ["In the 1st generation the hours until death were between 140 and 180 hours.",
               "The flies of the 60th generation died sooner than those of the 1st generation.",
               "Both generations took the same time to die from starvation."]),
    # 6 of the memo's 7 points ("Any"): all 7 fill the 8 cards with one wrong (the 8-card limit): the Lamarckian slip
    "3.4.6": (1, ["There was variation in the population of fruit flies.", "Some flies were starvation resistant, while others were not.",
                  "The food source was removed.", "The flies that were not starvation resistant died.",
                  "The starvation-resistant flies survived and reproduced.",
                  "The survivors passed on the allele for starvation resistance to their offspring.",
                  "The next generation had a higher proportion of starvation-resistant flies."],
              ["The flies became starvation resistant during their lives because they needed to, and passed this on."]),
}
# A written part whose memo weighs two sides plays as a SORT (variety): 3.1.2's differences set a human feature against an ape's
# (each side ticked: 2 x 2). Its 4 marks are 4 rows = two whole differences of the memo (the jaws, the palate), each row sorted to its
# side, 1 mark a row. No "Not true" row: a fifth row would need a fifth mark, and a false row in place of one side would break a pair.
SORTS = {
    "3.1.2": (["Humans", "African apes"], [
        ("The jaws are smaller.", 0), ("The jaws are larger.", 1), ("The palate is C-shaped.", 0), ("The palate is U-shaped.", 1)]),
}


def sort_(n, q, marks, bins, rows, clues):
    order = list(range(len(rows)))
    random.Random(PID + ":sort:" + n).shuffle(order)
    rows = [rows[i] for i in order]
    assert marks == len(rows) and len(set(b for _, b in rows)) == len(bins), n
    return {"t": "match", "n": n, "marks": marks, "q": q + " Sort each statement.", "clues": clues, "left": [r for r, _ in rows],
            "right": bins, "a": [b for _, b in rows], "heads": ["STATEMENTS", "SORT INTO"], "groups": True}


# GATES: a part whose statements show an earlier part's answer opens only once that part is answered: 2.1.5 names crossing over
# (2.1.4(a)); 2.1.6's sperm carrying a Y-chromosome shows a male's XY (2.1.3); 2.2.3 names suspect 1 (2.2.2); 2.2.5 names DNA
# profiles (2.2.1); 2.3.4's children without CADASIL are homozygous recessive, as individual 5 is (2.3.3(b)); 2.5.2's 'neither allele
# is dominant ... intermediate phenotype' is incomplete dominance (2.5.1); 3.4.4 names the availability of food as the independent
# variable (3.4.1).
GATES = {"2.1.5": ["2.1.4(a)"], "2.1.6": ["2.1.3"], "2.2.3": ["2.2.2"], "2.2.5": ["2.2.1"], "2.3.4": ["2.3.3(b)"], "2.5.2": ["2.5.1"],
         "3.4.4": ["3.4.1"]}
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
_ORDER = [i["n"] for i in _ITEMS]
assert all(_ORDER.index(e) < _ORDER.index(n) for n, g in GATES.items() for e in g), "a gate names a later part"
for _m in missions + missions_b:
    assert sum(i["marks"] for i in _m["items"]) == _m["marks"], _m["id"]

paper = {
    "catalog": "https://nexera.app/catalogs/exam/v1",
    "paper": {"subject": "Life Sciences", "title": "Life Sciences P2", "sitting": "November 2025", "total_marks": 150, "time": "2½ hours"},
    "sections": [{"title": "Section A", "total": 50, "missions": missions}, {"title": "Section B", "total": 100, "missions": missions_b}],
    "flags": [
        {"n": "3.4", "kind": "no_fit", "detail": "The question prints TWO figures: the procedure diagram (page 16: a container of flies, food removed, food returned, a new generation) and the results graphs (page 17). A mission holds one figure: the graphs are kept (3.4.5 reads them); the procedure diagram repeats the printed procedure and is left out."},
        {"n": "3.4.4", "kind": "memo_issue", "detail": "The memo's third point reads 'so that any changes that occur are only due to food availability ✓ of food' (a repeated 'of food'); transcribed as 'only due to the availability of food'."},
        {"n": "paper", "kind": "low_confidence", "detail": "The whole paper (Questions 1 to 3), hand-transcribed from the paper and memo PDFs; no API call."},
        {"n": "2.1.3", "kind": "no_fit", "detail": "Written answers play as statements (Murci, 2026-10-10): " + ", ".join(STATEMENTS) + " pick the "
                                                   "memo's points among clearly wrong ones, 1 mark a tick (2.1.5 and 3.1.3: 2 a point, as the "
                                                   "memo ticks the point and its reason). 2.1.5's two OR answers are both right statements, "
                                                   "either worth the whole 2. 3.4.6 (any 6 of 7) fills the 8-card limit with the memo's 7 "
                                                   "points and ONE wrong statement."},
        {"n": "3.1.2", "kind": "no_fit", "detail": "The differences play as a sort into Humans and African apes: 4 rows, two whole differences "
                                                   "of the memo (the jaws, the palate), 1 mark a row as the memo ticks each side. No 'Not true' "
                                                   "row: it would need a fifth mark or break a pair."},
        {"n": "3.2.4", "kind": "no_fit", "detail": "The calculation plays as a whole-working multiple choice: the memo's working and three "
                                                   "workings built from learner errors (dividing by the new volume, reading Homo erectus' 959 "
                                                   "for Homo sapiens, rounding the fraction too early); all 3 marks or none."},
        {"n": "2.5.2", "kind": "memo_issue", "detail": "The memo reads 'Neither the allele of a cream-coloured coat and chestnut-coloured coat is "
                                                       "dominant'; the statement reads 'Neither ... nor ...'."},
    ],
}
out = Path(__file__).parent / "out" / "ls-p2-2025-11"
out.mkdir(parents=True, exist_ok=True)
(out / "response.json").write_text(json.dumps({"meta": {"transcribed": "by hand from the question paper and memo PDFs (no API call)", "scope": "Questions 1 to 3 (the whole paper)"},
                                               "paper": paper}, indent=1, ensure_ascii=False), encoding="utf-8")
for sec in paper["sections"]:
    print(sec["title"], "parts:", sum(len(m["items"]) for m in sec["missions"]), "marks:", sum(i["marks"] for m in sec["missions"] for i in m["items"]))
