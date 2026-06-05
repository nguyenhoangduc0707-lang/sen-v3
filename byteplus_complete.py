"""
Complete BytePlus Integration - Tất cả tính năng 1-4
"""
import time
import threading
from datetime import datetime

class CompleteBytePlusSystem:
    def __init__(self):
        self.running = True
    
    def run_tiktok_auto_post(self):
        """Chạy auto post TikTok"""
        from tiktok_auto_post import TikTokAutoPost
        bot = TikTokAutoPost()
        bot.auto_post_all()
    
    def run_trend_analyzer(self):
        """Chạy phân tích xu hướng"""
        from trend_analyzer import TrendAnalyzer
        analyzer = TrendAnalyzer()
        while self.running:
            analyzer.analyze_and_save()
            analyzer.recommend_campaign()
            time.sleep(3600)  # Mỗi giờ
    
    def run_analytics_dashboard(self):
        """Chạy dashboard báo cáo"""
        from analytics_dashboard import UnifiedAnalytics
        analytics = UnifiedAnalytics()
        while self.running:
            report = analytics.generate_report()
            print(f"📊 [{datetime.now()}] Báo cáo mới: {report['total']['revenue']} VND")
            time.sleep(86400)  # Mỗi ngày
    
    def run_all(self):
        """Chạy tất cả tính năng"""
        print("=" * 60)
        print("🚀 KHỞI ĐỘNG HỆ THỐNG BYTEPLUS")
        print("=" * 60)
        
        # Chạy các thread
        threads = [
            threading.Thread(target=self.run_tiktok_auto_post),
            threading.Thread(target=self.run_trend_analyzer),
            threading.Thread(target=self.run_analytics_dashboard)
        ]
        
        for t in threads:
            t.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            print("\n✅ Đã dừng hệ thống")

if __name__ == "__main__":
    system = CompleteBytePlusSystem()
    system.run_all()
