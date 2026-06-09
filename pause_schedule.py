import requests

resp = requests.post('http://localhost:8001/auth/login', 
                     json={'email': 'admin@senv3.com', 'password': 'Admin123'})
token = resp.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

resp = requests.post('http://localhost:8001/schedules/1/pause', headers=headers)
if resp.status_code == 200:
    print('✅ Schedule đã được tạm dừng')
else:
    print(f'❌ Lỗi: {resp.status_code}')
