"""
Auto post affiliate links to multiple platforms
"""
import webbrowser
import time
import random

# Danh sách link từ database
links = [
    ("TPBANK CREATOR", "https://go.isclix.com/deep_link/v5/6983938396644077046/6767399642708413705?sub4=sen_v3"),
    ("VPBank - Vay Tín chấp", "https://go.isclix.com/deep_link/v5/6983938396644077046/6822308958202075636?sub4=sen_v3"),
    ("Chứng khoán Maybank", "https://go.isclix.com/deep_link/v5/6983938396644077046/6827321992129624253?sub4=sen_v3"),
    ("AppMax Vay Nhanh", "https://go.isclix.com/deep_link/v5/6983938396644077046/6873138885445764645?sub4=sen_v3"),
    ("HDBank - Thẻ tín dụng", "https://go.isclix.com/deep_link/v5/6983938396644077046/6877351644194955800?sub4=sen_v3"),
    ("Chứng khoán Kafi X", "https://go.isclix.com/deep_link/v5/6983938396644077046/6896341778738303892?sub4=sen_v3"),
    ("iShinhan Vay IOS", "https://go.isclix.com/deep_link/v5/6983938396644077046/6949939948611548600?sub4=sen_v3"),
    ("iShinhan Vay Android", "https://go.isclix.com/deep_link/v5/6983938396644077046/6949942463850829113?sub4=sen_v3"),
    ("VPBank SenID", "https://go.isclix.com/deep_link/v5/6983938396644077046/6985504292608237862?sub4=sen_v3"),
    ("TPBank", "https://go.isclix.com/deep_link/v5/6983938396644077046/6985504292608237863?sub4=sen_v3"),
]

print("=" * 70)
print("🚀 KHỞI ĐỘNG QUẢNG BÁ AFFILIATE LINKS")
print("=" * 70)

# Hiển thị danh sách
for i, (name, link) in enumerate(links, 1):
    print(f"\n{i}. {name}")
    print(f"   Link: {link[:80]}...")

# Chọn link để mở
print("\n" + "=" * 70)
print("💡 CÁCH DÙNG:")
print("   1. Copy link và dán lên Facebook, Zalo, TikTok")
print("   2. Chia sẻ vào các group mua bán, tài chính")
print("   3. Theo dõi doanh số qua AccessTrade dashboard")
print("=" * 70)

# Mở nhanh 3 link hàng đầu
print("\n🚀 Mở nhanh 3 link hàng đầu...")
for i in range(3):
    webbrowser.open(links[i][1])
    time.sleep(1)

print("✅ Đã mở 3 link trong trình duyệt!")
