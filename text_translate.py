import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def translate_text():
    """Dịch văn bản sử dụng Gemini"""
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Chưa set GEMINI_API_KEY")
        return
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    print("🌐 DỊCH VĂN BẢN")
    print("="*40)
    print("Gõ 'q' để thoát")
    print("-"*40)
    
    while True:
        text = input("\n📝 Nhập văn bản (EN/VI): ").strip()
        if text.lower() == 'q':
            break
        
        if not text:
            continue
        
        prompt = f"""
        Dịch văn bản sau sang tiếng Việt (nếu đang là tiếng Anh) 
        hoặc sang tiếng Anh (nếu đang là tiếng Việt):
        
        Văn bản: {text}
        
        Chỉ trả về bản dịch, không giải thích.
        """
        
        try:
            response = model.generate_content(prompt)
            print(f"🤖 Dịch: {response.text}")
        except Exception as e:
            print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    translate_text()
