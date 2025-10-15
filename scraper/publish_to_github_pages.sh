#!/usr/bin/env bash
set -euo pipefail

# Publish the prepared apt-repo/ directory to the gh-pages branch of a GitHub repo.
# This script will not attempt to push without a remote repo URL. It assumes you
# have git configured and that you have push rights to the target repo.
#
# Usage:
#   ./publish_to_github_pages.sh --repo git@github.com:USERNAME/REPO.git [--branch gh-pages] [--dir ./apt-repo]

REPO=""
BRANCH="gh-pages"
REPO_DIR="./apt-repo"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    --dir) REPO_DIR="$2"; shift 2 ;;
    -h|--help) echo "Usage: $0 --repo git@github.com:USER/REPO.git [--branch gh-pages] [--dir ./apt-repo]"; exit 0 ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done

if [ -z "$REPO" ]; then
  echo "--repo is required (e.g. git@github.com:username/repo.git)" >&2
  exit 2
fi


# resolve to absolute path early
if [ ! -d "$REPO_DIR" ]; then
  echo "Repo dir not found: $REPO_DIR" >&2
  exit 2
fi
REPO_DIR_ABS=$(realpath "$REPO_DIR")

# create a temporary clone
TMP=$(mktemp -d)

git clone --no-checkout "$REPO" "$TMP"
cd "$TMP"

# create or switch to branch (orphan for fresh gh-pages)
git checkout --orphan "$BRANCH" || git checkout "$BRANCH" || true
# remove existing files in the worktree
git rm -rf . >/dev/null 2>&1 || true

# copy files from the absolute repo dir into the temp clone
cp -r "$REPO_DIR_ABS"/* . || true

git add --all
git commit -m "Publish fortune-swahili apt repo" || true

echo "Pushing to remote $REPO branch $BRANCH"
git push "$REPO" "HEAD:$BRANCH" --force

echo "Published apt-repo to $REPO#$BRANCH"
