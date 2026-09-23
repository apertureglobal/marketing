#!/usr/bin/env python3
"""
Builds cammack-radius.svg -- the Davidson County outline, distance rings drawn
from 805 Cammack Ct, and the west-side mailing-market markers.

It also (a) re-verifies the county by point-in-polygon against the real federal
county boundary, and (b) prints straight-line miles to every market plus the
marker percentages for the HTML overlay. Nothing in the document is eyeballed
off the map; the table on page 02 is this script's output.

County polygon: US Census TIGERweb State_County MapServer layer 13, GEOID 47037.
Subject coordinates: US Census geocoder, Public_AR_Current benchmark.

    python3 make_cammack_map.py        # writes cammack-radius.svg beside this file
"""
import json, math, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SUBJ = (36.1099019003, -86.909699363467)        # 805 Cammack Ct -- Census geocoder
COUNTY_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
              "State_County/MapServer/13/query?where=GEOID%3D%2747037%27"
              "&outFields=BASENAME&returnGeometry=true&f=json")

# name, lat, lon, label side ('r'/'l'), vertical nudge ('', 'up', 'up2', 'dn')
MARKETS = [
    ("Hillwood",           36.1200, -86.8830, 'r', 'up'),
    ("Charlotte Park",     36.1480, -86.8760, 'l', ''),
    ("The Nations",        36.1620, -86.8520, 'r', 'up'),
    ("Sylvan Park",        36.1490, -86.8390, 'r', 'dn'),
    ("Richland-West End",  36.1370, -86.8280, 'r', ''),
    ("Belle Meade",        36.0980, -86.8590, 'l', 'up'),
    ("Green Hills",        36.1050, -86.8150, 'r', 'dn'),
    ("Forest Hills",       36.0620, -86.8250, 'l', ''),
    ("Oak Hill",           36.0740, -86.7860, 'r', ''),
    ("Bellevue",           36.0700, -86.9500, 'l', ''),
    ("Downtown Core",      36.1600, -86.7760, 'l', 'up'),
]
# markets named in the document but deliberately NOT mailed -- distance only
EXCLUDED = [
    ("Brentwood",          36.0331, -86.7828),
    ("Franklin",           35.9251, -86.8689),
]
RINGS_MI = [1, 3, 5, 8]
SPAN_MI = 19.0
EAST_OFFSET_MI = 2.2     # shift the frame east so downtown fits without clipping Bellevue
SOUTH_OFFSET_MI = 1.6
W, H = 1000, 1000
MI_PER_DEG_LAT = 69.055


def mercator_to_ll(x, y):
    lon = x / 20037508.34 * 180.0
    lat = y / 20037508.34 * 180.0
    lat = 180.0 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2)
    return lat, lon


def point_in_ring(lat, lon, ring):
    inside = False
    n = len(ring)
    for i in range(n):
        y1, x1 = ring[i]
        y2, x2 = ring[(i + 1) % n]
        if (x1 > lon) != (x2 > lon):
            yint = y1 + (lon - x1) * (y2 - y1) / (x2 - x1)
            if lat < yint:
                inside = not inside
    return inside


def haversine_mi(a, b):
    R = 3958.7613
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = p2 - p1
    dl = math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def main():
    with urllib.request.urlopen(COUNTY_URL) as fh:
        geom = json.load(fh)['features'][0]['geometry']['rings']
    rings = [[mercator_to_ll(x, y) for x, y in r] for r in geom]
    hit = any(point_in_ring(SUBJ[0], SUBJ[1], r) for r in rings)
    print("point-in-polygon, subject vs TIGER county 47037 (Davidson) boundary:", hit)

    lat0 = math.radians(SUBJ[0])
    mi_per_deg_lon = MI_PER_DEG_LAT * math.cos(lat0)

    def to_mi(lat, lon):
        return ((lon - SUBJ[1]) * mi_per_deg_lon, -(lat - SUBJ[0]) * MI_PER_DEG_LAT)

    span = SPAN_MI
    cx, cy = EAST_OFFSET_MI, SOUTH_OFFSET_MI
    x0, y0 = cx - span / 2, cy - span / 2
    scale = W / span

    def px(mx, my):
        return ((mx - x0) * scale, (my - y0) * scale)

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
           f'<rect x="0" y="0" width="{W}" height="{H}" fill="#F7F6F3"/>',
           '<clipPath id="frame"><rect x="0" y="0" width="%d" height="%d"/></clipPath>' % (W, H),
           '<g clip-path="url(#frame)">']
    for r in rings:
        d = 'M' + ' L'.join('%.1f %.1f' % px(*to_mi(la, lo)) for la, lo in r) + ' Z'
        out.append(f'<path d="{d}" fill="#EAE5DC" stroke="#B8AEA2" stroke-width="2.2"/>')
    out.append('</g>')

    sx, sy = px(0, 0)
    for mi in RINGS_MI:
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#C9C0B6" '
                   'stroke-width="1" stroke-dasharray="4 5"/>' % (sx, sy, mi * scale))
        out.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="15" '
                   'fill="#8E8688" letter-spacing="2" text-anchor="middle">%d MI</text>'
                   % (sx, sy + mi * scale + 20, mi))

    overlay = []
    for name, la, lo, side, nudge in MARKETS:
        mx, my = px(*to_mi(la, lo))
        out.append('<circle cx="%.1f" cy="%.1f" r="6" fill="#B2C6D6"/>' % (mx, my))
        overlay.append((name, mx / W * 100, my / H * 100, side, nudge, haversine_mi(SUBJ, (la, lo))))
    out.append('<circle cx="%.1f" cy="%.1f" r="9" fill="#0E1113"/>' % (sx, sy))
    out.append('</svg>')

    path = os.path.join(HERE, 'cammack-radius.svg')
    with open(path, 'w') as fh:
        fh.write('\n'.join(out))
    print('wrote', path)

    print('\n<!-- overlay markers -->')
    print('<div class="mk subj l" style="left:%.2f%%;top:%.2f%%"><b>805 Cammack Ct</b></div>'
          % (sx / W * 100, sy / H * 100))
    for name, lx, ty, side, nudge, mi in overlay:
        cls = ('mk ' + side + (' ' + nudge if nudge else '')).strip()
        print('<div class="%s" style="left:%.2f%%;top:%.2f%%"><b>%s</b></div>' % (cls, lx, ty, name))

    print('\nstraight-line miles from the subject')
    for name, lx, ty, side, nudge, mi in sorted(overlay, key=lambda r: r[5]):
        print('  %-20s %5.1f' % (name, mi))
    for name, la, lo in EXCLUDED:
        print('  %-20s %5.1f   (Williamson County -- excluded)' % (name, haversine_mi(SUBJ, (la, lo))))


if __name__ == '__main__':
    main()
