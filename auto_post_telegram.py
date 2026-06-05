from config_global import config
"""
Auto Post Telegram - Gửi tin nhắn tự động lên Telegram
"""
import requests
import json
import time
from datetime import datetime

class TelegramAutoPost:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    def send_message(self, message):
        """Gửi tin nhắn đến Telegram"""
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(self.api_url, data=data)
            if response.status_code == 200:
                return True
            else:
                print(f"❌ Lỗi: {response.json()}")
                return False
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False
    
    def auto_post_all(self, posts, delay_seconds=30):
        """Tự động gửi tất cả bài đăng"""
        print("=" * 60)
        print("🚀 AUTO POST TELEGRAM")
        print(f"📊 Tổng số bài: {len(posts)}")
        print("=" * 60)
        
        for i, post in enumerate(posts, 1):
            message = f"<b>📌 BÀI {i}: {post['name']}</b>\n\n"
            message += f"{post['content']}\n\n"
            message += f"🔗 <a href='{post['link']}'>Đăng ký ngay</a>"
            
            print(f"\n📝 Đang gửi bài {i}: {post['name']}")
            
            if self.send_message(message):
                print(f"   ✅ Đã gửi bài {i}")
            else:
                print(f"   ❌ Gửi thất bại")
            
            if i < len(posts):
                time.sleep(delay_seconds)
        
        print("\n✅ HOÀN TẤT!")

# Hướng dẫn tạo bot
print("=" * 70)
print("🤖 HƯỚNG DẪN TẠO TELEGRAM BOT:")
print("=" * 70)
print("""
1. Tìm @BotFather trên Telegram
2. Gửi /newbot -> Đặt tên bot
3. Copy bot token (dạng: 123456:ABC-DEF)
4. Tạo group hoặc channel, thêm bot vào
5. Lấy chat_id (gửi tin nhắn, xem log)
""")
print("=" * 70)

if __name__ == "__main__":
    # Điền thông tin bot của bạn
    BOT_TOKEN = config.TELEGRAM_BOT_TOKEN  # Thay bằng token thật
    CHAT_ID = "YOUR_CHAT_ID_HERE"      # Thay bằng chat_id thật
    
    if BOT_TOKEN != "YOUR_BOT_TOKEN_HERE":
        with open('bulk_posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
        
        bot = TelegramAutoPost(BOT_TOKEN, CHAT_ID)
        bot.auto_post_all(posts, delay_seconds=30)
    else:
        print("⚠️ Cần cấu hình BOT_TOKEN và CHAT_ID trước!")


