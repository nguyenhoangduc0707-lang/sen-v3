"""
Quick Monitor - Bảng theo dõi nhanh
"""
import sqlite3
import time
import os
from datetime import datetime

def quick_monitor():
    print("\n" + "=" * 60)
    print("🔍 SEN V3 QUICK MONITOR")
    print("=" * 60)
    
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    # 1. Today's sales
    cursor.execute("""
        SELECT COALESCE(SUM(revenue), 0), COALESCE(SUM(commission), 0)
        FROM sales_tracking 
        WHERE date = date('now')
    """)
    today_revenue, today_commission = cursor.fetchone()
    
    # 2. Pending tasks
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")
    pending_tasks = cursor.fetchone()[0]
    
    # 3. Completed today
    cursor.execute("""
        SELECT COUNT(*) FROM tasks 
        WHERE status = 'completed' 
        AND date(updated_at) = date('now')
    """)
    completed_today = cursor.fetchone()[0]
    
    # 4. Workers running
    cursor.execute("SELECT COUNT(*) FROM worker_stats WHERE status = 'running'")
    workers_running = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n💰 DOANH SỐ HÔM NAY:")
    print(f"   📈 Doanh thu: {today_revenue:,.0f} VND")
    print(f"   🎁 Hoa hồng: {today_commission:,.0f} VND")
    
    print(f"\n📋 TASK HÔM NAY:")
    print(f"   ✅ Hoàn thành: {completed_today}")
    print(f"   ⏳ Đang chờ: {pending_tasks}")
    
    print(f"\n👷 WORKERS:")
    print(f"   🟢 Đang chạy: {workers_running}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    quick_monitor()
