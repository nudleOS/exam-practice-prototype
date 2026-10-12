"""Every drawing question as "pick the drawing" (Murci, 2026-10-12): {(paper id, part number): the options}. The right drawing is
the memo's; each wrong one is a mistake the memo names or marks down (the field of two like charges, a branched chain, a curve
not parallel, the wrong reagent). The words of each option are what a screen reader reads and what the review writes; they
describe the drawing, never judge it. apply() turns a "draw" item into an "mcq" with `pics`, its marks kept (0 or full, as the
calculation MCQs); the right options are spread over A-D."""
import drawings as D

RIGHT_AT = {}   # (paper, part) -> index of the right option, filled by opt()


def same_canvas(svgs):
    """The options of one part on ONE canvas size, each centred: an image fills its card's width, so a narrower drawing (a molecule
    with no end H) came out bigger than the others and stood out by its size alone."""
    import re
    dims = [tuple(float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups()) for s in svgs]
    W, Hh = max(w for w, _ in dims), max(h for _, h in dims)
    out = []
    for s, (w, h) in zip(svgs, dims):
        inner = s[s.index(">") + 1:s.rindex("</svg>")].replace(D.ARROW, "", 1)
        out.append(D.svg(W, Hh, D.G(inner, (W - w) / 2, (Hh - h) / 2)))
    return out


def opt(key, right, wrongs, at):
    """right / wrongs: (words, svg); `at`: where the right one goes (0-3)."""
    items = list(wrongs)
    items.insert(at, right)
    RIGHT_AT[key] = at
    return {"opts": [w for w, _ in items], "pics": same_canvas([s for _, s in items]), "a": at}


def m(name):
    return D.mol_svg(D.MOLS[name])


def eq(left, extra, right, rextra):
    return D.equation_svg(D.MOLS[left], extra, D.MOLS[right], rextra)


PICS = {}


def add(paper, n, right, wrongs, at):
    PICS[(paper, n)] = opt((paper, n), right, wrongs, at)


# ---- Physical Sciences P2 Nov 2024: structural formulae
add("ps-p2-2024-11", "2.4.3",
    ("CH₃–C(=O)–O–CH₂–CH₂–CH₃, every atom and bond drawn", m("propyl ethanoate")),
    [("CH₃–CH₂–CH₂–C(=O)–O–CH₃, every atom and bond drawn", m("methyl butanoate")),
     ("CH₃–CH₂–CH₂–CH₂–C(=O)–O–H, every atom and bond drawn", m("pentanoic acid")),
     ("CH₃–C(=O)–O–CH₂–CH–CH₃ with one H missing on the fifth carbon", m("propyl ethanoate, an H missing"))], 0)
add("ps-p2-2024-11", "4.3.1",
    ("CH₃–CH₂–CH₂–CH₃, a chain of four carbons, every H drawn", m("butane")),
    [("CH₂=CH–CH₂–CH₃, a double bond on the first carbon", m("but-1-ene")),
     ("CH₃–CH(CH₃)–CH₃, three carbons in the chain and one branch", m("2-methylpropane")),
     ("CH₃–CH–CH₂–CH₃ with one H missing on the second carbon", m("butane, an H missing"))], 1)
add("ps-p2-2024-11", "4.6.1",
    ("CH₂=CH–CH₂–CH₃ + HBr → CH₃–CHBr–CH₂–CH₃", eq("but-1-ene", "+ HBr", "2-bromobutane", "")),
    [("CH₂=CH–CH₂–CH₃ + H₂O → CH₃–CH(OH)–CH₂–CH₃", eq("but-1-ene", "+ H₂O", "butan-2-ol", "")),
     ("CH₂=CH–CH₂–CH₃ + Br₂ → CH₂Br–CHBr–CH₂–CH₃", eq("but-1-ene", "+ Br₂", "1,2-dibromobutane", "")),
     ("CH₃–CH=CH–CH₃ + HBr → CH₃–CHBr–CH₂–CH₃", eq("but-2-ene", "+ HBr", "2-bromobutane", ""))], 2)
