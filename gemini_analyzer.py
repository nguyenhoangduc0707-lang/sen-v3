import os
import pandas as pd
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def analyze_accesstrade_data():
    print("🤖 GEMINI DATA ANALYZER")
    print("="*60)
    
    # Kiểm tra API Key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ LỖI: Chưa cấu hình GEMINI_API_KEY trong .env")
        print("   Lấy key tại: https://aistudio.google.com/apikey")
        return
    
    # Cấu hình Gemini
    genai.configure(api_key=api_key)
    print("✅ Đã cấu hình Gemini API")
    
    # Tìm file Excel
    excel_files = [f for f in os.listdir('.') if f.startswith('accesstrade_report_') and f.endswith('.xlsx')]
    if not excel_files:
        print("❌ Không tìm thấy file Excel AccessTrade")
        return
    
    latest_file = max(excel_files, key=os.path.getctime)
    print(f"📂 Đọc file: {latest_file}")
    
    try:
        df = pd.read_excel(latest_file)
        print(f"✅ Đọc thành công {len(df)} dòng dữ liệu")
        
        # Tính toán thống kê
        total_billing = df['billing'].sum() if 'billing' in df.columns else 0
        total_commission = df['pub_commission'].sum() if 'pub_commission' in df.columns else 0
        
        # Top merchants
        merchant_text = ""
        if 'merchant' in df.columns:
            top = df.groupby('merchant')['pub_commission'].sum().nlargest(5)
            merchant_text = "\n".join([f"- {m}: {c:,.0f} VNĐ" for m, c in top.items()])
        
        # Tạo prompt
        prompt = f"""
        Phân tích báo cáo AccessTrade:

        📊 TỔNG QUAN:
        - Số đơn hàng: {len(df)}
        - Doanh thu: {total_billing:,.0f} VNĐ
        - Hoa hồng: {total_commission:,.0f} VNĐ
        - ROI: {(total_commission/total_billing*100) if total_billing > 0 else 0:.1f}%

        🏪 TOP 5 MERCHANTS:
        {merchant_text}

        Yêu cầu phân tích:
        1. Đánh giá hiệu suất tổng thể
        2. 3 insight quan trọng nhất
        3. 3 đề xuất chiến lược cải thiện

        Trả lời bằng tiếng Việt, trình bày rõ ràng.
        """
        
        print("🤖 Đang gọi Gemini API...")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Hiển thị kết quả
        print("\n" + "="*60)
        print("📊 KẾT QUẢ PHÂN TÍCH")
        print("="*60)
        print(response.text)
        
        # Lưu kết quả
        output_file = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"\n✅ Đã lưu kết quả vào: {output_file}")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    analyze_accesstrade_data()
