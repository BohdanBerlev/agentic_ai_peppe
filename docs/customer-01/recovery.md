# Session 2 → 3 remediation / Nacharbeit

**Team:** PepeGroup (Team 3)  
**Aktuelle Teamgröße bestätigt durch:** Mehrose Farooq, Maxim Bers, David Pisarkiewicz, Lars Boos  
**Erforderliche unterstützte Rollen:** 12 − 4 = **8 operativ unterstützte Rollen**

| Finding / Befund | Priority + owner | Issue | Fix or scope decision / Änderung oder Priorisierung | Test / run / evidence | Remaining gap |
|---|---|---|---|---|---|
| **#1 Menschliche Freigaben Headless:** Pipeline erzeugte headless fälschlicherweise `approved` unter Mitgliedernamen | P1 (Hoch), David Pisarkiewicz | #1 | In `src/workflows/feature_pipeline.py` gehärtet: headless setzt immer `decision: "pending_human_review"` und `reviewed_by: None`. | `tests/test_feature_pipeline.py::test_headless_pipeline_never_auto_approves_under_human_name` | Behoben (keine Lücke) |
| **#2 Runner schließt Issues bei Fehlern:** GitHub-Runner schloss Issues trotz negativer Zwischenstände | P1 (Hoch), David Pisarkiewicz | #2 | `should_close_issue()` in `run_github_issue.py` verlangt zwingend `status == "success" and decision == "approved" and bool(reviewed_by)`. | `test_github_runner_does_not_close_on_negative_or_pending_decisions` | Behoben (keine Lücke) |
| **#3 Widerspruch Dry Run 1:** Trace wies `approved` auf, Bericht forderte `changes_requested` | P2 (Mittel), David Pisarkiewicz | #3 | Transparenz-Hinweis / Erratum in `docs/dry-run-01.md` ergänzt (Terminal-Fehleingabe erklärt, keine Manipulation historischer Evidenz). | `docs/dry-run-01.md` (Zeile 15) | Behoben (keine Lücke) |
| **#4 Fehlende Rollenabdeckung (8 Rollen):** Anforderungen, Architektur, QA und Sicherheit waren nicht hinreichend getrennt | P1 (Hoch), David Pisarkiewicz & Lars Boos | #4 | 8 unterscheidbare Rollen mit eigenen Modellen, Prompts, Traces und Schemas implementiert (PO, PM, AE, SA, QA, Sec, Int, Cost). | `tests/test_requirements_agent.py`, `tests/test_qa_security_agent.py`, `tests/test_feature_pipeline.py` | Behoben (8/12 operational) |
| **#5 Google-Provider Reproduzierbarkeit:** `langchain-google-genai` fehlte in `requirements.txt` | P2 (Mittel), David Pisarkiewicz | #5 | In `requirements.txt` aufgenommen; Begründung (Hardwareausfall, Laptop-Wechsel, ICC-Freischaltung ausstehend) dokumentiert. | `requirements.txt`, `README.md`, `docs/architecture.md` | Behoben; wird bei ICC-Freischaltung migriert |
| **#6 Fehlende DB-Persistenz in Tests:** API-Tests nutzten nur Mocks | P1 (Hoch), Maxim Bers | #6 | `test_work_items_real_postgres_lifecycle` in `tests/test_work_items_api.py` hinzugefügt (echter CRUD-Zyklus gegen PostgreSQL). | `tests/test_work_items_api.py` | Behoben (47 passed) |
| **#7 QA-Agent führt keine realen Tests aus:** Agent bewertete nur Code | P1 (Hoch), Lars Boos | #7 | `execute_repository_pytest` in `src/agents/qa_security_agent.py` integriert; harter Guardrail setzt Status auf `changes_requested`, wenn Tests rot sind. | `tests/test_qa_security_agent.py::test_qa_test_execution_runs_real_pytest_subproc` | Behoben (keine Lücke) |
| **#8 Double-Counting im Cost-Agenten:** Orchestrator-Zeilen wurden zu Sub-Agenten addiert | P1 (Hoch), Maxim Bers | #8 | `read_log_file` in `src/agents/cost_agent.py` ignoriert `workflow_summary` / `feature_pipeline_workflow`. | `tests/test_cost_agent.py::test_read_log_file_excludes_orchestrator_double_counting` | Behoben (bestätigt exakt 16,5785 Credits) |
| **#9 Trennung menschlicher Zeiten:** Review/Wartezeit nicht von Implementierung getrennt | P2 (Mittel), Maxim Bers | #9 | `costs/usage.csv` um Spalte `activity` (`implementation`, `review`, `correction`, `waiting`, `meeting`) erweitert; `human_review_seconds` getrennt erfasst. | `costs/usage.csv`, `src/workflows/feature_pipeline.py` | Behoben |
| **#10 Fehlende Kontextdateien vor LLM-Aufruf:** Modell wurde trotz Lesefehlern aufgerufen | P1 (Hoch), David Pisarkiewicz | #10 | `validate_context` bricht vor dem LLM-Aufruf mit `calls = 0` und `status = "escalated"` ab. | `test_architect_missing_file_escalates_without_llm_call` | Behoben |
| **#11 Architekturdiagramm Schleife:** Diagramm zeigte keine Schleifenbegrenzung | P2 (Mittel), David Pisarkiewicz | #11 | Mermaid-Diagramm in `docs/architecture.md` aktualisiert: menschliches Changes-Requested erfordert Folgelauf; steckbarer Backend-Loop ist auf max. 3 Versuche begrenzt. | `docs/architecture.md` | Behoben |

---

## Role evidence / Rollenevidenz

| Role | Current actor type | Accountable human | Distinguishable behaviour / Verhalten | Actual run / artifact | Status / remaining gap |
|---|---|---|---|---|---|
| **1. product_owner_requirements** | agent | Mehrose Farooq | `run_requirements_analysis` (User Stories, messbare Akzeptanzkriterien, Scope-Prüfung) | `RequirementsReport` in `evidence/session-02/` & `session-03/` | Operational |
| **2. project_manager** | hybrid | Lars Boos | `run_project_planning` (Work Packages, Meilensteine, Lieferrisiken) | `ProjectPlanReport` | Operational |
| **3. agent_engineer** | hybrid | David Pisarkiewicz | `run_agent_engineering_spec` (LangGraph-Knoten, Tools, State-Felder) | `AgentDesignReport` | Operational |
| **4. software_architect** | agent | David Pisarkiewicz | `run_architect_review` (Architektur, Interfaces, ADR-Prüfung) | `ArchitectureReport` | Operational |
| **5. qa_test_engineer** | agent | Lars Boos | `run_qa_test_execution` (führt reales `pytest` aus, wertet Exit-Codes und Fehlerberichte aus) | `QASecurityReport` + `pytest_execution` | Operational |
| **6. ai_safety_security_engineer** | agent | Lars Boos | `run_security_audit` (SQLi, Secret Leaks, Path Traversal, Guardrails) | `QASecurityReport` | Operational |
| **7. integration_engineer** | hybrid | David Pisarkiewicz | `run_integration_check` & Orchestrator (A2A-Übergaben, Konsistenz) | `IntegrationHandoverReport` | Operational |
| **8. cost_observability_engineer** | hybrid | Maxim Bers | `run_cost_analysis` (Token- und Credit-Berechnung ohne Double-Counting) | `CostReport` | Operational |
