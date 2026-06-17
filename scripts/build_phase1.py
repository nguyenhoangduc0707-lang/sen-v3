python - << 'EOF'
import pathlib
ROOT = pathlib.Path(r"E:\DYT_01")
for d in ["logs","data","cache","fullwork/workers"]:
    (ROOT/d).mkdir(parents=True, exist_ok=True)

(ROOT/"config.json").write_text('{\n  "accesstrade": {\n    "access_key": "PASTE_YOUR_KEY_HERE",\n    "base_url": "https://api.accesstrade.vn/v1",\n    "timeout_seconds": 30\n  },\n  "picker": {\n    "min_commission_rate": 0.05,\n    "top_n": 5,\n    "loop_interval_minutes": 15\n  }\n}', encoding="utf-8")
print("[OK] config.json")
EOF