add("ps-p2-2024-11", "4.6.2",
    ("CH₃–CHBr–CH₂–CH₃ + NaOH → CH₃–CH=CH–CH₃ + NaBr + H₂O", eq("2-bromobutane", "+ NaOH", "but-2-ene", "+ NaBr + H₂O")),
    [("CH₃–CHBr–CH₂–CH₃ + NaOH → CH₃–CH(OH)–CH₂–CH₃ + NaBr", eq("2-bromobutane", "+ NaOH", "butan-2-ol", "+ NaBr")),
     ("CH₃–CHBr–CH₂–CH₃ + NaOH → CH₃–CH=CH–CH₃ + NaBr", eq("2-bromobutane", "+ NaOH", "but-2-ene", "+ NaBr")),
     ("CH₃–CHBr–CH₂–CH₃ + NaOH → CH₃–CH₂–CH₂–CH₃ + NaBr + H₂O", eq("2-bromobutane", "+ NaOH", "butane", "+ NaBr + H₂O"))], 3)
add("ps-p2-2024-11", "5.1.4",
    ("Curve B steeper than A all the way, levelling off at the same volume", D.rate_curves("right")),
    [("Curve B steeper than A, levelling off at a bigger volume", D.rate_curves("more_gas")),
     ("Curve B less steep than A, levelling off at the same volume", D.rate_curves("flatter")),
     ("Curve B steeper than A, levelling off at a smaller volume", D.rate_curves("less_gas"))], 0)

# ---- Physical Sciences P2 Nov 2025
add("ps-p2-2025-11", "2.2.4",
    ("1: HO–CH₂–CH₂–CH₂–CH₃; 2: CH₃–CH(OH)–CH₂–CH₃", D.stack_svg([("1", D.MOLS["butan-1-ol"]), ("2", D.MOLS["butan-2-ol"])])),
    [("1: HO–CH₂–CH₂–CH₂–CH₃; 2: HO–CH₂–CH(CH₃)–CH₃", D.stack_svg([("1", D.MOLS["butan-1-ol"]), ("2", D.MOLS["2-methylpropan-1-ol"])])),
     ("1: HO–CH₂–CH₂–CH₂–CH₃; 2: CH₃–CH₂–CH₂–CHO", D.stack_svg([("1", D.MOLS["butan-1-ol"]), ("2", D.MOLS["butanal"])])),
     ("1: CH₃–CH(OH)–CH₂–CH₃; 2: CH₃–CH₂–CH(OH)–CH₃", D.stack_svg([("1", D.MOLS["butan-2-ol"]), ("2", D.MOLS["butan-2-ol, mirrored"])]))], 1)
add("ps-p2-2025-11", "3.3.1",
    ("CH₃–CH₂–CH₂–C(=O)–O–H, every atom and bond drawn", m("butanoic acid")),
    [("CH₃–CH₂–C(=O)–O–CH₃, every atom and bond drawn", m("methyl propanoate")),
     ("CH₃–CH₂–CH₂–C(=O)–H, every atom and bond drawn", m("butanal")),
     ("CH₃–CH(CH₃)–C(=O)–O–H, a branched chain", m("2-methylpropanoic acid"))], 2)
add("ps-p2-2025-11", "4.1.5",
    ("CH₃–CH=CH–CH₃, the double bond between the second and third carbons", m("but-2-ene")),
    [("CH₂=CH–CH₂–CH₃, the double bond on the first carbon", m("but-1-ene")),
     ("CH₃–CH₂–CH₂–CH₃, no double bond", m("butane")),
     ("CH₂=C(CH₃)–CH₃, a branched chain", m("2-methylpropene"))], 3)
