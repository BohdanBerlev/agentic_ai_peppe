"""
Feature Pipeline Workflow
Orchestrates multi-role agents (PO Requirements, PM Planning, Agent Engineering Spec, Software Architect,
Backend Implementation Slot + bounded QA/Test retry loop, AI Safety & Security Audit, Integration Handover Check)
with an explicit Human Gate.
"""

import argparse
import json
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Callable, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from src.agents.architect_agent import run_architect_review
from src.agents.common import (
    REPO_ROOT,
    VALID_ACCOUNTABLE_HUMANS,
    read_repository_text_file,
)
from src.agents.integration_agent import run_integration_check
from src.agents.qa_security_agent import (
    run_qa_security_check,
    run_qa_test_execution,
    run_security_audit,
)
from src.agents.requirements_agent import (
    run_agent_engineering_spec,
    run_project_planning,
    run_requirements_analysis,
)
from src.app.settings import get_settings
from src.observability.tracing import append_trace


class EngineeringTask(BaseModel):
    task_id: str
    description: str
    assigned_role: str = "integration_engineer"
    input_files: list[str] = Field(default_factory=lambda: ["src/app/main.py"])
    test_targets: list[str] = Field(default_factory=lambda: ["tests/test_work_items_api.py"])
    parent_workflow_id: str | None = None
    human_feedback: str | None = None


class ImplementationResult(BaseModel):
    """Contract for the Backend / API Engineer implementation agent (pluggable slot)."""

    status_str: Literal["approved", "changes_requested", "unparseable", "escalated"] = "approved"
    summary: str
    modified_files: list[str] = Field(default_factory=list)
    attempt: int = 1


class HumanApprovalRecord(BaseModel):
    reviewed_by: str | None = None
    decision: Literal[
        "approved",
        "changes_requested",
        "escalate_to_human_review",
        "pending_human_review",
    ]
    agent_recommendation: Literal[
        "approved",
        "changes_requested",
        "escalate_to_human_review",
    ]
    task_id: str
    reviewed_artifacts: list[str] = Field(default_factory=list)
    timestamp: str
    human_review_seconds: float = 0.0
    note: str


class PipelineState(TypedDict, total=False):
    task: dict[str, Any]
    workflow_id: str
    trace_file: str
    interactive_override: bool | None
    full_company_mode: bool
    run_pytest_in_qa: bool
    max_impl_retries: int
    impl_attempts: int
    requirements_report: dict[str, Any]
    project_plan_report: dict[str, Any]
    agent_design_report: dict[str, Any]
    architecture_report: dict[str, Any]
    implementation_report: dict[str, Any]
    qa_security_report: dict[str, Any]
    security_audit_report: dict[str, Any]
    integration_report: dict[str, Any]
    human_approval: dict[str, Any]
    context_error: str
    error: str


def _compute_agent_recommendation(reports: list[dict[str, Any]]) -> Literal[
    "approved", "changes_requested", "escalate_to_human_review"
]:
    active_reports = [r for r in reports if r]
    if not active_reports:
        return "escalate_to_human_review"
    statuses = [r.get("status_str") for r in active_reports]
    if any(s in ("unparseable", "escalated") for s in statuses):
        return "escalate_to_human_review"
    if any(s == "changes_requested" for s in statuses):
        return "changes_requested"
    if all(s == "approved" for s in statuses):
        return "approved"
    return "changes_requested"


