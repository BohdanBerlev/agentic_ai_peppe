# Evidence Session 3 – Erster Kundenauftrag durch die Software Factory

**Team:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Datum:** 26. Oktober 2026 (Aktualisiert & verifiziert am 31. Oktober 2026)  
**Kunde:** Nordwerk Industrie-Service (Hamburg)  
**Auftrag:** `TASK-001` (`project_id: "client-01"`) – Initialer Release Candidate 1 Webauftritt (Termin 3 Scope)  
**Dokumentarische LLM-Ausnahmegenehmigung:** [`docs/GEMINI_PROVIDER_WAIVER.md`](../docs/GEMINI_PROVIDER_WAIVER.md)  

---

## 1. Repositories und Commit-Stände (L3.1 / A1)

Die Trennung zwischen Factory und Kundenprodukt ist technisch vollständig vollzogen:

| Repository | GitHub-URL / Lokaler Pfad | Eingabe-Commit (vor Lauf) | Ergebnis-Commit (nach Lauf) | Release-Tag / Status |
|---|---|---|---|---|
| **Factory-Repository** | `https://github.com/BohdanBerlev/agentic_ai_peppe` (`.`) | `7351867` | Aktueller `HEAD` auf `main` | Bereitgestellt für Evaluation |
| **Kundenprodukt-Repository** | `client-01-website` | `a93442b` (Initialer RC1-Stand) | `5e46bcb` (Validierter Stand mit UTF-8-Terminal-Kompatibilität) | `v0.1.0-t3` |

- **Verifizierte SHA-256 Prüfsummen (Release Candidate v0.1.0-t3):**
  - `client-01-website/index.html`: `4bfc474a5412158e9d5d4b5c9365a758436f60342a4cad963aaa5f3e18e155e2`
  - `client-01-website/styles.css`: `24822a903d848bcffb61cf68a943dd179ce4d486720f1f7c7f5ef6ccaad9f8f8`
  - `client-01-website/test_website.py`: `5103a20e5d758f180ac0707d5695b8e472bea8262a7337edd7d3eaeecb83ff15`
- **Konfiguration & Adressierung:** Die Factory adressiert das Produkt-Repository modular über `--target-dir client-01-website --project-id client-01 --task-id TASK-001`.
- **Unabhängiger Start ohne Factory (B5):** Das Produkt läuft vollständig isoliert ohne Factory, ohne DB und ohne LLM:
  ```powershell
  python -m http.server 8000 --directory client-01-website
  python client-01-website/test_website.py
  ```

---

## 2. Realer Factory-Durchlauf & Agenten-Kooperation (L3.2 / A2, A3)

- **Workflow-ID:** `bf81352d-f7cb-4628-ad10-475cad888f73`
- **Summary Run-ID:** `a1fefdef-eb4e-4c75-bb0b-41674d060079`
- **Trace-Datei:** [`evidence/session-03/bf81352d-f7cb-4628-ad10-475cad888f73.jsonl`](bf81352d-f7cb-4628-ad10-475cad888f73.jsonl)
- **Provider & Modell:** `google` / `gemini-3.8-flash` (8 reale LLM-Aufrufe, 0 Mocks; genehmigt via [`docs/GEMINI_PROVIDER_WAIVER.md`](../docs/GEMINI_PROVIDER_WAIVER.md))
- **Nachgewiesene Zusammenarbeit der 8 Rollen am echten Produktartefakt (`client-01-website/index.html`):**
  1. **`product_owner_requirements`** (`run_id: 0df93389-29be-49bf-a8ff-7b9e0fde1f14`): Liest `issue_t3.md` und `index.html` im `client-01-website`-Checkout und extrahiert 9 strukturierte Akzeptanzkriterien (`RequirementsReport`).
  2. **`project_manager`** (`run_id: 5bd39ce0-3619-4ef4-b274-82ffdc51cd28`): Erzeugt aus dem `RequirementsReport` 5 strukturierte Work Packages (`WP-1` bis `WP-5`) inkl. Abhängigkeiten und Lieferrisiken (`ProjectPlanReport`).
  3. **`agent_engineer`** (`run_id: a2e0de14-58ea-4ec8-8fa1-a8c48192a0f9`): Spezifiziert die Graph-Knoten und Tool-Verträge (`AgentDesignReport`).
  4. **`software_architect`** (`run_id: a45845d6-aaad-47fe-a122-fc5d77ad934d`): Prüft das initiale Skeleton und meldet fehlende semantische HTML5-Landmarken (`changes_requested`).
  5. **`backend_api_engineer`** (`run_id: 4e03fcfb-0d12-4a71-bd67-13e3e20a622a`): Übernimmt die Berichte von PO, PM und Architect und schreibt per `write_repository_text_file` die vollständige semantische `client-01-website/index.html`.
  6. **`qa_test_engineer`** (`run_id: aa24b936-9994-40a7-b14e-2f4f8c12a705`): Führt per `execute_repository_pytest` das reale Prüfskript `python test_website.py` im Kunden-Checkout aus (`tests_passed: true`, `exit_code: 0`, 8/8 Tests passed).
  7. **`ai_safety_security_engineer`** (`run_id: 1e62f54e-686a-4900-b6bd-132ccaa77b88`): Prüft die neu geschriebene `index.html` auf Script-Injections, externe Abhängigkeiten und Secrets (`approved`).
  8. **`integration_engineer`** (`run_id: 1ef37bd8-ef39-4032-9618-457d82745189`): Prüft alle Upstream-Handover (`PO->PM`, `PM->SA`, `SA->Implementation`, `Implementation->QA`, `Implementation->Security`) und bestätigt, dass die anfänglichen Architektur-Befunde durch den Backend-Agenten vollständig aufgelöst wurden (`approved`).

