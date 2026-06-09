# -*- coding: utf-8 -*-
"""
Script lưu session Facebook (facebook_auth.json) cho DYT Core.

QUAN TRỌNG KHI GẶP META ROBOT / CAPTCHA / "XÁC NHẬN BẠN KHÔNG PHẢI ROBOT":

Meta rất hay chặn Playwright. Bạn PHẢI giải thủ công trong browser.

Cách xử lý khi bị chặn:
1. Browser mở ra (có thể hiện trang login hoặc challenge).
2. Nếu hiện "Chúng tôi cần xác nhận đây là bạn", grid ảnh, "Hoạt động bất thường", nhập mã SMS, approve thiết bị trên điện thoại... 
   → GIẢI HOÀN TOÀN TRONG CỬA SỔ BROWSER ĐANG MỞ.
3. Di chuột tự nhiên, scroll, click chậm một chút (đừng vội).
4. Sau khi giải xong, ĐỢI THÊM 10-20 GIÂY cho đến khi trang load đầy đủ News Feed.
   - Bạn phải thấy các bài đăng của bạn bè hoặc page.
   - Tốt nhất là click vào page của bạn (affiliate hoặc motivational) và thấy nút "Viết điều gì đó" hoặc compose box.
5. CHỈ KHI ĐÓ mới quay lại console PowerShell và nhấn Enter.
6. Nếu bạn nhấn Enter quá sớm → auth yếu, lần sau lại bị chặn.

Script này đã dùng:
- Persistent profile (.fb_profile) → lần chạy sau ít bị chặn hơn.
- Thử dùng Chrome thật của máy (nếu có).
- Stealth scripts.

Nếu vẫn bị chặn nhiều lần:
- Chạy script này 3-4 lần liên tiếp (dùng chung profile).
- Trước khi chạy, mở Chrome thường của bạn, login FB, approve thiết bị nếu có.
- Chạy ở mạng nhà ổn định, không VPN.

Sau khi lưu thành công (có c_user + xs), chạy:
  python test_facebook_auth.py
  python run_scheduled_posts.py --once
"""

import asyncio
import os
import json
from playwright.async_api import async_playwright

AUTH_FILE = "facebook_auth.json"
USER_DATA_DIR = os.path.join(os.getcwd(), ".fb_profile_poster")  # persistent giúp giảm captcha, dùng chung với poster và test

