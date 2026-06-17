import os
import sys
from pathlib import Path

print("🔧 FIX MODULES")
print("="*40)

# 1. Tạo __init__.py
for dir_path in ['src', 'src/workers']:
    init_file = Path(dir_path) / '__init__.py'
    if not init_file.exists():
        init_file.touch()
        print(f'✅ Tạo {init_file}')

# 2. Sửa import trong shopee_worker.py
worker_file = Path('src/workers/shopee_worker.py')
if worker_file.exists():
    content = worker_file.read_text(encoding='utf-8')
    # Sửa import
    if 'from content_creation_agent import create_article' in content:
        new_content = content.replace(
            'from content_creation_agent import create_article',
            'from src.content_creation_agent import create_article'
        )
        worker_file.write_text(new_content, encoding='utf-8')
        print('✅ Đã sửa import trong shopee_worker.py')

# 3. Kiểm tra
try:
    from src.workers.shopee_worker import ShopeeWorker
    print('✅ Import ShopeeWorker thành công!')
except ImportError as e:
    print(f'❌ Vẫn còn lỗi: {e}')
