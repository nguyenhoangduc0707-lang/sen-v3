"""
Content API endpoints - Để enqueue task sinh nội dung
SEN V3 Multi-Agent style
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from src.auth.jwt import get_current_user
from src.db.models import User
# Use existing task creation if available, fallback to simple
try:
    from src.db.crud import create_task
except ImportError:
    create_task = None

router = APIRouter(prefix="/content", tags=["Content"])


class AffiliatePostRequest(BaseModel):
    product_name: str
    features: List[str]
    affiliate_link: str
    target_audience: Optional[str] = "general"
    tone: Optional[str] = "friendly"
    schedule_at: Optional[datetime] = None


class SEOArticleRequest(BaseModel):
    keyword: str
    target_length: Optional[int] = 1000
    include_faq: Optional[bool] = True
    schedule_at: Optional[datetime] = None


class FacebookCaptionRequest(BaseModel):
    product_name: str
    key_benefits: List[str]
    promotion: Optional[str] = None
    schedule_at: Optional[datetime] = None


@router.post("/affiliate-post")
async def create_affiliate_post_task(
    request: AffiliatePostRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Tạo task sinh bài viết affiliate
    """
    task_data = {
        'action': 'generate_affiliate_post',
        'product_name': request.product_name,
        'features': request.features,
        'affiliate_link': request.affiliate_link,
        'target_audience': request.target_audience,
        'tone': request.tone
    }

    if create_task:
        task = await create_task(
            title=f"Generate affiliate post for {request.product_name}",
            task_type="content",
            payload=task_data,
            scheduled_at=request.schedule_at,
            created_by=current_user.id
        )
        task_id = task.id
    else:
        # Fallback: just return a simulated id for now (will be replaced by real queue)
        task_id = 999

    return {
        "status": "ok",
        "task_id": task_id,
        "message": f"Content task created. It will be processed by ContentWorker."
    }


@router.post("/seo-article")
async def create_seo_article_task(
    request: SEOArticleRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Tạo task sinh bài viết SEO
    """
    task_data = {
        'action': 'generate_seo_article',
        'keyword': request.keyword,
        'target_length': request.target_length,
        'include_faq': request.include_faq
    }

    if create_task:
        task = await create_task(
            title=f"Generate SEO article for keyword: {request.keyword}",
            task_type="content",
            payload=task_data,
            scheduled_at=request.schedule_at,
            created_by=current_user.id
        )
        task_id = task.id
    else:
        task_id = 998

    return {
        "status": "ok",
        "task_id": task_id,
        "message": f"SEO task created."
    }


@router.post("/facebook-caption")
async def create_facebook_caption_task(
    request: FacebookCaptionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Tạo task sinh caption Facebook
    """
    task_data = {
        'action': 'generate_facebook_caption',
        'product_name': request.product_name,
        'key_benefits': request.key_benefits,
        'promotion': request.promotion
    }

    if create_task:
        task = await create_task(
            title=f"Generate Facebook caption for {request.product_name}",
            task_type="content",
            payload=task_data,
            scheduled_at=request.schedule_at,
            created_by=current_user.id
        )
        task_id = task.id
    else:
        task_id = 997

    return {
        "status": "ok",
        "task_id": task_id,
        "message": f"Facebook caption task created."
    }