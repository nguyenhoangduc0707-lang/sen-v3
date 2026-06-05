import asyncio
from playwright.async_api import async_playwright

async def save_auth():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.facebook.com")
        print("🔐 Vui lòng đăng nhập Facebook trong trình duyệt vừa mở.")
        input("✅ Sau khi đăng nhập xong, nhấn Enter để lưu session...")
        await context.storage_state(path="facebook_auth.json")
        await browser.close()
        print("💾 Đã lưu session vào file facebook_auth.json")

if __name__ == "__main__":
    asyncio.run(save_auth())
