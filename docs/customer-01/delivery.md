# CUST-001 / TASK-001 – Delivery / Lieferbericht (Termin 3)

**Kunde:** Nordwerk Industrie-Service (Hamburg)  
**Auftrag:** Kundenprojekt 01 (`TASK-001`, `project_id: "client-01"`) – Initialer Webauftritt Release Candidate 1  
**Lieferdatum:** 26. Oktober 2026 (Aktualisiert am 31. Oktober 2026)  
**Erstellt durch:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Ausnahmegenehmigung LLM-Provider:** [`docs/GEMINI_PROVIDER_WAIVER.md`](../GEMINI_PROVIDER_WAIVER.md)  

---

### 1. Kundennutzen & Scope
Nordwerk Industrie-Service erhält einen schnellen, modernen und barrierearmen Webauftritt (Release Candidate 1), der potenziellen B2B-Kunden sofort Identität (`N-01`), Hauptaussage (`N-02`) und die erste Kernleistung der Wartungsplanung (`N-03`) vermittelt. Über standardisierte `mailto:kontakt@nordwerk.example`-Buttons (`N-08`: „Anfrage stellen“) können Interessenten direkt Anfragen stellen, ohne dass ein wartungsintensives Backend oder externe Tracker erforderlich sind.

### 2. Commit-Stände, Hashes & Nachvollziehbarkeit
- **Produkt-Repository (`client-01-website`):**
  - **Eingabe-Commit vor Agenten-Lauf:** `a93442b` (enthielt das initiale HTML-Skeleton und Spezifikation `issue_t3.md`)
  - **Geprüfter Ergebnis-Commit nach Agenten-Lauf & UTF-8-Härtung:** `5e46bcb`
  - **Release-Tag:** `v0.1.0-t3`
  - **Verifizierte SHA-256 Prüfsummen:**
    - `client-01-website/index.html`: `4bfc474a5412158e9d5d4b5c9365a758436f60342a4cad963aaa5f3e18e155e2`
    - `client-01-website/styles.css`: `24822a903d848bcffb61cf68a943dd179ce4d486720f1f7c7f5ef6ccaad9f8f8`
    - `client-01-website/test_website.py`: `5103a20e5d758f180ac0707d5695b8e472bea8262a7337edd7d3eaeecb83ff15`
- **Factory-Repository (`agentic_ai_peppe`):**
  - **Factory-Commit beim Lauf:** `7351867`
  - **Liefer-/Evidenz-Commit:** Auf `main`.
- **Workflow & Run-IDs:**
  - **Workflow-ID:** `bf81352d-f7cb-4628-ad10-475cad888f73`
  - **Trace-Datei:** [`evidence/session-03/bf81352d-f7cb-4628-ad10-475cad888f73.jsonl`](../../evidence/session-03/bf81352d-f7cb-4628-ad10-475cad888f73.jsonl)
  - **Backend-Agent Schreib-Run-ID:** `4e03fcfb-0d12-4a71-bd67-13e3e20a622a` (`tools: ["read_repository_text_file", "write_repository_text_file"]`)
  - **QA-Agent Test-Run-ID:** `aa24b936-9994-40a7-b14e-2f4f8c12a705` (`tools: ["read_repository_text_file", "execute_repository_pytest"]`, `exit_code: 0`)

### 3. Startbefehle & Unabhängige Ausführung (B5)
Das Kundenprodukt benötigt weder Factory-Prozesse noch Datenbanken:
```powershell
# Lokaler Start des Kundenprodukts:
python -m http.server 8000 --directory client-01-website
# URL im Browser: http://localhost:8000

# Isolierter Produktcheck:
python client-01-website/test_website.py
```

### 4. Tests, Prüfungsergebnisse & PHP-Sicherheitsprüfung (`CVE-2026-109618` / `CVE-2026-109619`)
- **Eigener automatisierter Produktcheck (`client-01-website/test_website.py`):**
  - Ergebnis: **`PASSED` (Exit-Code 0, 8/8 Prüfungen bestanden)**.
  - Geprüft: `N-01`, `N-02`, `N-03`, `N-08` (`mailto:kontakt@nordwerk.example`), `N-09` (Lehrprojekt-Hinweis), semantische HTML5-Elemente (`<header>`, `<nav>`, `<main>`, `<h1>`, `<footer>`), `lang="de"`, `:focus-visible`, Abwesenheit externer URLs/Tracker/Zertifikate sowie PHP-Angriffsflächenfreiheit.
- **Factory-Tests (`pytest`):**
  - Befehl: `python -m pytest --junitxml=evidence/session-03/pytest.xml -v`
  - Ergebnis: **67 passed, 2 skipped** (JUnit-Report unter `evidence/session-03/pytest.xml`; die 2 übersprungenen Tests betreffen Live-PostgreSQL-Interaktion, welche einen laufenden Docker-DB-Container via `docker compose up -d db` erfordert).
