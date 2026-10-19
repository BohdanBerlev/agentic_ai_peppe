import json
import pytest
from langchain_core.messages import AIMessage

from src.workflows.feature_pipeline import EngineeringTask, run_feature_pipeline


class ApprovedMockLLM:
    def invoke(self, messages):
        content = json.dumps({
            "status_str": "approved",
            "summary": "Mock review passed without issues.",
            "acceptance_criteria": ["Endpoint works", "DB persists"],
            "findings": ["Clean structure"],
            "security_risks": [],
        })
        # Gibt absichtlich eine Liste zurück, um Gemini-Verhalten zu verifizieren
        return AIMessage(content=[{"type": "text", "text": content}])


class ChangesRequestedMockLLM:
    def invoke(self, messages):
        content = json.dumps({
            "status_str": "changes_requested",
            "summary": "Security risk identified.",
            "findings": ["Missing input validation"],
            "security_risks": ["Potential injection risk"],
            "acceptance_criteria": [],
        })
        return AIMessage(content=content)


class CorruptedMockLLM:
    def invoke(self, messages):
        return AIMessage(content="Das Modell hat das JSON vergessen.")


def test_pipeline_success_and_human_gate_approval(tmp_path):
    trace_file = tmp_path / "pipeline_success.jsonl"
    task = EngineeringTask(
        task_id="TEST-SUCCESS-001",
        description="Verify user authentication flow",
        input_files=["src/app/main.py"],
    )

    res = run_feature_pipeline(task, llm=ApprovedMockLLM(), trace_file=str(trace_file))

    assert res["status"] == "success"
    assert res["result_state"]["requirements"]["status_str"] == "approved"
    assert res["result_state"]["architecture"]["status_str"] == "approved"
    assert res["result_state"]["qa_security"]["status_str"] == "approved"

    # Human Gate muss einstimmig freigeben
    approval = res["result_state"]["human_approval"]
    assert approval["decision"] == "approved"
    assert "Mehrose Farooq" in approval["reviewed_by"]
    assert trace_file.exists()


def test_pipeline_changes_requested_escalation(tmp_path):
    trace_file = tmp_path / "pipeline_changes.jsonl"
    task = EngineeringTask(
        task_id="TEST-CHANGES-002",
        description="Refactor DB pooling",
        input_files=["src/app/main.py"],
    )

    res = run_feature_pipeline(task, llm=ChangesRequestedMockLLM(), trace_file=str(trace_file))

    assert res["status"] == "success"
    approval = res["result_state"]["human_approval"]
    assert approval["decision"] == "changes_requested"


def test_pipeline_corrupted_output_escalates_to_human(tmp_path):
    trace_file = tmp_path / "pipeline_corrupt.jsonl"
    task = EngineeringTask(
        task_id="TEST-CORRUPT-003",
        description="Process payment gateway",
        input_files=["src/app/main.py"],
    )

    res = run_feature_pipeline(task, llm=CorruptedMockLLM(), trace_file=str(trace_file))

    # Output muss als invalid markiert sein und eskalieren
    assert res["status"] == "invalid_output"
    assert res["result_state"]["requirements"]["status_str"] == "unparseable"
    approval = res["result_state"]["human_approval"]
    assert approval["decision"] == "escalate_to_human_review"