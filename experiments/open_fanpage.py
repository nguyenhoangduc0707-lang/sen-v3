# -*- coding: utf-8 -*-
"""
Simple script to open a fanpage with saved auth and check for compose box.
Useful to debug "content not available" or compose not found.

Usage:
  python open_fanpage.py --fanpage_key affiliate_fashion_cosmetics

This will:
- Use the persistent profile and auth
- Open the page
- Try to switch to "Đăng với tư cách Trang"
- Wait and print if compose box is found
- Keep browser open for 20s for manual inspection
"""

import asyncio
import json
import os
import sys
from playwright.async_api import async_playwright

async def main(fanpage_key: str):
    auth_file = "facebook_auth.json"
    if not os.path.exists(auth_file):
        print("❌ Không tìm thấy facebook_auth.json. Chạy save_facebook_auth.py trước.")
        return

    # Load config
    try:
        with open("config/fanpages.json", encoding="utf-8") as f:
            cfg = json.load(f)
        page_url = cfg[fanpage_key]["url"]
        name = cfg[fanpage_key]["name"]
        is_personal = cfg[fanpage_key].get("is_personal", False)
    except Exception as e:
        print(f"❌ Lỗi load config: {e}")
        return

    print(f"=== OPEN FANPAGE: {name} ===")
    print(f"URL: {page_url}")
    print(f"is_personal: {is_personal}")

    async with async_playwright() as p:
        user_data_dir = os.path.join(os.getcwd(), ".fb_profile_poster")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        await context.storage_state(path=auth_file)
        page = await context.new_page()
        print("\nĐang mở trang...")
        await page.goto(page_url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)

        # Try switch if needed
        if not is_personal:
            print("Thử chuyển sang Trang...")
            switch_sels = [
                'text="Đăng với tư cách Trang"',
                'span:has-text("Đăng với tư cách")',
                '[aria-label*="Đăng với tư cách Trang"]',
                f'text="{name}"',
            ]
            for sw in switch_sels:
                try:
                    await page.wait_for_selector(sw, timeout=3000)
                    await page.click(sw)
                    print(f"  → Clicked: {sw}")
                    await page.wait_for_timeout(2000)
                    break
                except:
                    pass

        # Check for compose
        compose_sels = [
            'div[aria-label="Viết điều gì đó lên trang..."]',
            'div[aria-label="Bạn đang nghĩ gì?"]',
            'div[contenteditable="true"]',
            'div[role="textbox"]',
        ]
        found = False
        for sel in compose_sels:
            try:
                el = await page.wait_for_selector(sel, timeout=5000)
                if el:
                    print(f"✅ TÌM THẤY ô soạn thảo: {sel}")
                    print("   → Page load OK, có thể post.")
                    found = True
                    break
            except:
                pass

        if not found:
            print("❌ KHÔNG tìm thấy ô soạn thảo.")
            print("   - Kiểm tra đã login đúng chưa (c_user, xs trong auth).")
            print("   - Thử click thủ công 'Đăng với tư cách Trang'.")
            print("   - Đảm bảo URL đúng và bạn là admin của page.")
            print("   - Nếu page hiện 'This content isn't available', có thể cần login lại hoặc sai quyền.")

        print("\n⏸️ Browser giữ mở 20 giây để bạn kiểm tra thủ công...")
        await page.wait_for_timeout(20000)
        await context.close()
        print("Đóng browser.")

if __name__ == "__main__":
    key = "affiliate_fashion_cosmetics"
    if len(sys.argv) > 1:
        key = sys.argv[1]
    asyncio.run(main(key))
