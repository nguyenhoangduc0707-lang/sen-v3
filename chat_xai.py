from xai_sdk import Client
from xai_sdk.chat import user, system

# Dán trực tiếp khóa thật vào đây để loại trừ lỗi biến môi trường
client = Client(
    api_key="xai-YOUR_ACTUAL_API_KEY_HERE",
    management_api_key="xai-YOUR_ACTUAL_MANAGEMENT_KEY_HERE",
    timeout=3600
)

chat = client.chat.create(model="grok-4.3")
chat.append(user("Hello, are you working?"))
response = chat.sample()
print(response)