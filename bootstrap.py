from pathlib import Path


def write(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  OK: {path}")


print("=== Tao toan bo file he thong ===")

# ---- base_affiliate.py ----
write(
    "fullwork/affiliate/base_affiliate.py",
    """
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
""".strip(),
)

# ---- tiktok_affiliate.py ----
write(
    "fullwork/affiliate/tiktok_affiliate.py",
    """
import logging, re, time
from fullwork.affiliate.base_affiliate import BaseAffiliateWorker
from src.orchestrator import register_worker
logger = logging.getLogger("TikTok.Affiliate")

@register_worker("tiktok_affiliate")
class TikTokAffiliateWorker(BaseAffiliateWorker):
    platform = "TikTok"
    def execute(self, url, user_id=0, **kw):
        if not re.match(r"https?://(www\\.)?(tiktok\\.com|vm\\.tiktok\\.com)", url):
            return {"status":"error","summary":"URL khong hop le","raw_stats":{"revenue":0}}
        m = re.search(r"/video/(\\d+)", url)
        product_id = m.group(1) if m else "unknown"
        logger.info(f"[TikTok] product_id={product_id}")
        time.sleep(0.5)
        stats = {"views":1200,"likes":340,"clicks":89,"conversions":3,
                 "revenue":round(3*15000*0.05,2),"product_id":product_id,"url":url}
        return {"status":"success",
                "summary":f"TikTok OK | {stats['conversions']} don | {stats['revenue']:,.0f}d",
                "raw_stats":stats}
""".strip(),
)

# ---- shopee_affiliate.py ----
write(
    "fullwork/affiliate/shopee_affiliate.py",
    """
import logging, re, time
from fullwork.affiliate.base_affiliate import BaseAffiliateWorker
from src.orchestrator import register_worker
logger = logging.getLogger("Shopee.Affiliate")

@register_worker("shopee_affiliate")
class ShopeeAffiliateWorker(BaseAffiliateWorker):
    platform = "Shopee"
    RATE = 0.08
    def execute(self, url, user_id=0, **kw):
        if not re.match(r"https?://(www\\.)?shopee\\.vn", url):
            return {"status":"error","summary":"URL Shopee khong hop le","raw_stats":{"revenue":0}}
        m = re.search(r"i\\.(\\d+)\\.(\\d+)", url)
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
""".strip(),
)

# ---- __init__.py affiliate ----
write(
    "fullwork/affiliate/__init__.py",
    """
from .tiktok_affiliate import TikTokAffiliateWorker
from .shopee_affiliate import ShopeeAffiliateWorker
__all__ = ["TikTokAffiliateWorker", "ShopeeAffiliateWorker"]
""".strip(),
)

# ---- __init__.py fullwork ----
write("fullwork/__init__.py", "# fullwork package")

# ---- Fix database.py ----
write(
    "src/database.py",
    """
import sqlite3, json, logging
from pathlib import Path
DB = Path("sen_v3.db")
logger = logging.getLogger("Database")

def save_task_result(user_id, worker, url, result):
    try:
        conn = sqlite3.connect(DB)
        conn.execute(
            "INSERT INTO tasks (user_id,worker,url,status,result_summary,raw_stats,revenue,finished_at) VALUES (?,?,?,?,?,?,?,datetime('now'))",
            (user_id, worker, url,
             result.get("status","unknown"),
             json.dumps(result.get("summary","")),
             json.dumps(result.get("raw_stats",{})),
             result.get("raw_stats",{}).get("revenue",0))
        )
        conn.commit()
        conn.close()
        logger.info(f"[DB] Saved: {worker} user={user_id}")
    except Exception as e:
        logger.error(f"[DB] Error: {e}")
""".strip(),
)

# ---- Fix orchestrator.py ----
write(
    "src/orchestrator.py",
    """
import importlib.util, logging
from pathlib import Path
logger = logging.getLogger("Orchestrator")
registry = {}

def register_worker(name):
    def decorator(cls):
        registry[name] = cls
        logger.info(f"[Worker] Registered: {name}")
        return cls
    return decorator

def _load_dir(directory, prefix):
    if not Path(directory).exists(): return
    for py in Path(directory).glob("*.py"):
        if py.name.startswith("_"): continue
        name = f"{prefix}.{py.stem}"
        try:
            spec = importlib.util.spec_from_file_location(name, py)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        except Exception as e:
            logger.error(f"[Discover] {name}: {e}")

def discoverregistry():
    _load_dir("src/workers", "src.workers")
    if Path("fullwork").exists():
        for g in Path("fullwork").iterdir():
            if g.is_dir() and not g.name.startswith("_"):
                _load_dir(g, f"fullwork.{g.name}")

def run_worker(name, **kw):
    cls = registry.get(name)
    if not cls:
        logger.error(f"[Worker] Not found: {name}")
        return {"status":"error","summary":f"Worker '{name}' not found"}
    try:
        return cls().run(**kw)
    except Exception as e:
        logger.error(f"[Worker] {name} crash: {e}")
        return {"status":"error","summary":str(e)}
""".strip(),
)

# ---- test_fullwork.py ----
write(
    "test_fullwork.py",
    """
import sys, logging
from pathlib import Path
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
sys.path.insert(0, str(Path(".").resolve()))

from src.orchestrator import discoverregistry, run_worker, registry
from src.task_queue import add_task, get_next_task, mark_task_done

print("\\n=== TEST 1: Discover Workers ===")
discoverregistry()
print("Workers:", list(registry.keys()))

print("\\n=== TEST 2: TikTok Affiliate ===")
r = run_worker("tiktok_affiliate", url="https://www.tiktok.com/@test/video/1234567890")
print("Status:", r.get("status"))
print("Summary:", r.get("summary"))

print("\\n=== TEST 3: Shopee Affiliate ===")
r2 = run_worker("shopee_affiliate", url="https://shopee.vn/product-i.123456.987654321")
print("Status:", r2.get("status"))
print("Summary:", r2.get("summary"))

print("\\n=== TEST 4: Task Queue end-to-end ===")
add_task("tiktok_affiliate", {"url":"https://www.tiktok.com/@shop/video/999","user_id":1})
task = get_next_task()
result = run_worker(task["worker"], **task["payload"])
mark_task_done(task, result)
print("Queue OK:", result.get("status"))

print("\\n=== ALL TESTS DONE ===")
""".strip(),
)

print("\\n=== Tat ca file da tao xong! ===")
print("Chay: python test_fullwork.py")
