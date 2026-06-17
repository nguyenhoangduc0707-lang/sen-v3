"""
Multi-Platform Analytics Dashboard
"""
import sqlite3
import json
from datetime import datetime, timedelta

class UnifiedAnalytics:
    def __init__(self):
        self.db_path = "sen_v3.db"
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_date DATE,
                tiktok_views INTEGER DEFAULT 0,
                tiktok_likes INTEGER DEFAULT 0,
                tiktok_shares INTEGER DEFAULT 0,
                facebook_clicks INTEGER DEFAULT 0,
                facebook_reach INTEGER DEFAULT 0,
                telegram_clicks INTEGER DEFAULT 0,
                total_sales REAL DEFAULT 0,
                total_commission REAL DEFAULT 0,
                created_at TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def get_tiktok_stats(self):
        """Lấy thống kê từ TikTok (mock)"""
        # TODO: Thay bằng API thật
        return {
            "views": 15000,
            "likes": 3200,
            "shares": 850,
            "comments": 420
        }
    
    def get_facebook_stats(self):
        """Lấy thống kê từ Facebook"""
        try:
            import requests
            from dotenv import load_dotenv
            import os
            load_dotenv()
            
            token = os.getenv("FACEBOOK_ACCESS_TOKEN")
            page_id = os.getenv("FACEBOOK_PAGE_ID")
            
            url = f"https://graph.facebook.com/v21.0/{page_id}/insights?metric=page_impressions,page_posts_impressions&access_token={token}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return {"reach": data.get('data', [{}])[0].get('values', [{}])[0].get('value', 0)}
        except:
            pass
        return {"reach": 0}
    
    def get_accesstrade_stats(self):
        """Lấy doanh số từ AccessTrade"""
        # Lấy từ database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(revenue), SUM(commission) FROM sales_tracking WHERE date >= date('now', '-7 days')")
        revenue, commission = cursor.fetchone()
        conn.close()
        return {"revenue": revenue or 0, "commission": commission or 0}
    
    def generate_report(self):
        """Tạo báo cáo tổng hợp"""
        tiktok = self.get_tiktok_stats()
        facebook = self.get_facebook_stats()
        accesstrade = self.get_accesstrade_stats()
        
        report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tiktok": tiktok,
            "facebook": facebook,
            "accesstrade": accesstrade,
            "total": {
                "views": tiktok.get("views", 0) + facebook.get("reach", 0),
                "revenue": accesstrade.get("revenue", 0),
                "commission": accesstrade.get("commission", 0)
            }
        }
        
        # Lưu vào database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO daily_reports 
            (report_date, tiktok_views, tiktok_likes, tiktok_shares,
             facebook_reach, total_sales, total_commission)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            report['date'],
            report['tiktok']['views'],
            report['tiktok']['likes'],
            report['tiktok']['shares'],
            report['facebook']['reach'],
            report['accesstrade']['revenue'],
            report['accesstrade']['commission']
        ))
        conn.commit()
        conn.close()
        
        return report

if __name__ == "__main__":
    analytics = UnifiedAnalytics()
    report = analytics.generate_report()
    
    print("=" * 50)
    print("📊 BÁO CÁO TỔNG HỢP")
    print("=" * 50)
    print(json.dumps(report, indent=2, ensure_ascii=False))
