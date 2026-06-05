"""
Find active products on Lazada using Playwright
"""
import asyncio
from playwright.async_api import async_playwright

async def find_active_products():
    print("=" * 60)
    print("🔍 Tìm kiếm sản phẩm đang bán trên Lazada")
    print("=" * 60)
    
    products = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Các từ khóa tìm kiếm
        keywords = ["điện thoại", "laptop", "tai nghe", "áo sơ mi"]
        
        for keyword in keywords:
            print(f"\n🔎 Tìm kiếm: {keyword}")
            
            search_url = f"https://www.lazada.vn/catalog/?q={keyword.replace(' ', '+')}"
            
            try:
                await page.goto(search_url, timeout=30000, wait_until="networkidle")
                await page.wait_for_timeout(3000)
                
                # Lấy các link sản phẩm
                product_links = await page.evaluate('''
                    () => {
                        const links = [];
                        const items = document.querySelectorAll('a[href*="/products/"]');
                        items.forEach(item => {
                            let href = item.getAttribute('href');
                            if (href && !href.includes('catalog')) {
                                links.push(href.startsWith('/') ? 'https://www.lazada.vn' + href : href);
                            }
                        });
                        return [...new Set(links)].slice(0, 3);
                    }
                ''')
                
                for link in product_links:
                    print(f"\n   📦 URL: {link}")
                    
                    # Lấy chi tiết sản phẩm
                    try:
                        await page.goto(link, timeout=30000, wait_until="networkidle")
                        
                        # Lấy tên
                        name = await page.evaluate('''
                            () => {
                                const selectors = ['h1', '[data-qa="product-name"]', '.pdp-product-title'];
                                for (let sel of selectors) {
                                    const el = document.querySelector(sel);
                                    if (el && el.innerText) return el.innerText.trim();
                                }
                                return null;
                            }
                        ''')
                        
                        # Lấy giá
                        price = await page.evaluate('''
                            () => {
                                const selectors = ['[data-qa="price"]', '.pdp-price', '.price'];
                                for (let sel of selectors) {
                                    const el = document.querySelector(sel);
                                    if (el && el.innerText) {
                                        const text = el.innerText;
                                        const match = text.match(/[\\d,.]+/);
                                        if (match) return match[0];
                                    }
                                }
                                return null;
                            }
                        ''')
                        
                        if name:
                            print(f"      ✅ Tên: {name[:80]}")
                            print(f"      💰 Giá: {price} VND" if price else "      💰 Giá: N/A")
                            
                            # Lưu sản phẩm
                            products.append({
                                'name': name,
                                'url': link,
                                'price': price,
                                'keyword': keyword
                            })
                        else:
                            print(f"      ⚠️ Không thể lấy thông tin")
                            
                    except Exception as e:
                        print(f"      ❌ Lỗi: {e}")
                    
                    await asyncio.sleep(1)
                    
            except Exception as e:
                print(f"   ❌ Lỗi tìm kiếm: {e}")
            
            await asyncio.sleep(2)
        
        await browser.close()
    
    # Hiển thị kết quả
    print("\n" + "=" * 60)
    print(f"📊 KẾT QUẢ: Tìm thấy {len(products)} sản phẩm")
    print("=" * 60)
    
    for i, p in enumerate(products, 1):
        print(f"\n{i}. {p['name'][:100]}")
        print(f"   URL: {p['url']}")
        print(f"   Giá: {p['price'] if p['price'] else 'N/A'} VND")
    
    # Lưu vào file
    import json
    with open('active_products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Đã lưu {len(products)} sản phẩm vào active_products.json")
    print("=" * 60)
    
    return products

async def main():
    try:
        products = await find_active_products()
        if not products:
            print("\n⚠️ Không tìm thấy sản phẩm nào.")
            print("💡 Gợi ý: Website Lazada có thể đã thay đổi cấu trúc.")
            print("   Hãy thử truy cập thủ công: https://www.lazada.vn")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")

if __name__ == "__main__":
    asyncio.run(main())
