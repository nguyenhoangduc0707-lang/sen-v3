"""
Complete Automation Scheduler
Chạy tự động hàng ngày: lấy link → đăng bài → báo cáo
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
        self.tasks = []
    
    def job_fetch_links(self):
        """Lấy link tự động"""
        logger.info("🔗 Fetching new affiliate links...")
        subprocess.run(["python", "auto_fetch_links.py"])
    
    def job_post_facebook(self):
        """Đăng bài lên Facebook"""
        logger.info("📘 Posting to Facebook...")
        subprocess.run(["python", "auto_facebook_post.py"])
    
    def job_post_telegram(self):
        """Đăng bài lên Telegram"""
        logger.info("📱 Posting to Telegram...")
        subprocess.run(["python", "auto_telegram_post.py"])
    
    def job_report(self):
        """Tạo báo cáo"""
        logger.info("📊 Generating daily report...")
        subprocess.run(["python", "sales_dashboard.py"])
    
    def setup_schedule(self):
        """Thiết lập lịch trình"""
        # Lấy link mới mỗi 6 giờ
        schedule.every(6).hours.do(self.job_fetch_links)
        
        # Đăng bài lên Facebook lúc 7h, 12h, 20h
        schedule.every().day.at("07:00").do(self.job_post_facebook)
        schedule.every().day.at("12:00").do(self.job_post_facebook)
        schedule.every().day.at("20:00").do(self.job_post_facebook)
        
        # Đăng bài lên Telegram mỗi 2 giờ
        schedule.every(2).hours.do(self.job_post_telegram)
        
        # Báo cáo cuối ngày
        schedule.every().day.at("23:00").do(self.job_report)
        
        logger.info("✅ Scheduler configured!")
    
    def run(self):
        """Chạy scheduler"""
        self.setup_schedule()
        logger.info("🚀 Auto Scheduler started!")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    scheduler = AutoScheduler()
    scheduler.run()
