# fix_routers.py
"""
Fix các lỗi Field trong router files
Chạy: python fix_routers.py
"""

import re
import os

def fix_router_file(filepath):
    """Fix lỗi Field parameter trong router"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Tìm pattern: param: type = Field(...)
    # Thay bằng: param: type
    pattern = r'(\w+):\s*(\w+)\s*=\s*Field\([^)]+\)'
    replacement = r'\1: \2'
    
    fixed_content = re.sub(pattern, replacement, content)
    
    if fixed_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"✅ Fixed: {filepath}")
        return True
    return False

# Fix all router files
routers = [
    "web/routers/commission.py",
    "web/routers/member_dashboard.py", 
    "web/routers/ai_generate.py",
    "web/routers/admin.py",
    "web/routers/auth.py"
]

for router in routers:
    if os.path.exists(router):
        fix_router_file(router)
    else:
        print(f"⚠️ Not found: {router}")

print("✅ All routers fixed!")