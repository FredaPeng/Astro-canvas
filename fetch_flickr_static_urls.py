"""
Fetch direct/static image URLs from Flickr photo page URLs.

Usage:
  python3 tools/fetch_flickr_static_urls.py flickr_pages.txt urls.txt

Input (flickr_pages.txt): one Flickr photo page URL per line. Optionally add a tab and a name.
Output (urls.txt): one direct image URL per line, optionally tab + name, suitable for `generate_spectrum_manifest.py`.

This script parses the Flickr page and looks for OpenGraph `og:image` meta tag which usually contains a direct image URL.

Requires: requests, beautifulsoup4
  pip install requests beautifulsoup4

Run locally in your environment (this script does network calls from your machine).
"""

import sys
import requests
from bs4 import BeautifulSoup


def extract_image_url(page_url):
    try:
        r = requests.get(page_url, timeout=20, headers={"User-Agent":"Mozilla/5.0"})
        r.raise_for_status()
    except Exception as e:
        print('ERROR fetching', page_url, e)
        return None
    soup = BeautifulSoup(r.text, 'html.parser')
    # Try og:image first
    og = soup.find('meta', property='og:image')
    if og and og.get('content'):
        return og.get('content')
    # Try twitter:image
    tw = soup.find('meta', attrs={'name':'twitter:image'})
    if tw and tw.get('content'):
        return tw.get('content')
    # Fallback: look for <img class="main-photo"> or similar
    img = soup.find('img')
    if img and img.get('src'):
        return img.get('src')
    return None


def main(input_file, output_file):
    with open(input_file, 'r') as inf:
        lines = [l.strip() for l in inf if l.strip()]
    out_lines = []
    for line in lines:
        parts = line.split('\t')
        page = parts[0].strip()
        name = parts[1].strip() if len(parts) > 1 else ''
        print('Processing', page)
        img_url = extract_image_url(page)
        if not img_url:
            print('  FAILED to extract image URL for', page)
            continue
        if name:
            out_lines.append(f"{img_url}\t{name}")
        else:
            out_lines.append(img_url)
        print('  ->', img_url)
    with open(output_file, 'w') as outf:
        outf.write('\n'.join(out_lines))
    print('Wrote', output_file)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python3 tools/fetch_flickr_static_urls.py flickr_pages.txt urls.txt')
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
