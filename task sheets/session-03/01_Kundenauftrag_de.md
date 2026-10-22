# Termin 3 – Kundenauftrag CUST-001: RequestBoard

**Montag, 26. Oktober 2026 · 10:00–15:00 Uhr**
**Fiktiver Kunde:** CampusService, interne IT-Unterstützung einer Hochschule.
**Auftraggeberrolle:** Lehrperson. Alle Teams erhalten denselben Auftrag.

## Die Anfrage des Kunden

„Unser kleines Serviceteam erhält Anfragen über verschiedene Kanäle. Wir verlieren den Überblick, was dringend ist und welche Anliegen bereits bearbeitet werden. Wir brauchen einen einfachen, verlässlichen Dienst, der Anfragen speichert, nach Priorität und Status filtert und ihren Bearbeitungsstand aktualisiert. Wir möchten heute eine vorführbare erste Version sehen.“

Ihr erweitert eure vorhandene Work-Item-Funktion aus Termin 2. Kein neuer technischer Unterbau. Vorhandene eigene Arbeit bleibt Grundlage; Bewertung honoriert den nachgewiesenen Kundenbeitrag und das Schließen relevanter Lücken.

## Verbindlicher MVP und API-Vertrag

Eine Anfrage besitzt `id`, `title`, optional `description`, `priority` und `status`. Der Kunde liefert keine personenbezogenen Daten; Beispiele sind synthetisch. Felder wie Zeitstempel aus dem bestehenden System dürfen bleiben.

| Operation | Verbindliches Verhalten |
|---|---|
| `POST /work-items` | Titel und optionale Beschreibung/Priorität annehmen; 201 mit gespeicherter Anfrage. |
| `GET /work-items` | Liste als JSON-Array; optional `status` und `priority` filtern. Beide Filter gemeinsam bedeuten UND. |
| `PATCH /work-items/{id}` | Genau das Feld `status` aktualisieren; 200 mit aktualisierter Anfrage. |

| Feld | Regel |
|---|---|
| `title` | String, getrimmt, 1–100 Zeichen nach Trimmen. |
| `description` | Optionaler String, maximal 1.000 Zeichen; fehlend wird leerer String. |
| `priority` | `low`, `normal`, `high`; Standard `normal`. |
| `status` | `open`, `in_progress`, `done`; bei Erstellung immer `open`. POST darf keinen anderen Status setzen. |
| Übergänge | `open → in_progress → done`; gleicher Zustand erneut ist zulässig und ändert nichts. Rückwärts und `open → done` sind unzulässig. |

Ungültige Eingaben, unbekannte Filterwerte und ungültige Übergänge liefern **422** ohne Zustandsänderung; unbekannte IDs bei PATCH **404**. Datenbankausfall liefert **503**, ohne Zugangsdaten, SQL oder rohe Ausnahmeinformationen im Response. Für POST sind nur `title`, `description`, `priority` erlaubt; PATCH akzeptiert nur `status`. Unbekannte JSON-Felder werden mit 422 abgelehnt. Fehlertexte innerhalb dieser Regeln dürfen teamspezifisch sein. Sortierung und DELETE sind heute keine zusätzlichen Kundenanforderungen.

Die API-Pfade sind für die Vergleichbarkeit verbindlich. Bestehende zusätzliche Endpunkte dürfen erhalten bleiben. Bestehende Daten müssen nach einer dokumentierten Migration verfügbar bleiben: fehlende Priorität wird `normal`, bisher `done=true` wird `done`, sonstige vorherige Zustände werden in einem dokumentierten Mapping übernommen. Kein Löschen produktiver/abgegebener Daten und kein `docker compose down -v` als Migrationsverfahren.

## Akzeptanzkriterien

| ID | Überprüfbare Abnahme |
|---|---|
| AC-01 | Gültiges POST erzeugt 201, neue ID, getrimmten Titel, Priorität und Status `open`. Defaults sind wie oben definiert. |
| AC-02 | Nach Schließen und Öffnen einer DB-Verbindung oder Neustart des API-Prozesses bleibt dieselbe Anfrage lesbar. Tatsächliches PostgreSQL verwenden. |
| AC-03 | GET ohne Filter liefert die gespeicherten Anfragen. Einzelfilter und kombinierte Filter liefern nur passende Einträge. |
| AC-04 | Ein gesetzter Status folgt den definierten Übergängen und bleibt über neue DB-Verbindungen erhalten. Gleicher Status erneut liefert 200. |
| AC-05 | Leerer/Blanko-/zu langer Titel, zu lange Beschreibung, ungültige Werte/Filter/Übergänge und unbekannte JSON-Felder werden mit 422 abgewiesen. |
| AC-06 | PATCH einer nicht vorhandenen ID liefert 404. |
| AC-07 | Simulierter DB-Ausfall liefert 503 und generische Fehlermeldung. Ein separater echter DB-Test belegt AC-02; Simulation ersetzt ihn nicht. |
| AC-08 | Eine Agentenübergabe verarbeitet ein vorher erzeugtes Artefakt fachlich. Ein Mensch prüft das Ergebnis und dokumentiert eine explizite Abnahme am eindeutigen Quellstand. |

Beispieldaten: „Beamer in Raum A prüfen“ (`high`), „Testkonto für Übung einrichten“ (`normal`), „Dokumentationslink aktualisieren“ (`low`). Ein vorführbares Beispiel verwendet mindestens drei Anfragen und zeigt Filter plus Statuswechsel.

## Rahmen und Umfang

Pflichtstack und Kostenmodell bleiben gültig: Python, FastAPI/Pydantic, PostgreSQL, LangGraph/LangChain, pytest, Docker und GitHub; LLM lokal/Ollama oder HAW ICC. Keine externen Cloud-LLM-Tokens oder externe Kundendatenübermittlung. Keine neuen Frameworks ohne vorherige Absprache. Authentifizierung, UI, E-Mail-Anbindung, RAG, Volltextsuche und Deployment sind nicht Teil dieser Tagesabnahme.

Die Lehrperson beantwortet fachliche Rückfragen in der Startphase. Haltet jede verbindliche Klärung in `docs/customer-01/clarifications.md` fest. Änderungen am verbindlichen API-Vertrag benötigen eine dokumentierte, für alle Teams kommunizierte Kundenentscheidung. Umsetzungsdetails entscheidet euer Team.
