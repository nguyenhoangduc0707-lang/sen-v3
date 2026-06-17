from pathlib import Path


def write(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  OK: {path}")


# ---- auto_picker.py ----
write(
    "fullwork/affiliate/auto_picker.py",
    """
import requests, logging, json, re
from datetime import datetime

logger = logging.getLogger("AutoPicker")
AT_API = "https://api.accesstrade.vn/v1"

# Cau hinh diem cham keo
SCORE_WEIGHTS = {
    "commission_high":   30,   # Hoa hong cao
    "shopee_merchant":   20,   # Shopee = uy tin, de ban
    "tiki_merchant":     15,
    "lazada_merchant":   15,
    "already_approved":  25,   # Da duoc duyet = chay duoc ngay
    "has_end_time":     -10,   # Sap het han = rui ro
    "cookie_long":       10,   # Cookie dai = co nhieu co hoi
}

TRUSTED_MERCHANTS = ["shopee", "tiki", "lazada", "sendo", "grab", "momo"]

def score_campaign(camp):
    score = 0
    reasons = []

    # Da duoc duyet
    if camp.get("approval") == "successful":
        score += SCORE_WEIGHTS["already_approved"]
        reasons.append("+25 da duoc duyet")

    # Merchant uy tin
    merchant = (camp.get("merchant") or "").lower()
    for m in TRUSTED_MERCHANTS:
        if m in merchant:
            bonus = SCORE_WEIGHTS.get(f"{m}_merchant", 10)
            score += bonus
            reasons.append(f"+{bonus} merchant={m}")
            break

    # Cookie duration
    cookie = camp.get("cookie_duration", 0) or 0
    if cookie >= 86400 * 7:  # >= 7 ngay
        score += SCORE_WEIGHTS["cookie_long"]
        reasons.append(f"+10 cookie={cookie//86400}ngay")

    # Sap het han
    end_time = camp.get("end_time")
    if end_time:
        try:
            end = datetime.fromisoformat(end_time.replace("Z",""))
            days_left = (end - datetime.utcnow()).days
            if days_left < 7:
                score += SCORE_WEIGHTS["has_end_time"]
                reasons.append(f"-10 sap het han ({days_left}ngay)")
        except:
            pass

    # Status dang chay
    if camp.get("status") == 1:
        score += 5
        reasons.append("+5 dang chay")

    return score, reasons


def fetch_all_campaigns(access_key, limit=50):
    headers = {
        "Authorization": f"Token {access_key}",
        "Content-Type": "application/json"
    }
    results = []
    # Lay campaign da duoc duyet
    r = requests.get(f"{AT_API}/campaigns", headers=headers,
                     params={"approval": "successful", "limit": limit}, timeout=15)
    if r.status_code == 200:
        results.extend(r.json().get("data", []))
    return results, headers


def create_tracking_link(headers, campaign_id, url=None, utm_source="sen_v3"):
    payload = {
        "campaign_id": str(campaign_id),
        "utm_source": utm_source,
        "utm_medium": "auto_picker",
        "utm_campaign": f"keo_{campaign_id}"
    }
    if url:
        payload["urls"] = [url]
    r = requests.post(f"{AT_API}/product_link/create",
                      headers=headers, json=payload, timeout=15)
    if r.status_code == 200:
        data = r.json().get("data", {})
        links = data.get("success_link", [])
        if links:
            return {
                "aff_link": links[0].get("aff_link"),
                "short_link": links[0].get("short_link"),
                "url_origin": links[0].get("url_origin")
            }
    return {"error": r.text[:200]}


def auto_pick_and_setup(access_key, top_n=5, auto_create_link=True):
    print("\\n" + "="*55)
    print("  AUTO CAMPAIGN PICKER — SEN V3")
    print("="*55)

    # 1. Fetch campaigns
    print("\\n[1/3] Dang scan tat ca campaign...")
    campaigns, headers = fetch_all_campaigns(access_key)
    print(f"  Tim thay {len(campaigns)} campaign duoc duyet")

    if not campaigns:
        print("  CANH BAO: Chua co campaign nao duoc duyet!")
        print("  -> Vao https://pub2.accesstrade.vn/ dang ky campaign")
        return []

    # 2. Cham diem
    print("\\n[2/3] Cham diem va xep hang keo...")
    scored = []
    for c in campaigns:
        score, reasons = score_campaign(c)
        scored.append({
            "id": c.get("id"),
            "name": c.get("name"),
            "merchant": c.get("merchant"),
            "approval": c.get("approval"),
            "url": c.get("url"),
            "cookie_days": (c.get("cookie_duration") or 0) // 86400,
            "score": score,
            "reasons": reasons,
            "end_time": c.get("end_time")
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[:top_n]

    # 3. Hien thi bang xep hang
    print(f"\\n TOP {top_n} KEO TOT NHAT:\\n")
    print(f"  {'#':<3} {'DIEM':<6} {'MERCHANT':<20} {'TEN CAMPAIGN':<35} {'APPROVAL'}")
    print("  " + "-"*85)
    for i, c in enumerate(top, 1):
        approval_icon = "✅" if c["approval"] == "successful" else "⏳"
        print(f"  {i:<3} {c['score']:<6} {c['merchant']:<20} {c['name'][:34]:<35} {approval_icon} {c['approval']}")
        for r in c["reasons"]:
            print(f"       └ {r}")

    # 4. Tu dong tao tracking link cho top keo
    if auto_create_link:
        print("\\n[3/3] Tu dong tao tracking link cho top keo...")
        results = []
        for c in top:
            if c["approval"] == "successful":
                print(f"  Dang tao link cho: {c['name']}...")
                link_info = create_tracking_link(
                    headers,
                    campaign_id=c["id"],
                    url=c.get("url"),
                    utm_source="sen_v3_auto"
                )
                c["tracking"] = link_info
                if "aff_link" in link_info:
                    print(f"  ✅ {c['merchant']}: {link_info.get('short_link') or link_info.get('aff_link','')[:60]}")
                else:
                    print(f"  ❌ Loi: {link_info}")
                results.append(c)

        # Luu ket qua vao file
        out_file = "fullwork/affiliate/active_campaigns.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump({
                "updated_at": datetime.now().isoformat(),
                "total": len(results),
                "campaigns": results
            }, f, ensure_ascii=False, indent=2)
        print(f"\\n  Luu ket qua vao: {out_file}")
        return results

    return top
""".strip(),
)

# ---- run_picker.py — file chay truc tiep ----
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
    print("Chua dien ACCESS_KEY! Sua trong file run_picker.py")
    print("Lay key tai: https://pub.accesstrade.vn/accounts/profile")
    sys.exit(1)

results = auto_pick_and_setup(
    access_key=ACCESS_KEY,
    top_n=5,              # So keo muon xem
    auto_create_link=True # Tu dong tao tracking link
)

print("\\n=== KET QUA CUOI CUNG ===")
print(f"Da setup {len(results)} keo san sang chay:")
for c in results:
    t = c.get("tracking", {})
    short = t.get("short_link") or t.get("aff_link","")
    print(f"  [{c['score']} diem] {c['name']}")
    print(f"    Link: {short[:80] if short else 'Loi tao link'}")

print("\\nLink da luu tai: fullwork/affiliate/active_campaigns.json")
print("Mo file do de copy link va bat dau promote!")
""".strip(),
)

print("\\nFile da tao xong!")
print("Chay: notepad run_picker.py  (dien key vao)")
print("Sau do: python run_picker.py")
