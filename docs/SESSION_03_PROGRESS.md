# Session 3 Preparation – Umsetzungs- und Test-Checkliste (PepeGroup)

Diese Datei dokumentiert alle umgesetzten und getesteten Verbesserungen aus dem Feedback zu Session 2 (`docs/Review/Team_3_Session_2_Feedback.md`), damit das Team und jede weitere Session den Stand sofort nachvollziehen können.

## Status-Übersicht nach Phasen

- [x] **Phase 0 – Aufräumen & Konsistenz (#3, #5, #12)**
  - [x] `README.md` auf die 4 aktiven Teammitglieder aktualisiert (Leon & Bohdan ausgeschieden; historische 6-Personen-Zeile aus Termin 1 in `costs/usage.csv` transparent erklärt).
  - [x] Davids Setup in `README.md` und `docs/architecture.md` dokumentiert: Windows 11 (HP Envy x360), VS Code, Google AI Studio (`gemini-3.8-flash`), da Ollama lokal hardwarebedingt nicht läuft und der HAW-ICC-Endpunkt noch nicht freigeschaltet wurde.
  - [x] `langchain-google-genai>=2.0.0` in `requirements.txt` ergänzt, damit der Google-Pfad reproduzierbar installiert wird.
  - [x] Widerspruch in `docs/dry-run-01.md` zum Trace `a4c5e5d8-6163-4b0f-a5e1-dcbaaefc0821` (Fehleingabe `approved` bei gleichzeitiger Notiz *„Bitte die Vorschläge umsetzen.“*) als transparentes Erratum dokumentiert, ohne historische JSONL-Evidenz zu manipulieren.
  - [x] CLI-Tippfehler `if __name__ == "_main_":` in allen Agenten auf `if __name__ == "__main__":` korrigiert und gemeinsame Security-/Hilfsfunktionen in `src/agents/common.py` gebündelt.

- [x] **Phase 1 – Kritische Fixes: Human Gate, Eskalation & Kosten (#1, #2, #8, #9, #10)**
  - [x] **Human Gate (`src/workflows/feature_pipeline.py`):** Im Headless-Modus wird niemals automatisch `"approved"` unter dem Namen eines Teammitglieds gesetzt (`decision: "pending_human_review"`, `reviewed_by: None`, separates Feld `agent_recommendation`). Im interaktiven Modus Pflicht-Prüfung gegen `VALID_ACCOUNTABLE_HUMANS` und Sicherheitsrückfrage bei Abweichung von der Agenten-Empfehlung.
  - [x] **GitHub-Issue-Runner (`src/workflows/run_github_issue.py`):** Schließt Issues nur noch bei `status == "success"` **und** echter menschlicher Freigabe (`decision == "approved"` mit `reviewed_by`). Negative Fälle (`changes_requested`, `invalid_output`, `pending_human_review`, `escalated`) durch Unit-Tests abgesichert.
  - [x] **Fehlende Kontextdateien (#10):** Alle Agenten und die Pipeline prüfen Kontextdateien vor dem LLM-Aufruf und eskalieren bei Lesefehlern sofort mit `calls = 0` (`status = "escalated"`).
  - [x] **Double-Counting im Cost-Agenten (#8):** `read_log_file` in `src/agents/cost_agent.py` überspringt Orchestrator-Summenzeilen (`feature_pipeline_workflow` / `workflow_summary`). Mit Regressionstest in `tests/test_cost_agent.py` abgesichert (bestätigt exakt `16.5785` Credits auf `evidence/session-02`).
  - [x] **Trennung menschlicher Zeiten (#9):** `human_review_seconds` wird getrennt von `duration_seconds` erfasst; `costs/usage.csv` besitzt nun die Spalte `activity` (`implementation`, `review`, `correction`, `waiting`, `meeting`).

- [x] **Phase 2 – 8 Operativ unterstützte Rollen, echte QA-Tests & Architektur (#4, #7, #11)**
  - [x] **8 technisch unterscheidbare Rollen mit eigenen Prompts, Schemas, Trace-Rollen und Tests:**
    1. `product_owner_requirements`: `requirements_agent.run_requirements_analysis` (`RequirementsReport`)
    2. `project_manager`: `requirements_agent.run_project_planning` (`ProjectPlanReport` mit `work_packages` & `delivery_risks`)
    3. `agent_engineer`: `requirements_agent.run_agent_engineering_spec` (`AgentDesignReport` mit `graph_nodes`, `required_tools`, `state_fields`)
    4. `software_architect`: `architect_agent.run_architect_review` (`ArchitectureReport`)
    5. `qa_test_engineer`: `qa_security_agent.run_qa_test_execution` (führt **echtes `pytest`** via `execute_repository_pytest` aus + deterministischer Guardrail bei Test-Fehlern)
    6. `ai_safety_security_engineer`: `qa_security_agent.run_security_audit` (`QASecurityReport`)
    7. `integration_engineer`: `integration_agent.run_integration_check` (`IntegrationHandoverReport` für A2A-Handover-Prüfung)
    8. `cost_observability_engineer`: `cost_agent.run_cost_analysis` (`CostReport`)
  - [x] **Backend-Agent-Steckplatz & Rückschleife (#11):** `build_pipeline_graph` unterstützt `backend_agent_fn` mit begrenzter automatischer Reparatur-Schleife (`max_impl_retries = 3`) zwischen `backend_implementation` und `qa_security`. Menschliches `changes_requested` beendet den Lauf und wird über `parent_workflow_id` im Folgelauf verknüpft.
  - [x] `organization/roles.yaml` und `docs/architecture.md` vollständig mit dem Code synchronisiert.

- [x] **Phase 3 – Echter PostgreSQL-Persistenz-Lifecycle-Test (#6)**
  - [x] `test_work_items_real_postgres_lifecycle` in `tests/test_work_items_api.py` ergänzt und gegen die laufende PostgreSQL-Datenbank erfolgreich ausgeführt (`47 passed` inkl. echtem `POST -> GET -> PATCH -> DELETE -> 404` Zyklus).

- [ ] **Phase 4 – Gemeinsamer Session-3-Auftrag (am Montag im Termin)**
  - [ ] Optional: Backend-Agent des Kollegen über `backend_agent_fn` in `run_feature_pipeline` einhängen.
  - [ ] Neuen Kundenauftrag aus Session 3 durch die Pipeline laufen lassen und Trace/Kosten dokumentieren.
