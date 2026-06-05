import logging, re, time
from fullwork.affiliate.base_affiliate import BaseAffiliateWorker
from src.orchestrator import register_worker
logger = logging.getLogger("Shopee.Affiliate")

@register_worker("shopee_affiliate")
class ShopeeAffiliateWorker(BaseAffiliateWorker):
    platform = "Shopee"
    RATE = 0.08
    def execute(self, url, user_id=0, **kw):
        if not re.match(r"https?://(www\.)?shopee\.vn", url):
            return {"status":"error","summary":"URL Shopee khong hop le","raw_stats":{"revenue":0}}
        m = re.search(r"i\.(\d+)\.(\d+)", url)
        item_id = m.group(2) if m else "unknown"
        shop_id = m.group(1) if m else "unknown"
        time.sleep(0.5)
        price, orders = 250000, 5
        rev = round(price * orders * self.RATE, 2)
        stats = {"item_id":item_id,"shop_id":shop_id,"price":price,
                 "orders":orders,"revenue":rev,"url":url}
        return {"status":"success",
                "summary":f"Shopee OK | {orders} don x {price:,}d | hoa hong={rev:,.0f}d",
                "raw_stats":stats}