add("ps-p2-2025-11", "4.2.3",
    ("CH₂=CH–CH₃, every atom and bond drawn", m("propene")),
    [("CH₃–CH₂–CH₃, no double bond", m("propane")),
     ("CH₂=CH₂, two carbons", m("ethene")),
     ("CH₂=C–CH₃ with the H on the second carbon missing", m("propene, an H missing"))], 0)
add("ps-p2-2025-11", "5.3.5",
    ("Curve Y higher than X, its peak at the same kinetic energy", D.maxwell("right")),
    [("Curve Y's peak moved to a higher kinetic energy and lower", D.maxwell("shifted")),
     ("Curve Y lower than X, its peak at the same kinetic energy", D.maxwell("lower")),
     ("Curve Y higher, its peak moved to a lower kinetic energy", D.maxwell("shifted_left"))], 1)

# ---- Physical Sciences P1 Nov 2024
add("ps-p1-2024-11", "2.2",
    ("T to the right, fs to the left", D.fbd([("T", 0, 80), ("fs", 180, 80)])),
    [("T to the right only", D.fbd([("T", 0, 80)])),
     ("T to the left and fs to the right", D.fbd([("T", 180, 80), ("fs", 0, 80)])),
     ("T to the right, fs to the left and an extra force F", D.fbd([("T", 0, 80), ("fs", 180, 80), ("F", 30, 70)]))], 2)
add("ps-p1-2024-11", "3.2",
    ("A from 12 at 0 s, B from −5,4 at 2 s, parallel, both ending at 4 s", D.vt_balls("right")),
    [("B from +5,4 at 2 s", D.vt_balls("b_up")),
     ("B from −5,4 at 0 s", D.vt_balls("b_zero")),
     ("B a horizontal line at −5,4", D.vt_balls("b_flat"))], 3)
add("ps-p1-2024-11", "5.2",
    ("w down, N up, f to the left, F at 30° above the horizontal", D.fbd([("w", 270, 78), ("N", 90, 62), ("f", 180, 70), ("F", 30, 82)])),
    [("w down, N up, f to the left, F drawn as two components", D.fbd([("w", 270, 78), ("N", 90, 62), ("f", 180, 70), ("Fx", 0, 70), ("Fy", 90, 34, (22, 30))])),
     ("w down, N up, f to the right, F at 30°", D.fbd([("w", 270, 78), ("N", 90, 62), ("f", 0, 50), ("F", 30, 82)])),
     ("w down, f to the left, F at 30°, no N", D.fbd([("w", 270, 78), ("f", 180, 70), ("F", 30, 82)]))], 0)
add("ps-p1-2024-11", "7.2",
    ("Lines from P to S, curving between and around them, never crossing", D.dipole("right")),
    [("Lines from S to P", D.dipole("reversed")),
     ("Lines pushing apart between P and S, as for two like charges", D.dipole("like")),
     ("Lines from P to S with two lines crossing", D.dipole("crossing"))], 1)

# ---- Physical Sciences P1 Nov 2025
add("ps-p1-2025-11", "2.2",
    ("w down, N up, fs to the left, F up at θ to the right", D.fbd([("w", 270, 78), ("N", 90, 60), ("fs", 180, 70), ("F", 34, 84)])),
    [("w down, N up, fs to the right, F at θ", D.fbd([("w", 270, 78), ("N", 90, 60), ("fs", 0, 46), ("F", 34, 84)])),
     ("w down, fs to the left, F at θ, no N", D.fbd([("w", 270, 78), ("fs", 180, 70), ("F", 34, 84)])),
     ("w down, N up, fs to the left, F at θ and an extra force Fnet", D.fbd([("w", 270, 78), ("N", 90, 60), ("fs", 180, 70), ("F", 34, 84), ("Fnet", 0, 50)]))], 2)
add("ps-p1-2025-11", "3.5",
    ("From 15 down to −17,97, through 0 at 1,53 s; after the bounce a slower parallel line ending at 0", D.vt_bounce("right")),
    [("After the bounce a line that is not parallel", D.vt_bounce("not_parallel")),
     ("After the bounce a line starting faster than 17,97", D.vt_bounce("faster_bounce")),
     ("A line starting at 0", D.vt_bounce("starts_zero"))], 3)
