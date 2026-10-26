"""
QA & Security Agent
Provides two distinct, traceable engineering capabilities:
1. ai_safety_security_engineer (run_security_audit): Evaluates code & architecture for security risks, guardrails, and secret exposure.
2. qa_test_engineer (run_qa_test_execution): Actually executes pytest on target test files, records test execution evidence, and evaluates coverage/quality.
Also maintains run_qa_security_check for backwards-compatibility.
"""

import argparse
import json
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from src.agents.common import (
    REPO_ROOT,
    clean_json_block,
    extract_message_text,
    read_repository_text_file,
    resolve_authorized_root,
)
from src.app.settings import get_settings
from src.llm.factory import get_chat_model
from src.observability.tracing import (
    append_trace,
    estimate_cost_credits,
    usage_from_message,
)


class QASecurityReport(BaseModel):
    status_str: Literal["approved", "changes_requested", "unparseable", "escalated"] = "approved"
    summary: str
    security_risks: list[str] = Field(default_factory=list)


class QATestExecutionReport(BaseModel):
    status_str: Literal["approved", "changes_requested", "unparseable", "escalated"] = "approved"
    summary: str
    tests_executed: bool = False
    tests_passed: bool = False
    exit_code: int = -1
    test_command: str = ""
    test_output_excerpt: str = ""
    quality_findings: list[str] = Field(default_factory=list)


class QASecurityState(TypedDict, total=False):
    architecture_report: dict[str, Any]
    target_file: str
    base_dir: str
    test_targets: list[str]
    role_mode: str
    source_snippet: str
    pytest_result: dict[str, Any]
    result: dict[str, Any]
    error: str


def _message_text(message: Any) -> str:
    return extract_message_text(message)


def _parse_qa_result(text: str) -> QASecurityReport:
    cleaned = clean_json_block(text)
    try:
        data = json.loads(cleaned)
        return QASecurityReport.model_validate(data)
    except Exception as exc:
        return QASecurityReport(
            status_str="unparseable",
            summary=f"Parsing error: {str(exc)} | Raw: {text[:200]}",
            security_risks=["QA & Security parsing failed."],
        )


def execute_repository_pytest(
    test_targets: list[str] | None = None,
    timeout_seconds: int = 30,
    base_dir: str | None = None,
) -> dict[str, Any]:
    """Safely execute pytest (or standalone product check script) in authorized workspace and return structured evidence."""
    root = resolve_authorized_root(base_dir)
    targets = test_targets or (["test_website.py"] if base_dir else ["tests/test_work_items_api.py"])
    validated_targets: list[str] = []
    for t in targets:
        resolved = (root / t).resolve()
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"Security violation: test path escapes repository root: {t}") from exc
        if not resolved.exists():
            raise FileNotFoundError(f"Test target not found: {t}")
        validated_targets.append(t)

    # If running inside an external customer checkout with a standalone check script, run python directly or pytest
    if base_dir and len(validated_targets) == 1 and validated_targets[0].endswith(".py"):
        cmd = [sys.executable, validated_targets[0]]
        cmd_label = f"python {validated_targets[0]}"
    else:
        cmd = [sys.executable, "-m", "pytest", "-q", *validated_targets]
        cmd_label = " ".join(["python", "-m", "pytest", "-q", *validated_targets])

    try:
        completed = subprocess.run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        stdout_excerpt = (completed.stdout + "\n" + completed.stderr).strip()[:1200]
        return {
            "tests_executed": True,
            "tests_passed": completed.returncode == 0,
            "exit_code": completed.returncode,
            "command": cmd_label,
            "output_excerpt": stdout_excerpt,
        }
    except Exception as exc:
        return {
            "tests_executed": False,
            "tests_passed": False,
            "exit_code": -1,
            "command": cmd_label,
            "output_excerpt": f"test execution failed: {exc}",
        }


