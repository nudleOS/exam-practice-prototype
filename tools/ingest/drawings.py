"""Drawings for "pick the drawing" (Murci, 2026-10-12): every drawing question plays as an MCQ whose options are DRAWINGS, the
right one as the memo draws it and the others each a mistake the memo names (a field of two like charges, a branched chain,
a curve that is not parallel). Each drawing is a small, self-contained SVG (no script, no link, no external font or image):
the paper's ink on white, as a figure. The app shows it through an <img>, so an SVG can never run anything.

Primitives first (text, lines, arrows), then one family per section: structural formulae, graphs, field patterns, free-body
diagrams, a Venn diagram, bar graphs, and the schematic diagrams (Geography, Life Sciences, a scaled drawing)."""
import math
from xml.sax.saxutils import escape

FONT = "Arial, Helvetica, sans-serif"
INK = "#111"
ARROW = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}" stroke="none"/></marker></defs>')


def svg(w, h, body):
    """One drawing: its own viewBox, the ink and the arrowhead; text is filled, lines are stroked."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" font-family="{FONT}" '
            f'fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ARROW}{body}</svg>')


def T(x, y, s, size=15, anchor="middle", weight=400, italic=False, fill=INK, halo=False):
    st = ' font-style="italic"' if italic else ""
    wt = f' font-weight="{weight}"' if weight != 400 else ""
    hs = ' stroke="#fff" stroke-width="5" paint-order="stroke"' if halo else ' stroke="none"'
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}"{hs}{wt}{st}>'
            f'{escape(str(s))}</text>')


def L(x1, y1, x2, y2, w=2, dash=None, arrow=False, color=INK):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    a = ' marker-end="url(#ah)"' if arrow else ""
    c = f' stroke="{color}"' if color != INK else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke-width="{w}"{d}{a}{c}/>'


def P(d, w=2, dash=None, arrow=False, fill="none"):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    a = ' marker-end="url(#ah)"' if arrow else ""
    return f'<path d="{d}" stroke-width="{w}" fill="{fill}"{ds}{a}/>'


def C(cx, cy, r, w=2, fill="none", dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" stroke-width="{w}" fill="{fill}"{ds}/>'


def R(x, y, w, h, sw=2, fill="none", dash=None, rx=0):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" stroke-width="{sw}" fill="{fill}"{ds}{r}/>'


def G(body, dx=0, dy=0, rot=None):
    r = f" rotate({rot})" if rot is not None else ""
    return f'<g transform="translate({dx:.1f},{dy:.1f}){r}">{body}</g>'


def poly(pts, w=2.4, dash=None, arrow=False):
    return P("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts), w=w, dash=dash, arrow=arrow)


def mid_arrow(x1, y1, x2, y2, at=0.55, size=7):
    """A filled arrowhead ON a line (a field line's direction), pointing from (x1, y1) to (x2, y2)."""
    mx, my = x1 + (x2 - x1) * at, y1 + (y2 - y1) * at
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (mx + size * math.cos(a), my + size * math.sin(a))
    p2 = (mx + size * math.cos(a + 2.5), my + size * math.sin(a + 2.5))
    p3 = (mx + size * math.cos(a - 2.5), my + size * math.sin(a - 2.5))
    return f'<path d="M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} L{p3[0]:.1f},{p3[1]:.1f} z" fill="{INK}" stroke="none"/>'


# ---------------------------------------------------------------- structural formulae (every atom and every bond drawn)

CELL = 34


def chain(members, cell=CELL):
    """A full structural formula from a horizontal chain. Each member: {"a": "C" | "O", "up", "down", "left", "right": a
    substituent, "next": the bond order to the next member (1 or 2)}. A substituent: "H", "Br", "OH" (O then H outwards), "=O"
    (O on a double bond) or "CH3" (a branch carbon two cells out, with its three H). Returns (width, height, body)."""
    atoms, bonds = {}, []
    dirs = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
    for i, m in enumerate(members):
        c = (i, 0)
        atoms[c] = m.get("a", "C")
        if i + 1 < len(members):
            bonds.append((c, (i + 1, 0), m.get("next", 1)))
        for k, (dx, dy) in dirs.items():
            s = m.get(k)
            if not s:
                continue
            n1 = (i + dx, dy)
            if s == "=O":
                atoms[n1] = "O"; bonds.append((c, n1, 2))
            elif s == "OH":
                n2 = (i + 2 * dx, 2 * dy)
                atoms[n1] = "O"; atoms[n2] = "H"; bonds += [(c, n1, 1), (n1, n2, 1)]
            elif s == "CH3":
                b = (i + 2 * dx, 2 * dy)
                atoms[b] = "C"; bonds.append((c, b, 1))
                for hx, hy in ((-1, 0), (1, 0), (dx, dy) if dy else (0, 1)):
                    h = (b[0] + hx, b[1] + hy)
                    if h not in atoms:
                        atoms[h] = "H"; bonds.append((b, h, 1))
            else:
                atoms[n1] = s; bonds.append((c, n1, 1))
    xs = [a for a, _ in atoms]; ys = [b for _, b in atoms]
    x0, y0, pad = min(xs), min(ys), 16
    X = lambda a: pad + (a - x0) * cell
    Y = lambda b: pad + (b - y0) * cell
    out = []
    for (a1, b1), (a2, b2), order in bonds:
        x1, y1, x2, y2 = X(a1), Y(b1), X(a2), Y(b2)
        d = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        g1 = 11 if atoms[(a1, b1)] != "Br" else 15
        g2 = 11 if atoms[(a2, b2)] != "Br" else 15
        sx, sy, ex, ey = x1 + ux * g1, y1 + uy * g1, x2 - ux * g2, y2 - uy * g2
        if order == 2:
            px, py = -uy * 3.2, ux * 3.2
            out += [L(sx + px, sy + py, ex + px, ey + py, w=1.8), L(sx - px, sy - py, ex - px, ey - py, w=1.8)]
        else:
            out.append(L(sx, sy, ex, ey, w=1.8))
    for (a, b), lab in atoms.items():
        out.append(T(X(a), Y(b) + 5.5, lab, size=16))
    return (max(xs) - x0) * cell + 2 * pad, (max(ys) - y0) * cell + 2 * pad, "".join(out)


def mol_svg(members, label=None):
    w, h, body = chain(members)
    top = 0
    if label:
        body = T(8, 20, label, size=14, anchor="start", weight=700) + G(body, 0, 22)
        top = 22
    return svg(max(w, 120), h + top, body)


def stack_svg(rows, gap=10):
    """Molecules one under another, each with an optional label ("1", "2")."""
    out, y, W = [], 0, 0
    for label, members in rows:
        w, h, body = chain(members)
        if label:
            out.append(T(10, y + h / 2 + 5, label, size=15, anchor="start", weight=700))
        out.append(G(body, 30 if label else 0, y))
        y += h + gap
        W = max(W, w + (30 if label else 0))
    return svg(W, y - gap, "".join(out))


def equation_svg(left, left_extra, right, right_extra):
    """A reaction in structural formulae: the reactant and its reagent on one line, then the arrow and the products under it
    (one line would be too wide for a phone)."""
    w1, h1, b1 = chain(left)
    w2, h2, b2 = chain(right)
    out = [G(b1, 0, 0), T(w1 + 6, h1 / 2 + 6, left_extra, size=16, anchor="start")]
    y = h1 + 6
    out.append(L(10, y + h2 / 2, 40, y + h2 / 2, w=2, arrow=True))
    out.append(G(b2, 46, y))
    out.append(T(46 + w2 + 4, y + h2 / 2 + 6, right_extra, size=16, anchor="start"))
    W = max(w1 + 8 + 9 * len(left_extra), 46 + w2 + 6 + 9 * len(right_extra))
    return svg(W, y + h2, "".join(out))


H = "H"
# the members of the molecules the papers ask for (a CH3 at a chain's end carries an H on the outside)
def end_l(**k): return {"a": "C", "left": "H", "up": "H", "down": "H", **k}
def end_r(**k): return {"a": "C", "right": "H", "up": "H", "down": "H", **k}
def ch2(**k): return {"a": "C", "up": "H", "down": "H", **k}
def ch(**k): return {"a": "C", "up": "H", **k}
OXY = {"a": "O"}

MOLS = {
    "propyl ethanoate": [end_l(), {"a": "C", "up": "=O"}, OXY, ch2(), ch2(), end_r()],
    "methyl butanoate": [end_l(), ch2(), ch2(), {"a": "C", "up": "=O"}, OXY, end_r()],
    "pentanoic acid": [end_l(), ch2(), ch2(), ch2(), {"a": "C", "up": "=O", "right": "OH"}],
    "propyl ethanoate, an H missing": [end_l(), {"a": "C", "up": "=O"}, OXY, ch2(), {"a": "C", "up": "H"}, end_r()],
    "butane": [end_l(), ch2(), ch2(), end_r()],
    "but-1-ene": [{"a": "C", "up": "H", "down": "H", "next": 2}, ch(), ch2(), end_r()],
    "2-methylpropane": [end_l(), {"a": "C", "up": "H", "down": "CH3"}, end_r()],
    "butane, an H missing": [end_l(), {"a": "C", "up": "H"}, ch2(), end_r()],
    "but-2-ene": [end_l(), ch(next=2), ch(), end_r()],
    "2-methylpropene": [{"a": "C", "up": "H", "down": "H", "next": 2}, {"a": "C", "down": "CH3"}, end_r()],
    "propene": [{"a": "C", "up": "H", "down": "H", "next": 2}, ch(), end_r()],
    "propane": [end_l(), ch2(), end_r()],
    "ethene": [{"a": "C", "up": "H", "down": "H", "next": 2}, {"a": "C", "up": "H", "down": "H"}],
    "propene, an H missing": [{"a": "C", "up": "H", "down": "H", "next": 2}, {"a": "C"}, end_r()],
    "butanoic acid": [end_l(), ch2(), ch2(), {"a": "C", "up": "=O", "right": "OH"}],
    "methyl propanoate": [end_l(), ch2(), {"a": "C", "up": "=O"}, OXY, end_r()],
    "butanal": [end_l(), ch2(), ch2(), {"a": "C", "up": "=O", "right": "H"}],
    "2-methylpropanoic acid": [end_l(), {"a": "C", "up": "H", "down": "CH3"}, {"a": "C", "up": "=O", "right": "OH"}],
    "butan-1-ol": [{"a": "C", "left": "OH", "up": "H", "down": "H"}, ch2(), ch2(), end_r()],
    "butan-2-ol": [end_l(), {"a": "C", "up": "H", "down": "OH"}, ch2(), end_r()],
    "butan-2-ol, mirrored": [end_l(), ch2(), {"a": "C", "up": "H", "down": "OH"}, end_r()],
    "2-methylpropan-1-ol": [{"a": "C", "left": "OH", "up": "H", "down": "H"}, {"a": "C", "up": "H", "down": "CH3"}, end_r()],
    "2-bromobutane": [end_l(), {"a": "C", "up": "H", "down": "Br"}, ch2(), end_r()],
    "1,2-dibromobutane": [{"a": "C", "left": "Br", "up": "H", "down": "H"}, {"a": "C", "up": "H", "down": "Br"}, ch2(), end_r()],
}


# ---------------------------------------------------------------- graphs on axes

def axes(x0, y0, x1, y1, xlab, ylab, ox=None, oy=None, zero=True):
    """Axes with arrowheads: the horizontal one at y = oy (default the bottom), the vertical one at x = ox (default the left).
    The labels sit at the arrow ends."""
    ox = x0 if ox is None else ox
    oy = y1 if oy is None else oy
    out = [L(x0, oy, x1, oy, arrow=True), L(ox, y1, ox, y0, arrow=True),
           T(x1 - 4, oy - 8, xlab, size=13, anchor="end", halo=True), T(ox + 6, y0 + 4, ylab, size=13, anchor="start")]
    if zero:
        out.append(T(ox - 7, oy + 15, "0", size=13, anchor="end"))
    return "".join(out)


def curve(f, xa, xb, X, Y, n=60):
    return [(X(xa + (xb - xa) * i / n), Y(f(xa + (xb - xa) * i / n))) for i in range(n + 1)]


def vt_balls(variant):
    """PS P1 Nov 2024 3.2: velocity-time for ball A (thrown up at 12 m/s at 0 s) and ball B (down at 5,4 m/s at 2 s), upwards
    positive, both in free fall until 4 s. variant: right | b_up (B starts at +5,4) | b_zero (B thrown at 0 s) | b_flat (B constant)."""
    X = lambda t: 50 + t * 62
    Y = lambda v: 72 - v * 4.4
    out = [axes(50, 6, 315, 210, "t (s)", "v (m·s⁻¹)", oy=Y(0))]
    out += [L(X(4), Y(0) - 4, X(4), Y(0) + 4), T(X(4) + 8, Y(0) + 16, "4", size=12), L(X(2), Y(0) - 4, X(2), Y(0) + 4),
            T(X(2) + 8, Y(0) + 16, "2", size=12), T(44, Y(12) + 5, "12", size=12, anchor="end")]
    g = 9.8
    out.append(poly([(X(0), Y(12)), (X(4), Y(12 - g * 4))]))
    out.append(T(X(4) + 12, Y(12 - g * 4) + 10, "A", size=14, weight=700, anchor="start"))
    if variant == "right":
        b = [(X(2), Y(-5.4)), (X(4), Y(-5.4 - g * 2))]
        out.append(T(44, Y(-5.4) + 5, "−5,4", size=12, anchor="end"))
    elif variant == "b_up":
        b = [(X(2), Y(5.4)), (X(4), Y(5.4 - g * 2))]
        out.append(T(44, Y(5.4) + 5, "5,4", size=12, anchor="end"))
    elif variant == "b_zero":
        b = [(X(0), Y(-5.4)), (X(2.5), Y(-5.4 - g * 2.5))]
        out.append(T(44, Y(-5.4) + 5, "−5,4", size=12, anchor="end"))
    else:
        b = [(X(2), Y(-5.4)), (X(4), Y(-5.4))]
        out.append(T(44, Y(-5.4) + 5, "−5,4", size=12, anchor="end"))
    out.append(L(*b[0], *b[1], w=2.4))
    out.append(T(b[1][0] + 12, b[1][1] + (18 if variant == "b_flat" else -6), "B", size=14, weight=700, anchor="start"))
    out.append(L(X(2), Y(0), X(2), b[0][1], w=1.2, dash="4 4"))
    return svg(330, 215, "".join(out))


def vt_bounce(variant):
    """PS P1 Nov 2025 3.5: a ball thrown up at 15 m/s; v = 0 at 1,53 s; it reaches the ground at −17,97 m/s; it bounces up
    slower and its line is parallel, ending at v = 0. variant: right | not_parallel | faster_bounce | starts_zero."""
    X = lambda t: 45 + t * 48
    Y = lambda v: 115 - v * 4.4
    out = [axes(45, 15, 318, 215, "t (s)", "v (m·s⁻¹)", oy=Y(0))]
    t1, tg = 1.53, 15 / 9.8 + 17.97 / 9.8
    v0 = 0 if variant == "starts_zero" else 15
    if variant == "starts_zero":
        out.append(poly([(X(0), Y(0)), (X(1.8), Y(-17.97))]))
        tg = 1.8
    else:
        out.append(poly([(X(0), Y(v0)), (X(tg), Y(-17.97))]))
        out.append(T(39, Y(15) + 5, "15", size=12, anchor="end"))
        out.append(T(X(t1) + 2, Y(0) - 8, "1,53", size=12, anchor="start"))
    out.append(L(X(tg), Y(-17.97), X(tg), Y(0), w=1.2, dash="4 4"))
    out.append(T(X(tg) + 6, Y(-17.97) + 12, "−17,97", size=12, anchor="start"))
    vb = {"right": 12, "not_parallel": 12, "faster_bounce": 20, "starts_zero": 12}[variant]
    tb = tg + 0.05
    if variant == "not_parallel":
        out.append(poly([(X(tb), Y(vb)), (X(tb + 1.9), Y(0))]))
    else:
        out.append(poly([(X(tb), Y(vb)), (X(tb + vb / 9.8), Y(0))]))
    out.append(L(X(tg), Y(-17.97), X(tb), Y(vb), w=1.2, dash="2 4"))
    return svg(330, 225, "".join(out))


def pf_dt(variant):
    """PS P1 Nov 2025 4.3: final momentum against contact time: line A through (0,01 ; 0) and (0,03 ; 4,5); with a bigger mass
    B is parallel and shifted right. variant: right | left | steeper | flatter."""
    X = lambda t: 50 + t * 6500
    Y = lambda p: 195 - p * 24
    out = [axes(50, 15, 320, 215, "Δt (s)", "pf (kg·m·s⁻¹)", oy=Y(0))]
    a = [(X(0.01), Y(0)), (X(0.04), Y(6.75))]
    out.append(poly(a))
    out.append(T(a[1][0] - 8, a[1][1] - 6, "A", size=14, weight=700))
    s = {"right": (0.016, 1.0), "left": (0.004, 1.0), "steeper": (0.01, 1.7), "flatter": (0.01, 0.55)}[variant]
    x0, k = s
    x1 = min(0.04, x0 + 6.75 / (225 * k))
    out.append(poly([(X(x0), Y(0)), (X(x1), Y((x1 - x0) * 225 * k))]))
    out.append(T(X(x1) + 10, Y((x1 - x0) * 225 * k) + 4, "B", size=14, weight=700))
    return svg(330, 225, "".join(out))


def generator_vt(variant):
    """PS P1 Nov 2025 9.4: A, a cosine over one rotation (4 s); doubling the speed: B's amplitude bigger and its period half,
    one cycle. variant: right | same_amp | same_period | sine."""
    X = lambda t: 45 + t * 64
    Y = lambda v: 115 - v * 34
    out = [axes(45, 12, 318, 218, "t (s)", "V (V)", oy=Y(0))]
    out += [T(X(4), Y(0) + 16, "4", size=12), T(X(2), Y(0) + 16, "2", size=12)]
    out.append(poly(curve(lambda t: math.cos(2 * math.pi * t / 4), 0, 4, X, Y), w=2))
    out.append(T(X(4) + 8, Y(1) + 4, "A", size=14, weight=700, anchor="start"))
    amp, per, f = {"right": (2.0, 2.0, math.cos), "same_amp": (1.0, 2.0, math.cos), "same_period": (2.0, 4.0, math.cos),
                   "sine": (2.0, 2.0, math.sin)}[variant]
    out.append(poly(curve(lambda t: amp * f(2 * math.pi * t / per), 0, per, X, Y), w=2.4, dash="7 4"))
    out.append(T(X(per) + 8, Y(amp * f(2 * math.pi)) + (-10 if f is math.sin else 4), "B", size=14, weight=700, anchor="start"))
    return svg(330, 228, "".join(out))


def rate_curves(variant):
    """PS P2 Nov 2024 5.1.4: volume of H2 against time; a stronger acid: curve B steeper all the way, the SAME final volume
    (the aluminium is used up). variant: right | more_gas | flatter | less_gas."""
    X = lambda t: 45 + t * 27
    Y = lambda v: 195 - v * 136
    out = [axes(45, 15, 318, 205, "time (min)", "V(H₂)", zero=True)]
    out.append(poly(curve(lambda t: 1 - math.exp(-t / 2.4), 0, 10, X, Y), w=2))
    out.append(T(X(10) + 2, Y(0.985) + 16, "A", size=14, weight=700, anchor="start"))
    k, top = {"right": (1.0, 1.0), "more_gas": (1.0, 1.25), "flatter": (3.3, 1.0), "less_gas": (1.0, 0.75)}[variant]
    out.append(poly(curve(lambda t: top * (1 - math.exp(-t / k)), 0, 10, X, Y), w=2.4, dash="7 4"))
    out.append(T(X(10) + 2, Y(top) - 4, "B", size=14, weight=700, anchor="start"))
    return svg(330, 228, "".join(out))


def maxwell(variant):
    """PS P2 Nov 2025 5.3.5: Maxwell-Boltzmann; more SO2 at the same temperature: more particles, the SAME most probable energy
    (the peak higher at the same Ek). variant: right | shifted | lower | shifted_left."""
    X = lambda e: 45 + e * 26
    Y = lambda n: 195 - n * 150
    f = lambda e, s=1.0, k=1.0: k * (e / s) * math.exp(1 - e / s) / 1.0
    out = [axes(45, 15, 318, 205, "Eₖ", "Number of particles")]
    out.append(poly(curve(lambda e: 0.72 * f(e, 2.2), 0, 10, X, Y)))
    out.append(T(X(2.2), Y(0.72) - 8, "X", size=14, weight=700))
    s, k = {"right": (2.2, 1.0), "shifted": (3.4, 0.6), "lower": (2.2, 0.5), "shifted_left": (1.4, 1.0)}[variant]
    out.append(poly(curve(lambda e: k * f(e, s), 0, 10, X, Y), w=2.4, dash="7 4"))
    out.append(T(X(s) + 14, Y(k) - 2, "Y", size=14, weight=700, anchor="start"))
    return svg(330, 228, "".join(out))


def dj_line(variant):
    """ML P1 Nov 2024 4.1.2(b): DJ Rain, R4 000 for up to 5 hours, then R1 250 an hour more: (0 ; 4 000) to (5 ; 4 000), then a
    straight rise through (6 ; 5 250) ... to (9 ; 9 000). variant: right | from_zero | flat_four | steps."""
    X = lambda h: 52 + h * 29
    Y = lambda c: 205 - c * 0.0185
    out = [axes(52, 12, 322, 205, "Hours", "Cost (R)")]
    for c in (2000, 4000, 6000, 8000):
        out += [L(48, Y(c), 52, Y(c), w=1.4), T(45, Y(c) + 4, f"{c // 1000} 000", size=11, anchor="end"),
                L(52, Y(c), 312, Y(c), w=0.6, dash="2 4")]
    for h in range(1, 10):
        out += [L(X(h), 205, X(h), 209, w=1.4), T(X(h), 222, str(h), size=11)]
    if variant == "steps":
        for a, b, c in [(0, 5, 4000)] + [(h - 1, h, 4000 + (h - 5) * 1250) for h in range(6, 10)]:
            out.append(L(X(a), Y(c), X(b), Y(c), w=2.6))
        return svg(330, 230, "".join(out))
    pts = {"right": [(0, 4000), (5, 4000), (9, 9000)], "from_zero": [(0, 0), (5, 4000), (9, 9000)],
           "flat_four": [(0, 4000), (4, 4000), (9, 9000)]}[variant]
    out.append(poly([(X(h), Y(c)) for h, c in pts], w=2.6))

    def at(h):   # the line's cost at hour h (linear between its corners)
        for (h0, c0), (h1, c1) in zip(pts, pts[1:]):
            if h0 <= h <= h1:
                return c0 + (c1 - c0) * (h - h0) / (h1 - h0)
        return pts[-1][1]
    for h in range(0, 10):
        out.append(C(X(h), Y(at(h)), 2.8, fill=INK, w=1))
    return svg(330, 230, "".join(out))


def histogram(variant):
    """Maths P2 Nov 2025 2.1.3: the frequencies from the cumulative table, 16, 24, 19, 8, 3 for 0-20 ... 80-100 minutes, the bars
    touching. variant: right | gaps | cumulative | swapped."""
    fr = {"right": [16, 24, 19, 8, 3], "gaps": [16, 24, 19, 8, 3], "cumulative": [16, 40, 59, 67, 70],
          "swapped": [16, 19, 24, 8, 3]}[variant]
    top = 70 if variant == "cumulative" else 30
    X = lambda t: 50 + t * 2.6
    Y = lambda n: 200 - n * (180 / top)
    out = [axes(50, 12, 318, 200, "t (min)", "People")]
    step = 10 if top == 70 else 5
    for n in range(step, top + 1, step):
        out += [L(46, Y(n), 50, Y(n), w=1.4), T(43, Y(n) + 4, str(n), size=11, anchor="end")]
    for i, n in enumerate(fr):
        x0, x1 = X(20 * i), X(20 * (i + 1))
        if variant == "gaps":
            x0, x1 = x0 + 8, x1 - 8
        out.append(R(x0, Y(n), x1 - x0, 200 - Y(n), sw=1.8, fill="#d9d9d9"))
    for t in range(20, 101, 20):
        out.append(T(X(t), 214, str(t), size=11))
    return svg(330, 222, "".join(out))


HATCH = ('<defs><pattern id="hx" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         f'<line x1="0" y1="0" x2="0" y2="7" stroke="{INK}" stroke-width="1.6"/></pattern></defs>')


def lte_bars(variant):
    """ML P1 Nov 2025 3.2.3: the stacked bars for KwaZulu-Natal and Mpumalanga, 2021 hatched, 2022 white, 2023 black: KZN's 2023
    part from 20 500 000 to 31 500 000, Mpumalanga's from 8 500 000 to 14 000 000. variant: right | from_zero | added_on | short."""
    Y = lambda n: 205 - n / 1e6 * 3.4
    out = [HATCH, axes(60, 12, 318, 205, "", "Devices")]
    for m in range(10, 51, 10):
        out += [L(56, Y(m * 1e6), 60, Y(m * 1e6), w=1.4), T(53, Y(m * 1e6) + 4, f"{m} m", size=11, anchor="end"),
                L(60, Y(m * 1e6), 312, Y(m * 1e6), w=0.6, dash="2 4")]
    bars = [("KZN", 90, 9e6, 20.5e6, 31.5e6), ("MP", 210, 3.5e6, 8.5e6, 14e6)]
    for name, x, a, b, c in bars:
        out.append(R(x, Y(a), 56, 205 - Y(a), sw=1.6, fill="url(#hx)"))
        out.append(R(x, Y(b), 56, Y(a) - Y(b), sw=1.6, fill="#fff"))
        if variant == "right":
            out.append(R(x, Y(c), 56, Y(b) - Y(c), sw=1.6, fill=INK))
        elif variant == "from_zero":
            out.append(R(x + 60, Y(c - b), 26, 205 - Y(c - b), sw=1.6, fill=INK))
        elif variant == "added_on":
            out.append(R(x, Y(b + c), 56, Y(b) - Y(b + c), sw=1.6, fill=INK))
        else:
            out.append(R(x, Y(c - 4e6), 56, Y(b) - Y(c - 4e6), sw=1.6, fill=INK))
        out.append(T(x + 28, 222, name, size=12))
    return svg(330, 228, "".join(out))


# ---------------------------------------------------------------- electric field patterns

def dipole(variant, labels=("P", "S"), signs=("+", "−")):
    """PS P1 Nov 2024 7.2: P (+2 nC) left, S (−2 nC) right. variant: right (from P to S, curving between and around, never
    crossing) | reversed (from S to P) | like (lines pushing apart, the field of two like charges) | crossing (two lines cross)."""
    P_, S_, cy = 110, 220, 110
    out = []
    if variant == "like":
        for cx, angs in ((P_, (90, 135, 180, 225, 270, 45, 315)), (S_, (90, 45, 0, 315, 270, 135, 225))):
            for a in angs:
                r = math.radians(a)
                x1, y1 = cx + 14 * math.cos(r), cy - 14 * math.sin(r)
                x2, y2 = cx + 72 * math.cos(r), cy - 72 * math.sin(r)
                out += [L(x1, y1, x2, y2, w=1.8), mid_arrow(x1, y1, x2, y2)]
    else:
        fwd = variant != "reversed"
        ar = lambda xa, ya, xb, yb: mid_arrow(xa, ya, xb, yb) if fwd else mid_arrow(xb, yb, xa, ya)
        out += [L(P_ + 14, cy, S_ - 14, cy, w=1.8), ar(P_ + 14, cy, S_ - 14, cy)]
        for dy in (-1, 1):
            for k in (34, 70):
                ys, q = cy + dy * 10, cy + dy * k * 1.4
                out.append(P(f"M{P_ + 10},{ys} Q165,{q} {S_ - 10},{ys}", w=1.8))
                ym = cy + dy * k * 0.7 + dy * 2
                out.append(ar(158, ym, 172, ym))
            out.append(P(f"M{P_ - 12},{cy + dy * 6} C40,{cy + dy * 125} 290,{cy + dy * 125} {S_ + 12},{cy + dy * 6}", w=1.8))
            yt = cy + dy * 95
            out.append(ar(158, yt, 172, yt))
        if variant == "crossing":
            out += [L(P_ + 6, cy - 12, S_ + 40, 30, w=1.8), L(P_ + 6, cy + 12, S_ + 40, 190, w=1.8)]
    out += [C(P_, cy, 12, fill="#fff"), C(S_, cy, 12, fill="#fff"),
            T(P_, cy + 5, signs[0], size=17, weight=700), T(S_, cy + 5, signs[1], size=17, weight=700)]
    if labels[0]:
        out.append(T(P_, cy + 32, labels[0], size=14))
    if labels[1]:
        out.append(T(S_, cy + 32, labels[1], size=14))
    return svg(330, 220, "".join(out))


def radial(variant):
    """PS P1 Nov 2025 7.2: the field of a positive sphere X. variant: right (radially outwards, arrows away) | inwards |
    two (a second charge drawn) | circles (field lines drawn as circles)."""
    cx, cy, out = 165, 110, []
    if variant == "two":
        return dipole("right", labels=("X", ""), signs=("+", "−"))
    if variant == "circles":
        for r in (34, 58, 82):
            out += [C(cx, cy, r, w=1.8), mid_arrow(cx - 6, cy - r, cx + 6, cy - r, at=0.5)]
    else:
        for k in range(8):
            a = 2 * math.pi * k / 8
            x1, y1 = cx + 19 * math.cos(a), cy + 19 * math.sin(a)
            x2, y2 = cx + 95 * math.cos(a), cy + 95 * math.sin(a)
            out += [L(x1, y1, x2, y2, w=1.8), mid_arrow(x1, y1, x2, y2) if variant == "right" else mid_arrow(x2, y2, x1, y1)]
    out += [C(cx, cy, 17, fill="#fff"), T(cx, cy + 6, "+", size=18, weight=700), T(cx + 30, cy + 16, "X", size=14, anchor="start", halo=True)]
    return svg(330, 220, "".join(out))


# ---------------------------------------------------------------- free-body diagrams (a dot and labelled arrows)

def fbd(forces, surface=0, ground=True):
    """forces: [(label, angle in degrees from +x, length[, (dx, dy) nudge for the label])]; the dot at the centre; the surface's
    tilt drawn faintly. Labels carry a white halo, so the dashed surface never runs through them."""
    cx, cy, out = 165, 112, []
    if ground:
        a = math.radians(surface)
        out.append(L(cx - 120 * math.cos(a), cy + 120 * math.sin(a), cx + 120 * math.cos(a), cy - 120 * math.sin(a), w=1, dash="3 5"))
    labels = []
    for f in forces:
        lab, ang, ln = f[:3]
        nx, ny = f[3] if len(f) > 3 else (0, 0)
        a = math.radians(ang)
        x2, y2 = cx + ln * math.cos(a), cy - ln * math.sin(a)
        out.append(L(cx, cy, x2, y2, w=2.4, arrow=True))
        lx, ly = cx + (ln + 17) * math.cos(a) + nx, cy - (ln + 17) * math.sin(a) + ny
        labels.append(T(lx, ly + 5, lab, size=15, italic=True, halo=True))
    out.append(C(cx, cy, 5, fill=INK, w=1))
    return svg(330, 225, "".join(out + labels))


# ---------------------------------------------------------------- a Venn diagram of three sets

def venn3(vals, outside=None):
    """vals: {"M", "T", "G", "MT", "MG", "TG", "MTG"}: the number in each region; M top left, T top right, G below."""
    out = [R(10, 10, 310, 225, sw=1.6), T(22, 30, "ξ", size=15, anchor="start")]
    cs = {"M": (128, 98), "T": (202, 98), "G": (165, 158)}
    for k, (x, y) in cs.items():
        out.append(C(x, y, 62, w=2))
    out += [T(70, 50, "M", size=15, weight=700), T(262, 50, "T", size=15, weight=700), T(165, 232, "G", size=15, weight=700)]
    pos = {"M": (100, 84), "T": (230, 84), "G": (165, 192), "MT": (165, 70), "MG": (128, 140), "TG": (202, 140), "MTG": (165, 118)}
    for k, (x, y) in pos.items():
        out.append(T(x, y + 6, vals[k], size=17, weight=700))
    if outside is not None:
        out.append(T(290, 220, outside, size=15, weight=700))
    return svg(330, 245, "".join(out))


# ---------------------------------------------------------------- schematic diagrams

def cloud(x, y, w, h):
    """A towering cumulonimbus: a lumpy column (x to x + w wide, its anvil at y, its base at y + h) with a flat, spreading anvil."""
    s, b = h / 4, y + h
    d = (f"M{x:.1f},{b:.1f} Q{x - 14:.1f},{b - s / 2:.1f} {x:.1f},{b - s:.1f} Q{x - 14:.1f},{b - 1.5 * s:.1f} {x:.1f},{b - 2 * s:.1f} "
         f"Q{x - 14:.1f},{b - 2.5 * s:.1f} {x:.1f},{y + s:.1f} L{x - 20:.1f},{y + 0.55 * s:.1f} L{x - 10:.1f},{y:.1f} "
         f"L{x + w + 10:.1f},{y:.1f} L{x + w + 20:.1f},{y + 0.55 * s:.1f} L{x + w:.1f},{y + s:.1f} "
         f"Q{x + w + 14:.1f},{y + 1.5 * s:.1f} {x + w:.1f},{y + 2 * s:.1f} Q{x + w + 14:.1f},{y + 2.5 * s:.1f} {x + w:.1f},{y + 3 * s:.1f} "
         f"Q{x + w + 14:.1f},{y + 3.5 * s:.1f} {x + w:.1f},{b:.1f} Z")
    return P(d, w=1.8, fill="#e9e9e9")


def cyclone(variant):
    """Geography P1 Nov 2024 1.4.4: a tropical cyclone in its mature stage: towering cumulonimbus on both sides of a clear eye,
    the air in the eye sinking. variant: right | rising (the eye's air going up) | no_eye (cloud across the centre) | stratus."""
    out = [L(15, 200, 315, 200, w=1.6), T(300, 216, "Sea", size=12, anchor="end")]
    if variant == "no_eye":
        out.append(cloud(40, 40, 250, 150))
    elif variant == "stratus":
        for i, y in enumerate((70, 100, 130)):
            out.append(R(30, y, 115, 16, sw=1.6, fill="#e9e9e9", rx=8))
            out.append(R(185, y, 115, 16, sw=1.6, fill="#e9e9e9", rx=8))
    else:
        out.append(cloud(42, 40, 85, 150))
        out.append(cloud(203, 40, 85, 150))
    lab = {"stratus": "Stratus", "no_eye": "Cb", "right": "Cb", "rising": "Cb"}[variant]
    out += [L(60, 34, 80, 18, w=1.2), T(84, 16, lab, size=14, anchor="start")]
    if variant != "no_eye":
        out.append(T(165, 30, "Eye", size=14, weight=700))
        for x in (152, 178):
            if variant == "rising":
                out.append(L(x, 170, x, 70, w=2, arrow=True))
            else:
                out.append(L(x, 70, x, 170, w=2, arrow=True))
    for x, d in ((30, 1), (300, -1)):
        out.append(L(x, 192, x + d * 40, 192, w=1.6, arrow=True))
    return svg(330, 222, "".join(out))


def cold_front(variant):
    """Geography P1 Nov 2025 1.3.5: a cold front's cross-section: cold air undercutting the warm air along a steep front, the
    system moving west to east, a cumulonimbus, a sector named. The front meets the ground at x = 215; its surface rises
    steeply there and leans back (west) over the cold air. variant: right | warm_front (a gentle slope, warm air gliding up
    over cold air ahead, stratus) | east_to_west | warm_under (warm air under the cold)."""
    out = [L(15, 200, 315, 200, w=1.6), T(20, 216, "W", size=13, anchor="start"), T(310, 216, "E", size=13, anchor="end")]
    if variant == "warm_front":
        out.append(P("M60,200 C150,197 240,165 305,100", w=2.2))
        out.append(T(250, 190, "Cold air", size=13, halo=True))
        out.append(T(110, 120, "Warm air", size=13))
        out.append(R(150, 112, 120, 14, sw=1.4, fill="#e9e9e9", rx=7))
        out.append(T(210, 104, "Stratus", size=12))
        arrow = (120, 40, 220, 40)
    else:
        under = variant == "warm_under"
        out.append(P("M215,200 C204,168 160,112 40,84", w=2.2))
        out.append(T(95, 186, "Warm air" if under else "Cold air", size=13, halo=True))
        out.append(T(275, 186, "Cold air" if under else "Warm air", size=13, halo=True))
        out.append(T(80, 150, "Warm sector" if under else "Cold sector", size=12, halo=True))
        out.append(cloud(222, 52, 46, 112))
        out.append(T(292, 70, "Cb", size=13, anchor="start"))
        arrow = (220, 32, 120, 32) if variant == "east_to_west" else (120, 32, 220, 32)
    out.append(L(*arrow, w=2.2, arrow=True))
    out.append(T((arrow[0] + arrow[2]) / 2, 22, "Movement", size=12))
    return svg(330, 222, "".join(out))


def gis_layer(variant):
    """Geography P2 Nov 2025 3.3.3: layer C with layers A and B on it: the woodland patches, the row of four trees and the
    non-perennial water (as in the sketch). variant: right | no_water | no_trees | no_woodland."""
    out = [P("M70,40 L320,40 L260,200 L10,200 Z", w=1.8), T(140, 190, "C", size=15)]
    if variant != "no_woodland":
        out.append(P("M60,170 C45,150 70,140 82,150 C95,120 70,110 90,98 C110,110 100,130 118,150 C140,160 140,180 110,185 Z", w=1.4, fill="#bdbdbd"))
        out.append(P("M118,52 C112,62 108,74 118,80 C132,76 140,64 132,54 Z", w=1.4, fill="#bdbdbd"))
        out.append(P("M240,48 C230,60 236,88 250,96 C268,98 284,90 290,70 C292,56 280,46 262,46 Z", w=1.4, fill="#bdbdbd"))
    if variant != "no_trees":
        for i in range(4):
            out.append(C(196 + i * 8, 70 + i * 16, 3.6, fill=INK, w=1))
    if variant != "no_water":
        out.append(P("M150,148 C150,126 196,118 236,122 L250,130 C226,150 200,160 176,162 C160,162 150,158 150,148 Z", w=1.6, fill="#d0d0d0"))
    return svg(330, 215, "".join(out))


def chromosome(x, y, shade, tip, flip=False, ang=0):
    """Two chromatids joined at a centromere: shade "dark" / "light", and one chromatid's tip the other way (crossing over)."""
    dark, light = INK, "#fff"
    body = dark if shade == "dark" else light
    tipc = light if shade == "dark" else dark
    out = []
    for dx in (-5, 5):
        out.append(R(x + dx - 3.5, y - 26, 7, 52, sw=1.6, fill=body, rx=3.5))
    if tip:
        tx = x + (5 if not flip else -5)
        out.append(R(tx - 3.5, y - 26, 7, 14, sw=1.6, fill=tipc, rx=3.5))
    out.append(C(x, y, 4, fill="#888", w=1.2))
    return "".join(out)


def metaphase2(variant):
    """Life Sciences P2 Nov 2024 2.2.5: metaphase II: two unpaired chromosomes in one row at the equator, spindle fibres to the
    poles, one shaded chromosome with an unshaded tip and one unshaded with a shaded tip, two labels. variant: right |
    four (homologous pairs: four chromosomes) | two_rows (pairs either side of the equator) | no_tips (no crossing over)."""
    cx, cy = 150, 115
    out = [C(cx, cy, 96, w=2), C(cx, 20, 3, fill=INK), C(cx, 210, 3, fill=INK)]
    xs = {"right": [126, 174], "no_tips": [126, 174], "four": [102, 134, 166, 198], "two_rows": [126, 174]}[variant]
    for x in xs:   # spindle fibres from each pole to each centromere
        ys = (cy - 32, cy + 32) if variant == "two_rows" else (cy, cy)
        out.append(L(cx, 22, x, ys[0], w=1, dash="4 3"))
        out.append(L(cx, 208, x, ys[1], w=1, dash="4 3"))
    if variant == "two_rows":
        out += [chromosome(126, cy - 32, "dark", True), chromosome(174, cy - 32, "light", True),
                chromosome(126, cy + 32, "dark", False), chromosome(174, cy + 32, "light", False)]
    elif variant == "four":
        out += [chromosome(102, cy, "dark", True), chromosome(134, cy, "dark", False), chromosome(166, cy, "light", True, flip=True),
                chromosome(198, cy, "light", False)]
    else:
        tips = variant == "right"
        out += [chromosome(126, cy, "dark", tips), chromosome(174, cy, "light", tips, flip=True)]
    out += [L(cx + 66, cy - 72, 268, cy - 92, w=1.2), T(272, cy - 88, "Cell membrane", size=12, anchor="start"),
            L(cx + 30, cy + 10, 268, cy + 40, w=1.2), T(272, cy + 44, "Chromosome", size=12, anchor="start")]
    return svg(380, 225, "".join(out))


def hardboard(variant):
    """ML P2 Nov 2025 5.1.3(b): the hardboard (60 cm × 90 cm) at 1 : 20: a rectangle 3 cm wide and 4,5 cm high, drawn to scale on
    a centimetre grid. variant: right (3 × 4,5) | ten (6 × 9: 1 : 10) | turned (4,5 wide × 3 high) | four (3 × 4)."""
    u = 22
    w, h = {"right": (3, 4.5), "ten": (6, 9), "turned": (4.5, 3), "four": (3, 4)}[variant]
    out = []
    for i in range(0, 11):
        out.append(L(20 + i * u, 12, 20 + i * u, 12 + 10 * u, w=0.6, color="#9a9a9a"))
        out.append(L(20, 12 + i * u, 20 + 10 * u, 12 + i * u, w=0.6, color="#9a9a9a"))
    out.append(T(20 + 5 * u, 12 + 10 * u + 18, "Each square: 1 cm × 1 cm", size=12))
    x, y = 20 + u, 12 + u * 0.5
    out.append(R(x, y, w * u, h * u, sw=2.6, fill="#ececec"))
    fmt = lambda v: f"{v:g}".replace(".", ",") + " cm"
    out.append(T(x + w * u / 2, y - 4, fmt(w), size=13, halo=True))
    out.append(T(x + w * u + 6, y + h * u / 2 + 4, fmt(h), size=13, anchor="start", halo=True))
    return svg(330, 262, "".join(out))
