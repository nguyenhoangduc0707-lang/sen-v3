"""
Auto post to Telegram using Bot API
"""
import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

class TelegramAutoPost:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
    
    def send_message(self, message):
        """Gửi tin nhắn tự động"""
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(self.api_url, data=data)
            if response.status_code == 200:
                print("✅ Message sent to Telegram")
                return True
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def auto_post_all(self, posts, delay=60):
        """Tự động gửi tất cả bài"""
        print(f"🚀 Sending {len(posts)} messages to Telegram...")
        
        for i, post in enumerate(posts, 1):
            message = f"<b>📢 BÀI {i}</b>\n\n{post['content']}\n\n🔗 <a href='{post['link']}'>Xem ngay</a>"
            self.send_message(message)
            
            if i < len(posts):
                time.sleep(delay)
        
        print("✅ All messages sent!")

def create_posts():
    posts = [
        {
            'content': '🛍️ SHOPEE SALE GIỮA THÁNG - GIẢM ĐẾN 70%\n\n🔥 Voucher Xtra giảm đến 5 triệu đồng\n🔥 Freeship 0Đ',
            'link': 'https://go.isclix.com/deep_link/v6/6983938396644077046/4751584435713464237?sub4=auto'
        },
        {
            'content': '💰 VPBank - Vay tín chấp lên đến 500 triệu\n✅ Lãi suất từ 0.8%/tháng\n✅ Giải ngân trong 24h',
            'link': 'https://go.isclix.com/deep_link/v5/6983938396644077046/6822308958202075636?sub4=auto'
        }
    ]
    return posts

if __name__ == "__main__":
    bot = TelegramAutoPost()
    posts = create_posts()
    bot.auto_post_all(posts)
