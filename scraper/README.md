Swahili Proverbs Scraper
=======================

This small scraper fetches category pages from the Swahili Proverbs site and saves proverbs
into delimited text files. Directory structure mirrors categories under `data/`.

Requirements
- Python 3.8+
- Install dependencies:

pip install -r requirements.txt


Usage
- Scrape a single category (example: Abuse):

python scrape_swahili_proverbs.py --category abuse.html --out ../data

- Crawl all categories (uses the listing page) and write JSON index:

python scrape_swahili_proverbs.py --out ../data --format json

Output format
- Files are placed in `data/<Category>/quotes.json` (or quotes.txt if --format text).
- Each JSON file is a list of objects with fields: quote, person, tail (explanatory text).
- The combined index is `data/quotes.json` containing objects with quote, person, category.

Packaging for fortune-like use
- I include a small CLI script `bin/fortune-swahili` that reads the combined JSON index and prints a random quote.
- A basic Debian package builder is provided in `debianize/` to assemble a .deb that installs the JSON data under `/usr/share/games/fortune-swahili` and the CLI into `/usr/games`.


Notes
- The scraper uses simple heuristics to extract the Swahili proverb (from <strong> tags)
  and a loose attempt to extract an attributed person. This can be improved if needed.
