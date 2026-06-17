# reorganize.py
import os
import shutil
from pathlib import Path

def reorganize_files():
    # Định nghĩa các nhóm file và thư mục đích
    categories = {
        'scripts': [
            '*.ps1',  # PowerShell scripts
            'setup_*.py', 'build_*.py', 'rebuild*.ps1',
            'update-*.ps1', 'security-*.ps1'
        ],
        'tools': [
            'check_*.py', 'show_*.py', 'view_*.py', 'list_*.py',
            'fetch_*.py', 'report_*.py', 'export_*.py'
        ],
        'experiments': [
            '*_agent.py', '*_explorer.py', '*_analyzer.py',
            '*_test.py', '*_experiment.py', 'hybrid_*.py',
            'computer_use_agent.py', 'dom_agent.py', 'meta_agent.py'
        ],
        'backups': [
            'backup_*.db', '*.bak'
        ]
    }
    
    # Di chuyển từng nhóm
    for category, patterns in categories.items():
        target_dir = Path(category)
        target_dir.mkdir(exist_ok=True)
        
        for pattern in patterns:
            for file in Path('.').glob(pattern):
                if file.is_file():
                    dest = target_dir / file.name
                    shutil.move(str(file), str(dest))
                    print(f"📁 Moved: {file.name} -> {category}/")

if __name__ == "__main__":
    reorganize_files()