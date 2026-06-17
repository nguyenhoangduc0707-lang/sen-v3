import sqlite3
import pandas as pd
from datetime import datetime

def analyze_sen_v3():
    db_path = 'sen_v3.db'
    
    if not __import__('os').path.exists(db_path):
        print(f"❌ Không tìm thấy file: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔍 PHÂN TÍCH SEN_V3.DB")
    print("="*60)
    print(f"🕐 Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 File: {db_path}")
    
    # Lấy danh sách tất cả bảng
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()
    
    print(f"\n📊 Tổng số bảng: {len(tables)}")
    print("-"*60)
    
    table_stats = []
    for table in tables:
        table_name = table[0]
        
        # Đếm số dòng
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        
        # Lấy schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        col_names = [col[1] for col in columns]
        
        table_stats.append({
            'name': table_name,
            'rows': count,
            'columns': len(columns),
            'col_names': col_names
        })
        
        print(f"\n📋 Bảng: {table_name}")
        print(f"   Số dòng: {count:,}")
        print(f"   Số cột: {len(columns)}")
        print(f"   Các cột: {', '.join(col_names[:5])}{'...' if len(col_names) > 5 else ''}")
        
        # Hiển thị vài dòng dữ liệu mẫu
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
            sample = cursor.fetchall()
            print(f"   Dữ liệu mẫu: {len(sample)} dòng")
    
    # Tìm bảng có dữ liệu nhiều nhất
    if table_stats:
        max_table = max(table_stats, key=lambda x: x['rows'])
        print("\n" + "="*60)
        print(f"🏆 BẢNG CÓ NHIỀU DỮ LIỆU NHẤT")
        print(f"   📋 {max_table['name']}")
        print(f"   📊 {max_table['rows']:,} dòng")
        print(f"   📝 {max_table['columns']} cột")
    
    conn.close()
    print("\n✅ PHÂN TÍCH HOÀN TẤT!")

if __name__ == "__main__":
    analyze_sen_v3()
