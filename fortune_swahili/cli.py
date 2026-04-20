"""fortune-swahili: prints a random Swahili proverb.

Cross-platform CLI that works whether installed via:
  - pip install fortune-swahili   (Linux, macOS, Windows)
  - apt install fortune-swahili   (.deb package)
  - running directly from a git clone

Data is discovered in this priority order:
  1. Path provided via --data
  2. Data bundled inside this Python package (pip installs)
  3. System path installed by the .deb (/usr/share/games/fortune-swahili/)
  4. Repository root data/ directory (development)
"""
import argparse
import json
import random
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Data discovery
# ---------------------------------------------------------------------------

def _find_data() -> str:
    """Return the best available path to the quotes data (file or directory)."""
    # 1. Data bundled with this Python package (pip install)
    pkg_data = Path(__file__).parent / "data" / "quotes.json"
    if pkg_data.is_file():
        return str(pkg_data)

    # 2. .deb install: single consolidated file
    deb_file = Path("/usr/share/games/fortune-swahili/quotes.json")
    if deb_file.is_file():
        return str(deb_file)

    # 3. .deb install: category-directory layout
    deb_dir = Path("/usr/share/games/fortune-swahili")
    if deb_dir.is_dir() and any(deb_dir.glob("*/quotes.json")):
        return str(deb_dir)

    # 4. Development: repo root data/ directory
    for candidate in (
        Path(__file__).parent.parent / "data",
        Path(__file__).parent / ".." / ".." / "data",
    ):
        candidate = candidate.resolve()
        if candidate.is_dir() and any(candidate.glob("*/quotes.json")):
            return str(candidate)

    # Fallback (will surface a clear error at runtime)
    return str(pkg_data)


def _find_nsfw() -> str:
    """Return the best available path to the nsfw word list."""
    candidates = [
        Path(__file__).parent / "nsfw.txt",                          # bundled
        Path(__file__).parent.parent / "scraper" / "nsfw.txt",       # dev
        Path("/usr/share/games/fortune-swahili/nsfw.txt"),            # .deb
    ]
    for c in candidates:
        if c.is_file():
            return str(c)
    return str(candidates[0])


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def load_quotes(path: Path) -> list:
    """Load quotes from a JSON file or a directory of category subdirectories."""
    if path.is_file():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    if path.is_dir():
        quotes: list = []
        for jf in sorted(path.glob("*/quotes.json")):
            with jf.open("r", encoding="utf-8") as f:
                quotes.extend(json.load(f))
        return quotes
    raise FileNotFoundError(f"Data path not found: {path}")


def format_quote(item: dict) -> str:
    """Return printable text for a quote entry."""
    return (item.get("quote") or "").strip()


def contains_nsfw(text: str, nsfw_words: set) -> bool:
    if not text:
        return False
    t = text.lower()
    return any(w and w in t for w in nsfw_words)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

_MAX_NSFW_FILTER_ATTEMPTS = 20


def main() -> None:
    p = argparse.ArgumentParser(
        description="Print a random Swahili proverb.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  fortune-swahili               # one random proverb\n"
            "  fortune-swahili --count 3     # three random proverbs\n"
            "  fortune-swahili --censor-nsfw # filter adult content\n"
        ),
    )
    p.add_argument(
        "--data",
        help="Path to a quotes JSON file or a directory of category sub-directories",
        default=_find_data(),
    )
    p.add_argument("--count", type=int, default=1, help="Number of random quotes to print")
    p.add_argument("--censor-nsfw", action="store_true", help="Filter out NSFW quotes")
    p.add_argument(
        "--nsfw-file",
        default=_find_nsfw(),
        help="Path to newline-separated NSFW tokens",
    )
    args = p.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        print(
            f"Error: data not found at '{data_path}'.\n"
            "Specify a path with --data, e.g.:\n"
            "  fortune-swahili --data /path/to/data/quotes.json",
            file=sys.stderr,
        )
        sys.exit(2)

    quotes = load_quotes(data_path)
    if not quotes:
        sys.exit(0)

    nsfw_words: set = set()
    if args.censor_nsfw:
        nsfw_path = Path(args.nsfw_file)
        if nsfw_path.is_file():
            for ln in nsfw_path.read_text(encoding="utf-8").splitlines():
                ln = ln.strip()
                if ln and not ln.startswith("#"):
                    nsfw_words.add(ln.lower())
        else:
            print(f"Warning: NSFW file not found: {nsfw_path}", file=sys.stderr)

    for i in range(args.count):
        item = None
        for _ in range(_MAX_NSFW_FILTER_ATTEMPTS):
            candidate = random.choice(quotes)
            if args.censor_nsfw and contains_nsfw(candidate.get("quote", ""), nsfw_words):
                continue
            item = candidate
            break
        if item is None:
            item = random.choice(quotes)
        print(format_quote(item))
        if i != args.count - 1:
            print()


if __name__ == "__main__":
    main()
