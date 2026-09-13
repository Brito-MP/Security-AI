from unittest.mock import patch, MagicMock
import pytest
import requests

from ai.client import OllamaClient, AIServiceUnavailableError, AIClientError
from ai.config import AIConfig


def test_client_generate_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "model": "qwen3.5:4b",
        "response": "Hello! System operational and secure.",
        "done": True,
        "total_duration": 450_000_000,
        "prompt_eval_count": 10,
        "eval_count": 15,
    }

    client = OllamaClient()
    with patch("requests.post", return_value=mock_response):
        result = client.generate(prompt="What is your status?")

        assert result.model == "qwen3.5:4b"
        assert "operational" in result.response
        assert result.done is True
        assert result.total_duration_ms == 450.0


def test_client_service_unavailable():
    client = OllamaClient()
    with patch("requests.post", side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(AIServiceUnavailableError) as exc_info:
            client.generate(prompt="Test")
        assert "Failed to connect to Ollama" in str(exc_info.value)


def test_client_api_error_status():
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"

    client = OllamaClient()
    with patch("requests.post", return_value=mock_response):
        with pytest.raises(AIClientError) as exc_info:
            client.generate(prompt="Test")
        assert "500" in str(exc_info.value)
