"""Termin 6: Deterministischer Projekt-Trennungstest (ohne Netz, ohne echtes LLM)."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from src.agents.common import write_target_text_file
from src.projects import (
    assert_target_belongs_to_project,
    get_project,
)
from src.workflows.feature_pipeline import EngineeringTask, run_feature_pipeline
from tests.test_feature_pipeline import ApprovedMockLLM


def _snapshot(root: Path) -> dict[str, str]:
    """Map every file below root (excluding .git) to its sha256 hex digest."""
    files: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if ".git" in rel.parts:
            continue
        files[str(rel)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


@pytest.fixture
def two_checkouts(tmp_path: Path) -> tuple[Path, Path]:
    nw = tmp_path / "client-01-website"
    nw.mkdir(parents=True, exist_ok=True)
    (nw / "index.html").write_text(
        "<!DOCTYPE html><html lang='de'><body>Nordwerk</body></html>", encoding="utf-8"
    )
    (nw / "test_website.py").write_text(
        "import sys\nif __name__ == '__main__':\n    sys.exit(0)\n", encoding="utf-8"
    )

    hp = tmp_path / "client-02-quotation"
    (hp / "fixtures").mkdir(parents=True, exist_ok=True)
    repo_fixture = (
        Path(__file__).resolve().parent.parent
        / "client-02-quotation"
        / "fixtures"
        / "HansePack_Katalog.json"
    )
    if repo_fixture.is_file():
        katalog_content = repo_fixture.read_text(encoding="utf-8")
    else:
        katalog_content = '{"products": []}'
    (hp / "fixtures" / "HansePack_Katalog.json").write_text(katalog_content, encoding="utf-8")
    (hp / "test_quotation.py").write_text(
        "import sys\nif __name__ == '__main__':\n    sys.exit(0)\n", encoding="utf-8"
    )
    return nw, hp


def test_hansepack_run_does_not_touch_nordwerk(tmp_path, two_checkouts):
    nw, hp = two_checkouts
    before = _snapshot(nw)

    def fake_backend(state, attempt: int):
        write_target_text_file(
            "quotation.py",
            "def quote():\n    return 0\n",
            target_dir=state["task"]["target_dir"],
        )
        return {
            "status_str": "approved",
            "summary": f"Backend implementation attempt {attempt}",
            "modified_files": ["quotation.py"],
            "attempt": attempt,
        }

    task = EngineeringTask(
        task_id="T6-SEP",
        project_id="client-02",
        target_dir=str(hp),
        description="HansePack quotation",
        input_files=["fixtures/HansePack_Katalog.json"],
        test_targets=["test_quotation.py"],
    )
    res = run_feature_pipeline(
        task,
        llm=ApprovedMockLLM(),
        trace_file=str(tmp_path / "t.jsonl"),
        interactive=False,
        run_pytest_in_qa=True,
        full_company_mode=True,
        backend_agent_fn=fake_backend,
        session_folder="session-06",
    )

    assert _snapshot(nw) == before
    assert (hp / "quotation.py").exists()
    assert res["project_id"] == "client-02"


def test_client02_cannot_target_nordwerk_checkout(tmp_path, two_checkouts):
    nw, _hp = two_checkouts
    before = _snapshot(nw)

    task = EngineeringTask(
        task_id="T6-GUARD-02",
        project_id="client-02",
        target_dir=str(nw),
        description="HansePack must not touch Nordwerk",
        input_files=["index.html"],
    )
    with pytest.raises(ValueError, match="isolation"):
        run_feature_pipeline(
            task,
            llm=ApprovedMockLLM(),
            trace_file=str(tmp_path / "guard02.jsonl"),
            interactive=False,
        )
    assert _snapshot(nw) == before


def test_client01_cannot_target_hansepack_checkout(tmp_path, two_checkouts):
    _nw, hp = two_checkouts
    with pytest.raises(ValueError, match="isolation"):
        run_feature_pipeline(
            EngineeringTask(
                task_id="T6-GUARD-01",
                project_id="client-01",
                target_dir=str(hp),
                description="Nordwerk must not touch HansePack",
                input_files=["fixtures/HansePack_Katalog.json"],
            ),
            llm=ApprovedMockLLM(),
            trace_file=str(tmp_path / "guard01.jsonl"),
            interactive=False,
        )


def test_unknown_project_id_rejected():
    with pytest.raises(ValueError):
        assert_target_belongs_to_project("client-99", None)


def test_registry_defaults():
    assert get_project("client-02").default_test_targets == ("test_quotation.py",)
    assert get_project("client-01").checkout_dir == "client-01-website"
