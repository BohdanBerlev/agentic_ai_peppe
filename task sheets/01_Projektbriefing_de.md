# Wahlpflichtprojekt Agentic AI – Projektbriefing

**HAW Hamburg – Fakultät Informatik**  
**Leitung:** Prof. Dr. Thomas Clemen  
**Format:** unbenotetes Wahlpflichtprojekt  
**Dauer:** 12 Termine, montags 10:00–15:00 Uhr  
**Teilnehmende:** ca. 17 Studierende  
**Organisation:** 3 Softwarefirmen mit jeweils ca. 5–6 Studierenden  
**Stand:** 7. Oktober 2026

---

## 1. Szenario

Ihr gründet im Team eine kleine Software-Entwicklungsfirma.

Für eure Firma sind mehr Rollen vorgesehen, als menschliche Teammitglieder vorhanden sind. Deshalb müsst ihr Rollen teilweise durch KI-Agenten oder hybride Human-Agent-Lösungen unterstützen.

Nach einer Aufbauphase von zwei Terminen erhält jede Firma einen Kundenauftrag.

Ab dann arbeitet ihr wie ein kleines Softwareunternehmen:

- Anforderungen verstehen,
- Aufgaben planen,
- Software entwickeln,
- testen,
- deployen,
- Agenten einsetzen,
- Kosten beobachten,
- auf Änderungswünsche und Störungen reagieren.

Das Projekt ist unbenotet. Trotzdem wird der technische Stand jeder Firma nach jedem Projekttag automatisiert anhand des GitHub-Repositories evaluiert.

---

## 2. Zentrale Fragestellung

Ziel ist nicht, möglichst viele Agenten zu bauen.

Ziel ist herauszufinden:

> **Wie kann ein Mixed Team aus Menschen und KI-Agenten zuverlässig und wirtschaftlich Software entwickeln?**

Dazu gehören insbesondere:

- sinnvolle Delegation an Agenten,
- Human Oversight,
- technische Integration von Agenten,
- Softwarequalität,
- Reproduzierbarkeit,
- Fehlerbehandlung,
- Cost Engineering,
- Anpassung der Organisation über das Semester.

---

## 3. Verbindliche Rollen

Jede Firma muss alle folgenden zwölf Rollen abdecken.

| Rolle | Hauptverantwortung |
|---|---|
| **1. Managing Director / Customer Lead** | Kundenkontakt, Prioritäten, Unternehmensentscheidungen |
| **2. Product Owner / Requirements Engineer** | Anforderungen, User Stories, Acceptance Criteria |
| **3. Project Manager** | Planung, Task-Zuordnung, Abhängigkeiten, Delivery-Risiken |
| **4. Software Architect** | Systemarchitektur, Schnittstellen, ADRs, technische Standards |
| **5. Backend / API Engineer** | FastAPI, Business Logic, API-Verträge |
| **6. Data & RAG Engineer** | PostgreSQL, pgvector, Ingestion, Retrieval, Embeddings |
| **7. Agent Engineer** | LangGraph-Workflows, LangChain, Agent State, Tools |
| **8. Integration Engineer** | Agent-to-Agent- und Agent-to-System-Schnittstellen |
| **9. QA & Test Engineer** | pytest, Regression Tests, Agent Evaluation |
| **10. DevOps Engineer** | Docker, GitHub Actions, Build, Deployment |
| **11. AI Safety & Security Engineer** | Tool Permissions, Guardrails, Secrets, Agent-Risiken |
| **12. Cost & Observability Engineer** | Traces, Laufzeiten, Token-Nutzung, Cost Engineering |

### Besetzungsregeln

Ein Mensch darf mehrere Rollen verantworten.

Für jede Rolle werden zwei Zustände unterschieden:

- **current_actor_type** – wie die Rolle aktuell ausgeführt wird,
- **target_actor_type** – wie die Rolle perspektivisch ausgeführt werden soll.

Mögliche Werte:

- `human`
- `agent`
- `hybrid`

Zusätzlich besitzt jede Rolle einen **accountable human**.

### Termin 1

Am ersten Termin darf eine geplante agentische Rolle noch aktuell durch einen Menschen ausgeführt werden.

Beispiel:

```yaml
current_actor_type: human
target_actor_type: agent
implementation_status: planned
```

### Ende Termin 2

