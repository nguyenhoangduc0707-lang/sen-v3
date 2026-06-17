import sys
import os

# Thêm thư mục gốc vào path
sys.path.insert(0, os.getcwd())

# Kiểm tra import
try:
    from src.content_creation_agent import create_article
    print('✅ Import thành công từ src.content_creation_agent')
except ImportError as e:
    print(f'❌ Lỗi import: {e}')
    
# Kiểm tra worker
try:
    from src.workers.shopee_worker import ShopeeWorker
    print('✅ Import ShopeeWorker thành công')
except ImportError as e:
    print(f'❌ Lỗi import ShopeeWorker: {e}')
