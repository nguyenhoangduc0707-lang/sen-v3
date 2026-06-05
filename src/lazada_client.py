"""
Lazada API Client - Lấy thông tin sản phẩm từ Lazada
"""
import aiohttp
import asyncio
import json
import re
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import logging
import hashlib
import time

logger = logging.getLogger(__name__)

# Load config
CONFIG_PATH = Path(__file__).parent.parent / "config" / "lazada_config.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    LAZADA_CONFIG = json.load(f)


class LazadaClient:
    """Client để lấy thông tin sản phẩm từ Lazada"""
    
    def __init__(self, domain: str = None):
        self.domain = domain or LAZADA_CONFIG["default_domain"]
        self.base_url = f"https://{self.domain}"
        self.session = None
        self.user_agents = LAZADA_CONFIG["scraping_settings"]["user_agents"]
        self.current_ua_index = 0
        
    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    def _get_user_agent(self) -> str:
        self.current_ua_index = (self.current_ua_index + 1) % len(self.user_agents)
        return self.user_agents[self.current_ua_index]
    
    async def get_product_by_sku(self, sku: str, domain: str = None) -> Dict:
        """Lấy thông tin sản phẩm từ SKU"""
        domain = domain or self.domain
        product_url = f"https://{domain}/products/{sku}"
        
        headers = {
            "User-Agent": self._get_user_agent(),
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
        }
        
        session = await self._get_session()
        
        try:
            async with session.get(product_url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    html = await response.text()
                    product_info = await self._parse_product_html(html, sku, domain)
                    return {"success": True, "data": product_info}
                else:
                    return {"success": False, "error": f"HTTP {response.status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _parse_product_html(self, html: str, sku: str, domain: str) -> Dict:
        """Parse HTML để extract thông tin sản phẩm"""
        product_info = {
            "sku": sku,
            "domain": domain,
            "url": f"https://{domain}/products/{sku}",
            "fetched_at": datetime.now().isoformat(),
            "source": "lazada"
        }
        
        # Extract JSON-LD data
        json_ld_pattern = r'<script type="application/ld\+json">(.*?)</script>'
        matches = re.findall(json_ld_pattern, html, re.DOTALL)
        
        for json_str in matches:
            try:
                data = json.loads(json_str)
                if data.get("@type") == "Product":
                    product_info["name"] = data.get("name", "")
                    product_info["price"] = data.get("offers", {}).get("price")
                    product_info["price_currency"] = data.get("offers", {}).get("priceCurrency", "VND")
                    product_info["images"] = data.get("image", [])
                    break
            except:
                continue
        
        # Fallback: extract from title
        if not product_info.get("name"):
            title_match = re.search(r'<title>(.*?)</title>', html)
            if title_match:
                title = title_match.group(1).replace("| Lazada.vn", "").strip()
                product_info["name"] = title
        
        # Fallback: extract price
        if not product_info.get("price"):
            price_match = re.search(r'<span[^>]*class="pdp-price"[^>]*>.*?(\d+(?:[.,]\d+)?)', html)
            if price_match:
                product_info["price"] = price_match.group(1)
        
        if not product_info.get("name"):
            product_info["name"] = f"Product {sku}"
        if not product_info.get("price"):
            product_info["price"] = "N/A"
        
        return product_info
    
    async def search_products(self, keyword: str, limit: int = 20) -> Dict:
        """Tìm kiếm sản phẩm theo từ khóa"""
        search_url = f"https://{self.domain}/catalog/ajax"
        params = {"q": keyword, "limit": limit}
        
        headers = {
            "User-Agent": self._get_user_agent(),
            "X-Requested-With": "XMLHttpRequest"
        }
        
        session = await self._get_session()
        
        try:
            async with session.get(search_url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    products = []
                    for item in data.get("mods", {}).get("listItems", []):
                        products.append({
                            "sku": item.get("itemSku"),
                            "name": item.get("name"),
                            "price": item.get("price"),
                            "url": f"https://{self.domain}{item.get('productUrl', '')}"
                        })
                    return {"success": True, "products": products, "total": len(products)}
                return {"success": False, "error": f"HTTP {response.status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def generate_affiliate_link(self, sku: str) -> str:
        """Tạo affiliate link từ sản phẩm"""
        return f"https://s.lazada.vn/{sku}?utm_source=sen_v3"
    
    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None
