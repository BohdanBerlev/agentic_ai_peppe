"""
Requirements Agent (Product Owner Role)
Analyzes task descriptions, extracts user stories and defines acceptance criteria.
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


class RequirementsReport(BaseModel):
    status_str: Literal["approved", "changes_requested", "unparseable"] = "approved"
    summary: str
    acceptance_criteria: list[str] = Field(default_factory=list)


class RequirementsState(TypedDict, total=False):
    description: str
    context_file: str
    context_data: str
    result: dict[str, Any]
    error: str


def read_repository_text_file(relative_path: str) -> str:
    """Sicherer Dateizugriff innerhalb des Repositorys."""
    requested = (REPO_ROOT / relative_path).resolve()
    try:
        requested.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise ValueError(f"Path escapes repository root: {relative_path}") from exc
    if not requested.is_file():
        raise FileNotFoundError(f"File not found: {relative_path}")
    return requested.read_text(encoding="utf-8")


def _message_text(message: Any) -> str:
    """Konvertiert String- oder Listen-Outputs (z. B. Gemini Content-Blocks) in reinen Text."""
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


def _parse_requirements_result(text: str) -> RequirementsReport:
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
        return RequirementsReport.model_validate(data)
    except Exception as exc:
        return RequirementsReport(
            status_str="unparseable",
            summary=f"Parsing error: {str(exc)} | Raw: {text[:200]}",
            acceptance_criteria=[],
        )


def build_requirements_graph(llm: Any | None = None, *, trace_context: dict[str, Any] | None = None):
    llm = llm or get_chat_model()
    trace_ctx = trace_context if trace_context is not None else {"tools": [], "calls": 0}

    def load_context(state: RequirementsState) -> RequirementsState:
        ctx_file = state.get("context_file")
        if ctx_file:
            trace_ctx["tools"].append("read_repository_text_file")
            try:
                content = read_repository_text_file(ctx_file)
                return {"context_data": content}
            except Exception as exc:
                return {"error": str(exc)}
        return {"context_data": ""}

    def analyze(state: RequirementsState) -> RequirementsState:
        system = SystemMessage(
            content=(
                "You are the Product Owner and Requirements Engineer. Analyze the feature request and "
                "produce clear acceptance criteria. Return ONLY valid JSON matching this schema: "
                '{"status_str": "approved", "summary": "brief summary", "acceptance_criteria": ["crit 1", "crit 2"]}'
            )
        )
        user_prompt = f"Feature Request:\n{state.get('description', '')}"
        if state.get("context_data"):
            user_prompt += f"\n\nContext file content:\n{state['context_data']}"

        human = HumanMessage(content=user_prompt)
        trace_ctx["calls"] += 1
        response = llm.invoke([system, human])
        in_tok, out_tok = usage_from_message(response)
        trace_ctx["input_tokens"] = in_tok
        trace_ctx["output_tokens"] = out_tok

        report = _parse_requirements_result(_message_text(response))
        report_dict = report.model_dump()
        report_dict["_usage"] = (in_tok, out_tok)
        return {"result": report_dict}

    builder = StateGraph(RequirementsState)
    builder.add_node("load_context", load_context)
    builder.add_node("analyze", analyze)
    builder.add_edge(START, "load_context")
    builder.add_edge("load_context", "analyze")
    builder.add_edge("analyze", END)
    return builder.compile()


def run_requirements_analysis(
    description: str,
    context_file: str | None = None,
    *,
    task_id: str = "REQ-001",
    workflow_id: str | None = None,
    llm: Any | None = None,
    trace_file: str | None = None,
) -> dict[str, Any]:
    settings = get_settings()
    run_id = str(uuid.uuid4())
    actual_wf_id = workflow_id or run_id
    started = time.perf_counter()
    ctx: dict[str, Any] = {"tools": [], "calls": 0, "input_tokens": None, "output_tokens": None}

    graph = build_requirements_graph(llm=llm, trace_context=ctx)
    state = graph.invoke(
        {"description": description, "context_file": context_file or ""},
        {"recursion_limit": 10},
    )
    duration = time.perf_counter() - started

    if state.get("error"):
        report = RequirementsReport(
            status_str="unparseable",
            summary=f"Execution error: {state['error']}",
            acceptance_criteria=[],
        ).model_dump()
    else:
        report = state.get("result", {})
        report.pop("_usage", None)

    append_trace(
        {
            "run_id": run_id,
            "workflow_id": actual_wf_id,
            "task_id": task_id,
            "agent": "requirements_agent",
            "role": "product_owner_requirements",
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
    parser.add_argument("--desc", type=str, default="Implement persistent work-items with CRUD endpoints.")
    args = parser.parse_args()

    res = run_requirements_analysis(args.desc)
    print(json.dumps(res, indent=2, ensure_ascii=False))