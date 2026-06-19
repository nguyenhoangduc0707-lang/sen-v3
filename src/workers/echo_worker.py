"""
Echo worker – chỉ trả lại payload.
"""

def run(payload: dict, **kwargs) -> dict:
    """Worker echo – trả về payload đã nhận."""
    return {
        "status": "success",
        "result": {
            "echo": payload,
            "worker": "echo_worker"
        }
    }

# Để tương thích với một số hàm gọi worker bằng tên class
class EchoWorker:
    @staticmethod
    def run(payload: dict, **kwargs) -> dict:
        return run(payload, **kwargs)
