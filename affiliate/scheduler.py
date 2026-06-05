import logging
import time

import schedule

from affiliate.fetcher import fetch_and_store

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def job():
    logger.info("Starting scheduled affiliate campaign sync")
    fetch_and_store()
    logger.info("Finished scheduled affiliate campaign sync")


schedule.every(6).hours.do(job)


if __name__ == "__main__":
    logger.info("Affiliate scheduler started. Running first sync now...")
    job()
    while True:
        schedule.run_pending()
        time.sleep(60)
