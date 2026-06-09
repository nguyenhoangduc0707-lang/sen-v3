#!/usr/bin/env python3
"""
Log conversion events (clicks, sales, revenue) attributed to a task/post.

Mục đích: Bổ sung data chất lượng thật để optimizer tối ưu TỈ LỆ CHUYỂN ĐỔI chính xác hơn.

Sử dụng:
  # Ghi nhận từ 1 bài đăng FB (task_id từ queue)
  python log_conversion.py --task_id 42 --clicks 128 --sales 3 --revenue 1450000 --note "post 18h affiliate_fashion"

  # Chỉ clicks
  python log_conversion.py --task_id 42 --clicks 55

  # Xem conversions đã log (gần đây)
  python log_conversion.py --list

Data được:
- Cập nhật vào Task (total_clicks, total_conversions, actual_commission ~ revenue proxy)
- Ghi raw event vào data/conversions.jsonl (dễ import sau này)

Sau này: optimizer.get_historical_performance sẽ có thể kết hợp signal này (không chỉ đếm COMPLETED).
"""
import argparse
import json
import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from src.db.session import get_engine
from src.db.models import Task

CONV_LOG = os.path.join("data", "conversions.jsonl")

def ensure_data_dir():
    os.makedirs("data", exist_ok=True)

def append_event(event: dict):
    ensure_data_dir()
    with open(CONV_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

def update_task_stats(task_id: int, clicks: int = 0, sales: int = 0, revenue: float = 0.0):
    """Update existing commission field on Task. Clicks/sales are primarily in the jsonl log for now.
    (We can extend Task model with clicks/conversions columns + migration later if volume grows.)
    """
    s = sessionmaker(bind=get_engine())()
    t = s.get(Task, task_id)
    if not t:
        print(f"⚠️ Task #{task_id} not found.")
        s.close()
        return False
    t.actual_commission = (t.actual_commission or 0.0) + revenue
    s.commit()
    s.refresh(t)
    print(f"✓ Updated Task #{task_id} revenue proxy (actual_commission += {revenue})")
    print(f"  Note: clicks={clicks}, sales={sales} recorded in data/conversions.jsonl (raw source for future optimizer).")
    print(f"  Current task actual_commission: {t.actual_commission}")
    s.close()
    return True

def list_recent(limit: int = 20):
    ensure_data_dir()
    if not os.path.exists(CONV_LOG):
        print("Chưa có log conversions nào.")
        return
    print(f"=== Recent conversions from {CONV_LOG} (last {limit}) ===")
    lines = []
    with open(CONV_LOG, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                lines.append(json.loads(line))
    for ev in lines[-limit:]:
        print(f"  {ev.get('ts')} task={ev.get('task_id')} clicks={ev.get('clicks',0)} sales={ev.get('sales',0)} revenue={ev.get('revenue',0)} note={ev.get('note','')[:40]}")

def main():
    p = argparse.ArgumentParser(description="Log real conversion data (clicks/sales) for conversion optimization.")
    p.add_argument("--task_id", type=int, help="ID of the Task (from queue) that generated the post")
    p.add_argument("--clicks", type=int, default=0)
    p.add_argument("--sales", type=int, default=0, help="Số đơn / conversions")
    p.add_argument("--revenue", type=float, default=0.0, help="Doanh thu hoặc hoa hồng thực nhận (VND)")
    p.add_argument("--note", default="")
    p.add_argument("--list", action="store_true", help="List recent logged conversions")
    args = p.parse_args()

    if args.list:
        list_recent()
        return

    if not args.task_id:
        print("Need --task_id (or use --list). See --help.")
        return

    event = {
        "ts": datetime.utcnow().isoformat(),
        "task_id": args.task_id,
        "clicks": args.clicks,
        "sales": args.sales,
        "revenue": args.revenue,
        "note": args.note,
    }
    append_event(event)
    print(f"Logged event: {event}")

    if args.clicks or args.sales or args.revenue:
        update_task_stats(args.task_id, args.clicks, args.sales, args.revenue)

    print("\nTip: Sau khi log vài event chất lượng, chạy lại analyze_performance.py (sẽ mở rộng sau để dùng signal này).")
    print("      Optimizer sẽ ưu tiên giờ có sales/clicks cao thay vì chỉ đếm số post COMPLETED.")

if __name__ == "__main__":
    main()
