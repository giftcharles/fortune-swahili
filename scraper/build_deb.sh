#!/usr/bin/env bash
set -euo pipefail

# Build a simple .deb that installs the fortune-swahili CLI and JSON data.
# Usage: ./build_deb.sh /absolute/path/to/scraper/data

DATA_DIR=${1:-"$(pwd)/../data"}
PKGDIR=$(mktemp -d)
PKGNAME=fortune-swahili_0.2_all

mkdir -p "$PKGDIR/DEBIAN"
mkdir -p "$PKGDIR/usr/bin"
mkdir -p "$PKGDIR/usr/share/games/fortune-swahili"

# copy control file
cp debian/control "$PKGDIR/DEBIAN/control"

# copy CLI
cp bin/fortune-swahili "$PKGDIR/usr/bin/fortune-swahili"
chmod 755 "$PKGDIR/usr/bin/fortune-swahili"

# copy JSON data (if exists). Before copying, strip any 'person' field from JSON objects
if [ -d "$DATA_DIR" ]; then
  mkdir -p "$PKGDIR/usr/share/games/fortune-swahili/"
  # find JSON files and clean them
  find "$DATA_DIR" -type f -name '*.json' | while read -r jf; do
  rel=$(realpath --relative-to="$DATA_DIR" "$jf")
  destdir=$(dirname "$PKGDIR/usr/share/games/fortune-swahili/$rel")
  mkdir -p "$destdir"
  # use python to remove 'person' keys from JSON arrays/objects
  python3 - <<PY
import json, sys, pathlib
src = pathlib.Path(r"$jf")
dst = pathlib.Path(r"$PKGDIR/usr/share/games/fortune-swahili") / pathlib.Path(r"$rel")
dst.parent.mkdir(parents=True, exist_ok=True)
try:
  j = json.loads(src.read_text(encoding='utf-8'))
  def clean(obj):
    if isinstance(obj, list):
      return [clean(i) for i in obj]
    if isinstance(obj, dict):
      obj.pop('person', None)
      for k,v in list(obj.items()):
        obj[k] = clean(v)
      return obj
    return obj
  clean(j)
  dst.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding='utf-8')
except Exception as e:
  # if parsing fails, just copy raw
  dst.write_text(src.read_text(encoding='utf-8'), encoding='utf-8')
PY
  done
fi

# fix permissions
find "$PKGDIR" -type d -exec chmod 755 {} +
find "$PKGDIR" -type f -exec chmod 644 {} +
chmod 755 "$PKGDIR/usr/bin/fortune-swahili"

dpkg-deb --build "$PKGDIR" "$PKGNAME.deb"
echo "Built $PKGNAME.deb"
