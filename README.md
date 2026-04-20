# fortune-swahili

A command-line tool that serves up 5,698 Swahili proverbs — one at a time or in batches — on Linux, macOS, and Windows. Think of it as `fortune`, but with wisdom from East Africa.

## Quick Install

The easiest path on any platform is pip:

```bash
pip install fortune-swahili
```

If you're on Debian, Ubuntu, or Linux Mint and prefer a native package, you can add the apt repository:

```bash
curl -fsSL https://giftcharles.github.io/fortune-swahili/public.key.asc | \
  gpg --dearmor | \
  sudo tee /etc/apt/trusted.gpg.d/fortune-swahili.gpg > /dev/null

echo "deb [signed-by=/etc/apt/trusted.gpg.d/fortune-swahili.gpg] https://giftcharles.github.io/fortune-swahili stable main" | \
  sudo tee /etc/apt/sources.list.d/fortune-swahili.list

sudo apt update
sudo apt install fortune-swahili
```

Want to install from source, or on macOS, Windows, Fedora, or Arch? See [INSTALL.md](INSTALL.md) — there's a method for every setup.

## Usage

```bash
fortune-swahili               # one random proverb
fortune-swahili --count 3     # three proverbs
fortune-swahili --censor-nsfw # filter adult content
fortune-swahili -h            # full help
```

## Features

- 🌍 **5,698 proverbs** spanning 59 categories — there's always something new
- 🖥️ **Truly cross-platform** — the same pip install works on Linux, macOS, and Windows
- 🔐 **GPG-signed apt repository** so Debian/Ubuntu users get verified packages

## Data Source

Proverbs scraped from [Swahili Proverbs Database](https://swahiliproverbs.afrst.illinois.edu/) maintained by the University of Illinois.

## Categories

Includes proverbs about: Abuse, Alertness, Ambition, Anger, Appearance, Association, Borrowing, Compatibility, Consequences, Constancy, Consultation, Contentment, Cooperation, Cunning, Death, Decision, Drinking, and many more...

## Repository Details

The apt repository is hosted on GitHub Pages and GPG-signed on every release. Full key details, fingerprints, and verification steps are in [INSTALL.md](INSTALL.md).

## Documentation

- [INSTALL.md](INSTALL.md) - All installation methods (pip, apt, macOS, Windows, Fedora/Arch, source)
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete project overview

## License

See [LICENSE](LICENSE) file.

## Maintenance

CI builds and publishes every push to `main` automatically. All releases are GPG-signed.

---

**Status**: ✅ Production Ready  

## Development

Here's what you need to get up and running locally as a contributor.

Start by installing the package in editable mode so changes to the source take effect immediately:

```bash
pip install -e .
fortune-swahili
```

If you need to run the scraper or other data-processing scripts, set up a virtualenv with the extra dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r scraper/requirements.txt
```

To build a distributable wheel and sdist:

```bash
pip install build
python -m build
# outputs: dist/fortune_swahili-0.3.1-py3-none-any.whl
```

To rebuild the `.deb` package:

```bash
cd scraper
./build_deb.sh ../data
```

The curated and parsed JSON files live under `scraper/`. Use them directly rather than re-running the raw HTML parsing scripts:

```bash
# curated/parsing outputs are stored under scraper/ as JSON files.
# Use those JSON files directly; do not re-run raw HTML parsing scripts.
ls scraper/*.json
```

To merge any curated JSON extracts back into the main dataset (a backup is kept automatically):

```bash
# merge any curated JSON files (keeps a backup of data/quotes.json)
python3 scraper/normalize_mwambao.py
```

To run the full apt-repo publish flow locally:

```bash
cd scraper
./make_apt_repo.sh ./fortune-swahili_0.2_all.deb ./apt-repo
```

To test the CLI locally:

```bash
# Using pip editable install (recommended):
fortune-swahili --count 3

# Or run directly:
python3 -m fortune_swahili.cli --count 3

# Or use the legacy scraper script:
python3 scraper/bin/fortune-swahili --data data/quotes.json --count 3
```

If you plan to publish to GitHub Pages via the workflow, make sure `GPG_PRIVATE_KEY` and `GPG_PASSPHRASE` are set as repository secrets so CI can sign the release.

To publish to PyPI, set the `PYPI_TOKEN` secret; the workflow will call `twine upload` automatically on every push to `main`.