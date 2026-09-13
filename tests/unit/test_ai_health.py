from unittest.mock import patch, MagicMock
import requests

from ai.config import AIConfig
from ai.health import check_ai_service, is_model_available


def test_check_ai_service_online():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [
            {"name": "qwen3.5:4b"},
            {"name": "phi3.5:latest"},
        ]
    }

    with patch("requests.get", return_value=mock_response):
        status = check_ai_service()
        assert status.is_online is True
        assert "qwen3.5:4b" in status.available_models
        assert status.error_message is None


def test_check_ai_service_offline():
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError("Offline")):
        status = check_ai_service()
        assert status.is_online is False
        assert status.available_models == []
        assert "Failed to connect" in status.error_message


def test_is_model_available():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [{"name": "qwen3.5:4b"}]
    }

    with patch("requests.get", return_value=mock_response):
        assert is_model_available("qwen3.5:4b") is True
        assert is_model_available("gpt-4") is False
