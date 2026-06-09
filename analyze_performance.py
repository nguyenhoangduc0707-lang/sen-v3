"""
Phân tích hiệu suất nội bộ để tối ưu tỉ lệ chuyển đổi.

Chạy: python analyze_performance.py

Nó sẽ dùng PostingOptimizer để báo cáo:
- Số post thành công (COMPLETED) theo fanpage/theme/giờ.
- Giờ nào đang convert tốt nhất (dựa trên data hiện có).
- Gợi ý giờ nên ưu tiên cho lần schedule sau.

Đây là nền tảng để "biết tối ưu được tỉ lệ chuyển đổi bằng mọi giá".
Sau này khi bạn bổ sung data chất lượng (clicks, sales, commissions thực), có thể mở rộng optimizer dễ dàng.
"""

from src.optimizer import PostingOptimizer
import json

def main():
    opt = PostingOptimizer()
    
    print("=" * 60)
    print("BÁO CÁO HIỆU SUẤT NỘI BỘ - TỐI ƯU TỈ LỆ CHUYỂN ĐỔI")
    print("=" * 60)
    
    report = opt.get_performance_report(days_back=30)
    
    for fanpage_key, data in report.items():
        print(f"\n📊 {fanpage_key}")
        print(f"   Tổng post thành công (COMPLETED): {data['total_successful_posts']}")
        print(f"   Có data không: {'Có' if data['has_data'] else 'Chưa (dùng config)'}")
        
        if data['best_hours']:
            print("   Top giờ convert tốt nhất (giờ: số thành công):")
            for hour, count in data['best_hours']:
                print(f"      {hour:02d}h → {count} posts thành công")
        else:
            print("   Chưa có data lịch sử → sẽ dùng best_posting_times trong config/fanpages.json")
    
    print("\n" + "=" * 60)
    print("KHUYẾN NGHỊ TỐI ƯU:")
    print("- Khi schedule, hệ thống tự động ưu tiên giờ có historical success cao.")
    print("- Nếu page mới → dùng best_posting_times bạn định nghĩa trong config.")
    print("- Chạy lại analyze_performance.py sau mỗi vài ngày để xem cải thiện.")
    print("=" * 60)

if __name__ == "__main__":
    main()
