"""Course-supplied infrastructure tests; excluded from team achievement."""

import json
import os

import psycopg
import pytest
from langchain_core.messages import AIMessage

from examples.file_review_agent import run_review
from src.app.settings import Settings, get_settings
from src.llm.factory import get_chat_model
from src.observability.tracing import append_trace, estimate_cost_credits


class FailingLLM:
    def invoke(self, messages):
        raise TimeoutError("simulated secret=do-not-log")


class InvalidLLM:
    def invoke(self, messages):
        return AIMessage(content="invalid output")


def test_provider_failure_is_traced_and_reraised(tmp_path):
    trace_file = tmp_path / "failure.jsonl"
    with pytest.raises(TimeoutError):
        run_review("src/app/main.py", llm=FailingLLM(), trace_file=str(trace_file))
    record = json.loads(trace_file.read_text())
    assert record["status"] == "error"
    assert record["model"] == "FailingLLM"
    assert record["calls"] == 1
    assert record["error_type"] == "TimeoutError"
    assert "do-not-log" not in trace_file.read_text()
    assert record["tools"] == ["read_repository_text_file"]
    assert record["input_tokens"] is None


def test_invalid_result_is_not_logged_as_success(tmp_path):
    path = tmp_path / "invalid.jsonl"
    result = run_review("src/app/main.py", llm=InvalidLLM(), trace_file=str(path))
    assert result.status == "unparseable"
    record = json.loads(path.read_text())
    assert record["status"] == "invalid_output"
    assert record["result_status"] == "unparseable"


def test_missing_file_has_no_llm_call_cost(tmp_path):
    path = tmp_path / "missing.jsonl"
    with pytest.raises(RuntimeError):
        run_review("does-not-exist.py", llm=FailingLLM(), trace_file=str(path))
    record = json.loads(path.read_text())
    assert record["calls"] == 0
    assert record["estimated_cost_credits"] < 1


def test_interruption_is_traced(tmp_path):
    class InterruptedLLM:
        def invoke(self, messages):
            raise KeyboardInterrupt()

    path = tmp_path / "interrupted.jsonl"
    with pytest.raises(KeyboardInterrupt):
        run_review("src/app/main.py", llm=InterruptedLLM(), trace_file=str(path))
    assert json.loads(path.read_text())["status"] == "interrupted"


def test_trace_files_are_separate_and_legacy_append_still_works(tmp_path):
    template = str(tmp_path / "RUN_ID.jsonl")
    first = append_trace({"run_id": "run-a"}, template)
    second = append_trace({"run_id": "run-b"}, template)
    assert first != second
    assert first.exists() and second.exists()
    legacy = str(tmp_path / "legacy.jsonl")
    append_trace({"run_id": "run-a"}, legacy)
    append_trace({"run_id": "run-b"}, legacy)
    assert len((tmp_path / "legacy.jsonl").read_text().splitlines()) == 2


def test_ollama_has_timeout_and_output_limit():
    model = get_chat_model(Settings(_env_file=None, llm_timeout_seconds=7, llm_max_output_tokens=42))
    assert model.client_kwargs["timeout"] == 7
    assert model.num_predict == 42


def test_cost_counts_all_calls():
    settings = Settings(_env_file=None)
    credits = estimate_cost_credits(
        duration_seconds=10, input_tokens=1000, output_tokens=500,
        calls=3, settings=settings,
    )
    assert credits == pytest.approx(3.14)


@pytest.mark.skipif(os.environ.get("STARTER_DATABASE_TEST") != "1", reason="Set STARTER_DATABASE_TEST=1 with PostgreSQL running")
def test_database_baseline_supports_committed_persistence():
    """Exercise the DB without implementing the teams' Work-Item feature."""
    import uuid

    table = "starter_probe_" + uuid.uuid4().hex
    url = get_settings().database_url
    identifier = psycopg.sql.Identifier(table)
    with psycopg.connect(url, autocommit=True) as conn:
        try:
            assert conn.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'").fetchone()
            conn.execute(psycopg.sql.SQL("CREATE TABLE {} (value text NOT NULL)").format(identifier))
            conn.execute(psycopg.sql.SQL("INSERT INTO {} VALUES (%s)").format(identifier), ("persisted",))
            with psycopg.connect(url) as other:
                row = other.execute(psycopg.sql.SQL("SELECT value FROM {}").format(identifier)).fetchone()
                assert row == ("persisted",)
        finally:
            conn.execute(psycopg.sql.SQL("DROP TABLE IF EXISTS {}").format(identifier))
