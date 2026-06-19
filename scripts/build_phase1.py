"""Create the minimal Phase 1 project folders and starter config.

The script is safe by default: it will not overwrite an existing config.json
unless --force is passed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = {
    "accesstrade": {
        "access_key": "PASTE_YOUR_KEY_HERE",
        "base_url": "https://api.accesstrade.vn/v1",
        "timeout_seconds": 30,
    },
    "picker": {
        "min_commission_rate": 0.05,
        "top_n": 5,
        "loop_interval_minutes": 15,
    },
}


def ensure_dirs(root: Path) -> None:
    for relative in ("logs", "data", "cache", "fullwork/workers"):
        path = root / relative
        path.mkdir(parents=True, exist_ok=True)
        print(f"OK directory: {path}")


def write_config(root: Path, force: bool = False) -> None:
    path = root / "config.json"
    if path.exists() and not force:
        print(f"SKIP existing config: {path}")
        return

    path.write_text(
        json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"OK config: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Overwrite config.json")
    args = parser.parse_args()

    ensure_dirs(ROOT)
    write_config(ROOT, force=args.force)


if __name__ == "__main__":
    main()
