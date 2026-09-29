"""Scenery cut-out + bake for the practice play screen's rocks and plants (nx-play.css).

Gemini renders have NO alpha channel, so the art is generated on a solid magenta background and cut here.
  python cutout.py cut  SRC.jpg OUT.png        # key the magenta out, trim to the art
  python cutout.py bake OUT.png NAME DRAWN_H   # write NAME.webp (light) + NAME-dark.webp at 1.5x DRAWN_H

Cut: alpha from 'magenta-ness' m = min(R,B) - G. Measured on the LS renders: the background scores 197-210, rocks and
leaves < 0, only the soft edges (~3% of pixels) fall between. Edge pixels are un-mixed from the background colour
(C = a*F + (1-a)*K  ->  F = (C - (1-a)*K) / a), then any leftover spill (min(R,B) > G, which no rock or leaf has) is
pulled back to G. Magenta, not green-screen green: the plants are green.

Bake: 1.5x the largest height the art is drawn at (measured: the pair's size follows pixel count, not quality —
2x was 110-133 KB at any quality, 1.5x q65 is 77 KB). The dark variant follows the mockup's measured dark tokens:
rock luminance 0.13 -> ~0.035 (x0.27 in linear light), leaves near kept (x0.9; mockup 0.148 vs the render's 0.130).
The rock weight is its blueness (B - G): rocks ~+30, leaves negative. Light mode uses the render as is (rock 0.129
vs the mockup's 0.135)."""
import sys
import numpy as np
from PIL import Image


def cut(src, out, pad=8):
    a = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    m = np.minimum(R, B) - G
    edge = np.concatenate([a[:12].reshape(-1, 3), a[-12:].reshape(-1, 3), a[:, :12].reshape(-1, 3), a[:, -12:].reshape(-1, 3)])
    K = np.median(edge, axis=0)                                                   # the background, measured on the border
    mb = np.percentile(np.minimum(edge[:, 0], edge[:, 2]) - edge[:, 1], 1) - 6   # just under its lowest score
    m0 = 10.0
    al = np.clip((mb - m) / (mb - m0), 0, 1)
    al[al < 0.03] = 0
    aa = np.maximum(al, 1e-3)[..., None]
    F = np.clip((a - (1 - aa) * K) / aa, 0, 255)
    spill = np.maximum(np.minimum(F[..., 0], F[..., 2]) - F[..., 1], 0)
    F[..., 0] -= spill
    F[..., 2] -= spill
    im = Image.fromarray(np.dstack([F, al * 255]).round().astype(np.uint8), "RGBA")
    ys, xs = np.nonzero(al > 0.5)
    box = (max(xs.min() - pad, 0), max(ys.min() - pad, 0), min(xs.max() + pad + 1, a.shape[1]), min(ys.max() + pad + 1, a.shape[0]))
    im.crop(box).save(out)
    print(out, "background", K.round(), "cut at", round(mb), "box", box)


def _lin(c):
    c = c / 255
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _srgb(v):
    return np.where(v <= 0.0031308, v * 12.92, 1.055 * np.power(np.clip(v, 0, 1), 1 / 2.4) - 0.055) * 255


def night(im):
    a = np.asarray(im).astype(np.float64)
    rgb, A = a[..., :3], a[..., 3:]
    w = np.clip((rgb[..., 2] - rgb[..., 1]) / 22, 0, 1)[..., None]
    k = 0.27 * w + 0.9 * (1 - w)
    return Image.fromarray(np.dstack([_srgb(_lin(rgb) * k), A]).round().clip(0, 255).astype(np.uint8), "RGBA")


def bake(png, name, drawn_h, scale=1.5, q=65):
    im = Image.open(png)
    h = round(drawn_h * scale)
    im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    for suffix, v in (("", im), ("-dark", night(im))):
        v.save(f"{name}{suffix}.webp", "WEBP", quality=q, method=6, alpha_quality=80)
        print(f"{name}{suffix}.webp", v.size)


if __name__ == "__main__":
    if sys.argv[1] == "cut":
        cut(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "bake":
        bake(sys.argv[2], sys.argv[3], int(sys.argv[4]))
