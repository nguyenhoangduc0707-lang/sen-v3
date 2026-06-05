import pyautogui
import time

print("=" * 50)
print("🎯 TOOL LẤY TỌA ĐỘ CHUỘT")
print("=" * 50)
print("\nHướng dẫn:")
print("1. Di chuyển chuột đến vị trí cần lấy tọa độ")
print("2. Nhấn 'c' để ghi nhận tọa độ")
print("3. Nhấn 'q' để thoát\n")

positions = []

while True:
    x, y = pyautogui.position()
    print(f"   Tọa độ hiện tại: ({x}, {y})", end="\r")
    
    # Kiểm tra phím bấm
    try:
        import msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key == 'c':
                positions.append((x, y))
                print(f"\n✅ Đã lưu tọa độ: ({x}, {y})")
            elif key == 'q':
                print("\n\n📋 DANH SÁCH TỌA ĐỘ ĐÃ LƯU:")
                for i, pos in enumerate(positions):
                    print(f"   {i+1}. ({pos[0]}, {pos[1]})")
                break
    except:
        pass
    
    time.sleep(0.1)
