import os
import asyncio
import base64
import io
import traceback
import cv2
import pyaudio
import PIL.Image
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

# Model configuration
MODEL = "models/gemini-3.5-live-translate-preview"
DEFAULT_MODE = "camera"

# Initialize Gemini client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("❌ LỖI: Chưa set GEMINI_API_KEY trong .env")
    print("   Lấy key tại: https://aistudio.google.com/apikey")
    exit(1)

client = genai.Client(
    http_options={"api_version": "v1beta"},
    api_key=api_key,
)

# Live configuration
CONFIG = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    media_resolution="MEDIA_RESOLUTION_MEDIUM",
    context_window_compression=types.ContextWindowCompressionConfig(
        trigger_tokens=0,
        sliding_window=types.SlidingWindow(target_tokens=0),
    ),
    translation_config=types.TranslationConfig(
        target_language_code="vi",  # Dịch sang tiếng Việt
    ),
)

pya = pyaudio.PyAudio()

class DYT01LiveTranslator:
    def __init__(self, video_mode=DEFAULT_MODE):
        self.video_mode = video_mode
        self.audio_in_queue = None
        self.out_queue = None
        self.session = None
        self.send_text_task = None
        self.receive_audio_task = None
        self.play_audio_task = None
        self.audio_stream = None
        self.transcription_history = []

    async def send_text(self):
        print("🎤 Live Translation Mode (type 'q' to quit)")
        print("📝 Gõ tin nhắn để dịch, hoặc nói vào microphone")
        print("-" * 50)
        
        while True:
            text = await asyncio.to_thread(
                input,
                "message > ",
            )
            if text.lower() == "q":
                break
            if self.session is not None:
                await self.session.send(input=text or ".", end_of_turn=True)

    def _get_frame(self, cap):
        ret, frame = cap.read()
        if not ret:
            return None
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = PIL.Image.fromarray(frame_rgb)
        img.thumbnail([1024, 1024])
        image_io = io.BytesIO()
        img.save(image_io, format="jpeg")
        image_io.seek(0)
        return {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(image_io.read()).decode()
        }

    async def get_frames(self):
        cap = await asyncio.to_thread(cv2.VideoCapture, 0)
        while True:
            frame = await asyncio.to_thread(self._get_frame, cap)
            if frame is None:
                break
            await asyncio.sleep(1.0)
            if self.out_queue is not None:
                await self.out_queue.put(frame)
        cap.release()

    async def send_realtime(self):
        while True:
            if self.out_queue is not None:
                msg = await self.out_queue.get()
                if self.session is not None:
                    await self.session.send(input=msg)

    async def listen_audio(self):
        mic_info = pya.get_default_input_device_info()
        self.audio_stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=SEND_SAMPLE_RATE,
            input=True,
            input_device_index=mic_info["index"],
            frames_per_buffer=CHUNK_SIZE,
        )
        while True:
            data = await asyncio.to_thread(self.audio_stream.read, CHUNK_SIZE)
            if self.out_queue is not None:
                await self.out_queue.put({"data": data, "mime_type": "audio/pcm"})

    async def receive_audio(self):
        while True:
            if self.session is not None:
                turn = self.session.receive()
                async for response in turn:
                    if data := response.data:
                        self.audio_in_queue.put_nowait(data)
                        continue
                    if text := response.text:
                        print(f"\n🤖 Dịch: {text}")
                        # Lưu lịch sử dịch
                        self.transcription_history.append({
                            "timestamp": asyncio.get_event_loop().time(),
                            "text": text
                        })
                # Clear queue when turn completes
                while not self.audio_in_queue.empty():
                    self.audio_in_queue.get_nowait()

    async def play_audio(self):
        stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=RECEIVE_SAMPLE_RATE,
            output=True,
        )
        while True:
            if self.audio_in_queue is not None:
                bytestream = await self.audio_in_queue.get()
                await asyncio.to_thread(stream.write, bytestream)

    async def save_translation_history(self):
        """Lưu lịch sử dịch vào file"""
        import json
        from datetime import datetime
        
        if self.transcription_history:
            filename = f"translations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.transcription_history, f, ensure_ascii=False, indent=2)
            print(f"\n✅ Đã lưu lịch sử dịch: {filename}")

    async def run(self):
        try:
            async with (
                client.aio.live.connect(model=MODEL, config=CONFIG) as session,
                asyncio.TaskGroup() as tg,
            ):
                self.session = session
                self.audio_in_queue = asyncio.Queue()
                self.out_queue = asyncio.Queue(maxsize=5)

                print("🚀 Bắt đầu Live Translation...")
                print("📹 Chế độ:", self.video_mode)
                print("🎯 Dịch sang tiếng Việt")
                print("-" * 50)

                tg.create_task(self.send_text())
                tg.create_task(self.send_realtime())
                tg.create_task(self.listen_audio())
                
                if self.video_mode == "camera":
                    tg.create_task(self.get_frames())
                elif self.video_mode == "screen":
                    # TODO: Implement screen capture
                    pass

                tg.create_task(self.receive_audio())
                tg.create_task(self.play_audio())

                await self.send_text_task
                raise asyncio.CancelledError("User requested exit")

        except asyncio.CancelledError:
            print("\n\n⏹️ Đang dừng...")
            await self.save_translation_history()
        except ExceptionGroup as EG:
            if self.audio_stream is not None:
                self.audio_stream.close()
                traceback.print_exception(EG)
        finally:
            if self.audio_stream is not None:
                self.audio_stream.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        type=str,
        default=DEFAULT_MODE,
        help="chế độ stream: camera hoặc screen",
        choices=["camera", "screen", "none"],
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="vi",
        help="ngôn ngữ đích (vi, en, ja, ...)",
    )
    args = parser.parse_args()
    
    # Cập nhật ngôn ngữ đích
    CONFIG.translation_config.target_language_code = args.lang
    
    main = DYT01LiveTranslator(video_mode=args.mode)
    asyncio.run(main.run())