def build_pipeline_graph(
    llm: Any | None = None,
    *,
    backend_agent_fn: Callable[[dict[str, Any], int], dict[str, Any]] | None = None,
):
    def step_validate_context(state: PipelineState) -> PipelineState:
        task = state.get("task", {})
        files = task.get("input_files") or []
        for rel_path in files:
            try:
                read_repository_text_file(rel_path)
            except Exception as exc:
                return {"context_error": str(exc)}
        return {"impl_attempts": 0}

    def route_after_context(state: PipelineState):
        return "human_gate" if state.get("context_error") else "requirements"

    def step_requirements(state: PipelineState) -> PipelineState:
        task = state.get("task", {})
        wf_id = state.get("workflow_id")
        trace_file = state.get("trace_file")
        task_id = task.get("task_id", "DRYRUN-002")
        desc = task.get("description", "Feature verification")
        if task.get("human_feedback"):
            desc = f"{desc}\n\nPrevious Human Feedback:\n{task['human_feedback']}"
        ctx_file = (task.get("input_files") or [None])[0]

        req_report = run_requirements_analysis(
            description=desc,
            context_file=ctx_file,
            task_id=task_id,
            workflow_id=wf_id,
            trace_file=trace_file,
            llm=llm,
        )
        updates: PipelineState = {"requirements_report": req_report}

        if state.get("full_company_mode") and req_report.get("status_str") != "escalated":
            pm_report = run_project_planning(
                description=desc,
                requirements_report=req_report,
                context_file=ctx_file,
                task_id=task_id,
                workflow_id=wf_id,
                trace_file=trace_file,
                llm=llm,
            )
            ae_report = run_agent_engineering_spec(
                description=desc,
                context_file=ctx_file,
                task_id=task_id,
                workflow_id=wf_id,
                trace_file=trace_file,
                llm=llm,
            )
            updates["project_plan_report"] = pm_report
            updates["agent_design_report"] = ae_report

        return updates

    def route_after_requirements(state: PipelineState):
        req = state.get("requirements_report") or {}
        if req.get("status_str") == "escalated":
            return "human_gate"
        return "architect"

    def step_architect(state: PipelineState) -> PipelineState:
        task = state.get("task", {})
        wf_id = state.get("workflow_id")
        trace_file = state.get("trace_file")
        task_id = task.get("task_id", "DRYRUN-002")
        target_file = (task.get("input_files") or ["src/app/main.py"])[0]

        report = run_architect_review(
            file_path=target_file,
            task_id=task_id,
            workflow_id=wf_id,
            trace_file=trace_file,
            llm=llm,
        )
        return {"architecture_report": report}

    def route_after_architect(state: PipelineState):
        arch = state.get("architecture_report") or {}
        if arch.get("status_str") == "escalated":
            return "human_gate"
        if backend_agent_fn is not None:
            return "backend_implementation"
        return "qa_security"

    def step_backend_implementation(state: PipelineState) -> PipelineState:
        attempts = int(state.get("impl_attempts", 0)) + 1
        if backend_agent_fn is not None:
            impl_res = backend_agent_fn(dict(state), attempts)
        else:
            impl_res = ImplementationResult(
                status_str="approved",
                summary="No backend agent plugged in; inspecting existing repository code.",
                modified_files=state.get("task", {}).get("input_files", []),
                attempt=attempts,
            ).model_dump()
        return {"implementation_report": impl_res, "impl_attempts": attempts}

    def step_qa_security(state: PipelineState) -> PipelineState:
        task = state.get("task", {})
        wf_id = state.get("workflow_id")
        trace_file = state.get("trace_file")
        task_id = task.get("task_id", "DRYRUN-002")
        target_file = (task.get("input_files") or ["src/app/main.py"])[0]
        test_targets = task.get("test_targets") or ["tests/test_work_items_api.py"]
        arch_rep = state.get("architecture_report", {})

        if state.get("full_company_mode"):
            qa_rep = run_qa_test_execution(
                architecture_report=arch_rep,
                target_file=target_file,
                test_targets=test_targets,
                task_id=task_id,
                workflow_id=wf_id,
                trace_file=trace_file,
                llm=llm,
            )
            sec_rep = run_security_audit(
                architecture_report=arch_rep,
                target_file=target_file,
                task_id=task_id,
                workflow_id=wf_id,
                trace_file=trace_file,
                llm=llm,
            )
            int_rep = run_integration_check(
                upstream_artifacts={
                    "requirements": state.get("requirements_report"),
                    "project_plan": state.get("project_plan_report"),
                    "architecture": arch_rep,
                    "qa_test": qa_rep,
                    "security": sec_rep,
                },
                target_file=target_file,
                task_id=task_id,
                workflow_id=wf_id,
                trace_file=trace_file,
                llm=llm,
            )
            return {
                "qa_security_report": qa_rep,
                "security_audit_report": sec_rep,
                "integration_report": int_rep,
            }

        report = run_qa_security_check(
            architecture_report=arch_rep,
            target_file=target_file,
            task_id=task_id,
            workflow_id=wf_id,
            trace_file=trace_file,
            llm=llm,
            run_tests=bool(state.get("run_pytest_in_qa", False)),
        )
        return {"qa_security_report": report}

    def route_after_qa(state: PipelineState):
        """Bounded Backend <-> QA repair loop (max_impl_retries, default 3) when backend_agent_fn is plugged in."""
        if backend_agent_fn is None:
            return "human_gate"
        qa_rep = state.get("qa_security_report") or {}
        attempts = int(state.get("impl_attempts", 1))
        max_retries = int(state.get("max_impl_retries", 3))
        if qa_rep.get("status_str") == "changes_requested" and attempts < max_retries:
            return "backend_implementation"
        return "human_gate"

    def step_human_gate(state: PipelineState) -> PipelineState:
        gate_started = time.perf_counter()
        req_rep = state.get("requirements_report") or {}
        pm_rep = state.get("project_plan_report") or {}
        ae_rep = state.get("agent_design_report") or {}
        arch_rep = state.get("architecture_report") or {}
        qa_rep = state.get("qa_security_report") or {}
        sec_rep = state.get("security_audit_report") or {}
        int_rep = state.get("integration_report") or {}
        task = state.get("task", {})
        task_id = task.get("task_id", "UNKNOWN")
        ctx_err = state.get("context_error")

        all_reports = [req_rep, pm_rep, ae_rep, arch_rep, qa_rep, sec_rep, int_rep]
        if ctx_err:
            recommendation: Literal[
                "approved", "changes_requested", "escalate_to_human_review"
            ] = "escalate_to_human_review"
        else:
            recommendation = _compute_agent_recommendation(all_reports)

        reviewed_artifacts = [
            name
            for name, rep in [
                ("requirements_report", req_rep),
                ("project_plan_report", pm_rep),
                ("agent_design_report", ae_rep),
                ("architecture_report", arch_rep),
                ("qa_security_report", qa_rep),
                ("security_audit_report", sec_rep),
                ("integration_report", int_rep),
            ]
            if rep
        ]

        override = state.get("interactive_override")
        is_interactive = (
            override
            if override is not None
            else (sys.stdin.isatty() and not state.get("auto_mode_for_testing", False))
        )

        if is_interactive and not ctx_err:
            print("\n" + "=" * 60)
            print(f"HUMAN APPROVAL GATE — Task: {task_id}")
            print("=" * 60)
            print(f"Requirements Status   : {req_rep.get('status_str')} — {req_rep.get('summary')}")
            if pm_rep:
                print(f"Project Plan Status   : {pm_rep.get('status_str')} — {pm_rep.get('summary')}")
            print(f"Architect Status      : {arch_rep.get('status_str')} — {arch_rep.get('summary')}")
            print(f"QA / Security Status  : {qa_rep.get('status_str')} — {qa_rep.get('summary')}")
            if sec_rep:
                print(f"Security Audit Status : {sec_rep.get('status_str')} — {sec_rep.get('summary')}")
            if int_rep:
                print(f"Integration Status    : {int_rep.get('status_str')} — {int_rep.get('summary')}")
            print(f"Agent Recommendation  : {recommendation}")
            print("-" * 60)
            print(f"Valid accountable humans: {', '.join(sorted(VALID_ACCOUNTABLE_HUMANS))}")

            reviewer_name = ""
            while reviewer_name not in VALID_ACCOUNTABLE_HUMANS:
                candidate = input("Dein vollständiger Name für die Freigabe (Pflichtfeld): ").strip()
                if candidate in VALID_ACCOUNTABLE_HUMANS:
                    reviewer_name = candidate
                else:
                    print(
                        f"Ungültiger Reviewer '{candidate}'. Bitte einen Accountable Human aus roles.yaml eingeben: "
                        f"{', '.join(sorted(VALID_ACCOUNTABLE_HUMANS))}"
                    )

            print("\nEntscheidungsoptionen:")
            print(" [a] = Approved (Code & Anforderungen vollständig freigeben)")
            print(" [c] = Changes Requested (Nachbesserung fordern -> neuer Lauf nötig)")
            print(" [e] = Escalate (An Accountable Human / Projektleitung eskalieren)")

            choice = ""
            while choice not in ("a", "c", "e"):
                choice = input("Deine Entscheidung (a/c/e): ").strip().lower()

            decision_map: dict[str, Literal["approved", "changes_requested", "escalate_to_human_review"]] = {
                "a": "approved",
                "c": "changes_requested",
                "e": "escalate_to_human_review",
            }
            decision = decision_map[choice]

            if decision == "approved" and recommendation != "approved":
                confirm = input(
                    f"ACHTUNG: Agenten-Empfehlung ist '{recommendation}'. Wirklich als 'approved' (Accepted Risk) freigeben? (yes/no): "
                ).strip().lower()
                if confirm not in ("yes", "y", "ja", "j"):
                    decision = "changes_requested"

            note = input("Begründung / Notiz zur Entscheidung (Pflicht bei Abweichung): ").strip()
            if not note:
                note = f"Manuelle Entscheidung ({decision}) durch {reviewer_name}."

            human_duration = round(time.perf_counter() - gate_started, 4)
            record = HumanApprovalRecord(
                reviewed_by=reviewer_name,
                decision=decision,
                agent_recommendation=recommendation,
                task_id=task_id,
                reviewed_artifacts=reviewed_artifacts,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                human_review_seconds=human_duration,
                note=note,
            )
            return {"human_approval": record.model_dump()}

        # Headless mode: NEVER auto-approve under a human's name!
        if ctx_err:
            headless_decision: Literal[
                "approved",
                "changes_requested",
                "escalate_to_human_review",
                "pending_human_review",
            ] = "escalate_to_human_review"
            note = f"Context validation failed before LLM execution: {ctx_err}"
        elif recommendation == "escalate_to_human_review":
            headless_decision = "escalate_to_human_review"
            note = "Headless execution: unparseable or escalated agent output requires human intervention."
        else:
            headless_decision = "pending_human_review"
            note = (
                f"Headless execution: agent recommendation is '{recommendation}'. "
                "Explicit human approval is still required before closing or releasing."
            )

        record = HumanApprovalRecord(
            reviewed_by=None,
            decision=headless_decision,
            agent_recommendation=recommendation,
            task_id=task_id,
            reviewed_artifacts=reviewed_artifacts,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            human_review_seconds=0.0,
            note=note,
        )
        return {"human_approval": record.model_dump()}

    builder = StateGraph(PipelineState)
    builder.add_node("validate_context", step_validate_context)
    builder.add_node("requirements", step_requirements)
    builder.add_node("architect", step_architect)
    builder.add_node("backend_implementation", step_backend_implementation)
    builder.add_node("qa_security", step_qa_security)
    builder.add_node("human_gate", step_human_gate)

    builder.add_edge(START, "validate_context")
    builder.add_conditional_edges(
        "validate_context", route_after_context, ["requirements", "human_gate"]
    )
    builder.add_conditional_edges(
        "requirements", route_after_requirements, ["architect", "human_gate"]
    )
    builder.add_conditional_edges(
        "architect",
        route_after_architect,
        ["backend_implementation", "qa_security", "human_gate"],
    )
    builder.add_edge("backend_implementation", "qa_security")
    builder.add_conditional_edges(
        "qa_security", route_after_qa, ["backend_implementation", "human_gate"]
    )
    builder.add_edge("human_gate", END)

    return builder.compile()


