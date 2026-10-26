# CUST-001 / TASK-001 – Delivery / Lieferbericht (Termin 3)

**Kunde:** Nordwerk Industrie-Service (Hamburg)  
**Auftrag:** Kundenprojekt 01 (`TASK-001`, `project_id: "client-01"`) – Initialer Webauftritt Release Candidate 1  
**Lieferdatum:** 26. Oktober 2026  
**Erstellt durch:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)

---

### 1. Kundennutzen & Scope
Nordwerk Industrie-Service erhält einen schnellen, modernen und barrierearmen Webauftritt (Release Candidate 1), der potenziellen B2B-Kunden sofort Identität (`N-01`), Hauptaussage (`N-02`) und die erste Kernleistung der Wartungsplanung (`N-03`) vermittelt. Über zwei standardisierte `mailto:kontakt@nordwerk.example`-Buttons (`N-08`: „Anfrage stellen“) können Interessenten direkt Anfragen stellen, ohne dass ein wartungsintensives Backend oder externe Tracker erforderlich sind.

### 2. Commit-Stände & Nachvollziehbarkeit (Vorher/Nachher-Diff)
- **Produkt-Repository:** `https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website`
  - **Eingabe-Commit vor Agenten-Lauf:** `cbbf7a9` (enthielt das leere HTML-Starter-Skeleton in `index.html` und die Spezifikation `issue_t3.md`)
  - **Geprüfter Ergebnis-Commit nach Agenten-Lauf:** `c952e98` (vom `backend_agent` generierte `index.html` + abgestimmte `styles.css`)
- **Factory-Repository (`agentic_ai_peppe`):**
  - **Factory-Commit beim Lauf:** `7351867`
  - **Liefer-/Evidenz-Commit:** Nachgelagerter Abgabe-Commit auf `main`.
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
  - Ergebnis: **`PASSED` (Exit-Code 0, 0 Fehler)**.
  - Geprüft: `N-01`, `N-02`, `N-03`, `N-08` (`mailto:kontakt@nordwerk.example`), `N-09` (Lehrprojekt-Hinweis), semantische HTML5-Elemente (`<header>`, `<nav>`, `<main>`, `<h1>`, `<footer>`), `lang="de"`, `:focus-visible`, Abwesenheit externer URLs/Tracker/Zertifikate **sowie `verify_no_php_attack_surface()` (0 `.php`/`.phtml`/`.phar`-Dateien, 0 `<?php`-Tags, 0 `.php`-Formular-Endpunkte)**.
- **PHP-Sicherheitsberatung & Factory-Guardrail (ENISA-Mitteilung vom 21.10.2026 zu `CVE-2026-109618` & `CVE-2026-109619`):**
  - Im `qa_security_agent.py` (`detect_php_security_risks`) und in `tests/test_qa_security_agent.py::test_security_audit_flags_php_rce_surface_cve_2026_109618` ist ein harter Guardrail aktiv, der jegliche PHP-Skripte oder `.php`-Formular-Actions sofort mit `changes_requested` abweist.
  - Detaillierte Einschätzung zum alten PHP-8.2-Auftritt des Kunden (erforderlicher Patchstand `>= PHP 8.2.35`, Hoster-Rückfragen, Isolation vs. statischer Ersatz, ehrliche Abgrenzung „statisch ≠ wartungsfrei“) ist in [`docs/customer-01/clarifications.md`](clarifications.md) dokumentiert.
- **Factory-Tests (`pytest`):**
  - Befehl: `python -m pytest --junitxml=evidence/session-03/pytest.xml -v`
  - Ergebnis: **67 passed, 2 skipped** (JUnit-Report unter `evidence/session-03/pytest.xml`; eigener PostgreSQL-Persistenztest `test_work_items_real_postgres_lifecycle` gegen echte PostgreSQL-DB bestanden).

### 5. Menschliche vs. Agenten-Arbeit
- **Agenten-Beitrag (8 Rollen im Lauf `bf81352d-f7cb-4628-ad10-475cad888f73`):**
  - `product_owner_requirements`, `project_manager` & `agent_engineer`: Extraktion der 9 Akzeptanzkriterien aus `issue_t3.md` und Strukturierung in 5 Work Packages (`WP-1` bis `WP-5`).
  - `software_architect`: Inspektion des initialen Placeholder-Skeletons (`cbbf7a9`) und Feststellung der fehlenden semantischen Landmarken (`changes_requested`).
  - `backend_api_engineer` (`backend_agent.py`): Vollständige Generierung und Schreiben der semantischen `client-01-website/index.html` mittels `write_repository_text_file`.
  - `qa_test_engineer`, `ai_safety_security_engineer` & `integration_engineer`: Reale Ausführung von `python test_website.py` (`exit_code: 0`), Sicherheitsprüfung und A2A-Handover-Validierung (`approved`).
