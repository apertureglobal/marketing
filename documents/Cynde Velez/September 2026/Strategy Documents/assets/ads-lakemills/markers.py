#!/usr/bin/env python3
"""Marker percentages for the North America frame used by these documents.
The frame's projection is recovered from six known placements in the shared
North America map asset, then checked back against them (max error below 0.1% of
the frame, i.e. under half a pixel at page width). Land is filled in the SVG,
never stroked. Warns if a marker leaves the frame."""
LEFT0, LON0, LON_K = 70.51, -81.4409, 1.5199
TOP0,  LAT0, LAT_K = 87.48,  27.4956, -3.5689

def project(lat, lon):
    return LEFT0 + (lon - LON0) * LON_K, TOP0 + (lat - LAT0) * LAT_K

CHECK = [("ref A", 27.4956, -81.4409, 70.51, 87.48),
         ("New York", 40.7128, -74.0060, 81.81, 40.31),
         ("Boston", 42.3601, -71.0589, 86.27, 34.43),
         ("Chicago", 41.8781, -87.6298, 61.17, 36.15),
         ("Atlanta", 33.7490, -84.3880, 66.08, 65.18),
         ("Toronto", 43.6532, -79.3832, 73.66, 29.81)]
worst = 0.0
for n, la, lo, el, et in CHECK:
    l, t = project(la, lo)
    worst = max(worst, abs(l - el), abs(t - et))
print(f"projection check: worst error {worst:.3f}% of frame")

MARKETS = [("Oviedo (the property)", 28.628129, -81.114332),
           ("New York",              40.7128,  -74.0060),
           ("Washington",            38.9072,  -77.0369),
           ("Chicago",               41.8781,  -87.6298),
           ("Boston",                42.3601,  -71.0589),
           ("Toronto",               43.6532,  -79.3832)]
for n, la, lo in MARKETS:
    l, t = project(la, lo)
    flag = "  *** OUTSIDE FRAME" if not (0 <= l <= 100 and 0 <= t <= 100) else ""
    print(f"{n:<22} left:{l:6.2f}%  top:{t:6.2f}%{flag}")
