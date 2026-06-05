import os

# C?u hÃ¬nh
SEARCH_TEXT = "registry"
REPLACE_TEXT = "registry"
EXTENSIONS = [".py"]
TARGET_DIR = "."  # QuÃ©t toÃ n b? thu m?c g?c

for root, dirs, files in os.walk(TARGET_DIR):
    for file in files:
        if any(file.endswith(ext) for ext in EXTENSIONS):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            if SEARCH_TEXT in content:
                new_content = content.replace(SEARCH_TEXT, REPLACE_TEXT)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"? ÃÃ£ c?p nh?t: {path}")

print("?? Migration hoÃ n t?t!")
