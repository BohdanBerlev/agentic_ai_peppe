"""
Shared utilities for PepeGroup agents:
- Safe repository and customer target-checkout file access (prevents path traversal)
- Controlled file writing inside authorized target directories
- Message text normalization across Ollama / OpenAI / Gemini responses
- Accountable human lookup from organization/roles.yaml
"""

from __future__ import annotations

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


def resolve_authorized_root(base_dir: str | Path | None = None) -> Path:
    """Resolve the authorized workspace root (Factory REPO_ROOT by default, or an explicit customer checkout)."""
    if base_dir is None or str(base_dir).strip() == "":
        return REPO_ROOT
    candidate = Path(base_dir)
    if not candidate.is_absolute():
        candidate = (REPO_ROOT / candidate).resolve()
    else:
        candidate = candidate.resolve()
    return candidate


def read_repository_text_file(relative_path: str, base_dir: str | Path | None = None) -> str:
    """Safely read a UTF-8 text file inside the authorized root directory."""
    if not relative_path or not relative_path.strip():
        raise FileNotFoundError("File not found: empty file path")
    root = resolve_authorized_root(base_dir)
    requested = (root / relative_path).resolve()
    try:
        requested.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            f"Security violation: Path escapes repository root: {relative_path}"
        ) from exc
    if not requested.is_file():
        raise FileNotFoundError(f"File not found: {relative_path}")
    return requested.read_text(encoding="utf-8")


def write_target_text_file(
    relative_path: str,
    content: str,
    target_dir: str | Path | None = None,
) -> Path:
    """Safely write a UTF-8 text file inside the authorized target directory (blocks path traversal)."""
    if not relative_path or not relative_path.strip():
        raise ValueError("Target file path must not be empty")
    root = resolve_authorized_root(target_dir)
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Authorized target directory does not exist: {root}")
    requested = (root / relative_path).resolve()
    try:
        requested.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            f"Security violation: Target file path escapes authorized target directory: {relative_path}"
        ) from exc
    if ".git" in requested.relative_to(root).parts:
        raise ValueError("Security violation: Modifying .git internals is forbidden")
    requested.parent.mkdir(parents=True, exist_ok=True)
    requested.write_text(content, encoding="utf-8")
    return requested


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
