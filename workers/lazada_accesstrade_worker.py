"""
Lazada + AccessTrade Worker
"""
import asyncio
import json
import sqlite3
from typing import Dict, List
from datetime import datetime
from pathlib import Path
import logging

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lazada_client import LazadaClient
from src.task_queue_db import get_task_queue, update_task_status

logger = logging.getLogger(__name__)


class LazadaAccessTradeWorker:
    def __init__(self, worker_id: str = "lazada_worker_1"):
        self.worker_id = worker_id
        self.running = False
        self.lazada_client = None
    
    async def get_lazada_client(self):
        if self.lazada_client is None:
            self.lazada_client = LazadaClient()
        return self.lazada_client
    
    async def process_task(self, task: Dict) -> Dict:
        task_type = task.get("task_type")
        data = task.get("data", {})
        
        if task_type == "fetch_lazada_products":
            return await self._fetch_product(data)
        elif task_type == "search_lazada_products":
            return await self._search_products(data)
        elif task_type == "create_lazada_promotion":
            return await self._create_promotion(data)
        else:
            return {"error": f"Unknown task type: {task_type}"}
    
    async def _fetch_product(self, data: Dict) -> Dict:
        sku = data.get("sku")
        if not sku:
            return {"error": "No SKU provided"}
        
        client = await self.get_lazada_client()
        result = await client.get_product_by_sku(sku)
        
        if result.get("success"):
            product = result["data"]
            affiliate_link = await client.generate_affiliate_link(sku)
            product["affiliate_link"] = affiliate_link
            
            # Save to database
            await self._save_product(product)
            
            return {"success": True, "product": product}
        return result
    
    async def _search_products(self, data: Dict) -> Dict:
        keyword = data.get("keyword")
        if not keyword:
            return {"error": "No keyword provided"}
        
        client = await self.get_lazada_client()
        return await client.search_products(keyword, data.get("limit", 20))
    
    async def _create_promotion(self, data: Dict) -> Dict:
        sku = data.get("sku")
        if not sku:
            return {"error": "No SKU provided"}
        
        client = await self.get_lazada_client()
        result = await client.get_product_by_sku(sku)
        
        if result.get("success"):
            promotion = {
                "sku": sku,
                "product_name": result["data"].get("name"),
                "price": result["data"].get("price"),
                "affiliate_link": await client.generate_affiliate_link(sku),
                "created_at": datetime.now().isoformat(),
                "type": data.get("promo_type", "standard")
            }
            
            # Save promotion
            conn = sqlite3.connect("sen_v3.db")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS lazada_promotions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sku TEXT,
                    promotion_data TEXT,
                    created_at TIMESTAMP
                )
            """)
            conn.execute(
                "INSERT INTO lazada_promotions (sku, promotion_data, created_at) VALUES (?, ?, ?)",
                (sku, json.dumps(promotion), promotion["created_at"])
            )
            conn.commit()
            conn.close()
            
            return {"success": True, "promotion": promotion}
        return result
    
    async def _save_product(self, product: Dict):
        conn = sqlite3.connect("sen_v3.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS lazada_products (
                sku TEXT PRIMARY KEY,
                name TEXT,
                price TEXT,
                url TEXT,
                affiliate_link TEXT,
                fetched_at TIMESTAMP
            )
        """)
        conn.execute(
            "INSERT OR REPLACE INTO lazada_products VALUES (?, ?, ?, ?, ?, ?)",
            (
                product.get("sku"),
                product.get("name"),
                product.get("price"),
                product.get("url"),
                product.get("affiliate_link"),
                product.get("fetched_at")
            )
        )
        conn.commit()
        conn.close()
    
    async def run(self):
        self.running = True
        logger.info(f"Worker {self.worker_id} started")
        
        while self.running:
            try:
                task = get_task_queue().get_next_task(worker_id=self.worker_id)
                
                if task:
                    logger.info(f"Processing task {task['id']}")
                    update_task_status(task['id'], "processing", worker_id=self.worker_id)
                    
                    result = await self.process_task(task)
                    
                    update_task_status(task['id'], "completed", result=result)
                    logger.info(f"Task {task['id']} completed")
                else:
                    await asyncio.sleep(3)
            except Exception as e:
                logger.error(f"Worker error: {e}")
                await asyncio.sleep(5)
        
        if self.lazada_client:
            await self.lazada_client.close()
    
    def stop(self):
        self.running = False


async def create_test_tasks():
    task_queue = get_task_queue()
    
    # Test with your SKU
    task_queue.add_task(
        task_type="fetch_lazada_products",
        data={"sku": "AN273FAAA1FXLXVNAMZ-2293380"},
        priority=1
    )
    
    task_queue.add_task(
        task_type="create_lazada_promotion",
        data={"sku": "AN273FAAA1FXLXVNAMZ-2293380", "promo_type": "hot_deal"},
        priority=2
    )
    
    print("✅ Test tasks created")
