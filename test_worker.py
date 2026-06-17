import sys
import os

# Thêm đường dẫn
sys.path.insert(0, os.getcwd())

print("🚀 CHẠY WORKER (SAFE MODE)")
print("="*40)

try:
    from src.workers.shopee_worker import ShopeeWorker
    print("✅ Import ShopeeWorker thành công")
    
    # Khởi tạo và chạy worker
    worker = ShopeeWorker()
    result = worker.run(name="Test Product")
    print(f"📊 Kết quả: {result}")
    
except Exception as e:
    print(f"❌ Lỗi: {e}")
