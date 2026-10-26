import json
from unittest.mock import patch
import pytest
from langchain_core.messages import AIMessage

from src.workflows.feature_pipeline import (
    EngineeringTask,
    record_human_decision,
    run_feature_pipeline,
)
from src.workflows.run_github_issue import handle_pipeline_result, should_close_issue


class ApprovedMockLLM:
    def __init__(self):
        self.calls = 0

    def invoke(self, messages):
        self.calls += 1
        content = json.dumps({
            "status_str": "approved",
            "summary": "Mock review passed without issues.",
            "acceptance_criteria": ["Endpoint works", "DB persists"],
            "findings": ["Clean structure"],
            "security_risks": [],
        })
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


def test_headless_pipeline_never_auto_approves_under_human_name(tmp_path):
    """Regression test (#1): Headless run with all 'approved' agents must stay pending_human_review."""
    trace_file = tmp_path / "pipeline_headless.jsonl"
    task = EngineeringTask(
        task_id="TEST-HEADLESS-001",
        description="Verify user authentication flow",
        input_files=["src/app/main.py"],
    )

    res = run_feature_pipeline(
        task, llm=ApprovedMockLLM(), trace_file=str(trace_file), interactive=False
    )

    assert res["status"] == "success"
    assert res["result_state"]["requirements"]["status_str"] == "approved"
    assert res["result_state"]["architecture"]["status_str"] == "approved"
    assert res["result_state"]["qa_security"]["status_str"] == "approved"

    approval = res["result_state"]["human_approval"]
    assert approval["agent_recommendation"] == "approved"
    assert approval["decision"] == "pending_human_review"
    assert approval["reviewed_by"] is None
    assert not should_close_issue(res)
    assert trace_file.exists()


def test_pipeline_changes_requested_stays_pending_until_human_decides(tmp_path):
    trace_file = tmp_path / "pipeline_changes.jsonl"
    task = EngineeringTask(
        task_id="TEST-CHANGES-002",
        description="Refactor DB pooling",
        input_files=["src/app/main.py"],
    )

    res = run_feature_pipeline(
        task, llm=ChangesRequestedMockLLM(), trace_file=str(trace_file), interactive=False
    )

    assert res["status"] == "success"
    approval = res["result_state"]["human_approval"]
    assert approval["agent_recommendation"] == "changes_requested"
    assert approval["decision"] == "pending_human_review"
    assert approval["reviewed_by"] is None
    assert not should_close_issue(res)


def test_pipeline_corrupted_output_escalates_to_human(tmp_path):
    trace_file = tmp_path / "pipeline_corrupt.jsonl"
    task = EngineeringTask(
        task_id="TEST-CORRUPT-003",
        description="Process payment gateway",
        input_files=["src/app/main.py"],
    )

    res = run_feature_pipeline(
        task, llm=CorruptedMockLLM(), trace_file=str(trace_file), interactive=False
    )

    assert res["status"] == "invalid_output"
    assert res["result_state"]["requirements"]["status_str"] == "unparseable"
    approval = res["result_state"]["human_approval"]
    assert approval["decision"] == "escalate_to_human_review"
    assert not should_close_issue(res)


def test_missing_context_file_escalates_before_llm_call(tmp_path):
    """Regression test (#10): Missing input file must escalate immediately with 0 LLM calls."""
    trace_file = tmp_path / "pipeline_missing_ctx.jsonl"
    mock_llm = ApprovedMockLLM()
    task = EngineeringTask(
        task_id="TEST-MISSING-CTX-004",
        description="Check non-existent module",
        input_files=["src/app/does_not_exist.py"],
    )

    res = run_feature_pipeline(
        task, llm=mock_llm, trace_file=str(trace_file), interactive=False
    )

    assert mock_llm.calls == 0
    assert res["status"] == "escalated"
    assert res["calls"] == 0
    assert res["estimated_cost_credits"] == 0.0
    approval = res["result_state"]["human_approval"]
    assert approval["decision"] == "escalate_to_human_review"
    assert "File not found" in (res["result_state"]["context_error"] or "")


