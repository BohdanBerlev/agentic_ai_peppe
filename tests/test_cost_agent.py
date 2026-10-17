import pytest
import json
from src.agents.cost_agent import read_log_file, _parse_result, CostReport

def test_read_log_file_not_found():
    """Prüft, ob das Tool eine fehlende Datei korrekt abfängt."""
    with pytest.raises(FileNotFoundError):
        read_log_file("logs/gibt_es_nicht.jsonl")

def test_read_log_file_path_traversal():
    """Prüft, ob Path Traversal blockiert wird."""
    with pytest.raises(ValueError, match="Security Violation"):
        read_log_file("../../etc/passwd")

def test_parse_result_valid_json():
    """Prüft, ob der LLM-Output korrekt in das Pydantic-Modell umgewandelt wird und Metriken eingefügt werden."""
    mock_llm_output = json.dumps({
        "status": "success",
        "summary": "Mock Summary",
        "insights": [
            {"agent_name": "test-agent", "finding": "Test finding"}
        ]
    })
    
    mock_metrics = {
        "total_runs": 10,
        "total_cost": 2.5,
        "total_duration": 15.0
    }
    
    result = _parse_result(mock_llm_output, mock_metrics)
    
    # Assertions prüfen, ob die Struktur exakt stimmt
    assert isinstance(result, CostReport)
    assert result.status == "success"
    assert result.total_runs_analyzed == 10
    assert result.total_cost_credits == 2.5
    assert result.total_duration_seconds == 15.0
    assert len(result.insights) == 1
    assert result.insights[0].agent_name == "test-agent"

def test_parse_result_invalid_json():
    """Prüft, ob der Parser bei kaputtem LLM-Output einen unparseable-Status zurückgibt, aber Metriken behält."""
    bad_output = "Hier ist dein Report, aber ich habe das JSON vergessen."
    
    mock_metrics = {
        "total_runs": 3,
        "total_cost": 0.5,
        "total_duration": 2.0
    }
    
    result = _parse_result(bad_output, mock_metrics)
    
    assert result.status == "unparseable"
    assert result.total_runs_analyzed == 3
    assert result.total_cost_credits == 0.5