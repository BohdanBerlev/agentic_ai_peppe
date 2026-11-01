"""
Termin 4 Factory Quality Gate Tests (Bewertungskriterien A3, A4, B6, Lernziele L4.2, L4.3).

Prüft deterministisch (ohne reale LLM-Aufrufe):
  1. Positiver Gate-Zustand: Vollständiger Release Candidate (AC-01..AC-08) besteht alle 4 Prüffamilien
     (F1 Pflichtinhalt, F2 Kontakt/Navigation, F3 Lokale Verweise/Assets, F4 Bedienbarkeit) -> Gate erlaubt 'approved'.
  2. Kontrollierter Fehler #1 (falsche Kontaktadresse mailto:kontakt@nordwerk-falsch.example):
     Produkttest schlägt fehl -> _compute_agent_recommendation liefert 'changes_requested' und
     enforce_quality_gate blockiert selbst eine versuchte 'approved'-Freigabe technisch.
  3. Kontrollierter Fehler #2 (gebrochener interner Navigationslink href="#kontakt-kaputt"):
     Produkttest schlägt fehl -> Gate blockiert 'approved' und erzwingt 'changes_requested'.
  4. Vollständiger Negativ-/Korrektur-Zyklus (run_fault_experiment) in isolierter Testkopie.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from src.agents.common import REPO_ROOT
from src.quality.fault_injection import inject_fault, run_fault_experiment
from src.workflows.feature_pipeline import (
    EngineeringTask,
    _compute_agent_recommendation,
    enforce_quality_gate,
    product_tests_failed,
    record_human_decision,
    run_feature_pipeline,
)
from tests.test_feature_pipeline import ApprovedMockLLM

FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "nordwerk_rc"


def _prepare_isolated_candidate(tmp_path: Path) -> Path:
    """Copy the complete Nordwerk RC fixture and product check script into an isolated temp directory."""
    dest = tmp_path / "candidate"
    shutil.copytree(FIXTURE_DIR, dest)
    live_check = REPO_ROOT / "client-01-website" / "test_website.py"
    if live_check.is_file():
        shutil.copyfile(live_check, dest / "test_website.py")
    else:
        shutil.copyfile(dest / "product_check_snapshot.py", dest / "test_website.py")
    return dest


def test_quality_gate_positive_candidate_passes_all_families(tmp_path):
    """A3/A4/B6 Positivfall: Vollständiger Candidate besteht F1-F4 und kann am Gate freigegeben werden."""
    candidate = _prepare_isolated_candidate(tmp_path)
    trace_file = tmp_path / "positive_gate.jsonl"

    task = EngineeringTask(
        task_id="TASK-002-POS",
        project_id="client-01",
        target_dir=str(candidate),
        description="Verify complete Nordwerk Release Candidate (AC-01 to AC-08)",
        input_files=["index.html"],
        test_targets=["test_website.py"],
    )

    res = run_feature_pipeline(
        task,
        llm=ApprovedMockLLM(),
        trace_file=str(trace_file),
        interactive=False,
        run_pytest_in_qa=True,
        session_folder="session-04",
    )

    qa_rep = res["result_state"]["qa_security"]
    assert qa_rep["pytest_execution"]["tests_passed"] is True
    assert qa_rep["pytest_execution"]["exit_code"] == 0
    assert product_tests_failed(qa_rep) is False

    approval = res["result_state"]["human_approval"]
    assert approval["agent_recommendation"] == "approved"
    assert approval["quality_gate_blocked"] is False
    assert approval["product_tests_passed"] is True

    # Menschliche Freigabe auf grünem Stand wird akzeptiert
    event = record_human_decision(
        str(trace_file),
        reviewer_name="David Pisarkiewicz",
        decision="approved",
        note="Alle Prüffamilien F1-F4 grün.",
        review_seconds=30.0,
    )
    assert event["decision"] == "approved"
    assert event["human_approval"]["quality_gate_blocked"] is False


@pytest.mark.parametrize("fault_kind", ["contact", "link"])
def test_quality_gate_blocks_controlled_fault_and_prevents_approval(tmp_path, fault_kind):
    """A3/A4/L4.3 Negativfall: Kontrollierter Kontakt- oder Linkfehler schlägt fehl und blockiert 'approved'."""
    candidate = _prepare_isolated_candidate(tmp_path)
    index_path = candidate / "index.html"
    original_html = index_path.read_text(encoding="utf-8")
    index_path.write_text(inject_fault(original_html, fault_kind), encoding="utf-8")

    trace_file = tmp_path / f"negative_gate_{fault_kind}.jsonl"
    task = EngineeringTask(
        task_id=f"TASK-002-FAULT-{fault_kind.upper()}",
        project_id="client-01",
        target_dir=str(candidate),
        description=f"Controlled {fault_kind} fault test",
        input_files=["index.html"],
        test_targets=["test_website.py"],
    )

    # Selbst mit einem Mock-LLM, das 'approved' zurückgibt, erkennt das QA-Tool den echten Testfehler
    res = run_feature_pipeline(
        task,
        llm=ApprovedMockLLM(),
        trace_file=str(trace_file),
        interactive=False,
        run_pytest_in_qa=True,
        session_folder="session-04",
    )

    qa_rep = res["result_state"]["qa_security"]
    assert qa_rep["pytest_execution"]["tests_passed"] is False
    assert qa_rep["pytest_execution"]["exit_code"] != 0
    assert qa_rep["status_str"] == "changes_requested"
    assert product_tests_failed(qa_rep) is True

    approval = res["result_state"]["human_approval"]
    assert approval["agent_recommendation"] == "changes_requested"
    assert approval["quality_gate_blocked"] is True
    assert approval["product_tests_passed"] is False

    # Selbst wenn ein Mensch versucht, den fehlerhaften Stand per record_human_decision als 'approved' freizugeben,
    # verweigert enforce_quality_gate die Freigabe technisch!
    blocked_event = record_human_decision(
        str(trace_file),
        reviewer_name="David Pisarkiewicz",
        decision="approved",
        note="Versuch einer Freigabe trotz Testfehler",
        review_seconds=15.0,
    )
    assert blocked_event["decision"] == "changes_requested"
    assert blocked_event["human_approval"]["quality_gate_blocked"] is True


def test_controlled_fault_experiment_detects_blocks_and_recovers(tmp_path):
    """A3/L4.3 End-to-End: Isolierte Testkopie -> Fehler erkannt & blockiert -> Korrektur besteht."""
    candidate = _prepare_isolated_candidate(tmp_path)
    work_root = tmp_path / "runs"
    ev_dir = tmp_path / "evidence"

    for fault in ("contact", "link"):
        record = run_fault_experiment(
            fault=fault,
            source_dir=candidate,
            work_root=work_root,
            evidence_dir=ev_dir,
        )
        assert record["status"] == "passed"
        assert record["expected_behaviour_observed"] is True
        assert record["negative_run"]["tests_passed"] is False
        assert record["negative_run"]["gate"]["quality_gate_blocked"] is True
        assert record["negative_run"]["gate"]["released"] is False
        assert record["corrected_run"]["tests_passed"] is True
        assert record["corrected_run"]["gate"]["quality_gate_blocked"] is False
        assert record["corrected_run"]["gate"]["released"] is True
        assert Path(record["evidence_file"]).is_file()


def test_c4_hypothesis_does_not_override_failed_product_tests():
    """Sicherstellen, dass die C4-Architektur-Auflösung NIEMALS einen fehlgeschlagenen Produkttest überstimmt."""
    arch_rep = {"status_str": "changes_requested", "role": "software_architect"}
    impl_rep = {"status_str": "approved", "role": "backend_api_engineer"}
    qa_rep = {
        "status_str": "approved",
        "role": "qa_test_engineer",
        "pytest_execution": {"tests_passed": False, "exit_code": 1},
    }
    int_rep = {"status_str": "approved", "role": "integration_engineer"}

    rec = _compute_agent_recommendation(
        [arch_rep, qa_rep, int_rep],
        arch_rep=arch_rep,
        impl_rep=impl_rep,
        qa_rep=qa_rep,
        int_rep=int_rep,
    )
    assert rec == "changes_requested"
    decision, blocked = enforce_quality_gate("approved", qa_rep)
    assert decision == "changes_requested"
    assert blocked is True
