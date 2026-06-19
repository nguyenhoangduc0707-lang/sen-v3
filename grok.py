"""Run the DYT_01 Grok Secretary from the repository root."""

from __future__ import annotations

import runpy
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "experiments" / "grok_secretary.py"


if __name__ == "__main__":
    runpy.run_path(str(SCRIPT), run_name="__main__")
