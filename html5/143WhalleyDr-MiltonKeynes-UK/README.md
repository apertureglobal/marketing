# Aperture Global · 143 Whalley Drive, Bletchley, Milton Keynes, MK3 6HX · HTML5 display ads

Twelve self-contained HTML5 units: six sizes, each as a **video** unit and a **carousel** unit.

Preview page: **[preview.html](preview.html)**, all twelve units on one page.

- **Video units** play a fifteen second walkthrough once, then hand over to the photo carousel.
  The walkthrough is a pan and zoom across four listing photographs (no agent footage was
  supplied). The carousel also sits underneath as the fallback if a browser refuses autoplay.
- **Carousel units** are the same ad with the photographs only: the backup for placements where
  the video does not load.
- The copy runs two 7.5 second cycles and then holds; the platform repeats the ad.

## Units

| Size | Variant | Unit | Zip | % of 700 KB budget |
|---|---|---:|---:|---:|
| 768x1024 | video | 659 KB | 584,359 B | 94% |
| 1024x768 | video | 664 KB | 588,848 B | 95% |
| 480x320 | video | 654 KB | 587,429 B | 93% |
| 970x250 | video | 656 KB | 585,899 B | 94% |
| 320x480 | video | 654 KB | 585,114 B | 93% |
| 300x600 | video | 655 KB | 586,370 B | 94% |
| 768x1024 | carousel | 440 KB | 363,284 B | 63% |
| 1024x768 | carousel | 581 KB | 508,626 B | 83% |
| 480x320 | carousel | 240 KB | 165,454 B | 34% |
| 970x250 | carousel | 271 KB | 194,563 B | 39% |
| 320x480 | carousel | 199 KB | 121,097 B | 28% |
| 300x600 | carousel | 214 KB | 136,832 B | 31% |

Each folder zips with `index.html` at its root, beside its own background, four photographs and,
for video units, the mp4. Beside each folder is a backup still, `*_backup.jpg`.

## Copy on file

- Eyebrow: **Premier Offering**
- Headline: **143 Whalley Dr**
- Sub 1: **Bletchley, Milton Keynes, MK3 6HX**
- Sub 2: **5 bed | 3 bath | 2,394 sq ft**
- Sub 3: **Listed by Krishan Mistry**
- CTA: **Schedule a viewing**
- clickTag: `https://www.apertureglobal.com/143whalleydrive`, overridable per placement with `?clicktag=<url>`

Photographs, in order: front elevation at twilight, sitting room through to dining, breakfast
bar, rear garden at twilight.
