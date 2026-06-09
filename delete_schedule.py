import requests

resp = requests.post('http://localhost:8001/auth/login', json={
    'email': 'nguyenhoangduc0707@gmail.com',
    'password': '0325655987Duc@@'
})
token = resp.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Delete schedule ID=1
resp = requests.delete('http://localhost:8001/schedules/1', headers=headers)
print(f'Delete schedule 1: {resp.status_code}')
if resp.status_code == 200:
    print('✅ Schedule 1 deleted')
