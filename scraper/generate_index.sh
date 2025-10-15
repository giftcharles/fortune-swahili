#!/usr/bin/env bash
set -euo pipefail

# Usage: generate_index.sh <out-dir>
OUT=${1:-"./apt-repo"}
mkdir -p "$OUT"

# Get the directory where this script lives
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy the HTML template to the output directory
cp -f "$SCRIPT_DIR/index.html.template" "$OUT/index.html"

# Copy README/INSTALL and public key if present
cp -f ../README.md "$OUT/README.md" 2>/dev/null || true
cp -f ../INSTALL.md "$OUT/INSTALL.md" 2>/dev/null || true
cp -f public.key.asc "$OUT/public.key.asc" 2>/dev/null || true

echo "✅ Generated landing page at $OUT/index.html"
echo "✅ Copied documentation files"
