# Session 3 – Technical notes / Technische Hinweise

## Provided infrastructure / Bereitgestellte Infrastruktur

This update is supplied course infrastructure, not student achievement. / Dieses Update zählt nicht als studentische Eigenleistung.

- CI preserves pytest text/JUnit as a workflow artifact even after failure; `pipefail` preserves the failing pytest exit status.
- `/db/health` returns a generic 503 rather than leaking a raw connection exception.
- Optional Ollama controls are available through the existing provider factory; no package/version changes.

## Optional structured local output / Optionale strukturierte lokale Ausgabe

```python
model = get_chat_model(reasoning=False, json_mode=True)
```

The no-argument call retains its prior behaviour. These options apply to Ollama; the ICC branch keeps its existing request contract. JSON mode does not validate your domain schema or guarantee content correctness. Use your own Pydantic validation and fallback/escalation. Some model variants require thinking; a request flag cannot change their capabilities. Record the actual installed tag/digest and observed response, rather than assuming the generic alias or this flag guarantees suitable behaviour. No automatic model switch is introduced.

Der Aufruf ohne Argumente bleibt kompatibel. Die Optionen betreffen Ollama; der ICC-Pfad erhält keine Ollama-spezifischen Parameter. JSON-Modus ersetzt weder Pydantic-Validierung noch fachliche Prüfung. Thinking-only-Varianten lassen sich nicht zwingend per Schalter umstellen. Tatsächlichen installierten Modelltag/Digest und Antwortverhalten dokumentieren; kein automatischer Modellwechsel.

Useful local checks / Lokale Diagnose:

```bash
ollama list
ollama show <YOUR_INSTALLED_MODEL>
```

Use only the authorised local/HAW ICC path. External Google/OpenAI/other cloud endpoints are not made permissible by API compatibility or a free tier. Do not add provider packages to work around a local setup issue without agreement.

Nur lokalen/HAW-ICC-Pfad verwenden. Ein OpenAI-kompatibler externer Cloudendpoint oder ein kostenloses Kontingent ist dadurch nicht zugelassen. Setupprobleme zuerst mit Lehrperson klären.

## Database and migrations / Datenbank und Migrationen

```bash
docker info
docker compose up -d db
docker compose ps
```

Then run your own migration command documented in delivery.md. Container initialisation SQL runs only for a newly initialised data directory; changing `db/init.sql` does not migrate an existing named volume. Preserve data. Do not use `docker compose down -v` as a migration shortcut.

Danach den teamspezifischen Migrationsbefehl ausführen. `db/init.sql` läuft nur bei erstmaliger Initialisierung des Datenverzeichnisses. Bestehende Volumes werden durch eine Änderung daran nicht automatisch migriert. Daten erhalten.

Run the standard tests and the mandatory customer persistence test as specified in the assignment. `STARTER_DATABASE_TEST=1` forces only the supplied starter DB test; it cannot override `skipif` or a memory fallback in your own tests. The CI service alone does not prove that a customer test used PostgreSQL. Inspect the actual test and JUnit outcome. No customer solution or own persistence test is supplied by this update.

Standardtests und verpflichtenden Kundentest nach Aufgabenblatt ausführen. `STARTER_DATABASE_TEST=1` steuert nur den Startertest, nicht eure eigenen Skips/Fallbacks. CI-Service allein beweist keinen eigenen Persistenztest. Eigene Kundenimplementierung und Tests bleiben Teamaufgabe.

## Evidence / Evidenz

Keep separate run files; retain failed runs; deduplicate by run ID. A workflow rollup is metadata, not an extra model call. Do not mix human waiting time into agent execution time. Keep human decisions separate from model recommendations, including headless execution. No issue may be marked complete solely because the Python process exited successfully.

Separate Laufdateien, auch Fehlerläufe; nach Run-ID deduplizieren. Workflow-Summen sind keine zusätzlichen Calls. Menschliche Wartezeit separat erfassen. Eine erfolgreiche Python-Ausführung ist keine menschliche Freigabe und kein automatischer Kundenabschluss.

Team integration: review supplied diffs and merge selectively; do not overwrite own agents, API or tests. Factory additions may conflict with existing team parameters: preserve their behaviour and add the optional controls compatibly. Keep supplied code under the assessment boundary.

Teamintegration: Änderungen gezielt mergen; eigene Agenten/API/Tests nicht überschreiben. Bestehende Factory-Erweiterungen erhalten, optionale Parameter kompatibel ergänzen. Kursupdate als Infrastruktur dokumentieren.
