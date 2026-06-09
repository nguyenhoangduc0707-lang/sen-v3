import requests

# Đăng nhập lấy token
login_resp = requests.post('http://localhost:8001/auth/login', json={
    'email': 'nguyenhoangduc0707@gmail.com',
    'password': '0325655987Duc@@'
})

if login_resp.status_code != 200:
    print(f'❌ Login failed: {login_resp.text}')
    exit()

TOKEN = login_resp.json()['access_token']
print(f'✅ Logged in, token: {TOKEN[:50]}...')

headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Tạo schedule
schedule = {
    "task_type": "facebook",
    "data": {
        "content": "Bài đăng test từ API schedule",
        "fanpage_key": "default"
    },
    "scheduled_at": "2026-06-10T09:00:00",
    "priority": 1
}

resp = requests.post("http://localhost:8001/schedules/", json=schedule, headers=headers)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    print(f"✅ Schedule created: {resp.json()}")
else:
    print(f"❌ Error: {resp.text}")
