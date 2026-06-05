# src/middleware/token_manager.py
"""
Quản lý Token và Rate Limiting cho Gemini API
Tích hợp Core Upgrade
"""

import re
from typing import Dict
from src.db.models import User


class TokenManager:
    """Quản lý token consumption và estimation"""
    
    # Mapping task type -> average tokens per request
    TOKEN_ESTIMATES = {
        "video_tiktok": 5000,
        "content_facebook": 3000,
        "scrape_deal": 2000,
        "seo_article": 4000,
        "email_marketing": 2500,
        "default": 2000
    }
    
    def estimate_tokens_from_prompt(self, prompt: str, task_type: str = "default") -> int:
        """
        Ước tính số token cần dùng dựa trên:
        - Độ dài prompt
        - Loại task
        - Độ phức tạp
        """
        # Base tokens from task type
        base_tokens = self.TOKEN_ESTIMATES.get(task_type, self.TOKEN_ESTIMATES["default"])
        
        # Additional tokens based on prompt length
        prompt_length = len(prompt)
        length_factor = min(2.0, max(0.5, prompt_length / 1000))  # Giới hạn 0.5x - 2x
        
        # Complexity factor (dựa trên số câu hỏi, từ khóa đặc biệt)
        complexity = 1.0
        if "?" in prompt:
            complexity += 0.2  # Có câu hỏi -> cần trả lời chi tiết hơn
        if any(keyword in prompt.lower() for keyword in ["analyze", "compare", "explain", "detail"]):
            complexity += 0.3
            
        estimated = int(base_tokens * length_factor * complexity)
        
        # Giới hạn an toàn
        return min(10000, max(500, estimated))
    
    def check_token_quota(self, user: User, required_tokens: int) -> bool:
        """Kiểm tra xem user có đủ token không"""
        return user.available_tokens >= required_tokens
    
    def deduct_tokens(self, user: User, tokens: int) -> bool:
        """Trừ token của user (KHÔNG commit DB)"""
        if self.check_token_quota(user, tokens):
            user.tokens_used += tokens
            return True
        return False
    
    def get_token_usage_stats(self, user: User) -> Dict:
        """Lấy thống kê sử dụng token"""
        return {
            "quota": user.token_quota,
            "used": user.tokens_used,
            "available": user.available_tokens,
            "usage_percent": user.token_usage_percent,
            "remaining_percent": 100 - user.token_usage_percent
        }