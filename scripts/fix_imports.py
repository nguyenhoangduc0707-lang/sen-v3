import os

# C?u hÃ¬nh cÃ¡c thay th?
# Key: Chu?i cu, Value: Chu?i m?i
REPLACEMENTS = {
    "from src.registry import register_worker": "from src.orchestrator import register_worker",
    "import src.registry": "from src import orchestrator",
}

TARGET_DIR = "fullwork"


def fix_imports():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                new_content = content
                changed = False
                for old, new in REPLACEMENTS.items():
                    if old in new_content:
                        new_content = new_content.replace(old, new)
                        changed = True

                if changed:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"? ÃÃ£ s?a import t?i: {path}")


if __name__ == "__main__":
    fix_imports()
    print("?? HoÃ n t?t chu?n hÃ³a import!")
