"""Pick the drawing for the provincial Grade 10 and 11 papers (2026-10-12), as pictures.py does for Grade 12: each drawing
question an MCQ of four drawings, the memo's and three mistakes the memo marks down. The drawings are built here from
drawings.py's primitives (no script, no link, no image: shown through an <img>). register(add) is called at the end of
pictures.py, so ingest.py --from-json and apply_pictures.py see these parts like any other."""
import math

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


def triangle(variant, w="W", f="Fₐ = 60 N", t="T"):
    """A closed vector diagram of three forces in equilibrium (PS P1 Nov 2024 EC 2.2): W down the left side, Fₐ along the bottom to
    the right, T closing the triangle back to the top, head to tail, θ at the top between W and T. variant: right | tails (T drawn the
    wrong way, so the arrows do not follow each other round) | open (the three forces from one point: a free-body diagram) | theta
    (θ marked at the bottom right, between Fₐ and T)."""
    A, B, Cc = (110, 30), (110, 190), (250, 190)    # top, bottom left, bottom right
    out = []
    if variant == "open":
        o = (165, 110)
        out += [L(o[0], o[1], o[0], o[1] + 85, w=2.4, arrow=True), L(o[0], o[1], o[0] + 120, o[1], w=2.4, arrow=True),
                L(o[0], o[1], o[0] - 70, o[1] - 80, w=2.4, arrow=True), D.C(o[0], o[1], 4, fill=D.INK, w=1),
                T(o[0] + 14, o[1] + 82, w, size=14, anchor="start", italic=True), T(o[0] + 118, o[1] - 10, f, size=13, anchor="end"),
                T(o[0] - 74, o[1] - 84, t, size=14, italic=True), T(o[0] - 16, o[1] - 30, "θ", size=14, italic=True)]
        return svg(330, 210, "".join(out))
    out += [L(*A, *B, w=2.4, arrow=True), L(*B, *Cc, w=2.4, arrow=True)]
    out.append(L(*A, *Cc, w=2.4, arrow=True) if variant == "tails" else L(*Cc, *A, w=2.4, arrow=True))
    out += [T(96, 115, w, size=14, anchor="end", italic=True), T(180, 208, f, size=13), T(192, 100, t, size=14, italic=True, anchor="start")]
    out.append(T(236, 178, "θ", size=14, italic=True) if variant == "theta" else T(122, 66, "θ", size=14, italic=True))
    return svg(330, 215, "".join(out))


SIDE = {"u": (0, -1), "d": (0, 1), "l": (-1, 0), "r": (1, 0)}


def lewis(atoms, bonds, w=330, h=150, extra=""):
    """A Lewis structure: atoms [(symbol, x, y, lone-pair sides "udlr")], bonds [(i, j, pairs)]: each shared pair two dots between the
    atoms (across the bond line's direction), each lone pair two dots on that side of the atom."""
    out = []
    for i, j, n in bonds:
        (_, x1, y1, _), (_, x2, y2, _) = atoms[i], atoms[j]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        px, py = -dy / ln, dx / ln               # across the bond
        ax, ay = dx / ln, dy / ln                # along the bond
        for k in range(n):
            off = (k - (n - 1) / 2) * 9
            cx, cy = mx + ax * off, my + ay * off
            for s in (-1, 1):
                out.append(D.C(cx + px * s * 4.5, cy + py * s * 4.5, 2.4, w=0, fill=D.INK))
    for sym, x, y, lone in atoms:
        out.append(T(x, y + 7, sym, size=20))
        for sd in lone:
            vx, vy = SIDE[sd]
            cx, cy = x + vx * 19, y + vy * 19
            for s in (-1, 1):
                out.append(D.C(cx + vy * s * 4.5, cy + vx * s * 4.5, 2.4, w=0, fill=D.INK))
    return svg(w, h, "".join(out) + extra)


def profile(hr, peak, hp, labels, dotted=None, dh=None):
    """A potential energy against course of reaction graph: the reactants' level hr, the peak, the products' level hp (numbers, kJ·mol⁻¹,
    drawn to scale between 0 and the top), each labelled with labels[k] at the axis ("" for none); dotted: a second (catalysed) peak;
    dh: the ΔH label beside an arrow from the reactants' level to the products'."""
    top = max(hr, peak, hp) * 1.15
    Y = lambda e: 196 - e * 176 / top
    x0, x1, x2, x3 = 70, 120, 220, 310
    out = [axes(60, 8, 318, 200, "Course of reaction", "", zero=False),
           T(16, 104, "Potential energy (kJ·mol⁻¹)", size=10).replace("<text ", '<text transform="rotate(-90 16 104)" ', 1)]

    def hump(pk, dash=None):
        return P(f"M{x0},{Y(hr):.1f} L{x1},{Y(hr):.1f} C{x1 + 30},{Y(hr):.1f} {x1 + 25},{Y(pk):.1f} {(x1 + x2) / 2},{Y(pk):.1f} "
                 f"C{x2 - 25},{Y(pk):.1f} {x2 - 30},{Y(hp):.1f} {x2},{Y(hp):.1f} L{x3},{Y(hp):.1f}", w=2.2, dash=dash)
    out.append(hump(peak))
    if dotted is not None:
        out.append(hump(dotted, dash="5 4"))
    for e, lab in zip((hr, peak, hp), labels):
        if lab:
            out += [L(60, Y(e), x3, Y(e), w=0.8, dash="2 4", color="#777"), T(56, Y(e) + 4, lab, size=10, anchor="end")]
    if dh:
        xa = x2 + 40
        out += [L(xa, Y(hr), xa, Y(hp), w=1.4, arrow=True), T(xa + 6, (Y(hr) + Y(hp)) / 2 + 4, dh, size=10, anchor="start", halo=True)]
    return svg(330, 215, "".join(out))


