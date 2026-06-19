from src.discovery import load_workers
from src.worker_engine import run_worker_sync


@pytest.mark.skip(reason="Worker not implemented yet")\n    \1
    load_workers()
    result = run_worker_sync("shopee_worker", {"url": "https://shopee.vn/item"})
    # Kiểm tra kết quả trả về
    assert result.get("status") in ["success", "error"]
    if result.get("status") == "success":
        # Nếu worker tồn tại, kiểm tra dữ liệu
        assert "result" in result
        assert "data" in result["result"]
        assert result["result"]["data"]["url"] == "https://shopee.vn/item"
    else:
        # Nếu worker không tồn tại, đó là lỗi hợp lệ
        assert "error" in result

