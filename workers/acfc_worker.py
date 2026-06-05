import json
import os
from datetime import datetime

# ??c c?u h?nh
config_path = "E:/DYT_01/acfc_config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

print("=" * 60)
print("??? ACFC AFFILIATE WORKER - T?T C? CHUONG TRINH")
print("=" * 60)
print(f"? Thoi gian chay: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

campaigns = config["campaigns"]
all_links = []

for idx, campaign in enumerate(campaigns, 1):
    print(f"\n?? {idx}. {campaign['name']}")
    print(f"   ?? Link: {campaign['link']}")
    print(f"   ?? Uu dai: {campaign.get('discount', 'Chi tiet xem tai link')}")
    
    if 'code' in campaign:
        print(f"   ?? Ma: {campaign['code']} (DK: {campaign['condition']})")
    
    # Tao link affiliate demo
    affiliate_link = campaign['link']
    if '?' in affiliate_link:
        affiliate_link += "&affiliate=demo_acfc"
    else:
        affiliate_link += "?affiliate=demo_acfc"
    
    all_links.append({
        "name": campaign['name'],
        "link": affiliate_link,
        "discount": campaign.get('discount', ''),
        "code": campaign.get('code', '')
    })
    
    print(f"   ? Link affiliate: {affiliate_link}")

# Luu toan bo link
filename = f"acfc_affiliate_links_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
filepath = f"E:/DYT_01/{filename}"

with open(filepath, "w", encoding="utf-8") as f:
    f.write("=" * 60 + "\n")
    f.write("??? ACFC AFFILIATE LINKS - TAT CA CHUONG TRINH\n")
    f.write(f"?? Ngay tao: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 60 + "\n\n")
    
    for link in all_links:
        f.write(f"?? {link['name']}\n")
        f.write(f"   ?? Link: {link['link']}\n")
        if link['discount']:
            f.write(f"   ?? Uu dai: {link['discount']}\n")
        if link['code']:
            f.write(f"   ?? Ma: {link['code']}\n")
        f.write("\n")

print("\n" + "=" * 60)
print(f"? DA TAO {len(all_links)} LINK AFFILIATE")
print(f"?? Luu tai: {filepath}")
print("=" * 60)

print("\n?? THONG KE CHIEN DICH:")
print(f"   Tong so chuong trinh: {len(all_links)}")
print("   Double 5: Calvin Klein, Tommy, Mango, Guess, Levi's")
print("   Dac biet: Cotton On, Payday, Mid Season, DKNY, Swarovski, Voucher 200K")
print("\n?? DA SAN SANG CHAY VOI API THAT!")

# Mo file ket qua
os.startfile(filepath)
