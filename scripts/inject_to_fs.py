import json
from datetime import datetime
from pathlib import Path

# Logic theo đúng src/task_queue.py của bạn
PENDING = Path("tasks/pending")
PENDING.mkdir(parents=True, exist_ok=True)


def inject_to_fs():
    # Payload khớp với cấu trúc task trong task_queue.py
    task = {
        "worker": "tiktok_worker",
        "payload": {"url": "https://tiktok.com/test"},
        "created_at": datetime.now().isoformat(),
    }
    fname = f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"

    with open(PENDING / fname, "w") as f:
        json.dump(task, f)
    print(f"✅ Đã tạo file task tại: {PENDING / fname}")


if __name__ == "__main__":
    inject_to_fs()