- **Menschlicher Beitrag:**
  - *Architektur & Factory-Erweiterung:* David Pisarkiewicz & Maxim Bers (`target_dir`-Isolation, Integration des `backend_agent`, Course Revision 5).
  - *Styling & Produkttest-Setup:* David Pisarkiewicz, Lars Boos & Mehrose Farooq (Abstimmung der CSS-Selektoren in `styles.css` auf die vom Backend-Agenten generierten Klassen, `test_website.py`, Sichtprüfung im Browser).

### 6. Freigabeentscheidung am Human Gate (A4 / D1)
- **Reviewer:** `David Pisarkiewicz` (Accountable Human)
- **Entscheidung:** **`approved`** am 2026-10-26 12:01:01 (`human_review_seconds: 322.45`)
- **Dokumentierte Begründung im Trace:** Der `architect_agent` lief in der Pipeline-Reihenfolge vor dem `backend_agent` und bewertete daher noch den leeren Placeholder (`changes_requested`). Da der `backend_agent` danach alle bemängelten Punkte in `index.html` behoben hat und QA (`exit_code: 0`), Security und Integration auf `approved` standen, wurde der Release-Stand nach menschlicher Prüfung freigegeben.

### 7. Kosten & Aufwand (C2 / C3)
- **Planbudget Lieferung T3/T4:** 1.200 Credits + 400 Credits Reserve für T5 (getrennt von der allgemeinen Factory-Weiterentwicklung).
- **Menschlicher Aufwand Termin 3 (4 Mitglieder à 5,0 h = 20,0 h = 2.000,0 Credits in `costs/usage.csv`):**
  - Aufgeteilt in `implementation` (9,5 h), `review` (6,5 h), `correction` (2,0 h), `waiting` (1,0 h) und `meeting` (1,0 h).
- **Inkrementelle Agenten-Kosten Lauf `bf81352d-f7cb-4628-ad10-475cad888f73`:** **30,9069 Credits** (8 reale LLM-Calls über `gemini-3.8-flash`, 2.239,75 s Agenten-Laufzeit, 322,45 s menschliche Reviewzeit getrennt ausgewiesen; kein Double-Counting).

### 8. Beobachteter Engpass & Überprüfbare Verbesserungshypothese für T4 (C4)
- **Beobachteter Engpass im echten Lauf (`bf81352d-f7cb-4628-ad10-475cad888f73`):**
  1. Weil der `architect_agent` (`run_id: a45845d6...`) in der Pipeline *vor* dem `backend_agent` (`run_id: 4e03fcfb...`) ausgeführt wird, prüft er den noch unfertigen Eingabestand (`cbbf7a9`) und meldet `changes_requested`, was die aggregierte `agent_recommendation` am Human Gate trotz erfolgreicher Implementierung und grünem QA-Test (`exit_code: 0`) auf `changes_requested` zieht.
  2. Zudem fehlte während der 37-minütigen Gesamtlaufzeit (`2239.75s` über 8 Gemini-API-Calls mit Rate-Limit-Backoff) eine Live-Fortschrittsanzeige im Terminal, welcher Pipeline-Schritt gerade aktiv ist.
- **Überprüfbare Hypothese für Termin 4:**
  *Wenn* wir in `feature_pipeline.py` (a) bei aktivem `backend_agent` für die finale `agent_recommendation` den Post-Implementation-Status (`implementation`, `qa_security`, `security_audit`, `integration`) höher gewichten als den Pre-Implementation-Architektur-Check und (b) nach jedem Knoten einen Fortschritts-Log ausgeben, *dann* entfällt der False-Negative-Status von `agent_recommendation` bei Neu-Implementierungen zu **100 %** und die menschliche Warte-/Review-Unsicherheit (`waiting` / `human_review_seconds`) sinkt in Termin 4 von `322,45 s` auf unter **120 s**.
