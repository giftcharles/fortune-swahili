#!/usr/bin/env bash
set -euo pipefail

# Usage: generate_index.sh <out-dir>
OUT=${1:-"./apt-repo"}
mkdir -p "$OUT"

# copy README/INSTALL if present
cp -f ../README.md "$OUT/README.md" 2>/dev/null || true
cp -f ../INSTALL.md "$OUT/INSTALL.md" 2>/dev/null || true
cp -f public.key.asc "$OUT/public.key.asc" 2>/dev/null || true

cat > "$OUT/index.html" <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>fortune-swahili — APT repository</title>
  <style>
    body{font-family:system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;color:#111}
    header{border-bottom:1px solid #eee;padding-bottom:1rem;margin-bottom:1rem}
    pre{background:#f7f7f8;padding:1rem;border-radius:6px;overflow:auto}
    a{color:#0366d6}
  </style>
</head>
<body>
  <header>
    <h1>fortune-swahili</h1>
    <p>APT repository hosting the <strong>fortune-swahili</strong> package — a small Debian package of Swahili proverbs (5,698 items).</p>
    <p><strong>GPG-signed</strong> repository. Key ID: <code>6C365AAADEC5D261</code></p>
  </header>
  <section>
    <h2>Install</h2>
    <pre>curl -fsSL https://giftcharles.github.io/fortune-swahili/public.key.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/fortune-swahili.gpg

echo "deb [signed-by=/etc/apt/trusted.gpg.d/fortune-swahili.gpg] https://giftcharles.github.io/fortune-swahili stable main" | sudo tee /etc/apt/sources.list.d/fortune-swahili.list

sudo apt update
sudo apt install fortune-swahili</pre>
  </section>
  <section>
    <h2>Files</h2>
    <ul>
      <li><a href="/fortune-swahili/dists/stable/Release">dists/stable/Release</a></li>
      <li><a href="/fortune-swahili/dists/stable/Release.gpg">dists/stable/Release.gpg</a></li>
      <li><a href="/fortune-swahili/dists/stable/InRelease">dists/stable/InRelease</a></li>
      <li><a href="/fortune-swahili/dists/stable/main/binary-all/Packages">Packages</a></li>
      <li><a href="/fortune-swahili/pool/main/f/fortune-swahili/fortune-swahili_0.1_all.deb">.deb package</a></li>
    </ul>
  </section>
  <footer>
    <p>Repository generated and published automatically via GitHub Actions.</p>
  </footer>
</body>
</html>
HTML

echo "Wrote $OUT/index.html"