add("ps-p1-2025-11", "4.3",
    ("B parallel to A, shifted to the right", D.pf_dt("right")),
    [("B parallel to A, shifted to the left", D.pf_dt("left")),
     ("B steeper than A", D.pf_dt("steeper")),
     ("B less steep than A", D.pf_dt("flatter"))], 0)
add("ps-p1-2025-11", "5.3",
    ("w straight down, f up the slope, N at right angles to the slope", D.fbd([("w", 270, 80), ("f", 160, 70), ("N", 70, 64)], surface=-20)),
    [("w straight down, f up the slope, N straight up", D.fbd([("w", 270, 80), ("f", 160, 70), ("N", 90, 64)], surface=-20)),
     ("w straight down, f down the slope, N at right angles to the slope", D.fbd([("w", 270, 80), ("f", 340, 70), ("N", 70, 64)], surface=-20)),
     ("w at right angles to the slope, f up the slope, N at right angles to the slope", D.fbd([("w", 250, 80), ("f", 160, 70), ("N", 70, 64)], surface=-20))], 1)
add("ps-p1-2025-11", "7.2",
    ("Lines straight out from X, arrows pointing away", D.radial("right")),
    [("Lines straight in to X, arrows pointing towards it", D.radial("inwards")),
     ("Two charges drawn", D.radial("two")),
     ("Field lines drawn as circles round X", D.radial("circles"))], 2)
add("ps-p1-2025-11", "9.4",
    ("B: one cosine cycle with a bigger amplitude, over half A's period", D.generator_vt("right")),
    [("B: the same amplitude as A, over half the period", D.generator_vt("same_amp")),
     ("B: a bigger amplitude over the same period as A", D.generator_vt("same_period")),
     ("B: a sine curve with a bigger amplitude over half the period", D.generator_vt("sine"))], 3)

# ---- Mathematics, Mathematical Literacy
add("math-p1-2024-11", "11.1",
    ("M only 11, T only 6, G only 9; M and T 5, M and G 4, T and G 3; all three 2",
     D.venn3({"M": 11, "T": 6, "G": 9, "MT": 5, "MG": 4, "TG": 3, "MTG": 2})),
    [("M only 22, T only 16, G only 18; M and T 5, M and G 4, T and G 3; all three 2",
      D.venn3({"M": 22, "T": 16, "G": 18, "MT": 5, "MG": 4, "TG": 3, "MTG": 2})),
     ("M only 11, T only 6, G only 9; M and T 5, M and G 3, T and G 4; all three 2",
      D.venn3({"M": 11, "T": 6, "G": 9, "MT": 5, "MG": 3, "TG": 4, "MTG": 2})),
     ("M only 13, T only 8, G only 11; M and T 5, M and G 4, T and G 3; none in all three",
      D.venn3({"M": 13, "T": 8, "G": 11, "MT": 5, "MG": 4, "TG": 3, "MTG": 0}))], 0)
add("math-p2-2025-11", "2.1.3",
    ("Bars 16, 24, 19, 8, 3, touching", D.histogram("right")),
    [("Bars 16, 24, 19, 8, 3 with gaps between them", D.histogram("gaps")),
     ("Bars of the cumulative frequencies 16, 40, 59, 67, 70", D.histogram("cumulative")),
     ("Bars 16, 19, 24, 8, 3, touching", D.histogram("swapped"))], 1)
add("ml-p1-2024-11", "4.1.2(b)",
    ("Flat at R4 000 from 0 to 5 hours, then a straight rise to R9 000 at 9 hours", D.dj_line("right")),
    [("A rise from R0 at 0 hours to R4 000 at 5 hours, then to R9 000", D.dj_line("from_zero")),
     ("Flat at R4 000 to 4 hours, then a straight rise to R9 000", D.dj_line("flat_four")),
     ("Flat at R4 000 to 5 hours, then a step for each hour", D.dj_line("steps"))], 2)
