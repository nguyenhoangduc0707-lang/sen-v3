"""
Auto Scheduler - Chỉ chạy các worker không bao gồm Facebook
"""
import schedule
import time
import subprocess
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutoScheduler:
    def __init__(self):
        self.running = True
    
    def job_trend_analyzer(self):
        """Chạy phân tích xu hướng"""
        logger.info("📊 Running trend analyzer...")
        subprocess.run(["python", "trend_analyzer.py"])
    
    def job_analytics_dashboard(self):
        """Cập nhật dashboard"""
        logger.info("📈 Updating analytics dashboard...")
        subprocess.run(["python", "analytics_dashboard.py"])
    
    def job_system_dashboard(self):
        """Cập nhật hệ thống dashboard"""
        logger.info("🖥️ Updating system dashboard...")
        subprocess.run(["python", "system_dashboard.py"])
    
    def setup_schedule(self):
        """Thiết lập lịch trình"""
        # Trend analyzer mỗi 2 giờ
        schedule.every(2).hours.do(self.job_trend_analyzer)
        
        # Analytics dashboard mỗi 4 giờ
        schedule.every(4).hours.do(self.job_analytics_dashboard)
        
        # System dashboard mỗi 6 giờ
        schedule.every(6).hours.do(self.job_system_dashboard)
        
        logger.info("✅ Scheduler configured (Facebook excluded)")
    
    def run(self):
        """Chạy scheduler"""
        self.setup_schedule()
        logger.info("🚀 Auto Scheduler started (no Facebook)")
        
        while self.running:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    scheduler = AutoScheduler()
    try:
        scheduler.run()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped")
