"""Pick the drawing for the provincial Grade 10 and 11 papers (2026-10-12), as pictures.py does for Grade 12: each drawing
question an MCQ of four drawings, the memo's and three mistakes the memo marks down. The drawings are built here from
drawings.py's primitives (no script, no link, no image: shown through an <img>). register(add) is called at the end of
pictures.py, so ingest.py --from-json and apply_pictures.py see these parts like any other."""
import drawings as D
from drawings import L, P, T, axes, poly, svg

# ---------------------------------------------------------------- an ogive (cumulative frequency graph)


def ogive(uppers, cums, lower0, variant, xlab="x", ylab="Cumulative frequency", xstep=None, ystep=5):
    """An ogive on a grid: `uppers` the class upper limits, `cums` their cumulative frequencies, `lower0` the first lower limit
    (the grounding point). variant: right (grounded, plotted at the upper limits, joined smoothly) | lower (plotted at the
    lower limits) | float (not grounded) | freq (the frequencies, not the cumulative ones, plotted at the upper limits)."""
    width = uppers[1] - uppers[0]
    xs, ys = list(uppers), list(cums)
    if variant == "lower":
        xs = [u - width for u in uppers]
    if variant == "freq":
        ys = [cums[0]] + [b - a for a, b in zip(cums, cums[1:])]
    pts = list(zip(xs, ys))
    if variant in ("right", "lower", "freq"):
        pts = [(lower0 - (width if variant == "lower" else 0), 0)] + pts
    x_lo, x_hi = lower0 - width, uppers[-1] + width
    top = max(cums) + (ystep - max(cums) % ystep) % ystep + ystep
    X = lambda v: 56 + (v - x_lo) * 270 / (x_hi - x_lo)
    Y = lambda n: 196 - n * 176 / top
    out = []
    for n in range(0, top + 1, ystep):   # the grid
        out.append(L(X(x_lo), Y(n), X(x_hi), Y(n), w=0.6, color="#bbb"))
    for v in range(x_lo, x_hi + 1, xstep or width):
        out.append(L(X(v), Y(0), X(v), Y(top), w=0.6, color="#bbb"))
    out.append(axes(X(x_lo), 8, X(x_hi) + 6, Y(0), xlab, "", zero=False))
    for n in range(0, top + 1, ystep):
        out.append(T(X(x_lo) - 5, Y(n) + 4, str(n), size=10, anchor="end"))
    for v in range(x_lo, x_hi + 1, xstep or width):
        out.append(T(X(v), Y(0) + 14, str(v), size=10))
    out.append(T(14, 104, ylab, size=11).replace("<text ", '<text transform="rotate(-90 14 104)" ', 1))
    sp = [(X(a), Y(b)) for a, b in pts]
    out.append(P(smooth(sp), w=2.2))
    for x, y in sp:
        out.append(D.C(x, y, 3, w=1, fill=D.INK))
    return svg(340, 226, "".join(out))


def smooth(pts):
    """A smooth path through the points (Catmull-Rom as cubic Béziers), as a hand-drawn ogive is joined."""
    d = "M%.1f,%.1f" % pts[0]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return d


def venn2(a_only, both, b_only, outside, names=("A", "B"), space="S"):
    """Two overlapping circles in a rectangle, a value in each region ("" leaves a region empty)."""
    out = [D.R(8, 8, 324, 184, sw=2), D.C(130, 100, 70), D.C(210, 100, 70),
           T(80, 34, names[0], size=15), T(260, 34, names[1], size=15), T(318, 28, space, size=13, anchor="end")]
    for x, y, v in ((100, 105, a_only), (170, 105, both), (240, 105, b_only), (300, 180, outside)):
        if v != "":
            out.append(T(x, y, v, size=14))
    return svg(340, 200, "".join(out))


