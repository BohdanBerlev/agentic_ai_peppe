# Termin 2 — operative Agenten und interner Dry Run

Montag, 19. Oktober 2026, **10:00–15:00 Uhr**.

Verbindlich sind [Aufgaben](../task%20sheets/Aufgaben_Termin_1_und_2_de.md) und [Bewertungsraster](../task%20sheets/03_Bewertungsraster_GitHub_Termin_1_und_2.md). Diese Anleitung erläutert die gemeinsame Infrastruktur und ergänzt keine Bewertungskriterien.

## Bestehende Team-Repositories aktualisieren

Das Infrastrukturupdate ist bereitgestellter Starter-Code und keine Teamleistung. Haltet euren ursprünglichen Ausgangsstand und den Update-Commit getrennt fest. Ersetzt euer Repository nicht durch einen neuen Klon.

1. Aktuelle Arbeit committen und einen Arbeitsbranch anlegen.
2. Kursupdate holen, ansehen und übernehmen:

```bash
git fetch https://github.com/MARS-Group-HAW/agentic_ai.git fix/session-02-readiness
git show --stat FETCH_HEAD
git cherry-pick FETCH_HEAD
```

Dieser Branch enthält einen Infrastruktur-Commit auf Basis des bisherigen Starters. Bei Konflikten eigene Änderungen erhalten und die Korrektur integrieren. Bei Unsicherheit mit `git cherry-pick --abort` abbrechen und den Dozenten fragen. Update-SHA mit `git rev-parse FETCH_HEAD` festhalten.

3. Bestehende lokale `.env` gezielt ergänzen; Zugangsdaten nicht überschreiben:

```text
TRACE_FILE=logs/RUN_ID.jsonl
LLM_TIMEOUT_SECONDS=120
LLM_MAX_OUTPUT_TOKENS=768
```

`RUN_ID` ist ein vom Trace-Helper ersetzter Dateinamenplatzhalter; keine Shell-Expansion erforderlich. Alte feste Dateipfade werden weiterhin im Append-Modus beschrieben. Der Timeout begrenzt HTTP-Operationen und garantiert keine Gesamtlaufzeit. Eigene Workflows benötigen außerdem Grenzen für Schleifen/Calls und Regeln für unvollständige Ergebnisse.

## Zunächst eine vollständige Verarbeitungskette

Gemeinsames Task-/State-Modell mit zwei Agenten, strukturierte Übergabe und menschliche Freigabe/Eskalation implementieren. Danach dritte Fähigkeit, weitere Rollenunterstützung und Work-Item-Dry-Run vervollständigen. Drei Fähigkeiten decken nicht automatisch sechs oder sieben Rollen ab.

| Teamgröße | Mindestens operativ agentisch/hybrid unterstützte Rollen |
|---|---:|
| 6 Personen | 6 |
| 5 Personen | 7 |

Pro unterstützter Rolle Implementierung, unterscheidbares Verhalten/Ergebnis, Test oder Trace sowie accountable human zuordnen. Ein LLM-Status `approved` ist keine menschliche Freigabe: Mensch, Entscheidung, Task, geprüftes Artefakt und Zeitpunkt im State oder in einem Artefakt festhalten.

## Traces bei verteilter Entwicklung

- Standardmäßig entsteht pro Run `logs/<run_id>.jsonl`. Zusammenwirkende Agenten teilen eine `workflow_id`; Code, Trace, Review und Kosten teilen eine `task_id`. Die Agenten behalten unterschiedliche Run-IDs. Beim einzelnen Referenzagenten entspricht die Workflow-ID seiner Run-ID.
- Rolle, Agent, Modell, Provider, Tools, Status, Dauer, Calls und verfügbare Tokenzahlen erfassen. Der Helper akzeptiert zusätzliche Felder; Rollen- und Workflowkontext eigener Agenten ergänzen die Teams.
- `logs/*.jsonl` bleibt absichtlich ignoriert. Ausgewählte bereinigte **eigene** Traces nach `evidence/session-02/<run_id>.jsonl` kopieren und committen. Referenz-/Mock-Läufe sind kein realer Ausführungsnachweis eigener Agenten. Keine Zugangsdaten oder geschützten Inhalte ablegen.
- Compose bindet `./logs` unter `/workspace/logs` ein. Standardlogs bleiben auf dem Host erhalten; eigene Pfade außerhalb dieses Verzeichnisses benötigen einen weiteren Mount oder Export.
- Der Referenzlauf protokolliert Fehler, ungültige Ergebnisse und Tastaturabbrüche. Harte Prozessabbrüche und nicht beschreibbare Datenträger können Logging verhindern. Gespeichert wird der Fehlertyp, kein möglicherweise vertraulicher Provider-Fehlertext.

