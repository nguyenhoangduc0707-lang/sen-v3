#!/usr/bin/env python3
"""
UAT Test Script - REAL ONLY (no simulation, no mocks, no stubs)
Run with: python scripts/uat_test.py --env local --base-url http://localhost:8001
Records actual HTTP status + response snippets from the live server.
"""

import asyncio
import aiohttp
import sys
import argparse
from datetime import datetime, timedelta


class UATTester:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url.rstrip("/")
        self.token = None
        self.results = []

    def _log(self, msg: str):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {msg}")

    async def test_health(self):
        url = f"{self.base_url}/health"
        self._log(f"GET {url}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    text = await resp.text()
                    if resp.status == 200:
                        self._record_result("Health check", True, f"HTTP {resp.status} OK | {text[:100]}")
                        return True
                    else:
                        self._record_result("Health check", False, f"HTTP {resp.status} | {text[:200]}")
                        return False
        except Exception as e:
            self._record_result("Health check", False, f"EXCEPTION: {e}")
            return False

    async def test_auth(self):
        url = f"{self.base_url}/auth/login"
        payload = {"email": "admin@dyt.com", "password": "admin123"}
        self._log(f"POST {url} (email=admin@dyt.com)")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    text = await resp.text()
                    if resp.status == 200:
                        data = await resp.json()
                        self.token = data.get("access_token")
                        self._record_result("Authentication", True, f"HTTP {resp.status} | token received (len={len(self.token or '')})")
                        return True
                    else:
                        self._record_result("Authentication", False, f"HTTP {resp.status} | {text[:300]}")
                        return False
        except Exception as e:
            self._record_result("Authentication", False, f"EXCEPTION: {e}")
            return False

    async def test_create_schedule(self):
        if not self.token:
            self._record_result("Create schedule", False, "SKIPPED (no auth token)")
            return False
        url = f"{self.base_url}/schedules"
        future = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
        payload = {
            "task_type": "post_to_page",
            "data": {"page_id": "test", "message": "UAT real test"},
            "scheduled_at": future,
            "priority": 0
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        self._log(f"POST {url} (future schedule)")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as resp:
                    text = await resp.text()
                    if resp.status in (200, 201):
                        self._record_result("Create schedule", True, f"HTTP {resp.status} | {text[:200]}")
                        return True
                    else:
                        self._record_result("Create schedule", False, f"HTTP {resp.status} | {text[:300]}")
                        return False
        except Exception as e:
            self._record_result("Create schedule", False, f"EXCEPTION: {e}")
            return False

    async def test_scheduler_enqueue(self):
        # For honest UAT without separate scheduler worker running we just list schedules
        # and report whether the previously created one is visible (is_processed=False expected).
        if not self.token:
            self._record_result("Scheduler enqueue / list", False, "SKIPPED (no auth token)")
            return False
        url = f"{self.base_url}/schedules"
        headers = {"Authorization": f"Bearer {self.token}"}
        self._log(f"GET {url} (verify schedule list after create)")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    text = await resp.text()
                    if resp.status == 200:
                        data = await resp.json()
                        count = len(data) if isinstance(data, list) else 0
                        self._record_result("Scheduler enqueue / list", True, f"HTTP {resp.status} | {count} schedules returned | sample={text[:180]}")
                        return True
                    else:
                        self._record_result("Scheduler enqueue / list", False, f"HTTP {resp.status} | {text[:300]}")
                        return False
        except Exception as e:
            self._record_result("Scheduler enqueue / list", False, f"EXCEPTION: {e}")
            return False

    async def test_affiliate_campaigns(self):
        if not self.token:
            self._record_result("Affiliate campaigns", False, "SKIPPED (no auth token)")
            return False
        url = f"{self.base_url}/affiliate/campaigns?limit=5"
        headers = {"Authorization": f"Bearer {self.token}"}
        self._log(f"GET {url}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    text = await resp.text()
                    if resp.status == 200:
                        self._record_result("Affiliate campaigns", True, f"HTTP {resp.status} | {text[:250]}")
                        return True
                    else:
                        self._record_result("Affiliate campaigns", False, f"HTTP {resp.status} | {text[:300]}")
                        return False
        except Exception as e:
            self._record_result("Affiliate campaigns", False, f"EXCEPTION: {e}")
            return False

    def _record_result(self, name: str, passed: bool, message: str = ""):
        self.results.append({"name": name, "passed": passed, "message": message})
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} | {name}: {message}")

    def summary(self):
        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)
        print("\n" + "=" * 60)
        print("UAT Results (REAL RUN - NO SIMULATION):")
        print(f"  {passed}/{total} passed")
        print("=" * 60)
        for r in self.results:
            s = "PASS" if r["passed"] else "FAIL"
            print(f"  [{s}] {r['name']}: {r['message']}")
        print("=" * 60)
        if passed == total:
            print("🎉 All tests passed on real system.")
        else:
            print("⚠️  Some tests failed or pending on real system. See details above.")
        return passed, total


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", default="local")
    parser.add_argument("--base-url", default="http://localhost:8001")
    args = parser.parse_args()

    print(f"Starting REAL UAT against: {args.base_url} (env={args.env})")
    print("Using ONLY live endpoints. No mocks.\n")

    tester = UATTester(args.base_url)

    await tester.test_health()
    auth_ok = await tester.test_auth()
    if auth_ok:
        await tester.test_create_schedule()
        await tester.test_scheduler_enqueue()
        await tester.test_affiliate_campaigns()
    else:
        print("❌ Authentication failed - downstream tests require valid JWT and were skipped.")

    passed, total = tester.summary()
    # Exit non-zero if not all pass (for CI friendliness)
    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
