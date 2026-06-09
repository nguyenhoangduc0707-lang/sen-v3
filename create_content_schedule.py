import requests
from datetime import datetime, timedelta

resp = requests.post('http://localhost:8001/auth/login', json={
    'email': 'nguyenhoangduc0707@gmail.com',
    'password': '0325655987Duc@@'
})
token = resp.json()['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

# Tạo schedule mới
schedule = {
    "task_type": "content",
    "data": {
        "prompt": "Viết bài về lợi ích của AI trong marketing",
        "model": "gemini"
    },
    "scheduled_at": (datetime.now() + timedelta(minutes=30)).isoformat(),
    "priority": 1
}

resp = requests.post('http://localhost:8001/schedules/', json=schedule, headers=headers)
print(f'Create schedule: {resp.status_code}')
if resp.status_code in [200, 201]:
    print(f'✅ Schedule created: {resp.json()}')
