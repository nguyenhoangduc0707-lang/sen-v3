import asyncio
from playwright.async_api import async_playwright

async def find_products():
    print("🔍 Searching for products on Lazada...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Search for popular products
        search_terms = ["điện thoại", "laptop", "tai nghe", "smartphone"]
        
        all_skus = []
        
        for term in search_terms:
            print(f"\n📝 Searching: {term}")
            search_url = f"https://www.lazada.vn/catalog/?q={term}"
            
            try:
                await page.goto(search_url, timeout=30000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                
                # Get product links
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
                    # Extract SKU
                    import re
                    match = re.search(r'/products/([^/?]+)', link)
                    if match:
                        sku = match.group(1)
                        all_skus.append(sku)
                        print(f"   ✅ Found SKU: {sku}")
                        
            except Exception as e:
                print(f"   ⚠️ Error: {e}")
        
        await browser.close()
        
        print(f"\n📦 Total SKUs found: {len(all_skus)}")
        
        # Test each SKU
        print("\n🧪 Testing SKUs...")
        for sku in all_skus[:5]:  # Test first 5
            test_url = f"https://lazada.vn/products/{sku}"
            print(f"\n   Testing: {sku}")
            print(f"   URL: {test_url}")
            
    return all_skus

async def main():
    print("=" * 60)
    print("Lazada SKU Finder")
    print("=" * 60)
    
    skus = await find_products()
    
    print("\n" + "=" * 60)
    print("✅ Done! You can use these SKUs:")
    for sku in skus[:10]:
        print(f"   {sku}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
