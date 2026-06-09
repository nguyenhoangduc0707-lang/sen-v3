import requests
from datetime import datetime, timedelta

# Login lấy token
resp = requests.post('http://localhost:8001/auth/login', 
                     json={'email': 'admin@senv3.com', 'password': 'Admin123'})
token = resp.json()['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

# Tạo schedule
schedule_data = {
    'task_type': 'facebook',
    'data': {
        'content': 'Bài đăng test lúc ' + datetime.now().strftime('%H:%M:%S'),
        'fanpage_key': 'default'
    },
    'scheduled_at': (datetime.now() + timedelta(minutes=5)).isoformat(),
    'priority': 1
}

print('📝 Tạo schedule...')
resp = requests.post('http://localhost:8001/schedules/', json=schedule_data, headers=headers)
if resp.status_code in [200, 201]:
    print('✅ Schedule đã được tạo!')
    print(f'   ID: {resp.json()["id"]}')
    print(f'   Thời gian: {resp.json()["scheduled_at"]}')
else:
    print(f'❌ Lỗi: {resp.text}')
