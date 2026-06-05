"""
Auto Worker - Fixed encoding
"""
import asyncio
import aiohttp
import json
import time
import random
from datetime import datetime
import os

class AutoWorker:
    def __init__(self, target_per_day=20):
        self.target_per_day = target_per_day
        self.start_time = datetime.now()
        self.session = None
        self.report_file = "auto_worker_report.json"
    
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    def save_report(self, processed, succeeded, failed):
        report = {
            "processed": processed,
            "succeeded": succeeded,
            "failed": failed,
            "target": self.target_per_day,
            "start_time": self.start_time.isoformat(),
            "last_update": datetime.now().isoformat(),
            "success_rate": round(succeeded / processed * 100, 2) if processed > 0 else 0
        }
        
        with open(self.report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    async def process_link(self, task):
        try:
            session = await self.get_session()
            async with session.get(task['link'], timeout=10) as resp:
                if resp.status == 200:
                    return {'success': True, 'status': resp.status}
                return {'success': False, 'status': resp.status}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def run_auto_worker(self):
        print("=" * 70)
        print(f"?? AUTO WORKER STARTED - Target: {self.target_per_day} tasks/day")
        print(f"?? Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Load tasks v?i encoding ??ng
        try:
            with open('auto_strategy.json', 'r', encoding='utf-8') as f:
                content = f.read()
                # Lo?i b? BOM n?u c?
                if content.startswith('\ufeff'):
                    content = content[1:]
                strategy = json.loads(content)
        except FileNotFoundError:
            print("? auto_strategy.json not found!")
            return
        except json.JSONDecodeError as e:
            print(f"? JSON error: {e}")
            print("?? Please check auto_strategy.json format")
            return
        
        tasks = strategy.get('tasks', [])
        
        if not tasks:
            print("? No tasks in auto_strategy.json")
            return
        
        print(f"?? Loaded {len(tasks)} tasks")
        
        processed = 0
        succeeded = 0
        failed = 0
        
        self.save_report(processed, succeeded, failed)
        
        for i, task in enumerate(tasks[:self.target_per_day]):
            processed += 1
            print(f"\n?? Task {processed}/{self.target_per_day}: {task.get('campaign', 'Unknown')}")
            print(f"   Link: {task['link'][:80]}...")
            
            result = await self.process_link(task)
            
            if result.get('success'):
                succeeded += 1
                print(f"   ? Success (Status: {result.get('status')})")
            else:
                failed += 1
                print(f"   ? Failed: {result.get('error', result.get('status', 'Unknown'))}")
            
            # L?u report sau m?i task
            self.save_report(processed, succeeded, failed)
            
            await asyncio.sleep(random.uniform(0.5, 1))
        
        final_report = self.save_report(processed, succeeded, failed)
        
        print("\n" + "=" * 70)
        print("? AUTO WORKER COMPLETED")
        print(f"   ?? Total: {final_report['processed']}")
        print(f"   ? Success: {final_report['succeeded']}")
        print(f"   ? Failed: {final_report['failed']}")
        print(f"   ?? Success rate: {final_report['success_rate']}%")
        print(f"   ?? Report: {self.report_file}")
        print("=" * 70)
        
        await self.close()
    
    async def close(self):
        if self.session:
            await self.session.close()

async def main():
    worker = AutoWorker(target_per_day=20)
    await worker.run_auto_worker()

if __name__ == "__main__":
    asyncio.run(main())
