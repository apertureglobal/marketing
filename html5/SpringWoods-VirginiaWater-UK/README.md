# Aperture Global · Spring Woods, Wentworth Estate, Virginia Water, Surrey, GU25 · HTML5 display ads

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
| 768x1024 | video | 662 KB | 576,855 | 95% |
| 1024x768 | video | 679 KB | 595,111 | 97% |
| 480x320 | video | 653 KB | 575,638 | 93% |
| 970x250 | video | 658 KB | 577,381 | 94% |
| 320x480 | video | 642 KB | 562,487 | 92% |
| 300x600 | video | 646 KB | 566,547 | 92% |
| 768x1024 | carousel | 550 KB | 465,668 | 79% |
| 1024x768 | carousel | 639 KB | 558,567 | 91% |
| 480x320 | carousel | 288 KB | 204,960 | 41% |
| 970x250 | carousel | 333 KB | 247,745 | 48% |
| 320x480 | carousel | 228 KB | 141,387 | 33% |
| 300x600 | carousel | 255 KB | 168,548 | 36% |

Each folder zips with `index.html` at its root, beside its own background, four photographs and,
for video units, the mp4. Beside each folder is a backup still, `*_backup.jpg`.

## Copy on file

- Eyebrow: **Premier Offering**
- Headline: **Spring Woods**
- Sub 1: **Wentworth Estate, Virginia Water, GU25**
- Sub 2: **6 bed | 7 bath | 7,970 sq ft**
- Sub 3: **Caroline De Havillande & Anna Cosio**
- CTA: **Schedule a viewing**
- clickTag: `https://www.apertureglobal.com/springlodge`, overridable per placement with `?clicktag=<url>`

Photographs, in order: front elevation and circular drive, kitchen opening to the orangery,
curtained bay with window seat in the reception, thatched gazebo in the garden.
