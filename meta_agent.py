"""
Meta Agent HA - High Availability với Leader Election
"""
import asyncio
import logging
import os
import json
from datetime import datetime
from typing import Optional
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetaAgentHA:
    def __init__(self):
        self.is_leader = False
        self.running = True
        self.leader_key = "sen_v3:leader"
        self.leader_ttl = 30  # seconds
    
    async def acquire_leadership(self) -> bool:
        """Tranh giành leadership"""
        try:
            import redis
            redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
            result = redis_client.setnx(self.leader_key, os.getpid())
            if result:
                redis_client.expire(self.leader_key, self.leader_ttl)
                return True
            return False
        except:
            # Fallback: nếu không có Redis, dùng SQLite
            return await self._acquire_leadership_sqlite()
    
    async def _acquire_leadership_sqlite(self) -> bool:
        """Fallback leadership với SQLite"""
        try:
            conn = sqlite3.connect('sen_v3.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS leader_election (
                    key TEXT PRIMARY KEY,
                    leader_id TEXT,
                    expires_at TIMESTAMP
                )
            ''')
            
            # Xóa key hết hạn
            cursor.execute('DELETE FROM leader_election WHERE expires_at < ?', (datetime.now().isoformat(),))
            
            # Thử insert
            try:
                cursor.execute('''
                    INSERT INTO leader_election (key, leader_id, expires_at)
                    VALUES (?, ?, ?)
                ''', ('leader', str(os.getpid()), datetime.now().isoformat()))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
            finally:
                conn.close()
        except Exception as e:
            logger.error(f"SQLite leadership error: {e}")
            return False
    
    async def renew_leadership(self):
        """Gia hạn leadership"""
        try:
            import redis
            redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
            redis_client.expire(self.leader_key, self.leader_ttl)
        except:
            conn = sqlite3.connect('sen_v3.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE leader_election 
                SET expires_at = ? 
                WHERE key = 'leader' AND leader_id = ?
            ''', (datetime.now().isoformat(), str(os.getpid())))
            conn.commit()
            conn.close()
    
    async def leader_loop(self):
        """Leader election loop"""
        while self.running:
            try:
                if not self.is_leader:
                    self.is_leader = await self.acquire_leadership()
                    if self.is_leader:
                        logger.info("👑 Became LEADER!")
                    else:
                        logger.debug("Standby mode (not leader)")
                else:
                    await self.renew_leadership()
                
                await asyncio.sleep(10)
            except Exception as e:
                logger.error(f"Leader loop error: {e}")
                await asyncio.sleep(5)
    
    async def work_loop(self):
        """Work loop - chỉ chạy khi là leader"""
        while self.running:
            if self.is_leader:
                try:
                    # Đây là nơi xử lý công việc chính
                    logger.debug("Processing work as leader...")
                    await asyncio.sleep(5)
                except Exception as e:
                    logger.error(f"Work loop error: {e}")
            else:
                await asyncio.sleep(2)
    
    async def health_server(self):
        """Simple HTTP health server"""
        from aiohttp import web
        
        async def handle_health(request):
            return web.json_response({
                "status": "healthy",
                "is_leader": self.is_leader,
                "timestamp": datetime.now().isoformat()
            })
        
        async def handle_circuits(request):
            try:
                from circuit_breaker import circuit_registry
                return web.json_response(circuit_registry.get_all_states())
            except:
                return web.json_response({"error": "Circuit breaker not available"})
        
        app = web.Application()
        app.router.add_get('/health', handle_health)
        app.router.add_get('/health/circuits', handle_circuits)
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8080)
        await site.start()
        logger.info("🏥 Health server started on http://localhost:8080")
        
        while self.running:
            await asyncio.sleep(1)
    
    async def start(self):
        """Start meta agent"""
        logger.info("🚀 Meta Agent HA starting...")
        
        try:
            await asyncio.gather(
                self.leader_loop(),
                self.work_loop(),
                self.health_server()
            )
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            self.running = False


async def main():
    agent = MetaAgentHA()
    await agent.start()


if __name__ == "__main__":
    asyncio.run(main())