def _aggregate_subagent_metrics(trace_path: str, workflow_id: str) -> dict[str, Any]:
    p = Path(trace_path)
    calls = 0
    agent_duration = 0.0
    total_cost = 0.0
    if p.is_file():
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("workflow_id") != workflow_id:
                continue
            if rec.get("record_type") == "workflow_summary" or rec.get("agent") == "feature_pipeline_workflow":
                continue
            calls += int(rec.get("calls", 0))
            agent_duration += float(rec.get("duration_seconds", 0.0))
            total_cost += float(rec.get("estimated_cost_credits", 0.0))
    return {
        "calls": calls,
        "agent_duration_seconds": round(agent_duration, 4),
        "total_cost_credits": round(total_cost, 4),
    }


def run_feature_pipeline(
    task: EngineeringTask | None = None,
    *,
    llm: Any | None = None,
    trace_file: str | None = None,
    interactive: bool | None = None,
    full_company_mode: bool = False,
    run_pytest_in_qa: bool = False,
    backend_agent_fn: Callable[[dict[str, Any], int], dict[str, Any]] | None = None,
    max_impl_retries: int = 3,
) -> dict[str, Any]:
    settings = get_settings()
    run_id = str(uuid.uuid4())
    workflow_id = str(uuid.uuid4())
    started = time.perf_counter()

    evidence_dir = REPO_ROOT / "evidence" / "session-02"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    custom_trace = trace_file or str(evidence_dir / f"{workflow_id}.jsonl")

    task = task or EngineeringTask(
        task_id="DRYRUN-002",
        description="Verify work item API implementation and schema persistence.",
        input_files=["src/app/main.py"],
    )

    graph = build_pipeline_graph(llm=llm, backend_agent_fn=backend_agent_fn)

    try:
        state = graph.invoke(
            {
                "task": task.model_dump(),
                "workflow_id": workflow_id,
                "trace_file": custom_trace,
                "interactive_override": interactive,
                "full_company_mode": full_company_mode,
                "run_pytest_in_qa": run_pytest_in_qa,
                "max_impl_retries": max_impl_retries,
            },
            {"recursion_limit": 30},
        )
    except Exception as exc:
        state = {"error": str(exc)}

    wall_duration = time.perf_counter() - started
    provider = settings.llm_provider if llm is None else "injected"
    model = settings.llm_model if llm is None else getattr(llm, "model", "mock")

    req = state.get("requirements_report") or {}
    pm = state.get("project_plan_report") or {}
    ae = state.get("agent_design_report") or {}
    arch = state.get("architecture_report") or {}
    impl = state.get("implementation_report") or {}
    qa = state.get("qa_security_report") or {}
    sec = state.get("security_audit_report") or {}
    integ = state.get("integration_report") or {}
    human = state.get("human_approval") or {}
    ctx_error = state.get("context_error")

    sub_reports = [r for r in (req, pm, ae, arch, qa, sec, integ) if r]
    has_unparseable = any(r.get("status_str") == "unparseable" for r in sub_reports)
    has_escalated = bool(ctx_error) or any(r.get("status_str") == "escalated" for r in sub_reports)

    if state.get("error"):
        overall_status = "error"
    elif has_escalated:
        overall_status = "escalated"
    elif has_unparseable:
        overall_status = "invalid_output"
    else:
        overall_status = "success"

    agg = _aggregate_subagent_metrics(custom_trace, workflow_id)
    human_review_sec = float(human.get("human_review_seconds", 0.0))
    agent_runtime_sec = agg["agent_duration_seconds"] or round(max(0.0, wall_duration - human_review_sec), 4)

    result_state: dict[str, Any] = {
        "requirements": req,
        "architecture": arch,
        "qa_security": qa,
        "human_approval": human,
        "context_error": ctx_error,
    }
    if pm:
        result_state["project_plan"] = pm
    if ae:
        result_state["agent_design"] = ae
    if impl:
        result_state["implementation"] = impl
        result_state["impl_attempts"] = state.get("impl_attempts", 1)
    if sec:
        result_state["security_audit"] = sec
    if integ:
        result_state["integration"] = integ

    trace_record = {
        "record_type": "workflow_summary",
        "run_id": run_id,
        "workflow_id": workflow_id,
        "parent_workflow_id": task.parent_workflow_id,
        "task_id": task.task_id,
        "agent": "feature_pipeline_workflow",
        "role": "integration_engineer",
        "provider": provider,
        "model": model,
        "status": overall_status,
        "tools": ["read_repository_text_file"],
        "calls": agg["calls"],
        "duration_seconds": agent_runtime_sec,
        "human_review_seconds": human_review_sec,
        "wall_clock_seconds": round(wall_duration, 4),
        "result_state": result_state,
        "estimated_cost_credits": agg["total_cost_credits"],
    }

    append_trace(trace_record, custom_trace)

    return trace_record


