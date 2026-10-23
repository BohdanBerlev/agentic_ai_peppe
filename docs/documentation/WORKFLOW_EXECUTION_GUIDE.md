# 🚀 PepeGroup – Workflow Execution Guide & Operations Manual

Dieser Leitfaden beschreibt im Detail, wie unsere Multi-Agenten-Pipeline aufgebaut ist, welche Ausführungsmodi existieren (CLI vs. GitHub Actions) und wie der Backend-Agent angebunden wird.

---

## 1. Übersicht der Pipeline-Architektur

Die Pipeline orchestriert alle **8 operativ unterstützten Rollen** in einer sauberen Reihenfolge:

```
Task-Eingabe (CLI / GitHub Issue)
   │
   ▼
1. validate_context (Prüft, ob Quell- und Kontextdateien existieren – verhindert LLM-Kosten bei Lesefehlern)
   │
   ▼
2. Product Owner (PO): requirements_agent.run_requirements_analysis
   └─ Erstellt User Stories & messbare Akzeptanzkriterien (RequirementsReport)
   │
   ▼ (im --full-company Modus)
3. Project Manager (PM): requirements_agent.run_project_planning
   └─ Erstellt Work Packages (WPs), Abhängigkeiten & Risikobewertung (ProjectPlanReport)
   │
   ▼ (im --full-company Modus)
4. Agent Engineer (AE): requirements_agent.run_agent_engineering_spec
   └─ Spezifiziert Graph-Knoten, State-Schema & benötigte Tools (AgentDesignReport)
   │
   ▼
5. Software Architect (SA): architect_agent.run_architect_review
   └─ Analysiert Code-Struktur, Schnittstellen, ADRs & Architektur-Findings (ArchitectureReport)
   │
   ▼
6. Backend / API Engineer (BE Slot): backend_implementation
   └─ Steckplatz für den autonomen Backend-Coding-Agenten (ImplementationResult)
   │
   ▼ ◄─────────────────────────────────────────────────────────────────┐
7. QA & Test Engineer: qa_security_agent.run_qa_test_execution         │
   └─ FÜHRT ECHTES PYTEST AUS! Evaluierung von Testlauf & Abdeckung     │ (Automatischer Fix-Loop:
   │                                                                    │  max. 3 Versuche bei
   ├─► [Tests rot / changes_requested?] ────────────────────────────────┘  fehlgeschlagenen Tests)
   │
   ▼ [Tests grün / approved]
8. AI Safety & Security Engineer: qa_security_agent.run_security_audit
   └─ Prüft SQL-Injection, Secrets, Prompt Injection & Guardrails (QASecurityReport)
   │
   ▼ (im --full-company Modus)
9. Integration Engineer: integration_agent.run_integration_check
   └─ Prüft Agent-to-Agent Übergabeverträge (PO->PM->SA->QA->Code) (IntegrationHandoverReport)
   │
   ▼
10. Human Approval Gate
    ├─ Interaktiv (Terminal): Mensch entscheidet (approved / changes_requested / escalate)
    └─ Headless (CI / Runner): Status bleibt 'pending_human_review' (kein Auto-Approve!)
    │
    ▼
11. Trace & Evidenz (evidence/session-02/ oder evidence/session-03/)
    └─ Zusammenfassung ohne Double-Counting; Kostenanalyse via cost_agent.run_cost_analysis
```

---

## 2. Ausführungsmöglichkeiten (Wie starte ich die Pipeline?)

Wir haben zwei primäre Wege, um die Pipeline zu triggern:

### Variante A: Lokal über die Kommandozeile (CLI)

Das ist der schnellste und flexibelste Weg für das Team im Labor / während der Session.

#### Modus 1: Standard-Review (Schneller 4-Augen-Check)
Führt PO (Requirements), SA (Architektur), QA/Security und das Human Gate aus:
```powershell
python -m src.workflows.feature_pipeline --desc "Überprüfe Endpunkt GET /work-items auf Pagination"
```

#### Modus 2: Full Company Modus (`--full-company`) – **Empfohlen für Session 3**
Aktiviert **alle 8 Rollen** inklusive Project Manager, Agent Engineer, Security Audit, Integration Handover Check und echte pytest-Ausführung:
```powershell
python -m src.workflows.feature_pipeline --desc "Implementiere Pagination und Status-Filter für Work-Items" --task-id "TASK-001" --full-company
```