add("ml-p1-2025-11", "3.2.3",
    ("The 2023 parts on top: KZN up to 31 500 000, Mpumalanga up to 14 000 000", D.lte_bars("right")),
    [("The 2023 values as separate bars from 0", D.lte_bars("from_zero")),
     ("The 2023 totals added on top of the 2022 bars", D.lte_bars("added_on")),
     ("The 2023 parts on top, each 4 000 000 short", D.lte_bars("short"))], 3)
add("ml-p2-2025-11", "5.1.3(b)",
    ("A rectangle 3 cm wide and 4,5 cm high", D.hardboard("right")),
    [("A rectangle 6 cm wide and 9 cm high", D.hardboard("ten")),
     ("A rectangle 4,5 cm wide and 3 cm high", D.hardboard("turned")),
     ("A rectangle 3 cm wide and 4 cm high", D.hardboard("four"))], 0)

# ---- Geography, Life Sciences
add("geo-p1-2024-11", "1.4.4",
    ("Towering cumulonimbus on both sides of a clear eye, the air in the eye sinking", D.cyclone("right")),
    [("Cumulonimbus on both sides of the eye, the air in the eye rising", D.cyclone("rising")),
     ("Cumulonimbus across the centre, no eye", D.cyclone("no_eye")),
     ("Flat stratus layers on both sides of the eye", D.cyclone("stratus"))], 1)
add("geo-p1-2025-11", "1.3.5",
    ("Cold air undercutting warm air along a steep front, cumulonimbus, moving west to east, the cold sector named", D.cold_front("right")),
    [("Warm air rising gently over cold air, stratus", D.cold_front("warm_front")),
     ("The steep front moving east to west", D.cold_front("east_to_west")),
     ("Warm air undercutting cold air", D.cold_front("warm_under"))], 2)
add("geo-p2-2025-11", "3.3.3",
    ("Layer C with the woodland, the row of trees and the non-perennial water", D.gis_layer("right")),
    [("Layer C with the woodland and the row of trees, no water", D.gis_layer("no_water")),
     ("Layer C with the woodland and the water, no row of trees", D.gis_layer("no_trees")),
     ("Layer C with the row of trees and the water, no woodland", D.gis_layer("no_woodland"))], 3)
add("ls-p2-2024-11", "2.2.5",
    ("Two chromosomes in one row at the equator: one shaded with an unshaded tip, one unshaded with a shaded tip",
     D.metaphase2("right")),
    [("Four chromosomes in one row at the equator", D.metaphase2("four")),
     ("Chromosomes in two rows, either side of the equator", D.metaphase2("two_rows")),
     ("Two chromosomes in one row, one shaded and one unshaded, no tips", D.metaphase2("no_tips"))], 0)


def apply(pid, paper):
    """The paper's "draw" items listed here become "pick the drawing" MCQs (their marks and clues kept). Returns their numbers."""
    done = []
    for sec in paper["sections"]:
        for mi in sec["missions"]:
            for i, it in enumerate(mi["items"]):
                p = PICS.get((pid, it["n"]))
                if not p:
                    continue
                if it["t"] != "draw":
                    raise SystemExit(f"{pid} {it['n']}: pictures for a part that is not a drawing ({it['t']})")
                new = {k: it[k] for k in ("n", "marks", "q", "clues", "after", "figure") if k in it}
                new.update({"t": "mcq", "opts": p["opts"], "pics": p["pics"], "a": p["a"]})
                new["q"] = it["q"].rstrip() + "\n\nChoose the drawing the examiner would accept."
                mi["items"][i] = new
                done.append(it["n"])
    want = sorted(n for (p, n) in PICS if p == pid)
    if sorted(done) != want:
        raise SystemExit(f"{pid}: pictures for {want}, found drawings for {sorted(done)}")
    return done