async def save_auth(fanpage_key: str = None):
    print("=" * 70)
    print("SAVE FACEBOOK AUTH - DYT Core (Stealth + Persistent)")
    print("=" * 70)
    print()
    print("HƯỚNG DẪN CHI TIẾT KHI GẶP META BLOCK:")
    print("  - Browser sẽ mở.")
    print("  - Đăng nhập nếu cần (bằng cách bạn hay dùng, KHÔNG cần password trong code).")
    print("  - KHI META HIỆN THÁCH THỨC ROBOT/CAPTCHA/ẢNH/XÁC NHẬN:")
    print("      → GIẢI TRONG BROWSER (chọn ảnh đúng, nhập code từ điện thoại, v.v.)")
    print("      → Di chuột tự nhiên, scroll chậm.")
    print("  - SAU KHI GIẢI XONG: ĐỢI THÊM 15-30 GIÂY cho News Feed load đầy đủ.")
    print("  - Script sẽ tự động mở đúng page từ config và thử chuyển sang 'Đăng với tư cách Trang'.")
    print("  - Tốt nhất: Đảm bảo thấy ô soạn bài 'Viết điều gì đó lên trang...' (cho Trang).")
    print("  - CHỈ KHI ẤY mới nhấn Enter ở console này.")
    print("  - Nếu nhấn sớm → auth yếu → lần sau lại gặp Meta.")
    print()
    print("=" * 70)
    print()

    # Thử dùng Chrome thật (tốt hơn rất nhiều)
    channel = None
    try:
        channel = "chrome"
        print("[INFO] Sẽ cố dùng Chrome thật của máy bạn (channel=chrome).")
    except:
        print("[INFO] Dùng Chromium mặc định của Playwright.")

    async with async_playwright() as p:
        # Tham khảo stealth từ archive/scripts/fb_auto_undetected.py, fb_selenium.py, computer_use_agent.py
        launch_args = {
            "headless": False,
            "channel": channel,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-site-isolation-trials",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-accelerated-2d-canvas",
                "--no-first-run",
                "--no-zygote",
                "--disable-gpu",
                "--disable-web-security",
                "--disable-features=Translate",
                "--disable-infobars",
                "--lang=vi-VN",
            ],
            "slow_mo": 50,   # chậm hơn để giống người
        }

        # Persistent context rất quan trọng để giảm block lần sau
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            **launch_args
        )

        # Stealth mạnh
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['vi-VN', 'vi', 'en-US', 'en'] });
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
        """)

        page = await context.new_page()
        await page.set_viewport_size({"width": 1366, "height": 768})

        print("\n🌐 Đang mở facebook.com ... (bạn có thể tự gõ nếu bị redirect)")
        try:
            await page.goto("https://www.facebook.com", wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print(f"[WARN] Lỗi load trang: {e}. Tiếp tục thôi.")

        print("\n" + "=" * 60)
        print("🔐 BÂY GIỜ HÃY ĐĂNG NHẬP VÀ GIẢI MỌI THÁCH THỨC CỦA META")
        print("   - Bạn KHÔNG cần nhập mật khẩu vào lệnh hay code.")
        print("   - Script chỉ mở trình duyệt sạch để BẠN tự đăng nhập như bình thường.")
        print("   - Dùng cách bạn hay dùng: số điện thoại + mã SMS, approve trên app điện thoại, 2FA, Google, v.v.")
        print("   - Sau khi login tài khoản cá nhân:")
        print("     + Click vào Trang (Page) của bạn để quản lý.")
        print("     + Click 'Đăng với tư cách Trang' nếu hiện.")
        print("     + Đợi thật kỹ (20-40 giây), scroll, đảm bảo thấy rõ ô soạn bài cho TRANG (không phải cá nhân).")
        print("   - CHỈ KHI ẤY mới quay lại console và nhấn Enter.")
        print("=" * 60 + "\n")

        input("✅ Nhấn Enter CHỈ SAU KHI BẠN ĐÃ LOGIN + CHUYỂN SANG TRANG + THẤY Ô SOẠN BÀI CHO TRANG RÕ RÀNG: ")

        # Thử chuyển sang page posting mode để capture cookies tốt hơn cho post
        try:
            switch_sels = ['text="Đăng với tư cách Trang"', 'span:has-text("Đăng với tư cách")']
            for sw in switch_sels:
                await page.wait_for_selector(sw, timeout=3000)
                await page.click(sw)
                print(f"   → Đã chuyển sang đăng với tư cách Trang trong lúc save (tốt cho cookies)")
                await page.wait_for_timeout(2000)
                break
        except:
            pass

        # Thử detect login mạnh hơn
        logged_in = False
        login_selectors = [
            '[aria-label*="Trang chủ"]',
            '[aria-label*="News Feed"]',
            'div[role="feed"]',
            'a[href*="/me/"]',
            '[data-pagelet="RightRail"]',
            'div[aria-label*="Tạo bài viết"]',
            'div[aria-label*="Viết điều gì đó"]'
        ]

        for sel in login_selectors:
            try:
                await page.wait_for_selector(sel, timeout=10000)
                print(f"   → Phát hiện login qua: {sel}")
                logged_in = True
                break
            except:
                continue

        if not logged_in:
            print("\n⚠️  Không tự detect được login đầy đủ.")
            print("   Có thể bạn vẫn đang ở trang challenge hoặc chưa load xong.")
            print("   Nếu bạn chắc chắn đã login và thấy feed → vẫn có thể thử lưu.")
            confirm = input("   Bạn có muốn lưu session hiện tại không? (y/n): ").strip().lower()
            if confirm != 'y':
                print("   Hủy lưu. Hãy giải challenge kỹ hơn rồi chạy lại script.")
                await context.close()
                return

        # Lưu
        await context.storage_state(path=AUTH_FILE)
        await context.close()

        print(f"\n💾 Đã lưu session vào: {os.path.abspath(AUTH_FILE)}")

        # Validate mạnh
        try:
            with open(AUTH_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            cookies = data.get("cookies", [])
            names = [c.get("name", "") for c in cookies]

            has_cuser = "c_user" in names
            has_xs = "xs" in names

            print(f"   Số cookies: {len(cookies)}")
            print(f"   c_user: {has_cuser} | xs: {has_xs}")

            if has_cuser and has_xs:
                print("\n✅ XUẤT SẮC! Auth có session đầy đủ (c_user + xs).")
                print("   Bây giờ chạy kiểm tra:")
                print("     python test_facebook_auth.py")
                print("   Sau đó đăng bài:")
                print("     python run_scheduled_posts.py --once")
            else:
                print("\n⚠️  Auth vẫn yếu (thiếu c_user hoặc xs).")
                print("    → Meta có thể vẫn coi là chưa login thật.")
                print("    → XÓA file facebook_auth.json")
                print("    → Chạy lại script này, GIẢI CHALLENGE KỸ HƠN, ĐỢI FEED LÂU HƠN trước khi nhấn Enter.")
        except Exception as ve:
            print(f"   Lỗi validate: {ve}")

        print("\n" + "=" * 70)
        print("MẸO GIẢM BỊ CHẶN LẦN SAU:")
        print("  - Giữ nguyên thư mục .fb_profile (đừng xóa).")
        print("  - Chạy script này vài lần (dù auth đã tốt) để profile 'quen' hơn.")
        print("  - Login bằng Chrome thường trước, approve thiết bị.")
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(save_auth())