def test_interactive_human_gate_and_record_decision(tmp_path, monkeypatch):
    trace_file = tmp_path / "pipeline_interactive.jsonl"
    task = EngineeringTask(
        task_id="TEST-INTERACTIVE-005",
        description="Interactive approval test",
        input_files=["src/app/main.py"],
    )

    inputs = iter(["David Pisarkiewicz", "a", "Geprüft und freigegeben."])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    res = run_feature_pipeline(
        task, llm=ApprovedMockLLM(), trace_file=str(trace_file), interactive=True
    )

    approval = res["result_state"]["human_approval"]
    assert approval["decision"] == "approved"
    assert approval["reviewed_by"] == "David Pisarkiewicz"
    assert approval["human_review_seconds"] >= 0.0
    assert should_close_issue(res)

    # Also verify explicit post-hoc human decision recording on a trace
    event = record_human_decision(
        str(trace_file),
        reviewer_name="Mehrose Farooq",
        decision="changes_requested",
        note="Bitte Akzeptanzkriterien nachschärfen.",
        review_seconds=45.0,
    )
    assert event["decision"] == "changes_requested"
    assert event["reviewed_by"] == "Mehrose Farooq"


@patch("src.workflows.run_github_issue.post_comment_only")
@patch("src.workflows.run_github_issue.close_issue_with_success")
def test_github_runner_does_not_close_on_negative_or_pending_decisions(mock_close, mock_comment):
    """Regression test (#1/#2): GitHub issue runner must NOT close issues on changes_requested, invalid_output, or pending."""
    pending_res = {
        "status": "success",
        "result_state": {
            "human_approval": {
                "decision": "pending_human_review",
                "agent_recommendation": "approved",
                "reviewed_by": None,
                "note": "Awaiting human review",
            }
        },
    }
    code = handle_pipeline_result("org/repo", 42, pending_res)
    assert code == 0
    mock_close.assert_not_called()
    mock_comment.assert_called_once()

    mock_comment.reset_mock()
    changes_res = {
        "status": "success",
        "result_state": {
            "human_approval": {
                "decision": "changes_requested",
                "agent_recommendation": "changes_requested",
                "reviewed_by": "David Pisarkiewicz",
                "note": "Fix SQL pooling",
            }
        },
    }
    code = handle_pipeline_result("org/repo", 42, changes_res)
    assert code == 1
    mock_close.assert_not_called()

    invalid_res = {
        "status": "invalid_output",
        "result_state": {
            "human_approval": {
                "decision": "escalate_to_human_review",
                "reviewed_by": None,
            }
        },
    }
    code = handle_pipeline_result("org/repo", 42, invalid_res)
    assert code == 1
    mock_close.assert_not_called()


