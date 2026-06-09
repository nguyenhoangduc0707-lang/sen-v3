# -*- coding: utf-8 -*-
"""
MANUAL WORKFLOW WIZARD - CHỈ DÀNH CHO PAGE "Beauty and Health Hup"
Phiên bản sạch, tập trung vào việc BẠN làm mẫu thủ công full 1 bài viết.

MỤC ĐÍCH:
- Mở browser với profile RIÊNG cho page này.
- Hướng dẫn từng bước rõ ràng bằng tiếng Việt.
- DỪNG LẠI (nhấn Enter) để BẠN thực hiện thủ công trên giao diện thật:
  + Đăng nhập (bước bạn nói thiếu trước đây)
  + Vào đúng page (dùng QR code)
  + Chuyển sang "Đăng với tư cách Trang"
  + Click đúng ô soạn bài CHÍNH của Trang (không phải comment box)
  + Gõ text (dùng 2 bài mẫu bên dưới)
  + Thêm ảnh (nếu muốn)
  + Chọn Cảm xúc / Hoạt động
  + Chọn Vị trí
  + Bấm nút "Đăng"
- Sau khi bạn làm xong 1 bài viết đầy đủ, script sẽ:
  - Lưu cookies/auth riêng: beauty_health_auth.json
  - Ghi log toàn bộ workflow: beauty_health_workflow_log.txt

SAU KHI XONG:
Bạn mô tả hoặc chụp lại CHÍNH XÁC những gì bạn click/gõ ở từng bước (đặc biệt nút Cảm xúc, Vị trí, nút "Đăng" cuối cùng, ô soạn bài chính).
Tôi sẽ dùng đúng những selector + thứ tự đó để viết code automation y chang cho page này.

Chạy:
    python manual_wizard_beauty_health.py

Lưu ý chống Meta block:
- Lần đầu nên login bằng Chrome thật của máy trước, approve thiết bị, tương tác nhẹ với page.
- Khi bị challenge (ảnh, "Hoạt động bất thường", mã SMS...): GIẢI THỦ CÔNG trong browser, di chuột chậm, scroll nhẹ.
- Sau khi giải xong: ĐỢI THÊM 20-40 GIÂY cho feed load đầy đủ trước khi nhấn Enter.
- Dùng profile riêng (.fb_profile_beauty_health) để "quen" dần.

Profile: .fb_profile_beauty_health (riêng biệt, không chung page khác)
Auth output: beauty_health_auth.json
Log: beauty_health_workflow_log.txt
"""

import asyncio
import os
import random
from datetime import datetime
from playwright.async_api import async_playwright

# ==================== CẤU HÌNH RIÊNG CHO PAGE NÀY ====================
PAGE_NAME = "Beauty and Health Hup"
USER_DATA_DIR = os.path.join(os.getcwd(), ".fb_profile_beauty_health")
AUTH_FILE = "beauty_health_auth.json"
LOG_FILE = "beauty_health_workflow_log.txt"

# 2 BÀI MẪU (bạn copy-paste khi đến bước soạn bài)
BAI_MAU_1 = """💧 Uống đủ 2 lít nước mỗi ngày không chỉ giúp da sáng mịn mà còn cải thiện năng lượng và sức khỏe tổng thể. 
Hãy bắt đầu thói quen tốt này từ hôm nay nhé!

#BeautyAndHealth #Skincare #HealthyHabits"""

BAI_MAU_2 = """🌿 Bổ sung vitamin C từ trái cây tươi và rau củ là cách tự nhiên giúp tăng cường miễn dịch và làm đẹp da từ bên trong. 
Bạn đã ăn đủ rau củ hôm nay chưa?

#BeautyAndHealth #NaturalWellness #GlowFromWithin"""

