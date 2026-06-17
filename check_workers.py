import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

print("👷 WORKER STATUS")
print("="*40)

workers = cursor.execute("""
    SELECT id, name, status, last_heartbeat, version
    FROM workers
    ORDER BY id
""").fetchall()

for worker in workers:
    status_icon = "✅" if worker[2] == 'active' else "❌" if worker[2] == 'error' else "⚠️"
    print(f"{status_icon} {worker[1]} (v{worker[4]}) - {worker[2]}")
    print(f"   Last heartbeat: {worker[3]}")
    print()

conn.close()
