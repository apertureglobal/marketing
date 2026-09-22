# Aperture Global · 11850 N 5th E, Idaho Falls, Idaho · HTML5 display ads

Six self-contained HTML5 units in the **"faux video"** style: no video file anywhere in the
package. Each unit is built from 4 listing stills, and a slow CSS pan/zoom (Ken Burns)
crossfades one into the next so the photo band reads as a slowly moving camera.

Preview page: **[preview.html](preview.html)** — all six units on one page. The unit loops
every 15 s; the preview plays two passes and then holds on the last frame.

## Units

| Size | Unit | Zip | % of 700 KB budget | Role |
|---|---:|---:|---:|---|
| 768x1024 | 405 KB | 334,176 B | 58% | Master unit |
| 1024x768 | 562 KB | 495,500 B | 80% | Landscape: the band runs to the top edge, 134 px row panel beneath (logo / rule / headline + rotating subline / CTA) |
| 480x320 | 219 KB | 150,650 B | 31% | The same row structure reduced |
| 970x250 | 245 KB | 174,369 B | 35% | Billboard |
| 320x480 | 182 KB | 110,615 B | 26% | Portrait, the master proportions at 320 wide |
| 300x600 | 202 KB | 130,898 B | 29% | Half page, 300x300 band |

Each folder zips with `index.html` at its root (6 files: the page, `bg.jpg`,
`photo1`-`photo4.jpg`).
Beside each is a 1x backup still, `*_backup.jpg`, for placements that cannot run HTML5.

## Copy on file

- Eyebrow — **Premier Offering**
- Headline — **11850 N 5th E**
- Sub 1 — **Idaho Falls, Idaho**
- Sub 2 — **25 acres | 7,000 SF event center**
- Sub 3 — **Listed by Mel Biggs**
- CTA — **Schedule a viewing** (sentence case, per the Aperture standard)
- clickTag → `https://www.apertureglobal.com/`

Copy is baked to SVG outline paths, so changing any line means a rebuild, not an edit to
`index.html`.

## Build

Generated, never hand-edited. Editing a unit's `index.html` is reverted by the next rebuild.

    python3 kenburns_build.py --order "<order folder>" --overrides overrides/<slug>.json \
      --folder 11850N5thE-IdahoFalls-ID --clicktag-slug <lofty-slug> --photos <six, in order>

The builder lives in `~/Documents/Claude/aperture-digital-ads`. Running order of the stills:

1. `exterior-27.jpg`
2. `living-10.jpg`
3. `amenities-04.jpg`
4. `interior-02.jpg`

Each still holds 3.75 s across the 15 s pass, with a 0.8 s crossfade into the next. One
extra layer repeats still 1 so the loop closes without a seam.

## Verified

Real browser, served over HTTP. For every one of the six sizes: each still is the top visible
layer at its own midpoint; the wrap layer reaches full opacity at 15 s; no moment of the pass
is blank; the eyebrow mark and text are centred in the unit; and no unit carries a video
element, an autoplay watchdog or any JavaScript beyond the clickTag shim. No unit makes an
external request of any kind. Every unit is under the 700 KB budget.
