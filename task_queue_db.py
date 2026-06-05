# tests/test_notebooklm_service.py
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.notebooklm_service import NotebookLMService


@pytest.fixture
def mock_notebooklm_client():
    with patch("src.notebooklm_service.NotebookLMClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.from_storage = AsyncMock(return_value=mock_client)
        # Mock context manager: async with client
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        yield mock_client


@pytest.fixture
def service():
    return NotebookLMService()


@pytest.mark.asyncio
async def test_get_client_creates_client_once(service, mock_notebooklm_client):
    client1 = await service.get_client()
    client2 = await service.get_client()
    assert client1 is client2
    mock_notebooklm_client.from_storage.assert_called_once()


@pytest.mark.asyncio
async def test_ask_notebook_success(service, mock_notebooklm_client):
    mock_notebooklm_client.chat.ask.return_value = AsyncMock(return_value=Mock(answer="Hello"))
    result = await service.ask_notebook("nb1", "question?")
    assert result == {"success": True, "answer": "Hello"}
    mock_notebooklm_client.chat.ask.assert_called_once_with("nb1", "question?")


@pytest.mark.asyncio
async def test_ask_notebook_exception(service, mock_notebooklm_client):
    mock_notebooklm_client.chat.ask.side_effect = Exception("API error")
    result = await service.ask_notebook("nb1", "q")
    assert result == {"success": False, "error": "API error"}


@pytest.mark.asyncio
async def test_list_notebooks_success(service, mock_notebooklm_client):
    mock_notebook = Mock()
    mock_notebook.model_dump.return_value = {"id": 1, "name": "test"}
    mock_notebooklm_client.notebooks.list.return_value = AsyncMock(return_value=[mock_notebook])
    result = await service.list_notebooks()
    assert result == [{"id": 1, "name": "test"}]


@pytest.mark.asyncio
async def test_list_notebooks_exception(service, mock_notebooklm_client):
    mock_notebooklm_client.notebooks.list.side_effect = Exception("list error")
    result = await service.list_notebooks()
    assert result == []
