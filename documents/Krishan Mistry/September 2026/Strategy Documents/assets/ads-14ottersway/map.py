#!/usr/bin/env python3
"""
Generates southern-england.svg for the 14 Otters Way strategy document, and
prints each chosen market as a percentage of the SVG frame for the absolutely
positioned dot overlay in the HTML.

Land is FILLED, never stroked -- outlines are illegible at page width.

Equirectangular projection with a cosine correction at the frame's mid
latitude, so the country reads at roughly its true proportions. Frame is
England and Wales with sea margin. Every chosen market lies on the London to
Peterborough axis, so the frame is portrait and sits in a column beside the
market table -- a landscape frame would waste two thirds of its width and
squeeze the markets into an unreadable knot.

Source outline: Natural Earth 1:50m admin 0 countries (public domain), via the
nvkelso/natural-earth-vector mirror. Cached beside this script as
ne_50m_countries.json; delete it to re-fetch.
"""
import itertools, json, math, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "ne_50m_countries.json")
SRC = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/"
       "geojson/ne_50m_admin_0_countries.geojson")

# Frame: lon west/east, lat south/north.
LON_W, LON_E = -6.2, 2.6
LAT_S, LAT_N = 49.9, 55.6
KX = math.cos(math.radians((LAT_S + LAT_N) / 2))

VB_H = 240.0
VB_W = VB_H * ((LON_E - LON_W) * KX) / (LAT_N - LAT_S)

def project(lat, lon):
    """lat/lon -> viewBox x,y"""
    x = (lon - LON_W) * KX / ((LON_E - LON_W) * KX) * VB_W
    y = (LAT_N - lat) / (LAT_N - LAT_S) * VB_H
    return x, y

def pct(lat, lon):
    x, y = project(lat, lon)
    return x / VB_W * 100.0, y / VB_H * 100.0

if not os.path.exists(CACHE):
    print("fetching Natural Earth 1:50m countries ...")
    urllib.request.urlretrieve(SRC, CACHE)
with open(CACHE) as fh:
    gj = json.load(fh)

# Britain and Ireland only; everything else is off-frame or a distraction.
KEEP = {"United Kingdom", "Ireland", "Isle of Man"}
rings = []
for feat in gj["features"]:
    p = feat["properties"]
    name = p.get("ADMIN") or p.get("NAME") or ""
    if name not in KEEP:
        continue
    geom = feat["geometry"]
    polys = (geom["coordinates"] if geom["type"] == "MultiPolygon"
             else [geom["coordinates"]])
    for poly in polys:
        for ring in poly:
            # Clip generously to the frame, then drop rings entirely outside.
            if not any(LON_W - 2 < lo < LON_E + 2 and LAT_S - 2 < la < LAT_N + 2
                       for lo, la in ring):
                continue
            pts = [project(la, lo) for lo, la in ring]
            if len(pts) < 4:
                continue
            rings.append(pts)

def path(pts):
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"
    return f'    <path d="{d}" />'

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W:.0f} {VB_H:.0f}"'
       f' width="{VB_W:.0f}" height="{VB_H:.0f}">',
       '  <g fill="#E3DAD1" stroke="none" fill-rule="evenodd">']
svg += [path(p) for p in rings]
svg += ['  </g>', '</svg>', '']
out = os.path.join(HERE, "southern-england.svg")
with open(out, "w") as fh:
    fh.write("\n".join(svg))
print(f"southern-england.svg  viewBox 0 0 {VB_W:.0f} {VB_H:.0f}  "
      f"{len(rings)} filled rings  {os.path.getsize(out)/1024:.0f} KB")

# (name, lat, lon)
MARKETS = [("Peterborough and its villages",         52.5695, -0.2405),
           ("Huntingdon and St Neots",                52.3300, -0.1900),
           ("Cambridge and South Cambridgeshire",     52.2053,  0.1218),
           ("The main line commuter towns",           51.9020, -0.2020),
           ("London",                                 51.5074, -0.1278)]

pts = []
for n, la, lo in MARKETS:
    l, t = pct(la, lo)
    flag = "  *** OUTSIDE FRAME" if not (0 <= l <= 100 and 0 <= t <= 100) else ""
    print(f"{n:<42} left:{l:6.2f}%  top:{t:6.2f}%{flag}")
    pts.append((l, t))

d = min(((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5
        for a, b in itertools.combinations(pts, 2))
print(f"closest pair: {d:.2f}% of frame width  "
      f"(~{d/100*2.75*96:.0f} px at 2.75in column width -- plain dots, keyed to the table)")
print("".join(
    f'<div style="position:absolute;left:{l:.2f}%;top:{t:.2f}%">'
    f'<div style="position:absolute;left:-2.5px;top:-2.5px;width:5px;height:5px;'
    f'border-radius:50%;background:#6E8FA8"></div></div>' for l, t in pts))
