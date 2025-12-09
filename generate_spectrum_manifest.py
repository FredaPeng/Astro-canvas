"""
Download images listed in a text file and compute a representative color (dominant color) for each.
Generates `assets/data/spectrum.json` entries with: name, file, hex, hue, range, source

Usage:
    python3 tools/generate_spectrum_manifest.py urls.txt

Where urls.txt contains one image URL per line (optionally followed by a tab and a short name).

Notes:
- Requires: Pillow, requests, colorthief
    pip install pillow requests colorthief
- This script is a convenience tool to build a local spectrum manifest from Flickr images.
- It does not bypass Flickr terms; ensure you have right to download and publish images and credit the source.
"""

import sys
import os
import hashlib
import json
import requests
from io import BytesIO
from PIL import Image
from colorthief import ColorThief

OUT_DIR = 'assets/images'
OUT_MANIFEST = 'assets/data/spectrum.json'

os.makedirs(OUT_DIR, exist_ok=True)


def sanitize_name(s):
    return ''.join(c if c.isalnum() or c in (' ', '-') else '_' for c in s).strip().replace(' ', '-')[:60]


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def rgb_to_hue(r,g,b):
    # convert to hsl and return hue in degrees
    r /= 255.0; g /= 255.0; b /= 255.0
    mx = max(r,g,b); mn = min(r,g,b)
    d = mx - mn
    if d == 0:
        return 0
    if mx == r:
        h = (g - b) / d % 6
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    h = h * 60
    if h < 0: h += 360
    return round(h)


def main(urls_file):
    entries = []
    with open(urls_file, 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    for i, line in enumerate(lines, start=1):
        parts = line.split('\t')
        url = parts[0].strip()
        name = parts[1].strip() if len(parts) > 1 else f'image-{i}'
        print('Fetching', url)
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
        except Exception as e:
            print('  ERROR', e)
            continue
        try:
            img = Image.open(BytesIO(r.content)).convert('RGB')
        except Exception as e:
            print('  ERROR decoding image', e)
            continue

        # derive filename by hashing url
        h = hashlib.sha1(url.encode('utf-8')).hexdigest()[:12]
        ext = '.jpg'
        fname = f'{sanitize_name(name)}-{h}{ext}'
        fpath = os.path.join(OUT_DIR, fname)
        with open(fpath, 'wb') as out_f:
            out_f.write(r.content)

        # dominant color
        try:
            ct = ColorThief(fpath)
            dominant = ct.get_color(quality=1)
        except Exception:
            # fallback average
            px = list(img.getdata())
            avg = tuple(sum(c[i] for c in px)//len(px) for i in range(3))
            dominant = avg

        hexcol = rgb_to_hex(dominant)
        hue = rgb_to_hue(*dominant)

        entry = {
            'name': name,
            'file': fname,
            'hex': hexcol,
            'hue': hue,
            'range': 25,
            'source': url
        }
        entries.append(entry)
        print('  ->', fname, hexcol, hue)

    # write manifest
    os.makedirs(os.path.dirname(OUT_MANIFEST), exist_ok=True)
    with open(OUT_MANIFEST, 'w') as mf:
        json.dump(entries, mf, indent=2)
    print('Wrote', OUT_MANIFEST)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 tools/generate_spectrum_manifest.py urls.txt')
        sys.exit(1)
    main(sys.argv[1])
