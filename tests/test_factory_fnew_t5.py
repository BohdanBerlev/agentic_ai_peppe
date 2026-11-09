"""Unit tests for Termin 5 targeted Factory improvement F-NEW-v1.0 (Criterion A4)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.llm.factory import resolve_google_model


def test_resolve_google_model_lru_cache_prevents_redundant_http_calls() -> None:
    """Verify F-NEW-v1.0 caches model resolution so 8 agent calls trigger only 1 HTTP request."""
    resolve_google_model.cache_clear()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [
            {
                "name": "models/gemini-3.5-flash-lite",
                "supportedGenerationMethods": ["generateContent"],
            }
        ]
    }

    with patch("httpx.get", return_value=mock_response) as mock_get:
        results = [
            resolve_google_model("gemini-3.5-flash-lite", "test-api-key-fnew")
            for _ in range(8)
        ]

    assert results == ["gemini-3.5-flash-lite"] * 8
    assert mock_get.call_count == 1
    info = resolve_google_model.cache_info()
    assert info.misses == 1
    assert info.hits == 7
    resolve_google_model.cache_clear()
