"""
Xem nội dung bài đăng đã tạo
"""
import json

with open('bulk_posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

print("=" * 80)
print(f"📢 DANH SÁCH {len(posts)} BÀI ĐĂNG ĐÃ TẠO")
print("=" * 80)

for i, post in enumerate(posts, 1):
    print(f"\n📌 BÀI #{i}: {post['name']}")
    print("-" * 60)
    print(f"{post['content']}")
    print("-" * 60)
    print(f"🔗 Link: {post['link']}")
    print()

# Lưu vào file dễ đọc
with open('posts_display.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("📢 BÀI ĐĂNG MẠNG XÃ HỘI\n")
    f.write("=" * 80 + "\n\n")
    
    for i, post in enumerate(posts, 1):
        f.write(f"\n📌 BÀI ĐĂNG #{i}: {post['name']}\n")
        f.write("-" * 60 + "\n")
        f.write(f"{post['content']}\n")
        f.write("-" * 60 + "\n")
        f.write(f"🔗 Link: {post['link']}\n\n")

print("\n" + "=" * 80)
print("✅ Đã lưu vào file: posts_display.txt")
print("📁 Mở file để copy bài đăng: notepad posts_display.txt")
print("=" * 80)
