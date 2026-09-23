#!/usr/bin/env python3
"""Downsample the six ad backup stills to 300 dpi at their printed width on the
Advertisements page. Chrome otherwise embeds them at native size."""
from PIL import Image
SRC = "/Users/kyleforeman/Documents/GitHub/APERTUREREPO/Untitled/html5/805CammackCt-Nashville-TN"
OUT = ("/Users/kyleforeman/Documents/GitHub/APERTUREREPO/Untitled/documents/"
       "Alex Brandau IV/September 2026/Strategy Documents/assets/ads-805cammack")
COL = 6.8  # inches of live column on the page
# (unit size, output name, share of the column width)
UNITS = [("1024x768", "editorial-display",     0.500),
         ("768x1024", "immersive-fullscreen",  0.220),
         ("320x480",  "telephone-fullscreen",  0.150),
         ("300x600",  "vertical-display",      0.130),
         ("480x320",  "compact-display",       0.260),
         ("970x250",  "wide-editorial",        0.400)]
for size, name, share in UNITS:
    im = Image.open(f"{SRC}/APERTURE_805CammackCt_{size}_backup.jpg").convert("RGB")
    target = round(COL * share * 300)
    if im.width > target:
        im = im.resize((target, round(im.height * target / im.width)), Image.LANCZOS)
    p = f"{OUT}/{name}.jpg"
    im.save(p, "JPEG", quality=88, subsampling=1, optimize=True, dpi=(300, 300))
    print(f"{name:<22} {size:>8}  ->  {im.size}  {round(im.width/(COL*share))} dpi")
