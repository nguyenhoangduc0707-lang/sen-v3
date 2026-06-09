import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Xem các bài đăng lúc 16:00
cursor.execute('''
    SELECT id, title, scheduled_at 
    FROM tasks 
    WHERE status='SCHEDULED' 
    AND time(scheduled_at) = '16:00:00'
    LIMIT 10
''')
posts = cursor.fetchall()
print(f'📋 Found {len(posts)} posts at 16:00 (showing first 10)')
for post in posts[:5]:
    print(f'   #{post[0]}: {post[1][:30]}')

# Gợi ý: Xóa bớt bài cũ và tạo lại với giờ đa dạng
response = input('\n✨ Do you want to clean old posts and create new balanced schedule? (y/n): ')
if response.lower() == 'y':
    # Xóa các bài cũ
    cursor.execute('DELETE FROM tasks WHERE id < 50 AND status="SCHEDULED"')
    print(f'✅ Deleted {cursor.rowcount} old posts')
    conn.commit()
    print('\n📅 Run: python google_sheets_integration.py --once')
    print('   Then check new distribution with: python quick_stats.py')
else:
    print('✅ Keeping current schedule')

conn.close()
