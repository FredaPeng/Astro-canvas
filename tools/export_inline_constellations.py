#!/usr/bin/env python3
"""Export selected constellations from the data JSON as a JS literal suitable
for inserting into `index.html`'s INLINE_CONSTELLATIONS.

Usage:
  python3 tools/export_inline_constellations.py centaurus orion "ursa-major" ...

If no slugs are provided, the script will export a small default set.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / 'assets' / 'data' / 'constellations_88.json'

DEFAULT = ['centaurus', 'orion', 'ursa-major', 'scorpius', 'cassiopeia', 'crux']

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_by_slug(data, slug):
    for e in data:
        if e.get('slug') == slug or e.get('id') == slug:
            return e
    return None

def to_js_literal(obj):
    # produce a compact JS literal for the object, including strokes (if present) or points
    out = {
        'name': obj.get('name'),
        'latin': obj.get('latin') or '',
        'slug': obj.get('slug') or obj.get('id'),
        'color': obj.get('color') or '#ffffff'
    }
    # Prefer strokes if present
    if obj.get('strokes'):
        out['strokes'] = obj['strokes']
    elif obj.get('points'):
        out['points'] = obj['points']
    return out

def main(slugs):
    data = load_data()
    slugs = slugs or DEFAULT
    selected = []
    for s in slugs:
        e = find_by_slug(data, s)
        if not e:
            print(f'# WARNING: slug not found: {s}', file=sys.stderr)
            continue
        selected.append(to_js_literal(e))

    # Print a JS array literal
    print(json.dumps(selected, indent=2))

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
