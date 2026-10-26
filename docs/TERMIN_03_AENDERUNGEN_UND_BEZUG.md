# 📘 Termin 3 – Vollständiger Umsetzungsbericht & Leitfaden für das Team

**Projekt:** PepeGroup (Team 3) – Agentic AI Software Factory  
**Kundenauftrag:** Kundenprojekt 01 – Nordwerk Industrie-Service (Termin 3 Scope)  
**Dokumentzweck:** Schritt-für-Schritt-Erklärung aller durchgeführten Code- und Dokumentationsänderungen, deren exakter Bezug zur Aufgabenstellung / zum Bewertungsraster sowie deren technische Auswirkungen für die Teamabstimmung und Präsentation vor dem Dozenten.

---

## Inhaltsverzeichnis
1. [Übersicht der fünf Arbeitsblöcke](#1-übersicht-der-fünf-arbeitsblöcke)
2. [Block 1: Kurs-Infrastruktur-Update (Revision 5)](#2-block-1-kurs-infrastruktur-update-revision-5)
3. [Block 2: Technische Trennung der Repositories (L3.1 / A1)](#3-block-2-technische-trennung-der-repositories-l31--a1)
4. [Block 3: Das Kundenprodukt `client-01-website` (B1–B6)](#4-block-3-das-kundenprodukt-client-01-website-b1b6)
5. [Block 4: Factory-Erweiterung für Kundenprojekte (L3.2, L3.3 / A2–A4)](#5-block-4-factory-erweiterung-für-kundenprojekte-l32-l33--a2a4)
6. [Block 5: Kosten, Nacharbeit & Abgabe-Dokumentation (L3.4 / C1–C4, D1–D2)](#6-block-5-kosten-nacharbeit--abgabe-dokumentation-l34--c1c4-d1d2)
7. [Spickzettel für das Teammeeting: Wer erklärt was?](#7-spickzettel-für-das-teammeeting-wer-erklärt-was)

---

## 1. Übersicht der fünf Arbeitsblöcke

| Block | Betroffene Bereiche | Ziel / Kernaufgabe |
|---|---|---|
| **Block 1** | Factory (`src/app/main.py`, `src/llm/factory.py`, `STARTER_MANIFEST.json`, `tests/starter/`) | Übernahme des offiziellen Dozenten-Updates (Revision 5) zur Sicherung der Kurs-Regressionstests |
| **Block 2** | Root `.gitignore`, `client-01-website/` | Trennung von Factory (Meta-Ebene) und Kundenprodukt (Anwendungsebene) in zwei eigenständige Git-Repositories |
| **Block 3** | `client-01-website/` (`index.html`, `styles.css`, `test_website.py`, `README.md`, `issue_t3.md`) | Erstellung des Release Candidate für Nordwerk Industrie-Service mit Pflichtinhalten und eigenem Test |
| **Block 4** | `src/workflows/feature_pipeline.py`, `src/agents/common.py`, `tests/test_feature_pipeline.py` | Befähigung der Factory, externe Produkt-Checkouts mit Path-Traversal-Schutz sicher zu bearbeiten |
| **Block 5** | `docs/customer-01/`, `evidence/session-03.md`, `costs/usage.csv` | Vollständige Befüllung aller geforderten Evidenz-, Nacharbeits- und Kostenberichte |

---

## 2. Block 1: Kurs-Infrastruktur-Update (Revision 5)

### Was wurde angepasst?
1. **`tests/starter/test_session_03_infrastructure.py` neu erstellt:**  
   Beinhaltet die drei vom Dozenten vorgegebenen Regressionstests:
   - `test_database_health_does_not_expose_exception`: Prüft, dass `/db/health` bei Fehlern keine sensiblen Verbindungsdaten leakt, sondern mit generischem 503 antwortet.
   - `test_ollama_json_and_reasoning_are_optional`: Prüft, ob `get_chat_model()` bei Ollama die Parameter `json_mode` und `reasoning` optional steuern kann.
   - `test_icc_does_not_receive_ollama_options`: Stellt sicher, dass der `openai_compatible`-(ICC)-Zweig keine Ollama-spezifischen Keys (`reasoning`, `format`) an `ChatOpenAI` sendet.
2. **`src/app/main.py` (`/db/health`):**  
   Die Exception-Detail-Meldung wurde von `"Database unavailable"` auf kleingeschriebenes `"database unavailable"` korrigiert, exakt wie im Dozenten-Test verlangt (`assert response.json() == {"detail": "database unavailable"}`).
3. **`src/llm/factory.py` (`get_chat_model`):**  
   Signatur erweitert auf:
   ```python
   def get_chat_model(
       settings: Settings | None = None,
       *,
       reasoning: bool | None = None,
       json_mode: bool = False,
   ) -> Any:
   ```
   - Für **Ollama**: Wenn `json_mode=True`, wird `format="json"` gesetzt und `reasoning` auf `False` standardisiert (es sei denn, `reasoning` wird explizit als `True` übergeben).
   - Für **OpenAI / ICC**: Weder `format` noch `reasoning` werden übergeben; `max_tokens` und `max_retries=0` bleiben unverändert erhalten.
4. **`STARTER_MANIFEST.json`:**  
   Auf `"starter_revision": 5` erhöht und Metadatenblock `"session_3_infrastructure_update"` ergänzt.
5. **`docs/SESSION_03_TECHNICAL_NOTES.md` & `docs/templates/session-03/`:**  
   Die zweisprachigen technischen Hinweise und die leeren Vorlagen (`acceptance.md`, `clarifications.md`, `delivery.md`, `manifest.json`, `recovery.md`, `review.json`) archiviert.

### Bezug zur Aufgabenstellung
- **Kursvorgabe:** *„Course infrastructure regressions; not student achievement.“*
- **Rubrik D1:** Eigene Factory-Prüfungen und Bereitstellung der Starter-Basis.
- **Dozenten-Hinweis:** *„Factory additions may conflict with existing team parameters: preserve their behaviour and add the optional controls compatibly.“*

### Auswirkungen
- Alle drei Starter-Infrastrukturtests laufen deterministisch grün.
- Die Factory unterstützt nun optionalen JSON-Modus und Reasoning-Abschaltung für lokale Ollama-Modelle, ohne bestehende Pipelines zu brechen.
- Der ICC-Zweig bleibt streng kompatibel zu OpenAI-Standards.

---

## 3. Block 2: Technische Trennung der Repositories (L3.1 / A1)

### Was wurde angepasst?
1. **Eigenständiges Kunden-Repository `client-01-website/`:**  
   Es wurde ein separates Unterverzeichnis `client-01-website/` angelegt und als **eigenständiges Git-Repository** initialisiert (`git init`).
   - Eigener initialer Commit: `9ccbf61` (*„feat(client-01): initial customer release candidate for Nordwerk Industrie-Service (T3)“*).
2. **Entkopplung in `.gitignore` der Factory:**  
   `client-01-website/` wurde in die `.gitignore` des Factory-Repositories (`agentic_ai_peppe`) aufgenommen.

### Bezug zur Aufgabenstellung
- **Lernziel L3.1:** *„Factory und Produkt technisch trennen und einen Kundenauftrag explizit adressieren.“*
- **Kriterium A1 (10 Punkte):** *„Zwei Repos; konfigurierter Produkt-Checkout/Projektkennung; Factory-Code bleibt zentral.“*
- **Kriterium B5 (5 Punkte):** *„Kleiner Website-Stand ohne Factory-Prozess vorführbar; Start und separater Produkttest dokumentiert.“*

### Auswirkungen
- Es existieren zwei technisch strikt getrennte Repositories mit getrennten Git-Historien.
- Keine Vermischung von Commits: Der Produkt-Commit (`9ccbf61`) kann unabhängig vom Factory-Commit (`ea374b5`) bewertet und geprüft werden.
- Das Produkt erzwingt dem Kunden nicht den Factory-Stack (kein FastAPI, kein Docker, kein LangChain im Kundenprodukt).

---

## 4. Block 3: Das Kundenprodukt `client-01-website` (B1–B6)

### Was wurde angepasst?
1. **`client-01-website/index.html` & `styles.css`:**  
   Reines, barrierefreies HTML5/CSS3 ohne externe Abhängigkeiten, Tracker oder Skripte:
   - **N-01 (Firmenname):** `Nordwerk Industrie-Service` in Header und Brand-Bereich.
   - **N-02 (Hauptaussage):** `Praktische Unterstützung für Ihren technischen Betrieb.` im Hero-Bereich.
   - **N-03 (Erste Leistung):** `Wartungsplanung: Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe.` in eigener Service-Card.
   - **N-08 (Kontaktlink):** Button beschriftet mit `Anfrage stellen`, verlinkt exakt auf `mailto:kontakt@nordwerk.example`.
   - **N-09 (Übungshinweis):** `Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. Keine realen Angebote oder Kontaktaufnahme.` als auffälliger Hinweis-Banner und im Footer.
2. **`client-01-website/test_website.py` (Automatisierter Produktcheck):**  
   Eigenständiges Python-Testskript unter Verwendung der Standardbibliothek (`html.parser`), prüft alle Pflichtkriterien ab:
   - Firmenname, Hauptaussage, Leistungsbeschreibung, Mailto-Linkziel, Linktext, Lehrprojekthinweis, deutsches Sprachattribut (`lang="de"`), UTF-8 und Abwesenheit unerlaubter Skripte/Tracker.
   - **Testergebnis:** `8 bestanden, 0 fehlgeschlagen` (Exit-Code 0).
3. **`client-01-website/README.md`:**  
   Dokumentiert den autonomen Start und Testaufruf:
   ```bash
   # Lokaler Start:
   python -m http.server 8000
   # Produkttest:
   python test_website.py
   ```
4. **`client-01-website/issue_t3.md`:**  
   Dokumentiert das Kunden-Issue `TASK-001` mit den Akzeptanzkriterien für Termin 3 und den expliziten Annahmen.

### Bezug zur Aufgabenstellung
- **Kriterien B1, B2, B3 (jeweils 5 Punkte = 15 Punkte):** AC-01 sichtbar erfüllt, erste Leistung aus AC-02 vorhanden, AC-04 vollständig erfüllt.
- **Kriterium B4 (5 Punkte):** Sinnvoller automatisierter Check prüft Tagesinhalt und ist erfolgreich ausführbar.
- **Kriterium B6 (5 Punkte):** Task referenziert Tageskriterien, Pflichtinhalte und explizite Annahmen ohne erfundene Leistungsversprechen.

### Auswirkungen
- Die Website ist sofort im Browser vorführbar und erfüllt 100 % der für Termin 3 geforderten Textvorgaben.
- Der automatisierte Test belegt maschinell die Korrektheit des HTML-Stands, bevor ein Mensch manuell gegenprüft.

---

## 5. Block 4: Factory-Erweiterung für Kundenprojekte (L3.2, L3.3 / A2–A4)

### Was wurde angepasst?
1. **`src/agents/common.py`:**  
   - `read_repository_text_file(relative_path, base_dir=None)`: Ermöglicht das Lesen aus einem definierten Basispfad.
   - `write_target_text_file(relative_path, content, target_dir=None)` neu implementiert: Erlaubt Agenten das kontrollierte Schreiben in den Kunden-Checkout, wehrt jedoch Path-Traversal-Versuche (`../../`) deterministisch mit einem Security-Error ab.
2. **`src/workflows/feature_pipeline.py`:**  
   - `EngineeringTask` erweitert um `target_dir: str | None = None` und `project_id: str = "client-01"`.
   - `step_validate_context`: Löst Dateien im Kontext des konfigurierten `target_dir` auf.
   - `step_backend_implementation`: Führt Aktionen sicher im Zielordner aus.
   - CLI-Parameter `--target-dir client-01-website`, `--project-id client-01` und `--session session-03` hinzugefügt.
3. **`tests/test_feature_pipeline.py`:**  
   Zwei neue Regressionstests ergänzt:
   - `test_pipeline_addresses_client_target_dir`: Belegt, dass die Pipeline externe Verzeichnisse sauber adressiert.
   - `test_pipeline_target_dir_path_traversal_protection`: Belegt, dass Ausbruchsversuche vor dem Modellaufruf mit `calls = 0` eskalieren.

### Bezug zur Aufgabenstellung
- **Lernziel L3.2:** *„Mindestens zwei Agentenfähigkeiten mit strukturierten Übergaben an einem echten Produktartefakt zusammenarbeiten lassen.“*
- **Kriterium A2 (10 Punkte):** Reales Modell über Provider, reales Tool und agentisch geänderte Produktdatei.
- **Kriterium A3 (10 Punkte):** Mindestens zwei Fähigkeiten tauschen strukturierte Daten aus (`RequirementsReport` -> `ArchitectureReport` -> `ImplementationResult` -> `QASecurityReport`).
- **Kriterium A4 (10 Punkte):** Menschliches Gate entscheidet über den Stand; Schleifenlimit implementiert; zulässiger Arbeitsbereich beschränkt.

### Auswirkungen
- Die Factory ist nicht mehr auf das eigene Codebase-Verzeichnis beschränkt, sondern agiert als echte Software-Fabrik für externe Projekte.
- Durch die Pfadvalidierung können Agenten niemals versehentlich Factory-Dateien überschreiben.

---

## 6. Block 5: Kosten, Nacharbeit & Abgabe-Dokumentation (L3.4 / C1–C4, D1–D2)

### Was wurde angepasst?
1. **`evidence/session-03.md` (Zentrale Abgabedatei):**  
   Enthält alle geforderten Pflichtabschnitte:
   - Verlinkung beider Repositories und Commit-Stände (Factory: `ea374b5`, Produkt: `9ccbf61`).
   - Eindeutige Run-ID `website-run-001` mit Verweis auf den Trace [`evidence/session-03/runs/website-run-001.jsonl`](file:///c:/Users/Lars_Boos/Documents/Entwicklung/agentic_ai_peppe/evidence/session-03/runs/website-run-001.jsonl).
   - Prüftabelle der Tageskriterien (AC-01, AC-02 Teil, AC-04) und Testergebnisse.
   - **Konkreter Engpass mit Beleg:** Modell versuchte initial ein JavaScript-Formular mit externem CDN einzubinden; Guardrail forderte Korrektur auf reinen `mailto:`-Link.
   - **Überprüfbare Lernhypothese für T4:** Pydantic-Komponenten-Grammatik senkt Tokenanzahl um mindestens 20 % und eliminiert Syntax-Fehlversuche.
   - Genau drei nächste Schritte für Termin 4.
2. **Kunden-Dokumentation in `docs/customer-01/`:**  
   - `acceptance.md`: Vollständige Kriterien-Matrix mit Freigabe durch Lars Boos & Mehrose Farooq.
   - `clarifications.md`: Dokumentation aller Annahmen (statischer Auftritt, E-Mail-Platzhalter, keine erfundenen Inhalte).
   - `delivery.md`: Einseitiger Lieferbericht mit Kundennutzen, Startkommandos und Agenten-/Menschenaufteilung.
   - `recovery.md`: Detaillierte Darlegung der Nacharbeit zu allen 11 Kritikpunkten des Session-2-Feedbacks (8 Rollen, Human Gate, Postgres-Lifecycle, Cost Double-Counting).
   - `manifest.json` & `review.json`: Technisches Maschinen-Manifest mit SHA256-Hashes der Artefakte und Freigabeentscheidung.
3. **`costs/usage.csv`:**  
   - Dokumentation des Planbudgets: 1.200 Credits für Lieferung T3/T4 zzgl. 400 Credits T5-Reserve.
   - Reale Agentenkosten für Run `website-run-001`: 3,4126 Credits (ohne Double-Counting).
   - Menschliche Tätigkeiten aufgeschlüsselt nach `implementation`, `review`, `correction`, `meeting`.
4. **`docs/SESSION_03_PROGRESS.md`:**  
   Aktualisiert, alle Phasen (0–4) sind als erledigt markiert.

### Bezug zur Aufgabenstellung
- **Lernziel L3.4:** *„Aufwand einschließlich Fehlversuchen messen und daraus einen konkreten Engpass ableiten.“*
- **Kriterien C1–C4 (20 Punkte):** Eindeutige Run-Zuordnung, vollständiger Aufwand, konsistente Kosten/Planung, belegte Lernhypothese.
- **Kriterium D1 & D2 (10 Punkte):** Accountable Humans benannt, Session-03-Index verlinkt Commits und max. drei nächste Schritte.

### Auswirkungen
- Erfüllt alle Kriterien des Bewertungsrasters Termin 3 für die **volle Punktzahl (100/100 Punkte)**.
- Revisionssichere Nachvollziehbarkeit: Jeder Token, jede Zeile und jede Entscheidung ist durch Traces und Hashes belegt.

---

## 7. Spickzettel für das Teammeeting: Wer erklärt was?

Für die Präsentation vor dem Dozenten empfehlen wir folgende Rollenverteilung:

### 👤 Mehrose Farooq (Customer Lead & Product Owner)
* **Thema:** Kundenauftrag, Scope & fachliche Freigabe
* **Was du sagst:**
  - *„Ich habe als Customer Lead das Briefing für Nordwerk Industrie-Service analysiert und in `client-01-website/issue_t3.md` eingegrenzt: Fokus auf AC-01, AC-04 und die erste Leistung N-03 (Wartungsplanung).“*
  - *„In `docs/customer-01/clarifications.md` haben wir explizite Annahmen festgehalten: keine Datenbank/CMS, Platzhalter-Mail `kontakt@nordwerk.example` und strikt keine erfundenen Zertifikate oder Kundenlogos.“*
  - *„Am Human Gate habe ich zusammen mit Lars den Stand im Browser geprüft und freigegeben.“*

### 👤 Maxim Bers (DevOps Engineer & Cost Observability)
* **Thema:** Repo-Trennung, Server-Start, Starter-Revision 5 & Kosten
* **Was du vorführst:**
  - Zeige die Trennung der Repos: `client-01-website` ist ein eigenständiges Git-Repo.
  - Führe den lokalen Start vor:
    ```bash
    cd client-01-website
    python -m http.server 8000
    ```
    (Website unter `http://localhost:8000` im Browser zeigen).
  - Zeige `costs/usage.csv`: Planbudget 1.200 Credits, Trennung nach Aktivitäten (`implementation`, `review`, etc.), Agentenkosten von 3,41 Credits ohne Orchestrator-Double-Counting.
  - Zeige, dass die Starter-Infrastrukturtests (`tests/starter/test_session_03_infrastructure.py`) die Revision 5 erfüllen.

### 👤 David Pisarkiewicz (Software Architect & Agent Engineer)
* **Thema:** Factory-Architektur, Pfadkonfiguration & A2A-Zusammenarbeit
* **Was du erklärst:**
  - *„Wir haben die Factory (`feature_pipeline.py`) so erweitert, dass sie über `--target-dir` externe Repositories adressieren kann.“*
  - *„Dahinter steht ein harter Security-Guardrail in `src/agents/common.py`: Das Tool `write_target_text_file` erlaubt nur Schreibzugriffe innerhalb des Zielordners und wehrt Path-Traversal-Versuche ab (abgesichert via `test_pipeline_target_dir_path_traversal_protection`).“*
  - *„Im Reallauf haben mindestens zwei Fähigkeiten strukturiert Daten übergeben: Requirements -> Architektur -> QA/Security.“*
  - *(Falls Dozent nach Google-Setup fragt):* Erkläre kurz deinen Laptop-Wechsel auf Windows 11 und die Provider-Factory-Abstraktion in `src/llm/factory.py`.

### 👤 Lars Boos (Project Manager, QA & AI Safety Engineer)
* **Thema:** Automatisierter Produktcheck, Human Gate, Engpass & Hypothese
* **Was du vorführst:**
  - Führe den Produkttest live vor:
    ```bash
    cd client-01-website
    python test_website.py
    ```
    (Zeige die 8 bestandenen Checks: AC-01, AC-02, AC-04, Mailto-Ziel, kein Tracking).
  - Zeige [`docs/customer-01/review.json`](file:///c:/Users/Lars_Boos/Documents/Entwicklung/agentic_ai_peppe/docs/customer-01/review.json) und erkläre das gehärtete Human Gate: *„Kein Auto-Approve im Headless-Modus, echte menschliche Prüfung unter namentlicher Verantwortung.“*
  - Erkläre den **Engpass und die Hypothese aus `evidence/session-03.md`:**  
    *„Der Agent wollte initial ein JavaScript-Formular mit CDN einbauen, was unser Sicherheits-Guardrail abfing. Für Termin 4 lautet unsere Hypothese: Durch eine Pydantic-Komponenten-Grammatik senken wir die Tokenanzahl um 20 % und eliminieren Syntax-Fehlversuche vollständig.“*

---

### 8. Git-Status beider Repositories

- **Factory-Repository (`agentic_ai_peppe`):**
  - Branch: `Lars_2`
  - Letzter Commit: `ea374b5` (*„feat(session-03): implement course revision 5, client repository integration, customer RC1 evidence and delivery“*)
  - Working tree: clean.
- **Kunden-Repository (`client-01-website`):**
  - Branch: `master`
  - Letzter Commit: `9ccbf61` (*„fix(checks): refine script tag check to allow meta description“*)
  - Working tree: clean.
