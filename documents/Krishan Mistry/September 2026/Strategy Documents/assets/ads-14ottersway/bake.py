#!/usr/bin/env python3
"""Bake the cover and back-cover flat: photo + filter + scrim + hatch + inset
rule composited to one opaque JPEG, so the finished document needs no gradient,
alpha channel or blend mode.

The only listing photography available for this property is the 1024x634 set
carried inside the HTML5 ad units. Cropped to a portrait letter page that
leaves about 490x634 usable pixels, so these flats are baked at 150 dpi and
are soft in print. Re-bake from full-resolution originals when they exist.
"""
import numpy as np
from PIL import Image, ImageEnhance

SRC = ("/Users/kyleforeman/Documents/GitHub/APERTUREREPO/Untitled/html5/"
       "14OttersWay-Peterborough-UK/APERTURE_14OttersWay_1024x768")
OUT = ("/Users/kyleforeman/Documents/GitHub/APERTUREREPO/Untitled/documents/"
       "Krishan Mistry/September 2026/Strategy Documents/assets/ads-14ottersway")
DPI = 150
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

def inset_rule(arr, inset=26, ink=(214, 208, 200), weight=2):
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

# Cover: front elevation at dusk. Type sits low, so the scrim deepens downward.
arr = np.asarray(ImageEnhance.Color(load("photo1.jpg")).enhance(0.70), dtype=np.float64)
arr = arr * 0.90
prof = 0.40 + 0.52 * np.clip((rows - 0.14) / 0.86, 0, 1) ** 1.30
finish(inset_rule(hatch(scrim(arr, prof))), f"{OUT}/ottersway-cover-flat.jpg")

# Back cover: the rear garden. Headline and agent block are centred, so it
# deepens mid-page.
arr = np.asarray(ImageEnhance.Color(load("photo4.jpg")).enhance(0.76), dtype=np.float64)
arr = arr * 0.92
prof = 0.36 + 0.44 * np.exp(-((rows - 0.52) ** 2) / (2 * 0.26 ** 2))
prof = np.clip(prof + 0.16 * np.clip((rows - 0.80) / 0.20, 0, 1), 0, 0.93)
finish(inset_rule(hatch(scrim(arr, prof))), f"{OUT}/ottersway-back-flat.jpg")
