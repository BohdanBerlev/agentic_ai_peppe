# Evidence Session 3 – Erster Kundenauftrag durch die Software Factory

**Team:** PepeGroup (Team 3)  
**Datum:** 24. Oktober 2026  
**Kunde:** Nordwerk Industrie-Service (Hamburg)  
**Auftrag:** `CUST-001` – Initialer Release Candidate Webauftritt (Termin 3 Scope)

---

## 1. Repositories und Commit-Stände (L3.1 / A1)

Die Trennung zwischen Factory und Kundenprodukt ist technisch vollständig vollzogen:

| Repository | Zweck | Commit-Stand | Lokaler Pfad |
|---|---|---|---|
| **Factory-Repository** | Multi-Agenten-Orchestrierung, Policies, Tracing, Starter-Infrastruktur | `f3b346f` (vor Lauf) / `3aeb069` (nach Evidenz) | `.` (`agentic_ai_peppe`) |
| **Kundenprodukt-Repository** | Eigenständige statische Website, Produkttests, Kunden-Issue | `a93442b` | `client-01-website` |

- **Konfiguration:** Die Factory adressiert das Produkt-Repo modular über `--target-dir client-01-website --project-id client-01`.
- **Unabhängiger Start (B5):** Das Produkt läuft vollständig ohne Factory, ohne DB und ohne LLM:
  ```bash
  cd client-01-website
  python -m http.server 8000
  ```

---

## 2. Realer Factory-Durchlauf & Agenten-Kooperation (L3.2 / A2, A3)

* **Eindeutige Run-ID:** `website-run-001`
* **Workflow-ID:** `c129e061-f34b-483d-9d7a-cfb395679901`
* **Trace-Ablage:** [`evidence/session-03/runs/website-run-001.jsonl`](runs/website-run-001.jsonl)
* **Zusammenarbeit zweier Agentenfähigkeiten:**
  1. `requirements_agent` (`product_owner_requirements`): Liest den Task aus `issue_t3.md` und erzeugt strukturierte Akzeptanzkriterien für N-01 bis N-09 (`RequirementsReport`).
  2. `architect_agent` (`software_architect`): Prüft semantische Struktur, Barrierefreiheit und lokale Asset-Pfade (`ArchitectureReport`).
  3. `qa_security_agent` (`qa_test_engineer` & `ai_safety_security_engineer`): Führt den automatisierten Produktcheck aus und verifiziert Sicherheit gegen Path Traversals und externe Scripts.
* **Reale Tool-Aktion auf Produkt-Checkout:** `write_target_text_file` / `read_repository_text_file` mit strikter Path-Traversal-Absicherung auf `client-01-website`.

---

## 3. Geprüfte Tageskriterien & Produktprüfung (L3.3 / B1–B6)

| Kriterium | Beschreibung | Prüfmethode | Status |
|---|---|---|---|
| **AC-01 (B1)** | Firmenname (`Nordwerk Industrie-Service`) & Hauptaussage (`Praktische Unterstützung für Ihren technischen Betrieb.`) | `test_website.py` (Checks 1 & 2) + Sichtprüfung Browser | **Bestanden** |
| **AC-02 Teil (B2)** | Erste Leistung Wartungsplanung (`Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe.`) | `test_website.py` (Check 3) + Sichtprüfung Browser | **Bestanden** |
| **AC-04 (B3)** | Kontaktlink `mailto:kontakt@nordwerk.example` beschriftet mit `Anfrage stellen`; Übungshinweis (`Fiktives Unternehmen – Lehrprojekt der HAW Hamburg...`) sichtbar | `test_website.py` (Checks 4, 5, 6) + Klicktest Mailto | **Bestanden** |
| **B4** | Eigener automatisierter Produktcheck | `python test_website.py` (8 von 8 Checks grün) | **Bestanden** |
| **B5** | Unabhängiger Start dokumentiert | `README.md` im Produkt-Repo dokumentiert `python -m http.server 8000` | **Bestanden** |
| **B6** | Kunden-Task ohne erfundene Versprechen | `client-01-website/issue_t3.md` referenziert exakte ACs; keine erfundenen Zertifikate/Logos | **Bestanden** |

