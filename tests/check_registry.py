import logging
import sys
from pathlib import Path

# ensure project root is importable
sys.path.insert(0, str(Path(".").resolve()))

from src.orchestrator import load_workers, registry

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

if __name__ == "__main__":
    n = load_workers()
    print(f"Loaded {n} workers")
    assert "video.youtube_dl" in registry, f"Missing video.youtube_dl, found: {list(registry.keys())}"
    print("Test passed: video.youtube_dl present in registry")
