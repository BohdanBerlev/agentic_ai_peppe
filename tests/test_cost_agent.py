import pytest
import json
from src.agents.cost_agent import read_log_file, _parse_result, CostReport

def test_read_log_file_not_found():
    """Prüft, ob das Tool eine fehlende Datei korrekt abfängt."""
    with pytest.raises(FileNotFoundError):
        read_log_file("logs/gibt_es_nicht.jsonl")

def test_parse_result_valid_json():
    """Prüft, ob der LLM-Output korrekt in das Pydantic-Modell umgewandelt wird."""
    mock_llm_output = json.dumps({
        "status": "success",
        "total_runs_analyzed": 5,
        "summary": "Mock Summary",
        "insights": [
            {"agent_name": "test-agent", "finding": "Test finding"}
        ]
    })
    
    result = _parse_result(mock_llm_output)
    
    # Assertions prüfen, ob die Struktur exakt stimmt
    assert isinstance(result, CostReport)
    assert result.status == "success"
    assert result.total_runs_analyzed == 5
    assert len(result.insights) == 1
    assert result.insights[0].agent_name == "test-agent"

def test_parse_result_invalid_json():
    """Prüft, ob der Parser bei kaputtem LLM-Output einen unparseable-Status zurückgibt."""
    bad_output = "Hier ist dein Report, aber ich habe das JSON vergessen."
    
    result = _parse_result(bad_output)
    
    assert result.status == "unparseable"
    assert result.total_runs_analyzed == 0