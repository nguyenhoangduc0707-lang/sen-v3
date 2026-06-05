from __future__ import annotations
import logging, sqlite3, sys, json
from datetime import datetime
from pathlib import Path
import requests
from config_loader import get_access_key, get_base_url, get_picker_config

LOG_DIR = Path(__file__).resolve().parent / "logs"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[logging.FileHandler(LOG_DIR / "picker.log", encoding="utf-8"), logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger("auto_picker")
DB_PATH = Path(__file__).resolve().parent / "data" / "campaigns.db"

def _init_db(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS campaigns (id TEXT PRIMARY KEY, name TEXT, merchant TEXT, commission REAL, gross REAL, cookie_days INTEGER, status TEXT, tracking_url TEXT, fetched_at TEXT, score REAL DEFAULT 0)")
    conn.execute("CREATE TABLE IF NOT EXISTS tracking_links (campaign_id TEXT PRIMARY KEY, url TEXT, created_at TEXT)")
    conn.commit()

def _score(c):
    commission = float(c.get("commission_rate") or c.get("commission") or 0)
    gross = float(c.get("gross_commission") or 0)
    cookie = int(c.get("cookie_duration") or 0)
    approved = 10 if str(c.get("approval_status","")).lower() in ("approved","active","1") else 0
    return round(commission*50 + gross*0.001 + cookie*0.5 + approved, 4)

def fetch_campaigns():
    endpoints = ["/cashback/campaigns", "/campaigns"]
    headers = {"Authorization": f"Token {get_access_key()}"}
    for ep in endpoints:
        url = f"{get_base_url()}{ep}"
        log.info(f"Dang lay campaigns tu {ep}...")
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                campaigns = data if isinstance(data, list) else data.get("data", data.get("campaigns", data.get("result", [])))
                if campaigns and len(campaigns) > 0:
                    log.info(f"Lay duoc {len(campaigns)} campaigns tu {ep}.")
                    return campaigns
        except: pass
    return []

def run_picker():
    campaigns = fetch_campaigns()
    if not campaigns:
        log.warning("Khong bốc được campaign nào. Vui lòng kiểm tra lại Access Key!")
        return []
    cfg = get_picker_config()
    top_n = int(cfg.get("top_n", 5))
    min_r = float(cfg.get("min_commission_rate", 0.0))
    
    scored = []
    for c in campaigns:
        if isinstance(c, str):
            try: c = json.loads(c)
            except: continue
        if not isinstance(c, dict): continue
        if float(c.get("commission_rate") or c.get("commission") or 0) >= min_r:
            c["_score"] = _score(c)
            scored.append(c)
            
    top = sorted(scored, key=lambda x: x["_score"], reverse=True)[:top_n]
    log.info(f"Top {len(top)} campaigns sau scoring:")
    
    with sqlite3.connect(DB_PATH) as conn:
        _init_db(conn)
        fetched_at = datetime.utcnow().isoformat()
        for c in top:
            cid = str(c.get("id") or c.get("campaign_id") or "")
            name = c.get("name") or c.get("campaign_name") or "Chua co ten"
            log.info(f"  [{c['_score']:.4f}] {cid} - {name}")
            conn.execute("INSERT INTO campaigns (id,name,merchant,commission,gross,cookie_days,status,tracking_url,fetched_at,score) VALUES (?,?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET fetched_at=excluded.fetched_at, score=excluded.score", (cid, name, c.get("merchant_name") or c.get("merchant") or "", float(c.get("commission_rate") or 0), float(c.get("gross_commission") or 0), int(c.get("cookie_duration") or 0), str(c.get("approval_status") or ""), "", fetched_at, c["_score"]))
        conn.commit()
    log.info(f"Da luu {len(top)} campaigns vao DB.")
    return top

if __name__ == "__main__":
    run_picker()