def test_full_company_mode_and_bounded_backend_retry_loop(tmp_path):
    """Verifies (#4, #11) full 8-role company mode and bounded Backend <-> QA retry loop."""
    trace_file = tmp_path / "full_company.jsonl"
    attempts_seen: list[int] = []

    def fake_backend_agent(state, attempt: int):
        attempts_seen.append(attempt)
        return {
            "status_str": "approved",
            "summary": f"Backend implementation attempt {attempt}",
            "modified_files": ["src/app/main.py"],
            "attempt": attempt,
        }

    class AdaptiveMockLLM:
        def invoke(self, messages):
            sys_prompt = messages[0].content
            if "Project Manager" in sys_prompt:
                return AIMessage(content=json.dumps({
                    "status_str": "approved",
                    "summary": "Planned WPs",
                    "work_packages": [{"wp_id": "WP-1", "title": "API", "assigned_role": "backend_api_engineer"}],
                    "delivery_risks": [],
                }))
            if "Agent Engineer" in sys_prompt:
                return AIMessage(content=json.dumps({
                    "status_str": "approved",
                    "summary": "Graph spec",
                    "graph_nodes": ["requirements", "architect"],
                    "required_tools": ["read_repository_text_file"],
                    "state_fields": ["task"],
                }))
            if "Integration Engineer" in sys_prompt:
                return AIMessage(content=json.dumps({
                    "status_str": "approved",
                    "summary": "Handovers verified",
                    "validated_handovers": ["PO->PM", "PM->SA", "SA->QA"],
                    "interface_gaps": [],
                }))
            # Simulate QA requesting changes on attempt 1, then approving on attempt 2
            if "QA & Test Engineer" in sys_prompt and len(attempts_seen) == 1:
                return AIMessage(content=json.dumps({
                    "status_str": "changes_requested",
                    "summary": "Need edge-case check on attempt 1",
                    "security_risks": ["Add test case"],
                }))
            return AIMessage(content=json.dumps({
                "status_str": "approved",
                "summary": "Passed",
                "acceptance_criteria": ["Crit 1"],
                "findings": ["OK"],
                "security_risks": [],
            }))

    task = EngineeringTask(
        task_id="TEST-COMPANY-006",
        description="End-to-end multi-role verification",
        input_files=["src/app/main.py"],
        test_targets=["tests/starter/test_api.py"],
    )

    res = run_feature_pipeline(
        task,
        llm=AdaptiveMockLLM(),
        trace_file=str(trace_file),
        interactive=False,
        full_company_mode=True,
        backend_agent_fn=fake_backend_agent,
        max_impl_retries=3,
    )

    assert res["status"] == "success"
    assert len(attempts_seen) == 2  # Retried once after QA requested changes, then succeeded!
    assert res["result_state"]["impl_attempts"] == 2
    assert res["result_state"]["project_plan"]["role"] == "project_manager"
    assert res["result_state"]["agent_design"]["role"] == "agent_engineer"
    assert res["result_state"]["security_audit"]["role"] == "ai_safety_security_engineer"
    assert res["result_state"]["integration"]["role"] == "integration_engineer"


def test_pipeline_addresses_client_target_dir(tmp_path):
    """Session 3 Factory Test: Pipeline addresses an external customer checkout via target_dir."""
    from src.agents.common import write_target_text_file

    client_dir = tmp_path / "client-01-website"
    client_dir.mkdir(parents=True, exist_ok=True)
    write_target_text_file("index.html", "<!DOCTYPE html><html lang='de'><body>Nordwerk Industrie-Service</body></html>", target_dir=str(client_dir))
    write_target_text_file("test_website.py", "import sys\nsys.exit(0)\n", target_dir=str(client_dir))

    trace_file = tmp_path / "client_pipeline.jsonl"
    task = EngineeringTask(
        task_id="TASK-001",
        project_id="client-01",
        target_dir=str(client_dir),
        description="Nordwerk Industrie-Service B2B static website RC1",
        input_files=["index.html"],
        test_targets=["test_website.py"],
    )

    res = run_feature_pipeline(
        task,
        llm=ApprovedMockLLM(),
        trace_file=str(trace_file),
        interactive=False,
        run_pytest_in_qa=True,
        session_folder="session-03",
    )

    assert res["status"] == "success"
    assert res["project_id"] == "client-01"
    assert res["target_dir"] == str(client_dir)
    assert res["result_state"]["qa_security"]["pytest_execution"]["tests_passed"] is True


def test_pipeline_target_dir_path_traversal_protection(tmp_path):
    """Session 3 Security Guardrail: Path traversal outside target_dir is rejected with 0 LLM calls."""
    from src.agents.common import write_target_text_file

    client_dir = tmp_path / "client-01-website"
    client_dir.mkdir(parents=True, exist_ok=True)

    with pytest.raises(ValueError, match="Security violation"):
        write_target_text_file("../escape.html", "bad", target_dir=str(client_dir))

    with pytest.raises(ValueError, match="Security violation"):
        write_target_text_file(".git/config", "bad", target_dir=str(client_dir))

    mock_llm = ApprovedMockLLM()
    trace_file = tmp_path / "traversal_trace.jsonl"
    task = EngineeringTask(
        task_id="TASK-TRAVERSAL",
        project_id="client-01",
        target_dir=str(client_dir),
        description="Attempt path traversal",
        input_files=["../secret.txt"],
    )

    res = run_feature_pipeline(
        task, llm=mock_llm, trace_file=str(trace_file), interactive=False
    )

    assert mock_llm.calls == 0
    assert res["status"] == "escalated"
    assert res["calls"] == 0
    assert "Security violation" in (res["result_state"]["context_error"] or "")

