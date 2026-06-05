"""
content_creation_agent.py  —  SEN V3 (Groq edition) – Fixed event loop
"""
import os
import random
import time
import asyncio
import functools
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# ========== RATE LIMIT GUARD ==========
class RateLimitGuard:
    def __init__(self, max_per_minute: int = 25):
        self.max_rpm = max_per_minute
        self._timestamps: List[float] = []
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.time()
            self._timestamps = [t for t in self._timestamps if now - t < 60]
            if len(self._timestamps) >= self.max_rpm:
                wait = 61 - (now - self._timestamps[0])
                logger.warning(f"[RateLimit] Đạt {self.max_rpm} req/min, chờ {wait:.1f}s")
                await asyncio.sleep(wait)
            self._timestamps.append(time.time())

_groq_rate_guard = RateLimitGuard(max_per_minute=25)

class _NoRetryError(Exception):
    pass

def async_retry(max_attempts: int = 3, base_delay: float = 2.0):
    def decorator(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await fn(*args, **kwargs)
                except _NoRetryError:
                    raise
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                    logger.warning(f"[Retry] lần {attempt+1} thất bại: {e} — chờ {delay:.1f}s")
                    await asyncio.sleep(delay)
        return wrapper
    return decorator

# ========== CACHE ==========
_cache: Dict[str, tuple] = {}
CACHE_TTL = 3600

def _cache_key(campaign: Dict) -> str:
    comm_val = campaign.get('commission_value', 0)
    comm_type = campaign.get('commission_type', 'percent')
    return f"{campaign.get('name','')}|{comm_type}|{comm_val}"

def _cache_get(campaign: Dict):
    key = _cache_key(campaign)
    if key in _cache:
        content, ts = _cache[key]
        if time.time() - ts < CACHE_TTL:
            logger.debug(f"[Cache] HIT: {key}")
            return content
        del _cache[key]
    return None

def _cache_set(campaign: Dict, content: str):
    key = _cache_key(campaign)
    _cache[key] = (content, time.time())

# ========== FALLBACK ==========
def create_article_fallback(campaign: Dict[str, Any]) -> str:
    name = campaign.get("name", "Sản phẩm")
    comm_display = campaign.get("commission_display", "0%")
    templates = [
        f"🔥 Hót hòn họt: {name} – cơ hội kiếm tiền khủng với hoa hồng {comm_display}.",
        f"🌟 Siêu sale! {name} hoa hồng lên tới {comm_display}. Mua ngay kẻo lỡ!",
        f"💸 Thu nhập thụ động với {name} – nhận ngay {comm_display} cho mỗi đơn.",
        f"🚀 Đã có {name} – cơ hội affiliate không thể bỏ lỡ, hoa hồng {comm_display}.",
        f"🎯 Chốt đơn dễ dàng cùng {name}, hưởng hoa hồng {comm_display} cực đã.",
    ]
    return random.choice(templates)

# ========== GROQ ==========
@async_retry(max_attempts=3, base_delay=2.0)
async def _call_groq(prompt: str) -> str:
    from groq import Groq

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key or not api_key.startswith("gsk_"):
        raise _NoRetryError("GROQ_API_KEY chưa set hoặc sai format (phải bắt đầu bằng gsk_)")

    await _groq_rate_guard.acquire()

    client = Groq(api_key=api_key)
    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia viết content marketing affiliate tiếng Việt. Viết ngắn gọn, hấp dẫn, có emoji, kêu gọi hành động mạnh. Chỉ trả về nội dung, không giải thích."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=200,
        )
    except Exception as e:
        err = str(e)
        if "invalid_api_key" in err.lower() or "401" in err:
            raise _NoRetryError(f"GROQ_API_KEY không hợp lệ: {err}")
        if "rate_limit" in err.lower() or "429" in err:
            logger.warning("[Groq] Rate limit, chờ 10s rồi retry...")
            await asyncio.sleep(10)
            raise
        raise
    text = response.choices[0].message.content.strip()
    if not text:
        raise ValueError("Groq trả về nội dung rỗng")
    return text

async def create_article_groq_async(campaign: Dict[str, Any]) -> str:
    name = campaign.get("name", "Sản phẩm")
    comm_display = campaign.get("commission_display", "0%")
    desc = campaign.get("description", "")
    prompt = f"Viết 1-2 câu giới thiệu sản phẩm hấp dẫn cho affiliate marketing.\nSản phẩm: {name}\nHoa hồng: {comm_display}\nMô tả: {desc}\nYêu cầu: ngắn gọn, có emoji, nêu bật lợi ích, kêu gọi hành động."
    return await _call_groq(prompt)

async def create_article_async(campaign: Dict[str, Any]) -> Dict[str, Any]:
    cached = _cache_get(campaign)
    if cached:
        return {"content": cached, "provider": "cache", "cached": True}

    provider = "fallback"
    try:
        content = await create_article_groq_async(campaign)
        provider = "groq"
        logger.info(f"[ContentAgent] Groq OK — {len(content)} chars")
    except _NoRetryError as e:
        logger.warning(f"[ContentAgent] Groq bỏ qua: {e}")
        content = create_article_fallback(campaign)
    except Exception as e:
        logger.error(f"[ContentAgent] Groq thất bại: {e} — dùng fallback")
        content = create_article_fallback(campaign)

    _cache_set(campaign, content)
    return {"content": content, "provider": provider, "cached": False}

# ========== SYNC WRAPPER (using asyncio.run) ==========
def create_article(campaign_id_or_dict) -> str:
    if isinstance(campaign_id_or_dict, str):
        campaign = {"name": "Sản phẩm mẫu", "commission_display": "15%", "description": ""}
    else:
        campaign = campaign_id_or_dict

    try:
        result = asyncio.run(create_article_async(campaign))
        return result["content"]
    except Exception as e:
        logger.error(f"[ContentAgent] create_article lỗi: {e}")
        return create_article_fallback(campaign)

def create_article_with_params(campaign: Dict[str, Any], params: Dict[str, Any]) -> str:
    return create_article(campaign)