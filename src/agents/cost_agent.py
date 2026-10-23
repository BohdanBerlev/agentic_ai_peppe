"""
Cost & Observability Agent
Reads all agent execution trace files, extracts token/runtime usage,
and uses the LLM to generate a structured cost report based on user queries.
"""
import os
import json
import time
import uuid
import argparse
from pathlib import Path
from typing import Any, Literal, TypedDict, List
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from src.llm.factory import get_chat_model
from src.observability.tracing import append_trace, usage_from_message, estimate_cost_credits

REPO_ROOT = Path(__file__).resolve().parents[2]

ORCHESTRATOR_AGENTS = {"feature_pipeline_workflow"}


class CostInsight(BaseModel):
    agent_name: str
    finding: str


class CostReport(BaseModel):
    status: Literal["success", "error", "unparseable"]
    total_runs_analyzed: int
    total_cost_credits: float = 0.0
    total_duration_seconds: float = 0.0
    summary: str
    insights: List[CostInsight] = Field(default_factory=list)


class CostState(TypedDict, total=False):
    log_file_path: str
    log_content: str
    metrics: dict[str, Any]
    user_query: str
    result: dict[str, Any]
    error: str


def read_log_file(directory_path: str = "evidence") -> tuple[str, dict[str, Any]]:
    """Liest ALLE JSONL-Logdateien im Ordner aus und fasst sie ohne Orchestrator-Double-Counting zusammen."""
    log_dir = (REPO_ROOT / directory_path).resolve()

    allowed_evidence = (REPO_ROOT / "evidence").resolve()
    allowed_logs = (REPO_ROOT / "logs").resolve()

    # 1. ZUERST Security: Path Traversal blockieren
    if not (str(log_dir).startswith(str(allowed_evidence)) or str(log_dir).startswith(str(allowed_logs))):
        raise ValueError(f"Security Violation: Pfad '{directory_path}' verlässt die erlaubten Verzeichnisse!")

    # 2. DANN auf Existenz prüfen
    if not log_dir.exists():
        raise FileNotFoundError(f"Pfad nicht gefunden: {log_dir}")

    files = [log_dir] if log_dir.is_file() else list(log_dir.rglob("*.jsonl"))

    extracted_data = []
    total_runs = 0
    total_cost = 0.0
    total_duration = 0.0
    total_human_review_seconds = 0.0
    skipped_summaries = 0

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        if not isinstance(data, dict):
                            continue

                        # Separate human review time recorded on workflow summary lines
                        human_sec = data.get("human_review_seconds")
                        if human_sec is not None:
                            total_human_review_seconds += float(human_sec)

                        # Prevent double-counting of orchestrator summary lines
                        agent_name = data.get("agent", "unknown")
                        record_type = data.get("record_type", "agent_run")
                        if record_type == "workflow_summary" or agent_name in ORCHESTRATOR_AGENTS:
                            skipped_summaries += 1
                            continue

                        total_runs += 1
                        cost = data.get("estimated_cost_credits")
                        if cost is not None:
                            total_cost += float(cost)

                        duration = data.get("duration_seconds")
                        if duration is not None:
                            total_duration += float(duration)

                        extracted_data.append({
                            "task_id": data.get("task_id", "unknown"),
                            "run_id": data.get("run_id", "unknown"),
                            "agent": agent_name,
                            "duration": duration,
                            "cost": cost,
                        })
                    except json.JSONDecodeError:
                        continue

    metrics = {
        "total_runs": total_runs,
        "total_cost": round(total_cost, 4),
        "total_duration": round(total_duration, 4),
        "human_review_seconds": round(total_human_review_seconds, 4),
        "skipped_orchestrator_summaries": skipped_summaries,
    }

    if not extracted_data:
        return f"No execution data found in {directory_path}.", metrics

    return json.dumps(extracted_data, indent=2), metrics


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


def _parse_result(text: str, metrics: dict[str, Any]) -> CostReport:
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
        parsed_json = json.loads(cleaned)
        # Inject deterministic metrics to override whatever the LLM guessed
        parsed_json["total_runs_analyzed"] = metrics["total_runs"]
        parsed_json["total_cost_credits"] = metrics["total_cost"]
        parsed_json["total_duration_seconds"] = metrics["total_duration"]
        return CostReport.model_validate(parsed_json)
    except Exception:
        return CostReport(
            status="unparseable",
            total_runs_analyzed=metrics["total_runs"],
            total_cost_credits=metrics["total_cost"],
            total_duration_seconds=metrics["total_duration"],
            summary="Could not parse LLM output.",
            insights=[],
        )


