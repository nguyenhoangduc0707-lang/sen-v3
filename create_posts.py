# -*- coding: utf-8 -*-
print("Dang tao bai viet affiliate...")

# Doc link tu file
with open("affiliate_links.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Lay cac link
links = []
for line in lines:
    if "https://shorten.asia" in line:
        link = line.split(": ")[-1].strip()
        links.append(link)

print(f"Tim thay {len(links)} link")

# Tao bai viet cho tung link
for idx, link in enumerate(links, 1):
    content = f"""Bai viet affiliate {idx}

Chuong trinh: SHOPEE 6.6 MEGA SALE
Uu dai: Giam gia 50% + Freeship 0D
Link mua hang: {link}

Hashtag: #Shopee6_6 #Affiliate #Sale
"""
    filename = f"affiliate_post_{idx}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Da tao: {filename}")

print(f"\nHoan tat! Da tao {len(links)} bai viet")