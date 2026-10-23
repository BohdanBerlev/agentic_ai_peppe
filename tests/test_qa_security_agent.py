import json
import pytest
from langchain_core.messages import AIMessage

from src.agents.qa_security_agent import (
    _parse_qa_result,
    read_repository_text_file,
    run_qa_security_check,
    run_qa_test_execution,
    run_security_audit,
    QASecurityReport,
)


class MockLLMQASecurity:
    def invoke(self, messages):
        content = json.dumps({
            "status_str": "approved",
            "summary": "Code safe from SQL injection.",
            "security_risks": [],
        })
        return AIMessage(content=content)


def test_qa_security_parsing_valid():
    raw_json = json.dumps({
        "status_str": "changes_requested",
        "summary": "Raw SQL injection vulnerability detected",
        "security_risks": ["Line 45 uses unparameterized query"]
    })
    report = _parse_qa_result(raw_json)
    assert isinstance(report, QASecurityReport)
    assert report.status_str == "changes_requested"
    assert len(report.security_risks) == 1


def test_qa_security_parsing_fallback():
    report = _parse_qa_result("Fehlerhafter Text")
    assert report.status_str == "unparseable"
    assert "Parsing error" in report.summary
    assert report.security_risks == ["QA & Security parsing failed."]


def test_qa_security_tool_security():
    with pytest.raises(ValueError, match="Path escapes repository root"):
        read_repository_text_file("../../secret.env")


def test_qa_security_run_mocked(tmp_path):
    trace_file = tmp_path / "qa_test_trace.jsonl"
    result = run_qa_security_check(
        architecture_report={"status_str": "approved", "summary": "OK"},
        target_file="src/app/main.py",
        task_id="QA-TEST-001",
        llm=MockLLMQASecurity(),
        trace_file=str(trace_file),
    )
    assert result["status_str"] == "approved"
    assert trace_file.exists()

    trace_data = json.loads(trace_file.read_text(encoding="utf-8").splitlines()[0])
    assert trace_data["task_id"] == "QA-TEST-001"
    assert trace_data["agent"] == "qa_security_agent"
    assert trace_data["status"] == "success"


def test_qa_security_missing_file_escalates_without_llm_call(tmp_path):
    class ShouldNotBeCalledLLM:
        def invoke(self, messages):
            raise AssertionError("LLM must not be called when file is missing")

    trace_file = tmp_path / "qa_missing.jsonl"
    result = run_qa_security_check(
        architecture_report={"status_str": "approved", "summary": "OK"},
        target_file="src/app/missing_file.py",
        task_id="QA-MISSING-001",
        llm=ShouldNotBeCalledLLM(),
        trace_file=str(trace_file),
    )
    assert result["status_str"] == "escalated"
    trace_data = json.loads(trace_file.read_text(encoding="utf-8").splitlines()[0])
    assert trace_data["calls"] == 0
    assert trace_data["status"] == "escalated"


def test_qa_executes_real_pytest_and_separates_security_role(tmp_path):
    """Verifies (#4, #7) distinct qa_test_engineer (with real pytest execution) and ai_safety_security_engineer roles."""
    trace_file = tmp_path / "qa_sec_split.jsonl"
    qa_res = run_qa_test_execution(
        architecture_report={"status_str": "approved", "summary": "OK"},
        target_file="src/app/main.py",
        test_targets=["tests/starter/test_api.py"],
        task_id="QA-EXEC-01",
        llm=MockLLMQASecurity(),
        trace_file=str(trace_file),
    )
    sec_res = run_security_audit(
        architecture_report={"status_str": "approved", "summary": "OK"},
        target_file="src/app/main.py",
        task_id="SEC-AUDIT-01",
        llm=MockLLMQASecurity(),
        trace_file=str(trace_file),
    )

    assert qa_res["role"] == "qa_test_engineer"
    assert qa_res["pytest_execution"]["tests_executed"] is True
    assert qa_res["pytest_execution"]["tests_passed"] is True
    assert sec_res["role"] == "ai_safety_security_engineer"

    lines = [json.loads(line) for line in trace_file.read_text(encoding="utf-8").splitlines()]
    assert [r["role"] for r in lines] == ["qa_test_engineer", "ai_safety_security_engineer"]
    assert lines[0]["pytest_execution"]["tests_passed"] is True