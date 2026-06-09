import subprocess
import time
import psutil
import os

def is_worker_running():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'python.exe' and 'run_facebook_worker.py' in ' '.join(proc.info['cmdline']):
                return True
        except:
            pass
    return False

def start_worker():
    subprocess.Popen(['python', 'run_facebook_worker.py'], 
                     cwd=r'E:\DYT_01',
                     creationflags=subprocess.CREATE_NEW_CONSOLE)
    print('✅ Started Facebook Worker')

print('🛡️ Facebook Worker Monitor Started')
print('Checking every 30 seconds...\n')

try:
    while True:
        if not is_worker_running():
            print(f'⚠️ Worker not running! Restarting...')
            start_worker()
        time.sleep(30)
except KeyboardInterrupt:
    print('\n👋 Monitor stopped')
