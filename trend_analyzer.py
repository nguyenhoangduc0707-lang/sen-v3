"""
Trend Analyzer - Phát hiện sản phẩm hot để quảng bá
"""
import sqlite3
import requests
from datetime import datetime, timedelta

class TrendAnalyzer:
    def __init__(self):
        self.db_path = "sen_v3.db"
        self._init_db()
    
    def _init_db(self):
        """Khởi tạo bảng trending products"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trending_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                product_name TEXT,
                growth_rate REAL,
                video_count INTEGER,
                engagement REAL,
                status TEXT DEFAULT 'pending',
                detected_at TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def fetch_trending_topics(self):
        """Lấy xu hướng từ TikTok (mock data)"""
        # TODO: Thay bằng API thật
        mock_trends = [
            {"keyword": "mua sam tet", "product": "Đồ gia dụng", "growth": 45.5, "videos": 15000},
            {"keyword": "laptop gaming", "product": "Laptop", "growth": 32.0, "videos": 8000},
            {"keyword": "son mat", "product": "Mỹ phẩm", "growth": 28.3, "videos": 12000},
            {"keyword": "dien thoai", "product": "Điện thoại", "growth": 25.0, "videos": 25000},
            {"keyword": "the tin dung", "product": "Thẻ tín dụng", "growth": 20.5, "videos": 5000}
        ]
        return mock_trends
    
    def analyze_and_save(self):
        """Phân tích và lưu sản phẩm tiềm năng"""
        trends = self.fetch_trending_topics()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for trend in trends:
            cursor.execute('''
                INSERT INTO trending_products 
                (keyword, product_name, growth_rate, video_count, status, detected_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                trend['keyword'],
                trend['product'],
                trend['growth'],
                trend['videos'],
                'active',
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Đã phân tích {len(trends)} xu hướng mới")
        return trends
    
    def get_top_trends(self, limit=5):
        """Lấy top xu hướng"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT keyword, product_name, growth_rate 
            FROM trending_products 
            WHERE status = 'active'
            ORDER BY growth_rate DESC
            LIMIT ?
        ''', (limit,))
        trends = cursor.fetchall()
        conn.close()
        return trends
    
    def recommend_campaign(self):
        """Đề xuất chiến dịch dựa trên xu hướng"""
        top = self.get_top_trends(1)
        if top:
            keyword, product, growth = top[0]
            print(f"🎯 ĐỀ XUẤT CHIẾN DỊCH:")
            print(f"   Sản phẩm: {product}")
            print(f"   Từ khóa: {keyword}")
            print(f"   Mức độ hot: {growth}%")
            print(f"   👉 Nên quảng bá link Shopee với sản phẩm này!")

if __name__ == "__main__":
    analyzer = TrendAnalyzer()
    analyzer.analyze_and_save()
    analyzer.recommend_campaign()
