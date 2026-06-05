"""
Full System Report - All Workers Data
"""
import sqlite3
import json
from datetime import datetime

def generate_full_report():
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "workers": [],
        "tasks": {},
        "sales": {},
        "campaigns": {},
        "errors": []
    }
    
    # 1. Worker stats
    cursor.execute("SELECT worker_name, tasks_processed, tasks_succeeded, tasks_failed, status FROM worker_stats")
    for row in cursor.fetchall():
        report["workers"].append({
            "name": row[0],
            "processed": row[1],
            "succeeded": row[2],
            "failed": row[3],
            "status": row[4]
        })
    
    # 2. Task summary
    cursor.execute("SELECT task_type, status, COUNT(*) FROM tasks GROUP BY task_type, status")
    for row in cursor.fetchall():
        key = f"{row[0]}_{row[1]}"
        report["tasks"][key] = row[2]
    
    # 3. Sales summary
    cursor.execute("""
        SELECT 
            SUM(revenue) as total_revenue,
            SUM(commission) as total_commission,
            SUM(clicks) as total_clicks,
            SUM(orders) as total_orders
        FROM sales_tracking
    """)
    sales = cursor.fetchone()
    report["sales"] = {
        "total_revenue": sales[0] or 0,
        "total_commission": sales[1] or 0,
        "total_clicks": sales[2] or 0,
        "total_orders": sales[3] or 0
    }
    
    # 4. Campaign counts
    cursor.execute("SELECT COUNT(*) FROM accesstrade_campaigns")
    report["campaigns"]["accesstrade"] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM acfc_promotions WHERE status = 'active'")
    report["campaigns"]["acfc_active"] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM lazada_products")
    report["campaigns"]["lazada"] = cursor.fetchone()[0]
    
    # 5. Failed tasks
    cursor.execute("SELECT id, task_type, result FROM tasks WHERE status = 'failed' LIMIT 10")
    for row in cursor.fetchall():
        report["errors"].append({
            "task_id": row[0],
            "task_type": row[1],
            "result": row[2]
        })
    
    conn.close()
    
    # Save report
    with open('full_system_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("=" * 70)
    print("📊 FULL SYSTEM REPORT GENERATED")
    print("=" * 70)
    print(f"\n👷 WORKERS: {len(report['workers'])}")
    for w in report['workers']:
        print(f"   ✅ {w['name']}: {w['succeeded']}/{w['processed']} success ({w['status']})")
    
    print(f"\n💰 SALES SUMMARY:")
    print(f"   💰 Revenue: {report['sales']['total_revenue']:,.0f} VND")
    print(f"   🎁 Commission: {report['sales']['total_commission']:,.0f} VND")
    print(f"   👆 Clicks: {report['sales']['total_clicks']:,}")
    print(f"   📦 Orders: {report['sales']['total_orders']:,}")
    
    print(f"\n📈 SUCCESS RATE:")
    total_tasks = sum(report['tasks'].values())
    completed = sum(v for k, v in report['tasks'].items() if 'completed' in k)
    print(f"   ✅ {completed}/{total_tasks} tasks completed ({completed/total_tasks*100:.1f}%)" if total_tasks > 0 else "   ✅ No tasks yet")
    
    print(f"\n📁 Report saved: full_system_report.json")
    print("=" * 70)

if __name__ == "__main__":
    generate_full_report()
