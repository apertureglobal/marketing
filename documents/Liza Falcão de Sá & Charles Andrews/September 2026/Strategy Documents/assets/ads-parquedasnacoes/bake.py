#!/usr/bin/env python3
"""Bake the cover and back-cover pages flat: photo + filter + scrim + hatch + inset
rule composited to one opaque JPEG. Nothing in the finished document then needs a
gradient, an alpha channel or a blend mode - Heyzine renders either as a magenta page.

Listing photography for this property is 1920x1280, so a full-bleed portrait letter
page is filled from the 1280px dimension: about 116 dpi effective. Baked at 200 dpi;
crisp on screen and in the flipbook, visibly soft if this is printed large."""
import numpy as np
from PIL import Image, ImageEnhance
import os

SRC = ("/private/tmp/claude-501/-Users-kyleforeman-Documents-GitHub-APERTUREREPO-"
       "Untitled/89605ee2-e0e2-42b1-a533-95bf6685f64a/scratchpad/photos-pdn")
OUT = os.path.dirname(os.path.abspath(__file__))
DPI = 200
W, H = int(8.5 * DPI), int(11 * DPI)

def load(name):
    im = Image.open(f"{SRC}/{name}").convert("RGB")
    sw, sh = im.size
    scale = max(W / sw, H / sh)
    print(f"  {name} {sw}x{sh} -> upscaled {scale:.2f}x "
          f"({min(sw / 8.5, sh / 11):.0f} dpi effective)")
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
    print(f"  -> {os.path.basename(path)} {im.size} {im.mode} "
          f"{os.path.getsize(path)/1024:.0f} KB")

rows = np.arange(H) / (H - 1)

# Cover - the terrace above the Tagus. Type sits low, so the scrim deepens downward.
print("cover:")
arr = np.asarray(ImageEnhance.Color(load("33.jpg")).enhance(0.72), dtype=np.float64)
arr = arr * 0.92
prof = 0.26 + 0.70 * np.clip((rows - 0.14) / 0.86, 0, 1) ** 0.80
arr = inset_rule(hatch(scrim(arr, prof)))
finish(arr, f"{OUT}/cover-flat.jpg")

# Back cover - the social area. Headline and agent block are centred, so it
# deepens through the middle of the page.
print("back cover:")
arr = np.asarray(ImageEnhance.Color(load("48.jpg")).enhance(0.80), dtype=np.float64)
arr = arr * 0.93
prof = 0.34 + 0.44 * np.exp(-((rows - 0.52) ** 2) / (2 * 0.26 ** 2))
prof = np.clip(prof + 0.30 * np.clip((rows - 0.70) / 0.22, 0, 1), 0, 0.93)
arr = inset_rule(hatch(scrim(arr, prof)))
finish(arr, f"{OUT}/backpage-flat.jpg")
