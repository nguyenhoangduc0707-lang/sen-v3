import time
from google import genai
from google.auth import default

def run_safe_deep_research():
    print("🔐 Đang tải thông tin xác thực an toàn từ Application Default Credentials (ADC)...")
    try:
        credentials, project_id = default()
        print(f"✅ Thành công! Đã tìm thấy credentials cho project: {project_id}")
    except Exception as e:
        print(f"❌ Lỗi xác thực: {e}")
        print("👉 Hãy đảm bảo script setup_adc.ps1 đã chạy thành công.")
        return

    # Khởi tạo client cho Vertex AI
    client = genai.Client(
        vertexai=True,
        project=project_id,
        credentials=credentials
    )

    print("🚀 Bắt đầu tác vụ Gemini Deep Research Agent...")
    # Tạo một tác vụ nghiên cứu đơn giản
    interaction = client.interactions.create(
        agent="deep-research-preview-04-2026",
        input="Explain the concept of 'Artificial Intelligence' in three bullet points.",
        background=True,  # Bắt buộc cho tác vụ này
    )

    print(f"🆔 ID tác vụ: {interaction.id}")
    print("⏳ Quá trình nghiên cứu đang diễn ra (sẽ mất khoảng 1-2 phút)...")
    print("   (Nhấn Ctrl+C để dừng theo dõi, tác vụ vẫn chạy ngầm)")

    start_time = time.time()
    while True:
        # Lấy trạng thái mới nhất của tác vụ
        interaction = client.interactions.get(interaction.id)
        
        if interaction.status == "completed":
            elapsed_time = int(time.time() - start_time)
            print("\n" + "="*60)
            print(f"✅ Nghiên cứu hoàn tất sau {elapsed_time} giây!")
            print("📄 KẾT QUẢ:")
            print("="*60)
            print(interaction.output_text)
            break
        elif interaction.status == "failed":
            print(f"\n❌ Nghiên cứu thất bại: {interaction.error}")
            break
        else:
            # Vẫn đang trong quá trình xử lý
            print(".", end="", flush=True)
            time.sleep(10)

if __name__ == "__main__":
    run_safe_deep_research()