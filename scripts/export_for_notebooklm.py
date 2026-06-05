#!/usr/bin/env python3
"""
Export entire project to NotebookLM format
Supports: code files, documentation, database content, logs
"""
import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import argparse

def export_database_content(db_path: str = "sen_v3.db") -> Dict:
    """Export database content to JSON format"""
    if not Path(db_path).exists():
        return {}
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    export_data = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1000")  # Limit rows
        rows = cursor.fetchall()
        export_data[table_name] = [dict(row) for row in rows]
    
    conn.close()
    return export_data

def export_code_files(source_dir: str, extensions: List[str] = None) -> List[Dict]:
    """Export code files from project"""
    if extensions is None:
        extensions = ['.py', '.js', '.jsx', '.md', '.txt', '.json', '.yaml', '.yml']
    
    source_path = Path(source_dir)
    files = []
    
    for ext in extensions:
        for file_path in source_path.rglob(f"*{ext}"):
            # Skip virtual environment and cache
            if any(skip in str(file_path) for skip in ['venv', '__pycache__', '.git', '.pytest_cache']):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                files.append({
                    "path": str(file_path.relative_to(source_path)),
                    "name": file_path.name,
                    "extension": ext,
                    "size": len(content),
                    "content": content[:20000],  # Limit to 20k chars per file
                    "modified_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")
    
    return files

def create_notebooklm_export(project_dir: str = ".", output_file: str = "notebooklm_export.json"):
    """Main export function"""
    print("🚀 Exporting project to NotebookLM format...")
    
    # Collect data
    export_package = {
        "project_name": Path(project_dir).absolute().name,
        "exported_at": datetime.now().isoformat(),
        "contents": {
            "database": export_database_content(),
            "code_files": export_code_files(project_dir),
            "statistics": {}
        }
    }
    
    # Add statistics
    export_package["contents"]["statistics"] = {
        "total_files": len(export_package["contents"]["code_files"]),
        "database_tables": len(export_package["contents"]["database"]),
        "export_size_kb": 0  # Will calculate
    }
    
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_package, f, indent=2, ensure_ascii=False)
    
    # Calculate size
    file_size = Path(output_file).stat().st_size / 1024
    export_package["contents"]["statistics"]["export_size_kb"] = round(file_size, 2)
    
    # Also create markdown version for easy reading
    md_file = output_file.replace('.json', '.md')
    create_markdown_export(export_package, md_file)
    
    print(f"✅ Export complete!")
    print(f"   - JSON: {output_file} ({file_size:.2f} KB)")
    print(f"   - Markdown: {md_file}")
    print(f"   - Total files: {export_package['contents']['statistics']['total_files']}")
    print(f"   - Database tables: {export_package['contents']['statistics']['database_tables']}")
    
    return export_package

def create_markdown_export(export_package: Dict, output_file: str):
    """Create markdown version of export"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# {export_package['project_name']} - Export for NotebookLM\n\n")
        f.write(f"**Exported:** {export_package['exported_at']}\n\n")
        
        # Statistics
        f.write("## 📊 Statistics\n\n")
        stats = export_package['contents']['statistics']
        f.write(f"- Total files: {stats['total_files']}\n")
        f.write(f"- Database tables: {stats['database_tables']}\n")
        f.write(f"- Export size: {stats['export_size_kb']} KB\n\n")
        
        # Database content
        if export_package['contents']['database']:
            f.write("## 🗄️ Database Content\n\n")
            for table_name, rows in export_package['contents']['database'].items():
                f.write(f"### Table: {table_name}\n")
                f.write(f"Rows: {len(rows)}\n\n")
                if rows:
                    f.write("```json\n")
                    f.write(json.dumps(rows[:5], indent=2, ensure_ascii=False))
                    f.write("\n```\n\n")
        
        # Code files summary
        f.write("## 📁 Code Files\n\n")
        files_by_ext = {}
        for file_info in export_package['contents']['code_files']:
            ext = file_info['extension']
            if ext not in files_by_ext:
                files_by_ext[ext] = []
            files_by_ext[ext].append(file_info)
        
        for ext, files in sorted(files_by_ext.items()):
            f.write(f"### {ext} files ({len(files)})\n")
            for file in files[:20]:  # Limit to 20 per extension
                f.write(f"- `{file['path']}` ({file['size']} chars)\n")
            if len(files) > 20:
                f.write(f"- ... and {len(files) - 20} more\n")
            f.write("\n")

def main():
    parser = argparse.ArgumentParser(description="Export project for NotebookLM")
    parser.add_argument("--dir", default=".", help="Project directory to export")
    parser.add_argument("--output", default="notebooklm_export.json", help="Output JSON file")
    parser.add_argument("--no-db", action="store_true", help="Skip database export")
    
    args = parser.parse_args()
    
    create_notebooklm_export(args.dir, args.output)

if __name__ == "__main__":
    main()