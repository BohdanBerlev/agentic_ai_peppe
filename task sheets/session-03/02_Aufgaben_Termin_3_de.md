# Aufgaben Termin 3 – Erster Kundenauftrag

**26.10.2026 · 10:00–15:00 Uhr**
Lesereihenfolge: Kundenauftrag → Aufgaben → Bewertungsraster. Ziel ist ein kleiner, abgenommener Kundennutzen mit überprüfbarer Human-Agent-Zusammenarbeit.

## Tagesablauf

| Zeit | Tätigkeit / Ergebnis |
|---|---|
| 10:00–10:20 | Kundenbriefing, fachliche Rückfragen, bestätigte Teamgröße und Rollen. |
| 10:20–10:50 | Wichtigste Session-2-Lücke schließen; Human Gate und DB-Pfad prüfen. |
| 10:50–11:10 | Akzeptanzkriterien, Issues und Zuständigkeiten festlegen. |
| 11:10–12:30 | Erste vertikale Umsetzung, Migration und Tests. |
| 12:30–13:00 | Pause. |
| 13:00–14:00 | Agentenworkflow, Integrationstests, Fehlerfälle und Kosten. |
| 14:00–14:30 | Kundendemo und Review; höchstens 8 Minuten pro Team. |
| 14:30–15:00 | Korrekturen, finaler Testlauf und Abgabefreeze. |

## 1. Plattform stabilisieren und planen

Nehmt die drei wichtigsten Punkte aus eurem Feedback als Issues auf. Bestätigt die tatsächliche Teamgröße in `organization/company.md`; aktualisiert Rollen nach Evidenz. Die Mindestregel `12 − Teamgröße` bleibt ein organisatorisches Ziel. Offene Lücken werden ehrlich als solche dokumentiert. Es werden keine früheren Scores rückwirkend mit dem neuen Raster berechnet.

Vor einer Abnahme zwingend: kein automatisches `approved` als menschliche Entscheidung, keine Issue-Schließung bei `changes_requested`/ungültigem Ergebnis, zugelassener LLM-Pfad und ein ausführbarer echter DB-Test. Fehlende Rollenevidenz bearbeitet ihr parallel gezielt, ohne vier neue Agentenprogramme allein für Rollenlabels zu bauen.

Legt ein Kunden-Epic `CUST-001` sowie mindestens drei konkrete Issues an, z. B. Vertrag/Migration, Feature/Tests und Workflow/Abnahme. Ein Feature-PR mit kurzem menschlichem Review ist Pflicht. Ein Teammitglied darf mehrere Rollen haben; ein Mensch bleibt pro Task verantwortlich.

## 2. Anforderungen und Implementierung

Übertragt AC-01 bis AC-08 aus dem Kundenauftrag in `docs/customer-01/acceptance.md`: ID, Test/Artefakt, Ergebnis, Review. Ergänzt nur nachweisbar vereinbarte Kriterien. Modellvorschläge sind Entwürfe; erfundene Anforderungen werden verworfen und die freigegebene Fassung gespeichert.

Erweitert eure vorhandene API um Prioritäten, Filter und definierte Statuswechsel. Dokumentiert die Migration und das Mapping bestehender Daten. Eine funktionsfähige kleine Erweiterung genügt; kein Login, UI, RAG oder Deployment erforderlich.

## 3. Agentenbeitrag zeigen

Mindestens zwei eigene Fähigkeiten arbeiten an einem Kunden-Task. Mindestens ein Agent nutzt das fachliche Ergebnis eines anderen, z. B. Requirements-JSON → Architekturreview oder Review/Testreport → QA. Nur dieselbe Task-ID oder eine feste Aufrufreihenfolge reicht nicht.

Mindestens ein echter Lauf über lokales LLM/ICC; Unit-Tests dürfen Modelle mocken. Ein tatsächlicher Toolzugriff, strukturierte Outputs und Fehlerbehandlung sind Pflicht. Haltet `task_id`, `workflow_id`, `run_id`, Rolle, Provider, Modell, Tool, Ergebnisstatus und Artefaktreferenzen fest. Fachlicher Erfolg, technische Ausführung und menschliche Freigabe sind getrennte Zustände. Bei fehlender Eingabedatei kein kostenpflichtiger Modellaufruf.

