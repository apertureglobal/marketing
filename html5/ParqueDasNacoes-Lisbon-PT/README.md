# Aperture Global · Parque das Nações, Lisbon · HTML5 display ads

Twenty four units: six sizes, each as video and carousel, each in English and Portuguese.
This is the bilingual set as delivered, not a rebuild.

Preview page: **[preview.html](preview.html)** — all twenty four units on one page.

The delivery note that shipped with the set follows, unchanged.

```
Aperture Global Real Estate - Parque das Nacoes - HTML5 display ads, English + Portuguese

24 units: 6 sizes x {video, carousel} x {en, pt}. Every zip is under the 700 KB cap
(largest: 1024x768 video, 666 KB). Open preview.html to review them all in one page.

  APERTURE_ParqueDasNacoes_<size>_<video|carousel>_<en|pt>/
      index.html   the shippable unit, self-contained (no webfonts - copy is vector outlines)
      bg.jpg  photo1-4.jpg  video.mp4 (video units only)

Sizes: 768x1024, 1024x768, 480x320, 970x250, 320x480, 300x600.

COPY
  English                                  Portuguese
  Exclusive Offer                          Oferta Exclusiva
  Parque das Nações                        Parque das Nações
  Lisbon, Portugal                         Lisboa, Portugal
  4 br | 5 bth | 6,500 sqm                 4 br | 5 bth | 6,500 sqm
  Listed by Liza Falcão de Sá &            Listado por Liza Falcão de Sá &
    Charles Andrews                          Charles Andrews
  Schedule a viewing                       Agendar visita

Click-through: only the underlined CTA. clickTag defaults to apertureglobal.com and is
overridable with ?clicktag= on the unit's URL.

WHAT CHANGED FROM THE FIRST PARQUE BUILD (dist/aperture)
This set is on the current template, matching Priory Walk and Embassy Works:
  - CTA hover state (lifts, glows, text and rule go light blue) driven off the click layer
  - mobile swipe hint over the photo band, which disappears after the first manual swipe
  - the fixed autoplay watchdog: it only judges the video while the page is visible and the
    ad is on screen, so a hidden or below-the-fold slot is never mistaken for Low Power Mode
  - 1024x768 and 480x320 rebuilt as the row layout - video to the top edge, then a panel
    with logo | rule | headline + rotating text | CTA, auto-fit so nothing crowds the button
  - 970x250 is the one-pass 15 s story: icon group, then logo, then headline + rotating text,
    ending on the three-group frame
  - CTA set in sentence case
Because the two landscape bands got taller, the photos and video for every size were
re-rendered from source rather than reused.

FALLBACK
The video units carry the 4-photo carousel underneath. If autoplay is refused - Safari in
Low Power Mode, or "Never Auto-Play" - the unit switches to the interactive carousel with
arrows, dots and swipe. Verified in both states.

REBUILDING
  python3 ../../tools/serve/rangeserver.py ../.. 8801 &
  AP_MEDIA=<media dir> ../../tools/aperture/build_parque.sh
  python3 make-preview.py && python3 make-preview.py --site
Media is regenerated with tools/aperture/make_media.py from dist/aperture/ParqueDasNacoes
(stills 1-4.jpg, clips 1.mp4 and 2.mp4 - 7.5 s of each fills the 15 s loop).
Copy is baked to outlines with tools/aperture/bake_set.py.
```
