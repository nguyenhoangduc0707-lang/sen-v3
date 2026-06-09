import requests

login_data = {
    'email': 'admin@example.com',
    'password': 'admin123'
}

response = requests.post('http://localhost:8000/auth/login', json=login_data)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    token = response.json().get('access_token')
    print('✅ Login successful!')
    print(f'Token: {token[:50]}...')
    with open('token.txt', 'w') as f:
        f.write(token)
else:
    print(f'❌ Error: {response.text}')