Bis zum Ende von Termin 2 müssen mindestens

```text
12 - Anzahl menschlicher Teammitglieder
```

Rollen **operativ agentisch oder hybrid unterstützt** werden.

Bei 6 Studierenden also mindestens 6 Rollen, bei 5 Studierenden mindestens 7 Rollen.

Eine Rolle zählt nur dann als operativ agentisch/hybrid, wenn dafür technisch nachweisbares Verhalten existiert.

Ein Agent darf mehrere Rollen unterstützen, wenn:

- das rollenabhängige Verhalten unterscheidbar ist,
- unterschiedliche Inputs/Outputs oder Policies existieren,
- die Ausführung in Traces nachvollziehbar ist.

---

## 4. Verbindlicher Technologie-Stack

Alle Firmen beginnen mit demselben Starter Repository.

### Software Engineering

- GitHub
- GitHub Issues
- GitHub Actions
- Git
- Python 3.12
- FastAPI
- Pydantic
- pytest
- Docker
- Docker Compose

### Agentic AI

- LangGraph
- LangChain
- LLM über die im Starter definierte Provider-Abstraktion
- lokal über Ollama **oder**
- über einen von der HAW bereitgestellten ICC-Endpunkt

Agent-Code soll nicht direkt von einer konkreten LLM-Installation abhängen.

### Data / RAG

- PostgreSQL
- pgvector
- `langchain-postgres`
- psycopg 3

PostgreSQL dient als:

- relationale Anwendungsdatenbank,
- Metadatenbank,
- Basis für RAG / Vector Retrieval.

### Observability und Cost Engineering

Pflicht sind lokale, maschinenlesbare Projektartefakte:

- Agent Execution Traces,
- Laufzeiten,
- Modell / Agent / Task,
- Erfolg oder Fehler,
- Token-Nutzung, soweit verfügbar,
- Cost Records.

### LangSmith

LangSmith ist **optional** und kein Bestandteil der Bewertungsgrundlage.

Wenn LangSmith verwendet wird, ersetzt es nicht die lokalen Traces im Repository.

### Weitere Tools

Weitere Frameworks, Datenbanken, Vector Stores, Workflow Engines oder Observability-Plattformen dürfen nur nach vorheriger Absprache eingesetzt werden.

---

## 5. Das Starter Repository

Das Starter Repository liefert eine gemeinsame technische Basis.

Es enthält unter anderem:

- FastAPI-Basisservice,
- PostgreSQL + pgvector,
- Docker-Konfiguration,
- GitHub-Actions-Basisworkflow,
- pytest-Basistests,
- `pytest.ini` für konsistente Test-Imports und Testpfade,
- LLM-Provider-Abstraktion,
- lokale Trace-Hilfsfunktionen,
- Cost-Model-Template,
- Rollen-Template,
- Architektur-Template,
- einen LangGraph-Referenzagenten.

### Setup-Anleitungen und Aufgaben

Die ausführliche Einrichtung von Python, Docker und Ollama bzw. des HAW-ICC-Zugangs ist in den Setup-Anleitungen beschrieben:

- Deutsch: [SETUP_LOCAL_DE.md](../docs/SETUP_LOCAL_DE.md)
- Englisch: [SETUP_LOCAL_EN.md](../docs/SETUP_LOCAL_EN.md)

Die konkreten Aufgaben und Abgabe-Checklisten stehen in [Aufgaben Termin 1 und 2 – Deutsch](Aufgaben_Termin_1_und_2_de.md) bzw. [Tasks Sessions 1 and 2 – English](Tasks_Session_1_and_2_en.md). Die Bewertungskriterien stehen im [Bewertungsraster für Termin 1 und 2](03_Bewertungsraster_GitHub_Termin_1_und_2.md).

### Standard-Testaufruf

Für das Projekt gilt als Standard:

```bash
python -m pytest
```

Dieser Aufruf soll lokal und in der CI verwendet werden. Er stellt sicher, dass `pytest` aus derselben Python-Umgebung wie das Projekt ausgeführt wird.

### Tests und echte Ausführung unterscheiden

