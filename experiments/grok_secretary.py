"""
🤖 GROK SECRETARY - Thư ký AI cho dự án DYT_01
================================================
Sử dụng xAI API (tương thích OpenAI SDK).
Cần XAI_API_KEY trong file .env

Cài đặt: pip install openai
Chạy:    python grok_secretary.py
"""

import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# CẤU HÌNH
# ─────────────────────────────────────────────
XAI_API_KEY = os.getenv("XAI_API_KEY", "")
MODEL_FAST   = "grok-3-mini"   # Rẻ, nhanh – dùng cho câu hỏi đơn giản
MODEL_SMART  = "grok-3"        # Mạnh hơn – dùng cho phân tích sâu

# ─────────────────────────────────────────────
# NGỮ CẢNH DỰ ÁN (System Prompt)
# ─────────────────────────────────────────────
PROJECT_CONTEXT = """
Bạn là "Grok Secretary" – thư ký AI riêng của dự án DYT_01.

## 📁 DỰ ÁN DYT_01
- Loại: Hệ thống Marketing Automation + Affiliate Marketing
- Backend: Python (FastAPI) tại E:/DYT_01
- Frontend: React + Vite + TailwindCSS tại E:/DYT_01/frontend/dashboard
- Database: SQLite (app.db, sen_v3.db)
- Cổng backend: 8000 | Frontend: 5173/5174

## 🛒 CHIẾN DỊCH ĐANG CHẠY
- Shopee 6/6 Mid Year Mega Sale
- Lazada Super Sale
- AccessTrade Affiliate Campaign
- Tiki Campaign

## 👥 NHÂN SỰ
- Admin: quản trị toàn bộ hệ thống
- Team sales: theo dõi doanh thu, chiến dịch affiliate

## 🔧 TÍCH HỢP
- AccessTrade API: affiliate links
- Facebook Auto Post
- Telegram Bot
- NotebookLM: lưu trữ kiến thức dự án
- Grok CLI: AI agent viết code

## 📊 KPI THEO DÕI
- Doanh thu hàng ngày (target)
- Hoa hồng affiliate (5%)
- Task hoàn thành / tổng task
- Nhân sự active

## 🎯 NGUYÊN TẮC TRẢ LỜI
1. Trả lời BẰNG TIẾNG VIỆT
2. Ngắn gọn, súc tích, đi thẳng vào vấn đề
3. Ưu tiên giải pháp thực tế cho dự án DYT_01
4. Nếu cần code → viết Python hoặc JavaScript
5. Luôn hỏi lại nếu chưa rõ yêu cầu
"""

# ─────────────────────────────────────────────
# KHỞI TẠO CLIENT
# ─────────────────────────────────────────────
def get_client():
    if not XAI_API_KEY:
        raise ValueError(
            "❌ Chưa có XAI_API_KEY trong file .env!\n"
            "👉 Vào https://console.x.ai → API Keys → Tạo key → Paste vào .env:\n"
            "   XAI_API_KEY=xai-xxxxxxxxxxxxxxxx"
        )
    return OpenAI(
        api_key=XAI_API_KEY,
        base_url="https://api.x.ai/v1"
    )

# ─────────────────────────────────────────────
# HÀM CHAT CHÍNH
# ─────────────────────────────────────────────
def chat(
    message: str,
    history: list = None,
    smart_mode: bool = False
) -> str:
    """
    Gửi tin nhắn đến Grok Secretary.
    
    Args:
        message: Câu hỏi / yêu cầu
        history: Lịch sử hội thoại [{role, content}]
        smart_mode: True = dùng grok-3 (mạnh hơn, tốn quota hơn)
    
    Returns:
        Câu trả lời dạng string
    """
    client = get_client()
    model  = MODEL_SMART if smart_mode else MODEL_FAST
    
    messages = [{"role": "system", "content": PROJECT_CONTEXT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": message})
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=2000,
    )
    return response.choices[0].message.content

# ─────────────────────────────────────────────
# API ENDPOINT (FastAPI) – import vào main app
# ─────────────────────────────────────────────
def create_secretary_router():
    """Tạo FastAPI router cho thư ký Grok."""
    try:
        from fastapi import APIRouter
        from pydantic import BaseModel
        
        router = APIRouter(prefix="/api/secretary", tags=["Grok Secretary"])
        
        class ChatRequest(BaseModel):
            message: str
            history: list = []
            smart_mode: bool = False
        
        class ChatResponse(BaseModel):
            reply: str
            model: str
            timestamp: str
        
        @router.post("/chat", response_model=ChatResponse)
        async def secretary_chat(req: ChatRequest):
            reply = chat(req.message, req.history, req.smart_mode)
            return ChatResponse(
                reply=reply,
                model=MODEL_SMART if req.smart_mode else MODEL_FAST,
                timestamp=datetime.now().isoformat()
            )
        
        @router.get("/status")
        async def secretary_status():
            return {
                "status": "online",
                "model_fast": MODEL_FAST,
                "model_smart": MODEL_SMART,
                "api_key_set": bool(XAI_API_KEY),
                "project": "DYT_01"
            }
        
        return router
    except ImportError:
        return None

# ─────────────────────────────────────────────
# CHẠY TRỰC TIẾP – TERMINAL CHAT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("🤖 GROK SECRETARY - Thư ký AI dự án DYT_01")
    print("=" * 55)
    print(f"Model nhanh : {MODEL_FAST}")
    print(f"Model mạnh  : {MODEL_SMART}")
    print("Lệnh: 'smart' = chuyển sang grok-3 | 'exit' = thoát")
    print("-" * 55)
    
    if not XAI_API_KEY:
        print("\n❌ CHƯA CÓ API KEY!")
        print("👉 Làm theo 3 bước:")
        print("   1. Vào https://console.x.ai")
        print("   2. Tạo API Key (được $25 miễn phí)")
        print("   3. Thêm vào file E:/DYT_01/.env:")
        print("      XAI_API_KEY=xai-xxxxxxxxxxxxxxxx")
        exit(1)
    
    history = []
    smart   = False
    
    while True:
        try:
            user_input = input(f"\n[{'SMART' if smart else 'FAST'}] Bạn: ").strip()
        except KeyboardInterrupt:
            print("\n👋 Tạm biệt!")
            break
        
        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("👋 Tạm biệt!")
            break
        if user_input.lower() == "smart":
            smart = not smart
            print(f"✅ Chuyển sang {'SMART (grok-3)' if smart else 'FAST (grok-3-mini)'}")
            continue
        if user_input.lower() == "clear":
            history = []
            print("🗑️  Đã xóa lịch sử hội thoại")
            continue
        
        print("\n🤖 Grok đang xử lý...", end="", flush=True)
        try:
            reply = chat(user_input, history, smart)
            history.append({"role": "user",      "content": user_input})
            history.append({"role": "assistant",  "content": reply})
            print(f"\r🤖 Grok:\n{reply}")
            # Giữ tối đa 10 lượt hội thoại (tiết kiệm token)
            if len(history) > 20:
                history = history[-20:]
        except Exception as e:
            print(f"\r❌ Lỗi: {e}")

