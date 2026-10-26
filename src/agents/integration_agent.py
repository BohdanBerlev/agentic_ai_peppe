"""
Integration Agent (Integration Engineer Role)
Validates agent-to-agent (A2A) handover contracts, normalizes external task payloads (e.g., GitHub Issues),
and verifies system-level integration readiness across pipeline stages.
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


class IntegrationHandoverReport(BaseModel):
    status_str: Literal["approved", "changes_requested", "unparseable", "escalated"] = "approved"
    summary: str
    validated_handovers: list[str] = Field(default_factory=list)
    interface_gaps: list[str] = Field(default_factory=list)


class IntegrationState(TypedDict, total=False):
    upstream_artifacts: dict[str, Any]
    target_file: str
    base_dir: str
    source_snippet: str
    result: dict[str, Any]
    error: str


def _parse_integration_result(text: str) -> IntegrationHandoverReport:
    cleaned = clean_json_block(text)
    try:
        data = json.loads(cleaned)
        return IntegrationHandoverReport.model_validate(data)
    except Exception as exc:
        return IntegrationHandoverReport(
            status_str="unparseable",
            summary=f"Parsing error: {str(exc)} | Raw: {text[:200]}",
            validated_handovers=[],
            interface_gaps=["Integration parsing failed."],
        )


def build_integration_graph(llm: Any | None = None, *, trace_context: dict[str, Any] | None = None):
    llm = llm or get_chat_model()
    trace_ctx = trace_context if trace_context is not None else {"tools": [], "calls": 0}

    def inspect_interfaces(state: IntegrationState) -> IntegrationState:
        target = state.get("target_file")
        if target:
            trace_ctx["tools"].append("read_repository_text_file")
            try:
                snippet = read_repository_text_file(target, base_dir=state.get("base_dir"))
                return {"source_snippet": snippet[:1500]}
            except Exception as exc:
                return {"error": str(exc)}
        return {"source_snippet": ""}

    def route_after_inspect(state: IntegrationState):
        return END if state.get("error") else "analyze"

    def analyze(state: IntegrationState) -> IntegrationState:
        system = SystemMessage(
            content=(
                "You are the Integration Engineer. Validate the agent-to-agent (A2A) handover artifacts "
                "(Requirements -> Project Plan -> Architecture -> Security/QA) and system API interfaces for "
                "consistency and completeness. Return ONLY valid JSON matching this schema: "
                '{"status_str": "approved", "summary": "integration check summary", '
                '"validated_handovers": ["PO->PM", "PM->SA"], "interface_gaps": []}'
            )
        )
        prompt = (
            f"Upstream Agent Handover Artifacts:\n"
            f"{json.dumps(state.get('upstream_artifacts', {}), indent=2)}"
        )
        if state.get("source_snippet"):
            prompt += f"\n\nTarget interface code:\n{state['source_snippet']}"

        human = HumanMessage(content=prompt)
        trace_ctx["calls"] += 1
        response = llm.invoke([system, human])
        in_tok, out_tok = usage_from_message(response)
        trace_ctx["input_tokens"] = in_tok
        trace_ctx["output_tokens"] = out_tok

        report = _parse_integration_result(extract_message_text(response))
        report_dict = report.model_dump()
        report_dict["role"] = "integration_engineer"
        report_dict["_usage"] = (in_tok, out_tok)
        return {"result": report_dict}

    builder = StateGraph(IntegrationState)
    builder.add_node("inspect_interfaces", inspect_interfaces)
    builder.add_node("analyze", analyze)
    builder.add_edge(START, "inspect_interfaces")
    builder.add_conditional_edges("inspect_interfaces", route_after_inspect, ["analyze", END])
    builder.add_edge("analyze", END)
    return builder.compile()


def run_integration_check(
    upstream_artifacts: dict[str, Any],
    target_file: str | None = "src/app/main.py",
    *,
    base_dir: str | None = None,
    task_id: str = "INT-001",
    workflow_id: str | None = None,
    llm: Any | None = None,
    trace_file: str | None = None,
) -> dict[str, Any]:
    """Integration Engineer role entry point."""
    settings = get_settings()
    run_id = str(uuid.uuid4())
    actual_wf_id = workflow_id or run_id
    started = time.perf_counter()
    ctx: dict[str, Any] = {"tools": [], "calls": 0, "input_tokens": None, "output_tokens": None}

    graph = build_integration_graph(llm=llm, trace_context=ctx)
    state = graph.invoke(
        {
            "upstream_artifacts": upstream_artifacts,
            "target_file": target_file or "",
            "base_dir": base_dir or "",
        },
        {"recursion_limit": 10},
    )
    duration = time.perf_counter() - started

    if state.get("error"):
        report = IntegrationHandoverReport(
            status_str="escalated",
            summary=f"Context file error (escalated before LLM call): {state['error']}",
            validated_handovers=[],
            interface_gaps=["Target file unreadable; escalated without LLM call."],
        ).model_dump()
        report["role"] = "integration_engineer"
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
            "agent": "integration_agent",
            "role": "integration_engineer",
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

    sample_upstream = {"requirements": {"status_str": "approved"}, "architecture": {"status_str": "approved"}}
    res = run_integration_check(sample_upstream, target_file=args.file)
    print(json.dumps(res, indent=2, ensure_ascii=False))
