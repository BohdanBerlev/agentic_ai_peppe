# Architecture

## Current System (Termin 1)

Das System basiert auf LangGraph. Der aktuell operative eigene Agent ist der
**Cost & Observability Agent** (`src/agents/cost_agent.py`); er liest die
Ausführungsnachweise (Traces) des Teams und erzeugt einen strukturierten
Kostenreport.

### Agentic Flow: Cost & Observability

```mermaid
flowchart TD
    Human([Team member / CLI]) -->|start| Agent[Cost & Observability Agent\nLangGraph]

    subgraph Graph[LangGraph]
        Agent --> Load[Node: load_logs]
        Load -->|Tool: read_log_file| Evidence[(evidence/ + logs/)]
        Load -->|error| End((END))
        Load -->|ok| Analyze[Node: analyze]
        Analyze --> LLM{LLM adapter\nOllama / HAW ICC / Gemini}
        Analyze --> Parser[Pydantic: CostReport]
        Parser --> Gate{Human Gate}
    end

    Gate -->|approved| Report[CostReport / Kosten]
    Gate -->|changes_requested / escalate| Human
    Report --> Traces[(Lokale JSONL-Traces)]
    Traces --> CostModel[costs/ - Credits]

    API[FastAPI] --> DB[(PostgreSQL + pgvector)]
    Report -.persist.-. DB
```

### LLM-Zugang

- Zugriff nur über die Abstraktion `src/llm/factory.py`.
- Provider pro `.env`: lokal `ollama` (`qwen3:4b`) oder OpenAI-kompatibel
  (HAW ICC). Kein Agent-Code hängt direkt von einem konkreten Modell ab.

### Tools and Security

- Tool: `read_log_file` liest Traces aus `evidence/` bzw. `logs/`.
- Strikte Pfadgrenze per `.resolve()`, um Path Traversal außerhalb des
  Repos zu blockieren.

### Human Gate / Escalation

- Der erzeugte `CostReport` ist ein **Vorschlag**, keine Freigabe.
- Freigabe/Eskalation durch den accountable human (Cost & Observability
  Engineer, Lars Boos). Bei Security-/Architekturthemen zusätzlich Architect
  und AI Safety.
- Ein LLM-Status wie `approved` zählt nicht als menschliche Freigabe.

### Traces and Cost Path

- Laufzeit-Traces: `logs/*.jsonl` (gitignored). Ausgewählte, bereinigte Traces
  werden in `evidence/session-01/` committet.
- Der Cost Agent aggregiert Läufe, Laufzeit und Tokens und bildet daraus die
  Credits (`costs/`).

### Integration with FastAPI / PostgreSQL

- Der Basis-Service (FastAPI) liefert `/health` und `/db/health`.
- PostgreSQL + pgvector ist die gemeinsame Datenplattform und später Träger der
  persistenten Work-Items (Termin 2). Der Agent nutzt den LLM-/DB-Zugang über
  dieselbe Konfiguration (`.env`).

## Baseline Design Decisions

* **Agent Orchestration:** Uses LangGraph.
* **Abstractions:** LangChain provides model/integration abstractions.
* **LLM Independence:** Team code must not depend directly on a specific LLM deployment.
* **Data Platform:** PostgreSQL + pgvector is the common relational and vector data platform.
* **Project Evidence:** Local structured traces are mandatory project evidence.
* **Observability:** LangSmith is optional and cannot replace local evidence.
* **Local Environment:** Ollama normally runs natively on the host when used on macOS.

## Team Changes / ADRs

* **LLM Provider:** Factory-Abstraktion; Agenten laufen je nach `.env` über
  lokale Modelle (Ollama) oder ICC/Gemini.
* **Datenaustausch:** Lokale Logs sind gitignored; bereinigte Traces werden nach
  `evidence/` gepusht. Der Cost Agent liest dieses Verzeichnis dynamisch aus.
* **Sicherheit:** `read_log_file` blockiert Path Traversal.
