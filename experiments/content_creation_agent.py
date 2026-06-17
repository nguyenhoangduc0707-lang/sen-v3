"""
content_creation_agent.py  —  SEN V3 (Gemini/Groq edition) – Fixed event loop + real key support
"""
import os
import random
import time
import asyncio
import functools
import logging
from typing import Dict, Any, List

from dotenv import load_dotenv
load_dotenv()  # Load .env so GEMINI_API_KEY and GROQ_API_KEY are picked up even in direct python runs

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
    affiliate_link = campaign.get("affiliate_link", "https://your-affiliate-link.com")
    templates = [
        f"🔥 Siêu hot! {name} – hoa hồng cực khủng {comm_display}. Mua ngay tại {affiliate_link} để nhận deal tốt nhất! Sản phẩm chất lượng cao, nhiều người dùng hài lòng. #dealhot #affiliate #muangay",
        f"🌟 Cơ hội vàng: {name} với hoa hồng {comm_display}. Sở hữu ngay tại {affiliate_link} kẻo lỡ! Đừng bỏ lỡ cơ hội kiếm tiền thụ động này. #hotdeal #affiliate",
        f"💸 Kiếm tiền thụ động dễ dàng với {name} – hoa hồng {comm_display} mỗi đơn. Đặt hàng ngay: {affiliate_link} Sản phẩm uy tín, hỗ trợ tốt. #affiliate #kinhtien #deal",
        f"🚀 {name} đang giảm giá sốc! Hoa hồng {comm_display}. Click mua ngay {affiliate_link} để trải nghiệm ngay hôm nay. #sale #affiliate #muangay",
    ]
    return random.choice(templates)

# ========== GROQ ==========
@async_retry(max_attempts=3, base_delay=2.0)
async def _call_gemini(prompt: str) -> str:
    """Gọi Gemini (khuyến nghị cho PHASE 1) - hỗ trợ prompt nghiêm ngặt về link/CTA/hashtag"""
    import aiohttp
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key or not api_key.startswith("AIza"):
        raise _NoRetryError("GEMINI_API_KEY chưa set hoặc sai format (phải bắt đầu bằng AIza...)")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.65,
            "maxOutputTokens": 600,
            "topP": 0.9
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
                if not text:
                    raise ValueError("Gemini trả về nội dung rỗng")
                return text
            else:
                err = await resp.text()
                if "API_KEY_INVALID" in err or resp.status == 400:
                    raise _NoRetryError(f"GEMINI_API_KEY không hợp lệ")
                raise Exception(f"Gemini error {resp.status}: {err[:300]}")

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
    """Tạo content affiliate - ƯU TIÊN Gemini (nếu có key AIza...), fallback Groq."""
    name = campaign.get("name", "Sản phẩm")
    comm_display = campaign.get("commission_display", "0%")
    desc = campaign.get("description", "")
    affiliate_link = campaign.get("affiliate_link", "https://your-affiliate-link.com")

    prompt = f"""Viết bài giới thiệu sản phẩm {name} để đăng Facebook affiliate.

⚠️ YÊU CẦU BẮT BUỘC (không được thiếu):
1. Phải chèn link affiliate này đúng 1 lần: {affiliate_link}
2. Phải có CTA rõ ràng: "Mua ngay", "Đặt hàng ngay", "Sở hữu ngay tại link", "Click mua ngay"...
3. Phải có ít nhất 2-3 hashtags ở cuối: ví dụ #ten-san-pham #dealhot #muangay #affiliate
4. Độ dài: 150-350 từ (khoảng 4-8 dòng)
5. Ngôn ngữ: hấp dẫn, lợi ích rõ ràng, dùng emoji phù hợp (🔥🌟💸🚀)
6. Nêu bật hoa hồng {comm_display} nếu có.

Sản phẩm: {name}
Mô tả: {desc}

Chỉ trả về nội dung bài đăng, không giải thích thêm."""

    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if gemini_key and gemini_key.startswith("AIza"):
        try:
            return await _call_gemini(prompt)
        except _NoRetryError as e:
            logger.warning(f"[Gemini] Key lỗi, thử Groq: {e}")
        except Exception as e:
            logger.warning(f"[Gemini] Thất bại, fallback Groq: {e}")

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

async def llm_health_check() -> Dict[str, Any]:
    """Simple LLM health check for SEN V3 monitoring. Returns status and provider."""
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    groq_key = os.environ.get("GROQ_API_KEY", "").strip()
    if gemini_key and gemini_key.startswith("AIza"):
        return {"status": "ok", "provider": "gemini", "message": "Gemini key present"}
    elif groq_key and groq_key.startswith("gsk_"):
        return {"status": "ok", "provider": "groq", "message": "Groq key present"}
    else:
        return {"status": "degraded", "provider": "fallback", "message": "No LLM key, using fallback templates"}