Ein QA-Agent muss keine Tests selbst erzeugen; behauptet aber keine Testausführung, wenn er nur Code liest. Mindestens ein für die Abnahme verwendeter echter pytest-Lauf muss nachvollziehbar sein.

## 4. Testen und echte Persistenz belegen

Standardlauf im aktiven Projekt-Python:

```bash
python -m pytest -ra --junitxml=evidence/session-03/pytest.xml
```

Mindestens: gültige Erstellung/Defaults, Filter einzeln/kombiniert, gültige und ungültige Statuswechsel, unveränderte Daten nach 422, 404, generischer 503-Fehler und realer PostgreSQL-Persistenzfall. Parametrisierung ist erlaubt; Anzahl allein erzeugt keine Punkte.

Vereinbart für alle Teams einen eigenen Testort `tests/test_customer_persistence.py`; Helper dürfen anderswo liegen. Pflichtaufruf nach team-eigener dokumentierter DB-/Migrationsvorbereitung:

```bash
python -m pytest tests/test_customer_persistence.py -ra --junitxml=evidence/session-03/postgres.xml
```

Dieser Test öffnet eine neue DB-Verbindung oder einen neuen API-Prozess und prüft gespeicherte Werte erneut. Er darf PostgreSQL nicht mocken, nicht auf Memory wechseln und bei fehlender DB nicht still skippen. Lokal kann eine separate optionale DB-Suite bestehen; der Abnahmeaufruf muss bei fehlender DB fehlschlagen. Mindestens ein eigener Fall in der Ausgabe muss tatsächlich ausgeführt und bestanden sein. Ein Starter-DB-Test ersetzt den Kundentest nicht. Bereinigt nur selbst erzeugte Testdaten; niemals das gesamte Datenvolume löschen.

## 5. Human Gate und Demo

Standard: `pending_approval`, `changes_requested` oder Eskalation. Ohne Mensch keine Freigabe. Speichert Reviewer, Entscheidung, UTC-Zeit, Task/Workflow, geprüfte Artefakte und deren Quellstand/Hash. Ein Formular/CLI mit selbst angegebener Identität genügt für die Lehre; es wird keine IAM-Lösung verlangt. Hashwerte binden Inhalt, authentifizieren aber nicht die Person.

Tests müssen belegen: Headless erzeugt keine menschliche Zustimmung; ungültige/fehlgeschlagene Reports führen nicht zum automatischen Kundenabschluss. Eine begründete menschliche Risikoakzeptanz ist möglich, ersetzt aber keine Nachweise verbindlicher ACs. Wird nach dem Review Code geändert, erneut testen und reviewen.

Demo: Kundenproblem → drei Anfragen → Filter/Status → Persistenznachweis → Agentenübergabe → menschliche Entscheidung → Kosten/offene Punkte.

## 6. Kosten und Abgabe

Offizielle Credits: Call 1,0; Laufzeit 0,01/s; Input 0,02/1.000 Tokens; Output 0,04/1.000; Mensch 100/h; CI-Lauf 1,0. Fehlversuche zählen mit. Unbekannte Tokens als `null` plus unvollständige Schätzung ausweisen. Automatische Agentenlaufzeit ohne Human-Gate-Wartezeit erfassen. Summenzeilen/Orchestrator-Metadaten nicht zusätzlich als Calls oder Tokenverbrauch buchen; nach Run-ID deduplizieren. Shared-Setup-Kosten getrennt von Zusatzkosten dieses Tasks ausweisen.

Abgabe am finalen Commit: `docs/customer-01/acceptance.md`, `delivery.md`, `clarifications.md`, `recovery.md`; eigene Tests und Code; `evidence/session-03/` mit Traces, JUnit und Review; aktualisierte Kosten und Rollen/Architektur. Verwendet die Vorlagen unter `docs/templates/session-03/` und kopiert sie in euren Kundenordner. Die Templates selbst und Starterfixes zählen nicht als Eigenleistung.

Erfasst in `evidence/session-03/manifest.json` den geprüften Code-Commit, Testbefehle, Provider/Modell, IDs und Pfade. Evidenz darf in einem nachfolgenden reinen Evidenz-Commit ergänzt werden: nennt dann geprüften Code-Commit und Abgabe-Commit getrennt. Kein Quellcodewechsel zwischen Test und Review ohne erneute Prüfung.
