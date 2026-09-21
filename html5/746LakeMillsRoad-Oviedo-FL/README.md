# Aperture Global — 746 Lake Mills Road, Oviedo FL — HTML5 display ads

Six units, the core six sizes every live Aperture display campaign traffics. Every zip is
well under the 700 KB cap (largest: 1024x768 at 611,939 B). Open `preview.html` to review
all six on one page with play/pause, replay and a 15 s scrubber.

    APERTURE_746LakeMillsRoad_<size>/
        index.html   the shippable unit, self-contained (copy is vector outlines, no webfonts)
        bg.jpg  photo1-5.jpg

| Size | Zip | Layout |
|---|---|---|
| 768x1024 | 411,015 B | master — header, 768x473 photo band, copy stack below |
| 1024x768 | 611,939 B | band to the top edge, 134 px row panel beneath |
| 480x320 | 168,387 B | the same row structure reduced |
| 970x250 | 213,194 B | billboard — photo left (592 px), a single 15 s story right |
| 320x480 | 107,061 B | portrait, the master proportions at 320 wide |
| 300x600 | 131,277 B | half page, 300x300 band |

`300x250`, `728x90`, `160x600` and `320x50` are **not** part of this campaign and are not
built here.

## Copy

    eyebrow   Premier Listing
    headline  Lakefront / Equestrian Estate   (two lines, full size)
    location  746 Lake Mills Road, Oviedo
    spec      6 br | 8 bth | 5,776 sq ft | 15.06 acres
    agent     Listed by Cynde Velez
    CTA       Schedule a viewing  ->  https://www.apertureglobal.com/746lakemillsroad

Source: the Aperture listing page for this property. Price of record $4,500,000 — the ads
display no price, per house convention, so nothing here depends on it.

**Address form.** The listing page titles this property "746/0 Lake Mills Road", the `/0`
reflecting the second of the two contiguous parcels. The creative uses the plain
**746 Lake Mills Road**, which is how the property was briefed. Changing it is one re-bake
of `sub1` plus a rebuild.

**Eyebrow.** The listing's own eyebrow is "Lakefront Equestrian Estate" — but that is
already the headline, verbatim, and it appears in the same frame as the eyebrow on every
size. Using it twice would read as a mistake, so the eyebrow stays **"Premier Listing"** and
the listing's own language carries the headline, where it has the most weight. One re-bake
to change if you would rather have the repetition.

## Faux video

There is no video file and no footage for this property. Each unit is a CSS Ken Burns pass
over the listing stills: every still is rendered at 1.1x its band and animated with a slow
eased pan/zoom, crossfading into the next, so the band reads as a slowly moving camera
rather than a slideshow. Because there is no `<video>` element there is no autoplay
fallback and no carousel tier — the motion cannot be refused.

**Five stills, in their numbered order (1, 2, 3, 4, 5)** — a deliberate direction:
sequential as numbered, not a curated cut order.

1. aerial over the residence — paddocks, sand riding arena, barn, winding drive
2. the great room — stacked-stone fireplace, coffered ceiling, open kitchen beyond
3. the stable interior — four stalls
4. wide aerial over the estate to the Lake Mills frontage
5. the dock at sunset, through the cypress

It opens wide on the land, moves inside, makes the equestrian point, pulls back out to the
lake and closes on the water — which is a coherent arc without any reordering, so nothing
was lost by taking the stills as numbered.

**Timing.** 15 s / 5 stills = **3.0 s per still**, with a 0.8 s crossfade into each
successor. The cuts land at 3.0, 6.0, 9.0 and 12.0 s; a duplicate of still 1 rides on top
for the last 0.8 s so the wrap at 15 s hands back to the frame the cycle opens with. The
composer derives all of this from the still count, so nothing is hard-coded to five. Six
stills would have given 2.5 s each; five at 3.0 s hold slightly longer, which suits a set
whose photographs are wide and slow.

The loop runs **infinitely** — the Aperture exception. (`preview.html` deliberately plays
two loops then holds, so you can inspect the last frame; the shipped units do not stop.)

## Photo quality

JPEG quality is the only budget lever here, since there is no video bitrate to trade
against. Five stills instead of six frees about a sixth of the photo payload, and it is
spent on quality rather than left unused: **q62** across the board — the documented
ceiling — with **1024x768 held at q56**. That size carries the largest band and is always
the tight one; q62 fits at 663 KB but leaves only 36 KB of margin, while q56 lands at
612 KB with ~88 KB, which is the right trade.

## Type

Copy is baked to SVG outline paths, so the units need no webfonts and make no external
request of any kind. The two-line headline is set at full size with 0.86 em leading rather
than being shrunk to one line.

- The **`|` dividers in the spec line are at 50% opacity**, so the pipes separate the
  figures without competing with them. House rule, applied at bake time.
- **970x250 centres every beat** in its right-hand panel — hero group, wordmark, headline,
  sublines and CTA, on every beat and in the final frame. House rule.
- Consequently the two-line headline takes its **flush-left** setting on the row layouts
  (1024x768 and 480x320), which are left-aligned compositions, and its **centred** setting
  on 970x250. Verified in the shipped files, not assumed: the flush-left twin appears in
  1024x768 and 480x320 only, and the centred one in the other four.

## Trafficking

- One `index.html` at each zip root, every asset flat beside it, no subdirectories.
- `ad.size` meta tag per unit; `clickTag` overridable per placement with `?clicktag=<url>`.
- **Only the underlined "Schedule a viewing" is clickable** — not the whole unit. Verified
  by hit-testing the photo band, headline area and panel, none of which are click targets.
- `_backup.jpg` beside each unit is the static backup still, rendered at 13 s (the final
  hold).

## Rebuilding

The units are generated — never hand-edit a unit's `index.html`, because the next rebuild
silently reverts it. Change the fragments or the composer and rebuild:

    animatedads/tools/aperture/build_lakemills_faux.sh            # all six, or pass sizes
    python3 animatedads/tools/aperture/make_preview_lakemills.py .   # run in this folder

The copy fragments are the `lm` set in `animatedads/tools/aperture/assets/`; re-bake with
`bake_set.py lm '{...}'`, passing the headline as a two-element list to keep it on two
lines and to regenerate the flush-left twin.
