"""
Auto setup for banking_finance fanpage entry in config.

Since you currently don't have the banking fanpage yet, this script ensures the entry exists with good default best_posting_times (optimized for banking content, e.g. business hours + evenings).

Run: python auto_setup_banking_fanpage.py

It will:
- Load or create the config.
- Add/update the "banking_finance" entry with sensible defaults.
- Print next steps (you will fill the real URL later when you have the page).

After running, you can still edit the URL in config/fanpages.json.
"""
import json
import os

def main():
    config_path = os.path.join("config", "fanpages.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {}

    # Default good times for banking/finance content (business hours + peak engagement)
    default_banking_times = [8, 9, 12, 17, 18, 19, 20]

    if "banking_finance" not in config:
        config["banking_finance"] = {
            "name": "Tài Chính Ngân Hàng - Vay Tiền Dễ Dàng",
            "url": "https://www.facebook.com/your-banking-fanpage-3",  # TODO: replace with real URL when you create the page
            "theme": "banking",
            "description": "Fanpage về sản phẩm ngân hàng, vay tín chấp, thẻ tín dụng, tài chính cá nhân. Kết hợp động lực và thông tin hữu ích.",
            "style_prompt": "Viết bài về tài chính ngân hàng, nhấn mạnh lợi ích vay nhanh, lãi suất tốt, hỗ trợ tài chính. Kết hợp yếu tố truyền động lực và lời khuyên tài chính. Dùng ngôn từ tin cậy, chuyên nghiệp nhưng dễ hiểu.",
            "best_posting_times": default_banking_times
        }
        print("Added new 'banking_finance' entry with defaults.")
    else:
        # Update times if missing or to ensure good defaults
        config["banking_finance"]["best_posting_times"] = default_banking_times
        print("Updated 'banking_finance' best_posting_times with optimized defaults.")

    # Ensure other keys if not present (for completeness)
    # But assume they are from previous setup

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print("Config updated successfully.")
    print("\nNext steps:")
    print("1. When you create the banking fanpage, open config/fanpages.json and replace the 'url' for 'banking_finance'.")
    print("2. Adjust 'best_posting_times' based on the new page's Insights.")
    print("3. Then use: python schedule_optimized_posts.py --fanpage_key banking_finance --days 3")
    print("\nThe entry is ready for autosetup.")

if __name__ == "__main__":
    main()
