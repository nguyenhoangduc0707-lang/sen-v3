import asyncio
import json
from playwright.async_api import async_playwright

async def open_facebook():
    with open("facebook_auth.json", "r") as f:
        storage_state = json.load(f)
    
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context(storage_state=storage_state)
    page = await context.new_page()
    
    await page.goto("https://www.facebook.com/")
    
    print("\n✅ Đã đăng nhập! Bạn có thể đăng bài THỦ CÔNG")
    print("📝 Hãy đăng bài bằng tay trong trình duyệt")
    print("🔄 Sau khi đăng bài xong, đóng trình duyệt và quay lại")
    
    input("\nNhấn Enter để đóng...")
    await browser.close()

asyncio.run(open_facebook())
