from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.app.settings import Settings, get_settings


def estimate_cost_credits(
    *,
    duration_seconds: float,
    input_tokens: int | None,
    output_tokens: int | None,
    settings: Settings | None = None,
    calls: int = 1,
) -> float:
    """Calculate abstract course credits, not monetary cost."""
    settings = settings or get_settings()
    if calls < 0 or duration_seconds < 0:
        raise ValueError("Calls and duration must be non-negative")
    total = calls * settings.cost_call_base_credits
    total += duration_seconds * settings.cost_runtime_credits_per_second
    if input_tokens is not None:
        total += (input_tokens / 1000) * settings.cost_input_credits_per_1k_tokens
    if output_tokens is not None:
        total += (output_tokens / 1000) * settings.cost_output_credits_per_1k_tokens
    return round(total, 4)


def append_trace(record: dict[str, Any], trace_file: str | None = None) -> Path:
    settings = get_settings()
    # A unique file per run avoids Git merge conflicts between developers.
    # Explicit legacy paths remain supported for existing team implementations.
    run_id = str(record.get("run_id") or uuid.uuid4())
    if not run_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in run_id):
        raise ValueError("run_id must contain only letters, digits, '-' or '_'")
    path = Path((trace_file or settings.trace_file).replace("{run_id}", run_id).replace("RUN_ID", run_id))
    path.parent.mkdir(parents=True, exist_ok=True)

    enriched = {
        "logged_at": datetime.now(timezone.utc).isoformat(),
        **record,
        "run_id": run_id,
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(enriched, ensure_ascii=False) + "\n")
    return path


def usage_from_message(message: Any) -> tuple[int | None, int | None]:
    """Extract token counts when the provider returns LangChain usage metadata."""
    usage = getattr(message, "usage_metadata", None) or {}
    if not isinstance(usage, dict):
        return None, None

    input_tokens = usage.get("input_tokens")
    output_tokens = usage.get("output_tokens")
    return input_tokens, output_tokens
