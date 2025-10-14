# Installation Guide

## Installing fortune-swahili from the apt repository

### Quick Install (3 commands)

```bash
# 1. Add GPG signing key
curl -fsSL https://giftcharles.github.io/fortune-swahili/public.key.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/fortune-swahili.gpg > /dev/null

# 2. Add repository to sources
echo "deb [signed-by=/etc/apt/trusted.gpg.d/fortune-swahili.gpg] https://giftcharles.github.io/fortune-swahili stable main" | sudo tee /etc/apt/sources.list.d/fortune-swahili.list

# 3. Install the package
sudo apt update && sudo apt install fortune-swahili
```

### 4. Use the CLI

Display a random Swahili proverb:
```bash
fortune-swahili
```

Display 3 random proverbs:
```bash
fortune-swahili 3
```

## Verification

The repository is GPG-signed. You can verify the signature manually:

```bash
# Download the Release file and signature
curl -O https://giftcharles.github.io/fortune-swahili/Release
curl -O https://giftcharles.github.io/fortune-swahili/Release.gpg

# Import the public key
curl https://giftcharles.github.io/fortune-swahili/public.key.asc | gpg --import

# Verify the signature
gpg --verify Release.gpg Release
```

You should see: `Good signature from "giftcharles (Cool!) <giftnakembetwa@gmail.com>"`

## Repository Details

- **Repository URL**: https://giftcharles.github.io/fortune-swahili
- **GPG Key ID**: 6C365AAADEC5D261
- **GPG Fingerprint**: A8CE 059B 44D0 BAEF BB63 072A 6C36 5AAA DEC5 D261
- **Package**: fortune-swahili_0.1_all.deb
- **Data**: 5,698 Swahili proverbs organized into 60 categories

## Automated Updates

The repository is automatically built and published via GitHub Actions whenever changes are pushed to the main branch. All releases are GPG-signed for security.
