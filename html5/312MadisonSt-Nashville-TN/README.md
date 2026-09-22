# Aperture Global · 312 Madison St, Germantown, Nashville, Tennessee · HTML5 display ads

Six self-contained HTML5 units in the **"faux video"** style: no video file anywhere in the
package. Each unit is built from 4 listing stills, and a slow CSS pan/zoom (Ken Burns)
crossfades one into the next so the photo band reads as a slowly moving camera.

Preview page: **[preview.html](preview.html)** — all six units on one page. The unit loops
every 15 s; the preview plays two passes and then holds on the last frame.

## Units

| Size | Unit | Zip | % of 700 KB budget | Role |
|---|---:|---:|---:|---|
| 768x1024 | 468 KB | 391,104 B | 67% | Master unit |
| 1024x768 | 587 KB | 514,543 B | 84% | Landscape: the band runs to the top edge, 134 px row panel beneath (logo / rule / headline + rotating subline / CTA) |
| 480x320 | 248 KB | 172,630 B | 35% | The same row structure reduced |
| 970x250 | 279 KB | 201,597 B | 40% | Billboard |
| 320x480 | 203 KB | 124,648 B | 29% | Portrait, the master proportions at 320 wide |
| 300x600 | 228 KB | 149,835 B | 33% | Half page, 300x300 band |

Each folder zips with `index.html` at its root (6 files: the page, `bg.jpg`,
`photo1`-`photo4.jpg`).
Beside each is a 1x backup still, `*_backup.jpg`, for placements that cannot run HTML5.

## Copy on file

- Eyebrow — **Premier Offering**
- Headline — **312 Madison St**
- Sub 1 — **Germantown, Nashville, Tennessee**
- Sub 2 — **5 bed | 7 bath | 10,024 sq ft**
- Sub 3 — **Listed by Alex Brandau IV**
- CTA — **Schedule a viewing** (sentence case, per the Aperture standard)
- clickTag → `https://www.apertureglobal.com/312madisonst`

Copy is baked to SVG outline paths, so changing any line means a rebuild, not an edit to
`index.html`.

## Build

Generated, never hand-edited. Editing a unit's `index.html` is reverted by the next rebuild.

    python3 kenburns_build.py --order "<order folder>" --overrides overrides/<slug>.json \
      --folder 312MadisonSt-Nashville-TN --clicktag-slug <lofty-slug> --photos <six, in order>

The builder lives in `~/Documents/Claude/aperture-digital-ads`. Running order of the stills:

1. `COVER--011.jpg`
2. `31_living--045.jpg`
3. `09_S3-entertainment--137.jpg`
4. `50_outdoor--024.jpg`

Each still holds 3.75 s across the 15 s pass, with a 0.8 s crossfade into the next. One
extra layer repeats still 1 so the loop closes without a seam.

## Verified

Real browser, served over HTTP. For every one of the six sizes: each still is the top visible
layer at its own midpoint; the wrap layer reaches full opacity at 15 s; no moment of the pass
is blank; the eyebrow mark and text are centred in the unit; and no unit carries a video
element, an autoplay watchdog or any JavaScript beyond the clickTag shim. No unit makes an
external request of any kind. Every unit is under the 700 KB budget.
