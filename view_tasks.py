import sqlite3
import json

def view_results():
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    # Thống kê
    cursor.execute('''
        SELECT status, COUNT(*) 
        FROM tasks 
        GROUP BY status
    ''')
    
    print("=" * 60)
    print("📊 Task Statistics:")
    print("=" * 60)
    for status, count in cursor.fetchall():
        print(f"   {status}: {count}")
    
    # Chi tiết tasks
    cursor.execute('''
        SELECT id, task_type, status, result, created_at 
        FROM tasks 
        ORDER BY id DESC
    ''')
    
    print("\n" + "=" * 60)
    print("📋 Task Details:")
    print("=" * 60)
    
    for row in cursor.fetchall():
        task_id, task_type, status, result, created_at = row
        print(f"\n🔹 Task #{task_id}: {task_type}")
        print(f"   Status: {status}")
        print(f"   Created: {created_at}")
        
        if result and (status == 'completed' or status == 'failed'):
            try:
                result_data = json.loads(result)
                if result_data.get('success'):
                    product = result_data.get('product', {})
                    print(f"   ✅ Product: {product.get('name', 'N/A')[:70]}")
                    print(f"   💰 Price: {product.get('price', 'N/A')}")
                    print(f"   🔗 Affiliate: {product.get('affiliate_link', 'N/A')[:60]}")
                else:
                    print(f"   ❌ Error: {result_data.get('error', 'Unknown')}")
            except:
                print(f"   📝 Result: {str(result)[:100]}")
    
    conn.close()

if __name__ == "__main__":
    view_results()
