import sqlite3
import pandas as pd

conn = sqlite3.connect('sen_v3.db')

# Xem lỗi Facebook cụ thể
print("🔍 LỖI FACEBOOK:")
fb_errors = pd.read_sql_query("""
    SELECT id, original_task_id, error_message, payload 
    FROM dead_letters 
    WHERE category LIKE '%facebook%' OR error_message LIKE '%Page%'
    LIMIT 5
""", conn)
print(fb_errors)

conn.close()
