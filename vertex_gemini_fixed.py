# vertex_gemini_fixed.py
import os
import subprocess
import pandas as pd
from datetime import datetime

# Tự động lấy Project ID từ gcloud
def get_project_id():
    try:
        result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                               capture_output=True, text=True)
        project_id = result.stdout.strip()
        if project_id and project_id != '(unset)':
            return project_id
    except:
        pass
    
    # Fallback nếu không lấy được
    return "cosmic-attic-473011-m8"  # Project ID của bạn

PROJECT_ID = get_project_id()
LOCATION = "us-central1"

print(f"🔧 Sử dụng Project ID: {PROJECT_ID}")

# Kiểm tra đã cài đặt thư viện chưa
try:
    from google.cloud import aiplatform
    from vertexai.preview.generative_models import GenerativeModel, GenerationConfig
except ImportError:
    print("❌ Chưa cài đặt thư viện! Chạy lệnh:")
    print("   pip install google-cloud-aiplatform pandas openpyxl")
    exit(1)

# Khởi tạo Vertex AI
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def analyze_accesstrade_excel(file_path):
    """Phân tích file Excel AccessTrade"""
    
    print(f"📂 Đang đọc file: {file_path}")
    
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"❌ Lỗi đọc file: {e}")
        return None
    
    # Kiểm tra các cột cần thiết
    required_cols = ['billing', 'pub_commission']
    for col in required_cols:
        if col not in df.columns:
            print(f"⚠️ Cột '{col}' không tồn tại trong file")
            print(f"   Các cột hiện có: {list(df.columns)}")
            return None
    
    # Tính toán thống kê
    total_orders = len(df)
    total_billing = df['billing'].sum()
    total_commission = df['pub_commission'].sum()
    
    # Top merchants
    top_merchants = ""
    if 'merchant' in df.columns:
        merchant_stats = df.groupby('merchant')['pub_commission'].sum().nlargest(5)
        for merchant, commission in merchant_stats.items():
            top_merchants += f"- {merchant}: {commission:,.0f} VNĐ\n"
    
    # Tạo prompt
    prompt = f"""
    Phân tích báo cáo AccessTrade:

    📊 TỔNG QUAN:
    - Số đơn hàng: {total_orders}
    - Doanh thu: {total_billing:,.0f} VNĐ
    - Hoa hồng: {total_commission:,.0f} VNĐ
    
    🏪 TOP MERCHANTS:
    {top_merchants if top_merchants else "Không có dữ liệu"}
    
    Yêu cầu:
    1. Đánh giá hiệu suất
    2. 3 insight quan trọng
    3. 3 đề xuất cải thiện
    
    Trả lời bằng tiếng Việt.
    """
    
    print("🤖 Đang gọi Gemini API...")
    
    try:
        model = GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Lỗi gọi API: {e}")
        print("\n💡 Gợi ý: Bạn có thể dùng Gemini API free thay vì Vertex AI")
        return None

def main():
    # Tìm file Excel mới nhất
    excel_files = [f for f in os.listdir('.') if f.startswith('accesstrade_report_') and f.endswith('.xlsx')]
    
    if not excel_files:
        print("⚠️ Không tìm thấy file Excel AccessTrade!")
        print("   Chạy script fetch_accesstrade_all_drive.py trước.")
        return
    
    latest_file = max(excel_files, key=os.path.getctime)
    
    # Phân tích
    analysis = analyze_accesstrade_excel(latest_file)
    
    if analysis:
        print("\n" + "="*60)
        print("📊 KẾT QUẢ PHÂN TÍCH")
        print("="*60)
        print(analysis)
        
        # Lưu kết quả
        output_file = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(analysis)
        print(f"\n✅ Đã lưu: {output_file}")
    else:
        print("\n💡 Bạn có thể dùng Gemini API free thay thế:")
        print("   pip install google-generativeai")
        print("   python -c \"import google.generativeai as genai; genai.configure(api_key='YOUR_KEY')\"")

if __name__ == "__main__":
    main()	