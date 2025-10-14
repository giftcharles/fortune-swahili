#!/usr/bin/env python3
"""Simple scraper for Swahili proverbs site.

Crawls category pages and saves each proverb into a delimited txt file.

Output directory structure mirrors categories, e.g. data/Abuse/quotes.txt
Each line in the file: quote|||quoted_person|||category

This script is conservative (no parallelism) and uses requests+BeautifulSoup.
"""
import os
import re
import sys
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE = "https://swahiliproverbs.afrst.illinois.edu"


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def parse_category(html: str):
    """Return a list of proverbs as dicts: {quote, person, raw_html}.

    Observed structure on category pages:
    - each proverb is inside a <p> where the proverb text in Swahili is inside a <strong>
    - after the strong text follows explanatory English text often separated by punctuation
    - there are abbreviation links; ignore them

    We'll extract the strong text as the quote field, and try to capture an attributed person
    by searching for patterns like "— Person" or "By Person" in the tailing text. If none,
    quoted person will be left empty.
    """
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find(text=re.compile("SWAHILI PROVERBS"))
    # fallback: use body
    container = soup.body if soup.body else soup

    proverbs = []
    for p in container.find_all("p"):
        strong = p.find("strong")
        if not strong:
            continue
        quote_text = strong.get_text(strip=True)
        # remove leading numbering like "1. "
        quote_text = re.sub(r"^\d+\.\s*", "", quote_text)

        # get the rest of paragraph text as possible attribution/source
        tail = ''.join([t for t in p.strings if t is not None])
        # remove the strong portion from tail
        tail = tail.replace(strong.get_text(), "")
        tail = re.sub(r"\s+", " ", tail).strip()

        # try to extract a quoted person pattern (improved heuristics)
        person = ''
        # normalize tail: remove bracketed refs like (123), [ABC], abbreviations (2., "20.")
        clean_tail = re.sub(r"\([^\)]*\)", "", tail)
        clean_tail = re.sub(r"\[[^\]]*\]", "", clean_tail)
        clean_tail = re.sub(r"\b(?:Cf|cf|See|see|link)[:.]?\b.*", "", clean_tail)
        # strip trailing citation-like fragments (e.g. ". 1181.")
        clean_tail = re.sub(r"\s+\d+[\.,]?\s*$", "", clean_tail)
        clean_tail = clean_tail.strip()

        # heuristic patterns (in order):
        # 1) em-dash or dash followed by Name (— Name or - Name)
        m = re.search(r"(?:—|-)\s*([A-Z][A-Za-z .'-]{2,})", clean_tail)
        if m:
            person = m.group(1).strip()
        # 2) 'By Name' or 'by Name' or 'Author: Name'
        if not person:
            m2 = re.search(r"\b[Bb]y\s+([A-Z][A-Za-z .'-]{2,})", clean_tail)
            if m2:
                person = m2.group(1).strip()
        if not person:
            m3 = re.search(r"\b[Aa]uthor[:\s]+([A-Z][A-Za-z .'-]{2,})", clean_tail)
            if m3:
                person = m3.group(1).strip()
        # 3) parenthetical attribution like "(— Name)" or trailing "-- Name"
        if not person:
            m4 = re.search(r"(?:--|—)\s*([A-Z][A-Za-z .'-]{2,})", tail)
            if m4:
                person = m4.group(1).strip()
        # 4) short names following comma near end: ", Name." e.g. "..., Said." (avoid common words)
        if not person:
            m5 = re.search(r",\s*([A-Z][A-Za-z .'-]{2,})[\.,]?\s*$", clean_tail)
            if m5:
                candidate = m5.group(1).strip()
                # avoid false positives that are single words like 'Cf' etc
                if len(candidate) > 2:
                    person = candidate

        proverbs.append({"quote": quote_text, "person": person, "tail": tail})

    return proverbs


