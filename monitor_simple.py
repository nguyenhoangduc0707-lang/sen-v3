# monitor_simple.py
import time
import datetime

print("Simple Monitor Started")
print("Press Ctrl+C to stop\n")

count = 0
while True:
    count += 1
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] Check {count}: System OK")
    time.sleep(10)