## Kosten und menschlicher Review-Aufwand

Die Kursraten in `costs/cost-model.yaml` gelten gemeinsam: Mensch 100 Credits/Stunde; LLM-Call 1; Laufzeit 0,01/Sekunde; Input 0,02/1000 Tokens; Output 0,04/1000 Tokens; CI 1/Lauf. Raten nicht eigenständig verändern.

Die Spalten von `costs/usage.csv` bleiben kompatibel. Pro zuordenbarem Verbrauch eine Zeile erfassen. Passende Run-/Workflow-ID, Modell, Calls, Dauer, Tokens und Tätigkeit (Implementierung/Review/Korrektur) in `notes` oder einer zusätzlichen strukturierten Kostendatei dokumentieren. Jede Zeile einem Task zuordnen; Detail- und Summenzeilen nicht doppelt zählen. Einzeldateien pro Person/Task können parallele Bearbeitung erleichtern; vor dem Snapshot einmal konsolidieren.

`estimate_cost_credits(..., calls=N)` berücksichtigt N Calls. Tokenzahlen summieren und Laufzeit für den abgerechneten Zeitraum einmal zählen. Standard `calls=1` erhält bisherige Aufrufe. Auch fehlgeschlagene Aufrufversuche zählen. Der OpenAI-kompatible Adapter deaktiviert automatische Retries, sodass ein Aufruf einem Versuch entspricht. Fehlende Tokenzahlen sind unbekannt, keine gemessene Null; Credits bleiben dann eine unvollständige Schätzung. Menschliche Zeit und CI separat ergänzen. Review-Zeit nicht zugleich als Implementierungszeit doppelt erfassen.

## PostgreSQL, Schema und Tests

Die CI stellt PostgreSQL/pgvector bereit, führt `db/init.sql` aus und setzt beide Datenbank-URLs. Ihr Persistenz-Probetest ist kein eigener API-Test. Work Items, eigenes Schema und API-/Persistenztests implementieren weiterhin die Teams.

Lokal:

```bash
docker compose up -d db
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1' < db/init.sql
python -m pytest
```

Für den mitgelieferten echten Datenbanktest vor pytest `STARTER_DATABASE_TEST=1` in der Shell setzen (`export STARTER_DATABASE_TEST=1` unter macOS/Linux; `$env:STARTER_DATABASE_TEST="1"` in PowerShell). Ohne Variable wird dieser Test übersprungen. `/db/health` zusätzlich bei laufender Anwendung prüfen. Der obige Aufruf mit Eingabeumleitung ist für Bash; in PowerShell das SQL beispielsweise mit `Get-Content db/init.sql | docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1'` übergeben.

Init-Skripte laufen automatisch nur bei einem neuen Datenverzeichnis. Für bestehende DBs einen expliziten, wiederholbaren Schema-/Migrationsaufruf dokumentieren. Keine Volumes zum Schema-Update löschen. Eigene Tests müssen ihr Schema vor API-Aufrufen initialisieren. Der DB-Nutzer des mitgelieferten CI-Probetests benötigt CREATE-TABLE-Rechte.

## Tagesablauf und Abgabe

| Zeit | Schwerpunkt |
|---|---|
| 10:00–10:20 | Stand-up, Blocker, Update und Rollenplan |
| 10:20–12:30 | Gemeinsames Modell, Workflow, Human Gate, Fähigkeiten und Tests |
| 12:30–13:00 | Pause |
| 13:00–14:30 | Persistente Work Items, Dry Run, Kosten und Review |
| 14:30–15:00 | Tests, Evidence-Export, Dokumentation und Repository Freeze |

Vor der Abgabe: `python -m pytest`, echte PostgreSQL-Persistenz prüfen, Workflow-Evidenz/Kosten committen, Rollen und Architektur aktualisieren und `docs/dry-run-01.md` auf maximal einer Seite erstellen. Nachweiskette erhalten: **Issue → Task → Agent/Mensch → Artefakt/Code → Test → menschliches Review**. Eigene Agenten und Work-Item-Lösung bleiben eure Implementierungsaufgabe.
