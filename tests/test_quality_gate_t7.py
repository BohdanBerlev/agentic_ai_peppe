"""Termin 7 (A3 & A4): Automatisierte Factory-Gate-Tests für HansePack (client-02).

Prüft deterministisch (ohne externes Netz, LLM gemockt, aber echte Produkttests via pytest):
1. Bestandener Gate-Zustand: Q01/Q03/E01 grün -> menschliche Freigabe ('approved') wird akzeptiert.
2. Zurückgehaltener Gate-Zustand (Rabatt-Injektion > 50 statt >= 50):
   Q03 liefert fälschlich 13700 statt 13075 Cent -> Quality Gate blockiert Freigabe hart.
3. Bounded Repair Loop: max_impl_retries wird strikt eingehalten.
4. Korrektur-Nachweis: Nach Behebung der Rabattgrenze besteht Q03 wieder und das Gate gibt frei.
"""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

from src.agents.common import REPO_ROOT
from src.workflows.feature_pipeline import (
    EngineeringTask,
    product_tests_failed,
    record_human_decision,
    run_feature_pipeline,
)
from tests.test_feature_pipeline import ApprovedMockLLM

FIXTURE_SOURCE_DIR = REPO_ROOT / "task sheets" / "session-06-08"

_QUOTATION_TEMPLATE = '''from __future__ import annotations
import json
from pathlib import Path


class QuotationError(ValueError):
    def __init__(self, reason: str, message: str) -> None:
        super().__init__(message)
        self.reason = reason
        self.message = message


def load_catalog() -> dict[str, dict]:
    catalog_path = Path(__file__).resolve().parent / "fixtures" / "HansePack_Katalog.json"
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    return {p["sku"]: p for p in data.get("products", [])}


def calculate_quote(items: list[dict], rule_version: str = "HP-V1") -> dict:
    if rule_version != "HP-V1":
        raise QuotationError("invalid_rule_version", "Only HP-V1 supported")
    if not isinstance(items, list) or len(items) == 0:
        raise QuotationError("empty_items", "Empty items")
    catalog = load_catalog()
    lines = []
    goods_net_cents = 0
    for item in items:
        sku = item["sku"]
        quantity = item["quantity"]
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise QuotationError("quantity_wrong_type", "Invalid quantity type")
        if quantity < 1 or quantity > 10000:
            raise QuotationError("quantity_out_of_range", "Quantity out of range")
        unit_price_cents = catalog[sku]["unit_price_cents"]
        list_amount_cents = quantity * unit_price_cents
        if 1 <= quantity <= 49:
            discount_percent = 0
        elif 50 <= quantity <= 99:
            discount_percent = 5
        else:
            discount_percent = 10
        discount_cents = (list_amount_cents * discount_percent + 50) // 100
        net_cents = list_amount_cents - discount_cents
        goods_net_cents += net_cents
        lines.append({
            "sku": sku,
            "quantity": quantity,
            "unit_price_cents": unit_price_cents,
            "list_amount_cents": list_amount_cents,
            "discount_percent": discount_percent,
            "discount_cents": discount_cents,
            "net_cents": net_cents,
        })
    shipping_cents = 1200 if goods_net_cents < 50000 else 0
    return {
        "lines": lines,
        "goods_net_cents": goods_net_cents,
        "shipping_cents": shipping_cents,
        "total_cents": goods_net_cents + shipping_cents,
        "currency": "EUR",
        "rule_version": "HP-V1",
    }
'''

_TEST_QUOTATION_TEMPLATE = '''from __future__ import annotations
import json
import sys
from pathlib import Path
import pytest
from quotation import QuotationError, calculate_quote

HERE = Path(__file__).resolve().parent
REF = json.loads((HERE / "fixtures" / "HansePack_Referenzfaelle.json").read_text(encoding="utf-8"))
VALID = {c["id"]: c for c in REF["valid_cases"]}
INVALID = {c["id"]: c for c in REF["invalid_cases"]}


@pytest.mark.parametrize("case_id", ["Q01", "Q03"])
def test_valid_case_hp_v1(case_id):
    case = VALID[case_id]
    res = calculate_quote(case["input"]["items"], rule_version="HP-V1")
    exp = case["expected"]["HP-V1"]
    assert res["goods_net_cents"] == exp["goods_net_cents"]
    assert res["shipping_cents"] == exp["shipping_cents"]
    assert res["total_cents"] == exp["total_cents"]


def test_q03_explicit_boundary_50():
    res = calculate_quote([{"sku": "HP-BOX", "quantity": 50}], rule_version="HP-V1")
    assert res["total_cents"] == 13075


def test_e01_quantity_zero_rejected():
    with pytest.raises(QuotationError) as exc:
        calculate_quote(INVALID["E01"]["input"]["items"])
    assert exc.value.reason == "quantity_out_of_range"


if __name__ == "__main__":
    sys.exit(pytest.main(["-q", str(Path(__file__).resolve())]))
'''


