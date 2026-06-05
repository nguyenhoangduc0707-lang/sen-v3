import logging, time
from abc import ABC, abstractmethod
logger = logging.getLogger("Affiliate")

class BaseAffiliateWorker(ABC):
    platform = "unknown"
    def run(self, url, user_id=0, **kw):
        logger.info(f"[{self.platform}] Start: {url}")
        t = time.time()
        try:
            r = self.execute(url=url, user_id=user_id, **kw)
            r["elapsed"] = round(time.time()-t, 2)
            r["platform"] = self.platform
            return r
        except Exception as e:
            logger.error(f"[{self.platform}] Error: {e}")
            return {"status":"error","summary":str(e),"platform":self.platform,"raw_stats":{"revenue":0}}
    @abstractmethod
    def execute(self, url, **kw): pass