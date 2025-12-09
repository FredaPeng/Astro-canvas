#!/usr/bin/env python3
"""Simplify constellation stroke data in assets/data/constellations_88.json

This script:
- backs up the original JSON (if backup not present)
- flattens strokes (or uses legacy points)
- downsamples to a fixed number of points (default 20)
- rounds coordinates to 3 decimal places
- writes the simplified strokes back as a single-stroke array per entry
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'assets' / 'data' / 'constellations_88.json'
BACKUP = ROOT / 'assets' / 'data' / 'constellations_88.json.bak2'

if not DATA.exists():
    print('Data file not found:', DATA)
    raise SystemExit(1)

if not BACKUP.exists():
    BACKUP.write_text(DATA.read_text())
    print('Backup written to', BACKUP)

with open(DATA, 'r', encoding='utf-8') as f:
    data = json.load(f)

def flatten_entry(e):
    # Prefer modern strokes field
    if isinstance(e.get('strokes'), list) and e.get('strokes'):
        s = e['strokes']
        # strokes may be [[ [x,y], ... ], ...] or [[x,y], ...]
        if s and isinstance(s[0], list) and s[0] and isinstance(s[0][0], list):
            pts = [tuple(pt) for stroke in s for pt in stroke]
        else:
            pts = [tuple(pt) for pt in s]
        return pts
    # legacy field
    if isinstance(e.get('points'), list) and e.get('points'):
        return [tuple(pt) for pt in e['points']]
    return []

def downsample(pts, n=20):
    if not pts:
        return []
    L = len(pts)
    if L <= n:
        return list(pts)
    # pick evenly spaced indices
    idxs = [int(round(i*(L-1)/(n-1))) for i in range(n)]
    out = [pts[i] for i in idxs]
    return out

processed = 0
for entry in data:
    pts = flatten_entry(entry)
    if not pts:
        entry['strokes'] = []
        continue
    small = downsample(pts, n=20)
    # round coordinates to 3 decimals
    small = [[round(float(x), 3), round(float(y), 3)] for x, y in small]
    entry['strokes'] = [small]
    processed += 1

with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f'Simplified strokes for {processed} entries in {DATA}')
