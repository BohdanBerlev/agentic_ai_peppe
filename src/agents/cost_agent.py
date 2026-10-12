"""
Cost & Observability Agent
Reads the agent execution trace file, extracts token/runtime usage,
and uses the LLM to generate a structured cost report.
"""
import json
import time
import uuid
from pathlib import Path
from typing import Any, Literal, TypedDict, List

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field, ValidationError

from src.llm.factory import get_chat_model
from src.observability.tracing import append_trace, usage_from_message

# Pfad zum Hauptverzeichnis des Repositories
REPO_ROOT = Path(__file__).resolve().parents[2]


# 1. Wir definieren den strukturierten Output (Pydantic Model)
class CostInsight(BaseModel):
    agent_name: str
    finding: str

class CostReport(BaseModel):
    status: Literal["success", "error", "unparseable"]
    total_runs_analyzed: int
    summary: str
    insights: List[CostInsight] = Field(default_factory=list)


# 2. Wir definieren den State für LangGraph (den "Rucksack")
class CostState(TypedDict, total=False):
    log_file_path: str
    log_content: str
    result: dict[str, Any]
    error: str


# 3. Das Tool: Die Funktion zum Lesen der Trace-Datei
def read_log_file(relative_path: str) -> str:
    """Liest die JSONL-Logdatei mit den Agenten-Aufzeichnungen."""
    requested = (REPO_ROOT / relative_path).resolve()
    if not requested.is_file():
        raise FileNotFoundError(f"Log file not found: {relative_path}")
    
    # Lese die Datei ein und extrahiere relevante Felder um das LLM nicht zu überladen
    extracted_data = []
    with open(requested, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    data = json.loads(line)
                    # Nur relevante Felder für die Kosten behalten
                    extracted_data.append({
                        "agent": data.get("agent", "unknown"),
                        "status": data.get("status", "unknown"),
                        "duration": data.get("duration_seconds", 0),
                        "input_tokens": data.get("input_tokens", 0),
                        "output_tokens": data.get("output_tokens", 0),
                        "cost": data.get("estimated_cost_credits", 0)
                    })
                except json.JSONDecodeError:
                    continue
                    
    if not extracted_data:
        return "No execution data found in logs."
        
    return json.dumps(extracted_data, indent=2)


# Hilfsfunktionen fürs LLM (Parsing)
def _message_text(message: Any) -> str:
    content = getattr(message, "content", "")
    return content if isinstance(content, str) else str(content)

def _parse_result(text: str) -> CostReport:
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
        return CostReport.model_validate(json.loads(cleaned))
    except (json.JSONDecodeError, ValidationError):
        return CostReport(
            status="unparseable",
            total_runs_analyzed=0,
            summary="Could not parse LLM output.",
            insights=[],
        )


# 4. Der LangGraph-Aufbau
def build_cost_graph(llm: Any | None = None):
    llm = llm or get_chat_model()

    # Node 1: Log-Datei einlesen
    def load_logs(state: CostState) -> CostState:
        try:
            content = read_log_file(state["log_file_path"])
            return {"log_content": content}
        except Exception as exc:
            return {"error": str(exc)}

    # Conditional Edge: Wenn Fehler beim Lesen, brich ab
    def route_after_load(state: CostState):
        return END if state.get("error") else "analyze"

    # Node 2: LLM Analyse
    def analyze(state: CostState) -> CostState:
        system = SystemMessage(
            content=(
                "You are the Cost & Observability Engineer. Analyze the provided execution logs. "
                "Return ONLY valid JSON matching this schema: "
                '{"status": "success", "total_runs_analyzed": integer, "summary": "brief overview", '
                '"insights": [{"agent_name": "agent1", "finding": "observation about cost/tokens"}]}'
            )
        )
        human = HumanMessage(
            content=f"Please analyze these execution logs and summarize the cost/usage data:\n{state['log_content']}"
        )
        response = llm.invoke([system, human])
        result = _parse_result(_message_text(response))
        result_dict = result.model_dump()
        result_dict["_usage"] = usage_from_message(response)
        return {"result": result_dict}

    builder = StateGraph(CostState)
    builder.add_node("load_logs", load_logs)
    builder.add_node("analyze", analyze)
    builder.add_edge(START, "load_logs")
    builder.add_conditional_edges("load_logs", route_after_load, ["analyze", END])
    builder.add_edge("analyze", END)
    return builder.compile()


# 5. Die Ausführungs-Funktion (wie run_review im Starter)
def run_cost_analysis(
    log_file_path: str = "logs/agent-runs.jsonl",
    *,
    task_id: str = "COST-REPORT-001",
    trace_file: str | None = None,
) -> CostReport:
    run_id = str(uuid.uuid4())
    started = time.perf_counter()
    graph = build_cost_graph()
    
    state = graph.invoke({"log_file_path": log_file_path})
    duration = time.perf_counter() - started

    # Fehlerbehandlung
    if state.get("error"):
        append_trace(
            {
                "run_id": run_id,
                "task_id": task_id,
                "agent": "cost_observability_agent",
                "status": "error",
                "tools": ["read_log_file"],
                "duration_seconds": round(duration, 4),
                "error": state["error"],
            },
            trace_file,
        )
        raise RuntimeError(state["error"])

    # Erfolgreicher Durchlauf
    raw = dict(state["result"])
    input_tokens, output_tokens = raw.pop("_usage", (None, None))
    result = CostReport.model_validate(raw)

    append_trace(
        {
            "run_id": run_id,
            "task_id": task_id,
            "agent": "cost_observability_agent",
            "status": "success",
            "tools": ["read_log_file"],
            "duration_seconds": round(duration, 4),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        },
        trace_file,
    )
    return result


if __name__ == "__main__":
    print("Running Cost Agent...")
    try:
        result = run_cost_analysis()
        print(result.model_dump_json(indent=2))
    except Exception as e:
        print(f"Agent failed: {e}")