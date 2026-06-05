# monitor_workers.py - Fixed version
import time
import datetime
import os
import sys

class MonitorWorker:
    def __init__(self):
        self.running = True
        self.check_interval = 10  # giây
        self.log_file = "monitor_log.txt"
        
    def log(self, message):
        """Ghi log với thời gian"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        # Ghi ra file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_msg + "\n")
        except:
            pass
    
    def check_system(self):
        """Kiểm tra hệ thống"""
        try:
            # Kiểm tra CPU
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            self.log(f"CPU: {cpu_percent}% | RAM: {memory.percent}% | Free: {memory.available // (1024**3)}GB")
            
            # Cảnh báo nếu quá tải
            if cpu_percent > 80:
                self.log("⚠️ WARNING: CPU cao!")
            if memory.percent > 85:
                self.log("⚠️ WARNING: RAM sap day!")
                
        except ImportError:
            # Nếu không có psutil, chỉ log đơn giản
            self.log("System check: OK (simple mode)")
        except Exception as e:
            self.log(f"Loi check system: {e}")
    
    def check_workers(self):
        """Kiểm tra các worker khác"""
        try:
            # Tìm các process Python
            import subprocess
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                                   capture_output=True, text=True)
            
            python_processes = [line for line in result.stdout.split('\n') if 'python.exe' in line]
            worker_count = len(python_processes)
            
            self.log(f"Python processes: {worker_count}")
            
            if worker_count == 0:
                self.log("⚠️ Khong co worker nao dang chay!")
                
        except Exception as e:
            self.log(f"Loi check workers: {e}")
    
    def check_disk_space(self):
        """Kiểm tra dung lượng đĩa"""
        try:
            import shutil
            usage = shutil.disk_usage("E:/")
            free_gb = usage.free // (1024**3)
            total_gb = usage.total // (1024**3)
            
            self.log(f"Disk: {free_gb}GB free / {total_gb}GB total")
            
            if free_gb < 10:
                self.log("⚠️ WARNING: Disk sap day!")
                
        except Exception as e:
            self.log(f"Loi check disk: {e}")
    
    def check_affiliate_links(self):
        """Kiểm tra file link affiliate"""
        try:
            link_files = ["affiliate_links.txt", "links.txt"]
            for file in link_files:
                if os.path.exists(file):
                    with open(file, "r", encoding="utf-8", errors='ignore') as f:
                        content = f.read()
                        link_count = content.count("shorten.asia")
                        self.log(f"File {file}: {link_count} affiliate links")
                    break
            else:
                self.log("⚠️ Khong tim thay file affiliate links")
        except Exception as e:
            self.log(f"Loi check links: {e}")
    
    def run(self):
        """Chạy monitor worker"""
        self.log("=" * 50)
        self.log("MONITOR WORKER STARTED")
        self.log(f"Check interval: {self.check_interval} seconds")
        self.log("=" * 50)
        
        cycle = 0
        while self.running:
            try:
                cycle += 1
                self.log(f"\n--- Cycle {cycle} ---")
                
                # Thực hiện các kiểm tra
                self.check_system()
                self.check_workers()
                self.check_disk_space()
                self.check_affiliate_links()
                
                # Đợi đến lần kiểm tra tiếp theo
                for _ in range(self.check_interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                self.log("\n[*] Nhan Ctrl+C, dang dung...")
                self.running = False
            except Exception as e:
                self.log(f"[-] LOI: {e}")
                self.log("[*] Tiep tuc sau 5 giay...")
                time.sleep(5)
        
        self.log("=" * 50)
        self.log(f"MONITOR WORKER STOPPED. Total cycles: {cycle}")
        self.log("=" * 50)

def main():
    worker = MonitorWorker()
    
    print("\n" + "=" * 50)
    print("MONITOR WORKER - DYT01 SYSTEM")
    print("=" * 50)
    print("\nChuc nang:")
    print("- Giam sat CPU, RAM, Disk")
    print("- Kiem tra cac worker khac")
    print("- Kiem tra file affiliate")
    print("- Ghi log ra file: monitor_log.txt")
    print("\nNhan Ctrl+C de dung\n")
    
    try:
        worker.run()
    except Exception as e:
        print(f"Loi nghiem trong: {e}")
        input("Nhan Enter de thoat...")

if __name__ == "__main__":
    main()