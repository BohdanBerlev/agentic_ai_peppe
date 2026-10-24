"""
Shared utilities for PepeGroup agents:
- Safe repository and target directory file access (prevents path traversal)
- Message text normalization across Ollama / OpenAI / Gemini responses
- Accountable human lookup from organization/roles.yaml
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypeVar
from pydantic import BaseModel

REPO_ROOT = Path(__file__).resolve().parents[2]

T = TypeVar("T", bound=BaseModel)

VALID_ACCOUNTABLE_HUMANS = {
    "Mehrose Farooq",
    "Lars Boos",
    "Maxim Bers",
    "David Pisarkiewicz",
}


def read_repository_text_file(relative_path: str, base_dir: Path | None = None) -> str:
    """Safely read a UTF-8 text file inside the allowed base directory (default: REPO_ROOT)."""
    if not relative_path or not relative_path.strip():
        raise FileNotFoundError("File not found: empty file path")
    root = (base_dir or REPO_ROOT).resolve()
    requested = (root / relative_path).resolve()
    try:
        requested.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            f"Security violation: Path escapes allowed root: {relative_path}"
        ) from exc
    if not requested.is_file():
        raise FileNotFoundError(f"File not found: {relative_path}")
    return requested.read_text(encoding="utf-8")


def write_target_text_file(relative_path: str, content: str, target_dir: Path | None = None) -> Path:
    """Safely write a UTF-8 text file inside the authorized target directory (prevents path traversal)."""
    if not relative_path or not relative_path.strip():
        raise ValueError("File path cannot be empty.")
    root = (target_dir or (REPO_ROOT / "client-01-website")).resolve()
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            f"Security violation: Target file path escapes authorized target directory: {relative_path}"
        ) from exc
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(content, encoding="utf-8")
    return resolved


def extract_message_text(message: Any) -> str:
    """Convert string or content-block list outputs into plain text."""
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


def clean_json_block(text: str) -> str:
    """Extract the outermost JSON object from an LLM text response."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].lstrip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        cleaned = cleaned[start : end + 1]
    return cleaned
