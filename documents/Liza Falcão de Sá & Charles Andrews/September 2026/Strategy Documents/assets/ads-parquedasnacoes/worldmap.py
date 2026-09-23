#!/usr/bin/env python3
"""Atlantic frame for this campaign: the Americas, the Atlantic and western Europe
in one picture, because the markets span three continents - Toronto in the north,
Sao Paulo in the south, Zurich in the east. Natural Earth
110m country polygons, Mercator, land FILLED (never stroked - outlines are illegible
once a map this wide sits at page width). Also prints the marker percentages for the
HTML overlay and warns if a marker falls outside the frame."""
import json, math, itertools, os, tempfile, urllib.request

NE_URL = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/"
          "geojson/ne_110m_admin_0_countries.geojson")
# Cached outside the repo: the country data is an input, not a deliverable.
CACHE = os.path.join(tempfile.gettempdir(), "ne_110m_admin_0_countries.geojson")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atlantic.svg")

if not os.path.exists(CACHE):
    urllib.request.urlretrieve(NE_URL, CACHE)

# Latitude is pinned by the markets themselves: London at 51.5N and Sao Paulo at
# 23.6S, so the frame cannot be shallower than this. Longitude is then set to the
# widest span that still keeps London and Paris apart as two readable dots.
LON0, LON1 = -108.0, 44.0
LAT0, LAT1 = -28.0, 57.0
WIDTH = 1000.0

def merc(lat):
    lat = max(-85.0, min(85.0, lat))
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))

MY0, MY1 = merc(LAT0), merc(LAT1)
HEIGHT = WIDTH * (MY1 - MY0) / (LON1 - LON0)

def xy(lat, lon):
    x = (lon - LON0) / (LON1 - LON0) * WIDTH
    y = (MY1 - merc(lat)) / (MY1 - MY0) * HEIGHT
    return x, y

def pct(lat, lon):
    x, y = xy(lat, lon)
    return 100.0 * x / WIDTH, 100.0 * y / HEIGHT

# --- land paths -------------------------------------------------------------
PAD = 12.0
def rings(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"][0]]
    if geom["type"] == "MultiPolygon":
        return [p[0] for p in geom["coordinates"]]
    return []

paths = []
for feat in json.load(open(CACHE))["features"]:
    for ring in rings(feat["geometry"]):
        pts = [xy(la, lo) for lo, la in ring]
        if not pts:
            continue
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        if max(xs) < -PAD or min(xs) > WIDTH + PAD: continue
        if max(ys) < -PAD or min(ys) > HEIGHT + PAD: continue
        if (max(xs) - min(xs)) < 1.2 and (max(ys) - min(ys)) < 1.2: continue
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
        paths.append(d)

with open(OUT, "w") as fh:
    fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH:.0f} '
             f'{HEIGHT:.0f}" width="{WIDTH:.0f}" height="{HEIGHT:.0f}">\n')
    fh.write('  <g fill="#E3DAD1" stroke="none" fill-rule="evenodd">\n')
    for d in paths:
        fh.write(f'    <path d="{d}" />\n')
    fh.write('  </g>\n</svg>\n')
print(f"{OUT.split('/')[-1]}  {WIDTH:.0f}x{HEIGHT:.0f}  {len(paths)} filled rings")

# --- markers ----------------------------------------------------------------
MARKETS = [("Lisbon (the property)", 38.7629,  -9.0958),
           ("London",                51.5074,  -0.1278),
           ("Paris",                 48.8566,   2.3522),
           ("Zurich",                47.3769,   8.5417),
           ("New York",              40.7128, -74.0060),
           ("Toronto",               43.6532, -79.3832),
           ("Sao Paulo",            -23.5505, -46.6333)]
pts = []
for n, la, lo in MARKETS:
    l, t = pct(la, lo)
    flag = "  *** OUTSIDE FRAME" if not (0 <= l <= 100 and 0 <= t <= 100) else ""
    print(f"{n:<24} left:{l:6.2f}%  top:{t:6.2f}%{flag}")
    pts.append((l, t))

# True on-page separation. The percentages are of DIFFERENT axes, so they must be
# converted to pixels before they can be compared - mixing them understates how
# close two dots really are.
PRINT_W = 6.8 * 96                      # content width in CSS px
PRINT_H = PRINT_W * HEIGHT / WIDTH
pair, closest = None, 1e9
for (na, a), (nb, b) in itertools.combinations(zip([m[0] for m in MARKETS], pts), 2):
    d = (((a[0]-b[0])/100*PRINT_W)**2 + ((a[1]-b[1])/100*PRINT_H)**2) ** 0.5
    if d < closest:
        closest, pair = d, (na, nb)
print(f"map on page: {PRINT_W:.0f} x {PRINT_H:.0f} px")
print(f"closest pair: {pair[0]} / {pair[1]} at {closest:.1f}px "
      f"-> {'dots only, keyed to the table' if closest < 60 else 'far enough to label'}")
print("".join(
    f'<div style="position:absolute;left:{l:.2f}%;top:{t:.2f}%">'
    f'<div style="position:absolute;left:-2.5px;top:-2.5px;width:5px;height:5px;'
    f'border-radius:50%;background:#6E8FA8"></div></div>' for l, t in pts))
