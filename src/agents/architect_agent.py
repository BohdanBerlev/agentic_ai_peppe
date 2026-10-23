"""
Architect Agent (Software Architect Role)
Reviews code structure, endpoint designs, and API contracts.
"""

import argparse
import json
import time
import uuid
from typing import Any, Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from src.agents.common import (
    REPO_ROOT,
    clean_json_block,
    extract_message_text,
    read_repository_text_file,
)
from src.app.settings import get_settings
from src.llm.factory import get_chat_model
from src.observability.tracing import (
    append_trace,
    estimate_cost_credits,
    usage_from_message,
)


class ArchitectureReport(BaseModel):
    status_str: Literal["approved", "changes_requested", "unparseable", "escalated"] = "approved"
    summary: str
    findings: list[str] = Field(default_factory=list)


class ArchitectState(TypedDict, total=False):
    file_path: str
    code_content: str
    result: dict[str, Any]
    error: str


def _message_text(message: Any) -> str:
    return extract_message_text(message)


def _parse_architect_result(text: str) -> ArchitectureReport:
    cleaned = clean_json_block(text)
    try:
        data = json.loads(cleaned)
        return ArchitectureReport.model_validate(data)
    except Exception as exc:
        return ArchitectureReport(
            status_str="unparseable",
            summary=f"Parsing error: {str(exc)} | Raw: {text[:200]}",
            findings=["Architecture parsing failed."],
        )


def build_architect_graph(llm: Any | None = None, *, trace_context: dict[str, Any] | None = None):
    llm = llm or get_chat_model()
    trace_ctx = trace_context if trace_context is not None else {"tools": [], "calls": 0}

    def load_code(state: ArchitectState) -> ArchitectState:
        target_file = state.get("file_path", "src/app/main.py")
        trace_ctx["tools"].append("read_repository_text_file")
        try:
            code = read_repository_text_file(target_file)
            return {"code_content": code}
        except Exception as exc:
            return {"error": str(exc)}

    def route_after_load(state: ArchitectState):
        return END if state.get("error") else "analyze"

    def analyze(state: ArchitectState) -> ArchitectState:
        system = SystemMessage(
            content=(
                "You are the Software Architect. Review the architecture, interface contracts, and code structure. "
                "status_str must be 'approved' or 'changes_requested'. Return ONLY valid JSON with keys "
                "status_str, summary, findings. Example: "
                '{"status_str": "approved", "summary": "Architecture is clean", "findings": ["finding 1"]}'
            )
        )
        human = HumanMessage(
            content=f"Review file {state.get('file_path')}:\n\n{state.get('code_content', '')}"
        )
        trace_ctx["calls"] += 1
        response = llm.invoke([system, human])
        in_tok, out_tok = usage_from_message(response)
        trace_ctx["input_tokens"] = in_tok
        trace_ctx["output_tokens"] = out_tok

        report = _parse_architect_result(_message_text(response))
        report_dict = report.model_dump()
        report_dict["_usage"] = (in_tok, out_tok)
        return {"result": report_dict}

    builder = StateGraph(ArchitectState)
    builder.add_node("load_code", load_code)
    builder.add_node("analyze", analyze)
    builder.add_edge(START, "load_code")
    builder.add_conditional_edges("load_code", route_after_load, ["analyze", END])
    builder.add_edge("analyze", END)
    return builder.compile()


def run_architect_review(
    file_path: str = "src/app/main.py",
    *,
    task_id: str = "ARCH-001",
    workflow_id: str | None = None,
    llm: Any | None = None,
    trace_file: str | None = None,
) -> dict[str, Any]:
    settings = get_settings()
    run_id = str(uuid.uuid4())
    actual_wf_id = workflow_id or run_id
    started = time.perf_counter()
    ctx: dict[str, Any] = {"tools": [], "calls": 0, "input_tokens": None, "output_tokens": None}

    graph = build_architect_graph(llm=llm, trace_context=ctx)
    state = graph.invoke({"file_path": file_path}, {"recursion_limit": 10})
    duration = time.perf_counter() - started

    if state.get("error"):
        report = ArchitectureReport(
            status_str="escalated",
            summary=f"File error (escalated before LLM call): {state['error']}",
            findings=["File read failed; escalated without LLM invocation."],
        ).model_dump()
        report["error"] = state["error"]
        trace_status = "escalated"
    else:
        report = state.get("result", {})
        report.pop("_usage", None)
        trace_status = "invalid_output" if report.get("status_str") == "unparseable" else "success"

    append_trace(
        {
            "run_id": run_id,
            "workflow_id": actual_wf_id,
            "task_id": task_id,
            "agent": "architect_agent",
            "role": "software_architect",
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
        },
        trace_file,
    )
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="src/app/main.py")
    args = parser.parse_args()

    res = run_architect_review(args.file)
    print(json.dumps(res, indent=2, ensure_ascii=False))
