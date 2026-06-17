from config_global import config
"""
Cấu hình Telegram Bot nhanh
"""
import json
import requests
import webbrowser

print("=" * 70)
print("🤖 CẤU HÌNH TELEGRAM BOT")
print("=" * 70)

# Nhập token
bot_token = input("\n🔑 Nhập Bot Token (từ @BotFather): ").strip()

if not bot_token:
    print("❌ Chưa nhập token!")
    exit()

# Kiểm tra token
test_url = f"https://api.telegram.org/bot{bot_token}/getMe"
try:
    response = requests.get(test_url)
    if response.status_code == 200:
        bot_info = response.json()
        print(f"✅ Token hợp lệ! Bot: @{bot_info['result']['username']}")
    else:
        print(f"❌ Token không hợp lệ! Lỗi: {response.status_code}")
        exit()
except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")
    exit()

# Lấy chat_id
print("\n💬 Đang lấy Chat ID...")
print("👉 Hãy gửi tin nhắn bất kỳ đến bot vừa tạo!")

# Mở chat với bot
webbrowser.open(f"https://t.me/{bot_info['result']['username']}")
input("\n✅ Sau khi gửi tin nhắn đến bot, nhấn Enter để lấy Chat ID...")

# Lấy updates
updates_url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
try:
    response = requests.get(updates_url)
    updates = response.json()
    
    if updates.get('ok') and updates.get('result'):
        chat_id = updates['result'][-1]['message']['chat']['id']
        print(f"✅ Chat ID: {chat_id}")
        
        # Lưu cấu hình
        config = {
            "bot_token": bot_token,
            "chat_id": chat_id,
            "configured_at": __import__('datetime').datetime.now().isoformat()
        }
        
        with open('telegram_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Đã lưu cấu hình vào telegram_config.json")
        
        # Tạo file auto post đã cấu hình
        with open('auto_post_telegram_ready.py', 'w', encoding='utf-8') as f:
            f.write(f'''
import json
import requests
import time

# Bot đã được cấu hình sẵn
BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
CHAT_ID = {chat_id}

def send_messages():
    with open('bulk_posts.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    print("=" * 60)
    print(f"🚀 Đang gửi {{len(posts)}} bài đến Telegram...")
    print("=" * 60)
    
    for i, post in enumerate(posts, 1):
        message = f"<b>📌 BÀI {{i}}: {{post['name']}}</b>\\n\\n"
        message += f"{{post['content']}}\\n\\n"
        message += f"🔗 <a href='{{post['link']}}'>Đăng ký ngay</a>"
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {{"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}}
        
        try:
            r = requests.post(url, data=data)
            if r.status_code == 200:
                print(f"✅ {{i}}. {{post['name'][:40]}}...")
            else:
                print(f"❌ {{i}}. Lỗi: {{r.json()}}")
        except Exception as e:
            print(f"❌ {{i}}. Lỗi: {{e}}")
        
        time.sleep(2)
    
    print("\\n✅ HOÀN TẤT! Đã gửi {len(posts)} bài!")

if __name__ == "__main__":
    send_messages()
''')
        
        print("✅ Đã tạo file: auto_post_telegram_ready.py")
        print("\n🚀 CHẠY LỆNH: python auto_post_telegram_ready.py")
        
    else:
        print("❌ Chưa nhận được tin nhắn! Hãy gửi tin nhắn đến bot và thử lại.")
        
except Exception as e:
    print(f"❌ Lỗi: {e}")