def build_qa_security_graph(
    llm: Any | None = None,
    *,
    trace_context: dict[str, Any] | None = None,
    run_tests: bool = False,
):
    llm = llm or get_chat_model()
    trace_ctx = trace_context if trace_context is not None else {"tools": [], "calls": 0}

    def inspect_file(state: QASecurityState) -> QASecurityState:
        target = state.get("target_file")
        base_dir = state.get("base_dir")
        updates: QASecurityState = {"source_snippet": ""}
        if target:
            trace_ctx["tools"].append("read_repository_text_file")
            try:
                snippet = read_repository_text_file(target, base_dir=base_dir)
                updates["source_snippet"] = snippet[:1500]
            except Exception as exc:
                return {"error": str(exc)}

        if run_tests or state.get("role_mode") == "qa_test_engineer":
            trace_ctx["tools"].append("execute_repository_pytest")
            try:
                pytest_res = execute_repository_pytest(state.get("test_targets"), base_dir=base_dir)
                updates["pytest_result"] = pytest_res
            except Exception as exc:
                return {"error": str(exc)}

        return updates

    def route_after_inspect(state: QASecurityState):
        return END if state.get("error") else "analyze"

    def analyze(state: QASecurityState) -> QASecurityState:
        role_mode = state.get("role_mode", "ai_safety_security_engineer")
        pytest_res = state.get("pytest_result")

        if role_mode == "qa_test_engineer" and pytest_res is not None:
            system = SystemMessage(
                content=(
                    "You are the QA & Test Engineer. Evaluate the executed pytest results and source code for "
                    "test coverage and quality. Return ONLY valid JSON matching this schema: "
                    '{"status_str": "approved", "summary": "QA test evaluation", "security_risks": ["finding 1"]}'
                )
            )
        else:
            system = SystemMessage(
                content=(
                    "You are the AI Safety & Security Engineer. Evaluate the architecture report and source code for "
                    "security risks (injection, secret exposure, guardrails, data validation). "
                    "status_str must be 'approved' or 'changes_requested'. Return ONLY valid JSON matching this schema: "
                    '{"status_str": "approved", "summary": "Security audit summary", "security_risks": ["risk 1"]}'
                )
            )

        content_prompt = f"Architecture Report:\n{json.dumps(state.get('architecture_report', {}), indent=2)}"
        if pytest_res is not None:
            content_prompt += f"\n\nExecuted pytest result:\n{json.dumps(pytest_res, indent=2)}"
        if state.get("source_snippet"):
            content_prompt += f"\n\nSource code sample:\n{state['source_snippet']}"

        human = HumanMessage(content=content_prompt)
        trace_ctx["calls"] += 1
        response = llm.invoke([system, human])
        in_tok, out_tok = usage_from_message(response)
        trace_ctx["input_tokens"] = in_tok
        trace_ctx["output_tokens"] = out_tok

        report = _parse_qa_result(_message_text(response))
        report_dict = report.model_dump()

        # Deterministic QA guardrail: if real pytest execution failed, status CANNOT be 'approved'
        if pytest_res is not None:
            report_dict["pytest_execution"] = pytest_res
            if not pytest_res.get("tests_passed", False) and report_dict.get("status_str") == "approved":
                report_dict["status_str"] = "changes_requested"
                report_dict["summary"] = (
                    f"[Guardrail: pytest failed (exit={pytest_res.get('exit_code')})] " + report_dict.get("summary", "")
                )

        report_dict["role"] = role_mode
        report_dict["_usage"] = (in_tok, out_tok)
        return {"result": report_dict}

    builder = StateGraph(QASecurityState)
    builder.add_node("inspect_file", inspect_file)
    builder.add_node("analyze", analyze)
    builder.add_edge(START, "inspect_file")
    builder.add_conditional_edges("inspect_file", route_after_inspect, ["analyze", END])
    builder.add_edge("analyze", END)
    return builder.compile()


def run_security_audit(
    architecture_report: dict[str, Any],
    target_file: str | None = "src/app/main.py",
    *,
    base_dir: str | None = None,
    task_id: str = "SEC-001",
    workflow_id: str | None = None,
    llm: Any | None = None,
    trace_file: str | None = None,
) -> dict[str, Any]:
    """AI Safety & Security Engineer role entry point."""
    return _run_qa_or_security(
        architecture_report=architecture_report,
        target_file=target_file,
        base_dir=base_dir,
        role_mode="ai_safety_security_engineer",
        run_tests=False,
        task_id=task_id,
        workflow_id=workflow_id,
        llm=llm,
        trace_file=trace_file,
    )


def run_qa_test_execution(
    architecture_report: dict[str, Any],
    target_file: str | None = "src/app/main.py",
    test_targets: list[str] | None = None,
    *,
    base_dir: str | None = None,
    task_id: str = "QA-001",
    workflow_id: str | None = None,
    llm: Any | None = None,
    trace_file: str | None = None,
) -> dict[str, Any]:
    """QA & Test Engineer role entry point: executes real pytest suite and evaluates test results."""
    return _run_qa_or_security(
        architecture_report=architecture_report,
        target_file=target_file,
        test_targets=test_targets,
        base_dir=base_dir,
        role_mode="qa_test_engineer",
        run_tests=True,
        task_id=task_id,
        workflow_id=workflow_id,
        llm=llm,
        trace_file=trace_file,
    )


