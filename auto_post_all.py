"""
AUTO POST ALL PLATFORMS - Chạy 1 lần đăng tất cả
"""
import json
import webbrowser
import time
import subprocess

def auto_post_all():
    print("=" * 70)
    print("🚀 AUTO POST - TẤT CẢ NỀN TẢNG")
    print("=" * 70)
    
    # 1. Tải bài đăng
    with open('bulk_posts.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    print(f"📋 Đã tải {len(posts)} bài đăng")
    
    # 2. Mở Facebook và Zalo
    print("\n🔗 Mở Facebook và Zalo...")
    webbrowser.open("https://www.facebook.com")
    webbrowser.open("https://chat.zalo.me")
    time.sleep(3)
    
    # 3. Hướng dẫn đăng từng bài
    print("\n" + "=" * 70)
    print("📝 BẮT ĐẦU ĐĂNG BÀI (Copy & Paste)")
    print("=" * 70)
    
    # Cài đặt pyperclip nếu chưa có
    try:
        import pyperclip
    except:
        subprocess.run(["pip", "install", "pyperclip"])
        import pyperclip
    
    for i, post in enumerate(posts[:20], 1):  # 20 bài đầu
        print(f"\n{'='*60}")
        print(f"📌 BÀI {i}/{min(20, len(posts))}: {post['name']}")
        print(f"{'='*60}")
        print(f"\n{post['content']}\n")
        print(f"🔗 Link: {post['link']}")
        print(f"{'='*60}")
        
        # Copy nội dung
        full_text = f"{post['content']}\n\n{post['link']}"
        pyperclip.copy(full_text)
        print("✅ Đã copy nội dung vào clipboard!")
        
        choice = input("👉 Đã đăng xong? (Enter để tiếp / 's' để skip / 'q' để dừng): ")
        if choice.lower() == 'q':
            break
        elif choice.lower() == 's':
            continue
    
    print("\n" + "=" * 70)
    print("✅ HOÀN TẤT! Đã đăng bài thành công!")
    print("=" * 70)

if __name__ == "__main__":
    auto_post_all()
