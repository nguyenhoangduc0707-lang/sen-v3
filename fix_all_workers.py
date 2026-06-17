import os
import re
from pathlib import Path

print("🔧 FIX TẤT CẢ WORKER IMPORTS")
print("="*40)

# Duyệt tất cả file trong src/workers
workers_dir = Path('src/workers')
for file_path in workers_dir.glob('*.py'):
    if file_path.name == '__init__.py':
        continue
    
    print(f"📄 Đang xử lý: {file_path.name}")
    
    # Đọc nội dung
    content = file_path.read_text(encoding='utf-8', errors='ignore')
    
    # Sửa import
    new_content = content.replace(
        'from content_creation_agent import create_article',
        'from src.content_creation_agent import create_article'
    )
    new_content = new_content.replace(
        'from content_creation_agent import',
        'from src.content_creation_agent import'
    )
    
    # Ghi lại
    if new_content != content:
        file_path.write_text(new_content, encoding='utf-8')
        print(f"   ✅ Đã sửa import")

print("\n✅ Hoàn tất!")