---

## 3. Geprüfte Tageskriterien & Produktprüfung (L3.3 / B1–B6)

| Kriterium | Beschreibung | Prüfmethode | Status |
|---|---|---|---|
| **AC-01 (B1)** | Firmenname (`Nordwerk Industrie-Service`) & Hauptaussage (`Praktische Unterstützung für Ihren technischen Betrieb.`) | `test_website.py` + Sichtprüfung Browser (`http://localhost:8000`) | **Bestanden** |
| **AC-02 Teil (B2)** | Erste Leistung Wartungsplanung (`Wartungsplanung: Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe.`) | `test_website.py` + Sichtprüfung Browser | **Bestanden** |
| **AC-04 (B3)** | Kontaktlink `mailto:kontakt@nordwerk.example` beschriftet mit `Anfrage stellen` (`N-08`); Übungshinweis (`N-09`) im Footer sichtbar | `test_website.py` + Klicktest Mailto im Browser | **Bestanden** |
| **B4** | Eigener automatisierter Produktcheck (inkl. PHP-RCE-Guardrail `verify_no_php_attack_surface` gegen `CVE-2026-109618` / `CVE-2026-109619`) | `python client-01-website/test_website.py` (8/8 Checks bestanden, Exit-Code 0) | **Bestanden** |
| **B5** | Unabhängiger Start dokumentiert & Release getaggt | `python -m http.server 8000`, Tag `v0.1.0-t3` | **Bestanden** |
| **B6** | Kunden-Task & Sicherheits-Klärung (`CVE-2026-109618` / `CVE-2026-109619`, PHP `>= 8.2.35`) ohne erfundene Versprechen | [`client-01-website/issue_t3.md`](../client-01-website/issue_t3.md) & [`docs/customer-01/clarifications.md`](../docs/customer-01/clarifications.md) | **Bestanden** |

---

## 4. Menschliches Approval Gate & Eigene Factory-Prüfung (A4 / D1)

- **Accountable Humans:**
  - *Auftrag & Scope:* Mehrose Farooq & Lars Boos
  - *Technische Lieferung & Agenten-Orchestrierung:* David Pisarkiewicz & Maxim Bers
  - *Prüfung (QA) & Sichtprüfung:* David Pisarkiewicz & Lars Boos
  - *Interaktive Gate-Freigabe im Lauf `bf81352d-f7cb-4628-ad10-475cad888f73`:* **David Pisarkiewicz** (`decision: "approved"`, `human_review_seconds: 322.45`, dokumentiert in Trace Zeile 9 und [`docs/customer-01/review.json`](../docs/customer-01/review.json)).
- **Härtung der Tool-Sicherheit (Behebung Feedback Punkt 2):**
  - Backend-Agent nutzt nun zentral `write_target_text_file` mit Path-Traversal- und striktem `.git`-Schreibschutz.
  - Testabdeckung durch `tests/test_backend_agent.py::test_write_repository_text_file_git_protection` und `test_write_repository_text_file_target_dir_git_protection`.
- **Eigene Factory-Tests & Status (Behebung Feedback Punkt 3):**
  - Standalone-Testsuite: `python -m pytest tests/`
  - Befehl: `python -m pytest --junitxml=evidence/session-03/pytest.xml -v`
  - Ergebnis: **67 passed, 2 skipped** (JUnit-Report unter [`evidence/session-03/pytest.xml`](pytest.xml)).
  - *Hinweis zu den 2 übersprungenen Tests:* Die Tests für Live-PostgreSQL (`test_work_items_real_postgres_lifecycle` und Starter-Persistenz) erfordern einen lokal aktiven PostgreSQL-Dienst (`docker compose up -d db`). Ohne laufende Datenbank werden sie planmäßig via `pytest.skip` übersprungen und nicht als falsches "passed" deklariert.

---

## 5. Kosten, Aufwand und Planbudget (L3.4 / C1–C3)

