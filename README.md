# fortune-swahili

A Debian package providing 5,698 Swahili proverbs in a fortune-like command-line tool.

## Quick Install

Install from our GPG-signed APT repository:

```bash
# Add GPG signing key
curl -fsSL https://giftcharles.github.io/fortune-swahili/public.key.asc | \
  gpg --dearmor | \
  sudo tee /etc/apt/trusted.gpg.d/fortune-swahili.gpg > /dev/null

# Add repository
echo "deb [signed-by=/etc/apt/trusted.gpg.d/fortune-swahili.gpg] https://giftcharles.github.io/fortune-swahili stable main" | \
  sudo tee /etc/apt/sources.list.d/fortune-swahili.list

# Update and install
sudo apt update
sudo apt install fortune-swahili
```

## Usage

Display a random Swahili proverb:
```bash
fortune-swahili
```

Display multiple proverbs:
```bash
fortune-swahili --count 3
```

Help:
```bash
fortune-swahili -h
```

## Features

- 🌍 **5,698 Swahili proverbs** from 60 categories
- 🔐 **GPG-signed repository** for secure installation

## Data Source

Proverbs scraped from [Swahili Proverbs Database](https://swahiliproverbs.afrst.illinois.edu/) maintained by the University of Illinois.

## Categories

Includes proverbs about: Abuse, Alertness, Ambition, Anger, Appearance, Association, Borrowing, Compatibility, Consequences, Constancy, Consultation, Contentment, Cooperation, Cunning, Death, Decision, Drinking, and many more...

## Repository Details

- **URL**: https://giftcharles.github.io/fortune-swahili
- **GPG Key ID**: 6C365AAADEC5D261
- **Fingerprint**: A8CE 059B 44D0 BAEF BB63 072A 6C36 5AAA DEC5 D261
- **Package**: fortune-swahili_0.1_all.deb (364KB)

## Verification

Verify the repository signature:
```bash
curl -s https://giftcharles.github.io/fortune-swahili/dists/stable/Release | gpg --verify
```

## Documentation

- [INSTALL.md](INSTALL.md) - Detailed installation instructions
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete project overview

## License

See [LICENSE](LICENSE) file.

## Maintenance

This repository is automatically built and published via GitHub Actions on every push to `main`. All releases are GPG-signed for security.

---

**Status**: ✅ Production Ready  

## Development

Quick developer tasks and how to run things locally:

- Create a Python virtualenv and install runtime deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r scraper/requirements.txt
```

- Rebuild the .deb (uses `data/` by default):

```bash
cd scraper
./build_deb.sh ../data
```

- Use pre-parsed JSON files

```bash
# curated/parsing outputs are stored under scraper/ as JSON files.
# Use those JSON files directly; do not re-run raw HTML parsing scripts.
ls scraper/*.json
```

- Merge curated JSON extracts into the main dataset (creates a backup):

```bash
# merge any curated JSON files (keeps a backup of data/quotes.json)
python3 scraper/normalize_mwambao.py
```

- Run the full publish flow locally (produces `scraper/apt-repo`):

```bash
cd scraper
./make_apt_repo.sh ./fortune-swahili_0.2_all.deb ./apt-repo
```

-- To test the CLI locally against any JSON file:

```bash
python3 scraper/bin/fortune-swahili --data /path/to/quotes.json --count 3
```

If you plan to publish to GitHub Pages via the workflow, ensure the repository secrets `GPG_PRIVATE_KEY` and `GPG_PASSPHRASE` are set in the repo settings so the Release can be signed by CI.