# 2C Summit View - 302C Dr — HTML5 display ads

Aperture Global Real Estate · English · 12 units

## Open this first

`SummitView302C-preview/index.html` — double-click it. Every unit plays in one page.
No server and no internet connection required.

Each card has play/pause, replay and a 15-second scrubber, plus **Replay all** and
**Last frame** in the header, a link to open that unit on its own, its zipped weight, and its
backup still. Each unit loops every 7.5 s; the preview plays two loops then holds.

The units are inlined into the page, so the controls work straight off the disk rather than
needing a local server.

## What's in the set

| | |
|---|---|
| **Sizes** | 768×1024, 1024×768, 480×320, 970×250, 320×480, 300×600 |
| **Variants** | video — 12 units |
| **Loop** | 15 seconds, looping continuously |
| **Weight** | every unit under the 700 KB cap (largest: 1024x768 video, 665 KB) |
| **Click-through** | the underlined CTA only — not the whole ad |

**Video** units play the walkthrough as a silent 15-second loop. The four listing photos sit
underneath as the autoplay fallback, with arrows, dots and swipe.

## Copy

| | English |
|---|---|
| Eyebrow | Premier Offering |
| Headline | 2C Summit View - 302C Dr |
| Location | Big Sky, MT 59716 |
| Spec | 3 bed \| 3 bath \| 1,918 sq ft |
| Agents | Listed by Mazie & Suzanne Schreiner |
| CTA | Schedule a viewing |

All copy is baked to vector outlines, so the units carry no webfonts and render identically
everywhere. The faces are the Aperture ones — Cormorant Garamond for the headline and
eyebrow, Archivo for everything else.

## Notes for whoever traffics these

- **clickTag** defaults to `apertureglobal.com` and can be overridden per placement by
  appending `?clicktag=<url>` to the unit's URL. Built for StackAdapt; the same
  convention works on most DSPs.
- **Autoplay fallback.** The video units carry the photo carousel underneath them. If a
  browser refuses to autoplay — Safari in Low Power Mode, or "Never Auto-Play" — the unit
  switches to the interactive carousel instead of showing a frozen frame. Tested in both
  states.
- **Backup stills** are included for every unit (`*_backup.jpg`), for placements that need
  a static fallback.
- **Shippable zips** are in `zips/`, one per unit, with the ad HTML renamed to `index.html`.

## Reviewing on a phone

Open `index.html` on the phone itself, or view a single unit full-screen with the "open
alone" link on its card. The swipe hint on the photo band only appears on touch devices,
and disappears after the first manual swipe.
