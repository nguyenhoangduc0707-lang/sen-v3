import requests

resp = requests.post('http://localhost:8001/auth/login', 
                     json={'email': 'admin@senv3.com', 'password': 'Admin123'})
token = resp.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

resp = requests.get('http://localhost:8001/schedules/1', headers=headers)
if resp.status_code == 200:
    s = resp.json()
    print('📋 Chi tiết schedule:')
    print(f'   ID: {s["id"]}')
    print(f'   Task type: {s["task_type"]}')
    print(f'   Data: {s["data"]}')
    print(f'   Scheduled at: {s["scheduled_at"]}')
    print(f'   Is active: {s["is_active"]}')
    print(f'   Is processed: {s["is_processed"]}')
    print(f'   Priority: {s["priority"]}')
else:
    print(f'❌ Lỗi: {resp.status_code}')
