"""Doodle tiles for the play screen's background (a CSS mask; nx-play.css .nx-doodles).

Tiles a/b/c were laid out by hand-run code in an earlier session and not saved; this script makes more tiles from the SAME
icon drawings (read back out of a/b/c, so the look and the Lucide licence stay one set) and is re-runnable:

    python assets/scenery/doodles.py            # writes life-sciences/doodles-d.svg

Each icon sits on a jittered grid cell (so the tile never reads as a grid), at a random size and tilt, and its line is
scaled against its size so every doodle draws at LINE px, as in a/b/c. A fixed seed: re-running gives the same file.
Icons: Lucide (lucide-static, ISC, (c) Lucide Icons and Contributors; see assets/icons/LICENSE-lucide.txt).
"""
import random, re, pathlib

HERE = pathlib.Path(__file__).parent / "life-sciences"
LINE = 1.4          # drawn line width in px, whatever the icon's size
ICON = 24           # Lucide's own box

def icons():
    """Every distinct icon drawing in the existing tiles (the inside of each <g ...> group)."""
    seen, out = set(), []
    for f in ("doodles-a.svg", "doodles-b.svg", "doodles-c.svg"):
        for body in re.findall(r"<g transform=\"[^\"]*\" stroke-width=\"[^\"]*\">(.*?)</g>", (HERE / f).read_text(encoding="utf-8")):
            if body not in seen: seen.add(body); out.append(body)
    return out

def tile(name, size, cols, px_lo, px_hi, seed):
    rnd, drawings = random.Random(seed), icons()
    cell, parts = size / cols, []
    order = drawings[:] ; rnd.shuffle(order)
    for r in range(cols):
        for c in range(cols):
            px = rnd.uniform(px_lo, px_hi); k = px / ICON                      # the icon's drawn size, and its scale
            x = c * cell + rnd.uniform(0, max(0.0, cell - px)); y = r * cell + rnd.uniform(0, max(0.0, cell - px))
            body = order[(r * cols + c) % len(order)]
            parts.append(f'<g transform="translate({x:.1f} {y:.1f}) scale({k:.3f}) rotate({rnd.randint(-25, 25)} 12 12)" stroke-width="{LINE / k:.3f}">{body}</g>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}" fill="none" stroke="#000" '
           f'stroke-linecap="round" stroke-linejoin="round"><!-- Life Sciences doodles: Lucide icons (lucide-static, ISC, (c) Lucide Icons and '
           f'Contributors; see assets/icons/LICENSE-lucide.txt). Made by assets/scenery/doodles.py (seed {seed}). -->' + "".join(parts) + "</svg>")
    (HERE / name).write_text(svg, encoding="utf-8")
    return len(parts), len(drawings)

if __name__ == "__main__":
    n, kinds = tile("doodles-d.svg", size=420, cols=6, px_lo=15, px_hi=22, seed=20260930)
    print(f"doodles-d.svg: {n} icons from {kinds} drawings")
