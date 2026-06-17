"""
Dead Letter Monitor - Giám sát và alert khi queue tràn
"""
import asyncio
import logging
import os
from datetime import datetime
from typing import Optional
import aiohttp

logger = logging.getLogger(__name__)


class DeadLetterMonitor:
    def __init__(self, telegram_bot_token: str = None, telegram_chat_id: str = None):
        self.telegram_bot_token = telegram_bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = telegram_chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.threshold = 10  # Ngưỡng cảnh báo
        self.cooldown_minutes = 5
        self.last_alert_time = {}
        self.running = True
    
    async def send_telegram_alert(self, message: str):
        """Gửi alert qua Telegram"""
        if not self.telegram_bot_token or not self.telegram_chat_id:
            logger.warning("Telegram credentials missing")
            return
        
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        data = {
            "chat_id": self.telegram_chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as resp:
                    if resp.status == 200:
                        logger.info(f"Alert sent: {message[:50]}...")
                    else:
                        logger.error(f"Failed to send alert: {resp.status}")
        except Exception as e:
            logger.error(f"Telegram error: {e}")
    
    async def check_dead_letter(self):
        """Kiểm tra dead letter queue"""
        try:
            import sqlite3
            conn = sqlite3.connect('sen_v3.db')
            cursor = conn.cursor()
            
            # Kiểm tra bảng dead_letter
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dead_letter'")
            if cursor.fetchone():
                cursor.execute("SELECT COUNT(*) FROM dead_letter WHERE status = 'pending'")
                count = cursor.fetchone()[0]
                
                if count > self.threshold:
                    alert_key = "dead_letter"
                    last_alert = self.last_alert_time.get(alert_key, 0)
                    
                    if (datetime.now().timestamp() - last_alert) > self.cooldown_minutes * 60:
                        await self.send_telegram_alert(
                            f"⚠️ <b>Dead Letter Queue Alert</b>\n"
                            f"📊 Pending items: {count}\n"
                            f"🔧 Threshold: {self.threshold}\n"
                            f"💡 Please check the system immediately!"
                        )
                        self.last_alert_time[alert_key] = datetime.now().timestamp()
            
            conn.close()
        except Exception as e:
            logger.error(f"Check dead letter error: {e}")
    
    async def check_circuit_breakers(self):
        """Kiểm tra circuit breaker states"""
        try:
            from circuit_breaker import circuit_registry
            states = circuit_registry.get_all_states()
            
            for name, state in states.items():
                if state.get('state') == 'open':
                    alert_key = f"circuit_{name}"
                    last_alert = self.last_alert_time.get(alert_key, 0)
                    
                    if (datetime.now().timestamp() - last_alert) > self.cooldown_minutes * 60:
                        await self.send_telegram_alert(
                            f"🔌 <b>Circuit Breaker OPEN</b>\n"
                            f"📛 Name: {name}\n"
                            f"❌ Failures: {state.get('failure_count')}\n"
                            f"⏰ Duration: {state.get('state_duration_seconds'):.0f}s"
                        )
                        self.last_alert_time[alert_key] = datetime.now().timestamp()
        except Exception as e:
            logger.error(f"Check circuits error: {e}")
    
    async def check_worker_health(self):
        """Kiểm tra sức khỏe workers"""
        try:
            import psutil
            import subprocess
            
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                                   capture_output=True, text=True)
            worker_count = result.stdout.count('python.exe')
            
            if worker_count == 0:
                alert_key = "no_workers"
                last_alert = self.last_alert_time.get(alert_key, 0)
                
                if (datetime.now().timestamp() - last_alert) > self.cooldown_minutes * 60:
                    await self.send_telegram_alert(
                        "🚨 <b>CRITICAL: No workers running!</b>\n"
                        "System may be down. Please check immediately!"
                    )
                    self.last_alert_time[alert_key] = datetime.now().timestamp()
        except Exception as e:
            logger.error(f"Check workers error: {e}")
    
    async def start(self):
        """Start monitoring loop"""
        logger.info("📊 Dead Letter Monitor started")
        
        while self.running:
            try:
                await self.check_dead_letter()
                await self.check_circuit_breakers()
                await self.check_worker_health()
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Monitor loop error: {e}")
                await asyncio.sleep(60)
    
    def stop(self):
        self.running = False
