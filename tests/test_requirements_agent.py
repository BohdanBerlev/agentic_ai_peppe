import json
import pytest
from langchain_core.messages import AIMessage

from src.agents.requirements_agent import (
    _parse_requirements_result,
    read_repository_text_file,
    run_requirements_analysis,
    RequirementsReport,
)


class MockLLMSuccess:
    def invoke(self, messages):
        content = json.dumps({
            "status_str": "approved",
            "summary": "Requirements defined successfully.",
            "acceptance_criteria": [
                "POST /work-items returns 201",
                "Items are stored in PostgreSQL"
            ],
        })
        return AIMessage(content=content)


def test_requirements_parsing_valid():
    raw_json = json.dumps({
        "status_str": "approved",
        "summary": "Valid PO summary",
        "acceptance_criteria": ["Crit A", "Crit B"]
    })
    report = _parse_requirements_result(raw_json)
    assert isinstance(report, RequirementsReport)
    assert report.status_str == "approved"
    assert len(report.acceptance_criteria) == 2


def test_requirements_parsing_invalid_fallback():
    raw_invalid = "Ich bin ein LLM und habe den JSON-Standard ignoriert."
    report = _parse_requirements_result(raw_invalid)
    assert isinstance(report, RequirementsReport)
    assert report.status_str == "unparseable"
    assert "Parsing error" in report.summary
    assert report.acceptance_criteria == []


def test_requirements_tool_security():
    with pytest.raises(ValueError, match="Path escapes repository root"):
        read_repository_text_file("../../etc/shadow")


def test_requirements_run_mocked(tmp_path):
    trace_file = tmp_path / "req_test_trace.jsonl"
    result = run_requirements_analysis(
        description="Erstelle API Endpunkte für Work-Items",
        task_id="REQ-TEST-001",
        llm=MockLLMSuccess(),
        trace_file=str(trace_file),
    )
    assert result["status_str"] == "approved"
    assert len(result["acceptance_criteria"]) == 2
    assert trace_file.exists()

    trace_data = json.loads(trace_file.read_text(encoding="utf-8").splitlines()[0])
    assert trace_data["task_id"] == "REQ-TEST-001"
    assert trace_data["agent"] == "requirements_agent"
    assert trace_data["status"] == "success"