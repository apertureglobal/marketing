#!/usr/bin/env python3
"""Copy the six backup stills into this document's own asset folder, each resampled
to 300 dpi at the width it is actually printed at (never upscaled), so Chrome cannot
embed them at native size and inflate the PDF. Six units on disk, six advertisements."""
from PIL import Image
import glob, os

SRC = ("/Users/kyleforeman/Documents/GitHub/APERTUREREPO/Untitled/html5/"
       "ParqueDasNacoes-Lisbon-PT")
OUT = os.path.dirname(os.path.abspath(__file__))
CONTENT_IN = 8.5 - 0.85 * 2          # letter less the page's side margins

found = sorted(os.path.basename(p) for p in glob.glob(f"{SRC}/*_backup.jpg"))
print(f"{len(found)} backup stills on disk: "
      + ", ".join(f.split('_')[2] for f in found))
assert len(found) == 6, "expected the core six sizes"

UNITS = [("1024x768", "editorial-display",     0.50),
         ("768x1024", "immersive-fullscreen",  0.22),
         ("320x480",  "telephone-fullscreen",  0.15),
         ("300x600",  "vertical-display",      0.13),
         ("480x320",  "compact-display",       0.26),
         ("970x250",  "wide-editorial",        0.40)]
for unit, name, share in UNITS:
    im = Image.open(f"{SRC}/APERTURE_ParqueDasNacoes_{unit}_backup.jpg").convert("RGB")
    target = round(CONTENT_IN * share * 300)
    if target < im.width:
        im = im.resize((target, round(im.height * target / im.width)), Image.LANCZOS)
    im.save(f"{OUT}/{name}.jpg", "JPEG", quality=90, subsampling=1,
            optimize=True, dpi=(300, 300))
    print(f"{unit:>9} -> {name}.jpg {im.size}  printed {CONTENT_IN*share:.2f}in")
