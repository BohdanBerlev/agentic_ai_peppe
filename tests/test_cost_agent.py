import pytest
import json
from src.agents.cost_agent import read_log_file, _parse_result, CostReport, REPO_ROOT


def test_read_log_file_not_found():
    """Prüft, ob das Tool eine fehlende Datei korrekt abfängt."""
    with pytest.raises(FileNotFoundError):
        read_log_file("logs/gibt_es_nicht.jsonl")


def test_read_log_file_path_traversal():
    """Prüft, ob Path Traversal blockiert wird."""
    with pytest.raises(ValueError, match="Security Violation"):
        read_log_file("../../etc/passwd")


def test_read_log_file_excludes_orchestrator_double_counting():
    """Regressionstest (#8): Orchestrator-Summenzeilen ('feature_pipeline_workflow' / 'workflow_summary')
    dürfen NICHT zu den Sub-Agenten-Runs hinzugerechnet werden."""
    test_log = REPO_ROOT / "logs" / "test_double_counting_regression.jsonl"
    test_log.parent.mkdir(parents=True, exist_ok=True)
    try:
        records = [
            {"task_id": "T-1", "run_id": "r1", "agent": "requirements_agent", "duration_seconds": 10.0, "estimated_cost_credits": 1.2},
            {"task_id": "T-1", "run_id": "r2", "agent": "architect_agent", "duration_seconds": 15.0, "estimated_cost_credits": 1.3},
            {"task_id": "T-1", "run_id": "r3", "agent": "qa_security_agent", "duration_seconds": 20.0, "estimated_cost_credits": 1.5},
            {
                "record_type": "workflow_summary",
                "task_id": "T-1",
                "run_id": "r-orch",
                "agent": "feature_pipeline_workflow",
                "duration_seconds": 45.0,
                "human_review_seconds": 120.0,
                "estimated_cost_credits": 4.0,
            },
        ]
        test_log.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")

        _, metrics = read_log_file("logs/test_double_counting_regression.jsonl")

        assert metrics["total_runs"] == 3
        assert metrics["total_cost"] == 4.0  # 1.2 + 1.3 + 1.5 (nicht 8.0!)
        assert metrics["total_duration"] == 45.0  # ohne Orchestrator-Verdopplung & ohne Human-Gate-Wartezeit
        assert metrics["human_review_seconds"] == 120.0
        assert metrics["skipped_orchestrator_summaries"] == 1
    finally:
        if test_log.exists():
            test_log.unlink()


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
