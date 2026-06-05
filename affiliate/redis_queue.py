import redis
import json
import logging

logger = logging.getLogger(__name__)

# Kết nối Redis (mặc định localhost:6379, không password)
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

CAMPAIGN_QUEUE = "campaign:queue"

def push_campaign_to_queue(campaign_id):
    """Đẩy campaign_id vào hàng đợi Redis"""
    redis_client.lpush(CAMPAIGN_QUEUE, campaign_id)
    logger.info(f"Đã push campaign {campaign_id} vào queue")

def pop_campaign_from_queue():
    """Lấy campaign_id từ hàng đợi (FIFO)"""
    return redis_client.rpop(CAMPAIGN_QUEUE)

def get_queue_length():
    return redis_client.llen(CAMPAIGN_QUEUE)