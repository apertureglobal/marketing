#!/usr/bin/env python3
"""
Generates lakemills-radius.svg for the 746 Lake Mills Road direct mail strategy.

Local equirectangular projection centred on the subject property, so the
distance rings render as true circles and short distances are accurate.
Draws the Central Florida county boundaries as hairlines, fills the subject's
own county, adds concentric distance rings from the residence, and plots the
mailing markets. Also prints each marker as a percentage of the SVG frame,
for the absolutely-positioned label overlay in the HTML.

Source outline: plotly/datasets geojson-counties-fips.json, a derivative of the
US Census cartographic county boundaries (public domain). A copy is cached
beside this script as us-counties.json; delete it to re-fetch.

Subject county was verified independently of the source data, via the US Census
Geocoder (address lookup and reverse coordinate lookup both return Seminole
County, FIPS 12117, Oviedo CCD, no incorporated place).
"""
import json, math, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "us-counties.json")
SRC = ("https://raw.githubusercontent.com/plotly/datasets/master/"
       "geojson-counties-fips.json")

SUBJECT = (28.628129, -81.114332)   # 746 Lake Mills Road, Oviedo FL 32766
SUBJECT_FIPS = "12117"              # Seminole County
RINGS_MI = [10, 20, 30, 40]

# Counties drawn as hairlines: the Orlando region plus its immediate ring.
COUNTIES = ["12117", "12095", "12069", "12097", "12127",
            "12009", "12105", "12119", "12083"]

# Labelled markets. (name, lat, lon)
MARKETS = [
    ("Geneva",                      28.7397, -81.1176),
    ("Oviedo",                      28.6700, -81.2081),
    ("Sanford",                     28.8006, -81.2731),
    ("Lake Mary / Heathrow",        28.7589, -81.3178),
    ("Longwood / Markham Woods",    28.7031, -81.3703),
    ("Winter Park",                 28.6000, -81.3392),
    ("Orlando",                     28.5383, -81.3792),
    ("Windermere / Winter Garden",  28.5300, -81.5600),
    ("Clermont / Groveland",        28.5530, -81.8100),
    ("Lake Nona",                   28.3772, -81.2497),
    ("St. Cloud",                   28.2489, -81.2812),
    ("Christmas / Lake Pickett",    28.5361, -81.0139),
]

LAT_MIN, LAT_MAX = 27.98, 29.25
LON_MIN, LON_MAX = -81.95, -80.50

W, H = 500.0, 500.0
INK, HAIR, ACCENT = "#0E1113", "#D8CFC6", "#B2C6D6"
COUNTY_LINE, COUNTY_FILL = "#CFC6BC", "#E4DCD2"
LAND_FILL = "#F1EDE7"   # every county, so land reads against the Atlantic


def fetch():
    if not os.path.exists(CACHE):
        with urllib.request.urlopen(SRC, timeout=60) as r:
            open(CACHE, "wb").write(r.read())
    d = json.load(open(CACHE))
    out = {}
    for f in d["features"]:
        fips = f["properties"]["STATE"] + f["properties"]["COUNTY"]
        if fips not in COUNTIES:
            continue
        g = f["geometry"]
        polys = (g["coordinates"] if g["type"] == "MultiPolygon"
                 else [g["coordinates"]])
        out[fips] = [r for poly in polys for r in poly]
    return out


