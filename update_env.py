import os
from datetime import datetime

ENV_FILE = ".env"

def backup_env():
    if not os.path.exists(ENV_FILE):
        return
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f".env.backup.{ts}"
    with open(ENV_FILE, "r", encoding="utf-8") as f_src, \
         open(backup_name, "w", encoding="utf-8") as f_dst:
        f_dst.write(f_src.read())
    print(f"[OK] Đã backup .env → {backup_name}")

def update_env(key, value):
    lines = []
    found = False

    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

    with open(ENV_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            if line.startswith(key + "="):
                f.write(f"{key}={value}\n")
                found = True
            else:
                f.write(line)

        if not found:
            f.write(f"{key}={value}\n")

if __name__ == "__main__":
    print("=== SEN V3 - KEY MANAGER ===")
    backup_env()
    print("Nhập key theo dạng: KEY=VALUE")
    print("Gõ 'exit' để thoát.\n")

    while True:
        user_input = input("> ").strip()

        if user_input.lower() == "exit":
            print("Thoát.")
            break

        if "=" not in user_input:
            print("Sai định dạng. Ví dụ: GOOGLE_API_KEY=abc123")
            continue

        key, value = user_input.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            print("KEY không được rỗng.")
            continue

        update_env(key, value)
        print(f"[OK] Đã cập nhật {key} vào .env")
