#!/usr/bin/env python3
"""Parse saved glcom_kanga.html into structured JSON.

Output: scraper/glcom_kanga.json which will contain list of objects with fields:
- quote: Kanga writing (Swahili)
- literal_translation: literal translation column
- common_meaning: the 'Most Common Meaning' column
- source: 'glcom'
"""
from bs4 import BeautifulSoup
from pathlib import Path
import json

IN = Path(__file__).parent / 'glcom_kanga.html'
OUT = Path(__file__).parent / 'glcom_kanga.json'

if not IN.exists():
    print('Input file not found:', IN)
    raise SystemExit(1)

html = IN.read_text(encoding='utf-8')
soup = BeautifulSoup(html, 'html.parser')

# find the main table with headers 'Kanga Writing (Swahili)' or similar
table = None
for t in soup.find_all('table'):
    ths = t.find_all('th')
    headers = [th.get_text(strip=True).lower() for th in ths]
    if any('kanga' in h or 'writing' in h for h in headers):
        table = t
        break

if table is None:
    # fallback: pick the first table
    table = soup.find('table')

rows = []
for tr in table.find_all('tr'):
    tds = tr.find_all(['td','th'])
    # skip header row
    if tds and any('kanga' in td.get_text(strip=True).lower() for td in tds[:3]):
        continue
    if len(tds) < 3:
        continue
    # typical structure: No., Kanga Writing, Literal Translation, Most Common Meaning
    # some tables include the No. as first td.
    # We'll try to map by position: last two tds are translation and meaning
    # and one before is the kanga phrase.
    try:
        quote = tds[1].get_text(' ', strip=True)
        literal = tds[2].get_text(' ', strip=True) if len(tds) > 2 else ''
        meaning = tds[3].get_text(' ', strip=True) if len(tds) > 3 else ''
    except Exception:
        continue
    rows.append({
        'quote': quote,
        'literal_translation': literal,
        'common_meaning': meaning,
        'source': 'glcom'
    })

OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Wrote {len(rows)} items to {OUT}')
