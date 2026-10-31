"""
Backend Engineer Agent (Phase 3: TDD & Implementation)
Implements core business logic and FastAPI endpoints based on Work Packages (WPs) or specifications,
executing automated test-and-repair loops without Human-in-the-Loop.
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

from src.llm.factory import get_chat_model
from src.observability.tracing import (
    append_trace,
    estimate_cost_credits,
    usage_from_message,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


class BackendImplementationReport(BaseModel):
    status: Literal["success", "tests_failed", "error", "unparseable"]
    wp_id: str = "WP-UNKNOWN"
    target_files: list[str] = Field(default_factory=list)
    tests_passed: bool = False
    iterations_used: int = 1
    summary: str
    changes: list[str] = Field(default_factory=list)
    test_output: str = ""


class BackendState(TypedDict, total=False):
    wp_content: str
    wp_id: str
    target_file: str
    test_files: list[str]
    current_iteration: int
    max_iterations: int
    current_code: str
    test_passed: bool
    test_output: str
    result: dict[str, Any]
    error: str


def read_repository_text_file(relative_path: str, base_dir: str | Path | None = None) -> str:
    """Sicherer Dateizugriff innerhalb des Repositorys bzw. autorisierten Kunden-Checkouts mit Path-Traversal-Schutz."""
    root = REPO_ROOT if not base_dir else (Path(base_dir).resolve() if Path(base_dir).is_absolute() else (REPO_ROOT / base_dir).resolve())
    requested = (root / relative_path).resolve()
    try:
        requested.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Security Violation: Pfad '{relative_path}' verlässt das Repository-Verzeichnis!") from exc

    if not requested.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {relative_path}")

    return requested.read_text(encoding="utf-8")


def write_repository_text_file(relative_path: str, content: str, base_dir: str | Path | None = None) -> None:
    """Sicheres Schreiben von Quellcode innerhalb des Repositorys bzw. autorisierten Kunden-Checkouts mit Path-Traversal- und .git-Schutz."""
    from src.agents.common import write_target_text_file
    try:
        write_target_text_file(relative_path, content, target_dir=base_dir)
    except ValueError as exc:
        raise ValueError(f"Security Violation: {exc}") from exc


def run_pytest(test_files: list[str]) -> tuple[bool, str]:
    """Führt automatisierte Tests via pytest aus (TDD Loop)."""
    if not test_files:
        return True, "No test files specified."

    cmd = [sys.executable, "-m", "pytest"] + test_files

    try:
        result = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = (result.stdout + "\n" + result.stderr).strip()
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "Pytest execution timed out after 60 seconds."
    except Exception as exc:
        return False, f"Execution error running pytest: {str(exc)}"


def _message_text(message: Any) -> str:
    """Konvertiert String- oder Listen-Outputs in reinen Text."""
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


def _parse_result(text: str, wp_id: str, tests_passed: bool, iterations: int, test_output: str) -> BackendImplementationReport:
    """Parst die Antwort des LLM und sichert deterministische Metriken ab."""
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
        parsed_json["wp_id"] = wp_id
        parsed_json["tests_passed"] = tests_passed
        parsed_json["iterations_used"] = iterations
        parsed_json["test_output"] = test_output[-2000:] if test_output else ""
        if not tests_passed and parsed_json.get("status") == "success":
            parsed_json["status"] = "tests_failed"
        return BackendImplementationReport.model_validate(parsed_json)
    except Exception as exc:
        return BackendImplementationReport(
            status="unparseable",
            wp_id=wp_id,
            target_files=[],
            tests_passed=tests_passed,
            iterations_used=iterations,
            summary=f"Could not parse LLM output: {exc}",
            changes=[],
            test_output=test_output[-2000:] if test_output else "",
        )


def build_backend_graph(llm: Any | None = None):
    """Baut den autonomen LangGraph für den Backend Agent (ohne Human-in-the-Loop)."""
    llm = llm or get_chat_model()

    def load_context(state: BackendState) -> BackendState:
        try:
            target_file = state.get("target_file", "src/app/main.py")
            current_code = ""
            target_path = (REPO_ROOT / target_file).resolve()
            if target_path.exists() and target_path.is_file():
                current_code = read_repository_text_file(target_file)

            return {
                "current_code": current_code,
                "current_iteration": 0,
                "max_iterations": state.get("max_iterations", 3),
            }
        except Exception as exc:
            return {"error": str(exc)}

    def route_after_load(state: BackendState):
        return END if state.get("error") else "implement"

    def implement(state: BackendState) -> BackendState:
        iteration = state.get("current_iteration", 0) + 1
        system = SystemMessage(
            content=(
                "You are the Backend / API Engineer for an enterprise AI development pipeline (Phase 3). "
                "Your role is to implement core business logic and FastAPI endpoints according to the Work Package, "
                "architecture specifications, and tests without Human-in-the-Loop.\n"
                "Return ONLY a valid JSON object matching this schema:\n"
                "{\n"
                '  "status": "success",\n'
                '  "target_files": ["src/app/main.py"],\n'
                '  "summary": "Implemented requested endpoints and logic",\n'
                '  "changes": ["Added endpoint X", "Updated model Y"],\n'
                '  "code": "FULL_SOURCE_CODE_OF_TARGET_FILE"\n'
                "}\n"
                "Do not include markdown code block wrappers around the JSON if possible."
            )
        )

        test_feedback = ""
        if state.get("test_output") and not state.get("test_passed"):
            test_feedback = f"\n\nPREVIOUS TEST FAILURE (Iteration {iteration - 1}):\n{state['test_output']}\nPlease fix the errors identified in the test output."

        human = HumanMessage(
            content=(
                f"Work Package Specification:\n{state.get('wp_content', '')}\n\n"
                f"Target File: {state.get('target_file', 'src/app/main.py')}\n\n"
                f"Current Code:\n{state.get('current_code', '')}"
                f"{test_feedback}"
            )
        )

        try:
            response = llm.invoke([system, human])
            text = _message_text(response)
            usage = usage_from_message(response)

            cleaned = text.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.strip("`")
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:].lstrip()

            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start >= 0 and end > start:
                cleaned = cleaned[start : end + 1]

            parsed = json.loads(cleaned)
            new_code = parsed.get("code")
            target_file = state.get("target_file", "src/app/main.py")

            if new_code:
                write_repository_text_file(target_file, new_code)
                code_to_keep = new_code
            else:
                code_to_keep = state.get("current_code", "")

            return {
                "current_code": code_to_keep,
                "current_iteration": iteration,
                "result": {
                    "summary": parsed.get("summary", "Code updated"),
                    "changes": parsed.get("changes", []),
                    "target_files": parsed.get("target_files", [target_file]),
                    "_usage": usage,
                    "_raw_text": text,
                },
            }
        except Exception as exc:
            return {"error": f"LLM / Implementation Exception: {str(exc)}", "current_iteration": iteration}

    def run_tests(state: BackendState) -> BackendState:
        test_files = state.get("test_files", [])
        if not test_files:
            return {"test_passed": True, "test_output": "No tests provided."}

        passed, output = run_pytest(test_files)
        return {
            "test_passed": passed,
            "test_output": output,
        }

    def route_after_tests(state: BackendState):
        if state.get("error"):
            return END
        if state.get("test_passed", False):
            return "finalize"

        iteration = state.get("current_iteration", 0)
        max_iter = state.get("max_iterations", 3)
        if iteration >= max_iter:
            return "finalize"

        # Automated repair loop
        return "implement"

    def finalize(state: BackendState) -> BackendState:
        wp_id = state.get("wp_id", "WP-UNKNOWN")
        passed = state.get("test_passed", False)
        iterations = state.get("current_iteration", 1)
        test_output = state.get("test_output", "")

        raw_result = state.get("result", {})
        raw_text = raw_result.get("_raw_text", json.dumps({
            "status": "success" if passed else "tests_failed",
            "summary": raw_result.get("summary", "Completed implementation cycle."),
            "changes": raw_result.get("changes", []),
        }))

        report = _parse_result(raw_text, wp_id, passed, iterations, test_output)
        report_dict = report.model_dump()
        report_dict["_usage"] = raw_result.get("_usage", (None, None))
        return {"result": report_dict}

    builder = StateGraph(BackendState)
    builder.add_node("load_context", load_context)
    builder.add_node("implement", implement)
    builder.add_node("run_tests", run_tests)
    builder.add_node("finalize", finalize)

    builder.add_edge(START, "load_context")
    builder.add_conditional_edges("load_context", route_after_load, ["implement", END])
    builder.add_edge("implement", "run_tests")
    builder.add_conditional_edges("run_tests", route_after_tests, ["implement", "finalize", END])
    builder.add_edge("finalize", END)

    return builder.compile()


def run_backend_agent(
    wp_content: str,
    *,
    wp_id: str = "WP-101",
    target_file: str = "src/app/main.py",
    test_files: list[str] | None = None,
    max_iterations: int = 3,
    task_id: str = "BACKEND-IMPL-001",
    workflow_id: str | None = None,
    trace_file: str | None = None,
) -> BackendImplementationReport:
    """Führt den autonomen Backend-Agenten aus und zeichnet Observability Traces auf."""
    run_id = str(uuid.uuid4())
    actual_workflow_id = workflow_id or run_id
    started = time.perf_counter()
    graph = build_backend_graph()

    test_file_list = test_files or []

    state = graph.invoke({
        "wp_content": wp_content,
        "wp_id": wp_id,
        "target_file": target_file,
        "test_files": test_file_list,
        "max_iterations": max_iterations,
    })
    duration = time.perf_counter() - started

    provider = "unknown"
    model = "unknown"
    try:
        from src.app.settings import get_settings
        settings = get_settings()
        provider = settings.llm_provider
        model = settings.llm_model
    except Exception:
        pass

    if state.get("error"):
        append_trace(
            {
                "run_id": run_id,
                "workflow_id": actual_workflow_id,
                "task_id": task_id,
                "agent": "backend_agent",
                "role": "backend_engineer",
                "provider": provider,
                "model": model,
                "status": "error",
                "tools": ["read_repository_text_file", "write_repository_text_file", "run_pytest"],
                "calls": state.get("current_iteration", 1),
                "duration_seconds": round(duration, 4),
                "error": state["error"],
                "estimated_cost_credits": estimate_cost_credits(
                    duration_seconds=duration,
                    input_tokens=0,
                    output_tokens=0,
                    calls=state.get("current_iteration", 1),
                ),
            },
            trace_file,
        )
        raise RuntimeError(state["error"])

    raw = dict(state.get("result", {}))
    input_tokens, output_tokens = raw.pop("_usage", (None, None))
    result = BackendImplementationReport.model_validate(raw)

    append_trace(
        {
            "run_id": run_id,
            "workflow_id": actual_workflow_id,
            "task_id": task_id,
            "agent": "backend_agent",
            "role": "backend_engineer",
            "provider": provider,
            "model": model,
            "status": "success" if result.tests_passed else "tests_failed",
            "result_status": result.status,
            "tools": ["read_repository_text_file", "write_repository_text_file", "run_pytest"],
            "calls": result.iterations_used,
            "duration_seconds": round(duration, 4),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_credits": estimate_cost_credits(
                duration_seconds=duration,
                input_tokens=input_tokens or 0,
                output_tokens=output_tokens or 0,
                calls=result.iterations_used,
            ),
        },
        trace_file,
    )
    return result


def my_backend_agent(state: dict[str, Any], attempt: int = 1) -> dict[str, Any]:
    """
    Contract-Funktion für die Multi-Agenten-Pipeline (src/workflows/feature_pipeline.py).
    
    1. Input:
       - state['task']['description']: Feature-Aufgabe
       - state['task']['input_files']: Zieldateien (default: ["src/app/main.py"])
       - state['requirements_report']: Akzeptanzkriterien vom PO
       - state['project_plan_report']: WPs vom PM
       - state['architecture_report']: Vorgaben / Interfaces vom SA
       - state['qa_security_report']: Feedback / Fehler bei attempt > 1
    
    2. Output:
       {
           "status_str": "approved", # oder "changes_requested"
           "summary": "...",
           "modified_files": ["src/app/main.py"],
           "attempt": attempt
       }
    """
    task = state.get("task", {})
    task_id = task.get("task_id", "BACKEND-IMPL-001")
    task_desc = task.get("description", "Implement requested backend feature.")
    input_files = task.get("input_files") or ["src/app/main.py"]
    target_file = input_files[0]
    target_dir = task.get("target_dir")
    wf_id = state.get("workflow_id") or str(uuid.uuid4())
    trace_file = state.get("trace_file")
    started = time.perf_counter()
    run_id = str(uuid.uuid4())

    # Context aus den Upstream-Rollen zusammenstellen
    req_rep = state.get("requirements_report", {})
    plan_rep = state.get("project_plan_report", {})
    arch_rep = state.get("architecture_report", {})
    qa_rep = state.get("qa_security_report", {})

    if target_dir:
        try:
            issue_doc = read_repository_text_file("issue_t3.md", base_dir=target_dir)
            task_desc = f"{task_desc}\n\nCustomer Issue Specification (issue_t3.md):\n{issue_doc}"
        except Exception:
            pass

    feedback_parts = [
        f"Feature Description:\n{task_desc}",
        f"\nRequirements (PO):\n{json.dumps(req_rep, indent=2)}",
        f"\nProject Plan (PM):\n{json.dumps(plan_rep, indent=2)}",
        f"\nArchitecture Spec (SA):\n{json.dumps(arch_rep, indent=2)}",
    ]

    # Falls attempt > 1, Feedback von QA / pytest einbinden
    if attempt > 1 and qa_rep:
        feedback_parts.append(f"\nPREVIOUS QA / TEST FEEDBACK (Attempt {attempt - 1}):\n{json.dumps(qa_rep, indent=2)}")

    full_spec = "\n\n".join(feedback_parts)
    tools_used = ["read_repository_text_file"]

    try:
        current_code = (
            read_repository_text_file(target_file, base_dir=target_dir)
            if target_dir
            else read_repository_text_file(target_file)
        )
    except Exception:
        current_code = ""

    # LLM instanziieren (nutzt injiziertes Test-LLM falls vorhanden)
    llm = state.get("_injected_llm") or get_chat_model()

    system = SystemMessage(
        content=(
            "You are the Implementation / Backend Engineer. Implement or update the source code (Python, HTML5, or CSS3) "
            "for the target file based on the specifications provided by PO, PM, Architect, and QA.\n"
            "Preserve all mandatory customer texts verbatim when editing HTML/CSS.\n"
            "Return ONLY a valid JSON object matching this schema:\n"
            "{\n"
            '  "status_str": "approved",\n'
            '  "summary": "Summary of what was changed",\n'
            '  "code": "FULL_SOURCE_CODE_OF_TARGET_FILE"\n'
            "}\n"
            "If you cannot implement the request or if there is a fatal blocker, set 'status_str' to 'changes_requested'.\n"
            "Do not include any text outside the JSON object."
        )
    )

    human = HumanMessage(
        content=(
            f"Target File: {target_file}\n"
            f"Attempt: {attempt}\n\n"
            f"Specifications & Context:\n{full_spec}\n\n"
            f"Current Code of {target_file}:\n{current_code}"
        )
    )

    try:
        response = llm.invoke([system, human])
        in_tok, out_tok = usage_from_message(response)
        text = _message_text(response).strip()

        if text.startswith("```"):
            text = text.strip("`")
            if text.startswith("json"):
                text = text[4:].lstrip()

        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            text = text[start : end + 1]

        parsed = json.loads(text)
        new_code = parsed.get("code")
        if new_code:
            tools_used.append("write_repository_text_file")
            if target_dir:
                write_repository_text_file(target_file, new_code, base_dir=target_dir)
            else:
                write_repository_text_file(target_file, new_code)

        status_str = parsed.get("status_str", "approved")
        if status_str not in ("approved", "changes_requested"):
            status_str = "approved"

        summary = parsed.get("summary", f"Backend implemented changes for {target_file} (attempt {attempt}).")
        duration = time.perf_counter() - started

        if trace_file:
            from src.app.settings import get_settings
            settings = get_settings()
            append_trace(
                {
                    "run_id": run_id,
                    "workflow_id": wf_id,
                    "task_id": task_id,
                    "agent": "backend_agent",
                    "role": "backend_api_engineer",
                    "provider": settings.llm_provider if not state.get("_injected_llm") else "injected",
                    "model": settings.llm_model if not state.get("_injected_llm") else getattr(llm, "model", "mock"),
                    "status": "success",
                    "result_status": status_str,
                    "tools": tools_used,
                    "calls": 1,
                    "duration_seconds": round(duration, 4),
                    "input_tokens": in_tok,
                    "output_tokens": out_tok,
                    "estimated_cost_credits": estimate_cost_credits(
                        duration_seconds=duration,
                        input_tokens=in_tok or 0,
                        output_tokens=out_tok or 0,
                        calls=1,
                    ),
                },
                trace_file,
            )

        return {
            "status_str": status_str,
            "summary": summary,
            "modified_files": [target_file],
            "attempt": attempt,
        }
    except Exception as exc:
        return {
            "status_str": "changes_requested",
            "summary": f"Backend agent error on attempt {attempt}: {exc}",
            "modified_files": [target_file],
            "attempt": attempt,
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Backend Engineer Agent (Phase 3)")
    parser.add_argument("--wp", type=str, default="Implement health and metrics endpoint in FastAPI", help="Work package description")
    parser.add_argument("--wp-id", type=str, default="WP-101", help="Work Package ID")
    parser.add_argument("--target", type=str, default="src/app/main.py", help="Target source file")
    parser.add_argument("--test", type=str, action="append", default=[], help="Pytest file to verify implementation")
    args = parser.parse_args()

    print(f"Running Backend Agent for {args.wp_id}...")
    try:
        report = run_backend_agent(
            wp_content=args.wp,
            wp_id=args.wp_id,
            target_file=args.target,
            test_files=args.test,
        )
        print(report.model_dump_json(indent=2))
    except Exception as exc:
        print(f"Backend Agent failed: {exc}", file=sys.stderr)
        sys.exit(1)
