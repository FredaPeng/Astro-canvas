Spectrum manifest helper

This folder contains a small helper script to build a local `assets/data/spectrum.json` manifest from a list of image URLs (for example from Flickr).

Usage

1. Create a text file `urls.txt` with one image URL per line. Optionally add a tab and a short name after the URL:

   https://live.staticflickr.com/.../image.jpg	Lagoon Nebula

2. Install Python dependencies (recommended into a venv):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pillow requests colorthief
```

3. Run the generator:

```bash
python3 tools/generate_spectrum_manifest.py urls.txt
```

Output

- Downloads images to `assets/images/` (filename hashed + name)
- Writes `assets/data/spectrum.json` with entries containing `file`, `hex`, `hue`, `range`, `source`.

Notes and warnings

- The script uses the `colorthief` package for a quick dominant-color estimate; if unavailable it falls back to average color.
- Respect Flickr usage terms and include proper credits when publishing.
