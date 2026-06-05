"""
Real-time Monitor for Auto Worker
Theo dõi tiến trình chạy workers
"""
import json
import time
import os
from datetime import datetime
import threading

class RealTimeMonitor:
    def __init__(self):
        self.stats_file = "worker_stats.json"
        self.running = True
    
    def get_worker_stats(self):
        """Lấy thống kê từ worker"""
        try:
            with open('auto_worker_report.json', 'r') as f:
                return json.load(f)
        except:
            return None
    
    def get_strategy_info(self):
        """Lấy thông tin chiến lược"""
        try:
            with open('auto_strategy.json', 'r') as f:
                return json.load(f)
        except:
            return None
    
    def get_database_stats(self):
        """Lấy thống kê từ database"""
        import sqlite3
        try:
            conn = sqlite3.connect('sen_v3.db')
            cursor = conn.cursor()
            
            # Số campaigns
            cursor.execute("SELECT COUNT(*) FROM accesstrade_campaigns")
            campaigns = cursor.fetchone()[0]
            
            # Số ACFC promotions
            cursor.execute("SELECT COUNT(*) FROM acfc_promotions WHERE status = 'active'")
            acfc = cursor.fetchone()[0]
            
            # Số tasks đã xử lý
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
            completed = cursor.fetchone()[0]
            
            conn.close()
            return {
                'campaigns': campaigns,
                'acfc': acfc,
                'completed_tasks': completed
            }
        except:
            return {'campaigns': 0, 'acfc': 0, 'completed_tasks': 0}
    
    def display_dashboard(self):
        """Hiển thị dashboard real-time"""
        while self.running:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("=" * 80)
            print(f"📊 SEN V3 - REAL-TIME WORKER MONITOR")
            print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 80)
            
            # Worker stats
            worker_stats = self.get_worker_stats()
            if worker_stats:
                print("\n🤖 WORKER STATUS:")
                print(f"   📊 Target: {worker_stats.get('target', 0):,} tasks/day")
                print(f"   ✅ Processed: {worker_stats.get('processed', 0):,}")
                print(f"   📈 Succeeded: {worker_stats.get('succeeded', 0):,}")
                print(f"   ❌ Failed: {worker_stats.get('failed', 0):,}")
                
                if worker_stats.get('processed', 0) > 0:
                    success_rate = worker_stats['succeeded'] / worker_stats['processed'] * 100
                    print(f"   📊 Success Rate: {success_rate:.1f}%")
                
                if worker_stats.get('time_taken_minutes', 0) > 0:
                    print(f"   ⏱️ Time taken: {worker_stats['time_taken_minutes']:.1f} minutes")
            
            # Strategy info
            strategy = self.get_strategy_info()
            if strategy:
                analysis = strategy.get('analysis', {})
                print("\n🎯 STRATEGY INFO:")
                print(f"   💰 High Value: {analysis.get('high_value_count', 0)}")
                print(f"   📦 High Volume: {analysis.get('high_volume_count', 0)}")
                print(f"   📈 New Trend: {analysis.get('new_trend_count', 0)}")
                print(f"   📋 Total Tasks: {strategy.get('total_tasks', 0)}")
            
            # Database stats
            db_stats = self.get_database_stats()
            print("\n💾 DATABASE STATS:")
            print(f"   📊 AccessTrade Campaigns: {db_stats.get('campaigns', 0)}")
            print(f"   🎯 ACFC Promotions: {db_stats.get('acfc', 0)}")
            print(f"   ✅ Completed Tasks: {db_stats.get('completed_tasks', 0)}")
            
            # Progress bar
            if worker_stats and worker_stats.get('target', 0) > 0:
                processed = worker_stats.get('processed', 0)
                target = worker_stats.get('target', 1)
                percent = min(100, int(processed / target * 100))
                bar = "█" * (percent // 2) + "░" * (50 - percent // 2)
                print(f"\n📈 PROGRESS: [{bar}] {percent}% ({processed}/{target})")
            
            # Tips
            print("\n" + "=" * 80)
            print("💡 TIPS:")
            print("   • Press Ctrl+C to stop monitor")
            print("   • Run 'python auto_worker.py' to start worker")
            print("   • Check successful_links.json for working links")
            print("=" * 80)
            
            time.sleep(3)
    
    def stop(self):
        self.running = False

def main():
    monitor = RealTimeMonitor()
    try:
        monitor.display_dashboard()
    except KeyboardInterrupt:
        print("\n✅ Monitor stopped!")
        monitor.stop()

if __name__ == "__main__":
    main()
