# create_affiliate_posts.py
print("Dang tao bai viet affiliate...")

# Danh sach link
links = [
    "https://shorten.asia/3cSC6EUX",
    "https://shorten.asia/PjYek8R8", 
    "https://shorten.asia/MxvRDqNg"
]

# Danh sach chien dich
campaigns = [
    "1.6 Opening Sale",
    "6.6 Mid Year Mega Sale",
    "15.6 Mid-month Sale",
    "25.6 Payday Sale"
]

# Tao bai viet
count = 0
for campaign in campaigns:
    for link in links:
        count += 1
        
        # Noi dung bai viet
        content = f"""========================================
Bai viet {count} - {campaign}
========================================

SHOPEE MEGA SALE 6.6

- Giam gia den 50%
- Freeship 0D toan quoc
- Voucher Xtra len den 6 trieu dong
- Mua truoc tra sau 0%

Dang ky ngay hom nay:
{link}

#Shopee6_6 #MegaSale #Affiliate

"""
        # Luu file
        filename = f"post_{count}_{campaign.replace(' ', '_')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Da tao: {filename}")

print(f"\nHoan tat! Da tao {count} bai viet")