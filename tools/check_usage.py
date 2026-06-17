# check_usage.py
import os
import ast
from collections import Counter

def analyze_imports():
    imports = []
    for file in os.listdir('.'):
        if file.endswith('.py') and file not in ['check_usage.py', 'requirements.txt']:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                imports.append(alias.name.split('.')[0])
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                imports.append(node.module.split('.')[0])
            except:
                pass
    
    counter = Counter(imports)
    print("=== TOP 20 IMPORT ĐƯỢC DÙNG NHIỀU NHẤT ===")
    for lib, count in counter.most_common(20):
        print(f"{lib}: {count} lần")

if __name__ == "__main__":
    analyze_imports()