"""
Optional database cleanup script for legacy tables.

Run only after you are sure the new models (Task + FacebookAccount + ScheduledTask + AffiliateLink) are working.

Usage:
    python scripts/db_cleanup.py --dry-run
    python scripts/db_cleanup.py --execute
"""

import argparse
import sqlite3
from pathlib import Path

LEGACY_TABLES = [
    "facebook_posts",   # replaced by Task + FacebookAccount
    "campaigns",        # old affiliate fetcher table
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Only show what would be dropped")
    parser.add_argument("--execute", action="store_true", help="Actually drop the tables")
    args = parser.parse_args()

    db_path = Path("sen_v3.db")
    if not db_path.exists():
        print("Database not found. Nothing to clean.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    for table in LEGACY_TABLES:
        cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        if cur.fetchone():
            if args.dry_run:
                print(f"[DRY] Would drop table: {table}")
            elif args.execute:
                print(f"Dropping table: {table}")
                cur.execute(f"DROP TABLE IF EXISTS {table}")
        else:
            print(f"Table not present: {table}")

    if args.execute:
        conn.commit()
        print("Cleanup committed.")

    conn.close()


if __name__ == "__main__":
    main()
