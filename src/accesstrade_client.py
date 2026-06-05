"""
AccessTrade API Client - Working Endpoints
Based on successful tests: /v1/me and /v1/campaigns
"""
import aiohttp
import json
import os
from typing import Dict, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AccessTradeClient:
    def __init__(self, access_key: str = None):
        self.access_key = access_key or os.getenv("ACCESSTRADE_ACCESS_KEY")
        self.base_url = "https://api.accesstrade.vn/v1"
        self.session = None
        
    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    def _get_headers(self):
        return {
            "Authorization": f"Token {self.access_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def get_publisher_info(self) -> Dict:
        """Lấy thông tin publisher (endpoint: /v1/me)"""
        url = f"{self.base_url}/me"
        
        session = await self._get_session()
        
        try:
            async with session.get(url, headers=self._get_headers()) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('data', {})
                else:
                    return {"error": f"HTTP {resp.status}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_campaigns(self, limit: int = 20, page: int = 1, 
                           category: str = None, keyword: str = None) -> Dict:
        """Lấy danh sách campaigns (endpoint: /v1/campaigns)"""
        url = f"{self.base_url}/campaigns"
        params = {
            "limit": limit,
            "page": page,
            "sort": "-commission"
        }
        if category:
            params["category"] = category
        if keyword:
            params["keyword"] = keyword
        
        session = await self._get_session()
        
        try:
            async with session.get(url, params=params, headers=self._get_headers()) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {
                        "success": True,
                        "data": data.get('data', []),
                        "total": len(data.get('data', []))
                    }
                else:
                    return {"success": False, "error": f"HTTP {resp.status}", "data": []}
        except Exception as e:
            return {"success": False, "error": str(e), "data": []}
    
    async def get_campaign_detail(self, campaign_id: int) -> Dict:
        """Lấy chi tiết campaign"""
        url = f"{self.base_url}/campaigns/{campaign_id}"
        
        session = await self._get_session()
        
        try:
            async with session.get(url, headers=self._get_headers()) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {"error": f"HTTP {resp.status}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_affiliate_links(self, campaign_id: int, url: str, 
                                   tracking_id: str = None) -> Dict:
        """Tạo affiliate link cho campaign"""
        api_url = f"{self.base_url}/affiliate/links"
        
        data = {
            "campaignId": campaign_id,
            "url": url
        }
        if tracking_id:
            data["trackingId"] = tracking_id
        
        session = await self._get_session()
        
        try:
            async with session.post(api_url, json=data, headers=self._get_headers()) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {"error": f"HTTP {resp.status}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_categories(self) -> List[Dict]:
        """Lấy danh sách categories"""
        url = f"{self.base_url}/categories"
        
        session = await self._get_session()
        
        try:
            async with session.get(url, headers=self._get_headers()) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('data', [])
                else:
                    return []
        except Exception as e:
            return []
    
    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None


_accesstrade_client = None


async def get_accesstrade_client() -> AccessTradeClient:
    global _accesstrade_client
    if _accesstrade_client is None:
        _accesstrade_client = AccessTradeClient()
    return _accesstrade_client


async def close_accesstrade_client():
    global _accesstrade_client
    if _accesstrade_client:
        await _accesstrade_client.close()
        _accesstrade_client = None
