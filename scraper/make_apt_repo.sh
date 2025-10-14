#!/usr/bin/env bash
set -euo pipefail

# Create a minimal apt repository containing the built .deb
# Usage: ./make_apt_repo.sh [path-to-deb] [repo-dir]

DEB_PATH=${1:-"$(pwd)/fortune-swahili_0.1_all.deb"}
REPO_DIR=${2:-"$(pwd)/apt-repo"}

if [ ! -f "$DEB_PATH" ]; then
  echo "Deb not found: $DEB_PATH" >&2
  exit 2
fi

mkdir -p "$REPO_DIR/pool/main/f/fortune-swahili"
cp -v "$DEB_PATH" "$REPO_DIR/pool/main/f/fortune-swahili/"

cd "$REPO_DIR"

# generate Packages and compress
dpkg-scanpackages pool /dev/null > Packages
gzip -f -k Packages

# create a simple Release file
cat > Release <<'REL'
Origin: fortune-swahili
Label: fortune-swahili
Suite: stable
Codename: stable
Date: PLACEHOLDER
Architectures: all
Components: main
Description: A small apt repo with fortune-swahili package
REL

# set Date
python3 - <<PY
from datetime import datetime
from pathlib import Path
rt = Path('Release')
txt = rt.read_text()
txt = txt.replace('PLACEHOLDER', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S UTC'))
rt.write_text(txt)
print('Wrote Release')
PY

echo "Repo created at: $REPO_DIR"
echo "Upload the contents of $REPO_DIR to a static web host and add 'deb [trusted=yes] http://yourhost/path stable main' to clients' sources.list"
