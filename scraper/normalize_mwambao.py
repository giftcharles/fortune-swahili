#!/usr/bin/env python3
"""Normalize mwambao scrape and merge into data/quotes.json

Usage: python3 normalize_mwambao.py

This script parses `scraper/mwambao_methali.txt`, normalizes entries,
detects duplicates (exact and near-duplicates using difflib), and merges
them into `data/quotes.json`. Existing entries will gain a `count` field
if missing. New entries are appended with metadata: translation, source,
and count=1.
"""
import json
import re
import difflib
import unicodedata
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "quotes.json"
MWAMBA_FILE = Path(__file__).resolve().parents[0] / "mwambao_methali.txt"


def normalize_text(s: str) -> str:
    s = s or ""
    s = s.strip()
    # Unicode normalize and collapse whitespace
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s)
    s = s.lower()
    # remove punctuation for matching
    s = re.sub(r'[\[\]"\'`(),.\-:;!?—–]+', "", s)
    s = s.strip()
    return s


def split_line(line: str):
    # Heuristic split: prefer a comma followed by space, else first period+space,
    # else try ' - ' or ' — '. If nothing, return line as quote and empty translation.
    line = line.strip()
    if not line:
        return None, None
    # try comma
    m = re.split(r",\s+", line, maxsplit=1)
    if len(m) == 2:
        left, right = m
        return left.strip().rstrip('.'), right.strip()
    # try period
    m = re.split(r"\.\s+", line, maxsplit=1)
    if len(m) == 2:
        left, right = m
        return left.strip().rstrip('.'), right.strip()
    # try dash
    m = re.split(r"\s[\-—–]\s", line, maxsplit=1)
    if len(m) == 2:
        left, right = m
        return left.strip().rstrip('.'), right.strip()
    # fallback: no translation found
    return line, ""


def load_mwambao():
    items = []
    if not MWAMBA_FILE.exists():
        print(f"No mwambao file found at {MWAMBA_FILE}")
        return items
    for ln in MWAMBA_FILE.read_text(encoding='utf-8').splitlines():
        ln = ln.strip()
        if not ln:
            continue
        quote, trans = split_line(ln)
        if not quote:
            continue
        items.append({
            "quote": quote.strip(),
            "translation": trans.strip() if trans else "",
            "person": "",
            "category": "mwambao",
            "source": "mwambao",
            "count": 1,
        })
    return items


def load_existing():
    if not DATA_FILE.exists():
        print(f"Data file not found: {DATA_FILE}")
        return []
    with DATA_FILE.open('r', encoding='utf-8') as f:
        data = json.load(f)
    # ensure count field exists
    for it in data:
        if 'count' not in it:
            it['count'] = 1
        if 'source' not in it:
            it['source'] = it.get('category', '') or 'unknown'
        # keep existing translation if present, else empty
        if 'translation' not in it:
            it['translation'] = ''
    return data


def find_best_match(norm, keys):
    # NOTE: This fallback should not be used; in merge() we supply a
    # trigram index to prefilter candidates. Keep a simple length-based
    # prefilter as a last resort to avoid worst-case full comparisons.
    if not norm or not keys:
        return None, 0.0
    nlen = len(norm)
    max_delta = max(3, int(nlen * 0.2))
    candidates = [k for k in keys if abs(len(k) - nlen) <= max_delta]
    if not candidates:
        return None, 0.0
    matches = difflib.get_close_matches(norm, candidates, n=1, cutoff=0.75)
    if not matches:
        return None, 0.0
    best = matches[0]
    best_ratio = difflib.SequenceMatcher(None, norm, best).ratio()
    return best, best_ratio


def merge(new_items, existing):
    # build normalized key map for existing
    norm_map = {}
    for i, it in enumerate(existing):
        n = normalize_text(it.get('quote', ''))
        if n:
            norm_map[n] = i

    existing_keys = list(norm_map.keys())

    # Build a simple trigram index for fast candidate lookup
    def trigrams(s):
        s = s.replace(' ', '_')
        return [s[i:i+3] for i in range(max(0, len(s)-2))]

    tri_index = {}
    for k in existing_keys:
        for t in set(trigrams(k)):
            tri_index.setdefault(t, set()).add(k)

    added = 0
    merged = 0
    for ni in new_items:
        nq = ni['quote']
        nn = normalize_text(nq)
        if not nn:
            continue
        # exact
        if nn in norm_map:
            idx = norm_map[nn]
            existing[idx]['count'] = existing[idx].get('count', 1) + ni.get('count', 1)
            merged += 1
            continue
        # fuzzy: use trigram index to produce a small candidate set
        query_tris = set(trigrams(nn))
        cand_counts = {}
        for t in query_tris:
            for k in tri_index.get(t, ()):  # may be empty
                cand_counts[k] = cand_counts.get(k, 0) + 1

        # take top candidates by shared trigram count
        if cand_counts:
            sorted_cands = sorted(cand_counts.items(), key=lambda x: x[1], reverse=True)
            candidates = [c for c, _ in sorted_cands[:30]]
        else:
            candidates = []

        best_key, ratio = find_best_match(nn, candidates if candidates else existing_keys)
        if best_key and ratio >= 0.92:
            idx = norm_map[best_key]
            existing[idx]['count'] = existing[idx].get('count', 1) + ni.get('count', 1)
            # if we have a translation and existing lacks it, add it
            if ni.get('translation') and not existing[idx].get('translation'):
                existing[idx]['translation'] = ni.get('translation')
            merged += 1
            continue
        # new entry
        new_entry = {
            'quote': ni['quote'],
            'person': ni.get('person', ''),
            'category': ni.get('category', ''),
            'translation': ni.get('translation', ''),
            'source': ni.get('source', 'mwambao'),
            'count': ni.get('count', 1),
        }
        existing.append(new_entry)
        # update maps
        new_norm = normalize_text(new_entry['quote'])
        norm_map[new_norm] = len(existing) - 1
        existing_keys.append(new_norm)
        added += 1

    return existing, added, merged


def main():
    print("Loading mwambao scraped items...")
    new_items = load_mwambao()
    print(f"Parsed {len(new_items)} new items")

    print("Loading existing dataset...")
    existing = load_existing()
    print(f"Existing items: {len(existing)}")

    merged_data, added, merged = merge(new_items, existing)
    print(f"Added: {added}, merged (count increments): {merged}")

    # backup
    bak = DATA_FILE.with_suffix('.json.bak')
    if not bak.exists():
        DATA_FILE.replace(bak)
        # reload from bak back to DATA_FILE to preserve original ordering when writing
        with bak.open('r', encoding='utf-8') as f:
            original = json.load(f)
        # write merged
        with DATA_FILE.open('w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=2)
        print(f"Wrote merged dataset to {DATA_FILE} (backup at {bak})")
    else:
        # if bak already exists, just write a timestamped backup
        from datetime import datetime
        bak2 = DATA_FILE.with_name(f"quotes.json.bak.{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}")
        DATA_FILE.replace(bak2)
        with DATA_FILE.open('w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=2)
        print(f"Wrote merged dataset to {DATA_FILE} (backup at {bak2})")


if __name__ == '__main__':
    main()
