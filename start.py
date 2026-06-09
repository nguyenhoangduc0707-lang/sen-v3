#!/usr/bin/env python3
"""
SEN V3 Unified Launcher - Fixed version
Usage:
    python start.py api
    python start.py worker --type facebook
    python start.py scheduler
    python start.py all
"""

import sys
import os
import asyncio
import subprocess
import argparse
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def cmd_api(host="0.0.0.0", port=8001, reload=False):
    """Start API server - FIXED version"""
    print(f"🚀 Server starting at http://{host}:{port}")
    import uvicorn
    
    # Fix: Use uvicorn.run directly (not asyncio.run inside asyncio)
    config = uvicorn.Config("web.main:app", host=host, port=port, reload=reload, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

def cmd_worker(worker_type="facebook"):
    """Start a worker"""
    print(f"🔧 Starting worker: {worker_type}")
    
    if worker_type == "facebook":
        os.system("python -m src.workers.facebook_worker")
    elif worker_type == "affiliate":
        os.system("python -m src.workers.affiliate_worker")
    elif worker_type == "shopee":
        os.system("python -m src.workers.shopee_worker")
    else:
        print(f"Unknown worker type: {worker_type}")

def cmd_scheduler():
    """Start scheduler"""
    print("⏰ Starting scheduler...")
    os.system("python -m src.workers.scheduler_worker")

async def cmd_all():
    """Start everything"""
    print("🚀 Starting ALL (API + workers + scheduler)")
    
    # Start API in background
    import uvicorn
    import threading
    
    def run_api():
        uvicorn.run("web.main:app", host="0.0.0.0", port=8001)
    
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Give API time to start
    await asyncio.sleep(2)
    
    # Start workers in background processes
    processes = []
    
    # Facebook worker
    p = subprocess.Popen([sys.executable, "-m", "src.workers.facebook_worker"])
    processes.append(p)
    
    # Affiliate worker
    p = subprocess.Popen([sys.executable, "-m", "src.workers.affiliate_worker"])
    processes.append(p)
    
    # Scheduler
    p = subprocess.Popen([sys.executable, "-m", "src.workers.scheduler_worker"])
    processes.append(p)
    
    print("✅ All components started. Press Ctrl+C to stop.")
    
    try:
        # Wait for all processes
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping all components...")
        for p in processes:
            p.terminate()
        print("✅ All stopped")

def main():
    parser = argparse.ArgumentParser(description='SEN V3 Launcher')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # API command
    api_parser = subparsers.add_parser('api', help='Start API server')
    api_parser.add_argument('--host', default='0.0.0.0')
    api_parser.add_argument('--port', type=int, default=8001)
    api_parser.add_argument('--reload', action='store_true')
    
    # Worker command
    worker_parser = subparsers.add_parser('worker', help='Start a worker')
    worker_parser.add_argument('--type', choices=['facebook', 'affiliate', 'shopee'], default='facebook')
    
    # Scheduler command
    subparsers.add_parser('scheduler', help='Start scheduler')
    
    # All command
    subparsers.add_parser('all', help='Start all components')
    
    args = parser.parse_args()
    
    if args.command == 'api':
        asyncio.run(cmd_api(host=args.host, port=args.port, reload=args.reload))
    elif args.command == 'worker':
        cmd_worker(worker_type=args.type)
    elif args.command == 'scheduler':
        cmd_scheduler()
    elif args.command == 'all':
        asyncio.run(cmd_all())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
