import asyncio
import sqlite3
from datetime import datetime
from playwright.async_api import async_playwright
import logging

logger = logging.getLogger(__name__)

class FacebookAutoPoster:
    def __init__(self, headless=False, page_url=None):
        self.headless = headless
        # THAY YOUR_FANPAGE_NAME BẰNG TÊN FANPAGE THẬT CỦA BẠN
        self.page_url = page_url or "https://www.facebook.com/CHẠM"

    async def run(self, **kwargs):
        post_id = kwargs.get("post_id")
        if not post_id:
            return {"status": "error", "summary": "Missing post_id"}

        conn = sqlite3.connect('sen_v3.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT id, content, media_path, media_type, scheduled_time
            FROM facebook_posts
            WHERE id = ? AND status = 'pending'
        """, (post_id,))
        row = cur.fetchone()
        cur.close()
        
        if not row:
            conn.close()
            return {"status": "error", "summary": f"Post {post_id} not found or already posted"}

        content = row["content"]
        media_path = row["media_path"]
        media_type = row["media_type"]

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless)
                context = await browser.new_context(storage_state="facebook_auth.json")
                page = await context.new_page()
                await page.goto(self.page_url)

                # Chờ và nhập nội dung (selector cho Fanpage)
                try:
                    await page.wait_for_selector('div[aria-label="Viết điều gì đó lên trang..."]', timeout=15000)
                    await page.click('div[aria-label="Viết điều gì đó lên trang..."]')
                except:
                    await page.wait_for_selector('div[contenteditable="true"]', timeout=15000)
                    await page.click('div[contenteditable="true"]')
                
                await page.keyboard.type(content)

                # Upload ảnh/video nếu có
                if media_path and media_type:
                    await page.set_input_files('input[type="file"]', media_path)

                # Nhấn nút đăng
                await page.click('div[aria-label="Đăng"]')
                await page.wait_for_timeout(5000)

                # Lấy URL bài đăng (nếu có thể)
                post_url = page.url
                await browser.close()

            cur = conn.cursor()
            cur.execute("""
                UPDATE facebook_posts 
                SET status = 'posted', post_url = ?, updated_at = ?
                WHERE id = ?
            """, (post_url, datetime.now(), post_id))
            conn.commit()
            cur.close()
            conn.close()

            logger.info(f"✅ Đã đăng bài {post_id} thành công lên Fanpage")
            return {"status": "ok", "summary": f"Posted post_id={post_id}", "post_url": post_url}

        except Exception as e:
            cur = conn.cursor()
            cur.execute("""
                UPDATE facebook_posts 
                SET status = 'failed', error_message = ?, updated_at = ?
                WHERE id = ?
            """, (str(e), datetime.now(), post_id))
            conn.commit()
            cur.close()
            conn.close()
            
            logger.error(f"❌ Lỗi khi đăng bài {post_id}: {e}")
            return {"status": "error", "summary": str(e)}
