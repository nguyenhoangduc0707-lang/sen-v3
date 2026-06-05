from pathlib import Path


def write(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  OK: {path}")


write(
    "fullwork/affiliate/auto_picker.py",
    """
import requests, logging, json
from datetime import datetime

logger = logging.getLogger("AutoPicker")
AT_API  = "https://api.accesstrade.vn/v1"

def get_headers(access_key):
    return {
        "Authorization": f"Token {access_key}",
        "Content-Type": "application/json"
    }

def score_campaign(c):
    score = 0
    reasons = []

    # Da duoc duyet — chay duoc ngay
    if c.get("approval") == "successful":
        score += 30
        reasons.append("+30 da duoc duyet")

    # Hoa hong cao (dung max_commission tu API moi)
    max_comm = float(c.get("max_commission") or 0)
    if c.get("commission_type") == "percentage":
        if max_comm >= 10:
            score += 25; reasons.append(f"+25 hoa hong cao {max_comm}%")
        elif max_comm >= 5:
            score += 15; reasons.append(f"+15 hoa hong kha {max_comm}%")
        elif max_comm > 0:
            score += 5;  reasons.append(f"+5  hoa hong {max_comm}%")
    else:  # fixed
        if max_comm >= 100000:
            score += 20; reasons.append(f"+20 fixed {max_comm:,.0f}d/don")
        elif max_comm >= 30000:
            score += 10; reasons.append(f"+10 fixed {max_comm:,.0f}d/don")

    # gross_commission = tong hoa hong da chi tra thuc te (popularity)
    gross = float(c.get("gross_commission") or 0)
    if gross >= 10_000_000:
        score += 20; reasons.append(f"+20 gross={gross/1e6:.1f}M (rat hot)")
    elif gross >= 1_000_000:
        score += 10; reasons.append(f"+10 gross={gross/1e6:.1f}M (hot)")
    elif gross > 0:
        score += 5;  reasons.append(f"+5  gross={gross/1e3:.0f}K")

    # Cookie dai
    cookie_s = int(c.get("cookie_expire") or 0)
    cookie_d = cookie_s // 86400
    if cookie_d >= 30:
        score += 10; reasons.append(f"+10 cookie={cookie_d}ngay")
    elif cookie_d >= 7:
        score += 5;  reasons.append(f"+5  cookie={cookie_d}ngay")

    # Merchant uy tin
    merchant = (c.get("merchant") or "").lower()
    trusted = {"shopee":20,"tiki":15,"lazada":15,"grab":12,
               "momo":12,"sendo":10,"thefaceshop":8}
    for m, bonus in trusted.items():
        if m in merchant:
            score += bonus
            reasons.append(f"+{bonus} merchant uy tin ({m})")
            break

    # Sap het han
    end = c.get("end_date") or c.get("end_time")
    if end:
        try:
            days_left = (datetime.fromisoformat(
                end.replace("Z","").split("T")[0]) - datetime.utcnow()).days
            if days_left < 7:
                score -= 15; reasons.append(f"-15 sap het han ({days_left}ngay)")
        except: pass

    return score, reasons


def fetch_campaigns_v2(access_key):
    headers = get_headers(access_key)
    all_camps = []
    page = 1
    while True:
        r = requests.get(
            f"{AT_API}/cashback/campaigns",
            headers=headers,
            params={"page": page, "page_size": 50,
                    "sort_by": "max_commission", "sort_order": "desc"},
            timeout=15
        )
        if r.status_code != 200:
            logger.error(f"API loi: {r.status_code} — {r.text[:100]}")
            break
        body = r.json()
        camps = body.get("data", {}).get("campaigns", [])
        if not camps: break
        all_camps.extend(camps)
        meta  = body.get("data", {}).get("meta", {})
        total = meta.get("total", 0)
        if len(all_camps) >= total: break
        page += 1
    return all_camps, headers


def create_tracking_link(headers, campaign_id, url=None):
    payload = {
        "campaign_id": str(campaign_id),
        "utm_source":   "sen_v3",
        "utm_medium":   "auto_picker",
        "utm_campaign": f"keo_{campaign_id}"
    }
    if url:
        payload["urls"] = [url]
    r = requests.post(f"{AT_API}/product_link/create",
                      headers=headers, json=payload, timeout=15)
    if r.status_code == 200:
        links = r.json().get("data", {}).get("success_link", [])
        if links:
            return {
                "aff_link":   links[0].get("aff_link", ""),
                "short_link": links[0].get("short_link", ""),
                "url_origin": links[0].get("url_origin", "")
            }
    return {"error": r.text[:200]}


def auto_pick_and_setup(access_key, top_n=8, auto_create_link=True):
    SEP = "="*60
    print(f"\\n{SEP}")
    print("  AUTO CAMPAIGN PICKER v2 — SEN V3 / AccessTrade")
    print(SEP)

    # 1. Fetch
    print("\\n[1/3] Scan tat ca campaign (API v2 voi hoa hong thuc te)...")
    campaigns, headers = fetch_campaigns_v2(access_key)
    approved = [c for c in campaigns if c.get("approval") == "successful"]
    print(f"  Tong: {len(campaigns)} | Da duyet: {len(approved)}")

    if not campaigns:
        print("  CANH BAO: Khong lay duoc campaign nao!")
        return []

    # 2. Score
    print("\\n[2/3] Cham diem toan bo keo...")
    scored = []
    for c in campaigns:
        score, reasons = score_campaign(c)
        max_c  = float(c.get("max_commission") or 0)
        comm_t = c.get("commission_type","")
        comm_str = f"{max_c}%" if comm_t=="percentage" else f"{max_c:,.0f}d"
        scored.append({
            "id":           c.get("campaign_id"),
            "name":         c.get("name",""),
            "merchant":     c.get("merchant",""),
            "approval":     c.get("approval",""),
            "url":          c.get("url",""),
            "max_commission": max_c,
            "commission_type": comm_t,
            "commission_str": comm_str,
            "gross_commission": float(c.get("gross_commission") or 0),
            "cookie_days":  int(c.get("cookie_expire") or 0) // 86400,
            "category":     c.get("category_name",""),
            "score":        score,
            "reasons":      reasons
        })
    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[:top_n]

    # 3. In bang xep hang
    print(f"\\n  TOP {top_n} KEO TOT NHAT:\\n")
    print(f"  {'#':<3} {'DIEM':<6} {'HOA HONG':<12} {'GROSS(M)':<10} {'MERCHANT':<22} TEN CAMPAIGN")
    print("  " + "-"*90)
    for i, c in enumerate(top, 1):
        icon = "✅" if c["approval"]=="successful" else "⏳"
        gross_m = c["gross_commission"] / 1_000_000
        name_s  = c["name"][:30]
        print(f"  {i:<3} {c['score']:<6} {c['commission_str']:<12} {gross_m:<10.1f} {c['merchant'][:21]:<22} {icon} {name_s}")
        for r in c["reasons"]:
            print(f"       └ {r}")

    # 4. Tao tracking link
    results = []
    if auto_create_link:
        print("\\n[3/3] Tu dong tao tracking link cho top keo da duyet...")
        for c in top:
            if c["approval"] != "successful":
                print(f"  SKIP {c['name'][:30]} (chua duyet)")
                continue
            print(f"  Dang tao link: {c['name'][:40]}...")
            link = create_tracking_link(headers, c["id"], c.get("url"))
            c["tracking"] = link
            if "aff_link" in link:
                short = link.get("short_link") or link.get("aff_link","")[:60]
                print(f"  ✅ {c['merchant']}: {short}")
            else:
                print(f"  ❌ Loi: {link}")
            results.append(c)

        # Luu file
        out = "fullwork/affiliate/active_campaigns.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump({
                "updated_at": datetime.now().isoformat(),
                "total": len(results),
                "campaigns": results
            }, f, ensure_ascii=False, indent=2)
        print(f"\\n  Saved → {out}")
    else:
        results = top

    return results
""".strip(),
)

write(
    "run_picker.py",
    """
import sys, logging
from pathlib import Path
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
sys.path.insert(0, str(Path(".").resolve()))
from fullwork.affiliate.auto_picker import auto_pick_and_setup

# === DIEN KEY CUA BAN ===
ACCESS_KEY = "DIEN_KEY_THAT_CUA_BAN_VAO_DAY"

if ACCESS_KEY == "DIEN_KEY_THAT_CUA_BAN_VAO_DAY":
    print("Chua dien ACCESS_KEY!")
    print("Lay key tai: https://pub.accesstrade.vn/accounts/profile")
    sys.exit(1)

results = auto_pick_and_setup(
    access_key=ACCESS_KEY,
    top_n=8,
    auto_create_link=True
)

print("\\n" + "="*60)
print("  TONG KET — LINK SAN SANG PROMOTE")
print("="*60)
for c in results:
    t = c.get("tracking", {})
    link = t.get("short_link") or t.get("aff_link","")[:70]
    print(f"  [{c['score']}pt] {c['name'][:35]}")
    print(f"    Hoa hong : {c['commission_str']} | Cookie: {c['cookie_days']}ngay")
    print(f"    Link     : {link or 'Loi tao link'}")
    print()
print("Chi tiet luu tai: fullwork/affiliate/active_campaigns.json")
""".strip(),
)

print("Upgrade xong! Chay: notepad run_picker.py -> dien key -> python run_picker.py")