# ========== ASYNC-FIRST ENTRY POINT (FIXED for event loop) ==========
async def create_article_async(campaign: Dict[str, Any], theme: str = "affiliate") -> Dict[str, Any]:
    """
    Async version - preferred for modern async code (ContentWorker, etc.)
    This fixes the 'asyncio.run() cannot be called from a running event loop' error.
    """
    if theme == "motivational":
        try:
            return await create_motivational_async(campaign)
        except Exception as e:
            logger.error(f"[ContentAgent] motivational lỗi: {e}")
            return {"content": create_motivational_fallback(campaign), "provider": "fallback"}
    elif theme == "banking":
        try:
            return await create_banking_async(campaign)
        except Exception as e:
            logger.error(f"[ContentAgent] banking lỗi: {e}")
            return {"content": create_banking_fallback(campaign), "provider": "fallback"}
    elif theme == "ai_tech":
        try:
            return await create_ai_tech_async(campaign)
        except Exception as e:
            logger.error(f"[ContentAgent] ai_tech lỗi: {e}")
            return {"content": create_ai_tech_fallback(campaign), "provider": "fallback"}
    else:
        # default affiliate - use Groq with strong prompt
        try:
            return await create_article_groq_async(campaign)
        except Exception as e:
            logger.error(f"[ContentAgent] create_article_async lỗi: {e}")
            return {"content": create_article_fallback(campaign), "provider": "fallback"}


# ========== ASYNC ENTRYPOINT (refactored - no asyncio.run in async context) ==========
async def create_article(campaign_id_or_dict, theme: str = "affiliate") -> str:
    """Async entrypoint for content creation. Use this in async code (workers, etc.)."""
    if isinstance(campaign_id_or_dict, str):
        campaign = {"name": "Sản phẩm mẫu", "commission_display": "15%", "description": ""}
    else:
        campaign = campaign_id_or_dict

    try:
        result = await create_article_async(campaign, theme=theme)
        return result.get("content", create_article_fallback(campaign))
    except Exception as e:
        logger.error(f"[ContentAgent] create_article lỗi: {e}")
        return create_article_fallback(campaign)

# Legacy sync wrapper kept for backward compat (e.g. old scripts)
def create_article_sync(campaign_id_or_dict, theme: str = "affiliate") -> str:
    """Sync wrapper - only for non-async legacy code. Avoid in new async paths."""
    import asyncio
    try:
        return asyncio.run(create_article(campaign_id_or_dict, theme=theme))
    except Exception as e:
        logger.error(f"[ContentAgent] create_article_sync lỗi: {e}")
        if isinstance(campaign_id_or_dict, str):
            campaign = {"name": "Sản phẩm mẫu", "commission_display": "15%", "description": ""}
        else:
            campaign = campaign_id_or_dict
        return create_article_fallback(campaign)


# ========== MOTIVATIONAL / POSTCARD THEME ==========
def create_motivational_fallback(campaign: Dict[str, Any]) -> str:
    name = campaign.get("name", "Cuộc Sống")
    templates = [
        f"🌸 Hôm nay, hãy nhớ rằng bạn xứng đáng được hạnh phúc. {name} – một lời nhắc nhở nhỏ cho tâm hồn.",
        f"💫 Đừng vội vàng, hãy chậm lại một chút để cảm nhận cuộc sống. Mỗi ngày là một cơ hội mới.",
        f"❤️ Tình yêu bản thân là khởi nguồn của mọi điều tốt đẹp. Hãy yêu thương chính mình nhiều hơn.",
        f"🌟 Dù khó khăn đến đâu, hãy tin rằng bạn mạnh mẽ hơn những gì bạn nghĩ. Tiếp tục bước tiếp nhé!",
        f"✨ Cuộc sống không phải là đích đến, mà là hành trình. Hãy tận hưởng từng khoảnh khắc nhỏ bé."
    ]
    return random.choice(templates)

async def create_motivational_async(campaign: Dict[str, Any]) -> Dict[str, Any]:
    topic = campaign.get("name", "Cuộc Sống")
    desc = campaign.get("description", "truyền động lực và tình cảm")
    prompt = f"""Viết một bài đăng phong cách postcard tình cảm, truyền động lực cuộc sống.
Chủ đề: {topic}
Mô tả thêm: {desc}
Yêu cầu:
- Ngắn gọn, 3-6 dòng
- Ngôn từ ấm áp, tích cực, truyền cảm hứng
- Có thể dùng trích dẫn hoặc hình ảnh miêu tả
- Không bán hàng, không quảng cáo, không link
- Thêm emoji phù hợp
- Kết thúc bằng lời chúc hoặc câu hỏi gợi mở suy nghĩ
Chỉ trả về nội dung bài đăng, không giải thích."""

    try:
        content = await _call_groq(prompt)
        # Override system prompt for this theme if needed, but reuse _call_groq with different system?
        # For simplicity, we can customize by re-calling with different system, but to avoid complexity, use prompt.
        provider = "groq"
    except Exception as e:
        logger.warning(f"[ContentAgent] Groq motivational thất bại: {e}")
        content = create_motivational_fallback(campaign)
        provider = "fallback"

    return {"content": content, "provider": provider}

