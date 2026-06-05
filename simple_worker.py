
import time
import datetime

def main():
    print(f"[{datetime.datetime.now()}] Simple worker started")
    print("Processing affiliate links...")
    
    links = [
        "https://shorten.asia/3cSC6EUX",
        "https://shorten.asia/PjYek8R8",
        "https://shorten.asia/MxvRDqNg"
    ]
    
    count = 0
    while True:
        count += 1
        print(f"[{datetime.datetime.now()}] Cycle {count}")
        
        for link in links:
            print(f"  -> {link}")
            # TODO: Add your logic here
            
        time.sleep(30)

if __name__ == "__main__":
    main()
