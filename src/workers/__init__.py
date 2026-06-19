from .scheduler_worker import SchedulerWorker
from .echo_worker import EchoWorker
from .shopee_worker import ShopeeWorker
from .tiktok_worker import TikTokWorker
from .content_worker import ContentWorker
from .facebook_autoposter import FacebookAutoPoster

# Registry cac worker
WORKER_REGISTRY = {
    "echo_worker": EchoWorker,
    "shopee_affiliate": ShopeeWorker,
    "tiktok_affiliate": TikTokWorker,
    "content_creator": ContentWorker,
    "facebook_autoposter": FacebookAutoPoster,
}
