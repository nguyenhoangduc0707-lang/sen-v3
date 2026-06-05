"""
Auto Worker v?i User-Agent gi? l?p tr?nh duy?t
"""
import asyncio
import aiohttp
import json
import random
from datetime import datetime

class ImprovedAutoWorker:
    def __init__(self, target_per_day=20):
        self.target_per_day = target_per_day
        self.start_time = datetime.now()
        self.report_file = "auto_worker_report.json"
        
        # User agents gi? l?p tr?nh duy?t
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0"
        ]
    
    async def process_link(self, session, task):
        """X? l? link v?i headers gi? l?p tr?nh duy?t"""
        headers = {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none"
        }
        
        try:
            async with session.get(task['link'], headers=headers, timeout=15, allow_redirects=True) as resp:
                return {
                    'success': resp.status == 200,
                    'status': resp.status,
                    'url': str(resp.url)
                }
        except asyncio.TimeoutError:
            return {'success': False, 'error': 'Timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def save_report(self, results):
        """L?u b?o c?o"""
        processed = len(results)
        succeeded = sum(1 for r in results if r.get('success'))
        failed = processed - succeeded
        
        report = {
            "processed": processed,
            "succeeded": succeeded,
            "failed": failed,
            "target": self.target_per_day,
            "start_time": self.start_time.isoformat(),
            "last_update": datetime.now().isoformat(),
            "success_rate": round(succeeded / processed * 100, 2) if processed > 0 else 0,
            "results": results
        }
        
        with open(self.report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    async def run(self):
        print("=" * 70)
        print(f"?? IMPROVED AUTO WORKER STARTED")
        print(f"?? Target: {self.target_per_day} tasks/day")
        print("=" * 70)
        
        # Load tasks
        try:
            with open('auto_strategy.json', 'r', encoding='utf-8') as f:
                content = f.read()
                if content.startswith('\ufeff'):
                    content = content[1:]
                strategy = json.loads(content)
        except Exception as e:
            print(f"? Error loading tasks: {e}")
            return
        
        tasks = strategy.get('tasks', [])
        if not tasks:
            print("? No tasks found")
            return
        
        print(f"?? Loaded {len(tasks)} tasks")
        print("?? Simulating browser requests with realistic headers...")
        
        results = []
        
        async with aiohttp.ClientSession() as session:
            for i, task in enumerate(tasks[:self.target_per_day], 1):
                print(f"\n?? [{i}/{min(self.target_per_day, len(tasks))}] {task.get('campaign', 'Unknown')}")
                
                result = await self.process_link(session, task)
                result['campaign'] = task.get('campaign')
                result['link'] = task['link']
                results.append(result)
                
                if result.get('success'):
                    print(f"   ? Status: {result.get('status')}")
                else:
                    print(f"   ? Failed: {result.get('error', f'HTTP {result.get(\"status\")}')}")
                
                # L?u sau m?i 3 tasks
                if i % 3 == 0:
                    self.save_report(results)
                
                await asyncio.sleep(random.uniform(1, 2))
        
        final_report = self.save_report(results)
        
        print("\n" + "=" * 70)
        print("? AUTO WORKER COMPLETED")
        print(f"   ?? Total: {final_report['processed']}")
        print(f"   ? Success: {final_report['succeeded']}")
        print(f"   ? Failed: {final_report['failed']}")
        print(f"   ?? Success rate: {final_report['success_rate']}%")
        print(f"   ?? Report: {self.report_file}")
        print("=" * 70)
        
        # Hi?n th? chi ti?t
        print("\n?? DETAILED RESULTS:")
        for r in results:
            status = "?" if r.get('success') else "?"
            print(f"   {status} {r['campaign'][:30]}: {r.get('status', r.get('error', 'N/A'))}")

async def main():
    worker = ImprovedAutoWorker(target_per_day=20)
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