def boyle(variant):
    """Volume (cm³) against pressure (kPa), PS P2 Nov 2024 EC 4.5: A, the ideal gas (pV = 480), and B, the real gas at high pressure.
    variant: right (B above A at high pressure) | below (B under A at high pressure) | low (B above A at LOW pressure) | line (B a
    straight line)."""
    X = lambda p: 50 + p * 270 / 180
    Y = lambda v: 196 - v * 176 / 20
    out = [axes(50, 8, 324, 196, "Pressure (kPa)", "", zero=False),
           T(14, 104, "Volume (cm³)", size=10).replace("<text ", '<text transform="rotate(-90 14 104)" ', 1)]
    for v in range(0, 21, 4):
        out.append(T(46, Y(v) + 4, str(v), size=9, anchor="end"))
    for p in range(0, 181, 30):
        out.append(T(X(p), 208, str(p), size=9))
    pts = [(X(p), Y(480 / p)) for p in range(25, 171, 5)]
    out.append(poly(pts, w=2.2))
    out.append(T(X(172), Y(480 / 170) + 14, "A", size=12, weight=700))
    if variant == "right":
        b = [(X(p), Y(480 / p + max(0, p - 100) * 0.03)) for p in range(100, 171, 5)]
    elif variant == "below":
        b = [(X(p), Y(480 / p - max(0, p - 100) * 0.025)) for p in range(100, 171, 5)]
    elif variant == "low":
        b = [(X(p), Y(480 / p + max(0, 60 - p) * 0.12)) for p in range(25, 61, 5)]
    else:
        b = [(X(100), Y(4.8)), (X(170), Y(0.5))]
    out.append(poly(b, w=2.2, dash="5 4"))
    bx, by = b[-1] if variant != "low" else b[0]
    out.append(T(bx + 8, by + 4, "B", size=12, weight=700, anchor="start"))
    return svg(334, 215, "".join(out))


def point_field(sign, variant, label=""):
    """The field of one point charge (sign "+" or "−"): variant in (lines radially inwards, arrows towards the charge) | out (arrows away)
    | circles (field lines drawn as circles) | short (lines that stop short of the charge, not starting at it)."""
    cx, cy, out = 165, 110, []
    if variant == "circles":
        for r in (34, 58, 82):
            out += [D.C(cx, cy, r, w=1.8), D.mid_arrow(cx - 6, cy - r, cx + 6, cy - r, at=0.5)]
    else:
        r0 = 19 if variant != "short" else 48
        for k in range(8):
            a = 2 * math.pi * k / 8
            x1, y1 = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
            x2, y2 = cx + 95 * math.cos(a), cy + 95 * math.sin(a)
            out += [L(x1, y1, x2, y2, w=1.8), D.mid_arrow(x2, y2, x1, y1) if variant in ("in", "short") else D.mid_arrow(x1, y1, x2, y2)]
    out += [D.C(cx, cy, 17, fill="#fff"), T(cx, cy + 6, sign, size=18, weight=700)]
    if label:
        out.append(T(cx + 30, cy + 16, label, size=14, anchor="start", halo=True))
    return svg(330, 220, "".join(out))


def breakeven(income, b=None, xmax=110, ymax=16000, xstep=10, ystep=2000, cost=(2400, 50), xlab="Number of learners", ylab="Cost in rands"):
    """The answer sheet's graph (ML P1 Nov 2024 EC 4.1.3/4.1.4): the printed cost line (cost = a + b·n, dots every 10) and the learner's
    income line from income[0] to income[1] (two (n ; rand) points, drawn dashed-free), with point B marked when given."""
    X = lambda n: 52 + n * 268 / xmax
    Y = lambda r: 196 - r * 180 / ymax
    out = []
    for r in range(0, ymax + 1, ystep):
        out += [L(X(0), Y(r), X(xmax), Y(r), w=0.5, color="#ccc"), T(48, Y(r) + 3, f"{r:,}".replace(",", " "), size=8, anchor="end")]
    for n in range(0, xmax + 1, xstep):
        out += [L(X(n), Y(0), X(n), Y(ymax), w=0.5, color="#ccc"), T(X(n), 208, str(n), size=8)]
    out.append(axes(X(0), 6, X(xmax) + 6, Y(0), "", "", zero=False))
    a, s = cost
    out.append(L(X(0), Y(a), X(100), Y(a + s * 100), w=1.8, color="#777"))
    for n in range(0, 101, 10):
        out.append(D.C(X(n), Y(a + s * n), 2.2, w=0, fill="#777"))
    (n0, r0), (n1, r1) = income
    out.append(L(X(n0), Y(r0), X(n1), Y(r1), w=2.4))
    if b:
        out += [D.C(X(b[0]), Y(b[1]), 4, w=0, fill=D.INK), T(X(b[0]) - 6, Y(b[1]) - 8, "B", size=13, weight=700, anchor="end", halo=True)]
    out += [T(186, 222, xlab, size=9), T(12, 104, ylab, size=9).replace("<text ", '<text transform="rotate(-90 12 104)" ', 1)]
    return svg(330, 228, "".join(out))


