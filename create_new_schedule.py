import requests
from datetime import datetime, timedelta

resp = requests.post('http://localhost:8001/auth/login', 
                     json={'email': 'admin@senv3.com', 'password': 'Admin123'})
token = resp.json()['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

schedule_data = {
    'task_type': 'facebook',
    'data': {
        'content': 'Bài đăng mới lúc ' + datetime.now().strftime('%H:%M:%S'),
        'fanpage_key': 'default'
    },
    'scheduled_at': (datetime.now() + timedelta(minutes=10)).isoformat(),
    'priority': 1
}

resp = requests.post('http://localhost:8001/schedules/', json=schedule_data, headers=headers)
if resp.status_code in [200, 201]:
    print(f'✅ Schedule mới đã được tạo! ID: {resp.json()["id"]}')
    print(f'   Thời gian: {resp.json()["scheduled_at"]}')
else:
    print(f'❌ Lỗi: {resp.text}')
