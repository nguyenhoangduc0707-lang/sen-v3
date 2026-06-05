import sqlite3
from content_creation_agent import create_article

class ContentWorker:
    def run(self, **kwargs):
        campaign_id = kwargs.get("campaign_id")
        if not campaign_id:
            return {"status": "error", "summary": "Missing campaign_id"}
        
        try:
            conn = sqlite3.connect('sen_v3.db')
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("""
                SELECT name, commission_rate, commission_fixed, cpc_price, description
                FROM campaigns
                WHERE id = ?
            """, (campaign_id,))
            row = cur.fetchone()
            cur.close()
            conn.close()
            
            if not row:
                return {"status": "error", "summary": f"Campaign {campaign_id} not found"}
            
            name = row["name"]
            commission_rate = row["commission_rate"]
            commission_fixed = row["commission_fixed"]
            cpc_price = row["cpc_price"]
            description = row["description"] or ""
            
            if commission_rate is not None:
                commission_display = f"{commission_rate}%"
            elif commission_fixed is not None:
                commission_display = f"{commission_fixed:,.0f} VND"
            elif cpc_price is not None:
                commission_display = f"{cpc_price} VND/click"
            else:
                commission_display = "0"
            
            campaign_info = {
                "name": name,
                "commission_display": commission_display,
                "description": description
            }
            
            content = create_article(campaign_info)
            return {"status": "ok", "summary": content}
            
        except Exception as e:
            return {"status": "error", "summary": f"DB error: {str(e)}"}
