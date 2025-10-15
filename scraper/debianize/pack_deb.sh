#!/usr/bin/env bash
# Simple script to assemble a .deb package named fortune-swahili_1.0_all.deb
set -euo pipefail
rootdir=$(cd "$(dirname "$0")/.." && pwd)
pkgdir="$rootdir/debian_pack"
rm -rf "$pkgdir"
mkdir -p "$pkgdir/DEBIAN"
mkdir -p "$pkgdir/usr/games"
mkdir -p "$pkgdir/usr/share/games/fortune-swahili"

# copy CLI
install -m 755 "$rootdir/bin/fortune-swahili" "$pkgdir/usr/games/fortune-swahili"

# copy data (expects data/quotes.json to exist)
cp -a "$rootdir/../data/quotes.json" "$pkgdir/usr/share/games/fortune-swahili/" || true

# control file
cat > "$pkgdir/DEBIAN/control" <<EOF
Package: fortune-swahili
Version: 1.0
Section: games
Priority: optional
Architecture: all
Maintainer: <you@localhost>
Description: Swahili proverbs for fortune-like use
 A simple package that installs Swahili proverbs and a small CLI to print one at random.
EOF

dpkg-deb --build "$pkgdir" "$rootdir/fortune-swahili_1.0_all.deb"
echo "Built $rootdir/fortune-swahili_1.0_all.deb"
