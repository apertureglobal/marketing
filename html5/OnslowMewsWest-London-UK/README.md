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
| 768x1024 | video | 650 KB | 566,147 | 93% |
| 1024x768 | video | 660 KB | 575,984 | 94% |
| 480x320 | video | 644 KB | 568,078 | 92% |
| 970x250 | video | 655 KB | 575,592 | 94% |
| 320x480 | video | 651 KB | 572,229 | 93% |
| 300x600 | video | 642 KB | 563,246 | 92% |
| 768x1024 | carousel | 452 KB | 365,481 | 65% |
| 1024x768 | carousel | 569 KB | 487,003 | 81% |
| 480x320 | carousel | 246 KB | 162,871 | 35% |
| 970x250 | carousel | 273 KB | 186,288 | 39% |
| 320x480 | carousel | 210 KB | 122,768 | 30% |
| 300x600 | carousel | 234 KB | 146,865 | 33% |

Each folder zips with `index.html` at its root, beside its own background, four photographs and,
for video units, the mp4. Beside each folder is a backup still, `*_backup.jpg`.

## Copy on file

- Eyebrow: **Premier Offering**
- Headline: **Onslow Mews West**
- Sub 1: **South Kensington, London SW7 3AF**
- Sub 2: **3 bed | 2 bath | 1,249 sq ft**
- Sub 3: **Listed by De Havillande Cosio Team**
- CTA: **Schedule a viewing**
- clickTag: `https://www.apertureglobal.com/onslowmewswest`, overridable per placement with `?clicktag=<url>`

Photographs, in order: the mews frontage with its balcony and garage, the reception room with
its fireplace, the kitchen under its skylight, and the private terrace through open doors.