#### Modus 3: Nachbesserung (Re-Run nach `changes_requested`)
Wenn ein Mensch im vorherigen Lauf Änderungen gefordert hat, verknüpft man den neuen Lauf direkt mit dem alten:
```powershell
python -m src.workflows.feature_pipeline --desc "Pagination nachgebessert" --task-id "TASK-001" --parent-workflow-id "<alte-workflow-id>" --feedback "Bitte Limit auf max 50 begrenzen" --full-company
```

---

### Variante B: Vollautomatisch über GitHub Issues & Actions

1. Ein Teammitglied oder Kunde erstellt ein neues **GitHub Issue** im Repository (z. B. mit Titel `[Feature]: Add sorting to work-items`).
2. GitHub Actions (`.github/workflows/agent_issue_trigger.yml`) triggert automatisch den Runner [`src/workflows/run_github_issue.py`](file:///c:/Users/pisar/Desktop/Studium/Semester%205/Agentic%20AI%20Projekt/agentic_ai_peppe/agentic_ai_peppe/src/workflows/run_github_issue.py).
3. **Ablauf im Issue:**
   - Das Issue erhält das Label `in-progress` und einen Kommentar: *"🤖 Agentic Pipeline gestartet!"*
   - Die Pipeline läuft headless durch.
   - **Wichtig – Human Gate Absicherung:** Da der Runner headless läuft, setzt das Human Gate die Entscheidung auf `pending_human_review` (oder `changes_requested` / `escalated`).
   - Der Runner postet die Ergebnisse aller Agenten als Kommentar.
   - **Das Issue wird NICHT voreilig geschlossen!** Erst wenn ein Mensch das Ergebnis freigegeben hat (z. B. lokal freigegeben oder via `record_human_decision`), darf das Issue geschlossen werden.

---

## 3. Kosten- & Observability-Auswertung (Cost Agent)

Nachdem ein oder mehrere Durchläufe gelaufen sind, kann der `cost_agent` gestartet werden, um die Traces zusammenzufassen:

```powershell
# Analysiert alle Traces in evidence/session-02 (ohne Orchestrator-Double-Counting):
python -m src.agents.cost_agent --dir "evidence/session-02" --query "Berechne die Gesamtkosten und Laufzeiten aller Agenten"
```

---

## 4. Steckplatz & Schnittstelle für den Backend-Agenten

Der Backend-Agent (geschrieben von Maxim / Backend-Team) wird als einfache Python-Funktion übergeben.

### Schnittstellendefinition (Contract):

```python
from pydantic import BaseModel, Field
from typing import Literal

class ImplementationResult(BaseModel):
    status_str: Literal["approved", "changes_requested", "unparseable", "escalated"] = "approved"
    summary: str
    modified_files: list[str] = Field(default_factory=list)
    attempt: int = 1
```

### Funktions-Signatur des Backend-Agenten:
```python
def my_backend_agent(state: dict, attempt: int) -> dict:
    """
    Input:
      state: Enthält den aktuellen Workflow-State:
        - state['task']['description']          -> Was soll gebaut werden?
        - state['requirements_report']           -> Akzeptanzkriterien vom PO
        - state['project_plan_report']           -> Work Packages vom PM
        - state['architecture_report']           -> Architektur-Vorgaben vom SA
        - state['qa_security_report']            -> Testergebnisse (bei Re-Try wertvoll!)
      attempt: Aktuelle Iteration (1, 2 oder 3)

    Output:
      Dictionary passend zu ImplementationResult:
      {
          "status_str": "approved",
          "summary": "Endpoints /work-items um Pagination erweitert",
          "modified_files": ["src/app/main.py"],
          "attempt": attempt
      }
    """
    # 1. Code generieren / modifizieren
    # 2. Datei speichern
    # 3. Ergebnis zurückgeben
    ...
```

### Einhängen in die Pipeline:
```python
from src.workflows.feature_pipeline import run_feature_pipeline, EngineeringTask
from src.agents.my_backend_agent import my_backend_agent

task = EngineeringTask(
    task_id="TASK-001",
    description="Implementiere Pagination für /work-items",
    input_files=["src/app/main.py"],
    test_targets=["tests/test_work_items_api.py"],
)

result = run_feature_pipeline(
    task,
    full_company_mode=True,
    backend_agent_fn=my_backend_agent,
    max_impl_retries=3  # Versucht bei roten pytest-Tests bis zu 3x automatisch zu fixen!
)
```
