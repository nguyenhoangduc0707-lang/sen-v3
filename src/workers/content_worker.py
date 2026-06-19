"""
Content worker – giả lập xử lý nội dung.
"""

def run(payload: dict, **kwargs) -> dict:
    """Worker Content – trả về payload đã nhận."""
    return {
        "status": "success",
        "result": {
            "data": payload,
            "worker": "content"
        }
    }

class ContentWorker:
    @staticmethod
    def run(payload: dict, **kwargs) -> dict:
        return run(payload, **kwargs)
