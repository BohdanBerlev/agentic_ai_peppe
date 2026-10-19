"""
QA & Security Agent (QA & Test and AI Safety & Security Roles)
Evaluates architecture findings, identifies security risks, and assesses test requirements.
"""

import argparse
import json
import time
import uuid
from pathlib import Path
from typing import Any, Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from src.app.settings import get_settings
from src.llm.factory import get_chat_model
from src.observability.tracing import (
    append_trace,
    estimate_cost_credits,
    usage_from_message,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


class QASecurityReport(BaseModel):
    status_str: Literal["approved", "changes_requested", "unparseable"] = "approved"
    summary: str
    security_risks: list[str] = Field(default_factory=list)


class QASecurityState(TypedDict, total=False):
    architecture_report: dict[str, Any]
    target_file: str
    source_snippet: str
    result: dict[str, Any]
    error: str


def read_repository_text_file(relative_path: str) -> str:
    """Sicherer Dateizugriff zur Verifikation von Quelltext-Sicherheitsrisiken."""
    requested = (REPO_ROOT / relative_path).resolve()
    try:
        requested.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise ValueError(f"Path escapes repository root: {relative_path}") from exc
    if not requested.is_file():
        raise FileNotFoundError(f"File not found: {relative_path}")
    return requested.read_text(encoding="utf-8")


def _message_text(message: Any) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "\n".join(parts)
    return str(content)


def _parse_qa_result(text: str) -> QASecurityReport:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].lstrip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        cleaned = cleaned[start : end + 1]

    try:
        data = json.loads(cleaned)
        return QASecurityReport.model_validate(data)
    except Exception as exc:
        return QASecurityReport(
            status_str="unparseable",
            summary=f"Parsing error: {str(exc)} | Raw: {text[:200]}",
            security_risks=["QA & Security parsing failed."],
        )


def build_qa_security_graph(llm: Any | None = None, *, trace_context: dict[str, Any] | None = None):
    llm = llm or get_chat_model()
    trace_ctx = trace_context if trace_context is not None else {"tools": [], "calls": 0}

    def inspect_file(state: QASecurityState) -> QASecurityState:
        target = state.get("target_file")
        if target:
            trace_ctx["tools"].append("read_repository_text_file")
            try:
                snippet = read_repository_text_file(target)
                return {"source_snippet": snippet[:1500]}
            except Exception as exc:
                return {"error": str(exc)}
        return {"source_snippet": ""}

    def analyze(state: QASecurityState) -> QASecurityState:
        system = SystemMessage(
            content=(
                "You are the QA & Security Engineer. Evaluate the architecture report and source code for "
                "functional correctness, test coverage, and security risks (e.g. injection, data validation). "
                "status_str must be 'approved' or 'changes_requested'. Return ONLY valid JSON matching this schema: "
                '{"status_str": "approved", "summary": "QA evaluation summary", "security_risks": ["risk 1"]}'
            )
        )
        content_prompt = f"Architecture Report:\n{json.dumps(state.get('architecture_report', {}), indent=2)}"
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
        report_dict["_usage"] = (in_tok, out_tok)
        return {"result": report_dict}

    builder = StateGraph(QASecurityState)
    builder.add_node("inspect_file", inspect_file)
    builder.add_node("analyze", analyze)
    builder.add_edge(START, "inspect_file")
    builder.add_edge("inspect_file", "analyze")
    builder.add_edge("analyze", END)
    return builder.compile()


def run_qa_security_check(
    architecture_report: dict[str, Any],
    target_file: str | None = "src/app/main.py",
    *,
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

    graph = build_qa_security_graph(llm=llm, trace_context=ctx)
    state = graph.invoke(
        {"architecture_report": architecture_report, "target_file": target_file or ""},
        {"recursion_limit": 10},
    )
    duration = time.perf_counter() - started

    if state.get("error"):
        report = QASecurityReport(
            status_str="unparseable",
            summary=f"Analysis error: {state['error']}",
            security_risks=["Analysis failed due to runtime error."],
        ).model_dump()
    else:
        report = state.get("result", {})
        report.pop("_usage", None)

    append_trace(
        {
            "run_id": run_id,
            "workflow_id": actual_wf_id,
            "task_id": task_id,
            "agent": "qa_security_agent",
            "role": "qa_test_engineer",
            "provider": settings.llm_provider if llm is None else "injected",
            "model": settings.llm_model if llm is None else getattr(llm, "model", "mock"),
            "status": "invalid_output" if report.get("status_str") == "unparseable" else "success",
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
        },
        trace_file,
    )
    return report


if __name__ == "_main_":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="src/app/main.py")
    args = parser.parse_args()

    sample_arch = {"status_str": "approved", "summary": "Sample architecture", "findings": []}
    res = run_qa_security_check(sample_arch, target_file=args.file)
    print(json.dumps(res, indent=2, ensure_ascii=False))