def record_human_decision(
    trace_file: str,
    *,
    reviewer_name: str,
    decision: Literal["approved", "changes_requested", "escalate_to_human_review"],
    note: str,
    review_seconds: float = 0.0,
) -> dict[str, Any]:
    """Explicitly record a human gate decision for a previously pending workflow trace."""
    if reviewer_name not in VALID_ACCOUNTABLE_HUMANS:
        raise ValueError(
            f"Reviewer '{reviewer_name}' is not an accountable human in organization/roles.yaml."
        )
    path = Path(trace_file)
    if not path.is_file():
        raise FileNotFoundError(f"Trace file not found: {trace_file}")

    lines = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    summary_rec = next(
        (r for r in reversed(lines) if r.get("agent") == "feature_pipeline_workflow"),
        None,
    )
    if not summary_rec:
        raise ValueError("No feature_pipeline_workflow record found in trace file.")

    prev_human = summary_rec.get("result_state", {}).get("human_approval", {})
    approval = HumanApprovalRecord(
        reviewed_by=reviewer_name,
        decision=decision,
        agent_recommendation=prev_human.get("agent_recommendation", "changes_requested"),
        task_id=summary_rec.get("task_id", "UNKNOWN"),
        reviewed_artifacts=prev_human.get(
            "reviewed_artifacts",
            ["requirements_report", "architecture_report", "qa_security_report"],
        ),
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        human_review_seconds=round(review_seconds, 4),
        note=note,
    ).model_dump()

    decision_event = {
        "record_type": "human_approval_event",
        "run_id": str(uuid.uuid4()),
        "workflow_id": summary_rec.get("workflow_id"),
        "task_id": summary_rec.get("task_id"),
        "agent": "human_gate",
        "role": "accountable_human",
        "actor_type": "human",
        "reviewed_by": reviewer_name,
        "decision": decision,
        "human_review_seconds": round(review_seconds, 4),
        "human_approval": approval,
        "estimated_cost_credits": 0.0,
    }
    append_trace(decision_event, str(path))
    return decision_event


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--desc", type=str, default="Review work-item feature implementation.")
    parser.add_argument("--task-id", type=str, default="DRYRUN-002")
    parser.add_argument("--parent-workflow-id", type=str, default=None)
    parser.add_argument("--feedback", type=str, default=None)
    parser.add_argument("--full-company", action="store_true")
    args = parser.parse_args()

    print("Running Independent Agent Modular Feature Pipeline...")
    result = run_feature_pipeline(
        EngineeringTask(
            task_id=args.task_id,
            description=args.desc,
            parent_workflow_id=args.parent_workflow_id,
            human_feedback=args.feedback,
        ),
        full_company_mode=args.full_company,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
