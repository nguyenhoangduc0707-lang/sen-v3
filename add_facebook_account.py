import sqlite3
import os
from dotenv import load_dotenv, set_key

load_dotenv()

def add_facebook_account():
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    print("🔑 THÊM TÀI KHOẢN FACEBOOK")
    print("="*40)
    
    # Lấy token từ .env hoặc nhập thủ công
    token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    page_id = os.getenv('FACEBOOK_PAGE_ID')
    
    if not token or not page_id:
        print("⚠️ Chưa có token trong .env. Nhập thủ công:")
        token = input("Facebook Access Token: ").strip()
        page_id = input("Facebook Page ID: ").strip()
        
        # Lưu vào .env
        set_key('.env', 'FACEBOOK_ACCESS_TOKEN', token)
        set_key('.env', 'FACEBOOK_PAGE_ID', page_id)
    
    # Kiểm tra đã có account chưa
    cursor.execute("SELECT COUNT(*) FROM facebook_accounts")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"⚠️ Đã có {count} tài khoản trong database")
        update = input("Cập nhật tài khoản hiện có? (y/n): ")
        if update.lower() == 'y':
            cursor.execute("""
                UPDATE facebook_accounts 
                SET page_id = ?, 
                    access_token_encrypted = ?,
                    is_active = 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
            """, (page_id, token))
            print("✅ Đã cập nhật tài khoản")
    else:
        # Thêm mới
        cursor.execute("""
            INSERT INTO facebook_accounts 
            (page_id, page_name, access_token_encrypted, is_active, created_at, updated_at)
            VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (page_id, "Facebook Page", token))
        print("✅ Đã thêm tài khoản mới")
    
    conn.commit()
    conn.close()
    print("\n✅ Hoàn tất!")

if __name__ == "__main__":
    add_facebook_account()
