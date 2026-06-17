import sqlite3
import pandas as pd
from datetime import datetime, timedelta

class SENV3Database:
    def __init__(self, db_path='sen_v3.db'):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Kết nối đến database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        print(f"✅ Kết nối thành công: {self.db_path}")
        return self.conn
    
    def get_table_names(self):
        """Lấy danh sách tất cả bảng"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        return [row[0] for row in cursor.fetchall()]
    
    def query_table(self, table_name, limit=10):
        """Truy vấn dữ liệu từ một bảng"""
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return pd.read_sql_query(query, self.conn)
    
    def get_table_stats(self, table_name):
        """Thống kê một bảng"""
        cursor = self.conn.cursor()
        
        # Tổng số dòng
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_rows = cursor.fetchone()[0]
        
        # Thông tin cột
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        return {
            'table_name': table_name,
            'total_rows': total_rows,
            'columns': [col[1] for col in columns],
            'column_count': len(columns)
        }
    
    def export_to_excel(self, table_name, output_file=None):
        """Xuất bảng ra file Excel"""
        df = self.query_table(table_name, limit=10000)  # Giới hạn 10k dòng để tránh quá tải
        if output_file is None:
            output_file = f"{table_name}_export.xlsx"
        df.to_excel(output_file, index=False)
        print(f"✅ Đã xuất {len(df)} dòng ra {output_file}")
        return output_file
    
    def get_recent_records(self, table_name, days=7):
        """Lấy các bản ghi trong khoảng thời gian"""
        # Thử tìm cột ngày tháng
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        date_columns = [col for col in columns if 'date' in col.lower() or 'time' in col.lower()]
        
        if not date_columns:
            print(f"⚠️ Không tìm thấy cột ngày tháng trong bảng {table_name}")
            return None
        
        date_col = date_columns[0]
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        query = f"""
        SELECT * FROM {table_name} 
        WHERE {date_col} >= '{cutoff_date}'
        ORDER BY {date_col} DESC
        LIMIT 100
        """
        
        return pd.read_sql_query(query, self.conn)
    
    def close(self):
        """Đóng kết nối"""
        if self.conn:
            self.conn.close()
            print("🔒 Đã đóng kết nối")

# Hàm tương tác
def interactive_sen_v3():
    db = SENV3Database()
    db.connect()
    
    print("\n🔍 SEN_V3.DB - TRÌNH DUYỆT DỮ LIỆU")
    print("="*50)
    
    tables = db.get_table_names()
    print(f"\n📋 Các bảng trong database:")
    for i, table in enumerate(tables, 1):
        stats = db.get_table_stats(table)
        print(f"   {i}. {table} ({stats['total_rows']:,} dòng)")
    
    while True:
        print("\n" + "-"*50)
        print("1. Xem nội dung bảng")
        print("2. Xuất bảng ra Excel")
        print("3. Xem dữ liệu mới nhất (7 ngày)")
        print("4. Thoát")
        
        choice = input("\nChọn chức năng (1-4): ").strip()
        
        if choice == '1':
            table_name = input("Nhập tên bảng: ").strip()
            if table_name in tables:
                df = db.query_table(table_name)
                print(f"\n📊 {len(df)} dòng đầu tiên:")
                print(df)
            else:
                print(f"❌ Không tìm thấy bảng {table_name}")
        
        elif choice == '2':
            table_name = input("Nhập tên bảng: ").strip()
            if table_name in tables:
                db.export_to_excel(table_name)
            else:
                print(f"❌ Không tìm thấy bảng {table_name}")
        
        elif choice == '3':
            table_name = input("Nhập tên bảng: ").strip()
            if table_name in tables:
                df = db.get_recent_records(table_name)
                if df is not None and not df.empty:
                    print(f"\n📊 {len(df)} bản ghi mới nhất:")
                    print(df)
            else:
                print(f"❌ Không tìm thấy bảng {table_name}")
        
        elif choice == '4':
            break
        
        else:
            print("❌ Lựa chọn không hợp lệ")
    
    db.close()

if __name__ == "__main__":
    interactive_sen_v3()
