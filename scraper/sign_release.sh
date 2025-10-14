#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: sign_release.sh <Release-file> [passphrase]" >&2
  exit 2
fi

RELEASE_FILE="$1"
PASSPHRASE="${2:-}"

if [ ! -f "$RELEASE_FILE" ]; then
  echo "Release file not found: $RELEASE_FILE" >&2
  exit 2
fi

# create detached binary signature (Release.gpg) and clearsigned InRelease
# apt clients expect a binary detached signature (not ASCII-armored) named Release.gpg
# and a clearsigned file named InRelease. Sign to temporary files and move them
# into place only on success to avoid leaving empty files when GPG fails.
OUT_DIR="$(dirname "$RELEASE_FILE")"
TMP_SIG=$(mktemp "$OUT_DIR/Release.gpg.tmp.XXXX")
TMP_INREL=$(mktemp "$OUT_DIR/InRelease.tmp.XXXX")

set -x
if gpg --batch --yes --pinentry-mode loopback ${PASSPHRASE:+--passphrase "$PASSPHRASE"} --output "$TMP_SIG" --detach-sign "$RELEASE_FILE"; then
  if gpg --batch --yes --pinentry-mode loopback ${PASSPHRASE:+--passphrase "$PASSPHRASE"} --clearsign --output "$TMP_INREL" "$RELEASE_FILE"; then
    mv -f "$TMP_SIG" "$OUT_DIR/Release.gpg"
    mv -f "$TMP_INREL" "$OUT_DIR/InRelease"
    echo "Signed release: $OUT_DIR/Release.gpg and $OUT_DIR/InRelease"
    exit 0
  else
    echo "Failed to clearsign Release file" >&2
    rm -f "$TMP_SIG" "$TMP_INREL"
    exit 3
  fi
else
  echo "Failed to create detached signature for Release" >&2
  rm -f "$TMP_SIG" "$TMP_INREL"
  exit 2
fi
