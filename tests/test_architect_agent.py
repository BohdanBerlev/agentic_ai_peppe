import json
import pytest
from langchain_core.messages import AIMessage

from src.agents.architect_agent import (
    _parse_architect_result,
    read_repository_text_file,
    run_architect_review,
    ArchitectureReport,
)


class MockLLMArchitect:
    def invoke(self, messages):
        content = json.dumps({
            "status_str": "approved",
            "summary": "Architecture complies with FastAPI standards.",
            "findings": ["Clean separation between routes and db"],
        })
        return AIMessage(content=content)


def test_architect_parsing_valid():
    raw_json = json.dumps({
        "status_str": "changes_requested",
        "summary": "Database indexes missing",
        "findings": ["Add index on work_items.status"]
    })
    report = _parse_architect_result(raw_json)
    assert isinstance(report, ArchitectureReport)
    assert report.status_str == "changes_requested"
    assert len(report.findings) == 1


def test_architect_parsing_fallback():
    report = _parse_architect_result("Kein JSON")
    assert report.status_str == "unparseable"
    assert "Parsing error" in report.summary
    assert report.findings == ["Architecture parsing failed."]


def test_architect_tool_prevents_path_traversal():
    with pytest.raises(ValueError, match="Security violation"):
        read_repository_text_file("../../../windows/system32/config/sam")


def test_architect_run_mocked(tmp_path):
    trace_file = tmp_path / "arch_test_trace.jsonl"
    result = run_architect_review(
        file_path="src/app/main.py",
        task_id="ARCH-TEST-001",
        llm=MockLLMArchitect(),
        trace_file=str(trace_file),
    )
    assert result["status_str"] == "approved"
    assert len(result["findings"]) == 1
    assert trace_file.exists()

    trace_data = json.loads(trace_file.read_text(encoding="utf-8").splitlines()[0])
    assert trace_data["task_id"] == "ARCH-TEST-001"
    assert trace_data["agent"] == "architect_agent"
    assert "read_repository_text_file" in trace_data["tools"]