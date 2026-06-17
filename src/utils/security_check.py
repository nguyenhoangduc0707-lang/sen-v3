# security_check.py
import os
import re
from pathlib import Path

print("=" * 50)
print("KIỂM TRA BẢO MẬT DỰ ÁN")
print("=" * 50)

# Kiểm tra file .env
if Path(".env").exists():
    print("⚠️ File .env tồn tại - CẨN THẬN không commit lên GitHub!")
    
    # Đọc nội dung .env với encoding phù hợp
    try:
        with open(".env", "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(".env", "r", encoding="latin-1") as f:
                content = f.read()
        except:
            with open(".env", "r", encoding="cp1252") as f:
                content = f.read()
    
    # Kiểm tra xem có API key thật không (bỏ qua các dòng comment)
    has_real_keys = False
    for line in content.split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            if "=" in line and not any(x in line.lower() for x in ["your_", "example", "demo", "test", "xxx"]):
                if len(line.split("=")[1].strip()) > 5:  # Giá trị không quá ngắn
                    has_real_keys = True
                    print(f"🔴 Phát hiện: {line.split('=')[0]} đã được cấu hình")
    
    if has_real_keys:
        print("\n🔴 CẢNH BÁO: Phát hiện API keys thật trong file .env!")
        print("   → Đảm bảo .env đã được thêm vào .gitignore")
    else:
        print("✅ Các API keys đang dùng giá trị mẫu (an toàn)")

# Kiểm tra .gitignore
if Path(".gitignore").exists():
    with open(".gitignore", "r") as f:
        content = f.read()
    
    if ".env" in content:
        print("✅ .env đã được thêm vào .gitignore")
    else:
        print("🔴 CẢNH BÁO: .env CHƯA được thêm vào .gitignore!")
        print("   → Thêm dòng '.env' vào file .gitignore")
else:
    print("🔴 Không tìm thấy file .gitignore")

# Kiểm tra file backup
backup_files = list(Path(".").glob(".env.backup_*"))
if backup_files:
    print(f"\n⚠️ Phát hiện {len(backup_files)} file backup của .env:")
    for bf in backup_files:
        print(f"   → {bf.name}")
    print("   → Nên xóa các file này để tránh rò rỉ thông tin")

print("\n✅ Đã kiểm tra xong!")