def tree2(first, second, outcomes):
    """A two-stage tree: first = [(event, p), (event, p)]; second = per first branch [(event, p), (event, p)]; outcomes: the four
    end labels (top to bottom) or None."""
    out, ys = [], [(40, 0), (40, 1), (150, 0), (150, 1)]
    x0, y0, x1, x2 = 14, 100, 130, 250
    mid = [52, 148]
    for i, ((ev, p), ym) in enumerate(zip(first, mid)):
        out += [L(x0, y0, x1, ym, w=1.8), T((x0 + x1) / 2 - 6, (y0 + ym) / 2 + (-8 if i == 0 else 16), p, size=12, anchor="end"),
                T(x1 + 2, ym + 5, ev, size=13, anchor="start")]
        for j, (ev2, p2) in enumerate(second[i]):
            ye = ym - 26 + 52 * j
            out += [L(x1 + 18, ym, x2, ye, w=1.8), T((x1 + 18 + x2) / 2, (ym + ye) / 2 + (-6 if j == 0 else 15), p2, size=12),
                    T(x2 + 4, ye + 5, ev2, size=13, anchor="start")]
            if outcomes:
                out.append(T(x2 + 32, ye + 5, outcomes[2 * i + j], size=11, anchor="start"))
    return svg(340, 200, "".join(out))


def register(add):
    # ---- Grade 11 Mathematics P2 Nov 2024 (EC) 2.4: the ogive of the boxers' weights (memo: grounding, upper limits, shape)
    U, CF = [55, 75, 95, 115, 135, 155], [1, 4, 13, 19, 22, 23]
    og = lambda v: ogive(U, CF, 35, v, xlab="Mass (kg)", xstep=20)
    add("g11-math-p2-2024-11-ec", "2.4",
        ("Points (35 ; 0), (55 ; 1), (75 ; 4), (95 ; 13), (115 ; 19), (135 ; 22), (155 ; 23) joined by a smooth S-shaped curve", og("right")),
        [("Points (15 ; 0), (35 ; 1), (55 ; 4), (75 ; 13), (95 ; 19), (115 ; 22), (135 ; 23): each class plotted at its lower limit",
          og("lower")),
         ("Points (55 ; 1), (75 ; 4), (95 ; 13), (115 ; 19), (135 ; 22), (155 ; 23), the curve starting at (55 ; 1)", og("float")),
         ("Points (35 ; 0), (55 ; 1), (75 ; 3), (95 ; 9), (115 ; 6), (135 ; 3), (155 ; 1): the frequencies plotted", og("freq"))], 2)

    # ---- Grade 11 Mathematics P1 Nov 2025 (EC) 9.1.2: the Venn diagram of independent A and B (memo: 0,18; 0,12 and 0,42; 0,28)
    add("g11-math-p1-2025-11-ec", "9.1.2",
        ("0,12 in A only, 0,18 in both, 0,42 in B only, 0,28 outside the circles", venn2("0,12", "0,18", "0,42", "0,28")),
        [("0,3 in A only, 0 in both, 0,6 in B only, 0,1 outside: no overlap", venn2("0,3", "0", "0,6", "0,1")),
         ("0,3 in A only, 0,18 in both, 0,6 in B only, 0,28 outside: the totals in the only-regions", venn2("0,3", "0,18", "0,6", "0,28")),
         ("0,12 in A only, 0,18 in both, 0,42 in B only, nothing outside the circles", venn2("0,12", "0,18", "0,42", ""))], 1)
    # ---- 9.3.1: the tree of sunny weather (S) and sunscreen (U) (memo: first branches, second branches, outcomes)
    S1 = [("S", "0,7"), ("S′", "0,3")]
    OUT = ["SU", "SU′", "S′U", "S′U′"]
    add("g11-math-p1-2025-11-ec", "9.3.1",
        ("S 0,7 then U x, U′ 1 − x; S′ 0,3 then U 0,2x, U′ 1 − 0,2x; outcomes SU, SU′, S′U, S′U′",
         tree2(S1, [[("U", "x"), ("U′", "1 − x")], [("U", "0,2x"), ("U′", "1 − 0,2x")]], OUT)),
        [("S 0,7 then U x, U′ 1 − x; S′ 0,3 then U x, U′ 1 − x: the same chances after not sunny",
          tree2(S1, [[("U", "x"), ("U′", "1 − x")], [("U", "x"), ("U′", "1 − x")]], OUT)),
         ("S 0,7 then U x, U′ 1 − x; S′ 0,3 then U 0,2x, U′ 0,8x",
          tree2(S1, [[("U", "x"), ("U′", "1 − x")], [("U", "0,2x"), ("U′", "0,8x")]], OUT)),
         ("S 0,7 then U x, U′ x − 1; S′ 0,3 then U 0,2x, U′ 0,2x − 1",
          tree2(S1, [[("U", "x"), ("U′", "x − 1")], [("U", "0,2x"), ("U′", "0,2x − 1")]], OUT))], 3)
