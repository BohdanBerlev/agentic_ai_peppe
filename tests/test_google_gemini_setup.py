import os
from unittest.mock import MagicMock, patch
import pytest

from src.app.settings import Settings
from src.llm.factory import get_chat_model
from src.workflows.run_github_issue import should_close_issue


def test_settings_resolves_gemini_api_key(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.setenv("GEMINI_API_KEY", "test-gemini-key-123")

    settings = Settings(_env_file=None)
    assert settings.llm_api_key == "test-gemini-key-123"


def test_settings_resolves_google_api_key(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("GOOGLE_API_KEY", "test-google-key-456")

    settings = Settings(_env_file=None)
    assert settings.llm_api_key == "test-google-key-456"


def test_settings_resolves_llm_api_key(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "test-llm-key-789")

    settings = Settings(_env_file=None)
    assert settings.llm_api_key == "test-llm-key-789"


def test_get_chat_model_google_provider_success(monkeypatch):
    captured = {}

    def mock_chat_google(*args, **kwargs):
        captured.update(kwargs)
        return MagicMock(name="ChatGoogleGenerativeAI")

    monkeypatch.setattr("langchain_google_genai.ChatGoogleGenerativeAI", mock_chat_google)
    monkeypatch.setenv("GEMINI_API_KEY", "ai-studio-valid-key")

    settings = Settings(_env_file=None, llm_provider="google", llm_model="")
    model = get_chat_model(settings)

    assert captured.get("api_key") == "ai-studio-valid-key"
    assert captured.get("model") == "gemini-1.5-flash"
    assert "rate_limiter" in captured


def test_get_chat_model_google_missing_key_raises(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("AI_STUDIO_API_KEY", raising=False)

    settings = Settings(_env_file=None, llm_provider="google", llm_api_key="")
    with pytest.raises(ValueError, match="Google Gemini API-Key fehlt"):
        get_chat_model(settings)
