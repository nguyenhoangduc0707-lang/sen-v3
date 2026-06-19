import json
import asyncio
from pathlib import Path
from typing import Dict, Any

# Đường dẫn đến file auth (tìm từ root dự án)
AUTH_FILE = Path(__file__).resolve().parent.parent.parent / "credentials" / "facebook_auth.json"

class FacebookAutoPoster:
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Kiểm tra dry_run
        if self.dry_run or payload.get("dry_run", False):
            return {
                "status": "ok",
                "summary": "dry_run - simulated post (no browser actions performed)",
                "fanpage": payload.get("fanpage", "default"),
                "post_url": None
            }

        # Nếu không dry_run, cần auth file
        if not AUTH_FILE.exists():
            return {
                "status": "error",
                "message": "Missing facebook_auth.json. Run save_facebook_auth.py first.",
                "auth_file": str(AUTH_FILE)
            }

        # Đọc auth file và thực hiện post
        try:
            with open(AUTH_FILE, "r", encoding="utf-8") as f:
                auth_data = json.load(f)
            # Gọi hàm post thực tế (có thể dùng playwright)
            result = asyncio.run(self._post_with_session(payload, auth_data))
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to post: {str(e)}"
            }

    async def _post_with_session(self, payload: Dict[str, Any], auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Thực hiện post thật với session đã lưu (cần playwright)"""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            return {
                "status": "error",
                "message": "Playwright not installed. Run: pip install playwright && playwright install chromium"
            }

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=auth_data.get("storage"))
            page = await context.new_page()

            fanpage = payload.get("fanpage", "default")
            content = payload.get("content", "")

            if not content:
                return {"status": "error", "message": "Missing content"}

            # Điều hướng đến fanpage
            await page.goto(f"https://www.facebook.com/{fanpage}")

            # Click vào textarea và nhập nội dung
            await page.click('div[role="textbox"]')
            await page.fill('div[role="textbox"]', content)

            # Click nút Post
            await page.click('div[role="button"]:has-text("Post")')

            # Đợi bài viết xuất hiện (có thể kiểm tra thêm)
            await page.wait_for_selector('div[role="article"]', timeout=10000)

            await browser.close()
            return {
                "status": "success",
                "message": "Posted successfully",
                "fanpage": fanpage,
                "post_url": f"https://www.facebook.com/{fanpage}"
            }