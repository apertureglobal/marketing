#!/usr/bin/env python3
"""Bake the cover and back-cover flat: photo + filter + scrim + hatch + inset
rule composited to one opaque JPEG, so the finished document needs no gradient,
alpha channel or blend mode. Listing photography tops out at 1920px, so the
flats are baked at 200 dpi rather than 300."""
import numpy as np
from PIL import Image, ImageEnhance

SRC = ("/private/tmp/claude-501/-Users-kyleforeman-Documents-GitHub-APERTUREREPO-"
       "Untitled/89605ee2-e0e2-42b1-a533-95bf6685f64a/scratchpad/cammack/photos")
OUT = ("/Users/kyleforeman/Documents/GitHub/APERTUREREPO/Untitled/documents/"
       "Alex Brandau IV/September 2026/Strategy Documents/assets/ads-805cammack")
DPI = 200
W, H = int(8.5 * DPI), int(11 * DPI)

def load(name):
    im = Image.open(f"{SRC}/{name}").convert("RGB")
    sw, sh = im.size
    s = max(W / sw, H / sh)
    im = im.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))

def scrim(arr, prof, ink=(14, 17, 19)):
    a = prof[:, None, None]
    ink = np.array(ink, dtype=np.float64)[None, None, :]
    return arr * (1.0 - a) + ink * a

def hatch(arr, strength=0.045, pitch=7):
    yy, xx = np.mgrid[0:H, 0:W]
    m = ((xx + yy) % pitch == 0).astype(np.float64) * strength
    return arr * (1.0 - m[:, :, None]) + 255.0 * m[:, :, None]

def inset_rule(arr, inset=35, ink=(214, 208, 200), weight=2):
    for a, b in ((inset, inset + weight), (H - inset - weight, H - inset)):
        arr[a:b, inset:W - inset] = ink
    for a, b in ((inset, inset + weight), (W - inset - weight, W - inset)):
        arr[inset:H - inset, a:b] = ink
    return arr

def finish(arr, path):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").save(
        path, "JPEG", quality=88, subsampling=1, optimize=True, dpi=(DPI, DPI))
    print(path.split("/")[-1], Image.open(path).size, Image.open(path).mode)

rows = np.arange(H) / (H - 1)

# Cover: type sits low, so the scrim deepens downward.
arr = np.asarray(ImageEnhance.Color(load("1.jpg")).enhance(0.72), dtype=np.float64)
arr = arr * 0.92
prof = 0.42 + 0.50 * np.clip((rows - 0.14) / 0.86, 0, 1) ** 1.30
finish(inset_rule(hatch(scrim(arr, prof))), f"{OUT}/cammack-cover-flat.jpg")

# Back cover: headline and agent block are centred, so it deepens mid-page.
arr = np.asarray(ImageEnhance.Color(load("31.jpg")).enhance(0.78), dtype=np.float64)
arr = arr * 0.93
prof = 0.34 + 0.44 * np.exp(-((rows - 0.52) ** 2) / (2 * 0.26 ** 2))
prof = np.clip(prof + 0.16 * np.clip((rows - 0.80) / 0.20, 0, 1), 0, 0.93)
finish(inset_rule(hatch(scrim(arr, prof))), f"{OUT}/cammack-back-flat.jpg")
