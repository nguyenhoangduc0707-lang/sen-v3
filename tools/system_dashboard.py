"""
Main Dashboard - Bảng theo dõi tổng hợp (không cần tabulate)
"""
import sqlite3
import os
import psutil
from datetime import datetime

class SystemDashboard:
    def __init__(self):
        self.db_path = "sen_v3.db"
    
    def get_affiliate_stats(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM accesstrade_campaigns")
        total_campaigns = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM acfc_promotions WHERE status = 'active'")
        active_acfc = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT 
                COALESCE(SUM(revenue), 0),
                COALESCE(SUM(commission), 0),
                COALESCE(SUM(clicks), 0),
                COALESCE(SUM(orders), 0)
            FROM sales_tracking
        """)
        revenue, commission, clicks, orders = cursor.fetchone()
        
        conn.close()
        
        return {
            "total_campaigns": total_campaigns,
            "active_acfc": active_acfc,
            "revenue": revenue,
            "commission": commission,
            "clicks": clicks,
            "orders": orders
        }
    
    def get_worker_stats(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COALESCE(COUNT(*), 0),
                COALESCE(SUM(tasks_processed), 0),
                COALESCE(SUM(tasks_succeeded), 0),
                COALESCE(SUM(tasks_failed), 0)
            FROM worker_stats
        """)
        workers, tasks, succeeded, failed = cursor.fetchone()
        
        cursor.execute("""
            SELECT task_type, status, created_at 
            FROM tasks 
            ORDER BY id DESC 
            LIMIT 5
        """)
        recent_tasks = cursor.fetchall()
        
        conn.close()
        
        success_rate = round((succeeded or 0) / (tasks or 1) * 100, 2)
        
        return {
            "total_workers": workers,
            "total_tasks": tasks,
            "succeeded": succeeded,
            "failed": failed,
            "success_rate": success_rate,
            "recent_tasks": recent_tasks
        }
    
    def get_system_health(self):
        health = {
            "status": "🟢 GOOD",
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "db_size_mb": round(os.path.getsize(self.db_path) / 1024 / 1024, 2) if os.path.exists(self.db_path) else 0
        }
        
        if health["cpu_percent"] > 80 or health["memory_percent"] > 80:
            health["status"] = "🟡 WARNING"
        if health["cpu_percent"] > 95 or health["memory_percent"] > 95:
            health["status"] = "🔴 CRITICAL"
        
        return health
    
    def display_dashboard(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "=" * 80)
        print(f"📊 SEN V3 SYSTEM DASHBOARD")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # 1. AFFILIATE STATS
        affiliate = self.get_affiliate_stats()
        print("\n🎯 1. AFFILIATE MARKETING")
        print("-" * 50)
        print(f"   📊 AccessTrade Campaigns: {affiliate['total_campaigns']}")
        print(f"   🎯 ACFC Promotions: {affiliate['active_acfc']}")
        print(f"   💰 Doanh thu: {affiliate['revenue']:,.0f} VND")
        print(f"   🎁 Hoa hồng: {affiliate['commission']:,.0f} VND")
        print(f"   👆 Clicks: {affiliate['clicks']:,}")
        print(f"   📦 Đơn hàng: {affiliate['orders']:,}")
        
        # 2. WORKER STATS
        worker = self.get_worker_stats()
        print("\n👷 2. WORKER SYSTEM")
        print("-" * 50)
        print(f"   🔄 Workers: {worker['total_workers']}")
        print(f"   📋 Tasks: {worker['total_tasks']} (✅ {worker['succeeded']} | ❌ {worker['failed']})")
        print(f"   📈 Success Rate: {worker['success_rate']}%")
        
        if worker['recent_tasks']:
            print("\n   📝 Recent Tasks:")
            for task in worker['recent_tasks']:
                icon = "✅" if task[1] == "completed" else "🔄" if task[1] == "processing" else "⏳"
                print(f"      {icon} {task[0]}: {task[1]} - {task[2][:16] if task[2] else 'N/A'}")
        
        # 3. SYSTEM HEALTH
        health = self.get_system_health()
        print("\n🖥️ 3. SYSTEM HEALTH")
        print("-" * 50)
        print(f"   🟢 Status: {health['status']}")
        print(f"   💻 CPU: {health['cpu_percent']}%")
        print(f"   🧠 Memory: {health['memory_percent']}%")
        print(f"   💾 Disk: {health['disk_usage']}%")
        print(f"   🗄️ DB Size: {health['db_size_mb']} MB")
        
        print("\n" + "=" * 80)
        print("🔄 Auto-refresh every 10 seconds... (Press Ctrl+C to stop)")
        print("=" * 80)

def run_dashboard():
    import time
    dashboard = SystemDashboard()
    try:
        while True:
            dashboard.display_dashboard()
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n✅ Dashboard stopped!")

if __name__ == "__main__":
    run_dashboard()
