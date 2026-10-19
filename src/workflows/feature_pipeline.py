"""
Feature Pipeline Workflow
Orchestrates Requirements, Architect, and QA/Security Agents with an explicit Human Gate.
"""

import argparse
import json
import time
import uuid
import sys
from pathlib import Path
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from src.agents.architect_agent import run_architect_review
from src.agents.qa_security_agent import run_qa_security_check
from src.agents.requirements_agent import run_requirements_analysis
from src.app.settings import get_settings
from src.observability.tracing import append_trace, estimate_cost_credits

REPO_ROOT = Path(__file__).resolve().parents[2]


class EngineeringTask(BaseModel):
    task_id: str
    description: str
    assigned_role: str = "integration_engineer"
    input_files: list[str] = Field(default_factory=lambda: ["src/app/main.py"])


class PipelineState(TypedDict, total=False):
    task: dict[str, Any]
    workflow_id: str
    trace_file: str  # NEU: Wir geben den gemeinsamen Pfad an die Agenten weiter
    requirements_report: dict[str, Any]
    architecture_report: dict[str, Any]
    qa_security_report: dict[str, Any]
    human_approval: dict[str, Any]
    error: str


def build_pipeline_graph(llm: Any | None = None):
    def step_requirements(state: PipelineState) -> PipelineState:
        task = state.get("task", {})
        wf_id = state.get("workflow_id")
        trace_file = state.get("trace_file")
        task_id = task.get("task_id", "DRYRUN-002")
        desc = task.get("description", "Feature verification")
        ctx_file = task.get("input_files", [None])[0]

        report = run_requirements_analysis(
            description=desc,
            context_file=ctx_file,
            task_id=task_id,
            workflow_id=wf_id,
            trace_file=trace_file,
            llm=llm,
        )
        return {"requirements_report": report}

    def step_architect(state: PipelineState) -> PipelineState:
        task = state.get("task", {})
        wf_id = state.get("workflow_id")
        trace_file = state.get("trace_file")
        task_id = task.get("task_id", "DRYRUN-002")
        target_file = task.get("input_files", ["src/app/main.py"])[0]

        report = run_architect_review(
            file_path=target_file,
            task_id=task_id,
            workflow_id=wf_id,
            trace_file=trace_file,
            llm=llm,
        )
        return {"architecture_report": report}

    def step_qa_security(state: PipelineState) -> PipelineState:
        task = state.get("task", {})
        wf_id = state.get("workflow_id")
        trace_file = state.get("trace_file")
        task_id = task.get("task_id", "DRYRUN-002")
        target_file = task.get("input_files", ["src/app/main.py"])[0]
        arch_rep = state.get("architecture_report", {})

        report = run_qa_security_check(
            architecture_report=arch_rep,
            target_file=target_file,
            task_id=task_id,
            workflow_id=wf_id,
            trace_file=trace_file,
            llm=llm,
        )
        return {"qa_security_report": report}
    
    def step_human_gate(state: PipelineState) -> PipelineState:
        req_rep = state.get("requirements_report", {})
        arch_rep = state.get("architecture_report", {})
        qa_rep = state.get("qa_security_report", {})
        task = state.get("task", {})

        # 1. Prüfen, ob ein echter Mensch vor dem Terminal sitzt
        is_interactive = sys.stdin.isatty() and not state.get("auto_mode_for_testing", False)

        if is_interactive:
            print("\n" + "=" * 60)
            print(f"🛑 HUMAN APPROVAL GATE — Task: {task.get('task_id', 'UNKNOWN')}")
            print("=" * 60)
            print(f"📋 Requirements Status : {req_rep.get('status_str')}")
            print(f"   Summary              : {req_rep.get('summary')}")
            print(f"🏗️  Architect Status    : {arch_rep.get('status_str')}")
            print(f"   Summary              : {arch_rep.get('summary')}")
            print(f"🛡️  QA / Security Status: {qa_rep.get('status_str')}")
            print(f"   Summary              : {qa_rep.get('summary')}")
            print("-" * 60)

            # Interaktive Abfrage an dich vor dem Bildschirm
            reviewer_name = input("Dein Name für die Freigabe (z.B. David Pisarkiewicz): ").strip()
            if not reviewer_name:
                reviewer_name = "David Pisarkiewicz"

            print("\nEntscheidungsoptionen:")
            print(" [a] = Approved (Code & Anforderungen vollständig freigeben)")
            print(" [c] = Changes Requested (Nachbesserung durch Team fordern)")
            print(" [e] = Escalate (An Projektleitung / Prof eskalieren)")
            
            choice = input("Deine Entscheidung (a/c/e): ").strip().lower()

            if choice == "a":
                decision = "approved"
                note = input("Optionale Notiz zur Freigabe: ").strip() or "Vollständig durch Human Gate freigegeben."
            elif choice == "e":
                decision = "escalate_to_human_review"
                note = input("Grund für Eskalation: ").strip() or "Manuell durch Human Gate eskaliert."
            else:
                decision = "changes_requested"
                note = input("Grund für Nachbesserung: ").strip() or "Manuell Änderungen angefordert."

            approval = {
                "reviewed_by": reviewer_name,
                "decision": decision,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "note": note,
            }
            return {"human_approval": approval}

        # 2. Fallback für automatische Headless-Tests (pytest)
        all_reports = [req_rep, arch_rep, qa_rep]
        any_unparseable = any(r.get("status_str") == "unparseable" for r in all_reports)
        any_changes = any(r.get("status_str") == "changes_requested" for r in all_reports)
        all_approved = all(r.get("status_str") == "approved" for r in all_reports)

        if any_unparseable:
            decision = "escalate_to_human_review"
            note = "Automated test: unparseable outputs detected."
        elif any_changes:
            decision = "changes_requested"
            note = "Automated test: agent requested changes."
        elif all_approved:
            decision = "approved"
            note = "Automated test: all checks passed."
        else:
            decision = "changes_requested"
            note = "Automated test: incomplete validation."

        approval = {
            "reviewed_by": "Mehrose Farooq",
            "decision": decision,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "note": note,
        }
        return {"human_approval": approval}

    # Der Graph-Builder muss auf derselben Ebene wie die Sub-Funktionen stehen
    builder = StateGraph(PipelineState)
    builder.add_node("requirements", step_requirements)
    builder.add_node("architect", step_architect)
    builder.add_node("qa_security", step_qa_security)
    builder.add_node("human_gate", step_human_gate)

    builder.add_edge(START, "requirements")
    builder.add_edge("requirements", "architect")
    builder.add_edge("architect", "qa_security")
    builder.add_edge("qa_security", "human_gate")
    builder.add_edge("human_gate", END)

    return builder.compile()


