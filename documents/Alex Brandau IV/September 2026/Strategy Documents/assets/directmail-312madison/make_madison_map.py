#!/usr/bin/env python3
"""
Builds madison-radius.svg -- Davidson County outline, distance rings drawn from
312 Madison St, and the mailing-market markers. Also performs a point-in-polygon
check of the subject coordinates against the real county boundary, and prints the
marker percentages for the HTML overlay.

County polygon: US Census TIGERweb State_County MapServer layer 13, GEOID 47037.
Subject coordinates: US Census geocoder, Public_AR_Current.

    python3 make_madison_map.py            # writes madison-radius.svg next to this file
"""
import json, math, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SUBJ = (36.176061613686, -86.786337584336)      # 312 Madison St -- Census geocoder
COUNTY_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
              "State_County/MapServer/13/query?where=GEOID%3D%2747037%27"
              "&outFields=BASENAME&returnGeometry=true&f=json")

MARKETS = [
    # name,               lat,       lon,      side  ('r'/'l'), nudge ('', 'up', 'dn')
    ("Salemtown",         36.1870, -86.7930, 'l', 'up'),
    ("Downtown Core",     36.1600, -86.7760, 'r', ''),
    ("The Gulch",         36.1520, -86.7880, 'l', ''),
    ("East Nashville",    36.1780, -86.7480, 'r', ''),
    ("Inglewood",         36.2110, -86.7300, 'l', ''),
    ("Wedgewood-Houston", 36.1380, -86.7690, 'r', 'dn'),
    ("12South",           36.1230, -86.7900, 'r', ''),
    ("Belmont-Hillsboro", 36.1310, -86.7990, 'r', 'up'),
    ("Sylvan Park",       36.1490, -86.8390, 'l', 'up'),
    ("Richland-West End", 36.1370, -86.8280, 'l', 'dn'),
    ("Green Hills",       36.1050, -86.8150, 'r', 'dn'),
    ("Belle Meade",       36.0980, -86.8590, 'l', ''),
    ("Forest Hills",      36.0620, -86.8250, 'l', ''),
    ("Oak Hill",          36.0740, -86.7860, 'r', ''),
]
RINGS_MI = [1, 3, 6, 8]
SPAN_MI = 17.0          # width of the rendered frame; the county is clipped to it
CENTRE_OFFSET_MI = 2.6  # shift the frame south so the southern enclaves fit
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


def main():
    with urllib.request.urlopen(COUNTY_URL) as fh:
        geom = json.load(fh)['features'][0]['geometry']['rings']
    rings = [[mercator_to_ll(x, y) for x, y in r] for r in geom]

    hit = any(point_in_ring(SUBJ[0], SUBJ[1], r) for r in rings)
    print(f"point-in-polygon, subject vs TIGER county 47037 boundary: {hit}")

    # local equirectangular projection centred on the subject
    lat0 = math.radians(SUBJ[0])
    mi_per_deg_lon = MI_PER_DEG_LAT * math.cos(lat0)

    def to_mi(lat, lon):
        return ((lon - SUBJ[1]) * mi_per_deg_lon, -(lat - SUBJ[0]) * MI_PER_DEG_LAT)

    span = SPAN_MI
    cx, cy = -1.4, CENTRE_OFFSET_MI
    x0, y0 = cx - span / 2, cy - span / 2
    scale = W / span

    def px(mx, my):
        return ((mx - x0) * scale, (my - y0) * scale)

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
           f'<rect x="0" y="0" width="{W}" height="{H}" fill="#F7F6F3"/>',
           f'<clipPath id="frame"><rect x="0" y="0" width="{W}" height="{H}"/></clipPath>',
           '<g clip-path="url(#frame)">']

    for r in rings:
        d = 'M' + ' L'.join('%.1f %.1f' % px(*to_mi(la, lo)) for la, lo in r) + ' Z'
        out.append(f'<path d="{d}" fill="#EAE5DC" stroke="#B8AEA2" stroke-width="2.2"/>')
    out.append('</g>')

    sx, sy = px(0, 0)
    for mi in RINGS_MI:
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#C9C0B6" '
                   'stroke-width="1" stroke-dasharray="4 5"/>' % (sx, sy, mi * scale))
        # ring labels sit due west of centre, the emptiest line in the frame
        out.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="15" '
                   'fill="#8E8688" letter-spacing="2" text-anchor="middle">%d MI</text>'
                   % (sx - mi * scale, sy + 22, mi))

    overlay = []
    for name, la, lo, side, nudge in MARKETS:
        mx, my = px(*to_mi(la, lo))
        out.append('<circle cx="%.1f" cy="%.1f" r="6" fill="#B2C6D6"/>' % (mx, my))
        overlay.append((name, mx / W * 100, my / H * 100, side, nudge))
    out.append('<circle cx="%.1f" cy="%.1f" r="9" fill="#0E1113"/>' % (sx, sy))
    out.append('</svg>')

    path = os.path.join(HERE, 'madison-radius.svg')
    with open(path, 'w') as fh:
        fh.write('\n'.join(out))
    print('wrote', path)

    print('\n<!-- overlay markers -->')
    print('<div class="mk subj r" style="left:%.2f%%;top:%.2f%%"><b>312 Madison St</b></div>'
          % (sx / W * 100, sy / H * 100))
    for name, lx, ty, side, nudge in overlay:
        cls = ('mk ' + side + (' ' + nudge if nudge else '')).strip()
        print('<div class="%s" style="left:%.2f%%;top:%.2f%%"><b>%s</b></div>' % (cls, lx, ty, name))


if __name__ == '__main__':
    main()
