import json
import pytest
from langchain_core.messages import AIMessage

from src.agents.requirements_agent import (
    _parse_requirements_result,
    read_repository_text_file,
    run_agent_engineering_spec,
    run_project_planning,
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


def test_requirements_missing_context_file_escalates_without_llm_call(tmp_path):
    class ShouldNotBeCalledLLM:
        def invoke(self, messages):
            raise AssertionError("LLM must not be called when context file is missing")

    trace_file = tmp_path / "req_missing.jsonl"
    result = run_requirements_analysis(
        description="Test missing context",
        context_file="src/app/missing_file.py",
        task_id="REQ-MISSING-001",
        llm=ShouldNotBeCalledLLM(),
        trace_file=str(trace_file),
    )
    assert result["status_str"] == "escalated"
    trace_data = json.loads(trace_file.read_text(encoding="utf-8").splitlines()[0])
    assert trace_data["calls"] == 0
    assert trace_data["status"] == "escalated"


def test_project_manager_and_agent_engineer_distinct_roles(tmp_path):
    """Verifies (#4) that project_manager and agent_engineer produce distinct schemas and trace roles."""
    class RoleAwareMockLLM:
        def invoke(self, messages):
            sys_text = messages[0].content
            if "Project Manager" in sys_text:
                return AIMessage(
                    content=json.dumps({
                        "status_str": "approved",
                        "summary": "2 Work Packages planned",
                        "work_packages": [
                            {"wp_id": "WP-1", "title": "DB Schema", "assigned_role": "data_rag_engineer", "depends_on": [], "estimated_hours": 1.5}
                        ],
                        "delivery_risks": ["DB connection timeout"],
                    })
                )
            return AIMessage(
                content=json.dumps({
                    "status_str": "approved",
                    "summary": "LangGraph spec ready",
                    "graph_nodes": ["load_context", "analyze"],
                    "required_tools": ["read_repository_text_file"],
                    "state_fields": ["task", "result"],
                })
            )

    trace_file = tmp_path / "multi_role.jsonl"
    pm_res = run_project_planning(
        description="Plan work-items feature",
        task_id="PM-TEST-01",
        llm=RoleAwareMockLLM(),
        trace_file=str(trace_file),
    )
    ae_res = run_agent_engineering_spec(
        description="Design agent workflow",
        task_id="AE-TEST-01",
        llm=RoleAwareMockLLM(),
        trace_file=str(trace_file),
    )

    assert pm_res["role"] == "project_manager"
    assert pm_res["work_packages"][0]["wp_id"] == "WP-1"
    assert ae_res["role"] == "agent_engineer"
    assert "load_context" in ae_res["graph_nodes"]

    lines = [json.loads(line) for line in trace_file.read_text(encoding="utf-8").splitlines()]
    assert [r["role"] for r in lines] == ["project_manager", "agent_engineer"]