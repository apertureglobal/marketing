#!/usr/bin/env python3
"""
Generates florida-radius.svg for the 2961 Lakeview Drive direct mail strategy.

Local equirectangular projection centred on the subject property. Draws the
Florida state outline as a hairline, concentric distance rings from the
residence, and market markers. Also prints the marker positions as percentages
of the SVG frame, for the absolutely-positioned label overlay in the HTML.

Source outline: glynnbird/usstatesgeojson florida.geojson (public domain,
US Census cartographic boundary derivative). A copy is cached beside this
script as florida.geojson; delete it to re-fetch.
"""
import json, math, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "florida.geojson")
SRC = "https://raw.githubusercontent.com/glynnbird/usstatesgeojson/master/florida.geojson"

SUBJECT = (27.506872, -81.465173)          # 2961 Lakeview Drive, Sebring FL 33870
RINGS_MI = [25, 50, 75, 100]

# Labelled markets. (name, lat, lon)
MARKETS = [
    ("Lakeland",                    28.0395, -81.9498),
    ("Orlando / Winter Park",       28.6000, -81.3392),
    ("Tampa",                       27.9203, -82.4937),
    ("Sarasota / Longboat Key",     27.3364, -82.5307),
    ("Vero Beach",                  27.6386, -80.3973),
    ("Stuart / Sewall's Point",     27.1973, -80.2528),
]

# Explicit lat/lon frame, cropped to the peninsula. The Census outline carries
# the panhandle, which is irrelevant here and would push the subject property
# into the right-hand third of the frame and leave no room for labels.
LAT_MIN, LAT_MAX = 25.40, 29.75
LON_MIN, LON_MAX = -83.70, -79.00

W, H = 500.0, 522.0          # SVG user units
INK, HAIR, ACCENT = "#0E1113", "#D8CFC6", "#B2C6D6"


def fetch():
    if not os.path.exists(CACHE):
        with urllib.request.urlopen(SRC, timeout=40) as r:
            open(CACHE, "wb").write(r.read())
    d = json.load(open(CACHE))
    g = d["geometry"] if "geometry" in d else d
    if g.get("type") == "FeatureCollection":
        g = g["features"][0]["geometry"]
    return g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]


def miles(lat1, lon1, lat2, lon2):
    R = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def main():
    polys = fetch()
    rings = [r for poly in polys for r in poly]

    # Local equirectangular: x scaled by cos(centre latitude) so distances are
    # true near the subject and rings render as true circles.
    k = math.cos(math.radians(SUBJECT[0]))
    lat_mi = 69.055                      # miles per degree latitude

    def proj(lat, lon):
        return ((lon - SUBJECT[1]) * k * lat_mi, -(lat - SUBJECT[0]) * lat_mi)

    x0, _ = proj(LAT_MAX, LON_MIN)
    _, y0 = proj(LAT_MAX, LON_MIN)
    x1, _ = proj(LAT_MIN, LON_MAX)
    _, y1 = proj(LAT_MIN, LON_MAX)
    sx, sy = W / (x1 - x0), H / (y1 - y0)
    s = min(sx, sy)
    ox = (W - (x1 - x0) * s) / 2 - x0 * s
    oy = (H - (y1 - y0) * s) / 2 - y0 * s

    def px(lat, lon):
        x, y = proj(lat, lon)
        return x * s + ox, y * s + oy

    def inside(lat, lon):
        return LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
           f'width="{W:.0f}" height="{H:.0f}">']

    cx, cy = px(*SUBJECT)
    out.append('  <g fill="none" stroke="%s" stroke-width="0.7">' % HAIR)
    for mi in RINGS_MI:
        out.append(f'    <circle cx="{cx:.2f}" cy="{cy:.2f}" r="{mi * s:.2f}" '
                   f'stroke-dasharray="1.6 3.2"/>')
    out.append('  </g>')

    out.append('  <g fill="none" stroke="#B9B2A8" stroke-width="0.9" '
               'stroke-linejoin="round">')
    for r in rings:
        # Break each ring into runs of points inside the frame, so the
        # cropped-away panhandle leaves no stray chord across the map.
        run = []
        for lon, lat in list(r) + [(None, None)]:
            if lat is not None and inside(lat, lon):
                run.append("%.2f,%.2f" % px(lat, lon))
                continue
            if len(run) > 1:
                out.append('    <polyline points="%s"/>' % " ".join(run))
            run = []
    out.append('  </g>')

    # Ring captions, stacked due north of the subject.
    out.append('  <g font-family="Inter,sans-serif" font-size="7" '
               'letter-spacing="1.1" fill="#A79F98">')
    for mi in RINGS_MI:
        out.append(f'    <text x="{cx + 3:.2f}" y="{cy - mi * s + 9:.2f}">'
                   f'{mi} MI</text>')
    out.append('  </g>')

    out.append('  <g>')
    for name, lat, lon in MARKETS:
        mx, my = px(lat, lon)
        out.append(f'    <circle cx="{mx:.2f}" cy="{my:.2f}" r="3.1" fill="{ACCENT}"/>')
    out.append(f'    <circle cx="{cx:.2f}" cy="{cy:.2f}" r="4.6" fill="none" '
               f'stroke="{INK}" stroke-width="0.8"/>')
    out.append(f'    <circle cx="{cx:.2f}" cy="{cy:.2f}" r="2.1" fill="{INK}"/>')
    out.append('  </g>')
    out.append('</svg>')

    dest = os.path.join(HERE, "florida-radius.svg")
    open(dest, "w").write("\n".join(out) + "\n")
    print("wrote", dest)

    print("\n--- overlay percentages (left%, top%) ---")
    print('%-26s %7s %7s  %s' % ("MARKET", "LEFT", "TOP", "STRAIGHT-LINE MI"))
    for name, lat, lon in [("2961 Lakeview Drive", *SUBJECT)] + MARKETS:
        mx, my = px(lat, lon)
        print('%-26s %6.2f%% %6.2f%%  %6.1f' % (
            name, mx / W * 100, my / H * 100, miles(*SUBJECT, lat, lon)))


if __name__ == "__main__":
    main()
