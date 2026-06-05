import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from affiliate.fetcher import init_db


if __name__ == "__main__":
    init_db()
    print("Campaign table is ready.")
