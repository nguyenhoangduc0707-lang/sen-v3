# vertex_gemini_accesstrade.py
import os
import pandas as pd
from datetime import datetime
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig

# Cấu hình - THAY ĐỔI CÁC GIÁ TRỊ NÀY
PROJECT_ID = "YOUR_PROJECT_ID"  # Thay bằng Project ID thật
LOCATION = "us-central1"  # us-central1, asia-southeast1, v.v.

# Khởi tạo Vertex AI
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def analyze_accesstrade_excel(file_path):
    """Phân tích file Excel AccessTrade bằng Gemini trên Vertex AI"""
    
    print(f"📂 Đang đọc file: {file_path}")
    
    # Đọc dữ liệu Excel
    df = pd.read_excel(file_path)
    
    # Tính toán thống kê
    total_orders = len(df)
    total_billing = df['billing'].sum() if 'billing' in df.columns else 0
    total_commission = df['pub_commission'].sum() if 'pub_commission' in df.columns else 0
    
    # Top merchants
    top_merchants = ""
    if 'merchant' in df.columns and 'pub_commission' in df.columns:
        merchant_stats = df.groupby('merchant')['pub_commission'].sum().nlargest(5)
        for merchant, commission in merchant_stats.items():
            top_merchants += f"- {merchant}: {commission:,.0f} VNĐ\n"
    
    # Tạo prompt
    prompt = f"""
    Bạn là chuyên gia phân tích dữ liệu e-commerce. Hãy phân tích báo cáo AccessTrade:

    📊 THỐNG KÊ TỔNG QUAN:
    - Tổng số đơn hàng: {total_orders}
    - Tổng doanh thu: {total_billing:,.0f} VNĐ
    - Tổng hoa hồng: {total_commission:,.0f} VNĐ
    
    🏪 TOP MERCHANTS THEO HOA HỒNG:
    {top_merchants}
    
    YÊU CẦU:
    1. Đánh giá hiệu suất tổng thể
    2. Chỉ ra 3 insight quan trọng nhất
    3. Đề xuất 3 chiến lược cụ thể để tăng hoa hồng
    
    Trình bày ngắn gọn, chuyên nghiệp bằng tiếng Việt.
    """
    
    print("🤖 Đang gọi Gemini API...")
    
    # Gọi Gemini
    model = GenerativeModel("gemini-1.5-flash")  # Hoặc gemini-1.5-pro
    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            temperature=0.7,
            max_output_tokens=2048,
        )
    )
    
    return response.text

def main():
    """Main function"""
    
    # Kiểm tra đã set project ID chưa
    if PROJECT_ID == "YOUR_PROJECT_ID":
        print("❌ Lỗi: Bạn cần thay đổi PROJECT_ID trong script!")
        print("   Lấy Project ID tại: https://console.cloud.google.com")
        print("   Hoặc chạy: gcloud config get-value project")
        return
    
    # Tìm file Excel mới nhất
    excel_files = [f for f in os.listdir('.') if f.startswith('accesstrade_report_') and f.endswith('.xlsx')]
    
    if not excel_files:
        print("⚠️ Không tìm thấy file Excel AccessTrade!")
        print("   Hãy chạy script fetch_accesstrade_all_drive.py trước.")
        return
    
    latest_file = max(excel_files, key=os.path.getctime)
    
    try:
        # Phân tích
        analysis = analyze_accesstrade_excel(latest_file)
        
        # In kết quả
        print("\n" + "="*60)
        print("📊 KẾT QUẢ PHÂN TÍCH")
        print("="*60)
        print(analysis)
        
        # Lưu kết quả
        output_file = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(analysis)
        print(f"\n✅ Đã lưu phân tích vào: {output_file}")
        
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    main()