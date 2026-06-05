import json
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Đường dẫn: C:\DYT_01\tasks\campaign_queue.json
QUEUE_FILE = Path("tasks/campaign_queue.json")

def _init_queue():
    if not QUEUE_FILE.parent.exists():
        QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not QUEUE_FILE.exists():
        with open(QUEUE_FILE, 'w') as f:
            json.dump([], f)

def push_campaign_to_queue(campaign_id):
    _init_queue()
    with open(QUEUE_FILE, 'r+') as f:
        data = json.load(f)
        data.append(campaign_id)
        f.seek(0)
        json.dump(data, f)
    logger.info(f"[FILE_QUEUE] Đã push campaign {campaign_id}")

def pop_campaign_from_queue():
    _init_queue()
    with open(QUEUE_FILE, 'r+') as f:
        data = json.load(f)
        if not data:
            return None
        campaign_id = data.pop(0)
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        return campaign_id

def get_queue_length():
    _init_queue()
    with open(QUEUE_FILE, 'r') as f:
        return len(json.load(f))