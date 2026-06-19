from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_CONFIG_PATH = Path(os.getenv("DYT_CONFIG_PATH", _ROOT / "config.json"))
_config = None


def get_config():
    global _config
    if _config is not None:
        return _config
    if not _CONFIG_PATH.exists():
        print(f"[CONFIG] Khong tim thay config.json tai: {_CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)
    try:
        text = _CONFIG_PATH.read_text(encoding="utf-8")
        _config = json.loads(text)
        return _config
    except Exception as e:
        print(f"[CONFIG] config.json loi: {e}", file=sys.stderr)
        sys.exit(1)


def load_config():
    return get_config()


def get_accesstrade_config():
    config = get_config()
    return config.get("accesstrade") or config.get("accessctrade") or {}


def get_access_key():
    key = get_accesstrade_config().get("access_key", "")
    if not key or key == "PASTE_YOUR_KEY_HERE":
        key = os.getenv("ACCESSTRADE_ACCESS_KEY") or os.getenv("ACCESSTRADE_API_KEY") or ""
    if not key or key == "PASTE_YOUR_KEY_HERE":
        print("[CONFIG] Chua dien access_key vao config.json!", file=sys.stderr)
        sys.exit(1)
    return key


def get_base_url():
    return get_accesstrade_config().get("base_url", "https://api.accesstrade.vn/v1")


def get_picker_config():
    return get_config().get("picker", {"min_commission_rate": 0.0, "top_n": 5, "loop_interval_minutes": 15})