def inject_discount_boundary_fault(source_code: str) -> str:
    """Termin 7 A3: 5%-Rabatt erst oberhalb 50 (> 50) statt ab 50 (>= 50)."""
    faulty = source_code.replace("if 1 <= quantity <= 49:", "if 1 <= quantity <= 50:")
    faulty = faulty.replace("elif 50 <= quantity <= 99:", "elif 51 <= quantity <= 99:")
    assert faulty != source_code, "Discount boundary pattern not found in source_code"
    return faulty


def _prepare_isolated_hansepack(tmp_path: Path) -> Path:
    """Erstellt einen isolierten client-02-quotation-Checkout ohne Abhängigkeit zu externen Repos."""
    hp = tmp_path / "client-02-quotation"
    fixtures_dir = hp / "fixtures"
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    for fname in ("HansePack_Katalog.json", "HansePack_Referenzfaelle.json"):
        src = FIXTURE_SOURCE_DIR / fname
        assert src.is_file(), f"Missing course fixture: {src}"
        shutil.copyfile(src, fixtures_dir / fname)
    (hp / "quotation.py").write_text(_QUOTATION_TEMPLATE, encoding="utf-8")
    (hp / "test_quotation.py").write_text(_TEST_QUOTATION_TEMPLATE, encoding="utf-8")
    return hp


