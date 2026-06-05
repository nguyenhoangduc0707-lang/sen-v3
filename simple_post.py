print("Starting to create posts...")

links = ["https://shorten.asia/3cSC6EUX", "https://shorten.asia/PjYek8R8", "https://shorten.asia/MxvRDqNg"]

for i, link in enumerate(links, 1):
    post = f"""
========================================
POST {i}
========================================

SHOPEE MEGA SALE 6.6

- Discount up to 50%
- Free shipping 0Đ
- Voucher up to 6 million
- Buy now pay later 0%

SHOP NOW:
{link}

#Shopee6_6 #MegaSale #Affiliate

"""
    with open(f"post_{i}.txt", "w", encoding="utf-8") as f:
        f.write(post)
    print(f"Created: post_{i}.txt")

print(f"\nDone! Created {len(links)} posts")