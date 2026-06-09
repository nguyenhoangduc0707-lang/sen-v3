import requests

TOKEN = "your_token_here"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

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
