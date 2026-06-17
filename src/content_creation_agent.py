# content_creation_agent.py
def create_article(campaign_info):
    if not campaign_info:
        return "Không có thông tin sản phẩm"
    
    name = campaign_info.get('name', 'Sản phẩm')
    commission = campaign_info.get('commission_display', '10%')
    description = campaign_info.get('description', '')
    url = campaign_info.get('url', '')
    
    article = f"""
🌟 SẢN PHẨM HOT 🌟

📦 {name}
💰 Hoa hồng: {commission}

📝 Mô tả: {description if description else 'Sản phẩm chất lượng cao'}

🔗 Link: {url if url else '#'}

#Shopee #Affiliate
"""
    return article