def plot(pts, xmax, ymax, xstep, ystep, xlab, ylab, join=None, title=""):
    """Points on a grid from (0 ; 0) (a learner's graph or scatter plot on an answer sheet): join None (a scatter plot) |
    "line" (straight segments in the order given) | "smooth" (one smooth curve, in the order given); a title above when given."""
    top = 30 if title else 10
    X = lambda v: 58 + v * 262 / xmax
    Y = lambda v: 200 - v * (200 - top) / ymax
    out = []
    for v in range(0, ymax + 1, ystep):
        out += [L(X(0), Y(v), X(xmax), Y(v), w=0.5, color="#ccc"), T(52, Y(v) + 3, str(v), size=9, anchor="end")]
    for v in range(0, xmax + 1, xstep):
        out += [L(X(v), Y(0), X(v), Y(ymax), w=0.5, color="#ccc"), T(X(v), 213, str(v), size=9)]
    out.append(axes(X(0), top - 4, X(xmax) + 6, Y(0), "", "", zero=False))
    sp = [(X(a), Y(b)) for a, b in pts]
    if join == "line":
        out.append(poly(sp, w=2))
    if join == "smooth":
        out.append(P(smooth(sp), w=2.2))
    for x, y in sp:
        out.append(D.C(x, y, 3.2, w=0, fill=D.INK))
    if title:
        out.append(T(189, 16, title, size=10, weight=700))
    out += [T(189, 228, xlab, size=10), T(14, (top + 200) / 2, ylab, size=10).replace("<text ", '<text transform="rotate(-90 14 %g)" '
                                                                                       % ((top + 200) / 2), 1)]
    return svg(340, 234, "".join(out))


def bars(labels, values, ymax, ystep, xlab, ylab, title="", line=False):
    """A bar graph of one value per category (a learner's 'histogram' of a table), or, with line=True, the same values joined as a
    line graph; a title above when given (the memo's caption mark)."""
    top = 30 if title else 10
    n = len(labels)
    X = lambda i: 58 + (i + 0.5) * 262 / n
    Y = lambda v: 200 - v * (200 - top) / ymax
    out = []
    for v in range(0, ymax + 1, ystep):
        out += [L(58, Y(v), 320, Y(v), w=0.5, color="#ccc"), T(52, Y(v) + 3, str(v), size=9, anchor="end")]
    out.append(axes(58, top - 4, 326, Y(0), "", "", zero=False))
    bw = 262 / n * 0.55
    for i, (lab, v) in enumerate(zip(labels, values)):
        if not line:
            out.append(f'<rect x="{X(i) - bw / 2:.1f}" y="{Y(v):.1f}" width="{bw:.1f}" height="{Y(0) - Y(v):.1f}" fill="#9aa4b1" stroke-width="1.2"/>')
        out.append(T(X(i), 213, lab, size=10))
    if line:
        out.append(poly([(X(i), Y(v)) for i, v in enumerate(values)], w=2))
        out += [D.C(X(i), Y(v), 3.2, w=0, fill=D.INK) for i, v in enumerate(values)]
    if title:
        out.append(T(189, 16, title, size=9.5, weight=700))
    if xlab:
        out.append(T(189, 228, xlab, size=10))
    if ylab:
        out.append(T(14, (top + 200) / 2, ylab, size=9).replace("<text ", '<text transform="rotate(-90 14 %g)" ' % ((top + 200) / 2), 1))
    return svg(340, 234, "".join(out))


