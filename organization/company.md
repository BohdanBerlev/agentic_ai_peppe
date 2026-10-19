# PepeGroup

## Mission

Software zuverlässig und wirtschaftlich bauen – als Team aus Menschen und
Agenten, mit klaren Rollen und messbaren Kosten.

## Team

- **Mehrose Farooq** ([@Vanitas50](https://github.com/Vanitas50)) – Managing Director, Product Owner
- **Lars Boos** ([@Lbo114](https://github.com/Lbo114)) – Project Manager, QA & Test, AI Safety & Security
- **Maxim Bers** ([@Valik71186](https://github.com/Valik71186)) – Backend/API, Data & RAG, DevOps, Cost & Observability
- **David Pisarkiewicz** ([@DavidPisark](https://github.com/DavidPisark)) – Software Architect, Agent Engineer, Integration

> 4 Mitglieder → bis Ende Termin 2 mindestens **8 Rollen** operativ agentisch/hybrid.

## Zusammenarbeit

- Task im Team besprechen, sich einigen, dann der Person mit der passenden
  Rolle zuweisen (siehe `roles.yaml`).
- Technische Entscheidungen trifft die zuständige Rolle, bei übergreifenden
  Themen das Team.

## Menschliche Freigabe

- Bei Security und anderen kritischen Themen entscheidet der Mensch. Ein
  LLM-Status wie `approved` ist keine Freigabe.
- Freigabepflichtig: Requirements, Architektur, QA-Ergebnisse, DevOps/Release, AI Safety & Security sowie alle übergeordneten Kunden- und Projektentscheidungen.

## Agenten

- Agenten arbeiten nur im zugewiesenen Task; Ergebnisse prüft immer ein Mensch.

## Eskalation und Kosten

- Blocker oder Fehler an den accountable human; bei Security/Architektur
  zusätzlich an Architect und AI Safety.
- Kosten pro Task erfassen. Über dem Budget: Stopp, Eskalation an den Project
  Manager, weiter nur mit Freigabe.

## Erste Entscheidungen

1. Erster Agent: **Cost_Agent** – übernimmt die Rolle des Cost & Observability Engineers, liest Trace-Logs aus dem `evidence/`-Ordner aus, aggregiert deterministisch Token-/Laufzeitdaten und generiert strukturierte Kostenreports.
2. Bleibt menschlich: **Managing Director** – Kundenkontakt und Verantwortung.
3. **Human Gate:** Security und Freigaben vor einem Release.