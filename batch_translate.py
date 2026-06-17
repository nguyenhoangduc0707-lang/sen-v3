import os
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig

load_dotenv()

class BatchTranslator:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("Chưa set GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash-exp"
    
    def translate_text(self, text, target="vi"):
        if not text or pd.isna(text):
            return text
        
        prompt = f"Dịch sang {target}: {text}"
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=GenerateContentConfig(temperature=0.1)
            )
            return response.text.strip()
        except:
            return text
    
    def translate_column(self, df, column, target="vi"):
        """Dịch một cột trong DataFrame"""
        print(f"📝 Đang dịch cột '{column}'...")
        df[f'{column}_translated'] = df[column].apply(
            lambda x: self.translate_text(x, target)
        )
        return df

def main():
    # Tìm file Excel
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    if not excel_files:
        print("❌ Không tìm thấy file Excel")
        return
    
    # Chọn file mới nhất
    latest = max(excel_files, key=os.path.getctime)
    print(f"📂 File: {latest}")
    
    # Đọc và dịch
    df = pd.read_excel(latest)
    translator = BatchTranslator()
    
    # Dịch cột 'merchant' nếu có
    if 'merchant' in df.columns:
        df = translator.translate_column(df, 'merchant')
    
    # Lưu file mới
    output = f"translated_{latest}"
    df.to_excel(output, index=False)
    print(f"✅ Đã lưu: {output}")
    print(f"📊 {len(df)} dòng đã xử lý")

if __name__ == "__main__":
    main()