def build_cost_graph(llm: Any | None = None):
    llm = llm or get_chat_model()

    def load_logs(state: CostState) -> CostState:
        try:
            content, metrics = read_log_file(state.get("log_file_path", "evidence"))
            return {"log_content": content, "metrics": metrics}
        except Exception as exc:
            return {"error": str(exc)}

    def route_after_load(state: CostState):
        return END if state.get("error") else "analyze"

    def analyze(state: CostState) -> CostState:
        metrics = state.get("metrics", {"total_runs": 0, "total_cost": 0.0, "total_duration": 0.0})
        system = SystemMessage(
            content=(
                "You are the Cost & Observability Engineer. Analyze the provided execution logs. "
                "Return ONLY valid JSON matching this exact schema. NEVER translate the JSON keys or the 'status' value! "
                '{"status": "success", "summary": "brief summary", "insights": [{"agent_name": "agent1", "finding": "observation"}]}'
            )
        )
        query = state.get("user_query", "Summarize the overall cost and usage.")
        human = HumanMessage(
            content=f"User Request: {query}\n\nExecution logs:\n{state.get('log_content', '')}"
        )

        try:
            response = llm.invoke([system, human])
            result = _parse_result(_message_text(response), metrics)
            result_dict = result.model_dump()
            result_dict["_usage"] = usage_from_message(response)
            return {"result": result_dict}
        except Exception as exc:
            return {"error": f"LLM Exception: {str(exc)}"}

    builder = StateGraph(CostState)
    builder.add_node("load_logs", load_logs)
    builder.add_node("analyze", analyze)
    builder.add_edge(START, "load_logs")
    builder.add_conditional_edges("load_logs", route_after_load, ["analyze", END])
    builder.add_edge("analyze", END)
    return builder.compile()


def run_cost_analysis(
    log_directory: str = "evidence",
    user_query: str = "Summarize the overall cost and usage.",
    *,
    task_id: str = "COST-REPORT-001",
    workflow_id: str | None = None,
    llm: Any | None = None,
    trace_file: str | None = None,
) -> CostReport:
    run_id = str(uuid.uuid4())
    actual_workflow_id = workflow_id or run_id
    started = time.perf_counter()
    graph = build_cost_graph(llm=llm)

    state = graph.invoke({
        "log_file_path": log_directory,
        "user_query": user_query,
    })
    duration = time.perf_counter() - started

    provider = os.getenv("LLM_PROVIDER", "unknown") if llm is None else "injected"
    model = os.getenv("LLM_MODEL", "unknown") if llm is None else getattr(llm, "model", "mock")

    if state.get("error"):
        append_trace(
            {
                "run_id": run_id,
                "workflow_id": actual_workflow_id,
                "task_id": task_id,
                "agent": "cost_observability_agent",
                "role": "cost_observability_engineer",
                "provider": provider,
                "model": model,
                "status": "error",
                "tools": ["read_log_file"],
                "calls": 0,
                "duration_seconds": round(duration, 4),
                "error": state["error"],
                "estimated_cost_credits": estimate_cost_credits(
                    duration_seconds=duration,
                    input_tokens=0,
                    output_tokens=0,
                    calls=0,
                ),
            },
            trace_file,
        )
        raise RuntimeError(state["error"])

    raw = dict(state["result"])
    input_tokens, output_tokens = raw.pop("_usage", (None, None))
    result = CostReport.model_validate(raw)

    append_trace(
        {
            "run_id": run_id,
            "workflow_id": actual_workflow_id,
            "task_id": task_id,
            "agent": "cost_observability_agent",
            "role": "cost_observability_engineer",
            "provider": provider,
            "model": model,
            "status": "invalid_output" if result.status == "unparseable" else "success",
            "result_status": result.status,
            "tools": ["read_log_file"],
            "calls": 1,
            "duration_seconds": round(duration, 4),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_credits": estimate_cost_credits(
                duration_seconds=duration,
                input_tokens=input_tokens or 0,
                output_tokens=output_tokens or 0,
                calls=1,
            ),
        },
        trace_file,
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, default="Fasse die generellen Kosten und Dauer aller Logs zusammen.")
    parser.add_argument("--dir", type=str, default="evidence/session-02")
    args = parser.parse_args()

    print(f"Running Cost Agent in directory '{args.dir}' with query: '{args.query}'...")
    try:
        result = run_cost_analysis(log_directory=args.dir, user_query=args.query)
        print(result.model_dump_json(indent=2))
    except Exception as e:
        print(f"Agent failed: {e}")
