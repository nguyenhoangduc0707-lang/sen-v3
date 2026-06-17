import subprocess
import sys
import os

def show_menu():
    print("🚀 DYT_01 - AI HUB")
    print("="*50)
    print("1. Phân tích AccessTrade (Gemini)")
    print("2. Dịch văn bản tương tác")
    print("3. Dịch hàng loạt từ Excel")
    print("4. Kiểm tra hệ thống")
    print("5. Backup & Sync")
    print("6. Thoát")
    print("-"*50)
    
    while True:
        choice = input("\nChọn (1-6): ").strip()
        
        if choice == "1":
            subprocess.run([sys.executable, "gemini_analyzer.py"])
        elif choice == "2":
            subprocess.run([sys.executable, "translator.py"])
        elif choice == "3":
            subprocess.run([sys.executable, "batch_translate.py"])
        elif choice == "4":
            subprocess.run([sys.executable, "check_all.py"])
        elif choice == "5":
            subprocess.run([sys.executable, "backup_project.py"])
            subprocess.run([sys.executable, "sync_project.py"])
        elif choice == "6":
            print("👋 Tạm biệt!")
            break
        else:
            print("❌ Chọn lại")

if __name__ == "__main__":
    show_menu()
