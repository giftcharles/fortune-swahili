# Installation Guide

Pick the method that fits your setup — they all end up with the same `fortune-swahili` command.

---

## pip (Linux, macOS, Windows) ✅ Recommended

Requires Python 3.8+ and `pip`. Works on any operating system.

```bash
pip install fortune-swahili
```

Then use it immediately:

```bash
fortune-swahili               # one random Swahili proverb
fortune-swahili --count 3     # three proverbs
```

### Install from source (git clone)

If you want the latest unreleased changes, install directly from the repo instead:

```bash
git clone https://github.com/giftcharles/fortune-swahili.git
cd fortune-swahili
pip install .
fortune-swahili
```

---

## apt (Debian, Ubuntu, Linux Mint, Raspberry Pi OS)

If you're on a Debian-based system and prefer a native `.deb` package, here's the three-step setup.

First, trust the signing key so apt can verify the package:

```bash
curl -fsSL https://giftcharles.github.io/fortune-swahili/public.key.asc | \
  gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/fortune-swahili.gpg > /dev/null
```

Then register the repository:

```bash
echo "deb [signed-by=/etc/apt/trusted.gpg.d/fortune-swahili.gpg] \
  https://giftcharles.github.io/fortune-swahili stable main" | \
  sudo tee /etc/apt/sources.list.d/fortune-swahili.list
```

Now install:

```bash
sudo apt update && sudo apt install fortune-swahili
```

### Verify the GPG signature

Adding the GPG signing key keeps your system secure — you can double-check the signature yourself if you want to be sure the packages haven't been tampered with:

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

## macOS

pip works great on macOS — just run:

```bash
pip3 install fortune-swahili
fortune-swahili
```

If `fortune-swahili` isn't found after install (because your PATH isn't set up for pip scripts yet), you can run it directly with:

```bash
python3 -m fortune_swahili.cli
```

---

## Windows

Open **Command Prompt** or **PowerShell** and run:

```powershell
pip install fortune-swahili
fortune-swahili
```

> **Note**: Make sure Python is added to your `PATH` during installation — that's what lets you type `fortune-swahili` directly. If it's not on your PATH yet, `py -m fortune_swahili.cli` will always work as a fallback.

---

## Fedora / RHEL / Arch / other Linux

There's no native RPM or PKGBUILD yet, but pip is your friend here — it works just as well as on any other platform:

```bash
pip install fortune-swahili
```

---

## Usage

Once installed, here's everything the CLI can do:

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

CI builds and publishes every push to `main` automatically, producing both the `.deb` package and a cross-platform Python wheel.
