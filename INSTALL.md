# Installation Guide

fortune-swahili runs on **Linux**, **macOS**, and **Windows**. Choose the
method that suits your system.

---

## Option 1 — pip (Linux, macOS, Windows) ✅ Recommended

Requires **Python 3.8+** and `pip`. Works on any operating system.

```bash
pip install fortune-swahili
```

Then use it immediately:

```bash
fortune-swahili               # one random Swahili proverb
fortune-swahili --count 3     # three proverbs
```

### Install from source (git clone)

```bash
git clone https://github.com/giftcharles/fortune-swahili.git
cd fortune-swahili
pip install .
fortune-swahili
```

---

## Option 2 — apt / Debian package (Debian, Ubuntu, Linux Mint, Raspberry Pi OS)

### Quick Install (3 commands)

```bash
# 1. Add GPG signing key
curl -fsSL https://giftcharles.github.io/fortune-swahili/public.key.asc | \
  gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/fortune-swahili.gpg > /dev/null

# 2. Add repository
echo "deb [signed-by=/etc/apt/trusted.gpg.d/fortune-swahili.gpg] \
  https://giftcharles.github.io/fortune-swahili stable main" | \
  sudo tee /etc/apt/sources.list.d/fortune-swahili.list

# 3. Install
sudo apt update && sudo apt install fortune-swahili
```

### Verify the GPG signature

```bash
# Download the Release file and signature
curl -O https://giftcharles.github.io/fortune-swahili/dists/stable/Release
curl -O https://giftcharles.github.io/fortune-swahili/dists/stable/Release.gpg

# Import the public key
curl https://giftcharles.github.io/fortune-swahili/public.key.asc | gpg --import

# Verify the signature
gpg --verify Release.gpg Release
# Expected: Good signature from "giftcharles (Cool!) <giftnakembetwa@gmail.com>"
```

---

## Option 3 — macOS

```bash
pip3 install fortune-swahili
fortune-swahili
```

Or run without modifying your PATH:

```bash
python3 -m fortune_swahili.cli
```

---

## Option 4 — Windows

Open **Command Prompt** or **PowerShell**:

```powershell
pip install fortune-swahili
fortune-swahili
```

> **Note**: Ensure Python is on your `PATH` during installation.
> Alternatively run `py -m fortune_swahili.cli`.

---

## Option 5 — Fedora / RHEL / Arch / other Linux

No native RPM/PKGBUILD yet — use pip (Option 1).

---

## Usage

```
fortune-swahili [--count N] [--censor-nsfw] [--data PATH] [--help]

Options:
  --count N        Print N random proverbs (default: 1)
  --censor-nsfw    Filter out proverbs containing adult content
  --data PATH      Path to a quotes JSON file or a data directory
                   (auto-detected by default)
```

---

## Repository Details (apt)

- **Repository URL**: https://giftcharles.github.io/fortune-swahili
- **GPG Key ID**: 6C365AAADEC5D261
- **GPG Fingerprint**: A8CE 059B 44D0 BAEF BB63 072A 6C36 5AAA DEC5 D261
- **Package**: fortune-swahili_0.3.1_all.deb
- **Data**: 5,698 Swahili proverbs across 59 categories

## Automated CI

The repository is automatically built via GitHub Actions on every push to
`main`. The workflow builds both the Debian `.deb` package **and** a
cross-platform Python wheel.
