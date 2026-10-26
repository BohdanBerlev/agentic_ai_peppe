# Evidence Session 3 – Erster Kundenauftrag durch die Software Factory

**Team:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Datum:** 26. Oktober 2026  
**Kunde:** Nordwerk Industrie-Service (Hamburg)  
**Auftrag:** `TASK-001` (`project_id: "client-01"`) – Initialer Release Candidate 1 Webauftritt (Termin 3 Scope)

---

## 1. Repositories und Commit-Stände (L3.1 / A1)

Die Trennung zwischen Factory und Kundenprodukt ist technisch vollständig vollzogen:

| Repository | GitHub-URL / Lokaler Pfad | Eingabe-Commit (vor Lauf) | Ergebnis-Commit (nach Lauf) |
|---|---|---|---|
| **Factory-Repository** | `https://github.com/BohdanBerlev/agentic_ai_peppe` (`.`) | `7351867` | Aktueller `HEAD` auf `main` |
| **Kundenprodukt-Repository** | `https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website` (`client-01-website`) | `cbbf7a9` (Starter-Placeholder in `index.html`) | `c952e98` (Vom Agenten implementierte `index.html` + abgestimmte `styles.css`) |

- **Konfiguration & Adressierung:** Die Factory adressiert das externe Produkt-Repository modular über `--target-dir client-01-website --project-id client-01 --task-id TASK-001`.
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
- **Provider & Modell:** `google` / `gemini-3.8-flash` (8 reale LLM-Aufrufe, 0 Mocks)
- **Nachgewiesene Zusammenarbeit der 8 Rollen am echten Produktartefakt (`client-01-website/index.html`):**
  1. **`product_owner_requirements`** (`run_id: 0df93389-29be-49bf-a8ff-7b9e0fde1f14`): Liest `issue_t3.md` und `index.html` im `client-01-website`-Checkout und extrahiert 9 strukturierte Akzeptanzkriterien (`RequirementsReport`).
  2. **`project_manager`** (`run_id: 5bd39ce0-3619-4ef4-b274-82ffdc51cd28`): Erzeugt aus dem `RequirementsReport` 5 strukturierte Work Packages (`WP-1` bis `WP-5`) inkl. Abhängigkeiten und Lieferrisiken (`ProjectPlanReport`).
  3. **`agent_engineer`** (`run_id: a2e0de14-58ea-4ec8-8fa1-a8c48192a0f9`): Spezifiziert die Graph-Knoten und Tool-Verträge (`AgentDesignReport`).
  4. **`software_architect`** (`run_id: a45845d6-aaad-47fe-a122-fc5d77ad934d`): Prüft das initiale Placeholder-Skeleton (`cbbf7a9`) und meldet fehlende semantische HTML5-Landmarken (`changes_requested`).
  5. **`backend_api_engineer`** (`run_id: 4e03fcfb-0d12-4a71-bd67-13e3e20a622a`): Übernimmt die Berichte von PO, PM und Architect und **schreibt per `write_repository_text_file` die vollständige semantische `client-01-website/index.html`** (sichtbar im Git-Diff `cbbf7a9..c952e98`).
  6. **`qa_test_engineer`** (`run_id: aa24b936-9994-40a7-b14e-2f4f8c12a705`): Führt per `execute_repository_pytest` das reale Prüfskript `python test_website.py` im Kunden-Checkout aus (`tests_passed: true`, `exit_code: 0`).
  7. **`ai_safety_security_engineer`** (`run_id: 1e62f54e-686a-4900-b6bd-132ccaa77b88`): Prüft die neu geschriebene `index.html` auf Script-Injections, externe Abhängigkeiten und Secrets (`approved`).
  8. **`integration_engineer`** (`run_id: 1ef37bd8-ef39-4032-9618-457d82745189`): Prüft alle Upstream-Handover (`PO->PM`, `PM->SA`, `SA->Implementation`, `Implementation->QA`, `Implementation->Security`) und bestätigt, dass die anfänglichen Architektur-Befunde durch den Backend-Agenten vollständig aufgelöst wurden (`approved`).

---

## 3. Geprüfte Tageskriterien & Produktprüfung (L3.3 / B1–B6)

| Kriterium | Beschreibung | Prüfmethode | Status |
|---|---|---|---|
| **AC-01 (B1)** | Firmenname (`Nordwerk Industrie-Service`) & Hauptaussage (`Praktische Unterstützung für Ihren technischen Betrieb.`) | `test_website.py` + Sichtprüfung Browser (`http://localhost:8000`) | **Bestanden** |
| **AC-02 Teil (B2)** | Erste Leistung Wartungsplanung (`Wartungsplanung: Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe.`) | `test_website.py` + Sichtprüfung Browser | **Bestanden** |
| **AC-04 (B3)** | Kontaktlink `mailto:kontakt@nordwerk.example` beschriftet mit `Anfrage stellen` (`N-08`); Übungshinweis (`Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. Keine realen Angebote oder Kontaktaufnahme.`, `N-09`) im Footer sichtbar | `test_website.py` + Klicktest Mailto im Browser | **Bestanden** |
| **B4** | Eigener automatisierter Produktcheck | `python client-01-website/test_website.py` (`exit_code: 0`) | **Bestanden** |
| **B5** | Unabhängiger Start dokumentiert | [`client-01-website/README.md`](https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website/blob/c952e98/README.md) dokumentiert `python -m http.server 8000` | **Bestanden** |
| **B6** | Kunden-Task ohne erfundene Versprechen | [`client-01-website/issue_t3.md`](https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website/blob/c952e98/issue_t3.md) referenziert exakte ACs und Annahmen (`A-01`, `A-02`) | **Bestanden** |

---

## 4. Menschliches Approval Gate & Eigene Factory-Prüfung (A4 / D1)

