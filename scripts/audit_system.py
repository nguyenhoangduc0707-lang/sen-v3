import os


def audit_system():
    print("--- SEN V3 SYSTEM AUDIT ---")

    folders = ["src", "src/workers", "scripts", "logs", "web", "frontend", "alembic"]
    for folder in folders:
        if os.path.exists(folder):
            print(f"[OK] Found directory: {folder}")
        else:
            print(f"[ERROR] Missing directory: {folder}")

    files = [
        "main.py",
        "run_api.py",
        "run_worker.py",
        "web/main.py",
        "src/orchestrator.py",
        "src/orchestrator_async.py",
        "src/task_queue_db.py",
        "requirements.txt",
    ]
    for file in files:
        if os.path.exists(file):
            print(f"[OK] Found file: {file}")
        else:
            print(f"[ERROR] Missing file: {file}")

    if os.path.exists(".env"):
        print("[OK] .env file detected.")
    else:
        print("[WARN] .env file NOT found. Configuration might be missing.")

    print("--- AUDIT COMPLETE ---")


if __name__ == "__main__":
    audit_system()
