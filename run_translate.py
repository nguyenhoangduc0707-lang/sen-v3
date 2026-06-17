import os
import subprocess
import sys
from pathlib import Path

def run_live_translate():
    """Chạy live translation với các tùy chọn"""
    
    print("🌐 DỊCH THUẬT THỜI GIAN THỰC")
    print("="*50)
    print("1. Dịch từ mic và camera")
    print("2. Dịch từ mic (không camera)")
    print("3. Dịch văn bản (text-to-text)")
    print("4. Thoát")
    print("-"*50)
    
    choice = input("Chọn chế độ (1-4): ").strip()
    
    if choice == "1":
        subprocess.run([sys.executable, "live_translate.py", "--mode", "camera"])
    elif choice == "2":
        subprocess.run([sys.executable, "live_translate.py", "--mode", "none"])
    elif choice == "3":
        # Sử dụng text translation
        from text_translate import translate_text
        translate_text()
    elif choice == "4":
        print("👋 Tạm biệt!")
    else:
        print("❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    run_live_translate()