- **Härtung der Tool-Sicherheit:**
  - Der Backend-Agent nutzt die gehärtete `write_target_text_file`-Logik mit striktem Schutz gegen Path Traversal und Blockierung von Schreibzugriffen auf `.git`-Interna (Regressionstest `test_write_repository_text_file_git_protection` in `tests/test_backend_agent.py`).

### 5. Menschliche vs. Agenten-Arbeit
- **Agenten-Beitrag (8 Rollen im Lauf `bf81352d-f7cb-4628-ad10-475cad888f73`):**
  - `product_owner_requirements`, `project_manager` & `agent_engineer`: Extraktion der 9 Akzeptanzkriterien aus `issue_t3.md` und Strukturierung in 5 Work Packages (`WP-1` bis `WP-5`).
  - `software_architect`: Inspektion des initialen Skeletons und Meldung der fehlenden semantischen Landmarken (`changes_requested`).
  - `backend_api_engineer` (`backend_agent.py`): Vollständige Generierung und Schreiben der semantischen `client-01-website/index.html` mittels `write_repository_text_file`.
  - `qa_test_engineer`, `ai_safety_security_engineer` & `integration_engineer`: Reale Ausführung von `python test_website.py` (`exit_code: 0`), Sicherheitsprüfung und A2A-Handover-Validierung (`approved`).
- **Menschlicher Beitrag (in `costs/usage.csv` strikt getrennt verbucht):**
  - *Factory-Entwicklung (`FACTORY-DEV`):* 750 Credits (7,5 Personenstunden) für target_dir-Isolation, Härtung der Tools, PostgreSQL-API und Test-Infrastruktur.
  - *Kundenlieferung (`TASK-001`):* 1.250 Credits (12,5 Personenstunden) für Briefing, Live-Run, interaktives Gate-Review (322 s), Produkttests und Browser-Abnahme.

### 6. Freigabeentscheidung am Human Gate (A4 / D1)
- **Reviewer:** `David Pisarkiewicz` (Accountable Human)
- **Entscheidung:** **`approved`** am 2026-10-26 12:01:01 (`human_review_seconds: 322.45`)
- **Dokumentierte Begründung im Trace:** Der `architect_agent` lief in der Pipeline-Reihenfolge vor dem `backend_agent` und bewertete daher noch den leeren Placeholder (`changes_requested`). Da der `backend_agent` danach alle bemängelten Punkte in `index.html` behoben hat und QA (`exit_code: 0`), Security und Integration auf `approved` standen, wurde der Release-Stand nach menschlicher Prüfung freigegeben.

### 7. Kosten, Aufwand & Kostentrennung (C2 / C3)
- **Planbudget Lieferung T3/T4:** 1.200 Credits + 400 Credits Reserve für T5.
- **Ist-Kosten Kundenlieferung Termin 3 (`TASK-001`):** **1.250,0 Credits** menschlicher Aufwand (12,5 h) zzgl. **30,9069 Credits** Agentenkosten (8 reale Gemini 3.8 Flash Calls, 2.239,75 s Inferenzzeit). Die Planabweichung beträgt lediglich +50 Credits (+4,2 %) und liegt voll im Toleranzbereich der 400-Credit-Reserve.
- **Ist-Kosten Factory-Entwicklung Termin 3 (`FACTORY-DEV`):** **750,0 Credits** (7,5 h getrennt von der Kundenlieferung verbucht).

### 8. Beobachteter Engpass & Überprüfbare Verbesserungshypothese für T4 (C4)
- **Beobachteter Engpass im echten Lauf (`bf81352d-f7cb-4628-ad10-475cad888f73`):**
  1. Weil der `architect_agent` (`run_id: a45845d6...`) in der Pipeline *vor* dem `backend_agent` (`run_id: 4e03fcfb...`) ausgeführt wird, prüft er den noch unfertigen Eingabestand und meldet `changes_requested`, was die aggregierte `agent_recommendation` am Human Gate trotz erfolgreicher Implementierung und grünem QA-Test (`exit_code: 0`) auf `changes_requested` zieht.
  2. Zudem fehlte während der 37-minütigen Gesamtlaufzeit eine Live-Fortschrittsanzeige im Terminal, welcher Pipeline-Schritt gerade aktiv ist.
- **Überprüfbare Hypothese für Termin 4:**
  *Wenn* wir in `feature_pipeline.py` (a) bei aktivem `backend_agent` für die finale `agent_recommendation` den Post-Implementation-Status (`implementation`, `qa_security`, `security_audit`, `integration`) höher gewichten als den Pre-Implementation-Architektur-Check und (b) nach jedem Knoten einen Fortschritts-Log ausgeben, *dann* entfällt der False-Negative-Status von `agent_recommendation` bei Neu-Implementierungen zu **100 %** und die menschliche Warte-/Review-Unsicherheit (`waiting` / `human_review_seconds`) sinkt in Termin 4 von `322,45 s` auf unter **120 s**.
