#!/usr/bin/env python3
"""
Builds willowdale-county.svg -- the Davidson County boundary with the Williamson
County boundary drawn adjacent and hatch-free, distance rings from 806 Willowdale
Ct, and the mailing-market markers.

Also does the work that must not be taken on trust:
  * point-in-polygon of the subject coordinates against the real TIGER county
    boundary for Davidson (47037) AND Williamson (47187),
  * straight-line miles from the subject to every market and to downtown,
  * the marker percentages for the HTML overlay.

County polygons: US Census TIGERweb State_County MapServer layer 13.
Subject coordinates: US Census geocoder, Public_AR_Current ->
    36.057794452804, -86.774765374312

    python3 make_willowdale_map.py     # writes willowdale-county.svg beside this file
"""
import json, math, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SUBJ = (36.057794452804, -86.774765374312)   # 806 Willowdale Ct -- Census geocoder
DOWNTOWN = (36.1627, -86.7816)               # Nashville courthouse / core

CO_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
          "State_County/MapServer/13/query?where=GEOID%%3D%%27%s%%27"
          "&outFields=BASENAME&returnGeometry=true&f=json")

# name, lat, lon, county, side ('r'/'l'), nudge ('', 'up', 'up2', 'dn')
MARKETS = [
    ("Oak Hill",           36.0740, -86.7860, "Davidson",  'l', 'up'),
    ("Crieve Hall",        36.0640, -86.7420, "Davidson",  'r', 'up'),
    ("Forest Hills",       36.0620, -86.8250, "Davidson",  'l', 'dn'),
    ("Green Hills",        36.1050, -86.8150, "Davidson",  'r', 'dn'),
    ("Belle Meade",        36.0980, -86.8590, "Davidson",  'l', 'dn2'),
    ("Hillwood",           36.1140, -86.8730, "Davidson",  'l', 'dn2'),
    ("West Meade",         36.1170, -86.8880, "Davidson",  'l', 'dn'),
    ("Berry Hill",         36.1120, -86.7670, "Davidson",  'r', ''),
    ("12South",            36.1230, -86.7900, "Davidson",  'l', ''),
    ("Belmont-Hillsboro",  36.1310, -86.7990, "Davidson",  'l', 'up'),
    ("Sylvan Park",        36.1490, -86.8390, "Davidson",  'l', 'up'),
    ("East Nashville",     36.1780, -86.7480, "Davidson",  'r', ''),
    ("Downtown Core",      36.1600, -86.7760, "Davidson",  'r', 'up'),
    ("Brentwood",          35.9700, -86.7830, "Williamson",'r', 'dn'),
    ("Franklin",           35.9250, -86.8690, "Williamson",'r', ''),
]

RINGS_MI = [2, 5, 8, 11]
SPAN_MI = 31.0
CENTRE_DX, CENTRE_DY = -1.6, -2.4      # nudge frame so both county outlines fit
W = H = 1000
MI_PER_DEG_LAT = 69.055


def mercator_to_ll(x, y):
    lon = x / 20037508.34 * 180.0
    lat = y / 20037508.34 * 180.0
    lat = 180.0 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2)
    return lat, lon


def fetch_rings(geoid):
    with urllib.request.urlopen(CO_URL % geoid) as fh:
        geom = json.load(fh)['features'][0]['geometry']['rings']
    return [[mercator_to_ll(x, y) for x, y in r] for r in geom]


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
    dav = fetch_rings('47037')
    wil = fetch_rings('47187')

    print("point-in-polygon, subject vs TIGER 47037 Davidson   :",
          any(point_in_ring(*SUBJ, r) for r in dav))
    print("point-in-polygon, subject vs TIGER 47187 Williamson :",
          any(point_in_ring(*SUBJ, r) for r in wil))
    print("straight-line miles, subject -> downtown core       : %.2f"
          % haversine_mi(SUBJ, DOWNTOWN))

    lat0 = math.radians(SUBJ[0])
    mi_per_deg_lon = MI_PER_DEG_LAT * math.cos(lat0)

    def to_mi(lat, lon):
        return ((lon - SUBJ[1]) * mi_per_deg_lon, -(lat - SUBJ[0]) * MI_PER_DEG_LAT)

    x0 = CENTRE_DX - SPAN_MI / 2
    y0 = CENTRE_DY - SPAN_MI / 2
    scale = W / SPAN_MI

    def px(mx, my):
        return ((mx - x0) * scale, (my - y0) * scale)

    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
           % (W, H, W, H),
           '<rect x="0" y="0" width="%d" height="%d" fill="#F7F6F3"/>' % (W, H),
           '<clipPath id="frame"><rect x="0" y="0" width="%d" height="%d"/></clipPath>' % (W, H),
           '<g clip-path="url(#frame)">']

    # Williamson first, drawn plain -- it is shown to be excluded, not to be mailed
    for r in wil:
        d = 'M' + ' L'.join('%.1f %.1f' % px(*to_mi(la, lo)) for la, lo in r) + ' Z'
        out.append('<path d="%s" fill="#F1EEE8" stroke="#CFC7BC" stroke-width="1.6" '
                   'stroke-dasharray="7 6"/>' % d)
    for r in dav:
        d = 'M' + ' L'.join('%.1f %.1f' % px(*to_mi(la, lo)) for la, lo in r) + ' Z'
        out.append('<path d="%s" fill="#EAE5DC" stroke="#B8AEA2" stroke-width="2.4"/>' % d)
    out.append('</g>')

    sx, sy = px(0, 0)
    for mi in RINGS_MI:
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#C9C0B6" '
                   'stroke-width="1" stroke-dasharray="4 5"/>' % (sx, sy, mi * scale))
        # ring labels ride the down-right diagonal -- no market sits in that sector,
        # so they cannot collide with a neighbourhood name
        k = mi * scale * 0.7071
        out.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="15" '
                   'fill="#8E8688" letter-spacing="2" text-anchor="middle">%d MI</text>'
                   % (sx + k, sy + k + 5, mi))

    overlay = []
    print('\n%-20s %8s  %s' % ('market', 'miles', 'county'))
    for name, la, lo, county, side, nudge in MARKETS:
        mx, my = px(*to_mi(la, lo))
        fill = "#B2C6D6" if county == "Davidson" else "#FFFFFF"
        stroke = '' if county == "Davidson" else ' stroke="#A9A19A" stroke-width="1.8"'
        out.append('<circle cx="%.1f" cy="%.1f" r="6" fill="%s"%s/>' % (mx, my, fill, stroke))
        print('%-20s %8.2f  %s' % (name, haversine_mi(SUBJ, (la, lo)), county))
        overlay.append((name, mx / W * 100, my / H * 100, side, nudge))

    out.append('<circle cx="%.1f" cy="%.1f" r="9.5" fill="#0E1113"/>' % (sx, sy))
    out.append('</svg>')

    path = os.path.join(HERE, 'willowdale-county.svg')
    with open(path, 'w') as fh:
        fh.write('\n'.join(out))
    print('\nwrote', path)

    print('\n<!-- overlay markers -->')
    print('<div class="mk subj r" style="left:%.2f%%;top:%.2f%%"><b>806 Willowdale Ct</b></div>'
          % (sx / W * 100, sy / H * 100))
    for name, lx, ty, side, nudge in overlay:
        cls = ('mk ' + side + (' ' + nudge if nudge else '')).strip()
        print('<div class="%s" style="left:%.2f%%;top:%.2f%%"><b>%s</b></div>' % (cls, lx, ty, name))


if __name__ == '__main__':
    main()
