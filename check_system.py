import os
import sys
import importlib
import sqlite3
from datetime import datetime

print("🔍 KIỂM TRA HỆ THỐNG DỰ ÁN")
print("="*60)
print(f"🕐 Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 1. Kiểm tra Python
print("1️⃣ PYTHON ENVIRONMENT")
print(f"   Python: {sys.version[:10]}")
print(f"   Path: {sys.executable}")
print()

# 2. Kiểm tra thư viện
print("2️⃣ THƯ VIỆN CÀI ĐẶT")
libraries = {
    'pandas': 'Xử lý dữ liệu',
    'openpyxl': 'Đọc/ghi Excel',
    'google.generativeai': 'Gemini API',
    'sqlalchemy': 'ORM Database',
    'fastapi': 'Web API',
    'uvicorn': 'Web Server'
}
for lib, desc in libraries.items():
    try:
        importlib.import_module(lib.replace('.', '_'))
        print(f"   ✅ {lib}: {desc}")
    except ImportError:
        print(f"   ❌ {lib}: {desc} - CHƯA CÀI")
print()

# 3. Kiểm tra file cấu hình
print("3️⃣ FILE CẤU HÌNH")
files = ['.env', 'requirements.txt', 'docker-compose.yml']
for file in files:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"   ✅ {file}: {size} bytes")
    else:
        print(f"   ❌ {file}: KHÔNG TÌM THẤY")
print()

# 4. Kiểm tra database
print("4️⃣ CƠ SỞ DỮ LIỆU")
databases = ['app.db', 'sen_v3.db']
for db in databases:
    if os.path.exists(db):
        size = os.path.getsize(db) / 1024
        print(f"   ✅ {db}: {size:.1f} KB")
        try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"      Bảng: {len(tables)} bảng")
            conn.close()
        except:
            print(f"      ⚠️ Không thể đọc")
    else:
        print(f"   ❌ {db}: KHÔNG TÌM THẤY")
print()

# 5. Kiểm tra dữ liệu AccessTrade
print("5️⃣ DỮ LIỆU ACCESSTRADE")
excel_files = [f for f in os.listdir('.') if f.startswith('accesstrade_report_') and f.endswith('.xlsx')]
if excel_files:
    for f in excel_files:
        size = os.path.getsize(f) / 1024
        print(f"   ✅ {f}: {size:.1f} KB")
else:
    print("   ⚠️ Không có file Excel AccessTrade")
print()

# 6. Kiểm tra biến môi trường
print("6️⃣ BIẾN MÔI TRƯỜNG (.env)")
env_vars = ['GEMINI_API_KEY', 'ACCESS_TRADE_API_KEY', 'DATABASE_URL']
for var in env_vars:
    value = os.getenv(var)
    if value:
        masked = value[:5] + '*'*5 if len(value) > 10 else '***'
        print(f"   ✅ {var}: {masked}")
    else:
        print(f"   ❌ {var}: CHƯA SET")
print()

print("="*60)
print("✅ KIỂM TRA HOÀN TẤT!")
