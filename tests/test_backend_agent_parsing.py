import json

import pytest

from src.agents.backend_agent import _parse_backend_output


def test_valid_json_preserves_code_with_quotes_and_umlauts():
    code = 'raise ValueError("Menge ungültig", "x")  # ä ö ü ß'
    text = json.dumps({"status_str": "approved", "summary": "ok", "code": code})

    parsed = _parse_backend_output(text)

    assert parsed["code"] == code


def test_json_with_real_newlines_in_string():
    text = '{"status_str": "approved", "summary": "s", "code": "line1\nline2"}'

    parsed = _parse_backend_output(text)

    assert parsed["code"] == "line1\nline2"


def test_python_code_block_fallback():
    text = "Hier der Code:\n```python\nprint('ü')\n```\n"

    parsed = _parse_backend_output(text)

    assert parsed == {"code": "print('ü')"}


def test_garbage_raises_json_decode_error():
    with pytest.raises(json.JSONDecodeError):
        _parse_backend_output("das ist kein json und kein codeblock")