def miles(lat1, lon1, lat2, lon2):
    R = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def main():
    counties = fetch()

    k = math.cos(math.radians(SUBJECT[0]))
    lat_mi = 69.055

    def proj(lat, lon):
        return ((lon - SUBJECT[1]) * k * lat_mi, -(lat - SUBJECT[0]) * lat_mi)

    x0, y0 = proj(LAT_MAX, LON_MIN)
    x1, y1 = proj(LAT_MIN, LON_MAX)
    s = min(W / (x1 - x0), H / (y1 - y0))
    ox = (W - (x1 - x0) * s) / 2 - x0 * s
    oy = (H - (y1 - y0) * s) / 2 - y0 * s

    def px(lat, lon):
        x, y = proj(lat, lon)
        return x * s + ox, y * s + oy

    def path(ring):
        # Full geometry, unclamped. Everything is drawn inside a clipPath on the
        # frame rect instead: clamping stray vertices to the frame edge folds
        # the out-of-frame parts of a county into false straight boundaries.
        return " ".join("%.2f,%.2f" % px(lat, lon) for lon, lat in ring)

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
           f'width="{W:.0f}" height="{H:.0f}">',
           f'  <clipPath id="frame"><rect x="0" y="0" width="{W:.0f}" '
           f'height="{H:.0f}"/></clipPath>',
           '  <g clip-path="url(#frame)">']

    # Land first: every county filled, so the Atlantic reads as empty.
    out.append(f'  <g fill="{LAND_FILL}" stroke="none">')
    for fips in COUNTIES:
        for ring in counties.get(fips, []):
            out.append(f'    <polygon points="{path(ring)}"/>')
    out.append('  </g>')

    # Subject county, filled a shade darker.
    for ring in counties.get(SUBJECT_FIPS, []):
        out.append(f'  <polygon points="{path(ring)}" fill="{COUNTY_FILL}" '
                   f'stroke="none"/>')

    # County hairlines over the fills.
    out.append(f'  <g fill="none" stroke="{COUNTY_LINE}" stroke-width="0.7" '
               'stroke-linejoin="round">')
    for fips in COUNTIES:
        for ring in counties.get(fips, []):
            out.append(f'    <polygon points="{path(ring)}"/>')
    out.append('  </g>')

    # Subject county emphasised.
    out.append('  <g fill="none" stroke="#A79F98" stroke-width="1.2" '
               'stroke-linejoin="round">')
    for ring in counties.get(SUBJECT_FIPS, []):
        out.append(f'    <polygon points="{path(ring)}"/>')
    out.append('  </g>')

    cx, cy = px(*SUBJECT)
    out.append(f'  <g fill="none" stroke="#B8AFA5" stroke-width="0.7">')
    for mi in RINGS_MI:
        out.append(f'    <circle cx="{cx:.2f}" cy="{cy:.2f}" r="{mi * s:.2f}" '
                   f'stroke-dasharray="1.6 3.2"/>')
    out.append('  </g>')

    # Ring captions, stacked due north of the subject.
    out.append('  <g font-family="Inter,sans-serif" font-size="7" '
               'letter-spacing="1.1" fill="#A79F98">')
    for mi in RINGS_MI:
        out.append(f'    <text x="{cx + 3.5:.2f}" y="{cy - mi * s + 9:.2f}">'
                   f'{mi} MI</text>')
    out.append('  </g>')

    out.append('  <g>')
    for name, lat, lon in MARKETS:
        mx, my = px(lat, lon)
        out.append(f'    <circle cx="{mx:.2f}" cy="{my:.2f}" r="3.1" '
                   f'fill="{ACCENT}"/>')
    out.append(f'    <circle cx="{cx:.2f}" cy="{cy:.2f}" r="4.6" fill="none" '
               f'stroke="{INK}" stroke-width="0.8"/>')
    out.append(f'    <circle cx="{cx:.2f}" cy="{cy:.2f}" r="2.1" fill="{INK}"/>')
    out.append('  </g>')

    out.append('  </g>')   # close frame clip
    out.append('</svg>')

    dest = os.path.join(HERE, "lakemills-radius.svg")
    open(dest, "w").write("\n".join(out) + "\n")
    print("wrote", dest)

    print("\n--- overlay percentages (left%, top%) ---")
    print('%-28s %7s %7s  %s' % ("MARKET", "LEFT", "TOP", "STRAIGHT-LINE MI"))
    for name, lat, lon in [("746 Lake Mills Road", *SUBJECT)] + MARKETS:
        mx, my = px(lat, lon)
        print('%-28s %6.2f%% %6.2f%%  %6.1f' % (
            name, mx / W * 100, my / H * 100, miles(*SUBJECT, lat, lon)))

    # Off-map markets, for the ledger only.
    print("\n--- off-map (ledger only) ---")
    for name, lat, lon in [("Wellington", 26.6618, -80.2681),
                           ("Loxahatchee Groves", 26.6834, -80.2776),
                           ("Ocala", 29.1872, -82.1401),
                           ("Mount Dora", 28.8025, -81.6473),
                           ("Orlando Intl Airport", 28.4312, -81.3081)]:
        print('%-28s %6.1f mi' % (name, miles(*SUBJECT, lat, lon)))


if __name__ == "__main__":
    main()
