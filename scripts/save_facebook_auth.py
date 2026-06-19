#!/usr/bin/env python3
"""
Interactive script to save Facebook session for facebook_autoposter worker.
Usage:
  pip install playwright
  playwright install chromium
  python scripts/save_facebook_auth.py

It opens Chromium (not headless), let you login, then saves storage_state to credentials/facebook_auth.json
"""
import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

AUTH_FILE = Path("credentials/facebook_auth.json")

async def save_facebook_session():
    print("Starting save_facebook_auth session flow")
    try:
        import playwright
    except ImportError:
        print("Playwright not installed. Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.facebook.com/")

        print("\nPlease login to Facebook in the opened browser window. After login (and 2FA if any), come back here and press ENTER to save session.")
        input("Press ENTER after successful login to save session...\n")

        storage = await context.storage_state()
        auth_data = {
            "storage_state": storage,
            "saved_at": datetime.utcnow().isoformat(),
        }
        AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(AUTH_FILE, "w", encoding="utf-8") as f:
            json.dump(auth_data, f, indent=2, ensure_ascii=False)

        print(f"Saved Facebook auth to: {AUTH_FILE.resolve()}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(save_facebook_session())
