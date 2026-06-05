import schedule
import time
import subprocess
import datetime

def post_to_facebook():
    print(f"\n[{datetime.datetime.now()}] Bắt đầu đăng bài...")
    # Gọi script đăng bài
    subprocess.run(["python", "fb_auto_click.py"])
    print(f"[{datetime.datetime.now()}] Đã đăng bài xong!")

# Lên lịch đăng bài
# Ví dụ: đăng bài lúc 8:00, 12:00, 18:00 hàng ngày
schedule.every().day.at("08:00").do(post_to_facebook)
schedule.every().day.at("12:00").do(post_to_facebook)
schedule.every().day.at("18:00").do(post_to_facebook)

print("🤖 SCHEDULER FACEBOOK POSTER")
print("Lịch đăng bài: 8:00, 12:00, 18:00 hàng ngày")
print("Nhấn Ctrl+C để dừng")

while True:
    schedule.run_pending()
    time.sleep(60)
