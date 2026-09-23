#!/usr/bin/env python3
"""Marker percentages for the shared North America frame. Projection recovered
from known placements in the map asset and checked back against them. Land is
filled in the SVG, never stroked. Warns if a marker leaves the frame."""
import itertools
LEFT0, LON0, LON_K = 70.51, -81.4409, 1.5199
TOP0,  LAT0, LAT_K = 87.48,  27.4956, -3.5689

def project(lat, lon):
    return LEFT0 + (lon - LON0) * LON_K, TOP0 + (lat - LAT0) * LAT_K

CHECK = [("New York", 40.7128, -74.0060, 81.81, 40.31),
         ("Chicago", 41.8781, -87.6298, 61.17, 36.15),
         ("Atlanta", 33.7490, -84.3880, 66.08, 65.18)]
print("projection check: worst error %.3f%% of frame" % max(
    max(abs(project(la, lo)[0] - el), abs(project(la, lo)[1] - et))
    for _, la, lo, el, et in CHECK))

MARKETS = [("Nashville metropolitan area", 36.1627, -86.7816),
           ("Chicago",                     41.8781, -87.6298),
           ("Dallas",                      32.7767, -96.7970),
           ("Atlanta",                     33.7490, -84.3880),
           ("Los Angeles",                 34.0522, -118.2437)]
pts = []
for n, la, lo in MARKETS:
    l, t = project(la, lo)
    flag = "  *** OUTSIDE FRAME" if not (0 <= l <= 100 and 0 <= t <= 100) else ""
    print(f"{n:<30} left:{l:6.2f}%  top:{t:6.2f}%{flag}")
    pts.append((l, t))

d = min(((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5
        for a, b in itertools.combinations(pts, 2))
print(f"closest pair: {d:.2f}% of frame width")
print("".join(
    f'<div style="position:absolute;left:{l:.2f}%;top:{t:.2f}%">'
    f'<div style="position:absolute;left:-2.5px;top:-2.5px;width:5px;height:5px;'
    f'border-radius:50%;background:#6E8FA8"></div></div>' for l, t in pts))