- **Planbudget Lieferung T3/T4:** 1.200 Credits (12 Personenstunden) zzgl. 400 Credits Reserve für T5.
- **Saubere Kostentrennung in [`costs/usage.csv`](../costs/usage.csv) (Behebung Feedback Punkt 3):**
  - **Kundenlieferung Termin 3 (`TASK-001`):** **1.250,0 Credits** menschliche Arbeitszeit (12,5 h)
    - `human_david` (3,5 h = 350 Credits): Vorbereitung & Live-Run (1,0 h), Human Gate Review & CSS (1,5 h), Terminal-Wartezeit (1,0 h)
    - `human_lars` (4,0 h = 400 Credits): Testsuite `test_website.py` (1,5 h), Sichtprüfung Browser (2,0 h), Hash- & Commit-Abgleich (0,5 h)
    - `human_mehrose` (5,0 h = 500 Credits): Kundenbriefing & Issue (1,5 h), PO-Abnahme & Clarifications (2,0 h), Abnahmeberichte (1,5 h)
    - *Planabweichung Kundenlieferung:* +50 Credits (+4,2 %) gegenüber 1.200 Credits Planbudget; durch die T5-Reserve (400 Credits) vollständig gedeckt.
  - **Factory-Entwicklung Termin 3 (`FACTORY-DEV`):** **750,0 Credits** (7,5 h getrennt von der Kundenlieferung erfasst)
    - `human_david` (1,5 h = 150 Credits): `target_dir`-Isolation und Backend-Agent-Anbindung
    - `human_maxim` (5,0 h = 500 Credits): Backend-Agent TDD-Loop, PostgreSQL-Tests, Sprint-Planung & Budgetierung
    - `human_lars` (1,0 h = 100 Credits): Factory-Tests und Evidenz-Struktur
  - **Agenten-Kosten Lauf `bf81352d-f7cb-4628-ad10-475cad888f73`:** **30,9069 Credits** (8 reale LLM-Aufrufe über `gemini-3.8-flash`, `2239.7507s` reine Agenten-Laufzeit, `322.45s` menschliche Review-Zeit getrennt ausgewiesen; kein Double-Counting).

---

## 6. Konkreter Engpass & Überprüfbare Lernhypothese (C4)

- **Beobachteter Engpass (belegt durch Trace `bf81352d-f7cb-4628-ad10-475cad888f73.jsonl`, Zeilen 4, 5 & 9):**
  Im echten Durchlauf trat ein struktureller Reihenfolge-Engpass auf: Da `architect_agent` die Zieldatei `index.html` *vor* dem `backend_agent` inspiziert, bewertete er das initiale Skeleton mit `changes_requested`. Obwohl der `backend_agent` die Datei anschließend vollständig implementierte und `qa_test_engineer` (`exit_code: 0`), `ai_safety_security_engineer` sowie `integration_engineer` alle `approved` meldeten, berechnete `_compute_agent_recommendation` wegen des historischen Pre-Implementation-Architekturstatus am Human Gate `agent_recommendation: "changes_requested"`. Das erforderte `322.45s` manuellen Prüfaufwand am Gate zur Verifikation des Override.
- **Überprüfbare Verbesserungshypothese für Termin 4:**
  *Wenn* wir in `src/workflows/feature_pipeline.py` die Empfehlungslogik (`_compute_agent_recommendation`) so anpassen, dass ein Pre-Implementation-`changes_requested` des `architect_agent` als aufgelöst gilt, sobald `backend_agent`, `qa_test_engineer` (`exit_code == 0`) und `integration_engineer` nach der Implementierung alle `approved` liefern, *dann* sinkt die Rate falscher `changes_requested`-Empfehlungen nach erfolgreicher Code-Generierung auf **0 %** und die menschliche Gate-Prüfzeit (`human_review_seconds`) reduziert sich in Termin 4 von **322,45 s auf unter 120 s**.

---

## 7. Höchstens drei nächste Schritte für Termin 4 (D2)

1. **Ausbau der Leistungsbereiche & Sektionen (AC-02, AC-03, AC-05):** Integration von `N-04` (Ersatzteilkoordination), `N-05` (Betriebsdokumentation), `N-06` (Zielgruppen) und `N-07` (Arbeitsweise) inkl. Navigations-Sprungmarken durch die Pipeline.
2. **Pipeline-Empfehlungslogik & Fortschritts-Logging (Hypothese C4):** Anpassung von `_compute_agent_recommendation` in `feature_pipeline.py` nach erfolgreicher Backend-Implementierung sowie Konsolen-Fortschrittsanzeige pro Agenten-Schritt.
3. **Kontrollierte Fehlersituation & R-01 Baseline:** Durchführung des Negativ-/Positiv-Tests am Qualitätsgate sowie Sicherung der isolierten Referenzmessung R-01 auf `R-BASE` vor Beginn der T5-Optimierungen.