Die Startertests verwenden ein simuliertes LLM. Ein erfolgreicher Testlauf weist daher noch keinen echten LLM-Aufruf und keine funktionierende PostgreSQL-Verbindung nach. Prüft die Datenbank separat über `/db/health` und führt den Referenzagenten mit eurem konfigurierten LLM aus. Der Referenzlauf dient der Starter-Verifikation; für die Abgabe ist zusätzlich ein echter Lauf eures eigenen Agenten mit zuordenbarem Trace erforderlich.

### Laufzeit und Terminierung

Eigene Workflows sollen nachvollziehbare Grenzen für Laufzeit, LLM-Aufrufe und mögliche Schleifen besitzen. Zeitüberschreitungen und andere Fehler müssen zu einem definierten Fehlerergebnis führen. Der unveränderte Starter garantiert diese Begrenzungen noch nicht durchgehend; eine gesetzte Timeout-Variable allein genügt nicht als Nachweis. Der Referenzlauf kann auf lokaler Hardware mehrere Minuten dauern. Hinweise dazu stehen in der Setup-Anleitung.

### Wichtig

Der Starter ist **keine studentische Leistung**.

Insbesondere zählen folgende Bereiche nicht als Nachweis eines eigenen Agenten oder eigener Tests:

```text
examples/**
tests/starter/**
pytest.ini
```

Templates zählen erst dann als studentische Leistung, wenn sie sinnvoll an die eigene Firma angepasst wurden.

Die genaue Grenze ist in

```text
docs/STARTER_BOUNDARY.md
```

beschrieben.

---

## 6. GitHub ist die zentrale Projektakte

Nach jedem Projekttag wird ein Snapshot des Firmen-Repositories evaluiert.

Bewertet wird ausschließlich nachvollziehbare Repository-Evidenz.

### Gute Evidenz

- eigener ausführbarer Code,
- eigene Tests,
- GitHub Issues,
- Pull Requests ab dem Kundenprojekt,
- Agent Execution Traces,
- strukturierte Outputs,
- Cost Records,
- Architecture Decision Records,
- aktualisierte Architektur,
- nachvollziehbare Kunden-Deliverables.

### Keine ausreichende Evidenz

Eine Aussage wie

> „Unser QA-Agent übernimmt die Qualitätskontrolle.“

reicht nicht.

Ein Nachweis wäre beispielsweise:

```text
Task
   ↓
QA Agent unter src/agents/
   ↓
Execution Trace
   ↓
strukturierter QA-Report
   ↓
Test / Human Review
```

### Menschliche Freigaben

Ein vom LLM erzeugter Status wie `approved` ist eine Modellbewertung und keine menschliche Freigabe. Ein Human Approval Gate benötigt eine ausdrückliche menschliche Entscheidung, die dem Task und dem Agentenergebnis zugeordnet werden kann. Ein strukturell gültiges Ergebnis muss weiterhin fachlich geprüft werden.

An Termin 1 kann ein manuelles Review-Artefakt die Entscheidung dokumentieren. Bis Ende Termin 2 muss mindestens ein Workflow einen expliziten menschlichen Freigabe- oder Eskalationspunkt vorsehen; die Entscheidung muss im Workflow-State oder im erzeugten Artefakt nachvollziehbar sein.

Grundregel:

> **Evidence over claims.**

---

## 7. Cost Engineering von Anfang an

Auch ein lokal ausgeführtes LLM wird im Projekt nicht als „kostenlos“ behandelt.

Alle Firmen verwenden ein abstraktes Credit-Modell.

Ab Termin 1 werden mindestens erfasst:

- menschliche Arbeitszeit,
- Agentenläufe,
- verwendetes Modell,
- Agentenlaufzeit,
- Tokens, soweit verfügbar,
- CI-Läufe.

Ab Termin 2 kommen task-bezogene Kosten und menschlicher Review-/Korrekturaufwand hinzu.

Die entscheidende Frage ist nicht:

> Welches Team nutzt die meisten Agenten?

Sondern:

> Welche Human-Agent-Konfiguration liefert bei guter Qualität den sinnvollsten Aufwand?

---

## 8. Arbeitsweise

Die Teams arbeiten weitgehend selbstorganisiert.

Ein sinnvoller Tagesrhythmus ist:

### 10:00–10:20 – Company Stand-up

- Tagesziel
- Blocker
- aktuelle Rollen
- geplante Human-/Agent-Aufgabenteilung

### 10:20–12:30 – Engineering

### 12:30–13:00 – Pause

### 13:00–14:30 – Engineering

