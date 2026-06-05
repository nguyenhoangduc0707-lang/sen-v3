import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup

async def find_active_products():
    print("=" * 60)
    print("🔍 Tìm kiếm sản phẩm đang bán trên Lazada")
    print("=" * 60)
    
    # Các từ khóa tìm kiếm phổ biến
    keywords = ["điện thoại samsung", "laptop dell", "tai nghe bluetooth", "áo thun nam"]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    async with aiohttp.ClientSession() as session:
        for keyword in keywords:
            search_url = f"https://www.lazada.vn/catalog/?q={keyword.replace(' ', '+')}"
            
            try:
                async with session.get(search_url, headers=headers) as resp:
                    if resp.status == 200:
                        html = await resp.text()
                        
                        # Tìm link sản phẩm
                        pattern = r'https://www\.lazada\.vn/products/[^"?\s]+'
                        links = re.findall(pattern, html)
                        
                        # Lọc link unique
                        unique_links = list(set(links))[:3]
                        
                        for link in unique_links:
                            print(f"\n📦 {keyword}:")
                            print(f"   Link: {link}")
                            
                            # Thử lấy thông tin chi tiết
                            async with session.get(link, headers=headers) as product_resp:
                                if product_resp.status == 200:
                                    product_html = await product_resp.text()
                                    
                                    # Lấy tên sản phẩm
                                    title_match = re.search(r'<title>(.*?)</title>', product_html)
                                    if title_match:
                                        title = title_match.group(1).replace('| Lazada.vn', '').strip()
                                        print(f"   Tên: {title[:80]}")
                                    
                                    # Lấy giá
                                    price_match = re.search(r'<span[^>]*class="pdp-price"[^>]*>.*?(\d+(?:[.,]\d+)?)', product_html)
                                    if price_match:
                                        print(f"   Giá: {price_match.group(1)} VND")
                            
                            await asyncio.sleep(1)  # Tránh rate limit
                    
            except Exception as e:
                print(f"❌ Lỗi tìm kiếm {keyword}: {e}")
            
            await asyncio.sleep(2)
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(find_active_products())
