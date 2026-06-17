from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

class DOMAgent:
    """Agent phân tích DOM, không cần AI vision, nhanh hơn"""
    
    def find_post_button_by_text(self, driver):
        """Tìm nút đăng bằng text với nhiều biến thể"""
        
        text_variants = ["Đăng", "Post", "Share", "Chia sẻ", "Publish"]
        
        for text in text_variants:
            try:
                # Tìm button có text
                btn = driver.find_element(By.XPATH, f"//div[@role='button'][contains(., '{text}')]")
                if btn.is_displayed() and btn.is_enabled():
                    return btn
            except:
                pass
        
        # Tìm bằng aria-label
        try:
            btn = driver.find_element(By.XPATH, "//div[@aria-label='Đăng' or @aria-label='Post']")
            return btn
        except:
            pass
        
        return None
    
    def find_post_box_by_attributes(self, driver):
        """Tìm ô đăng bài bằng nhiều thuộc tính"""
        
        attributes = [
            'aria-label="Tạo bài viết"',
            'aria-label="Create a post"',
            'data-testid="status-attachment-mentions-input"'
        ]
        
        for attr in attributes:
            try:
                box = driver.find_element(By.XPATH, f"//div[@{attr}]")
                return box
            except:
                pass
        
        # Tìm bằng placeholder text
        try:
            box = driver.find_element(By.XPATH, "//*[contains(text(), 'Bạn đang nghĩ gì') or contains(text(), 'What\'s on your mind')]")
            return box
        except:
            pass
        
        return None
