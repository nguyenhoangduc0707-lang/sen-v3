import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.notebooklm_service import NotebookLMService


@pytest.fixture
def mock_notebooklm_client():
    with patch("src.notebooklm_service.NotebookLMClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.from_storage = AsyncMock(return_value=mock_client)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        yield mock_client_class  # Trả về class, không phải client


@pytest.fixture
def service():
    return NotebookLMService()


@pytest.mark.asyncio
async def test_get_client_creates_once(service, mock_notebooklm_client):
    client1 = await service.get_client()
    client2 = await service.get_client()
    assert client1 is client2
    mock_notebooklm_client.from_storage.assert_called_once()


@pytest.mark.asyncio
async def test_ask_notebook_success(service, mock_notebooklm_client):
    mock_response = Mock()
    mock_response.answer = "Câu trả lời mẫu"
    # Lấy client instance từ mock class
    mock_client_instance = mock_notebooklm_client.from_storage.return_value
    mock_client_instance.chat.ask = AsyncMock(return_value=mock_response)

    result = await service.ask_notebook("nb123", "Hỏi gì?")
    assert result == {"success": True, "answer": "Câu trả lời mẫu"}
    mock_client_instance.chat.ask.assert_called_once_with("nb123", "Hỏi gì?")


@pytest.mark.asyncio
async def test_ask_notebook_exception(service, mock_notebooklm_client):
    mock_client_instance = mock_notebooklm_client.from_storage.return_value
    mock_client_instance.chat.ask = AsyncMock(side_effect=Exception("Lỗi API"))
    result = await service.ask_notebook("nb1", "q")
    assert result == {"success": False, "error": "Lỗi API"}


@pytest.mark.asyncio
async def test_list_notebooks_success(service, mock_notebooklm_client):
    mock_nb = Mock()
    mock_nb.model_dump.return_value = {"id": "nb1", "name": "Ghi chú"}
    mock_client_instance = mock_notebooklm_client.from_storage.return_value
    mock_client_instance.notebooks.list = AsyncMock(return_value=[mock_nb])

    result = await service.list_notebooks()
    assert result == [{"id": "nb1", "name": "Ghi chú"}]


@pytest.mark.asyncio
async def test_list_notebooks_exception(service, mock_notebooklm_client):
    mock_client_instance = mock_notebooklm_client.from_storage.return_value
    mock_client_instance.notebooks.list = AsyncMock(side_effect=Exception("Lỗi danh sách"))
    result = await service.list_notebooks()
    assert result == []
