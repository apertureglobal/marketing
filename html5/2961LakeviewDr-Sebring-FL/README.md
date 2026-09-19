# Aperture Global · 2961 Lakeview Drive, Sebring FL · HTML5 display ads

Ten self-contained HTML5 units in the **"faux video"** style: no video file anywhere in the
package. Each unit is built from six listing stills, and a slow CSS pan/zoom (Ken Burns)
crossfades one into the next so the photo band reads as a slowly moving camera.

Preview page: **[preview.html](preview.html)** — all ten units on one page with play/pause,
replay and a 15 s scrubber.

## Units

**Core six** — the established Aperture set, one layout each:

| Size | Zip | % of 700 KB budget | Role |
|---|---:|---:|---|
| 768×1024 | 497,603 B | 71% | master; header, 768×473 band, copy stack below |
| 1024×768 | 649,754 B | 92% | band to the top edge, 134 px row panel |
| 480×320 | 219,032 B | 31% | same row structure, reduced |
| 970×250 | 268,821 B | 38% | billboard; photo left, one-pass story right |
| 320×480 | 136,624 B | 19% | portrait, master proportions |
| 300×600 | 173,456 B | 24% | half page, 300×300 band |

**Added four** — adapted from the closest-proportion layout above, not newly invented:

| Size | Zip | % of budget | Adapted from |
|---|---:|---:|---|
| 300×250 | 95,798 B | 13% | the 320×480 centred stack at 250 tall (its ~17/42/41 split) |
| 728×90 | 82,758 B | 11% | the 480×320 row panel, photo moved left as on 970×250 |
| 160×600 | 116,609 B | 16% | the 300×600 vertical structure exactly, at 160 wide |
| 320×50 | 42,190 B | 6% | the same row as 728×90, smallest usable scale |

Each folder zips with `index.html` at its root (8 files: the page, `bg.jpg`, `photo1–6.jpg`).
Beside each is a 1× backup still, `*_backup.jpg`, for placements that cannot run HTML5.

## Copy on file

Verified against the live Stellar MLS listing **#O6431426**. Nothing here was inferred.

- Eyebrow — **Premier Listing**
- Headline — **2961 Lakeview Drive**
- Sub 1 — **Sebring, Florida**
- Sub 3 — **5 br | 10 bth | 10,648 sq ft | 1.74 acres**
- Sub 4 — **Listed by Cynde Velez**
- CTA — **Schedule a viewing** (sentence case, per the Aperture standard)
- clickTag → `https://www.apertureglobal.com/2961lakeviewdrive`

The `|` dividers in the spec line bake at **50% opacity** — house rule across every Aperture
brand and property, recorded in the toolchain's `DIGITAL-ADS.md` §6 and implemented in the
shared emitter `run_svg()` in `bake_set.py`. The figures stay at full strength.

Copy is baked to SVG outline paths (fragment set key `lv`), so changing any line — including
the divider opacity — means a re-bake with `bake_set.py` and a rebuild, not an edit to
`index.html`.

## Build

Generated, never hand-edited. Editing a unit's `index.html` is reverted by the next rebuild.

    tools/aperture/build_lakeview.sh                    # all ten sizes
    tools/aperture/build_lakeview.sh 1024x768           # one size
    python3 tools/aperture/make_preview_lakeview.py <this folder>

Both scripts live in the `animatedads` toolchain (`k4design.github.io/animatedads/`), not in
this repo. Source stills are `properties/2961LakeviewDr-Sebring-FL/1.jpg`–`6.jpg`.

**Cut order is `2,1,6,3,4,5`** — facade, aerial lake, loggia, grand living, fireplace salon,
car gallery. Each still holds 2.5 s across the 15 s pass.

## Assumptions — worth a second look

1. **Sizes — read this before trafficking.** Every live Aperture display campaign on
   StackAdapt traffics **exactly the same six sizes**: 1024×768, 970×250, 768×1024,
   480×320, 320×480, 300×600. Verified against six separate campaigns spanning US and UK
   properties (203 Lakeridge, 23205 Logan Canyon, 72 Mount Pleasant, Alston Urban
   Residences, Greenacre, 3000 Poston Ave, 70 Calabria Court) — none of them runs 300×250,
   728×90, 160×600 or 320×50. The campaign automation's checklist wording ("upload the ten
   creative sizes") does **not** correspond to ten distinct pixel dimensions in anything
   currently running.

   The added four are therefore **net-new inventory**, not a gap being closed. They were
   built on explicit direction. 6 + 4 = 10, which makes the checklist count work, but that
   is arithmetic, not confirmation — **320×50 in particular is an inference**, not
   something any Aperture campaign or spec document names.
2. **Eyebrow.** The listing carries no eyebrow line. "Premier Listing" was chosen to match
   Priory Walk, Lake Mills and Trophy Bull. One re-bake to change.
3. **No price in the creative.** $4,850,000 is the price of record but, as with every other
   Aperture unit, it is not shown. The units are deliberately price-free.
4. **Bathrooms shown as "10 bth"** — the MLS counts 8 full + 2 half. The spec line follows
   the house format rather than spelling the split out.
5. **JPEG quality is the only budget lever here**, since there is no video bitrate to trade
   against. 1024×768 runs at q40 and is the tight unit at 92% of budget; the other five of
   the core six sit at q56–q62. Adding a seventh still, or raising 1024×768 above q40,
   would push it over. The added four have small bands, so they run at q72–q78 and still
   land at 6–16% of budget — there is no budget pressure anywhere in that group.
6. **Backup stills** are taken at 3.8 s — the lake hero beat with the spec line showing —
   except 970×250, whose single-pass story is only fully composed at its 13.5 s end frame.
7. **No "onepage" bundle** was produced; it was excluded from this request.
8. **320×50 legibility.** The rotating subline
   ("5 br | 10 bth | 10,648 sq ft | 1.74 acres") renders about 5 px tall at 1×. The
   headline and CTA are fine; that one line is at or below the legibility floor. This is
   the row layout's auto-fit working correctly with four elements in 320 px, not a bug.
   Two clean fixes if it matters: drop the sublines on 320×50 and hold the headline, or use
   an icon-only lockup instead of the full wordmark to buy back roughly 90 px. Both are
   design calls, so neither was made here.
9. **`bg.jpg` for the added four** is cover-cropped from the nearest-aspect shipped
   background (`kb_bg.py`), since the brand artwork only ships at the original six sizes.
   A cover crop is a uniform scale plus a crop, so the diagonals keep their angle.

## Verified

Real browser, served over HTTP: all ten units report no broken images, animations running,
and still running past one full 15 s period (22 live animations at 18 s, none paused — the
loop-handover bug fixed in Sept 2026 does not recur here, and these units carry no video
element or autoplay watchdog at all). Every link on the preview page returns 200. No unit
makes an external request of any kind.
