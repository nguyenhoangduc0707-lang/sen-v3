import os
from datetime import datetime

ENV_FILE = ".env"

if not os.path.exists(ENV_FILE):
    print("[ERR] Không tìm thấy .env")
else:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f".env.backup.{ts}"
    with open(ENV_FILE, "r", encoding="utf-8") as f_src, \
         open(backup_name, "w", encoding="utf-8") as f_dst:
        f_dst.write(f_src.read())
    print(f"[OK] Đã backup .env → {backup_name}")
