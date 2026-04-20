#!/usr/bin/env python3
"""
clean_data.py – In-place data quality fixes for all data/*/quotes.json files.

Issues fixed:
  1. Numeric/index prefixes in quote field  (e.g. "33a. Kaa..." → "Kaa...")
  2. Broken/mixed-case in quote field       (e.g. "AkutuKAnaye" → "Akutukane")
  3. Stray non-standard characters          (leading É, embedded ÿ)
  4. person field fragments merged into tail
  5. tail field starts with stray leading punctuation (". " or ", ")
  6. Excess whitespace in quote and tail
  7. Duplicate category directories: data/abuse/ merged into data/Abuse/
"""

import json
import os
import re
import shutil

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
FLAT_FILE = os.path.join(DATA_DIR, "quotes.json")

# Specific broken-caps corrections (quote field)
BROKEN_CAPS_FIXES = {
    "AkutuKAnaye hakuchagulii tusi.": "Akutukane hakuchagulii tusi.",
}

# Regex: strip leading numeric/letter index like "33a. " or "111 . "
NUMERIC_PREFIX_RE = re.compile(r"^\d+[a-z]?\s*\.\s*")


def clean_quote(text: str) -> str:
    """Apply all quote-field cleaning rules."""
    # 1. Strip numeric/index prefix
    text = NUMERIC_PREFIX_RE.sub("", text)
    # 2. Broken/mixed-case fixes
    if text in BROKEN_CAPS_FIXES:
        text = BROKEN_CAPS_FIXES[text]
    # 3a. Strip leading É (scraping artifact)
    if text.startswith("É"):
        text = text[1:]
    # 3b. Remove stray ÿ characters
    text = text.replace("ÿ", "")
    # 6. Collapse internal whitespace and strip
    text = re.sub(r"  +", " ", text).strip()
    return text


def clean_tail(text: str) -> str:
    """Apply all tail-field cleaning rules."""
    # 5. Strip leading ". " or ", "
    text = re.sub(r"^[.,]\s+", "", text)
    # 6. Collapse internal whitespace and strip
    text = re.sub(r"  +", " ", text).strip()
    return text


def clean_entry(entry: dict) -> dict:
    """Clean a single proverb entry dict."""
    quote = entry.get("quote", "")
    tail = entry.get("tail", "")
    person = entry.get("person", "")

    # 4. Merge non-empty person into beginning of tail, then clear person
    if person.strip():
        if tail.strip():
            tail = person.strip() + " " + tail.strip()
        else:
            tail = person.strip()
        person = ""

    entry["quote"] = clean_quote(quote)
    entry["tail"] = clean_tail(tail)
    entry["person"] = person.strip()
    return entry


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def clean_file(path: str) -> int:
    """Clean all entries in a quotes.json file in-place. Returns number of modified entries."""
    data = load_json(path)
    modified = 0
    cleaned = []
    for entry in data:
        original = dict(entry)
        entry = clean_entry(dict(entry))
        if entry != original:
            modified += 1
        cleaned.append(entry)
    save_json(path, cleaned)
    return modified


def merge_abuse_dirs() -> int:
    """Merge data/abuse/ into data/Abuse/ (dedup by quote), remove data/abuse/."""
    abuse_lower = os.path.join(DATA_DIR, "abuse", "quotes.json")
    abuse_upper = os.path.join(DATA_DIR, "Abuse", "quotes.json")

    if not os.path.exists(abuse_lower):
        return 0

    upper_data = load_json(abuse_upper) if os.path.exists(abuse_upper) else []
    lower_data = load_json(abuse_lower)

    existing_quotes = {e["quote"] for e in upper_data}
    added = 0
    for entry in lower_data:
        if entry["quote"] not in existing_quotes:
            upper_data.append(entry)
            existing_quotes.add(entry["quote"])
            added += 1

    save_json(abuse_upper, upper_data)

    # Remove the lowercase directory
    lower_dir = os.path.join(DATA_DIR, "abuse")
    shutil.rmtree(lower_dir)

    return added


def main():
    files_modified = 0
    total_entries_modified = 0

    # Step 1: Merge data/abuse/ into data/Abuse/ before processing
    added = merge_abuse_dirs()
    if added >= 0:
        print(f"Abuse merge: {added} entries added from data/abuse/ → data/Abuse/ (directory removed)")

    # Step 2: Find all category quotes.json files (skip the flat combined file)
    category_files = []
    for root, dirs, files in os.walk(DATA_DIR):
        # Skip the external/ subdirectory if present
        dirs[:] = [d for d in sorted(dirs) if d != "external"]
        for fname in files:
            if fname != "quotes.json":
                continue
            path = os.path.join(root, fname)
            if os.path.abspath(path) == os.path.abspath(FLAT_FILE):
                continue
            category_files.append(path)

    for path in sorted(category_files):
        n = clean_file(path)
        rel = os.path.relpath(path, DATA_DIR)
        if n:
            print(f"  {rel}: {n} entries modified")
            files_modified += 1
            total_entries_modified += n

    # Step 3: Clean the flat combined file
    if os.path.exists(FLAT_FILE):
        n = clean_file(FLAT_FILE)
        if n:
            print(f"  quotes.json (flat): {n} entries modified")
            files_modified += 1
            total_entries_modified += n

    print(f"\nDone. {files_modified} file(s) modified, {total_entries_modified} entries cleaned.")


if __name__ == "__main__":
    main()
