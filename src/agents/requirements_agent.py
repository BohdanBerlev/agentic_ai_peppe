"""
Requirements & Planning Agent
Supports three distinct engineering roles with role-specific prompts, schemas, outputs, and traces:
1. product_owner_requirements: User stories & acceptance criteria (RequirementsReport)
2. project_manager: Work packages, dependencies, effort & delivery risks (ProjectPlanReport)
3. agent_engineer: LangGraph node/state/tool specification (AgentDesignReport)
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


class RequirementsReport(BaseModel):
    status_str: Literal["approved", "changes_requested", "unparseable", "escalated"] = "approved"
    summary: str
    acceptance_criteria: list[str] = Field(default_factory=list)


class WorkPackageSpec(BaseModel):
    wp_id: str
    title: str
    assigned_role: str = "backend_api_engineer"
    depends_on: list[str] = Field(default_factory=list)
    estimated_hours: float = 2.0


class ProjectPlanReport(BaseModel):
    status_str: Literal["approved", "changes_requested", "unparseable", "escalated"] = "approved"
    summary: str
    work_packages: list[WorkPackageSpec] = Field(default_factory=list)
    delivery_risks: list[str] = Field(default_factory=list)


class AgentDesignReport(BaseModel):
    status_str: Literal["approved", "changes_requested", "unparseable", "escalated"] = "approved"
    summary: str
    graph_nodes: list[str] = Field(default_factory=list)
    required_tools: list[str] = Field(default_factory=list)
    state_fields: list[str] = Field(default_factory=list)


class RequirementsState(TypedDict, total=False):
    description: str
    context_file: str
    base_dir: str
    context_data: str
    role_mode: str
    result: dict[str, Any]
    error: str


def _message_text(message: Any) -> str:
    return extract_message_text(message)


def _parse_requirements_result(text: str) -> RequirementsReport:
    cleaned = clean_json_block(text)
    try:
        data = json.loads(cleaned)
        return RequirementsReport.model_validate(data)
    except Exception as exc:
        return RequirementsReport(
            status_str="unparseable",
            summary=f"Parsing error: {str(exc)} | Raw: {text[:200]}",
            acceptance_criteria=[],
        )


def _parse_project_plan_result(text: str) -> ProjectPlanReport:
    cleaned = clean_json_block(text)
    try:
        data = json.loads(cleaned)
        return ProjectPlanReport.model_validate(data)
    except Exception as exc:
        return ProjectPlanReport(
            status_str="unparseable",
            summary=f"Parsing error: {str(exc)} | Raw: {text[:200]}",
            work_packages=[],
            delivery_risks=[],
        )


def _parse_agent_design_result(text: str) -> AgentDesignReport:
    cleaned = clean_json_block(text)
    try:
        data = json.loads(cleaned)
        return AgentDesignReport.model_validate(data)
    except Exception as exc:
        return AgentDesignReport(
            status_str="unparseable",
            summary=f"Parsing error: {str(exc)} | Raw: {text[:200]}",
            graph_nodes=[],
            required_tools=[],
            state_fields=[],
        )


def build_requirements_graph(llm: Any | None = None, *, trace_context: dict[str, Any] | None = None):
    llm = llm or get_chat_model()
    trace_ctx = trace_ctx = trace_context if trace_context is not None else {"tools": [], "calls": 0}

    def load_context(state: RequirementsState) -> RequirementsState:
        ctx_file = state.get("context_file")
        base_dir = state.get("base_dir")
        if ctx_file:
            trace_ctx["tools"].append("read_repository_text_file")
            try:
                content = read_repository_text_file(ctx_file, base_dir=base_dir)
                return {"context_data": content}
            except Exception as exc:
                return {"error": str(exc)}
        return {"context_data": ""}

    def route_after_load(state: RequirementsState):
        return END if state.get("error") else "analyze"

    def analyze(state: RequirementsState) -> RequirementsState:
        role_mode = state.get("role_mode", "product_owner_requirements")

        if role_mode == "project_manager":
            system = SystemMessage(
                content=(
                    "You are the Project Manager. Break down the requirements into structured Work Packages (WPs), "
                    "assign engineering roles, sequence dependencies, and identify delivery risks. "
                    "Return ONLY valid JSON matching this schema: "
                    '{"status_str": "approved", "summary": "plan summary", '
                    '"work_packages": [{"wp_id": "WP-1", "title": "task", "assigned_role": "backend_api_engineer", '
                    '"depends_on": [], "estimated_hours": 2.0}], "delivery_risks": ["risk 1"]}'
                )
            )
        elif role_mode == "agent_engineer":
            system = SystemMessage(
                content=(
                    "You are the Agent Engineer. Specify the LangGraph workflow nodes, state schema fields, and "
                    "bound tools required to support this engineering task. Return ONLY valid JSON matching this schema: "
                    '{"status_str": "approved", "summary": "agent workflow spec", '
                    '"graph_nodes": ["load_context", "analyze"], "required_tools": ["read_repository_text_file"], '
                    '"state_fields": ["task", "result"]}'
                )
            )
        else:
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

        raw_text = _message_text(response)
        if role_mode == "project_manager":
            report_obj = _parse_project_plan_result(raw_text)
        elif role_mode == "agent_engineer":
            report_obj = _parse_agent_design_result(raw_text)
        else:
            report_obj = _parse_requirements_result(raw_text)

        report_dict = report_obj.model_dump()
        report_dict["role"] = role_mode
        report_dict["_usage"] = (in_tok, out_tok)
        return {"result": report_dict}

    builder = StateGraph(RequirementsState)
    builder.add_node("load_context", load_context)
    builder.add_node("analyze", analyze)
    builder.add_edge(START, "load_context")
    builder.add_conditional_edges("load_context", route_after_load, ["analyze", END])
    builder.add_edge("analyze", END)
    return builder.compile()


def _run_role_analysis(
    description: str,
    context_file: str | None = None,
    *,
    base_dir: str | None = None,
    role_mode: Literal[
        "product_owner_requirements", "project_manager", "agent_engineer"
    ] = "product_owner_requirements",
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
        {
            "description": description,
            "context_file": context_file or "",
            "base_dir": base_dir or "",
            "role_mode": role_mode,
        },
        {"recursion_limit": 10},
    )
    duration = time.perf_counter() - started

    if state.get("error"):
        if role_mode == "project_manager":
            report = ProjectPlanReport(
                status_str="escalated",
                summary=f"Context file error (escalated before LLM call): {state['error']}",
            ).model_dump()
        elif role_mode == "agent_engineer":
            report = AgentDesignReport(
                status_str="escalated",
                summary=f"Context file error (escalated before LLM call): {state['error']}",
            ).model_dump()
        else:
            report = RequirementsReport(
                status_str="escalated",
                summary=f"Context file error (escalated before LLM call): {state['error']}",
            ).model_dump()
        report["role"] = role_mode
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
            "agent": "requirements_agent",
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
        },
        trace_file,
    )
    return report


def run_requirements_analysis(
    description: str,
    context_file: str | None = None,
    *,
    base_dir: str | None = None,
    task_id: str = "REQ-001",
    workflow_id: str | None = None,
    llm: Any | None = None,
    trace_file: str | None = None,
) -> dict[str, Any]:
    """Product Owner / Requirements Engineer role entry point."""
    return _run_role_analysis(
        description=description,
        context_file=context_file,
        base_dir=base_dir,
        role_mode="product_owner_requirements",
        task_id=task_id,
        workflow_id=workflow_id,
        llm=llm,
        trace_file=trace_file,
    )


def run_project_planning(
    description: str,
    requirements_report: dict[str, Any] | None = None,
    context_file: str | None = None,
    *,
    base_dir: str | None = None,
    task_id: str = "PM-001",
    workflow_id: str | None = None,
    llm: Any | None = None,
    trace_file: str | None = None,
) -> dict[str, Any]:
    """Project Manager role entry point: creates Work Packages (WPs), dependencies, and delivery risks."""
    enriched = description
    if requirements_report:
        enriched += f"\n\nApproved Requirements:\n{json.dumps(requirements_report, indent=2)}"
    return _run_role_analysis(
        description=enriched,
        context_file=context_file,
        base_dir=base_dir,
        role_mode="project_manager",
        task_id=task_id,
        workflow_id=workflow_id,
        llm=llm,
        trace_file=trace_file,
    )


def run_agent_engineering_spec(
    description: str,
    context_file: str | None = None,
    *,
    base_dir: str | None = None,
    task_id: str = "AE-001",
    workflow_id: str | None = None,
    llm: Any | None = None,
    trace_file: str | None = None,
) -> dict[str, Any]:
    """Agent Engineer role entry point: specifies LangGraph nodes, state fields, and bound tools."""
    return _run_role_analysis(
        description=description,
        context_file=context_file,
        base_dir=base_dir,
        role_mode="agent_engineer",
        task_id=task_id,
        workflow_id=workflow_id,
        llm=llm,
        trace_file=trace_file,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--desc", type=str, default="Implement persistent work-items with CRUD endpoints.")
    parser.add_argument(
        "--role",
        type=str,
        choices=["product_owner_requirements", "project_manager", "agent_engineer"],
        default="product_owner_requirements",
    )
    args = parser.parse_args()

    res = _run_role_analysis(args.desc, role_mode=args.role)  # type: ignore[arg-type]
    print(json.dumps(res, indent=2, ensure_ascii=False))
