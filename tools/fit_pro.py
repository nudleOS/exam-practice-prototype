"""Turn a Gemini pair (person on white, hologram on black; prompts in _ref/nexera-hero/README.md) into the industry page's two
layers in assets/pro/, fitted to the Nexera reference pair (healthcare).

  python tools/fit_pro.py <person.jpg> <object.jpg> assets/pro/<name>-person.webp assets/pro/<name>-object.webp
  (needs Pillow + numpy; then set the industry's `pro: "<name>"` in INDUSTRIES)

person: white keyed out by a flood fill from the frame's edges (white INSIDE the figure stays) plus walled-in pure-white pockets
(the gaps between arms and body); a 2 px edge band takes its alpha from how white it is (an anti-aliased outline px is part
clear) and its colour from the solid pixels beside it; resized to 896x1344. It assumes the hands sit where the nurse's do
(centre 50% across, 71.5% down): Gemini's engineer measured 49.9% / 71.4%; check a new person before trusting the fit.
object: black keyed to transparency (alpha = brightness, colour un-mixed from black), scaled to the heart's size (x1.1) and
standing on the heart's baseline in a 640x960 frame."""
import sys
import numpy as np
from PIL import Image

src_person, src_object, out_person, out_object = sys.argv[1:5]

# person: white -> alpha
rgb = np.asarray(Image.open(src_person).convert("RGB")).astype(np.float32)
d = 255 - rgb.min(-1)                       # distance from white in the darkest channel
LO, HI = 6.0, 28.0
cand = d < HI
bg = np.zeros_like(cand); bg[0, :] = cand[0, :]; bg[-1, :] = cand[-1, :]; bg[:, 0] = cand[:, 0]; bg[:, -1] = cand[:, -1]
while True:                                 # flood fill through near-white pixels from the frame's edges
    g = bg.copy()
    g[1:] |= bg[:-1]; g[:-1] |= bg[1:]; g[:, 1:] |= bg[:, :-1]; g[:, :-1] |= bg[:, 1:]
    g &= cand
    if (g == bg).all(): break
    bg = g
# background walled in by the figure (the gaps between the arms and the body): pockets of near-white the fill could not reach,
# taken when almost pure white (mean d < 10); a lens or a highlight is greyer (the glasses measured 20.8) and stays
from collections import deque
inner = cand & ~bg; seen = np.zeros_like(inner); H, W = inner.shape
for y, x in zip(*np.nonzero(inner)):
    if seen[y, x]: continue
    q = deque([(y, x)]); seen[y, x] = True; px = []
    while q:
        cy, cx = q.popleft(); px.append((cy, cx))
        for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
            if 0 <= ny < H and 0 <= nx < W and inner[ny, nx] and not seen[ny, nx]: seen[ny, nx] = True; q.append((ny, nx))
    ys, xs = np.array(px).T
    if len(px) >= 30 and d[ys, xs].mean() < 10:
        bg[ys, xs] = True; print("pocket removed", len(px), "px at x", xs.min(), "y", ys.min())
alpha = np.where(bg, np.clip((d - LO) / (HI - LO), 0, 1), 1.0)
# the drawn edge itself: 2 px next to the background are part white (a light outline once keyed); their alpha comes from how
# white they are too, on a ramp to the outline's own darkness (d 240: an anti-aliased px at d 86 is ~1/3 outline)
near = bg.copy()
for _ in range(2):
    g = near.copy(); g[1:] |= near[:-1]; g[:-1] |= near[1:]; g[:, 1:] |= near[:, :-1]; g[:, :-1] |= near[:, 1:]; near = g
edge = near & ~bg
alpha[edge] = np.minimum(alpha[edge], np.clip((d[edge] - LO) / (240 - LO), 0, 1))
a3 = np.maximum(alpha, 1e-3)[..., None]
fg = np.clip((rgb - (1 - a3) * 255) / a3, 0, 255)   # un-mix the edge from the white it was drawn on
# un-mixing a mostly clear pixel magnifies JPEG noise into light specks: a part-clear pixel takes the mean colour of the solid
# pixels within 3 px instead (colour decontamination)
solid = alpha >= 0.999
acc = np.zeros_like(rgb); cnt = np.zeros(alpha.shape, np.float32)
for dy in range(-3, 4):
    for dx in range(-3, 4):
        acc += np.roll(np.roll(rgb * solid[..., None], dy, 0), dx, 1); cnt += np.roll(np.roll(solid, dy, 0), dx, 1)
soft = (alpha > 0) & ~solid & (cnt > 0)
fg[soft] = acc[soft] / cnt[soft][:, None]
out = np.dstack([fg, alpha * 255]).astype(np.uint8)
im = Image.fromarray(out, "RGBA")
w, h = im.size; s = 1344 / h; im = im.resize((round(w * s), 1344), Image.LANCZOS)
x0 = (im.width - 896) // 2; im = im.crop((x0, 0, x0 + 896, 1344))
im.save(out_person, "WEBP", quality=88, method=6)
print("person", im.size, "background px", int(bg.sum()), "of", bg.size)

# object: black -> alpha, fitted to the heart's box
rgb = np.asarray(Image.open(src_object).convert("RGB")).astype(np.float32)
m = rgb.max(-1); alpha = np.clip((m - 10) / (255 - 10), 0, 1)
a3 = np.maximum(alpha, 1e-3)[..., None]
fg = np.clip(rgb / a3, 0, 255)
obj = Image.fromarray(np.dstack([fg, alpha * 255]).astype(np.uint8), "RGBA")
ys, xs = np.nonzero(alpha > 40 / 255)
obj = obj.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
HEART = (0.272, 0.769, 0.202, 0.705)          # the heart's visible box in its 640x960 frame (measured)
hw, hh = (HEART[1] - HEART[0]) * 640, (HEART[3] - HEART[2]) * 960
k = min(hw / obj.width, hh / obj.height) * 1.1
obj = obj.resize((round(obj.width * k), round(obj.height * k)), Image.LANCZOS)
frame = Image.new("RGBA", (640, 960), (0, 0, 0, 0))
cx, bottom = (HEART[0] + HEART[1]) / 2 * 640, HEART[3] * 960
frame.alpha_composite(obj, (round(cx - obj.width / 2), round(bottom - obj.height)))
frame.save(out_object, "WEBP", quality=88, method=6)
print("object", frame.size, "content", obj.size, "bottom at %.3f" % (bottom / 960))
