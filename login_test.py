import requests

print("🔐 Dang nhap he thong...")
resp = requests.post('http://localhost:8001/auth/login', 
                     json={'email': 'admin@senv3.com', 'password': 'Admin123'})

print(f'Status code: {resp.status_code}')

if resp.status_code == 200:
    token = resp.json()['access_token']
    print('✅ Dang nhap thanh cong!')
    print(f'Token: {token[:50]}...')
    
    # Test schedules
    print('\n📋 Kiem tra schedules...')
    headers = {'Authorization': f'Bearer {token}'}
    schedules = requests.get('http://localhost:8001/schedules/', headers=headers)
    print(f'Schedules status: {schedules.status_code}')
    if schedules.status_code == 200:
        data = schedules.json()
        print(f'So luong schedules: {len(data)}')
        if data:
            print(f'Schedule dau tien: {data[0]}')
else:
    print('❌ Dang nhap that bai!')
    print(f'Chi tiet: {resp.text}')
