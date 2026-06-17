from src.base_worker import BaseWorker
from typing import Any, Dict
import asyncio
import sqlite3
from datetime import datetime
from playwright.async_api import async_playwright
import logging
import os
import json
import random
import time
import traceback

logger = logging.getLogger(__name__)

def _load_fanpage_config() -> Dict:
    """Load fanpage config. Supports multiple pages with themes."""
    config_path = os.path.join("config", "fanpages.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Cannot load fanpages.json: {e}")
    # Fallback to single page
    return {
        "default": {
            "name": "Default Fanpage",
            "url": "https://www.facebook.com/CHẠM",
            "theme": "affiliate"
        }
    }

_FANPAGES = _load_fanpage_config()


class FacebookAutoPoster(BaseWorker):
    description = "Auto post to Facebook Fanpage (Playwright) - Multi fanpage support with retry and verification"
    category = "facebook"
    version = "2.4"  # Updated version

    def __init__(self, headless: bool = False, page_url: str = None, fanpage_key: str = None):
        self.headless = headless
        self.fanpage_key = fanpage_key or "default"
        cfg = _FANPAGES.get(self.fanpage_key, _FANPAGES.get("default", {}))
        self.page_url = page_url or cfg.get("url", "https://www.facebook.com/CHẠM")
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    def healthcheck(self) -> bool:
        auth_file = "facebook_auth.json"
        if not os.path.exists(auth_file):
            logger.warning(f"facebook_auth.json not found at {os.getcwd()}")
            return False
        try:
            import playwright
            cfg = _FANPAGES.get(self.fanpage_key, {})
            logger.info(f"FacebookAutoPoster healthcheck OK for {cfg.get('name', self.fanpage_key)} - {self.page_url}")
            return True
        except ImportError:
            return False

    async def _ensure_browser(self):
        """Ensure browser, context and page are initialized and alive"""
        try:
            # Check if existing browser is still alive
            if self._browser:
                try:
                    await self._browser.contexts
                except Exception:
                    # Browser is dead, clean up
                    await self._cleanup_browser()
            
            if self._playwright is None:
                self._playwright = await async_playwright().start()
            
            if self._browser is None:
                self._browser = await self._playwright.chromium.launch(
                    headless=self.headless,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-infobars",
                        "--lang=vi-VN,vi",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                    ]
                )
            
            if self._context is None:
                self._context = await self._browser.new_context(
                    storage_state="facebook_auth.json",
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                    viewport={"width": 1366, "height": 768},
                )
            
            if self._page is None or self._page.is_closed():
                self._page = await self._context.new_page()
            
            return self._page
        except Exception as e:
            logger.error(f"Failed to ensure browser: {e}")
            await self._cleanup_browser()
            raise

    async def _cleanup_browser(self):
        """Clean up browser resources safely"""
        try:
            if self._page and not self._page.is_closed():
                await self._page.close()
        except:
            pass
        try:
            if self._context and not self._context._closed:
                await self._context.close()
        except:
            pass
        try:
            if self._browser:
                await self._browser.close()
        except:
            pass
        try:
            if self._playwright:
                await self._playwright.stop()
        except:
            pass
        self._page = None
        self._context = None
        self._browser = None
        self._playwright = None

    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Sync wrapper. Accepts payload or flat kwargs.
        """
        payload = kwargs.get("payload", {}) or kwargs

        # Resolve fanpage
        fanpage_key = payload.get("fanpage_key") or payload.get("fanpage") or payload.get("page") or self.fanpage_key
        page_url = payload.get("page_url") or payload.get("url")
        if page_url:
            self.page_url = page_url
        elif fanpage_key and fanpage_key in _FANPAGES:
            self.fanpage_key = fanpage_key
            self.page_url = _FANPAGES[fanpage_key].get("url", self.page_url)

        # Guard placeholder
        if self.page_url and ("your-" in self.page_url or "your-banking" in self.page_url or "your-ai-tech" in self.page_url):
            return {"status": "error", "summary": f"Placeholder URL for {self.fanpage_key}: {self.page_url}. Edit config/fanpages.json with real URL."}

        post_id = payload.get("post_id")
        content = payload.get("content")
        media_path = payload.get("media_path")
        media_type = payload.get("media_type")

        if not content and post_id:
            try:
                conn = sqlite3.connect('sen_v3.db')
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute("SELECT id, content, media_path, media_type FROM facebook_posts WHERE id = ? AND status = 'pending'", (post_id,))
                row = cur.fetchone()
                cur.close()
                conn.close()
                if row:
                    content = row["content"]
                    media_path = row["media_path"]
                    media_type = row["media_type"]
            except Exception as e:
                return {"status": "error", "summary": f"DB lookup failed: {str(e)}"}

        if not content:
            return {"status": "error", "summary": "Missing content"}

        is_personal = payload.get("is_personal", False) if isinstance(payload, dict) else False

        try:
            result = asyncio.run(self._post_to_facebook(post_id or "direct", content, media_path, media_type, is_personal))
            if isinstance(result, dict):
                result["fanpage"] = self.fanpage_key
                result["page_url"] = self.page_url
            return result
        except Exception as e:
            logger.error(f"Facebook post failed: {e}")
            logger.error(traceback.format_exc())
            return {"status": "error", "summary": str(e), "fanpage": self.fanpage_key}

    async def _post_to_facebook(self, post_id: Any, content: str, media_path: str = None, media_type: str = None, is_personal: bool = False) -> Dict[str, Any]:
        """Core posting logic with improved browser management and verification."""
        
        auth_file = "facebook_auth.json"
        if not os.path.exists(auth_file):
            return {"status": "error", "summary": f"Missing {auth_file}. Run save_facebook_auth.py first."}

        fp_cfg = _FANPAGES.get(self.fanpage_key, {})
        page_display_name = fp_cfg.get("name", self.fanpage_key)

        MAX_RETRIES = 3
        for attempt in range(MAX_RETRIES):
            page = None
            try:
                # Get or create browser instance
                page = await self._ensure_browser()
                
                # Navigate to target page
                await page.goto(self.page_url, wait_until="domcontentloaded", timeout=45000)
                await page.wait_for_timeout(3000)

                # SWITCH to page mode if needed
                switched = False
                if not is_personal:
                    switch_selectors = [
                        f'text="Đăng với tư cách {page_display_name}"',
                        'text="Đăng với tư cách Trang"',
                        '[aria-label*="Trang"]',
                        'button:has-text("Trang")',
                        f'text="{page_display_name}"',
                    ]
                    for sel in switch_selectors:
                        try:
                            el = await page.wait_for_selector(sel, timeout=3000)
                            if el:
                                await el.click()
                                await page.wait_for_timeout(2000)
                                switched = True
                                logger.info(f"Switched via: {sel}")
                                break
                        except:
                            continue
                    if switched:
                        await page.wait_for_timeout(2000)
                        try:
                            await page.reload(wait_until="domcontentloaded", timeout=30000)
                            await page.wait_for_timeout(3000)
                        except:
                            pass

                # COMPOSE - Find main composer
                compose_clicked = False
                main_composer = None
                compose_selectors = [
                    'div[aria-label="Viết điều gì đó lên trang..."]',
                    f'div[aria-label="Viết điều gì đó lên {page_display_name}..."]',
                    'div[aria-label*="Viết điều gì đó lên trang"]',
                    'div[role="button"][aria-label*="Tạo bài viết"]',
                    'div[contenteditable="true"][aria-label*="Viết điều gì đó lên trang"]',
                ]
                for sel in compose_selectors:
                    try:
                        el = await page.wait_for_selector(sel, timeout=8000)
                        if el:
                            await el.click()
                            await page.wait_for_timeout(1500)
                            compose_clicked = True
                            main_composer = el
                            logger.info(f"Clicked main page composer: {sel}")
                            break
                    except:
                        continue

                # Fallback composer finder
                if not compose_clicked:
                    try:
                        await page.keyboard.press("c")
                        await page.wait_for_timeout(1500)
                        for sel in [
                            'div[aria-label*="Viết điều gì đó lên trang"]',
                            'div[aria-label*="lên trang"]',
                            'div[contenteditable="true"][aria-label]'
                        ]:
                            try:
                                el = await page.wait_for_selector(sel, timeout=3000)
                                if el:
                                    await el.click()
                                    compose_clicked = True
                                    main_composer = el
                                    logger.info(f"Fallback clicked: {sel}")
                                    break
                            except:
                                pass
                    except:
                        pass

                # Last resort JS focus
                if not compose_clicked:
                    try:
                        await page.evaluate('''() => {
                            const eds = Array.from(document.querySelectorAll('div[contenteditable="true"], [role="textbox"][contenteditable="true"]'));
                            for (const ed of eds) {
                                const parent = ed.closest('div[role="article"], div[aria-label*="bình luận"], div[aria-label*="comment"]');
                                if (!parent) {
                                    ed.focus();
                                    return;
                                }
                            }
                            if (eds.length) eds[0].focus();
                        }''')
                        compose_clicked = True
                        logger.info("Used JS fallback to focus top composer")
                    except:
                        pass

                # TYPE CONTENT
                if content and compose_clicked:
                    try:
                        if main_composer:
                            await main_composer.click()
                            await page.wait_for_timeout(300)
                            await main_composer.type(content, delay=15)
                        else:
                            await page.keyboard.type(content, delay=15)
                        logger.info("Typed content into composer")
                    except Exception as e:
                        logger.warning(f"Typing failed, trying evaluate: {e}")
                        try:
                            await page.evaluate(f"""
                                (txt) => {{
                                    const eds = Array.from(document.querySelectorAll('div[contenteditable="true"], [role="textbox"][contenteditable="true"]'));
                                    for (const ed of eds) {{
                                        const parent = ed.closest('div[role="article"], div[aria-label*="bình luận"], div[aria-label*="comment"]');
                                        if (!parent) {{
                                            ed.focus();
                                            ed.innerText = txt;
                                            return;
                                        }}
                                    }}
                                    if (eds.length) {{
                                        eds[0].focus();
                                        eds[0].innerText = txt;
                                    }}
                                }}
                            """, content)
                            logger.info("Set content via evaluate")
                        except:
                            pass

                # UPLOAD MEDIA if provided
                if media_path and os.path.exists(media_path):
                    try:
                        await page.set_input_files('input[type="file"]', media_path)
                        await page.wait_for_timeout(3000)
                        logger.info("Media uploaded")
                    except Exception as ue:
                        logger.warning(f"Media upload failed: {ue}")

                # SUBMIT POST
                submitted = False
                submit_selectors = [
                    'div[aria-label="Đăng"]',
                    'div[aria-label="Đăng bài"]',
                    'div[role="button"]:has-text("Đăng")',
                    'div[aria-label*="Đăng"]:not([aria-label*="bình luận"])',
                    '[data-testid*="post"]',
                ]
                for sel in submit_selectors:
                    try:
                        await page.click(sel, timeout=5000)
                        submitted = True
                        logger.info(f"Submitted via: {sel}")
                        break
                    except:
                        continue
                
                if not submitted:
                    try:
                        await page.keyboard.press("Control+Enter")
                        submitted = True
                        logger.info("Submitted via Ctrl+Enter")
                    except:
                        pass

                await page.wait_for_timeout(8000)

                # VERIFICATION
                verified = False
                post_url = self.page_url
                snippet = (content or "")[:42].replace("\n", " ").strip()
                
                if snippet:
                    try:
                        for vs in [f'text="{snippet[:28]}"', 'div[role="article"]']:
                            loc = page.locator(vs)
                            if await loc.count() > 0:
                                verified = True
                                break
                        if not verified:
                            html = await page.content()
                            if snippet[:18] in html:
                                verified = True
                    except:
                        pass

                # Get post URL
                try:
                    link_el = await page.query_selector('a[href*="/posts/"], a[aria-label*="Vừa xong"]')
                    if link_el:
                        href = await link_el.get_attribute("href")
                        if href:
                            post_url = "https://www.facebook.com" + href if href.startswith("/") else href
                except:
                    pass

                if not verified:
                    return {
                        "status": "error",
                        "summary": f"Posted but not verified (url={self.page_url}). Snippet: {snippet[:30]}",
                        "post_url": post_url,
                        "fanpage": self.fanpage_key,
                        "attempt": attempt + 1
                    }

                # Update database if post_id is valid
                if isinstance(post_id, (int, str)) and str(post_id).isdigit():
                    try:
                        conn = sqlite3.connect('sen_v3.db')
                        cur = conn.cursor()
                        cur.execute("UPDATE facebook_posts SET status='posted', post_url=?, updated_at=? WHERE id=?",
                                    (post_url, datetime.now(), int(post_id)))
                        conn.commit()
                        cur.close()
                        conn.close()
                        logger.info(f"Updated database for post_id={post_id}")
                    except Exception as e:
                        logger.warning(f"Failed to update database: {e}")

                logger.info(f"✅ VERIFIED posted to {self.fanpage_key}: {post_url}")
                return {
                    "status": "ok",
                    "summary": f"Posted+verified post_id={post_id} to {self.fanpage_key}",
                    "post_url": post_url,
                    "fanpage": self.fanpage_key,
                    "attempt": attempt + 1
                }

            except Exception as e:
                error_msg = str(e).lower()
                logger.error(f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
                
                # Clean up browser on error
                await self._cleanup_browser()
                
                # Retry on browser-related errors
                if attempt < MAX_RETRIES - 1 and ("closed" in error_msg or "target" in error_msg or "browser" in error_msg or "context" in error_msg):
                    logger.info(f"Retrying after browser error...")
                    await asyncio.sleep(3)
                    continue
                
                # Update database on final failure
                if isinstance(post_id, (int, str)) and str(post_id).isdigit():
                    try:
                        conn = sqlite3.connect('sen_v3.db')
                        cur = conn.cursor()
                        cur.execute("UPDATE facebook_posts SET status='failed', error_message=?, updated_at=? WHERE id=?",
                                    (str(e)[:500], datetime.now(), int(post_id)))
                        conn.commit()
                        cur.close()
                        conn.close()
                    except:
                        pass
                
                return {"status": "error", "summary": str(e), "fanpage": self.fanpage_key, "attempt": attempt + 1}

        return {"status": "error", "summary": "Failed after all retries", "fanpage": self.fanpage_key}