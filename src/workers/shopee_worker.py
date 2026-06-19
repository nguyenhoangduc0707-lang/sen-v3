"""
Shopee worker – giả lập xử lý dữ liệu Shopee.
"""

def run(payload: dict, **kwargs) -> dict:
    """Worker Shopee – trả về payload đã nhận."""
    return {
        "status": "success",
        "result": {
            "data": payload,
            "worker": "shopee"
        }
    }

class ShopeeWorker:
    @staticmethod
    def run(payload: dict, **kwargs) -> dict:
        return run(payload, **kwargs)
