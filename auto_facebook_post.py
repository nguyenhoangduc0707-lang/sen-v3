"""
Auto post to Facebook using Graph API
"""
import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

class FacebookAutoPost:
    def __init__(self):
        self.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.page_id = os.getenv("FACEBOOK_PAGE_ID")
        
    def post_to_page(self, message, link=None):
        """Tự động đăng bài lên Facebook Page"""
        url = f"https://graph.facebook.com/v18.0/{self.page_id}/feed"
        
        data = {
            "message": message,
            "access_token": self.access_token
        }
        if link:
            data["link"] = link
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print(f"✅ Posted to Facebook: {message[:50]}...")
                return True
            else:
                print(f"❌ Facebook error: {response.json()}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def auto_post_all(self, posts, delay=300):
        """Tự động đăng tất cả bài"""
        print(f"🚀 Auto posting {len(posts)} articles to Facebook...")
        
        for i, post in enumerate(posts, 1):
            message = f"{post['content']}\n\n👉 {post['link']}"
            self.post_to_page(message, post['link'])
            
            if i < len(posts):
                print(f"⏰ Waiting {delay}s before next post...")
                time.sleep(delay)
        
        print("✅ All posts published!")

# Tạo bài đăng từ links
def create_posts_from_links():
    with open('auto_links.json', 'r', encoding='utf-8') as f:
        links = json.load(f)
    
    posts = []
    for link in links:
        posts.append({
            'content': f"🔥 {link['name']}\n\n⚡ Ưu đãi đặc biệt dành riêng cho bạn!",
            'link': link['link']
        })
    return posts

if __name__ == "__main__":
    # Cần set FACEBOOK_ACCESS_TOKEN và FACEBOOK_PAGE_ID trong .env
    bot = FacebookAutoPost()
    posts = create_posts_from_links()
    bot.auto_post_all(posts)
