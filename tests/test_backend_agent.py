import json
import pytest
from pathlib import Path
from src.agents.backend_agent import (
    REPO_ROOT,
    read_repository_text_file,
    write_repository_text_file,
    _parse_result,
    BackendImplementationReport,
    run_pytest,
)

def test_read_repository_text_file_not_found():
    """Prüft, ob das Lesen einer nicht existierenden Datei korrekt abgefangen wird."""
    with pytest.raises(FileNotFoundError):
        read_repository_text_file("src/app/non_existent_file_xyz.py")

def test_read_repository_text_file_path_traversal():
    """Prüft, ob Path Traversal beim Lesen blockiert wird."""
    with pytest.raises(ValueError, match="Security Violation"):
        read_repository_text_file("../../etc/passwd")

def test_write_repository_text_file_path_traversal():
    """Prüft, ob Path Traversal beim Schreiben blockiert wird."""
    with pytest.raises(ValueError, match="Security Violation"):
        write_repository_text_file("../../tmp/malicious.py", "malicious_code = True")


def test_write_repository_text_file_git_protection():
    """Sicherheitstest: Schreibversuche in .git internals werden strikt blockiert."""
    with pytest.raises(ValueError, match="Security Violation"):
        write_repository_text_file(".git/config", "[malicious]\\nkey=val")

def test_write_repository_text_file_target_dir_git_protection(tmp_path):
    """Sicherheitstest: Schreibversuche in .git eines Kunden-Zielverzeichnisses werden blockiert."""
    with pytest.raises(ValueError, match="Security Violation"):
        write_repository_text_file(".git/hooks/pre-commit", "#!/bin/sh\\nevil", base_dir=tmp_path)
def test_run_pytest_empty_list():
    """Prüft, dass leere Testlisten als bestanden gewertet werden."""
    passed, output = run_pytest([])
    assert passed is True
    assert "No test files" in output

def test_run_pytest_success():
    """Prüft die Ausführung eines existierenden Tests."""
    passed, output = run_pytest(["tests/test_cost_agent.py"])
    assert passed is True
    assert "passed" in output

def test_parse_result_valid_json():
    """Prüft, ob valides JSON vom LLM korrekt in BackendImplementationReport überführt wird."""
    mock_llm_output = json.dumps({
        "status": "success",
        "target_files": ["src/app/main.py"],
        "summary": "Endpoints added successfully",
        "changes": ["Added POST /items", "Validated payload"],
    })

    report = _parse_result(
        text=mock_llm_output,
        wp_id="WP-102",
        tests_passed=True,
        iterations=1,
        test_output="All 5 tests passed",
    )

    assert isinstance(report, BackendImplementationReport)
    assert report.status == "success"
    assert report.wp_id == "WP-102"
    assert report.tests_passed is True
    assert report.iterations_used == 1
    assert "Added POST /items" in report.changes
    assert report.test_output == "All 5 tests passed"

def test_parse_result_test_failed_override():
    """Prüft, dass bei nicht bestandenen Tests der Status 'tests_failed' erzwungen wird."""
    mock_llm_output = json.dumps({
        "status": "success",
        "target_files": ["src/app/main.py"],
        "summary": "Endpoints added",
        "changes": [],
    })

    report = _parse_result(
        text=mock_llm_output,
        wp_id="WP-102",
        tests_passed=False,
        iterations=3,
        test_output="FAILED test_something",
    )

    assert report.status == "tests_failed"
    assert report.tests_passed is False
    assert report.iterations_used == 3

def test_parse_result_invalid_json():
    """Prüft, ob der Parser bei kaputtem LLM-Output einen unparseable-Status zurückgibt."""
    bad_output = "Hier ist der Code, aber kein JSON!"

    report = _parse_result(
        text=bad_output,
        wp_id="WP-999",
        tests_passed=False,
        iterations=1,
        test_output="Error",
    )

    assert report.status == "unparseable"
    assert report.wp_id == "WP-999"
    assert report.tests_passed is False


def test_my_backend_agent_contract_success(monkeypatch):
    """Prüft, ob my_backend_agent den Pipeline-Vertrag (Contract) exakt erfüllt."""
    from unittest.mock import MagicMock
    from langchain_core.messages import AIMessage
    from src.agents.backend_agent import my_backend_agent

    mock_llm = MagicMock()
    mock_llm.invoke.return_value = AIMessage(
        content=json.dumps({
            "status_str": "approved",
            "summary": "Implemented requested endpoint",
            "code": "# mock updated code",
        })
    )
    monkeypatch.setattr("src.agents.backend_agent.get_chat_model", lambda: mock_llm)

    # Intercept write_repository_text_file to avoid modifying actual repo files
    written_files = {}
    monkeypatch.setattr(
        "src.agents.backend_agent.write_repository_text_file",
        lambda path, content: written_files.update({path: content}),
    )

    fake_state = {
        "task": {
            "description": "Add /items endpoint",
            "input_files": ["src/app/main.py"],
        },
        "requirements_report": {"acceptance_criteria": ["Return 200 OK"]},
        "project_plan_report": {"work_packages": [{"wp_id": "WP-1"}]},
        "architecture_report": {"findings": ["OK"]},
        "qa_security_report": {},
    }

    # Aufruf mit attempt=1
    res = my_backend_agent(fake_state, attempt=1)

    assert isinstance(res, dict)
    assert res["status_str"] == "approved"
    assert res["attempt"] == 1
    assert res["modified_files"] == ["src/app/main.py"]
    assert "Implemented" in res["summary"]
    assert written_files.get("src/app/main.py") == "# mock updated code"


def test_my_backend_agent_contract_with_qa_feedback(monkeypatch):
    """Prüft, ob my_backend_agent bei attempt > 1 das QA-Feedback übernimmt."""
    from unittest.mock import MagicMock
    from langchain_core.messages import AIMessage
    from src.agents.backend_agent import my_backend_agent

    captured_prompt = []

    def mock_invoke(messages):
        for m in messages:
            captured_prompt.append(m.content)
        return AIMessage(
            content=json.dumps({
                "status_str": "approved",
                "summary": "Fixed edge case from QA",
                "code": "",
            })
        )

    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = mock_invoke
    monkeypatch.setattr("src.agents.backend_agent.get_chat_model", lambda: mock_llm)

    fake_state = {
        "task": {
            "description": "Fix bug",
            "input_files": ["src/app/main.py"],
        },
        "requirements_report": {},
        "project_plan_report": {},
        "architecture_report": {},
        "qa_security_report": {
            "status_str": "changes_requested",
            "summary": "pytest failed: AssertionError on /ping",
        },
    }

    res = my_backend_agent(fake_state, attempt=2)
    assert res["status_str"] == "approved"
    assert res["attempt"] == 2
    # Sicherstellen, dass das QA Feedback im übergebenen Prompt enthalten war
    prompt_str = " ".join(captured_prompt)
    assert "PREVIOUS QA / TEST FEEDBACK" in prompt_str
    assert "AssertionError on /ping" in prompt_str