---

## 4. Menschliches Approval Gate & Rollen (D1)

* **Accountable Humans:**
  - *Auftrag & Scope:* Mehrose Farooq
  - *Technische Lieferung:* Maxim Bers & David Pisarkiewicz
  - *Prüfung (QA):* Lars Boos
  - *Freigabeentscheidung:* Lars Boos & Mehrose Farooq
* **Gate-Entscheidung:** **`approved`** (dokumentiert in [`docs/customer-01/review.json`](../docs/customer-01/review.json)).
* **Sichtprüfung:** Lars Boos öffnete die Website unter `http://localhost:8000`, prüfte die Lesbarkeit bei 375 px und 1280 px und klickte den Kontaktlink zur Verifikation des Mailto-Entwurfs.
* **Eigener Factory-Test:** `tests/test_feature_pipeline.py::test_pipeline_addresses_client_target_dir` und `test_session_03_infrastructure.py` laufen im regulären `pytest`-Lauf der Factory fehlerfrei durch.

---

## 5. Kosten, Aufwand und Planbudget (L3.4 / C1–C3)

* **Planbudget Lieferung T3/T4:** 1.200 Credits (12 Personenstunden) zzgl. 400 Credits Reserve für T5 (dokumentiert in `costs/usage.csv`).
* **Factory-Entwicklung:** Getrennt erfasst (Revision-5-Infrastruktur-Update und Pipeline-Target-Dir-Erweiterung).
* **Menschlicher Gesamtaufwand Termin 3:**
  - `implementation`: 5,5 h (550 Credits)
  - `review`: 5,5 h (550 Credits)
  - `correction`: 1,0 h (100 Credits)
  - `meeting`: 12,0 h (Budgetvereinbarung T3/T4)
* **Agenten-Kosten Lauf `website-run-001`:** 3,4126 Credits (3 Calls, 37,3s Agenten-Laufzeit, 180s menschliche Review-Zeit getrennt erfasst; kein Double-Counting).

---

## 6. Konkreter Engpass & Überprüfbare Lernhypothese (C4)

* **Beobachteter Engpass (mit Beleg):**  
  Im initialen Modell-Entwurf versuchte der Agent, für das Kontaktformular ein JavaScript-Snippet mit einem externen CDN-Script einzubinden. Dies führte zu einer Abweisung durch den Sicherheits-Guardrail und erforderte einen internen Korrekturlauf auf reines semantisches HTML mit `mailto:`.
* **Überprüfbare Verbesserungshypothese für Termin 4:**  
  *Wenn* wir dem Agenten für Termin 4 eine explizite Pydantic-Komponenten-Grammatik (z. B. `ServiceCard`- und `ContactSection`-Datenmodelle) als In-Context-Constraint vorgeben,  
  *dann* sinkt die Wahrscheinlichkeit unzulässiger Script-Injections auf 0 % und die für die Generierung benötigten Tokens sinken um mindestens **20 %** (Messgröße: `input_tokens` + `output_tokens` in `usage.csv` für `CUST-002`).

---

## 7. Höchstens drei nächste Schritte für Termin 4 (D2)

1. **Ergänzung der verbleibenden Leistungen:** Integration von N-04 (Ersatzteilkoordination) und N-05 (Betriebsdokumentation) in `client-01-website/index.html`.
2. **Zielgruppen & Arbeitsweise:** Einarbeitung von N-06 (Zielgruppen) und N-07 (Arbeitsweise) mit zugehörigen Sprungmarken in der Navigation (AC-03, AC-05).
3. **Responsive Matrix-Automatisierung:** Automatisierter Headless-Test für die Viewports 375 px und 1280 px zur formalen Erfüllung von AC-06.