def _load_calculate_quote(checkout_dir: Path):
    spec = importlib.util.spec_from_file_location(
        f"quotation_{checkout_dir.parent.name}", checkout_dir / "quotation.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod.calculate_quote


def test_t7_quality_gate_passed_state_allows_human_approval(tmp_path):
    """A4 Positivfall: Korrekter HansePack-Stand besteht Fachtests und erlaubt menschliche Freigabe."""
    hp = _prepare_isolated_hansepack(tmp_path)
    trace_file = tmp_path / "t7_gate_pass.jsonl"

    task = EngineeringTask(
        task_id="HP-T7-GATE-PASS",
        project_id="client-02",
        target_dir=str(hp),
        description="Verify HansePack HP-V1 quotation logic passes quality gate",
        input_files=["quotation.py"],
        test_targets=["test_quotation.py"],
    )
    res = run_feature_pipeline(
        task,
        llm=ApprovedMockLLM(),
        trace_file=str(trace_file),
        interactive=False,
        run_pytest_in_qa=True,
        session_folder="session-07",
    )

    qa_rep = res["result_state"]["qa_security"]
    assert qa_rep["pytest_execution"]["tests_passed"] is True
    assert qa_rep["pytest_execution"]["exit_code"] == 0
    assert product_tests_failed(qa_rep) is False

    approval = res["result_state"]["human_approval"]
    assert approval["agent_recommendation"] == "approved"
    assert approval["quality_gate_blocked"] is False
    assert approval["product_tests_passed"] is True
    assert approval["decision"] == "pending_human_review"

    event = record_human_decision(
        str(trace_file),
        reviewer_name="Lars Boos",
        decision="approved",
        note="Q01/Q03/E01 bestanden, Gate-Freigabe erteilt.",
        review_seconds=12.0,
        product_commit="T7-TEST-CLEAN",
        test_status="3/3 passed (Q01, Q03=13075, E01)",
    )
    assert event["decision"] == "approved"
    assert event["human_approval"]["quality_gate_blocked"] is False
    assert event["product_commit"] == "T7-TEST-CLEAN"


def test_t7_quality_gate_blocks_discount_boundary_fault_q03(tmp_path):
    """A3/A4 Negativfall: Rabattgrenze > 50 erzeugt Q03=13700 statt 13075 und blockiert Freigabe hart."""
    hp = _prepare_isolated_hansepack(tmp_path)
    q_path = hp / "quotation.py"
    q_path.write_text(inject_discount_boundary_fault(q_path.read_text(encoding="utf-8")), encoding="utf-8")

    # Fachliche Vorprüfung: Q03 ergibt tatsächlich 13700 statt 13075 Cent
    calc = _load_calculate_quote(hp)
    assert calc([{"sku": "HP-BOX", "quantity": 50}])["total_cents"] == 13700

    trace_file = tmp_path / "t7_gate_fault.jsonl"
    task = EngineeringTask(
        task_id="HP-T7-GATE-FAULT-Q03",
        project_id="client-02",
        target_dir=str(hp),
        description="Verify HansePack quality gate blocks Q03 discount boundary fault",
        input_files=["quotation.py"],
        test_targets=["test_quotation.py"],
    )
    res = run_feature_pipeline(
        task,
        llm=ApprovedMockLLM(),
        trace_file=str(trace_file),
        interactive=False,
        run_pytest_in_qa=True,
        session_folder="session-07",
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

    # Selbst ein expliziter Freigabeversuch wird vom Quality Gate technisch blockiert
    blocked_event = record_human_decision(
        str(trace_file),
        reviewer_name="Lars Boos",
        decision="approved",
        note="Versuch einer Freigabe trotz fehlgeschlagenem Q03",
        review_seconds=5.0,
        product_commit="T7-FAULT-Q03",
        test_status="Q03 failed (13700 != 13075)",
    )
    assert blocked_event["decision"] == "changes_requested"
    assert blocked_event["human_approval"]["quality_gate_blocked"] is True


def test_t7_quality_gate_bounded_repair_loop_respects_max_retries(tmp_path):
    """A4 Schleifengrenze: Bei anhaltendem Q03-Fehler stoppt die Backend<->QA-Schleife nach max_impl_retries."""
    hp = _prepare_isolated_hansepack(tmp_path)
    q_path = hp / "quotation.py"
    q_path.write_text(inject_discount_boundary_fault(q_path.read_text(encoding="utf-8")), encoding="utf-8")

    attempts_seen: list[int] = []

    def stub_backend(_state, attempt: int):
        attempts_seen.append(attempt)
        return {
            "status_str": "approved",
            "summary": f"Attempt {attempt} left fault unfixed",
            "modified_files": [],
            "attempt": attempt,
        }

    trace_file = tmp_path / "t7_gate_bounded.jsonl"
    task = EngineeringTask(
        task_id="HP-T7-GATE-BOUNDED",
        project_id="client-02",
        target_dir=str(hp),
        description="Verify repair loop terminates at max_impl_retries",
        input_files=["quotation.py"],
        test_targets=["test_quotation.py"],
    )
    res = run_feature_pipeline(
        task,
        llm=ApprovedMockLLM(),
        trace_file=str(trace_file),
        interactive=False,
        run_pytest_in_qa=True,
        backend_agent_fn=stub_backend,
        max_impl_retries=2,
        session_folder="session-07",
    )

    assert attempts_seen == [1, 2]
    assert res["result_state"]["human_approval"]["quality_gate_blocked"] is True


def test_t7_quality_gate_recovers_after_fault_correction(tmp_path):
    """A3/A4 End-to-End: Fehler blockiert Gate -> Korrektur auf >= 50 -> Gate lässt Freigabe wieder zu."""
    hp = _prepare_isolated_hansepack(tmp_path)
    q_path = hp / "quotation.py"
    original = q_path.read_text(encoding="utf-8")

    # 1. Fehler einschleusen -> Gate blockiert
    q_path.write_text(inject_discount_boundary_fault(original), encoding="utf-8")
    res_fault = run_feature_pipeline(
        EngineeringTask(
            task_id="HP-T7-E2E-FAULT",
            project_id="client-02",
            target_dir=str(hp),
            description="Faulty state",
            input_files=["quotation.py"],
            test_targets=["test_quotation.py"],
        ),
        llm=ApprovedMockLLM(),
        trace_file=str(tmp_path / "e2e_fault.jsonl"),
        interactive=False,
        run_pytest_in_qa=True,
        session_folder="session-07",
    )
    assert res_fault["result_state"]["human_approval"]["quality_gate_blocked"] is True

    # 2. Fehler beheben -> Gate besteht und erlaubt Freigabe
    q_path.write_text(original, encoding="utf-8")
    fixed_trace = tmp_path / "e2e_fixed.jsonl"
    res_fixed = run_feature_pipeline(
        EngineeringTask(
            task_id="HP-T7-E2E-FIXED",
            project_id="client-02",
            target_dir=str(hp),
            description="Corrected state",
            input_files=["quotation.py"],
            test_targets=["test_quotation.py"],
        ),
        llm=ApprovedMockLLM(),
        trace_file=str(fixed_trace),
        interactive=False,
        run_pytest_in_qa=True,
        session_folder="session-07",
    )
    assert res_fixed["result_state"]["human_approval"]["quality_gate_blocked"] is False
    assert res_fixed["result_state"]["qa_security"]["pytest_execution"]["tests_passed"] is True

    approved = record_human_decision(
        str(fixed_trace),
        reviewer_name="Lars Boos",
        decision="approved",
        note="Rabattgrenze >= 50 wiederhergestellt, Q03=13075 Cent verifiziert.",
        review_seconds=10.0,
        product_commit="T7-E2E-FIXED",
        test_status="3/3 passed",
    )
    assert approved["decision"] == "approved"
