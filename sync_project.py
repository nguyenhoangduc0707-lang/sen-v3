import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

class ProjectSync:
    def __init__(self):
        self.project_root = Path.cwd()
        self.issues = []
        self.success = []
        
    def check_python_version(self):
        print("🐍 Kiểm tra Python...")
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            self.success.append(f"Python {version.major}.{version.minor}")
            return True
        else:
            self.issues.append("Python < 3.8")
            return False
    
    def check_environment_file(self):
        print("📄 Kiểm tra .env...")
        env_file = self.project_root / '.env'
        if env_file.exists():
            self.success.append(".env tồn tại")
            # Kiểm tra các biến cần thiết
            required_vars = ['GEMINI_API_KEY', 'ACCESS_TRADE_API_KEY']
            with open(env_file, 'r') as f:
                content = f.read()
                for var in required_vars:
                    if var in content and 'your_' not in content:
                        self.success.append(f"{var} đã cấu hình")
                    else:
                        self.issues.append(f"{var} chưa cấu hình")
            return True
        else:
            self.issues.append(".env chưa tạo")
            return False
    
    def check_database(self):
        print("🗄️ Kiểm tra Database...")
        databases = ['app.db', 'sen_v3.db']
        for db in databases:
            db_path = self.project_root / db
            if db_path.exists():
                size = db_path.stat().st_size / 1024
                self.success.append(f"{db} ({size:.1f} KB)")
            else:
                self.issues.append(f"{db} không tồn tại")
    
    def check_directories(self):
        print("📁 Kiểm tra thư mục...")
        required_dirs = ['src', 'web', 'config', 'logs', 'backups', 'tools', 'scripts']
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                self.success.append(f"{dir_name}/")
            else:
                self.issues.append(f"{dir_name}/ chưa tạo")
    
    def check_git_ignore(self):
        print("🔒 Kiểm tra .gitignore...")
        gitignore = self.project_root / '.gitignore'
        if gitignore.exists():
            self.success.append(".gitignore tồn tại")
            return True
        else:
            self.issues.append(".gitignore chưa tạo")
            return False
    
    def run_migrations(self):
        print("🔄 Kiểm tra migrations...")
        alembic_dir = self.project_root / 'alembic'
        if alembic_dir.exists():
            self.success.append("alembic/ tồn tại")
            # Kiểm tra migrations
            versions_dir = alembic_dir / 'versions'
            if versions_dir.exists():
                count = len(list(versions_dir.glob('*.py')))
                self.success.append(f"{count} migrations")
        else:
            self.issues.append("alembic/ chưa tạo")
    
    def generate_report(self):
        print("\n" + "="*60)
        print("📊 BÁO CÁO ĐỒNG BỘ DỰ ÁN")
        print("="*60)
        print(f"📁 Dự án: {self.project_root.name}")
        print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("✅ THÀNH CÔNG:")
        for item in self.success:
            print(f"   ✓ {item}")
        
        if self.issues:
            print()
            print("⚠️ CẦN XỬ LÝ:")
            for item in self.issues:
                print(f"   ✗ {item}")
            print()
            print("📋 HƯỚNG DẪN:")
            print("   1. Tạo file .env với API keys")
            print("   2. Chạy: pip install -r requirements.txt")
            print("   3. Chạy: python gemini_analyzer.py")
        else:
            print()
            print("✅ MỌI THỨ ĐÃ SẴN SÀNG!")
            print("   Chạy: python gemini_analyzer.py")
    
    def run(self):
        print("🔄 ĐỒNG BỘ HÓA DỰ ÁN")
        print("="*60)
        
        self.check_python_version()
        self.check_environment_file()
        self.check_database()
        self.check_directories()
        self.check_git_ignore()
        self.run_migrations()
        self.generate_report()

if __name__ == "__main__":
    sync = ProjectSync()
    sync.run()
