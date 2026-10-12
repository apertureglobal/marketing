# Aperture Global · Priory Walk, London, SW10 9SP · HTML5 display ads

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
| 768x1024 | video | 663 KB | 588,120 | 95% |
| 1024x768 | video | 672 KB | 596,929 | 96% |
| 480x320 | video | 656 KB | 588,588 | 94% |
| 970x250 | video | 656 KB | 585,717 | 94% |
| 320x480 | video | 653 KB | 582,783 | 93% |
| 300x600 | video | 651 KB | 580,575 | 93% |
| 768x1024 | carousel | 499 KB | 423,602 | 71% |
| 1024x768 | carousel | 646 KB | 574,856 | 92% |
| 480x320 | carousel | 263 KB | 189,122 | 38% |
| 970x250 | carousel | 298 KB | 222,206 | 43% |
| 320x480 | carousel | 211 KB | 133,145 | 30% |
| 300x600 | carousel | 231 KB | 154,141 | 33% |

Each folder zips with `index.html` at its root, beside its own background, four photographs and,
for video units, the mp4. Beside each folder is a backup still, `*_backup.jpg`.

## Copy on file

- Eyebrow: **Premier Offering**
- Headline: **Priory Walk**
- Sub 1: **London, SW10 9SP**
- Sub 2: **6 bed | 5 bath | 3,853 sq ft**
- Sub 3: **Caroline De Havillande & Anna Cosio**
- CTA: **Schedule a viewing**
- clickTag: `https://www.apertureglobal.com/priorywalkkensington`, overridable per placement with `?clicktag=<url>`

Photographs, in order: the full stucco terrace frontage, the garden level reception with the
sculpted staircase and glazed rear extension, the kitchen with its walnut cabinetry and angled
island, the rear garden and terrace.
