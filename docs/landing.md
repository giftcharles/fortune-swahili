# fortune-swahili — APT repository landing page

This repository hosts a small Debian package, `fortune-swahili`, containing 5,698 Swahili proverbs organized into 60 categories. The package provides a fortune-like CLI that prints random Swahili proverbs.

## Quick facts

- Package: `fortune-swahili_0.1_all.deb`
- Size: ~364 KB
- Proverbs: 5,698
- Categories: 60
- Repository: GPG-signed (Key ID: `6C365AAADEC5D261`)
- Hosted on GitHub Pages: https://giftcharles.github.io/fortune-swahili

## Installation

1. Import the GPG signing key:

```bash
curl -fsSL https://giftcharles.github.io/fortune-swahili/public.key.asc | \
  gpg --dearmor | \
  sudo tee /etc/apt/trusted.gpg.d/fortune-swahili.gpg > /dev/null
```

2. Add the repository to your APT sources:

```bash
echo "deb [signed-by=/etc/apt/trusted.gpg.d/fortune-swahili.gpg] https://giftcharles.github.io/fortune-swahili stable main" | \
  sudo tee /etc/apt/sources.list.d/fortune-swahili.list
```

3. Update and install:

```bash
sudo apt update
sudo apt install fortune-swahili
```

## Usage

- Display one random proverb:

```bash
fortune-swahili
```

- Display three random proverbs:

```bash
fortune-swahili 3
```

## Verifying signatures

Download Release and signature and verify locally:

```bash
curl -O https://giftcharles.github.io/fortune-swahili/dists/stable/Release
curl -O https://giftcharles.github.io/fortune-swahili/dists/stable/Release.gpg
curl https://giftcharles.github.io/fortune-swahili/public.key.asc | gpg --import
gpg --verify Release.gpg Release
```

You should see `Good signature from "giftcharles (Cool!) <giftnakembetwa@gmail.com>"`.

## CI / Publishing

- A GitHub Actions workflow builds the `.deb`, creates APT metadata using `apt-ftparchive`, signs the Release using a GPG key supplied via repository secrets, and publishes the `apt-repo` to the `gh-pages` branch.
- Required repo secrets:
  - `GPG_PRIVATE_KEY` — ASCII-armored private key
  - `GPG_PASSPHRASE` — passphrase for the private key

## Notes for maintainers

- To update the proverbs, update the `data/` files and push to `main`. CI will rebuild and publish automatically.
- The published site includes an `index.html` landing page, `README.md`, and `INSTALL.md` for quick access.

---

If you'd like, I can also create a nicer Jekyll-based or custom HTML landing page and add badges, screenshots, and a download button. Let me know the desired layout and details (logo, colors, extra content).