# ========== BANKING / FINANCE THEME ==========
def create_banking_fallback(campaign: Dict[str, Any]) -> str:
    name = campaign.get("name", "Sản Phẩm Tài Chính")
    comm_display = campaign.get("commission_display", "ưu đãi tốt")
    templates = [
        f"💰 Cần vốn nhanh? {name} hỗ trợ vay tín chấp linh hoạt với {comm_display}. Giải pháp tài chính thông minh!",
        f"🏦 Ưu đãi đặc biệt từ {name} – lãi suất hấp dẫn, thủ tục đơn giản. Đừng bỏ lỡ cơ hội!",
        f"📈 Quản lý tài chính cá nhân dễ dàng hơn với {name}. Hỗ trợ bạn trên hành trình ổn định cuộc sống.",
        f"💳 Thẻ tín dụng / Vay tiêu dùng {name} – đồng hành cùng bạn trong mọi kế hoạch lớn nhỏ.",
        f"✅ Vay tiền nhanh chóng, an toàn với {name}. Hoa hồng {comm_display} cho người giới thiệu."
    ]
    return random.choice(templates)

async def create_banking_async(campaign: Dict[str, Any]) -> Dict[str, Any]:
    name = campaign.get("name", "Sản phẩm ngân hàng")
    comm_display = campaign.get("commission_display", "ưu đãi")
    desc = campaign.get("description", "tài chính cá nhân")
    prompt = f"""Viết bài đăng về sản phẩm tài chính ngân hàng (vay, thẻ tín dụng, tiết kiệm).
Sản phẩm: {name}
Ưu đãi: {comm_display}
Mô tả: {desc}
Yêu cầu:
- Kết hợp thông tin hữu ích + yếu tố truyền động lực tài chính
- Ngắn gọn, 4-7 dòng
- Nhấn mạnh lợi ích (thủ tục nhanh, lãi suất tốt, hỗ trợ khách hàng)
- Có emoji chuyên nghiệp nhưng gần gũi
- Kêu gọi hành động (tư vấn, đăng ký)
- Phù hợp fanpage tài chính ngân hàng
Chỉ trả về nội dung bài đăng."""

    try:
        content = await _call_groq(prompt)
        provider = "groq"
    except Exception as e:
        logger.warning(f"[ContentAgent] Groq banking thất bại: {e}")
        content = create_banking_fallback(campaign)
        provider = "fallback"

    return {"content": content, "provider": provider}

def create_article_with_params(campaign: Dict[str, Any], params: Dict[str, Any]) -> str:
    return create_article(campaign)


def create_ai_tech_fallback(campaign: Dict[str, Any]) -> str:
    name = campaign.get("name", "Công cụ AI")
    comm_display = campaign.get("commission_display", "hoa hồng tốt")
    templates = [
        f"🤖 Siêu phẩm AI: {name} – tăng năng suất x10, hoa hồng {comm_display}. Dùng ngay kẻo lỡ!",
        f"🚀 Công nghệ AI {name} giúp bạn làm việc nhanh hơn, tiết kiệm thời gian. Nhận {comm_display} mỗi đơn!",
        f"💡 AI đang thay đổi mọi thứ. {name} là công cụ bạn cần, hoa hồng {comm_display} cho affiliate.",
        f"⚡ Tối ưu công việc với {name} – AI thông minh, dễ dùng. Hoa hồng {comm_display} cực hấp dẫn.",
        f"🎯 Chốt deal AI ngay với {name}, hưởng {comm_display}. Tương lai thuộc về người dùng AI!",
    ]
    return random.choice(templates)

async def create_ai_tech_async(campaign: Dict[str, Any]) -> Dict[str, Any]:
    name = campaign.get("name", "Công cụ AI")
    comm_display = campaign.get("commission_display", "hoa hồng")
    desc = campaign.get("description", "công nghệ AI")
    prompt = f"""Viết bài đăng affiliate về sản phẩm công nghệ AI / công cụ AI.
Sản phẩm: {name}
Hoa hồng: {comm_display}
Mô tả: {desc}
Yêu cầu:
- Nhấn mạnh lợi ích: tiết kiệm thời gian, tăng năng suất, dễ sử dụng, thông minh.
- Ngắn gọn 4-7 dòng
- Dùng emoji công nghệ (🤖🚀💡⚡)
- Kêu gọi thử dùng / đăng ký ngay
- Phù hợp fanpage công nghệ AI affiliate
Chỉ trả về nội dung bài đăng."""

    try:
        content = await _call_groq(prompt)
        provider = "groq"
    except Exception as e:
        logger.warning(f"[ContentAgent] Groq ai_tech thất bại: {e}")
        content = create_ai_tech_fallback(campaign)
        provider = "fallback"

    return {"content": content, "provider": provider}