def bacterium(variant):
    """A labelled bacterium (a learner's drawing of 'micro-organism X'): right (cell wall, cell membrane, cytoplasm, ribosomes,
    nucleoid, plasmid, flagellum, captioned) | bare (the outline only: no labels, no caption) | nucleus (a nucleus and a
    mitochondrion drawn in, as for a eukaryote) | virus (a virus: a protein coat round DNA, tail fibres)."""
    out = []
    lab = lambda x0, y0, x1, y1, s, anchor="start": [L(x0, y0, x1, y1, w=1), T(x1 + (4 if anchor == "start" else -4), y1 + 4, s, size=11,
                                                                               anchor=anchor)]
    if variant == "virus":
        out += [P("M150,40 L195,65 L195,115 L150,140 L105,115 L105,65 Z", w=2.2), P("M130,80 q10,-12 20,0 t20,0 M128,100 q10,12 22,0 t22,0",
                                                                                      w=1.6),
                L(150, 140, 150, 185, w=3), L(150, 185, 120, 205, w=1.5), L(150, 185, 180, 205, w=1.5)]
        out += lab(195, 70, 245, 55, "Protein coat") + lab(165, 90, 245, 95, "DNA") + lab(152, 170, 245, 160, "Tail")
        out.append(T(170, 222, "Structure of micro-organism X", size=12, weight=700))
        return svg(340, 234, "".join(out))
    out += [P("M80,70 h140 a45,45 0 0 1 0,90 h-140 a45,45 0 0 1 0,-90 Z", w=2.4), P("M84,78 h132 a37,37 0 0 1 0,74 h-132 a37,37 0 0 1 0,-74 Z",
                                                                                      w=1.2),
            P("M265,115 q15,-14 30,0 t30,0", w=1.6)]
    if variant != "nucleus":
        out += [P("M110,105 q15,-15 30,0 t30,0 t30,0 M118,125 q15,15 30,0 t30,0", w=1.6), D.C(205, 135, 9, w=1.4)]
    for x, y in [(100, 95), (120, 140), (175, 90), (235, 100), (230, 140), (160, 145)]:
        out.append(D.C(x, y, 2, w=0, fill=D.INK))
    if variant == "nucleus":
        out += [D.C(150, 115, 22, w=1.8), D.C(150, 115, 6, w=0, fill=D.INK), P("M190,125 h40 a10,10 0 0 1 0,20 h-40 a10,10 0 0 1 0,-20 Z", w=1.4)]
        out += lab(150, 93, 150, 40, "Nucleus") + lab(225, 140, 250, 195, "Mitochondrion") + lab(85, 72, 30, 30, "Cell wall")
        out.append(T(170, 222, "Structure of micro-organism X", size=12, weight=700))
        return svg(340, 234, "".join(out))
    if variant == "right":
        out += lab(95, 70, 60, 40, "Cell wall", "end") + lab(150, 78, 150, 40, "Cell membrane") + lab(175, 90, 240, 40, "Ribosome")
        out += lab(140, 105, 70, 205, "Nucleoid (DNA)") + lab(205, 144, 210, 205, "Plasmid") + lab(300, 112, 325, 70, "Flagellum", "end")
        out += lab(120, 140, 20, 185, "Cytoplasm")
        out.append(T(170, 226, "Structure of a bacterium", size=12, weight=700))
    return svg(340, 234, "".join(out))


def pie(values, labels, title=""):
    """A pie chart of percentages (one sector each, clockwise from 12 o'clock), each sector labelled with its name and value;
    a title above when given."""
    import math
    cx, cy, r = 100, 128, 80
    fills = ["#5b6573", "#9aa4b1", "#c9d0d8", "#eef1f4"]
    out, a = [], -90.0
    for k, (v, name) in enumerate(zip(values, labels)):
        b = a + v * 3.6
        x0, y0 = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        x1, y1 = cx + r * math.cos(math.radians(b)), cy + r * math.sin(math.radians(b))
        out.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 {1 if b - a > 180 else 0} 1 {x1:.1f},{y1:.1f} Z" fill="{fills[k % 4]}" '
                   f'stroke-width="1.4"/>')
        out += [f'<rect x="190" y="{60 + k * 26}" width="12" height="12" fill="{fills[k % 4]}" stroke-width="1"/>',
                T(206, 70 + k * 26, f"{name} {str(v).replace('.', ',')}%", size=9, anchor="start")]
        a = b
    if title:
        out.append(T(180, 18, title, size=10, weight=700))
    return svg(360, 234, "".join(out))


