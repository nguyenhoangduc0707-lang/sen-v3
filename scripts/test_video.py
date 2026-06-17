import os
import subprocess
import sys

def install_and_test():
    print("📦 Đang kiểm tra công cụ làm video...")
    
    # 1. Cài MoviePy nếu chưa có
    try:
        import moviepy
        print("✅ MoviePy đã được cài đặt")
    except ImportError:
        print("⚠️ Chưa có MoviePy, đang tiến hành cài đặt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])
        print("✅ Đã cài đặt MoviePy thành công")

    # 2. Tạo một đoạn video test đơn giản
    try:
        from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
        
        # Tạo clip nền màu xanh (duration 3 giây)
        clip = ColorClip(size=(640, 480), color=(50, 100, 200), duration=3)
        
        # Xuất file video
        output_path = "output_test_video.mp4"
        clip.write_videofile(output_path, fps=24)
        print(f"🎬 Đã tạo video test thành công: {output_path}")
        
    except Exception as e:
        print(f"❌ Lỗi khi xử lý video: {e}")

if __name__ == "__main__":
    install_and_test()
    print("\n👉 Hãy kiểm tra file 'output_test_video.mp4' trong thư mục dự án!")