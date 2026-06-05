# src/utils/helpers.py
"""
Utility functions cho toàn hệ thống
"""

import re
import hashlib
import secrets
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json

def generate_api_key() -> str:
    """Tạo API key ngẫu nhiên"""
    return secrets.token_urlsafe(32)

def hash_string(text: str) -> str:
    """Hash một string bằng SHA256"""
    return hashlib.sha256(text.encode()).hexdigest()

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format số tiền"""
    return f"{currency} {amount:,.2f}"

def calculate_percentage(value: float, total: float) -> float:
    """Tính phần trăm"""
    if total == 0:
        return 0.0
    return (value / total) * 100

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Cắt ngắn text"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def safe_parse_json(json_string: str) -> Optional[Dict[str, Any]]:
    """Parse JSON an toàn, trả về None nếu lỗi"""
    try:
        return json.loads(json_string)
    except:
        return None

def calculate_token_cost(prompt_length: int, task_type: str) -> int:
    """Tính toán chi phí token dựa trên độ dài prompt và loại task"""
    # Base cost
    base_cost = 1000
    
    # Task type multiplier
    multipliers = {
        "content_facebook": 1.5,
        "video_tiktok": 2.0,
        "scrape_deal": 1.2,
        "seo_article": 1.8,
        "default": 1.0
    }
    
    multiplier = multipliers.get(task_type, 1.0)
    
    # Prompt length factor
    length_factor = min(3.0, max(0.5, prompt_length / 500))
    
    return int(base_cost * multiplier * length_factor)

def get_date_range(days: int = 30) -> tuple:
    """Lấy khoảng thời gian từ days trước đến hiện tại"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def mask_email(email: str) -> str:
    """Mask email để bảo vệ privacy"""
    if not email:
        return ""
    parts = email.split('@')
    if len(parts) != 2:
        return email
    username, domain = parts
    if len(username) <= 2:
        masked_username = username[0] + "*" * (len(username) - 1)
    else:
        masked_username = username[0] + "*" * (len(username) - 2) + username[-1]
    return f"{masked_username}@{domain}"

def generate_referral_code(user_id: int) -> str:
    """Tạo mã giới thiệu cho user"""
    return f"SEN{user_id}{secrets.token_hex(3).upper()}"

class Timer:
    """Context manager để đo thời gian thực thi"""
    def __init__(self, name: str = "Operation"):
        self.name = name
        
    def __enter__(self):
        self.start = time.time()
        return self
        
    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start
        logger.info(f"⏱️ {self.name} took {self.interval:.3f} seconds")