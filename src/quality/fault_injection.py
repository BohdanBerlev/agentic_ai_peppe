"""
Termin 4 – Kontrollierte Fehlersituation am Qualitätsgate (Aufgabenblatt Abschnitt 3, Kriterien A3/A4, Lernziel L4.3).

Ablauf (deterministisch, ohne LLM):
  1. Produkt-Checkout in eine ISOLIERTE Testkopie kopieren (runs/session-04/fault-test/<run_id>/product, ohne .git).
  2. Ausgangsprüfung der unveränderten Kopie (muss bestehen, sonst Abbruch).
  3. GENAU EINEN Fehler injizieren:
       contact -> erste Kontaktadresse mailto:kontakt@nordwerk.example wird zu mailto:kontakt@nordwerk-falsch.example
       link    -> erster Navigationslink href="#kontakt" wird zu href="#kontakt-kaputt"
  4. Produktprüfung über das reale QA-Tool (execute_repository_pytest) ausführen -> muss FEHLSCHLAGEN.
  5. Gate-Logik der Factory anwenden – selbst bei optimistischem LLM-Status 'approved' und menschlichem 'approved':
       _compute_agent_recommendation -> 'changes_requested'; enforce_quality_gate -> blockiert.
  6. Fehler korrigieren (Originaldatei zurück), erneut prüfen -> muss BESTEHEN, Gate nicht blockiert.
  7. Ergebnis als JSON-Evidenz ablegen (evidence/session-04/fault-injection/<run_id>.json).

Die finale Kundenlieferung wird dabei NIE verändert.
"""

from __future__ import annotations

import difflib
import json
import shutil
import time
import uuid
from pathlib import Path
from typing import Any, Literal

from src.agents.common import REPO_ROOT
from src.agents.qa_security_agent import execute_repository_pytest
from src.workflows.feature_pipeline import _compute_agent_recommendation, enforce_quality_gate

FaultKind = Literal["contact", "link"]

CORRECT_MAILTO = "mailto:kontakt@nordwerk.example"
FAULTY_MAILTO = "mailto:kontakt@nordwerk-falsch.example"
CORRECT_LINK = 'href="#kontakt"'
FAULTY_LINK = 'href="#kontakt-kaputt"'
IGNORE = shutil.ignore_patterns(".git", "__pycache__", ".idea", ".pytest_cache")


def inject_fault(html: str, fault: FaultKind) -> str:
    """Return HTML with exactly ONE controlled fault (first occurrence only)."""
    old, new = (CORRECT_MAILTO, FAULTY_MAILTO) if fault == "contact" else (CORRECT_LINK, FAULTY_LINK)
    if old not in html:
        raise ValueError(f"Fault '{fault}' cannot be injected: {old!r} not found in index.html")
    return html.replace(old, new, 1)


def _gate_state(pytest_res: dict[str, Any]) -> dict[str, Any]:
    """Apply the real Factory gate functions with deliberately optimistic agent and human input."""
    optimistic = {"status_str": "approved"}
    qa_rep = {"status_str": "approved", "role": "qa_test_engineer", "pytest_execution": pytest_res}
    reports = [dict(optimistic, role="product_owner_requirements"), dict(optimistic, role="software_architect"), qa_rep]
    recommendation = _compute_agent_recommendation(reports, qa_rep=qa_rep)
    decision, blocked = enforce_quality_gate("approved", qa_rep)
    return {
        "llm_status_assumed": "approved",
        "human_decision_attempted": "approved",
        "agent_recommendation": recommendation,
        "effective_decision": decision,
        "quality_gate_blocked": blocked,
        "released": decision == "approved",
    }


def run_fault_experiment(
    fault: FaultKind = "contact",
    *,
    source_dir: str | Path = "client-01-website",
    work_root: str | Path | None = None,
    evidence_dir: str | Path | None = None,
    test_target: str = "test_website.py",
) -> dict[str, Any]:
    run_id = str(uuid.uuid4())
    source = Path(source_dir)
    source = source if source.is_absolute() else (REPO_ROOT / source)
    work_root = Path(work_root) if work_root else REPO_ROOT / "runs" / "session-04" / "fault-test"
    copy_dir = work_root / run_id / "product"
    shutil.copytree(source, copy_dir, ignore=IGNORE)

    index = copy_dir / "index.html"
    original = index.read_text(encoding="utf-8")
    started = time.strftime("%Y-%m-%dT%H:%M:%S")

    baseline = execute_repository_pytest([test_target], base_dir=str(copy_dir))
    if not baseline["tests_passed"]:
        record = {
            "run_id": run_id,
            "fault": fault,
            "status": "aborted_red_baseline",
            "reason": "Unveränderte Kopie besteht die Produktprüfung nicht – zuerst Candidate fertigstellen.",
            "baseline": baseline,
        }
        _write(record, evidence_dir, run_id)
        return record

    faulty = inject_fault(original, fault)
    index.write_text(faulty, encoding="utf-8")
    diff = list(
        difflib.unified_diff(
            original.splitlines(), faulty.splitlines(), "index.html (candidate)", "index.html (fault)", lineterm="", n=0
        )
    )
    negative = execute_repository_pytest([test_target], base_dir=str(copy_dir))
    negative_gate = _gate_state(negative)

    index.write_text(original, encoding="utf-8")  # Korrektur
    positive = execute_repository_pytest([test_target], base_dir=str(copy_dir))
    positive_gate = _gate_state(positive)

    expected = (
        negative["tests_passed"] is False
        and negative_gate["quality_gate_blocked"] is True
        and negative_gate["released"] is False
        and positive["tests_passed"] is True
        and positive_gate["quality_gate_blocked"] is False
    )
    record = {
        "record_type": "controlled_fault_experiment",
        "run_id": run_id,
        "session": "session-04",
        "fault": fault,
        "started_at": started,
        "isolated_copy": str(copy_dir.relative_to(REPO_ROOT)) if copy_dir.is_relative_to(REPO_ROOT) else str(copy_dir),
        "source_dir": str(source),
        "fault_diff": diff,
        "baseline_check": {k: baseline[k] for k in ("tests_passed", "exit_code", "command")},
        "negative_run": {**negative, "gate": negative_gate},
        "corrected_run": {**positive, "gate": positive_gate},
        "expected_behaviour_observed": expected,
        "status": "passed" if expected else "unexpected_behaviour",
        "llm_used": False,
        "note": "Deterministischer Gate-Nachweis; realer LLM-Lauf auf der Fehlerkopie separat ausgewiesen.",
    }
    _write(record, evidence_dir, run_id)
    return record


def _write(record: dict[str, Any], evidence_dir: str | Path | None, run_id: str) -> None:
    if evidence_dir is False:  # type: ignore[comparison-overlap]
        return
    out_dir = Path(evidence_dir) if evidence_dir else REPO_ROOT / "evidence" / "session-04" / "fault-injection"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{run_id}.json").write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    record["evidence_file"] = str(out_dir / f"{run_id}.json")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Termin 4 controlled fault injection experiment.")
    parser.add_argument("--fault", choices=["contact", "link"], default="contact")
    parser.add_argument("--source-dir", default="client-01-website")
    parser.add_argument("--test-target", default="test_website.py")
    args = parser.parse_args()

    result = run_fault_experiment(
        fault=args.fault,
        source_dir=args.source_dir,
        test_target=args.test_target,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
