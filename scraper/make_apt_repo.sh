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

# Generate Release file using apt-ftparchive for proper checksums
# Create config for apt-ftparchive
cat > apt-ftparchive.conf <<'EOF'
Dir {
  ArchiveDir ".";
};

TreeDefault {
  Directory "pool/";
};

BinDirectory "pool/main" {
  Packages "dists/stable/main/binary-all/Packages";
  Contents "dists/stable/Contents-all";
};

Default {
  Packages {
    Extensions ".deb";
  };
};
EOF

# Generate Release file with apt-ftparchive
cd dists/stable
apt-ftparchive release \
  -o APT::FTPArchive::Release::Origin="fortune-swahili" \
  -o APT::FTPArchive::Release::Label="fortune-swahili" \
  -o APT::FTPArchive::Release::Suite="stable" \
  -o APT::FTPArchive::Release::Codename="stable" \
  -o APT::FTPArchive::Release::Architectures="all" \
  -o APT::FTPArchive::Release::Components="main" \
  -o APT::FTPArchive::Release::Description="Swahili proverbs fortune package repository" \
  . > Release

cd ../..

echo "Repo created at: $REPO_DIR"
echo "Structure: dists/stable/main/binary-all/ and pool/"
echo "Add to sources.list: deb [signed-by=/path/to/key.gpg] https://yourhost/ stable main"
