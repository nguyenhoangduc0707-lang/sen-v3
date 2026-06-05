import os
import sqlite3
import requests
from dotenv import load_database, load_dotenv

load_dotenv()

def check_env_variables():
    print("1. [CHECK] Biến môi trường...")
    required_keys = ["GEMINI_API_KEY", "DB_PATH"]
    all_pass = True
    for key in required_keys:
        if not os.getenv(key):
            print(f"❌ Thiếu biến môi trường: {key}")
            all_pass = False
        else:
            print(f"✅ {key}: Đã cấu hình")
    return all_pass

def check_database():
    print("\n2. [CHECK] Cơ sở dữ liệu (SQLite)...")
    db_path = os.getenv("DB_PATH", "sen_v3.db")
    if not os.path.exists(db_path):
        print(f"❌ Không tìm thấy file DB tại: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Kiểm tra nhanh số lượng task theo trạng thái
        cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
        rows = cursor.fetchall()
        print("📊 Trạng thái hàng đợi hiện tại:")
        if not rows:
            print("   (Hàng đợi đang trống)")
        for row in rows:
            print(f"   - {row[0]}: {row[1]} tasks")
        conn.close()
        print("✅ Kết nối Database hoạt động tốt.")
        return True
    except Exception as e:
        print(f"❌ Lỗi kết nối DB: {e}")
        return False

def check_gemini_api():
    print("\n3. [CHECK] Kết nối Gemini API...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return False
    
    # Gọi thử nghiệm một request siêu nhỏ để test API Key
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts":[{"text": "ping"}]}]}
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ Kết nối Gemini API: Thành công!")
            return True
        else:
            print(f"❌ Lỗi Gemini API (Status {response.status_code}): {response.text}")
            return False
    except Exception as e:
        print(f"❌ Không thể kết nối tới Gemini Server: {e}")
        return False

if __name__ == "__main__":
    print("=== BẮT ĐẦU KIỂM TRA SỨC KHỎE HỆ THỐNG ===")
    env_ok = check_env_variables()
    db_ok = check_database()
    api_ok = check_gemini_api()
    
    print("\n=== KẾT LUẬN ===")
    if env_ok and db_ok and api_ok:
        print("🚀 Hệ thống KHỎE MẠNH! Sẵn sàng chạy chiến dịch.")
    else:
        print("⚠️ Hệ thống có lỗi tiềm ẩn. Vui lòng kiểm tra lại các mục báo đỏ (❌).")