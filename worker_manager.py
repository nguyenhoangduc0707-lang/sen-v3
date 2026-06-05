# worker_manager.py
import subprocess
import time
import os
import signal
import sys

class WorkerManager:
    def __init__(self):
        self.workers = []
        self.running = True
        
    def start_worker(self, name, script):
        """Khoi dong worker"""
        try:
            if os.path.exists(script):
                print(f"[+] Dang khoi dong: {name}")
                proc = subprocess.Popen(
                    [sys.executable, script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                self.workers.append({"name": name, "process": proc, "script": script})
                return True
            else:
                print(f"[-] Khong tim thay: {script}")
                return False
        except Exception as e:
            print(f"[!] Loi khoi dong {name}: {e}")
            return False
    
    def stop_all(self):
        """Dung tat ca workers"""
        print("\n[*] Dang dung tat ca workers...")
        for worker in self.workers:
            try:
                worker["process"].terminate()
                print(f"[-] Da dung: {worker['name']}")
            except:
                pass
        self.workers.clear()
    
    def monitor(self):
        """Giam sat workers"""
        print("[*] Bat dau giam sat workers...")
        print("[*] Nhan Ctrl+C de dung tat ca\n")
        
        try:
            while self.running:
                for worker in self.workers[:]:
                    if worker["process"].poll() is not None:
                        print(f"[!] Worker {worker['name']} da dung!")
                        # Tu dong restart
                        print(f"[+] Dang restart {worker['name']}...")
                        self.start_worker(worker["name"], worker["script"])
                        self.workers.remove(worker)
                time.sleep(5)
        except KeyboardInterrupt:
            print("\n[*] Nhan Ctrl+C, dang dung...")
            self.stop_all()
            print("[+] Da dung toan bo workers")

def main():
    manager = WorkerManager()
    
    print("=" * 50)
    print("WORKER MANAGER - DYT01")
    print("=" * 50)
    
    # Danh sach workers can chay
    workers_to_start = [
    ("Monitor Worker", "monitor_workers.py"),  # Chỉ chạy monitor trước
    ]
    
    # Chỉ chạy workers có file tồn tại
    for name, script in workers_to_start:
        if os.path.exists(script):
            manager.start_worker(name, script)
        else:
            print(f"[-] Bo qua {name} - khong tim thay file")
    
    if not manager.workers:
        print("\n[!] Khong co worker nao duoc khoi dong!")
        print("[*] Tao file worker mau...")
        
        # Tao worker mau neu chua co
        with open("sample_worker.py", "w") as f:
            f.write("""
import time
print("Sample worker running...")
while True:
    print("Working...")
    time.sleep(10)
""")
        manager.start_worker("Sample Worker", "sample_worker.py")
    
    # Bat dau giam sat
    manager.monitor()

if __name__ == "__main__":
    main()