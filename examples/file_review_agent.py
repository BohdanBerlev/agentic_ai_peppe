"""COURSE-SUPPLIED REFERENCE EXAMPLE – NOT ASSESSMENT EVIDENCE.

A minimal LangGraph workflow that:
1. uses a deterministic file-reading tool,
2. sends the result to the configured LLM,
3. returns a structured Pydantic result,
4. writes a local JSONL execution trace.

It deliberately does not rely on model-native tool calling. This keeps the
baseline compatible with smaller local models and simple OpenAI-compatible
serving endpoints. Teams can implement autonomous tool selection later.
"""

from __future__ import annotations

import argparse
import json
import time
import uuid
from pathlib import Path
from typing import Any, Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field, ValidationError

from src.app.settings import get_settings
from src.llm.factory import get_chat_model
from src.observability.tracing import (
    append_trace,
    estimate_cost_credits,
    usage_from_message,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


class Finding(BaseModel):
    severity: Literal["low", "medium", "high"]
    description: str


class ReviewResult(BaseModel):
    status: Literal["approved", "changes_requested", "unparseable"]
    summary: str
    findings: list[Finding] = Field(default_factory=list)


class ReviewState(TypedDict, total=False):
    input_path: str
    file_content: str
    result: dict[str, Any]
    error: str


def read_repository_text_file(relative_path: str) -> str:
    """Read a UTF-8 file while preventing access outside the repository."""
    requested = (REPO_ROOT / relative_path).resolve()
    try:
        requested.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise ValueError("Path escapes repository root") from exc

    if not requested.is_file():
        raise FileNotFoundError(relative_path)
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


def _parse_result(text: str) -> ReviewResult:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].lstrip()

    # Be tolerant of a short explanation around the JSON object.
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        cleaned = cleaned[start : end + 1]

    try:
        return ReviewResult.model_validate(json.loads(cleaned))
    except (json.JSONDecodeError, ValidationError):
        return ReviewResult(
            status="unparseable",
            summary=text[:1000],
            findings=[],
        )


def build_graph(llm: Any | None = None, *, trace_context: dict[str, Any] | None = None):
    llm = llm if llm is not None else get_chat_model()
    trace_context = trace_context if trace_context is not None else {"tools": [], "calls": 0}

    def load_file(state: ReviewState) -> ReviewState:
        trace_context["tools"].append("read_repository_text_file")
        try:
            return {
                "file_content": read_repository_text_file(state["input_path"])
            }
        except Exception as exc:
            return {"error": f"{type(exc).__name__}: {exc}"}

    def route_after_load(state: ReviewState):
        return END if state.get("error") else "review"

    def review(state: ReviewState) -> ReviewState:
        system = SystemMessage(
            content=(
                "You are a careful software QA reviewer. Return ONLY valid JSON "
                "with keys status, summary, findings. status must be approved or "
                "changes_requested. findings must be a list of objects containing "
                "severity (low|medium|high) and description."
            )
        )
        human = HumanMessage(
            content=(
                f"Review file {state['input_path']} for obvious correctness, "
                "maintainability and security problems.\n\n"
                f"FILE CONTENT:\n{state['file_content']}"
            )
        )
        trace_context["calls"] += 1
        response = llm.invoke([system, human])
        trace_context["input_tokens"], trace_context["output_tokens"] = usage_from_message(response)
        result = _parse_result(_message_text(response))
        result_dict = result.model_dump()
        result_dict["_usage"] = usage_from_message(response)
        return {"result": result_dict}

    builder = StateGraph(ReviewState)
    builder.add_node("load_file", load_file)
    builder.add_node("review", review)
    builder.add_edge(START, "load_file")
    builder.add_conditional_edges("load_file", route_after_load, ["review", END])
    builder.add_edge("review", END)
    return builder.compile()


def run_review(
    input_path: str,
    *,
    task_id: str = "STARTER-DEMO",
    llm: Any | None = None,
    trace_file: str | None = None,
) -> ReviewResult:
    settings = get_settings()
    run_id = str(uuid.uuid4())
    started = time.perf_counter()
    context: dict[str, Any] = {
        "tools": [], "calls": 0, "input_tokens": None, "output_tokens": None,
    }
    record: dict[str, Any] = {
        "run_id": run_id,
        "workflow_id": run_id,
        "task_id": task_id,
        "agent": "starter-file-review-agent",
        "role": "reference_file_reviewer",
        "provider": settings.llm_provider if llm is None else "injected",
        "model": settings.llm_model if llm is None else (
            getattr(llm, "model", None) or getattr(llm, "model_name", None)
            or type(llm).__name__
        ),
        "status": "error",
    }
    try:
        graph = build_graph(llm, trace_context=context)
        state = graph.invoke({"input_path": input_path}, {"recursion_limit": 10})
        if state.get("error"):
            raise RuntimeError(state["error"])
        raw = dict(state["result"])
        raw.pop("_usage", None)
        result = ReviewResult.model_validate(raw)
        record["result_status"] = result.status
        record["status"] = "invalid_output" if result.status == "unparseable" else "success"
        return result
    except (Exception, KeyboardInterrupt) as exc:
        record["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "error"
        # Do not persist provider exception text: it may contain credentials/URLs.
        record["error_type"] = type(exc).__name__
        raise
    finally:
        duration = time.perf_counter() - started
        append_trace(
            {
                **record,
                **context,
                "duration_seconds": round(duration, 4),
                "estimated_cost_credits": estimate_cost_credits(
                    duration_seconds=duration,
                    input_tokens=context["input_tokens"],
                    output_tokens=context["output_tokens"],
                    calls=context["calls"],
                ),
                "token_usage_complete": context["input_tokens"] is not None
                and context["output_tokens"] is not None,
            },
            trace_file,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Repository-relative file path")
    parser.add_argument("--task-id", default="STARTER-DEMO")
    args = parser.parse_args()

    result = run_review(args.input, task_id=args.task_id)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
