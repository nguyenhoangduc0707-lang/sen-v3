import os
import json

# Lazy import to avoid requiring google libs during local dev
try:
    from google.cloud import aiplatform
    from vertexai.preview.generative_models import GenerativeModel, GenerationConfig
    _HAS_VERTEX = True
except Exception:
    _HAS_VERTEX = False

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION", "asia-southeast1")

if _HAS_VERTEX and PROJECT_ID:
    try:
        aiplatform.init(project=PROJECT_ID, location=LOCATION)
    except Exception:
        pass


def generate_content(prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
    """Gọi Gemini (Vertex AI) để sinh nội dung. Trả về plaintext result."""
    if not _HAS_VERTEX:
        # Fallback during local dev
        return json.dumps({"error": "vertex-ai not installed"})
    model = GenerativeModel("gemini-1.5-pro")
    config = GenerationConfig(temperature=temperature, max_output_tokens=max_tokens)
    response = model.generate_content(prompt, generation_config=config)
    # response may provide .text or .generations
    try:
        return response.text
    except Exception:
        try:
            return str(response)
        except Exception:
            return ""


def analyze_affiliate_data(product_data: dict) -> dict:
    """Phân tích dữ liệu affiliate và trả về JSON gợi ý.
    Trả về dictionary; nếu parsing JSON thất bại thì trả về raw string under 'raw'.
    """
    prompt = f"""
Bạn là chuyên gia marketing. Hãy phân tích dữ liệu sản phẩm sau và đề xuất chiến lược affiliate:
{json.dumps(product_data, indent=2, ensure_ascii=False)}
Trả về dạng JSON với các field: recommendation, estimated_commission, suggested_price.
"""
    result = generate_content(prompt, temperature=0.3, max_tokens=512)
    try:
        return json.loads(result)
    except Exception:
        return {"raw": result}
