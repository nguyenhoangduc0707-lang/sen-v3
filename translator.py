import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Lấy API Key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ Chưa có GEMINI_API_KEY trong .env")
    exit(1)

# Khởi tạo client
client = genai.Client(api_key=api_key)

print("🌐 DỊCH VĂN BẢN (Gemini 2.0 Flash)")
print("="*40)
print("Gõ 'q' để thoát")
print("-"*40)

while True:
    text = input("\n📝 Nhập văn bản (EN/VI): ").strip()
    if text.lower() == 'q':
        break
    if not text:
        continue
    
    prompt = f"Dịch sang tiếng Việt (hoặc Anh nếu là Việt): {text}"
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        print(f"🤖 {response.text}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
