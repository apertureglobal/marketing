# Aperture Global · Cambridge Street, Pimlico, London, SW1V 4QF · HTML5 display ads

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
| 768x1024 | video | 662 KB | 582,602 | 95% |
| 1024x768 | video | 677 KB | 598,800 | 97% |
| 480x320 | video | 655 KB | 584,195 | 94% |
| 970x250 | video | 659 KB | 584,596 | 94% |
| 320x480 | video | 649 KB | 574,767 | 93% |
| 300x600 | video | 656 KB | 582,335 | 94% |
| 768x1024 | carousel | 542 KB | 463,680 | 77% |
| 1024x768 | carousel | 664 KB | 590,434 | 95% |
| 480x320 | carousel | 278 KB | 200,755 | 40% |
| 970x250 | carousel | 313 KB | 233,113 | 45% |
| 320x480 | carousel | 221 KB | 139,826 | 32% |
| 300x600 | carousel | 248 KB | 167,090 | 35% |

Each folder zips with `index.html` at its root, beside its own background, four photographs and,
for video units, the mp4. Beside each folder is a backup still, `*_backup.jpg`.

## Copy on file

- Eyebrow: **Premier Offering**
- Headline: **Cambridge Street**
- Sub 1: **Pimlico, London, SW1V 4QF**
- Sub 2: **5 bed | 6 bath | 3,177 sq ft**
- Sub 3: **Caroline De Havillande & Anna Cosio**
- CTA: **Schedule a viewing**
- clickTag: `https://www.apertureglobal.com/cambridgestreet`, overridable per placement with `?clicktag=<url>`

Photographs, in order: the stucco and brick terrace frontage, the first floor reception with its
full height sash windows, the dining reception with the Miró and marble fireplace, the private
roof terrace.