### 14:30–15:00 – Repository Freeze

Vor dem Ende des Projekttages:

- Tests mit `python -m pytest` ausführen,
- offene Issues aktualisieren,
- Execution Traces sichern,
- Cost Records aktualisieren,
- Dokumentation auf den tatsächlichen Stand bringen.

---

## 9. Was nicht optimiert werden soll

Das Projekt belohnt nicht automatisch:

- viele Agenten,
- komplexe Multi-Agent-Systeme,
- sehr große Modelle,
- viele LLM Calls,
- möglichst viel Autonomie,
- viele Commits,
- umfangreiche Dokumentation ohne Implementierung.

Eine einfache Lösung kann die bessere Lösung sein.

Entscheidend sind:

- Funktionalität,
- technische Qualität,
- Nachvollziehbarkeit,
- sinnvoller Agenteneinsatz,
- Kosten,
- Lernfortschritt.

---

## 10. Ziel nach Termin 1

Nach dem ersten Projekttag soll gelten:

> **Firma steht. Plattform läuft. Ein erster eigener Agent arbeitet, wird getestet, hinterlässt Evidenz und seine Nutzung ist messbar.**

Es wird noch keine vollständige Agentenorganisation erwartet.

Zum Abgabezustand gehören mindestens ein eigener LangGraph-Agent mit realem Tool, strukturiertem Input/Output und sinnvoller Fehlerbehandlung, ein eigener pytest-Test, ein echter eigener Execution Trace sowie erfasste Nutzung und berechnete Credits. Firmenmodell, Rollenmodell, Architektur und Team-Setup müssen angepasst sein. Mindestens drei sinnvolle GitHub Issues und eine nachvollziehbare Commit-Historie sind erforderlich; Pull Requests sind an Termin 1 optional.

---

## 11. Ziel nach Termin 2

Nach Termin 2 soll jede Firma eine kleine, aber funktionsfähige **Agentic Development Platform** besitzen.

Sie soll mindestens zeigen:

- alle zwölf Rollen sind organisatorisch abgedeckt,
- mindestens `12 - Anzahl menschlicher Teammitglieder` Rollen sind operativ agentisch/hybrid unterstützt,
- mindestens drei unterscheidbare eigene Agentenfähigkeiten / Rollenimplementierungen sind vorhanden; drei getrennte Agenten sind dafür nicht zwingend erforderlich,
- LangGraph/LangChain werden tatsächlich genutzt,
- jede eigene Agentenfähigkeit besitzt klaren Input, strukturierten Output, mindestens ein reales Tool, Fehlerbehandlung und Trace-Evidenz,
- mindestens zwei Agenten verwenden ein gemeinsames Task-/State-Modell,
- mindestens ein LangGraph-Workflow verbindet mindestens zwei Agenten durch technische Übergabe über State / strukturierte Daten; manuelles Copy/Paste zählt nicht,
- mindestens ein Workflow enthält ein explizites Human Approval Gate oder einen Eskalationspunkt,
- strukturierte Traces machen einen echten Workflow-Run nachvollziehbar,
- Erfolgsfall, Fehlerfall, strukturierter State / Output und Terminierung bzw. Schleifenbegrenzung werden getestet,
- Kosten werden task-bezogen einschließlich menschlichem Review-/Korrekturaufwand erfasst,
- die Softwarebasis ist mit `python -m pytest` getestet und reproduzierbar.

### Verpflichtender interner Dry Run

Vor dem Kundenauftrag erweitert ihr den Starter-Service um eine persistente **Work-Item-Funktion**:

- Work Item anlegen,
- Work Items auflisten,
- Work Item als erledigt markieren oder löschen,
- Speicherung in PostgreSQL,
- eigene automatisierte API-Tests.

Mindestens ein Teil der Umsetzung wird über euren Agentic Development Workflow bearbeitet. Die Kette von GitHub Issue über Task und Agent-/Human-Beitrag bis zu Code, Test und Review muss nachvollziehbar sein.

Dokumentiert den Dry Run in `docs/dry-run-01.md` auf maximal einer Seite: Umsetzung, beteiligte Menschen und Agenten, notwendige Korrekturen/Freigaben, task-bezogene Kosten und eine konkrete Verbesserungsidee für den nächsten Task.

Ab Termin 3 beginnt der erste Kundenauftrag.

