import argparse, time
from auto_picker import run_picker, log
from config_loader import get_picker_config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", action="store_true")
    args = parser.parse_args()
    if not args.loop:
        run_picker()
        return
    cfg = get_picker_config()
    interval = int(cfg.get("loop_interval_minutes", 15)) * 60
    log.info(f"Chay loop moi {interval // 60} phut. Ctrl+C de dung.")
    while True:
        try: run_picker()
        except Exception as e: log.error(f"Loi: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    main()