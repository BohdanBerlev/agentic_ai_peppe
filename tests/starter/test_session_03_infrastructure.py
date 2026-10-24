"""Course infrastructure regressions; not student achievement."""
import pytest
from fastapi.testclient import TestClient
from src.app.main import app
from src.app.settings import Settings
from src.llm.factory import get_chat_model


def test_database_health_does_not_expose_exception(monkeypatch):
    def fail():
        raise RuntimeError("postgresql://user:private_value@host/db")
    monkeypatch.setattr("src.app.main.database_health", fail)
    response = TestClient(app).get("/db/health")
    assert response.status_code == 503
    assert response.json() == {"detail": "database unavailable"}
    assert "private_value" not in response.text


def test_ollama_json_and_reasoning_are_optional():
    settings = Settings(_env_file=None, llm_max_output_tokens=42)
    default = get_chat_model(settings)
    assert default.reasoning is None and default.format is None
    structured = get_chat_model(settings, json_mode=True)
    assert structured.format == "json" and structured.reasoning is False
    assert structured.num_predict == 42
    assert get_chat_model(settings, reasoning=True, json_mode=True).reasoning is True


def test_icc_does_not_receive_ollama_options(monkeypatch):
    captured = {}
    def model(**kwargs):
        captured.update(kwargs)
        return object()
    monkeypatch.setattr("src.llm.factory.ChatOpenAI", model)
    settings = Settings(_env_file=None, llm_provider="openai_compatible")
    get_chat_model(settings, json_mode=True, reasoning=False)
    assert "reasoning" not in captured and "format" not in captured
    assert captured["max_tokens"] == settings.llm_max_output_tokens
    assert captured["max_retries"] == 0
