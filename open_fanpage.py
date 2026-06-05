import asyncio
from playwright.async_api import async_playwright

async def open_fanpage():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state="facebook_auth.json")
        page = await context.new_page()
        
        # ĐỔI URL NÀY THÀNH FANPAGE CỦA BẠN
        await page.goto("https://www.facebook.com/YOUR_FANPAGE_NAME")
        
        print("🔍 Đã mở Fanpage. Kiểm tra thủ công xem có khung 'Viết điều gì đó lên trang...' không?")
        input("Nhấn Enter sau khi kiểm tra xong...")
        await browser.close()

asyncio.run(open_fanpage())
