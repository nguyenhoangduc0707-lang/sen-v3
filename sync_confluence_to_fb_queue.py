"""
Script: Đồng bộ nội dung đã approve từ Confluence vào Task Queue để đăng Facebook.

Cách dùng:
1. Trong Confluence, tạo các trang content với:
   - Label: "fb-approved"
   - Dùng Page Properties macro để set:
     - fanpage-key: "affiliate_fashion_cosmetics" hoặc "motivational_postcard"
     - scheduled-date: 2026-06-10 (hoặc dùng label + custom field)
     - theme: "affiliate" hoặc "motivational"

2. Chạy script này (sau khi đã set env vars):
   python sync_confluence_to_fb_queue.py

3. Sau đó chạy:
   python run_scheduled_posts.py --once   (hoặc để scheduled runner tự động)

Script sẽ:
- Tìm các trang approved chưa posted
- Tạo task facebook_autoposter trong queue với nội dung từ Confluence
- Đánh dấu trang là "posted" (thêm label "posted")

Yêu cầu: pip install requests (đã có trong requirements)
"""
import os
from datetime import datetime
from src.confluence_client import ConfluenceClient
from src.task_queue_db import TaskQueueDB

def main():
    print("=== Sync Confluence approved content to FB posting queue ===")

    try:
        confluence = ConfluenceClient()
    except Exception as e:
        print(f"❌ Lỗi kết nối Confluence: {e}")
        print("   Hãy set các biến môi trường:")
        print("   CONFLUENCE_BASE_URL=https://xxx.atlassian.net/wiki")
        print("   CONFLUENCE_EMAIL=your@email.com")
        print("   CONFLUENCE_API_TOKEN=ATATT...")
        print("   CONFLUENCE_SPACE_KEY=ABC")
        return

    q = TaskQueueDB()

    # Tìm nội dung đã approve
    print("Đang tìm trang đã approve trong Confluence...")
    pages = confluence.find_approved_fb_content(days_ahead=14)

    if not pages:
        print("Không tìm thấy trang nào phù hợp.")
        return

    print(f"Tìm thấy {len(pages)} trang sẵn sàng.")

    for page in pages:
        page_id = page["id"]
        title = page["title"]

        # Lấy nội dung
        body = confluence.get_page_content(page_id)

        # Lấy metadata từ page properties (nếu dùng Page Properties macro)
        props = confluence.get_page_properties(page_id)
        fanpage_key = props.get("fanpage-key") or props.get("fanpage_key") or "affiliate_fashion_cosmetics"
        theme = props.get("theme", "affiliate")
        scheduled_date = props.get("scheduled-date") or props.get("scheduled_date")

        # Tạo payload cho FB task
        payload = {
            "content": body,           # HTML từ Confluence, FB poster sẽ xử lý text
            "fanpage_key": fanpage_key,
            "theme": theme,
            "confluence_page_id": page_id,
            "confluence_title": title,
            "source": "confluence"
        }

        if scheduled_date:
            payload["scheduled_at"] = scheduled_date   # format YYYY-MM-DD or full ISO

        # Enqueue vào queue
        task_id = q.add_task(
            category="confluence-fb-post",
            worker_name="facebook_autoposter",
            payload=payload
        )

        print(f"  ✓ Enqueued task #{task_id} from Confluence page '{title}' (id={page_id}) → {fanpage_key}")

        # Đánh dấu đã đưa vào queue (tránh duplicate)
        confluence.mark_as_posted(page_id)

    print("\n✅ Hoàn tất sync. Chạy 'python run_scheduled_posts.py --once' để đăng các bài đã schedule.")

if __name__ == "__main__":
    main()