- **Accountable Humans:**
  - *Auftrag & Scope:* Mehrose Farooq & Lars Boos
  - *Technische Lieferung & Agenten-Orchestrierung:* David Pisarkiewicz & Maxim Bers
  - *Prüfung (QA) & Sichtprüfung:* David Pisarkiewicz & Lars Boos
  - *Interaktive Gate-Freigabe im Lauf `bf81352d-f7cb-4628-ad10-475cad888f73`:* **David Pisarkiewicz** (`decision: "approved"`, `human_review_seconds: 322.45`, dokumentiert in Trace Zeile 9 und [`docs/customer-01/review.json`](../docs/customer-01/review.json)).
- **Eigene Factory-Tests:**
  - `tests/test_feature_pipeline.py::test_pipeline_addresses_client_target_dir`
  - `tests/test_feature_pipeline.py::test_pipeline_target_dir_path_traversal_protection`
  - `tests/test_work_items_api.py::test_work_items_real_postgres_lifecycle` (gegen echte PostgreSQL-DB)
  - `tests/starter/test_session_03_infrastructure.py`
  - Alle **62 Tests** laufen im Standardlauf (`python -m pytest`) grün durch (JUnit-Bericht: [`evidence/session-03/pytest.xml`](pytest.xml)).

---

## 5. Kosten, Aufwand und Planbudget (L3.4 / C1–C3)

- **Planbudget Lieferung T3/T4:** 1.200 Credits (12 Personenstunden) zzgl. 400 Credits Reserve für T5 (getrennt von den gemeinsamen Factory-Ausbaukosten erfasst in [`costs/usage.csv`](../costs/usage.csv)).
- **Menschlicher Gesamtaufwand Termin 3 (4 Teammitglieder × 5,0 h = 20,0 h = 2.000,0 Credits):**
  - `human_david` (5,0 h = 500 Credits): 2,5 h `implementation`, 1,5 h `review`, 1,0 h `waiting`
  - `human_maxim` (5,0 h = 500 Credits): 3,0 h `implementation`, 1,0 h `review`, 1,0 h `meeting`
  - `human_lars` (5,0 h = 500 Credits): 2,5 h `implementation`, 2,0 h `review`, 0,5 h `correction`
  - `human_mehrose` (5,0 h = 500 Credits): 1,5 h `implementation`, 2,0 h `review`, 1,5 h `correction`
- **Agenten-Kosten Lauf `bf81352d-f7cb-4628-ad10-475cad888f73`:** **30,9069 Credits** (8 reale LLM-Aufrufe über `gemini-3.8-flash`, `2239.7507s` reine Agenten-Laufzeit, `322.45s` menschliche Review-Zeit getrennt ausgewiesen; kein Double-Counting der `workflow_summary`-Zeile).

---

## 6. Konkreter Engpass & Überprüfbare Lernhypothese (C4)

- **Beobachteter Engpass (belegt durch Trace `bf81352d-f7cb-4628-ad10-475cad888f73.jsonl`, Zeilen 4, 5 & 9):**
  Im echten Durchlauf trat ein struktureller Reihenfolge-Engpass auf: Da `architect_agent` (`a45845d6...`, Zeile 4) die Zieldatei `index.html` *vor* dem `backend_agent` (`4e03fcfb...`, Zeile 5) inspiziert, bewertete er das initiale leere Starter-Skeleton (`cbbf7a9`) richtigerweise mit `changes_requested`. Obwohl der `backend_agent` die Datei anschließend vollständig implementierte und `qa_test_engineer` (`exit_code: 0`), `ai_safety_security_engineer` sowie `integration_engineer` alle `approved` meldeten, berechnete `_compute_agent_recommendation` wegen des historischen Pre-Implementation-Architekturstatus am Human Gate `agent_recommendation: "changes_requested"`. Das erforderte `322.45s` manuellen Prüfaufwand am Gate zur Verifikation des Override.
- **Überprüfbare Verbesserungshypothese für Termin 4:**
  *Wenn* wir in `src/workflows/feature_pipeline.py` die Empfehlungslogik (`_compute_agent_recommendation`) so anpassen, dass ein Pre-Implementation-`changes_requested` des `architect_agent` als aufgelöst gilt, sobald `backend_agent`, `qa_test_engineer` (`exit_code == 0`) und `integration_engineer` nach der Implementierung alle `approved` liefern (und zusätzlich nach jedem Graph-Knoten eine Fortschrittszeile in der Konsole ausgeben), *dann* sinkt die Rate falscher `changes_requested`-Empfehlungen nach erfolgreicher Code-Generierung auf **0 %** und die menschliche Gate-Prüfzeit (`human_review_seconds`) reduziert sich in Termin 4 von **322,45 s auf unter 120 s**.

---

## 7. Höchstens drei nächste Schritte für Termin 4 (D2)

1. **Ausbau der Leistungsbereiche & Sektionen (AC-02, AC-03, AC-05):** Integration von `N-04` (Ersatzteilkoordination), `N-05` (Betriebsdokumentation), `N-06` (Zielgruppen) und `N-07` (Arbeitsweise) inkl. Navigations-Sprungmarken durch die Pipeline.
2. **Pipeline-Empfehlungslogik & Fortschritts-Logging (Hypothese C4):** Anpassung von `_compute_agent_recommendation` in `feature_pipeline.py` nach erfolgreicher Backend-Implementierung sowie Konsolen-Fortschrittsanzeige pro Agenten-Schritt.
3. **Multi-File-Support im Backend-Agenten & Responsive-Test (AC-06):** Erweiterung von `my_backend_agent` zur koordinierten Bearbeitung von `index.html` und `styles.css` in einem Lauf sowie automatisierter Viewport-Check (375 px / 1280 px).