def register(add):
    # ---- Grade 11 Life Sciences P2 Nov 2025 (EC) 3.3.4: the rate of photosynthesis in the groups WITH microplastics (B, C, D; memo:
    # type, caption, labels with units, scale and equal bars, the plotted values)
    MT = "Rate of photosynthesis for different groups of microplastics"
    mb = lambda labs, vals, title=MT, xl="Groups", yl="Rate of photosynthesis (%)", line=False: bars(labs, vals, 100, 10, xl, yl, title, line)
    add("g11-ls-p2-2025-11-ec", "3.3.4",
        ("A captioned bar graph of groups B 85%, C 67% and D 53%, equal bars, both axes labelled with the unit", mb(["B", "C", "D"],
                                                                                                                  [85, 67, 53])),
        [("The same values joined as a line graph", mb(["B", "C", "D"], [85, 67, 53], line=True)),
         ("A captioned bar graph that includes group A, the group with no microplastics", mb(["A", "B", "C", "D"], [100, 85, 67, 53])),
         ("The three bars with no caption and no axis labels", mb(["B", "C", "D"], [85, 67, 53], "", "", ""))], 1)
    # ---- Grade 11 Life Sciences P2 Nov 2024 (EC) 2.1.4: a labelled bacterium (memo: correct diagram, caption, any three labels)
    add("g11-ls-p2-2024-11-ec", "2.1.4",
        ("A captioned bacterium labelled cell wall, cell membrane, cytoplasm, ribosome, nucleoid (DNA), plasmid and flagellum",
         bacterium("right")),
        [("The bacterium's outline with no labels and no caption", bacterium("bare")),
         ("A cell drawn with a nucleus and a mitochondrion", bacterium("nucleus")),
         ("A virus: a protein coat round DNA, with a tail", bacterium("virus"))], 3)
    # ---- 3.2.5: the pie chart of plastic waste in 2019 (memo: pie chart, title, calculations, key, proportions)
    PL = ["Landfill sites", "Incinerated", "Released into the environment", "Recycled"]
    PT = "Percentage of plastic waste by type of plastic waste, 2019"
    add("g11-ls-p2-2024-11-ec", "3.2.5",
        ("A titled pie chart with a key: landfill sites 49,3%, incinerated 19%, released into the environment 22,4%, recycled 9,3%",
         pie([49.3, 19, 22.4, 9.3], PL, PT)),
        [("Four equal sectors of 25% each", pie([25, 25, 25, 25], PL, PT)),
         ("Landfill sites 19% and incinerated 49,3%: two sectors swapped", pie([19, 49.3, 22.4, 9.3], PL, PT)),
         ("The percentages drawn as a bar graph", bars(["Landfill", "Burned", "Released", "Recycled"], [49, 19, 22, 9], 60, 10,
                                                       "Type of plastic waste", "Percentage (%)", PT))], 0)

    # ---- Grade 11 Life Sciences P1 Nov 2024 (EC) 2.1.1: the time to release 20 bubbles under each colour of light (memo: type of
    # graph, caption, scale and equal bars, labels with the unit, the three bars plotted)
    CL, TS = ["Blue", "Green", "Red"], [40, 160, 80]
    TT = "Time to release 20 bubbles under different colours of light"
    bl = lambda vals, title=TT, xl="Colour of light", yl="Time to release 20 bubbles (s)", line=False: bars(CL, vals, 180, 20, xl, yl, title, line)
    add("g11-ls-p1-2024-11-ec", "2.1.1",
        ("A captioned bar graph: Blue 40 s, Green 160 s, Red 80 s, equal bars on a 0 – 180 s scale, both axes labelled with the unit",
         bl(TS)),
        [("The same values joined as a line graph", bl(TS, line=True)),
         ("A captioned bar graph with Green 80 s and Red 160 s", bl([40, 80, 160])),
         ("The three bars with no caption and no axis labels", bl(TS, "", "", ""))], 2)

    # ---- Grade 11 Mathematical Literacy P1 Nov 2025 (EC) 2.2.3: builders and days, 36 builder-days (memo: the points, a smooth curve)
    BD = [(3, 12), (4, 9), (6, 6), (9, 4), (12, 3)]
    bd = lambda pts, join: plot(pts, 14, 14, 2, 2, "Number of builders", "Number of days", join)
    add("g11-ml-p1-2025-11-ec", "2.2.3",
        ("Points (3 ; 12), (4 ; 9), (6 ; 6), (9 ; 4), (12 ; 3) joined by a smooth curve", bd(BD, "smooth")),
        [("The same five points, not joined", bd(BD, None)),
         ("Points (3 ; 12), (4 ; 11), (6 ; 9), (9 ; 6), (12 ; 3) on a straight line: builders + days kept at 15",
          bd([(3, 12), (4, 11), (6, 9), (9, 6), (12, 3)], "line")),
         ("The same five points joined by straight lines", bd(BD, "line"))], 2)
    # ---- 3.2: the scatter plot of antibiotics (x) and learners who contracted TB (y), classes A to I (memo: points, title, axes)
    AB = [(35, 40), (30, 45), (10, 50), (50, 5), (45, 20), (35, 25), (20, 50), (55, 10), (10, 55)]
    TB = "The results of learners who contracted TB"
    sc = lambda pts, xl, yl, join=None, title=TB: plot(pts, 60, 60, 10, 10, xl, yl, join, title)
    NA, NT = "Number of antibiotics", "Learners who contracted TB"
    add("g11-ml-p1-2025-11-ec", "3.2",
        ("A titled scatter plot: antibiotics on the x-axis, learners with TB on the y-axis, the nine points (35 ; 40), (30 ; 45), (10 ; 50), "
         "(50 ; 5), (45 ; 20), (35 ; 25), (20 ; 50), (55 ; 10), (10 ; 55)", sc(AB, NA, NT)),
        [("The axes swapped: learners with TB on the x-axis, antibiotics on the y-axis", sc([(b, a) for a, b in AB], NT, NA)),
         ("The same nine points joined class by class as a line graph", sc(AB, NA, NT, "line")),
         ("The points plotted with no title", sc(AB, NA, NT, None, ""))], 1)

    # ---- Grade 11 Mathematics P2 Nov 2024 (EC) 2.4: the ogive of the boxers' weights (memo: grounding, upper limits, shape)
    U, CF = [55, 75, 95, 115, 135, 155], [1, 4, 13, 19, 22, 23]
    og = lambda v: ogive(U, CF, 35, v, xlab="Mass (kg)", xstep=20)
    add("g11-math-p2-2024-11-ec", "2.4",
        ("Points (35 ; 0), (55 ; 1), (75 ; 4), (95 ; 13), (115 ; 19), (135 ; 22), (155 ; 23) joined by a smooth S-shaped curve", og("right")),
        [("Points (15 ; 0), (35 ; 1), (55 ; 4), (75 ; 13), (95 ; 19), (115 ; 22), (135 ; 23): each class plotted at its lower limit",
          og("lower")),
         ("Points (55 ; 1), (75 ; 4), (95 ; 13), (115 ; 19), (135 ; 22), (155 ; 23), the curve starting at (55 ; 1)", og("float")),
         ("Points (35 ; 0), (55 ; 1), (75 ; 3), (95 ; 9), (115 ; 6), (135 ; 3), (155 ; 1): the frequencies plotted", og("freq"))], 2)

    # ---- Grade 10 Mathematics P1 Nov 2024 (NW) 8.3: the Venn diagram of A and B (memo: 0,2709; 0,1591; 0,2109; 0,3591)
    add("g10-math-p1-2024-11-nw", "8.3",
        ("0,2709 in A only, 0,1591 in both, 0,2109 in B only, 0,3591 outside the circles", venn2("0,2709", "0,1591", "0,2109", "0,3591")),
        [("0,43 in A only, 0,1591 in both, 0,37 in B only, 0,0409 outside: the totals in the only-regions",
          venn2("0,43", "0,1591", "0,37", "0,0409")),
         ("0,43 in A only, 0 in both, 0,37 in B only, 0,2 outside: no overlap", venn2("0,43", "0", "0,37", "0,2")),
         ("0,2709 in A only, 0,1591 in both, 0,2109 in B only, nothing outside the circles", venn2("0,2709", "0,1591", "0,2109", ""))], 2)

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

    # ---- Grade 11 Physical Sciences P1 Nov 2024 (EC)
    PS = "g11-ps-p1-2024-11-ec"
    add(PS, "2.2", ("W down, Fₐ = 60 N to the right, T back to the top: head to tail, closed, θ between W and T", triangle("right")),
        [("The same triangle with T pointing away from the top: the arrows do not follow each other round", triangle("tails")),
         ("W, Fₐ and T drawn from one point, not a closed triangle", triangle("open")),
         ("A closed triangle with θ marked between Fₐ and T", triangle("theta"))], 0)
    # 5.2: the 3 kg block on the 30° slope (the memo's diagram): N, F, T, f and W
    add(PS, "5.2", ("N perpendicular to the slope, F up the slope, T and f down the slope, W straight down",
                    D.fbd([("N", 120, 66), ("F", 30, 88), ("T", 202, 80, (0, -8)), ("f", 218, 52, (-4, 12)), ("W", 270, 76)], surface=30)),
        [("N, F, T and W, with f up the slope", D.fbd([("N", 120, 66), ("F", 30, 88), ("T", 202, 80), ("f", 30, 50, (0, 18)), ("W", 270, 76)],
                                                      surface=30)),
         ("F, T, f and W, with no N", D.fbd([("F", 30, 88), ("T", 202, 80, (0, -8)), ("f", 218, 52, (-4, 12)), ("W", 270, 76)], surface=30)),
         ("N, F, T, f and W, and an extra force Fnet up the slope",
          D.fbd([("N", 120, 66), ("F", 30, 88), ("T", 202, 80, (0, -8)), ("f", 218, 52, (-4, 12)), ("W", 270, 76), ("Fnet", 30, 44, (8, 24))],
                surface=30))], 3)
    # 7.2: A (−15 nC) left, B (positive) right: the lines run from B to A
    ab, sg = ("A", "B"), ("−", "+")
    add(PS, "7.2", ("Lines from B to A, curving between and around them, never crossing", D.dipole("reversed", labels=ab, signs=sg)),
        [("Lines from A to B", D.dipole("right", labels=ab, signs=sg)),
         ("Lines pushing apart between A and B, as for two like charges", D.dipole("like", labels=ab, signs=sg)),
         ("Lines between A and B with two lines crossing", D.dipole("crossing", labels=ab, signs=sg))], 1)

    # ---- Grade 11 Physical Sciences P2 Nov 2024 (EC)
    P2 = "g11-ps-p2-2024-11-ec"
    hocl = lambda o_lone, cl_lone, n_ocl=1: lewis([("H", 80, 75, ""), ("O", 165, 75, o_lone), ("Cℓ", 250, 75, cl_lone)],
                                                  [(0, 1, 1), (1, 2, n_ocl)])
    add(P2, "2.3.1", ("H : O : Cℓ: two lone pairs on O, three on Cℓ, one shared pair in each bond", hocl("ud", "udr")),
        [("O with one lone pair only", hocl("u", "udr")),
         ("H : Cℓ : O, with Cℓ in the middle", lewis([("H", 80, 75, ""), ("Cℓ", 165, 75, "ud"), ("O", 250, 75, "udr")], [(0, 1, 1), (1, 2, 1)])),
         ("Two shared pairs between O and Cℓ", hocl("u", "ur", 2))], 2)
    h2s = lambda s_lone, h_lone="": lewis([("H", 90, 75, h_lone), ("S", 165, 75, s_lone), ("H", 240, 75, "")], [(0, 1, 1), (1, 2, 1)])
    add(P2, "2.3.2", ("H : S : H with two lone pairs on S", h2s("ud")),
        [("S with one lone pair only", h2s("u")),
         ("S with no lone pairs", h2s("")),
         ("A lone pair on H as well", h2s("ud", "l"))], 0)
    nh3 = [("H", 30, 75, ""), ("N", 75, 75, "u"), ("H", 120, 75, ""), ("H", 75, 125, "")]
    nh3b = [(0, 1, 1), (1, 2, 1), (1, 3, 1)]
    nh4 = [("H", 240, 75, ""), ("N", 280, 75, ""), ("H", 320, 75, ""), ("H", 280, 115, ""), ("H", 280, 35, "")]
    nh4b = [(0, 1, 1), (1, 2, 1), (1, 3, 1), (1, 4, 1)]
    plus = T(180, 82, "+  H⁺  →", size=16)
    shift = lambda at, dx: [(s, x + dx, y, lo) for s, x, y, lo in at]
    bracket = P("M220,22 L214,22 L214,135 L220,135 M340,22 L346,22 L346,135 L340,135", w=1.6) + T(352, 26, "+", size=16, anchor="start")
    add(P2, "2.4.2", ("NH₃ with its lone pair, plus H⁺, gives [NH₄]⁺: the lone pair now shared with the fourth H, in brackets with +",
                      lewis(nh3 + nh4, nh3b + [(i + 4, j + 4, n) for i, j, n in nh4b], w=370, extra=plus + bracket)),
        [("The same, but [NH₄] without brackets or a charge", lewis(nh3 + nh4, nh3b + [(i + 4, j + 4, n) for i, j, n in nh4b], w=370, extra=plus)),
         ("NH₃ drawn with no lone pair on N", lewis([(s, x, y, "") for s, x, y, _ in nh3] + nh4, nh3b + [(i + 4, j + 4, n) for i, j, n in nh4b],
                                                    w=370, extra=plus + bracket)),
         ("NH₃ plus H⁻ (two electrons on the H) gives NH₄",
          lewis(nh3 + [("H", 172, 75, "r")] + shift(nh4, 0), nh3b + [(i + 5, j + 5, n) for i, j, n in nh4b], w=370,
                extra=T(145, 82, "+", size=16) + T(205, 82, "→", size=16)))], 3)
    add(P2, "4.5", ("A the ideal curve; B, dashed, above A at high pressure", boyle("right")),
        [("B, dashed, below A at high pressure", boyle("below")), ("B, dashed, above A at low pressure", boyle("low")),
         ("B a straight dashed line at high pressure", boyle("line"))], 1)
    add(P2, "5.4", ("Exothermic: reactants at 26,6, the peak at 33,33, products at 19,32 kJ·mol⁻¹, ΔH = −7,28 kJ·mol⁻¹",
                    profile(26.6, 33.33, 19.32, ["26,6", "33,33", "19,32"], dh="ΔH = −7,28")),
        [("Endothermic: products at 33,88 above the reactants at 26,6", profile(26.6, 40.61, 33.88, ["26,6", "40,61", "33,88"], dh="ΔH = +7,28")),
         ("The peak labelled 6,73 (the activation energy as the peak's height)", profile(26.6, 33.33, 19.32, ["26,6", "6,73", "19,32"],
                                                                                         dh="ΔH = −7,28")),
         ("The products labelled −7,28 (ΔH as their energy)", profile(26.6, 33.33, 19.32, ["26,6", "33,33", "−7,28"], dh="ΔH = −7,28"))], 0)
    add(P2, "5.5", ("A dotted curve from the same reactants to the same products, with a lower peak", profile(26.6, 33.33, 19.32, ["", "", ""],
                                                                                                         dotted=29.5)),
        [("A dotted curve with a higher peak", profile(26.6, 33.33, 19.32, ["", "", ""], dotted=37.5)),
         ("A dotted curve with the same peak", profile(26.6, 33.33, 19.32, ["", "", ""], dotted=33.6)),
         ("A dotted curve with a lower peak, on an endothermic graph", profile(26.6, 40.61, 33.88, ["", "", ""], dotted=36.5))], 2)

    # ---- Grade 11 Physical Sciences P1 Nov 2025 (EC)
    P3 = "g11-ps-p1-2025-11-ec"
    n10 = [("N", 90, 64), ("F", 30, 84), ("T", 174, 78, (0, -10)), ("fk", 188, 52, (-6, 14)), ("Fg", 270, 76)]
    add(P3, "4.2", ("N up, F at 30° above the horizontal, T and fk to the left, Fg down", D.fbd(n10)),
        [("N, F, T and Fg, with fk to the right", D.fbd([("N", 90, 64), ("F", 30, 84), ("T", 180, 78), ("fk", 0, 50, (0, 16)), ("Fg", 270, 76)])),
         ("F, T, fk and Fg, with no N", D.fbd([f for f in n10 if f[0] != "N"])),
         ("N, F, T, fk and Fg, and an extra force Fnet to the right", D.fbd(n10 + [("Fnet", 0, 46, (6, 16))]))], 2)
    add(P3, "5.2", ("T up and w down, from the dot", D.fbd([("T", 90, 70), ("w", 270, 70)], ground=False)),
        [("w down only", D.fbd([("w", 270, 70)], ground=False)),
         ("T and w both down", D.fbd([("T", 262, 74, (-14, 0)), ("w", 278, 70, (14, 0))], ground=False)),
         ("T up, w down and an extra force F to the side", D.fbd([("T", 90, 70), ("w", 270, 70), ("F", 0, 60)], ground=False))], 0)
    add(P3, "7.3.2", ("Lines radially inwards, the arrows pointing towards the −2 μC charge", point_field("−", "in")),
        [("Lines radially outwards, the arrows pointing away from the charge", point_field("−", "out")),
         ("Field lines drawn as circles round the charge", point_field("−", "circles")),
         ("Inward lines that stop short of the charge", point_field("−", "short"))], 3)

    # ---- Grade 11 Physical Sciences P2 Nov 2025 (EC)
    P4 = "g11-ps-p2-2025-11-ec"
    add(P4, "2.2.1", ("H : O : Cℓ: two lone pairs on O, three on Cℓ, one shared pair in each bond", hocl("ud", "udr")),
        [("O with one lone pair only", hocl("u", "udr")),
         ("H : Cℓ : O, with Cℓ in the middle", lewis([("H", 80, 75, ""), ("Cℓ", 165, 75, "ud"), ("O", 250, 75, "udr")], [(0, 1, 1), (1, 2, 1)])),
         ("Two shared pairs between O and Cℓ", hocl("u", "ur", 2))], 1)
    hcn = lambda n_cn, n_lone, order=("H", "C", "N"): lewis([(order[0], 80, 75, ""), (order[1], 165, 75, ""), (order[2], 250, 75, n_lone)],
                                                            [(0, 1, 1), (1, 2, n_cn)])
    add(P4, "2.2.2", ("H : C ⋮ N: one shared pair H–C, three shared pairs C≡N, one lone pair on N", hcn(3, "r")),
        [("Two shared pairs between C and N, two lone pairs on N", hcn(2, "ud")),
         ("Three shared pairs between C and N, no lone pair on N", hcn(3, "")),
         ("H : N ⋮ C, with N in the middle", hcn(3, "r", ("H", "N", "C")))], 3)
    add(P4, "5.5", ("A dotted curve from 164,1 to 0 with a lower peak", profile(164.1, 405.3, 0, ["164,1", "", "0"], dotted=330)),
        [("A dotted curve with a higher peak", profile(164.1, 405.3, 0, ["164,1", "", "0"], dotted=460)),
         ("A dotted curve with the same peak", profile(164.1, 405.3, 0, ["164,1", "", "0"], dotted=408)),
         ("A dotted curve with a lower peak, on an endothermic graph from 0 to 164,1", profile(0, 241.2, 164.1, ["0", "", "164,1"], dotted=205))],
        0)

    # ---- Grade 11 Mathematical Literacy P1 Nov 2024 (EC) 4.1.3 / 4.1.4: the income line on the answer sheet, and the break-even point B
    ML1 = "g11-ml-p1-2024-11-ec"
    INC = ((0, 0), (100, 15000))
    add(ML1, "4.1.3", ("A straight line from (0 ; 0) to (100 ; 15 000)", breakeven(INC)),
        [("A straight line from (0 ; 2 400) to (100 ; 15 000)", breakeven(((0, 2400), (100, 15000)))),
         ("A straight line from (0 ; 0) to (50 ; 7 500), stopping at 50 learners", breakeven(((0, 0), (50, 7500)))),
         ("A straight line from (0 ; 0) to (100 ; 1 500)", breakeven(((0, 0), (100, 1500))))], 0)
    add(ML1, "4.1.4", ("B where the income line crosses the cost line, at 24 learners (R3 600)", breakeven(INC, (24, 3600))),
        [("B at (0 ; 2 400), where the cost line starts", breakeven(INC, (0, 2400))),
         ("B at (50 ; 4 900) on the cost line", breakeven(INC, (50, 4900))),
         ("B at (100 ; 15 000), the end of the income line", breakeven(INC, (100, 15000)))], 2)
