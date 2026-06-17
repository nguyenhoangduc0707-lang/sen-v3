from pathlib import Path


def write(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  OK: {path}")


# ---- accesstrade_affiliate.py ----
write(
    "fullwork/affiliate/accesstrade_affiliate.py",
    """
import logging, requests
from datetime import datetime, timedelta
from fullwork.affiliate.base_affiliate import BaseAffiliateWorker
from src.orchestrator import register_worker

logger = logging.getLogger("AccessTrade.Affiliate")

AT_API = "https://api.accesstrade.vn/v1"

@register_worker("accesstrade_affiliate")
class AccessTradeAffiliateWorker(BaseAffiliateWorker):
    \"\"\"
    Worker lay du lieu giao dich thuc tu AccessTrade VN API.

    Docs: https://developers.accesstrade.vn/api-publisher-vietnamese
    Auth: Header 'Authorization: Token <access_key>'
          Lay key tai: https://pub.accesstrade.vn/accounts/profile

    Payload nhan vao:
        access_key  : Access key cua publisher (bat buoc)
        days        : So ngay lay giao dich (mac dinh 7)
        merchant    : Ten merchant filter (vd: shopee, tiki) - tuy chon
        status      : 0=hold, 1=approved, 2=rejected - tuy chon
        user_id     : ID nguoi dung trong SEN V3
    \"\"\"
    platform = "AccessTrade"

    def execute(self, url="", access_key="", days=7, merchant=None, status=None, user_id=0, **kw):
        # --- Validate ---
        if not access_key:
            return {
                "status": "error",
                "summary": "Thieu access_key! Lay tai: pub.accesstrade.vn/accounts/profile",
                "raw_stats": {"revenue": 0}
            }

        # --- Tinh khoang thoi gian ---
        until = datetime.utcnow()
        since = until - timedelta(days=int(days))
        params = {
            "since": since.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "until": until.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "limit": 100,
        }
        if merchant:
            params["merchant"] = merchant
        if status is not None:
            params["status"] = status

        headers = {
            "Authorization": f"Token {access_key}",
            "Content-Type": "application/json"
        }

        logger.info(f"[AT] Goi API transactions | since={params['since']} until={params['until']}")

        # --- Goi API ---
        try:
            resp = requests.get(f"{AT_API}/transactions", headers=headers, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.HTTPError as e:
            code = e.response.status_code if e.response else "?"
            msg = "Sai access_key!" if code == 401 else f"HTTP {code}"
            return {"status": "error", "summary": f"[AT] API loi: {msg}", "raw_stats": {"revenue": 0}}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "summary": f"[AT] Loi ket noi: {e}", "raw_stats": {"revenue": 0}}

        # --- Xu ly ket qua ---
        transactions = data.get("data", [])
        total_count   = len(transactions)
        approved      = [t for t in transactions if t.get("status") == 1]
        pending       = [t for t in transactions if t.get("status") == 0]
        rejected      = [t for t in transactions if t.get("status") == 2]

        total_commission = sum(float(t.get("commission", 0)) for t in approved)
        total_value      = sum(float(t.get("transaction_value", 0)) for t in approved)

        # Gom theo merchant
        by_merchant = {}
        for t in approved:
            m = t.get("merchant", "unknown")
            if m not in by_merchant:
                by_merchant[m] = {"count": 0, "commission": 0}
            by_merchant[m]["count"] += 1
            by_merchant[m]["commission"] += float(t.get("commission", 0))

        # 5 giao dich gan nhat
        recent = sorted(approved, key=lambda x: x.get("transaction_time",""), reverse=True)[:5]
        recent_summary = [
            {
                "id": t.get("transaction_id"),
                "merchant": t.get("merchant"),
                "product": t.get("product_name","")[:50],
                "commission": t.get("commission"),
                "time": t.get("transaction_time"),
                "status_text": {0:"hold",1:"approved",2:"rejected"}.get(t.get("status"),"-")
            }
            for t in recent
        ]

        raw_stats = {
            "period_days": days,
            "since": params["since"],
            "until": params["until"],
            "total_transactions": total_count,
            "approved": len(approved),
            "pending": len(pending),
            "rejected": len(rejected),
            "total_commission": round(total_commission, 2),
            "total_value": round(total_value, 2),
            "by_merchant": by_merchant,
            "recent_transactions": recent_summary,
            "revenue": round(total_commission, 2)
        }

        summary = (
            f"AccessTrade {days} ngay | "
            f"Approved={len(approved)} | "
            f"Hoa hong={total_commission:,.0f}d | "
            f"Pending={len(pending)}"
        )

        logger.info(f"[AT] {summary}")
        return {"status": "success", "summary": summary, "raw_stats": raw_stats}
""".strip(),
)

# ---- Cap nhat __init__.py affiliate ---
write(
    "fullwork/affiliate/__init__.py",
    """
from .tiktok_affiliate import TikTokAffiliateWorker
from .shopee_affiliate import ShopeeAffiliateWorker
from .accesstrade_affiliate import AccessTradeAffiliateWorker

__all__ = [
    "TikTokAffiliateWorker",
    "ShopeeAffiliateWorker",
    "AccessTradeAffiliateWorker"
]
""".strip(),
)

# ---- Config mau ---
import json

write(
    "fullwork/affiliate/config_affiliate.json",
    json.dumps(
        {
            "_comment": "Dien access_key cua ban vao day. Lay tai: pub.accesstrade.vn/accounts/profile",
            "accesstrade": {
                "access_key": "YOUR_ACCESS_KEY_HERE",
                "default_days": 7,
                "merchants": ["shopee", "tiki", "lazada"],
            },
            "tiktok": {"account": "YOUR_TIKTOK_ACCOUNT"},
            "shopee": {"app_id": "YOUR_APP_ID", "secret_key": "YOUR_SECRET_KEY"},
        },
        indent=2,
        ensure_ascii=False,
    ),
)

# ---- Test file ---
write(
    "test_accesstrade.py",
    """
import sys, logging
from pathlib import Path
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
sys.path.insert(0, str(Path(".").resolve()))

from src.orchestrator import discoverregistry, run_worker, registry

discoverregistry()
print("Workers:", list(registry.keys()))

# Test 1: Thieu access_key
print("\\n=== TEST 1: Thieu access_key (phai bao loi) ===")
r = run_worker("accesstrade_affiliate", access_key="", days=7)
print("Status:", r["status"])
print("Summary:", r["summary"])

# Test 2: Sai access_key (goi API that, expect HTTP 401)
print("\\n=== TEST 2: Sai access_key (goi API that) ===")
r2 = run_worker("accesstrade_affiliate", access_key="fake_key_test_12345", days=1)
print("Status:", r2["status"])
print("Summary:", r2["summary"])

# Test 3: Dien key that cua ban vao day
ACCESS_KEY = "DIEN_KEY_THAT_CUA_BAN_VAO_DAY"
if ACCESS_KEY != "DIEN_KEY_THAT_CUA_BAN_VAO_DAY":
    print("\\n=== TEST 3: Key that ===")
    r3 = run_worker("accesstrade_affiliate", access_key=ACCESS_KEY, days=7)
    print("Status:", r3["status"])
    print("Summary:", r3["summary"])
    print("Chi tiet:", r3["raw_stats"])
else:
    print("\\n=== TEST 3: Bo qua (chua dien key that) ===")
    print("-> Vao file test_accesstrade.py, sua dong ACCESS_KEY thanh key that cua ban")
    print("-> Lay key tai: https://pub.accesstrade.vn/accounts/profile")

print("\\n=== DONE ===")
""".strip(),
)

print("\\nTat ca file da tao xong!")
print("Chay: python test_accesstrade.py")