def save_category(category_name: str, proverbs, outdir: Path, fmt: str = "json"):
    """Save proverbs for a category. Supports 'json' or 'text'."""
    cat_dir = outdir / category_name
    ensure_dir(cat_dir)
    if fmt == "json":
        out_file = cat_dir / "quotes.json"
        with out_file.open("w", encoding="utf-8") as f:
            json.dump(proverbs, f, ensure_ascii=False, indent=2)
    else:
        out_file = cat_dir / "quotes.txt"
        delim = "|||"
        with out_file.open("w", encoding="utf-8") as f:
            for p in proverbs:
                # escape delim in fields
                q = p['quote'].replace(delim, ' ')
                person = (p.get('person') or '').replace(delim, ' ')
                line = f"{q}{delim}{person}{delim}{category_name}\n"
                f.write(line)


def fetch(path: str):
    url = path if path.startswith("http") else BASE + ("/" + path.lstrip('/'))
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.text


def list_categories(index_html: str):
    """Parse the listing page and return list of (name, href) pairs."""
    soup = BeautifulSoup(index_html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a['href']
        text = a.get_text(strip=True)
        # category pages seem to be simple names like "abuse.html" or listing entry links
        if href.endswith('.html') and text and text.lower() not in ('intro', 'proverbs', 'kangas', 'links', 'contact'):
            links.append((text, href))
    # remove duplicates while keeping order
    seen = set()
    out = []
    for name, href in links:
        key = (name, href)
        if key in seen:
            continue
        seen.add(key)
        out.append((name, href))
    return out


def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--category", help="Category page href or name (e.g. abuse.html)")
    p.add_argument("--out", default="./data", help="Output directory")
    p.add_argument("--index", default=BASE + "/introduction%20to%20listing.html", help="Listing page URL")
    p.add_argument("--format", choices=["json", "text"], help="Output format: json (default) or text")
    args = p.parse_args()

    outdir = Path(args.out)
    ensure_dir(outdir)

    fmt = 'json' if args.format is None else args.format.lower()
    if args.category:
        print(f"Fetching category: {args.category}")
        html = fetch(args.category)
        proverbs = parse_category(html)
        save_category(Path(args.category).stem.replace(' ', '_'), proverbs, outdir, fmt=fmt)
        print(f"Saved {len(proverbs)} items to {outdir}/{Path(args.category).stem}/{ 'quotes.json' if fmt=='json' else 'quotes.txt'}")
        return

    # otherwise crawl all categories from listing
    print(f"Fetching index: {args.index}")
    idx_html = fetch(args.index)
    cats = list_categories(idx_html)
    print(f"Found {len(cats)} candidate categories")
    all_items = []
    for name, href in cats:
        try:
            html = fetch(href)
            proverbs = parse_category(html)
            cname = name.replace(' ', '_')
            save_category(cname, proverbs, outdir, fmt=fmt)
            print(f"Saved {len(proverbs)} items for {name}")
            # add category field to each item for global index
            for p in proverbs:
                item = {"quote": p['quote'], "person": p.get('person', ''), "category": cname}
                all_items.append(item)
        except Exception as e:
            print(f"Failed {name} ({href}): {e}")

    # save combined index
    idx_file = outdir / ("quotes.json" if fmt == 'json' else 'quotes.txt')
    if fmt == 'json':
        with idx_file.open('w', encoding='utf-8') as f:
            json.dump(all_items, f, ensure_ascii=False, indent=2)
        print(f"Saved combined index: {idx_file} ({len(all_items)} items)")
    else:
        delim = '|||'
        with idx_file.open('w', encoding='utf-8') as f:
            for p in all_items:
                q = p['quote'].replace(delim, ' ')
                person = (p.get('person') or '').replace(delim, ' ')
                line = f"{q}{delim}{person}{delim}{p['category']}\n"
                f.write(line)
        print(f"Saved combined index: {idx_file} ({len(all_items)} items)")


if __name__ == '__main__':
    main()