def log_step(step: str, details: str = ""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {step}"
    if details:
        line += f" | {details}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

async def add_strong_stealth(context):
    """Stealth nâng cao để giảm bị Meta chặn (dựa trên kinh nghiệm thực tế)"""
    await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => false });
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1,2,3,4,5].map(i => ({name: 'Plugin ' + i, description: 'desc', filename: 'file'}))
        });
        Object.defineProperty(navigator, 'languages', { get: () => ['vi-VN', 'vi', 'en-US', 'en'] });
        window.chrome = { runtime: { onConnect: null } };
        Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });

        // WebGL
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) return 'Intel Inc.';
            if (parameter === 37446) return 'Intel Iris OpenGL Engine';
            return getParameter.apply(this, arguments);
        };

        // Canvas noise
        const toDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function() {
            const context = this.getContext('2d');
            if (context) {
                context.fillStyle = 'rgba(0,0,0,0.01)';
                context.fillRect(0, 0, 1, 1);
            }
            return toDataURL.apply(this, arguments);
        };
    """)

async def pause_and_wait(step_title: str, instruction: str):
    print("\n" + "=" * 70)
    print(f"BƯỚC: {step_title}")
    print(instruction)
    print("\n→ Thực hiện xong trên trình duyệt (giải hết challenge nếu có).")
    print("→ Đợi feed / Trang load đầy đủ (20-40 giây sau khi giải block).")
    input("→ Nhấn Enter khi đã sẵn sàng bước tiếp theo >>> ")
    log_step("USER_COMPLETED", step_title)

async def main():
    print("=" * 72)
    print("MANUAL WIZARD - BEAUTY AND HEALTH HUP (LÀM MẪU THỦ CÔNG - STEALTH NÂNG CAO)")
    print("Mỗi page 1 script riêng biệt. Lần này chỉ cho page Beauty and Health Hup.")
    print("=" * 72)
    print()
    print("HƯỚNG DẪN QUAN TRỌNG KHI BỊ META CHẶN:")
    print("  - Browser sẽ mở với stealth mạnh.")
    print("  - Nếu hiện challenge (ảnh, 'Hoạt động bất thường', mã SMS, confirm device...):")
    print("      → GIẢI TOÀN BỘ THỦ CÔNG TRONG CỬA SỔ BROWSER.")
    print("      → Di chuột chậm, scroll nhẹ, không vội.")
    print("  - Sau khi giải xong: ĐỢI THÊM 20-40 GIÂY cho feed load đầy đủ.")
    print("  - Chỉ nhấn Enter khi đã thấy rõ giao diện Trang + ô soạn bài.")
    print()
    print("Lần đầu nên:")
    print("  - Mở Chrome thật của máy → đăng nhập → vào page → tương tác nhẹ.")
    print("  - Sau đó mới chạy script này (dùng chung profile sẽ ít bị chặn hơn).")
    print()
    print("2 BÀI MẪU (copy-paste khi đến bước soạn bài):")
    print("\n--- BÀI MẪU 1 ---")
    print(BAI_MAU_1)
    print("\n--- BÀI MẪU 2 ---")
    print(BAI_MAU_2)
    print()
    input("Nhấn Enter để bắt đầu (browser sẽ mở)...")

    os.makedirs(USER_DATA_DIR, exist_ok=True)

    async with async_playwright() as p:
        launch_options = {
            "headless": False,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--lang=vi-VN,vi",
                "--window-size=1366,768",
            ],
            "slow_mo": 80,
        }
        try:
            launch_options["channel"] = "chrome"
            print("[STEALTH] Đang cố dùng Chrome thật của máy bạn...")
        except:
            print("[STEALTH] Dùng Chromium (vẫn có stealth).")

        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            **launch_options
        )

        await add_strong_stealth(context)

        page = await context.new_page()
        await page.set_viewport_size({"width": 1366, "height": 768})

        log_step("WIZARD_STARTED", f"Page: {PAGE_NAME}")

        # BƯỚC 1: ĐĂNG NHẬP (bạn yêu cầu phải có bước này)
        print("\n" + "=" * 70)
        print("BƯỚC 1: ĐĂNG NHẬP THỦ CÔNG (BẮT BUỘC)")
        print("=" * 70)
        await page.goto("https://www.facebook.com", wait_until="domcontentloaded", timeout=60000)
        log_step("OPENED_FACEBOOK_LOGIN")

        await pause_and_wait(
            "ĐĂNG NHẬP THỦ CÔNG + GIẢI HẾT CHALLENGE",
            "Trong trình duyệt đang mở:\n"
            "- Đăng nhập bằng tài khoản thật (số điện thoại + mật khẩu).\n"
            "- Giải hết captcha, ảnh, mã SMS, approve thiết bị nếu có.\n"
            "- Đợi thấy News Feed rõ ràng (bài đăng của bạn bè)."
        )
        log_step("LOGIN_COMPLETED_BY_USER")

        # BƯỚC 2: MỞ ĐÚNG PAGE (dùng QR bạn gửi)
        print("\n" + "=" * 70)
        print("BƯỚC 2: MỞ ĐÚNG PAGE 'Beauty and Health Hup' (DÙNG QR BẠN GỬI)")
        print("=" * 70)
        print("Dùng QR code trong ảnh bạn gửi để tìm page trên Facebook.")
        print("Hoặc search tên 'Beauty and Health Hup'.")
        print("Click vào Trang để vào giao diện Trang (không phải profile cá nhân).")
        await pause_and_wait(
            "ĐÃ MỞ ĐÚNG PAGE 'Beauty and Health Hup'",
            "Đảm bảo bạn thấy tên Trang rõ ràng, có nút 'Thích'/'Theo dõi', và giao diện Trang."
        )
        log_step("PAGE_OPENED_BY_USER", page.url)

        # BƯỚC 3: CHUYỂN SANG "ĐĂNG VỚI TƯ CÁCH TRANG"
        print("\n" + "=" * 70)
        print("BƯỚC 3: CHUYỂN SANG 'ĐĂNG VỚI TƯ CÁCH TRANG'")
        print("=" * 70)
        print("Tìm và click 'Đăng với tư cách [Tên Trang]' hoặc 'Đăng với tư cách Trang'.")
        print("Sau khi click, đợi giao diện chuyển sang chế độ Trang (ô soạn bài mang tên Trang).")
        await pause_and_wait(
            "ĐÃ CHUYỂN THÀNH CÔNG SANG CHẾ ĐỘ TRANG",
            "Bạn phải thấy ô soạn bài có chữ 'Viết điều gì đó lên trang Beauty and Health Hup...' hoặc tương tự."
        )
        log_step("SWITCHED_TO_PAGE_MODE_BY_USER")

        # BƯỚC 4: CLICK Ô SOẠN BÀI CHÍNH CỦA TRANG (QUAN TRỌNG - KHÔNG PHẢI COMMENT)
        print("\n" + "=" * 70)
        print("BƯỚC 4: CLICK VÀO Ô SOẠN BÀI CHÍNH CỦA TRANG (KHÔNG PHẢI COMMENT BOX)")
        print("=" * 70)
        print("Click vào ô LỚN có placeholder 'Viết điều gì đó lên trang...' hoặc 'Tạo bài viết'.")
        print("Đây PHẢI là ô soạn bài CHÍNH của Trang (nằm ở phần trên, không phải ô nhỏ dưới các bài viết cũ).")
        await pause_and_wait(
            "ĐÃ CLICK VÀ FOCUS VÀO Ô SOẠN BÀI CHÍNH CỦA TRANG",
            "Ô soạn bài phải to, sẵn sàng để gõ nội dung, nằm ở vị trí trên cùng của Trang."
        )
        log_step("MAIN_COMPOSER_CLICKED_BY_USER")

        # BƯỚC 5: GÕ NỘI DUNG TEXT
        print("\n" + "=" * 70)
        print("BƯỚC 5: GÕ NỘI DUNG TEXT (DÙNG 1 TRONG 2 BÀI MẪU)")
        print("=" * 70)
        print("Copy một trong hai bài mẫu bên dưới và paste/gõ vào ô soạn bài.")
        print("Bạn có thể chỉnh sửa thêm emoji hoặc xuống dòng cho đẹp.")
        print("\n--- BÀI MẪU 1 ---")
        print(BAI_MAU_1)
        print("\n--- BÀI MẪU 2 ---")
        print(BAI_MAU_2)
        await pause_and_wait(
            "ĐÃ GÕ XONG NỘI DUNG TEXT VÀO Ô SOẠN BÀI",
            "Nội dung phải xuất hiện đầy đủ và rõ ràng trong ô soạn bài của Trang."
        )
        log_step("TEXT_TYPED_BY_USER")

        # BƯỚC 6: THÊM ẢNH (TÙY CHỌN)
        print("\n" + "=" * 70)
        print("BƯỚC 6: THÊM ẢNH (NẾU BẠN MUỐN)")
        print("=" * 70)
        print("Click biểu tượng ảnh/video (hình vuông) → chọn 1-2 ảnh liên quan beauty/health.")
        print("Ảnh phải xuất hiện trong bài trước khi bấm Đăng.")
        print("Nếu không muốn ảnh thì bỏ qua bước này.")
        await pause_and_wait(
            "ĐÃ THÊM ẢNH (HOẶC BỎ QUA NẾU KHÔNG CẦN)",
            "Ảnh (nếu có) phải hiển thị trong phần soạn bài."
        )
        log_step("MEDIA_ADDED_OR_SKIPPED_BY_USER")

        # BƯỚC 7: CHỌN CẢM XÚC / HOẠT ĐỘNG
        print("\n" + "=" * 70)
        print("BƯỚC 7: CHỌN CẢM XÚC / HOẠT ĐỘNG (NẾU BẠN THƯỜNG LÀM)")
        print("=" * 70)
        print("Click biểu tượng mặt cười hoặc dòng 'Cảm xúc/hoạt động' dưới ô soạn bài.")
        print("Chọn một cảm xúc phù hợp (Vui vẻ, Hạnh phúc, Khỏe mạnh...).")
        print("Hoặc bỏ qua nếu không muốn.")
        await pause_and_wait(
            "ĐÃ CHỌN CẢM XÚC (HOẶC BỎ QUA)",
            "Cảm xúc phải hiển thị dưới nội dung bài viết."
        )
        log_step("FEELING_SELECTED_OR_SKIPPED_BY_USER")

        # BƯỚC 8: CHỌN VỊ TRÍ
        print("\n" + "=" * 70)
        print("BƯỚC 8: CHỌN VỊ TRÍ / CHECK-IN (NẾU BẠN THƯỜNG LÀM)")
        print("=" * 70)
        print("Click biểu tượng vị trí (hình ghim bản đồ) dưới ô soạn bài.")
        print("Tìm và chọn địa điểm (spa, cửa hàng mỹ phẩm, phòng gym...).")
        print("Hoặc bỏ qua nếu không muốn.")
        await pause_and_wait(
            "ĐÃ CHỌN VỊ TRÍ (HOẶC BỎ QUA)",
            "Vị trí phải hiển thị dưới nội dung bài viết."
        )
        log_step("LOCATION_SELECTED_OR_SKIPPED_BY_USER")

        # BƯỚC 9: BẤM NÚT "ĐĂNG"
        print("\n" + "=" * 70)
        print("BƯỚC 9: BẤM NÚT 'ĐĂNG' (BƯỚC CUỐI CÙNG)")
        print("=" * 70)
        print("Tìm nút 'Đăng' (thường màu xanh dương, góc dưới bên phải của hộp soạn bài).")
        print("Click CHÍNH XÁC vào nút 'Đăng'.")
        print("Đợi bài xuất hiện trên Trang.")
        await pause_and_wait(
            "ĐÃ BẤM NÚT 'ĐĂNG' VÀ BÀI ĐÃ XUẤT HIỆN TRÊN TRANG",
            "Kiểm tra bài viết có hiển thị công khai trên Trang Beauty and Health Hup chưa."
        )
        log_step("POST_BUTTON_CLICKED_AND_VERIFIED_BY_USER")

        # Lưu auth và kết thúc
        await context.storage_state(path=AUTH_FILE)
        log_step("AUTH_SAVED", f"File: {AUTH_FILE}")

        print("\n" + "=" * 72)
        print("🎉 HOÀN TẤT WORKFLOW THỦ CÔNG CHO PAGE 'Beauty and Health Hup'")
        print("=" * 72)
        print(f"💾 Auth riêng đã lưu: {os.path.abspath(AUTH_FILE)}")
        print(f"📝 Log workflow đầy đủ: {os.path.abspath(LOG_FILE)}")
        print()
        print("BÂY GIỜ HÃY CHO TÔI BIẾT (CÀNG CHI TIẾT CÀNG TỐT):")
        print("  - Bạn gặp thách thức Meta nào? (captcha ảnh, 'Hoạt động bất thường', mã SMS...)")
        print("  - Ở bước Cảm xúc: bạn click vào đâu, chọn cái gì?")
        print("  - Ở bước Vị trí: bạn click vào đâu, chọn địa điểm nào?")
        print("  - Nút 'Đăng' cuối cùng: text trên nút là gì? (hoặc chụp F12 selector)")
        print("  - Ô soạn bài chính: bạn click vào text/aria-label nào?")
        print("  - Thứ tự bạn làm (gõ text trước hay thêm ảnh trước?)")
        print("  - Nếu có thể, F12 inspect và cho tôi selector của các nút quan trọng.")
        print()
        print("Tôi sẽ dùng CHÍNH XÁC những gì bạn làm để viết code automation y chang cho page này.")
        print("=" * 72)

        await context.close()

if __name__ == "__main__":
    # Fix RuntimeError: Event loop is closed trên Windows
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nĐã dừng bởi người dùng.")
    except Exception as e:
        print(f"\nLỗi: {e}")
        import traceback
        traceback.print_exc()
