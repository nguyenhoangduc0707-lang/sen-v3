import asyncio
from src.orchestrator_async import run_engine
from src.orchestrator import register_worker

from src.workers.echo_worker import EchoWorker
from src.workers.shopee_worker import ShopeeWorker
from src.workers.tiktok_worker import TikTokWorker
from src.workers.content_worker import ContentWorker
from src.workers.facebook_autoposter import FacebookAutoPoster

register_worker("echo_worker", EchoWorker)
register_worker("shopee_affiliate", ShopeeWorker)
register_worker("tiktok_affiliate", TikTokWorker)
register_worker("content_creator", ContentWorker)
register_worker("facebook_autoposter", FacebookAutoPoster)

if __name__ == "__main__":
    asyncio.run(run_engine())
