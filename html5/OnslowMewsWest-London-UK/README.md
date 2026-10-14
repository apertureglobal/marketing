# Aperture Global · Onslow Mews West, London, SW7 3AF · HTML5 display ads

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
| 768x1024 | video | 651 KB | 563,306 | 93% |
| 1024x768 | video | 662 KB | 574,143 | 95% |
| 480x320 | video | 647 KB | 566,445 | 92% |
| 970x250 | video | 648 KB | 564,925 | 93% |
| 320x480 | video | 650 KB | 567,555 | 93% |
| 300x600 | video | 643 KB | 560,461 | 92% |
| 768x1024 | carousel | 458 KB | 368,013 | 65% |
| 1024x768 | carousel | 575 KB | 489,378 | 82% |
| 480x320 | carousel | 252 KB | 164,639 | 36% |
| 970x250 | carousel | 279 KB | 188,853 | 40% |
| 320x480 | carousel | 216 KB | 125,251 | 31% |
| 300x600 | carousel | 240 KB | 149,293 | 34% |

Each folder zips with `index.html` at its root, beside its own background, four photographs and,
for video units, the mp4. Beside each folder is a backup still, `*_backup.jpg`.

## Copy on file

- Eyebrow: **Premier Offering**
- Headline: **Onslow Mews West**
- Sub 1: **South Kensington, London SW7 3AF**
- Sub 2: **3 bed | 2 bath | 1,249 sq ft**
- Sub 3: **Listed by Caroline De Havillande & Anna Cosio**
- CTA: **Schedule a viewing**
- clickTag: `https://www.apertureglobal.com/onslowmewswest`, overridable per placement with `?clicktag=<url>`

Photographs, in order: the mews frontage with its balcony and garage, the reception room with
its fireplace, the kitchen under its skylight, and the private terrace through open doors.
