#!/usr/bin/env python3
"""Bake the cover and back-cover pages flat: photo + filter + scrim + hatch +
inset rule composited to one opaque JPEG. Nothing in the finished document then
needs a gradient, an alpha channel or a blend mode. Listing photography for this
property tops out at 1920px, so the flats are baked at 200 dpi rather than 300."""
import numpy as np
from PIL import Image, ImageEnhance

SRC = ("/private/tmp/claude-501/-Users-kyleforeman-Documents-GitHub-APERTUREREPO-"
       "Untitled/89605ee2-e0e2-42b1-a533-95bf6685f64a/scratchpad/photos")
OUT = ("/Users/kyleforeman/Documents/GitHub/APERTUREREPO/Untitled/documents/"
       "Alex Brandau IV/September 2026/Strategy Documents/assets/ads-312madison")
DPI = 200
W, H = int(8.5 * DPI), int(11 * DPI)

def load(name):
    im = Image.open(f"{SRC}/{name}").convert("RGB")
    sw, sh = im.size
    scale = max(W / sw, H / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))

def scrim(arr, prof, ink=(14, 17, 19)):
    a = prof[:, None, None]
    ink = np.array(ink, dtype=np.float64)[None, None, :]
    return arr * (1.0 - a) + ink * a

def hatch(arr, strength=0.045, pitch=7):
    yy, xx = np.mgrid[0:H, 0:W]
    mask = ((xx + yy) % pitch == 0).astype(np.float64) * strength
    return arr * (1.0 - mask[:, :, None]) + 255.0 * mask[:, :, None]

def inset_rule(arr, inset=35, ink=(214, 208, 200), weight=2):
    for a, b in ((inset, inset + weight), (H - inset - weight, H - inset)):
        arr[a:b, inset:W - inset] = ink
    for a, b in ((inset, inset + weight), (W - inset - weight, W - inset)):
        arr[inset:H - inset, a:b] = ink
    return arr

def finish(arr, path):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").save(
        path, "JPEG", quality=88, subsampling=1, optimize=True, dpi=(DPI, DPI))
    im = Image.open(path)
    print(path.split("/")[-1], im.size, im.mode)

rows = np.arange(H) / (H - 1)

# Cover: type sits low, so the scrim deepens downward.
arr = np.asarray(ImageEnhance.Color(load("1.jpg")).enhance(0.74), dtype=np.float64)
arr = arr * 0.93
prof = 0.30 + 0.60 * np.clip((rows - 0.18) / 0.82, 0, 1) ** 1.35
arr = inset_rule(hatch(scrim(arr, prof)))
finish(arr, f"{OUT}/madison-cover-flat.jpg")

# Back cover: headline and agent block are centred, so it deepens mid-page.
arr = np.asarray(ImageEnhance.Color(load("2.jpg")).enhance(0.82), dtype=np.float64)
arr = arr * 0.94
prof = 0.32 + 0.44 * np.exp(-((rows - 0.52) ** 2) / (2 * 0.26 ** 2))
prof = np.clip(prof + 0.16 * np.clip((rows - 0.80) / 0.20, 0, 1), 0, 0.93)
arr = inset_rule(hatch(scrim(arr, prof)))
finish(arr, f"{OUT}/madison-back-flat.jpg")
