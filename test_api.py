import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def test_gemini():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ API Key không tìm thấy trong .env")
        return
    
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-10:]}")
    
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents="Xin chào, hãy giới thiệu ngắn gọn về bạn trong 1 câu."
        )
        print("\n✅ Kết nối thành công!")
        print(f"🤖 Response: {response.text}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    test_gemini()
