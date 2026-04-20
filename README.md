# fortune-swahili

5,698 Swahili proverbs in a cross-platform command-line tool.
Runs on **Linux**, **macOS**, and **Windows**.

## Quick Install

### pip — any platform (Linux, macOS, Windows)

```bash
pip install fortune-swahili
```

### apt — Debian / Ubuntu / Linux Mint

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

See [INSTALL.md](INSTALL.md) for macOS, Windows, Fedora/Arch, and other options.

## Usage

```bash
fortune-swahili               # one random proverb
fortune-swahili --count 3     # three proverbs
fortune-swahili --censor-nsfw # filter adult content
fortune-swahili -h            # full help
```

## Features

- 🌍 **5,698 Swahili proverbs** from 59 categories
- 🖥️ **Cross-platform** — pip install works on Linux, macOS, Windows
- 🔐 **GPG-signed apt repository** for Debian/Ubuntu users

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

- Install the package in editable mode (recommended):

```bash
pip install -e .
fortune-swahili
```

- Or create a virtualenv and install scraper deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r scraper/requirements.txt
```

- Build the Python wheel and sdist:

```bash
pip install build
python -m build
# outputs: dist/fortune_swahili-0.3.1-py3-none-any.whl
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

- Run the full apt-repo publish flow locally (produces `scraper/apt-repo`):

```bash
cd scraper
./make_apt_repo.sh ./fortune-swahili_0.2_all.deb ./apt-repo
```

- Test the CLI locally:

```bash
# Using pip editable install (recommended):
fortune-swahili --count 3

# Or run directly:
python3 -m fortune_swahili.cli --count 3

# Or use the legacy scraper script:
python3 scraper/bin/fortune-swahili --data data/quotes.json --count 3
```

If you plan to publish to GitHub Pages via the workflow, ensure the repository
secrets `GPG_PRIVATE_KEY` and `GPG_PASSPHRASE` are set in the repo settings
so the Release can be signed by CI.

To publish to PyPI, set the `PYPI_TOKEN` secret; the workflow will call
`twine upload` automatically on every push to `main`.