def _run_qa_or_security(
    architecture_report: dict[str, Any],
    target_file: str | None = "src/app/main.py",
    test_targets: list[str] | None = None,
    *,
    base_dir: str | None = None,
    role_mode: Literal["qa_test_engineer", "ai_safety_security_engineer"] = "qa_test_engineer",
    run_tests: bool = False,
    task_id: str = "QA-001",
    workflow_id: str | None = None,
    llm: Any | None = None,
    trace_file: str | None = None,
) -> dict[str, Any]:
    settings = get_settings()
    run_id = str(uuid.uuid4())
    actual_wf_id = workflow_id or run_id
    started = time.perf_counter()
    ctx: dict[str, Any] = {"tools": [], "calls": 0, "input_tokens": None, "output_tokens": None}

    graph = build_qa_security_graph(llm=llm, trace_context=ctx, run_tests=run_tests)
    state = graph.invoke(
        {
            "architecture_report": architecture_report,
            "target_file": target_file or "",
            "base_dir": base_dir or "",
            "test_targets": test_targets or (["test_website.py"] if base_dir else ["tests/test_work_items_api.py"]),
            "role_mode": role_mode,
        },
        {"recursion_limit": 10},
    )
    duration = time.perf_counter() - started

    if state.get("error"):
        report = QASecurityReport(
            status_str="escalated",
            summary=f"Context file error (escalated before LLM call): {state['error']}",
            security_risks=["Target file could not be read; escalated without LLM call."],
        ).model_dump()
        report["role"] = role_mode
        report["error"] = state["error"]
        trace_status = "escalated"
    else:
        report = state.get("result", {})
        report.pop("_usage", None)
        trace_status = "invalid_output" if report.get("status_str") == "unparseable" else "success"

    trace_payload: dict[str, Any] = {
        "run_id": run_id,
        "workflow_id": actual_wf_id,
        "task_id": task_id,
        "agent": "qa_security_agent",
        "role": role_mode,
        "provider": settings.llm_provider if llm is None else "injected",
        "model": settings.llm_model if llm is None else getattr(llm, "model", "mock"),
        "status": trace_status,
        "result_status": report.get("status_str"),
        "tools": ctx["tools"],
        "calls": ctx["calls"],
        "duration_seconds": round(duration, 4),
        "input_tokens": ctx["input_tokens"],
        "output_tokens": ctx["output_tokens"],
        "estimated_cost_credits": estimate_cost_credits(
            duration_seconds=duration,
            input_tokens=ctx["input_tokens"] or 0,
            output_tokens=ctx["output_tokens"] or 0,
            calls=ctx["calls"],
        ),
    }
    if "pytest_execution" in report:
        trace_payload["pytest_execution"] = {
            "tests_executed": report["pytest_execution"].get("tests_executed"),
            "tests_passed": report["pytest_execution"].get("tests_passed"),
            "exit_code": report["pytest_execution"].get("exit_code"),
            "command": report["pytest_execution"].get("command"),
        }

    append_trace(trace_payload, trace_file)
    return report


def run_qa_security_check(
    architecture_report: dict[str, Any],
    target_file: str | None = "src/app/main.py",
    *,
    base_dir: str | None = None,
    test_targets: list[str] | None = None,
    task_id: str = "QA-001",
    workflow_id: str | None = None,
    llm: Any | None = None,
    trace_file: str | None = None,
    run_tests: bool = False,
) -> dict[str, Any]:
    """Compatible entry point used by existing tests and pipeline."""
    return _run_qa_or_security(
        architecture_report=architecture_report,
        target_file=target_file,
        test_targets=test_targets,
        base_dir=base_dir,
        role_mode="qa_test_engineer",
        run_tests=run_tests,
        task_id=task_id,
        workflow_id=workflow_id,
        llm=llm,
        trace_file=trace_file,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="src/app/main.py")
    parser.add_argument("--run-tests", action="store_true")
    args = parser.parse_args()

    sample_arch = {"status_str": "approved", "summary": "Sample architecture", "findings": []}
    res = run_qa_security_check(sample_arch, target_file=args.file, run_tests=args.run_tests)
    print(json.dumps(res, indent=2, ensure_ascii=False))
