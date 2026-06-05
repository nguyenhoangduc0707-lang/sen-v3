import psycopg2
from content_creation_agent import create_article

class ShopeeWorker:
    def run(self, **kwargs):
        # Hỗ trợ nhận campaign_id hoặc url trực tiếp
        campaign_id = kwargs.get("campaign_id")
        url = kwargs.get("url")
        
        if campaign_id:
            # Lấy thông tin từ bảng campaigns
            try:
                conn = psycopg2.connect(
                    host="localhost",
                    port=5432,
                    database="sen_v3",
                    user="sen_user",
                    password="sen_pass"
                )
                cur = conn.cursor()
                cur.execute("""
                    SELECT name, commission_rate, commission_fixed, cpc_price, description, url
                    FROM campaigns
                    WHERE id = %s
                """, (campaign_id,))
                row = cur.fetchone()
                cur.close()
                conn.close()
                
                if not row:
                    return {"status": "error", "summary": f"Campaign {campaign_id} not found"}
                
                name, commission_rate, commission_fixed, cpc_price, description, db_url = row
                url = url or db_url
                
                # Xác định loại hoa hồng
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
                    "description": description or "",
                    "url": url or ""
                }
                
            except Exception as e:
                return {"status": "error", "summary": f"DB error: {str(e)}"}
        
        elif url:
            # Nếu chỉ có url, tạo thông tin tối thiểu (có thể mở rộng sau)
            campaign_info = {
                "name": "Sản phẩm Shopee",
                "commission_display": "10%",
                "description": "",
                "url": url
            }
        else:
            return {"status": "error", "summary": "Missing campaign_id or url"}
        
        # Gọi hàm tạo nội dung (dùng Groq)
        try:
            content = create_article(campaign_info)
            return {
                "status": "ok",
                "summary": content,
                "data": {
                    "url": campaign_info.get("url"),
                    "provider": "groq"
                }
            }
        except Exception as e:
            return {"status": "error", "summary": f"Content generation failed: {str(e)}"}
