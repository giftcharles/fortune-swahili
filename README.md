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
fortune-swahili 3
```

## Features

- 🌍 **5,698 Swahili proverbs** from 60 categories
- 🔐 **GPG-signed repository** for secure installation
- 🤖 **Automated CI/CD** builds and publishes on every commit
- 📦 **Standard Debian package** (`fortune-swahili_0.1_all.deb`)
- 🚀 **Hosted on GitHub Pages** with proper APT structure

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
**Maintainer**: [giftcharles](https://github.com/giftcharles)
