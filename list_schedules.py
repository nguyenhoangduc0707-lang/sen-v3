import requests

# Login
resp = requests.post('http://localhost:8001/auth/login', json={
    'email': 'nguyenhoangduc0707@gmail.com',
    'password': '0325655987Duc@@'
})
token = resp.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Get schedules
resp = requests.get('http://localhost:8001/schedules/', headers=headers)
print('📋 Schedules:')
for s in resp.json():
    print(f"   ID: {s['id']}, Type: {s['task_type']}, Active: {s['is_active']}, Time: {s['scheduled_at']}")