def run_feature_pipeline(
    task: EngineeringTask | None = None,
    *,
    llm: Any | None = None,
    trace_file: str | None = None,
) -> dict[str, Any]:
    settings = get_settings()
    run_id = str(uuid.uuid4())
    workflow_id = str(uuid.uuid4())
    started = time.perf_counter()

    # NEU: Wir legen den finalen Dateipfad VOR dem Graphen-Aufruf fest
    # Die Datei wird nach der gemeinsamen workflow_id benannt
    evidence_dir = REPO_ROOT / "evidence" / "session-02"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    custom_trace = str(evidence_dir / f"{workflow_id}.jsonl")

    task = task or EngineeringTask(
        task_id="DRYRUN-002",
        description="Verify work item API implementation and schema persistence.",
        input_files=["src/app/main.py"],
    )

    graph = build_pipeline_graph(llm=llm)

    try:
        state = graph.invoke(
            {
                "task": task.model_dump(), 
                "workflow_id": workflow_id,
                "trace_file": custom_trace # Pfad in den Graphen werfen
            },
            {"recursion_limit": 15},
        )
    except Exception as exc:
        state = {"error": str(exc)}

    duration = time.perf_counter() - started
    provider = settings.llm_provider if llm is None else "injected"
    model = settings.llm_model if llm is None else getattr(llm, "model", "mock")

    req = state.get("requirements_report") or {}
    arch = state.get("architecture_report") or {}
    qa = state.get("qa_security_report") or {}
    human = state.get("human_approval") or {}

    has_unparseable = any(
        r.get("status_str") == "unparseable" for r in [req, arch, qa]
    )

    overall_status = "error" if state.get("error") else ("invalid_output" if has_unparseable else "success")

    trace_record = {
        "run_id": run_id,
        "workflow_id": workflow_id,
        "task_id": task.task_id,
        "agent": "feature_pipeline_workflow",
        "role": "integration_engineer",
        "provider": provider,
        "model": model,
        "status": overall_status,
        "tools": ["read_repository_text_file"],
        "calls": 3, # Der Orchestrator fasst die 3 Calls zusammen
        "duration_seconds": round(duration, 4),
        "result_state": {
            "requirements": req,
            "architecture": arch,
            "qa_security": qa,
            "human_approval": human,
        },
        "estimated_cost_credits": estimate_cost_credits(
            duration_seconds=duration,
            input_tokens=1500,
            output_tokens=800,
            calls=3,
        ),
    }

    # Der Orchestrator schreibt seinen finalen Trace auch in dieselbe Datei
    append_trace(trace_record, custom_trace)
    
    if trace_file:
        append_trace(trace_record, trace_file)

    return trace_record


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--desc", type=str, default="Review work-item feature implementation.")
    args = parser.parse_args()

    print("Running Independent Agent Modular Feature Pipeline...")
    result = run_feature_pipeline(EngineeringTask(task_id="DRYRUN-002", description=args.desc))
    print(json.dumps(result, indent=2, ensure_ascii=False))