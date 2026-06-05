import os
from unittest.mock import patch

from src.key_manager import get_api_key


class TestKeyManager:
    @patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-openai"})
    def test_get_api_key_openai(self):
        """Test lấy key cho OpenAI"""
        key = get_api_key("openai")
        assert key == "sk-test-openai"

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-test-anthropic"})
    def test_get_api_key_anthropic(self):
        """Test lấy key cho Anthropic"""
        key = get_api_key("anthropic")
        assert key == "sk-test-anthropic"

    def test_get_api_key_unknown_service(self):
        """Test service không xác định trả về fake-key"""
        key = get_api_key("unknown")
        assert key == "fake-key"

    def test_get_api_key_missing_env_var(self):
        """Test khi biến môi trường không tồn tại"""
        # Giả sử không có OPENAI_API_KEY trong env thật
        with patch.dict(os.environ, {}, clear=True):
            key = get_api_key("openai")
            assert key == "fake-key"
