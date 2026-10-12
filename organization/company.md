# PepeGroup

## Name

**PepeGroup**

## Mission

Wir entwickeln Software zuverlässig und wirtschaftlich als Mixed Team aus
Menschen und KI-Agenten — mit klaren Rollen, nachvollziehbaren Entscheidungen
und messbaren Kosten.

## Team members

- **Mehrose Farooq** ([@Vanitas50](https://github.com/Vanitas50)) — Managing Director / Customer Lead, Product Owner / Requirements, Project Manager
- **Bohdan Berlev** ([@BohdanBerlev](https://github.com/BohdanBerlev)) — Software Architect, DevOps
- **Maxim Bers** ([@Valik71186](https://github.com/Valik71186)) — Backend / API, Data & RAG, QA & Test
- **Lars Boos** ([@Lbo114](https://github.com/Lbo114)) — AI Safety & Security, Cost & Observability, Backend / API, QA & Test
- **David Pisarkiewicz** ([@DavidPisark](https://github.com/DavidPisark)) — Agent Engineer, Integration
- **Heyen Leon** ([@heyenleon](https://github.com/heyenleon)) — Agent Engineer, Integration

## Working rules

### Task-Zuweisung

1. Task wird im Team **besprochen**.
2. Team erzielt eine **Einigung**.
3. Der Task wird der Person **zugeordnet**, deren Rolle am besten passt
   (siehe `organization/roles.yaml`).

### Entscheidungen

- Technische Entscheidungen trifft die jeweils zuständige Rolle; bei
  rollenübergreifenden Themen entscheidet das Team nach Einigung (siehe oben).
- Architektur- und Schnittstellenentscheidungen gehen über den Software
  Architect.

### Human Approval

- Bei **Security und anderen kritischen Kategorien ist der Mensch
  unersetzbar.** Ein vom LLM erzeugter Status wie `approved` ist eine
  Modellbewertung und **keine** menschliche Freigabe.
- Freigabepflichtig (accountable human): Requirements, Architektur, QA-Ergebnis,
  Releases und AI-Safety-/Security-Fragen.

### Agenten-Artefakte

- Agenten erstellen oder ändern Artefakte nur im Rahmen des zugewiesenen Tasks.
- Jeder agentische Output wird von einem **accountable human geprüft**, bevor er
  als Ergebnis zählt (Evidence over claims).

### Eskalation

- Blocker, Fehler oder unklare Verantwortung werden an den **accountable human**
  der Rolle eskaliert.
- Bei Sicherheits- oder Architekturfragen zusätzlich an Software Architect und
  AI Safety & Security.

### Kosten

- Kosten werden pro Task erfasst (Modell, Laufzeit, Tokens, Credits,
  Review-Aufwand).
- Bei Überschreitung des Task-Budgets stoppt die Arbeit und wird an den
  **Project Manager** eskaliert; Fortsetzung nur mit menschlicher Freigabe.
