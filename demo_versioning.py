"""
Demo s? d?ng Data Versioning - T?o v? qu?n l? prompt versions
"""
import sqlite3
from datetime import datetime

def demo_versioning():
    print("=" * 60)
    print("?? DATA VERSIONING DEMO")
    print("=" * 60)
    
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    # 1. Xem prompt hi?n t?i
    print("\n?? CURRENT ACTIVE PROMPT:")
    cursor.execute("SELECT id, name, version, system_prompt FROM prompt_templates WHERE is_active=1")
    row = cursor.fetchone()
    if row:
        print(f"   ID: {row[0]}")
        print(f"   Name: {row[1]}")
        print(f"   Version: {row[2]}")
        print(f"   System Prompt: {row[3][:80]}...")
    
    # 2. T?o prompt m?i
    print("\n? CREATING NEW PROMPT VERSION...")
    cursor.execute('''
        INSERT INTO prompt_templates (name, version, system_prompt, user_prompt, is_active, created_by)
        VALUES ('marketing_v2', 2, 
                'You are a creative marketing expert for SEN V3 platform.',
                'Create viral content for: {topic}',
                0, 'demo_user')
    ''')
    new_id = cursor.lastrowid
    print(f"   ? Created prompt ID: {new_id}")
    
    # 3. Activate prompt m?i (t? ??ng deactivate c?)
    print("\n?? ACTIVATING NEW PROMPT...")
    cursor.execute("UPDATE prompt_templates SET is_active=1, activated_at=? WHERE id=?", 
                   (datetime.now().isoformat(), new_id))
    conn.commit()
    print("   ? New prompt activated! Old prompt auto-deactivated (trigger)")
    
    # 4. Xem prompt hi?n t?i
    print("\n?? NEW ACTIVE PROMPT:")
    cursor.execute("SELECT id, name, version, activated_at FROM prompt_templates WHERE is_active=1")
    row = cursor.fetchone()
    if row:
        print(f"   ID: {row[0]}")
        print(f"   Name: {row[1]}")
        print(f"   Version: {row[2]}")
        print(f"   Activated: {row[3]}")
    
    # 5. Th?m param set m?i
    print("\n?? ADDING NEW PARAM SET...")
    cursor.execute('''
        INSERT INTO llm_param_sets (model, cycle, temperature, top_p, max_tokens, score_avg)
        VALUES ('gemini-1.5-flash', 2, 0.8, 0.95, 4096, 0.0)
    ''')
    print(f"   ? Added param set ID: {cursor.lastrowid}")
    
    # 6. L?u content version
    print("\n?? SAVING CONTENT VERSION...")
    cursor.execute('''
        INSERT INTO content_versions (prompt_id, param_set_id, content, score)
        VALUES (?, ?, ?, ?)
    ''', (new_id, 2, "Sample generated content from demo", 85.5))
    print(f"   ? Saved content version ID: {cursor.lastrowid}")
    
    conn.commit()
    
    # 7. Th?ng k?
    print("\n?? FINAL STATISTICS:")
    cursor.execute("SELECT COUNT(*) FROM prompt_templates")
    print(f"   ?? Total prompts: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM llm_param_sets")
    print(f"   ?? Total param sets: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM content_versions")
    print(f"   ?? Total content versions: {cursor.fetchone()[0]}")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("? VERSIONING DEMO COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    demo_versioning()
