import pyaudio

def test_microphone():
    print("🎤 Kiểm tra microphone...")
    p = pyaudio.PyAudio()
    
    # Liệt kê các thiết bị đầu vào
    print("\n📋 Các thiết bị đầu vào:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            print(f"   {i}: {info['name']}")
    
    # Test microphone
    print("\n🎤 Đang test microphone (nói vào mic)...")
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024
    )
    
    try:
        for _ in range(5):
            data = stream.read(1024)
            print(".", end="", flush=True)
        print("\n✅ Microphone hoạt động!")
    except Exception as e:
        print(f"\n❌ Lỗi microphone: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    test_microphone()
