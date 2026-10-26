# PepeGroup – Rollen & Agenten (Übersicht)

Stand: Termin 3. 4 Personen, 12 Rollen, 8 davon operativ durch Agenten/hybrid unterstützt.

## 1. Wer verantwortet welche Rolle

```mermaid
flowchart LR
    subgraph M["Mehrose Farooq"]
        MD["Managing Director<br/>(menschlich)"]
        PO["Product Owner<br/>(Agent)"]
    end
    subgraph L["Lars Boos"]
        PM["Project Manager<br/>(hybrid)"]
        QA["QA & Test<br/>(Agent)"]
        SEC["AI Safety & Security<br/>(Agent)"]
    end
    subgraph X["Maxim Bers"]
        BE["Backend / API<br/>(geplant)"]
        RAG["Data & RAG<br/>(geplant)"]
        OPS["DevOps<br/>(menschlich)"]
        COST["Cost & Observability<br/>(hybrid)"]
    end
    subgraph D["David Pisarkiewicz"]
        ARCH["Software Architect<br/>(Agent)"]
        AE["Agent Engineer<br/>(hybrid)"]
        INT["Integration<br/>(hybrid)"]
    end
```

## 2. Welcher Agent übernimmt welche Rolle

```mermaid
flowchart LR
    RA["requirements_agent"]
    AA["architect_agent"]
    QSA["qa_security_agent"]
    IA["integration_agent"]
    CA["cost_agent"]
    BA["backend_agent<br/>(implementation_agent)"]

    RA --> PO["Product Owner"]
    RA --> PM["Project Manager"]
    RA --> AE["Agent Engineer"]
    AA --> ARCH["Software Architect"]
    QSA --> QA["QA & Test"]
    QSA --> SEC["AI Safety & Security"]
    IA --> INT["Integration"]
    CA --> COST["Cost & Observability"]
    BA -. Ziel .-> BE["Backend / API"]
    BA -. Ziel .-> RAG["Data & RAG"]

    classDef op fill:#d3f9d8,stroke:#2b8a3e,color:#000;
    classDef plan fill:#e9ecef,stroke:#868e96,color:#000,stroke-dasharray:4 3;
    class PO,PM,AE,ARCH,QA,SEC,INT,COST op;
    class BE,RAG plan;
```

## 3. Die 12 Rollen im Detail

| # | Rolle | Aktuell | Agent / Funktion | Accountable | Status |
|---|---|---|---|---|---|
| 1 | Managing Director / Customer Lead | Mensch | – | Mehrose | geplant |
| 2 | Product Owner / Requirements | Agent | `requirements_agent` · `run_requirements_analysis` | Mehrose | **operational** |
| 3 | Project Manager | hybrid | `requirements_agent` · `run_project_planning` | Lars | **operational** |
| 4 | Software Architect | Agent | `architect_agent` · `run_architect_review` | David | **operational** |
| 5 | Backend / API | Mensch | `backend_agent` (Ziel) | Maxim | geplant |
| 6 | Data & RAG | Mensch | `implementation_agent` (Ziel) | Maxim | geplant |
| 7 | Agent Engineer | hybrid | `requirements_agent` · `run_agent_engineering_spec` | David | **operational** |
| 8 | Integration | hybrid | `integration_agent` · `run_integration_check` | David | **operational** |
| 9 | QA & Test | Agent | `qa_security_agent` · `run_qa_test_execution` (echtes pytest) | Lars | **operational** |
| 10 | DevOps | Mensch | – | Maxim | geplant |
| 11 | AI Safety & Security | Agent | `qa_security_agent` · `run_security_audit` | Lars | **operational** |
| 12 | Cost & Observability | hybrid | `cost_agent` · `run_cost_analysis` | Maxim | **operational** |

## 4. Die Agenten und ihre Fähigkeiten

| Agent | Fähigkeiten | Strukturierter Output | Rollen |
|---|---|---|---|
| `requirements_agent` | Requirements-Analyse, Projektplanung, Agent-Design | `RequirementsReport`, `ProjectPlanReport`, `AgentDesignReport` | PO, PM, Agent Engineer |
| `architect_agent` | Architektur-Review, Schnittstellen/ADRs | `ArchitectureReport` | Software Architect |
| `qa_security_agent` | QA (führt echtes `pytest` aus), Security-Audit | `QATestExecutionReport`, `QASecurityReport` | QA & Test, AI Safety & Security |
| `integration_agent` | Agent-to-Agent-Handover prüfen | `IntegrationHandoverReport` | Integration |
| `cost_agent` | Traces aggregieren, Kosten/Credits | `CostReport` | Cost & Observability |
| `backend_agent` | Produktdateien implementieren, `pytest` ausführen | `BackendImplementationReport` | Backend/API, Data & RAG (Ziel) |

## 5. Ablauf (Pipeline)

```mermaid
flowchart LR
    T["Kunden-Task / Issue"] --> REQ["requirements_agent"]
    REQ --> ARCH["architect_agent"]
    ARCH --> BE["backend_agent<br/>(optional, --use-backend-agent)"]
    BE --> QA["qa_security_agent<br/>(pytest + Security)"]
    QA --> INT["integration_agent"]
    INT --> G{"Human Gate"}
    G -->|approved| DONE["Freigabe"]
    G -->|changes_requested| NEXT["neuer Lauf"]
    G -->|escalate| HUMAN["Mensch / Eskalation"]
```

## 6. Menschliche Freigaben (Human Gate)

Freigabepflichtig (`human_approval_required: true`):
**Managing Director, Product Owner, Software Architect, QA & Test, DevOps, AI Safety & Security.**

Regel: Ein LLM-Status `approved` ist **keine** menschliche Freigabe. Headless bleibt die Entscheidung `pending_human_review`.

## 7. Verteilung auf 4 Personen

| Person | Rollen | Anzahl |
|---|---|---|
| Mehrose Farooq | Managing Director, Product Owner | 2 |
| Lars Boos | Project Manager, QA & Test, AI Safety & Security | 3 |
| Maxim Bers | Backend/API, Data & RAG, DevOps, Cost & Observability | 4 |
| David Pisarkiewicz | Software Architect, Agent Engineer, Integration | 3 |

**8 von 12** Rollen operativ agentisch/hybrid (Anforderung bei 4 Personen: ≥ 8).
