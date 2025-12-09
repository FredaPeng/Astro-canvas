#!/usr/bin/env python3
"""Generate simple stroke polylines for constellation images.

Algorithm (simple, dependency-light):
- Open each PNG in `assets/images/Constellation Flash Cards/`.
- Convert to grayscale and threshold to find bright pixels (the constellation drawing).
- Extract coordinates of bright pixels, normalize to [0..1] by width/height.
- Build a single greedy nearest-neighbor path (approximate stroke) from the set of points.
- Downsample the path to a maximum number of points (default 200) and write it as a single stroke.

Outputs:
- Updates `assets/data/constellations_88.json` by filling the `strokes` field for entries whose slug matches an image filename.
"""
import json
import os
import random
from math import hypot
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except Exception as exc:  # pragma: no cover - handled by installer step
    raise RuntimeError("Missing dependencies: please install pillow and numpy") from exc


ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = ROOT / "assets" / "images" / "Constellation Flash Cards"
DATA_FILE = ROOT / "assets" / "data" / "constellations_88.json"
BACKUP_FILE = ROOT / "assets" / "data" / "constellations_88.json.bak"


def slugify_filename(name: str) -> str:
    # derive slug from filename like "Canes Venatici.png" -> "canes-venatici"
    base = os.path.splitext(name)[0]
    s = base.lower().replace(" ", "-")
    s = s.replace("_", "-")
    return s


def threshold_image(img: Image.Image, thresh=200):
    gray = img.convert("L")
    arr = np.array(gray)
    mask = arr >= thresh
    return mask


def points_from_mask(mask: np.ndarray, limit=2000):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return []
    pts = list(zip(xs.tolist(), ys.tolist()))
    # If too many points, sample a subset to keep runtime reasonable
    if len(pts) > limit:
        pts = random.sample(pts, limit)
    return pts


def greedy_path(points):
    # simple O(n^2) nearest neighbor path building
    if not points:
        return []
    pts = points[:]
    # start from centroid
    sx = sum(p[0] for p in pts) / len(pts)
    sy = sum(p[1] for p in pts) / len(pts)
    cur = min(pts, key=lambda p: (p[0]-sx)**2 + (p[1]-sy)**2)
    path = [cur]
    pts.remove(cur)
    while pts:
        nxt = min(pts, key=lambda p: (p[0]-cur[0])**2 + (p[1]-cur[1])**2)
        path.append(nxt)
        pts.remove(nxt)
        cur = nxt
    return path


def normalize_path(path, width, height):
    return [[x / width, y / height] for x, y in path]


def downsample(path, max_points=200):
    n = len(path)
    if n <= max_points:
        return path
    # pick evenly spaced indices
    idxs = [int(i * n / max_points) for i in range(max_points)]
    # ensure unique and within bounds
    seen = set()
    out = []
    for i in idxs:
        if i >= n:
            i = n - 1
        if i in seen:
            continue
        seen.add(i)
        out.append(path[i])
    return out


def process_image(path: Path, max_points=200):
    try:
        img = Image.open(path)
    except Exception as e:
        print(f"Failed to open {path}: {e}")
        return []
    w, h = img.size
    mask = threshold_image(img)
    pts = points_from_mask(mask, limit=2500)
    if not pts:
        return []
    path_pts = greedy_path(pts)
    norm = normalize_path(path_pts, w, h)
    small = downsample(norm, max_points=max_points)
    return small


def main():
    if not DATA_FILE.exists():
        print("Data file not found:", DATA_FILE)
        return 1
    # backup
    if not BACKUP_FILE.exists():
        BACKUP_FILE.write_text(DATA_FILE.read_text())
        print("Backup written to", BACKUP_FILE)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # map available images by slug
    images = {slugify_filename(fn): (IMAGES_DIR / fn) for fn in os.listdir(IMAGES_DIR) if fn.lower().endswith(".png")}

    updated = 0
    for entry in data:
        sid = entry.get("slug") or entry.get("id")
        if not sid:
            continue
        img_path = images.get(sid)
        if img_path and img_path.exists():
            strokes = process_image(img_path, max_points=200)
            if strokes:
                # store as single stroke (list of points) inside strokes array
                entry["strokes"] = [strokes]
                updated += 1
            else:
                entry.setdefault("strokes", [])
        else:
            entry.setdefault("strokes", [])

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Updated strokes for {updated} entries in {DATA_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
