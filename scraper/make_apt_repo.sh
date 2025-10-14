#!/usr/bin/env bash
set -euo pipefail

# Create a proper Debian apt repository structure containing the built .deb
# Usage: ./make_apt_repo.sh [path-to-deb] [repo-dir]

DEB_PATH=${1:-"$(pwd)/fortune-swahili_0.1_all.deb"}
REPO_DIR=${2:-"$(pwd)/apt-repo"}

if [ ! -f "$DEB_PATH" ]; then
  echo "Deb not found: $DEB_PATH" >&2
  exit 2
fi

# Create proper Debian repository structure
mkdir -p "$REPO_DIR/pool/main/f/fortune-swahili"
mkdir -p "$REPO_DIR/dists/stable/main/binary-all"

# Copy .deb to pool
cp -v "$DEB_PATH" "$REPO_DIR/pool/main/f/fortune-swahili/"

cd "$REPO_DIR"

# Generate Packages file for binary-all architecture
dpkg-scanpackages --arch all pool /dev/null > dists/stable/main/binary-all/Packages
gzip -f -k dists/stable/main/binary-all/Packages

# Create Release file in dists/stable/
cat > dists/stable/Release <<'REL'
Origin: fortune-swahili
Label: fortune-swahili
Suite: stable
Codename: stable
Date: PLACEHOLDER
Architectures: all
Components: main
Description: Swahili proverbs fortune package repository
REL

# Set date and add checksums
python3 - <<'PY'
from datetime import datetime
from pathlib import Path
import hashlib

def file_hash(path, algo):
    h = hashlib.new(algo)
    h.update(Path(path).read_bytes())
    return h.hexdigest()

# Update date
release_path = Path('dists/stable/Release')
txt = release_path.read_text()
txt = txt.replace('PLACEHOLDER', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S UTC'))

# Add checksums for Packages files
packages_file = 'dists/stable/main/binary-all/Packages'
packages_gz = packages_file + '.gz'

md5_pkgs = file_hash(packages_file, 'md5')
sha1_pkgs = file_hash(packages_file, 'sha1')
sha256_pkgs = file_hash(packages_file, 'sha256')
size_pkgs = Path(packages_file).stat().st_size

md5_gz = file_hash(packages_gz, 'md5')
sha1_gz = file_hash(packages_gz, 'sha1')
sha256_gz = file_hash(packages_gz, 'sha256')
size_gz = Path(packages_gz).stat().st_size

txt += f"\nMD5Sum:\n {md5_pkgs} {size_pkgs} main/binary-all/Packages\n {md5_gz} {size_gz} main/binary-all/Packages.gz\n"
txt += f"SHA1:\n {sha1_pkgs} {size_pkgs} main/binary-all/Packages\n {sha1_gz} {size_gz} main/binary-all/Packages.gz\n"
txt += f"SHA256:\n {sha256_pkgs} {size_pkgs} main/binary-all/Packages\n {sha256_gz} {size_gz} main/binary-all/Packages.gz\n"

release_path.write_text(txt)
print('Wrote Release with checksums')
PY

echo "Repo created at: $REPO_DIR"
echo "Structure: dists/stable/main/binary-all/ and pool/"
echo "Add to sources.list: deb [signed-by=/path/to/key.gpg] https://yourhost/ stable main"
