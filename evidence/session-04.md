# Evidence Session 4 – Lieferfähige Website, wirksames Qualitätsgate und R-01 Baseline

**Team:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Datum:** 02. November 2026  
**Kunde:** Nordwerk Industrie-Service (Hamburg)  
**Auftrag Termin 4:** `TASK-002` (`project_id: "client-01"`) – Vollständiger Release Candidate (`AC-01` bis `AC-08`), kontrollierter Fehlernachweis am Qualitätsgate und reproduzierbare Ausgangsmessung `R-01` auf `R-BASE`.  
**LLM-Provider-Ausnahmegenehmigung:** [`docs/GEMINI_PROVIDER_WAIVER.md`](../docs/GEMINI_PROVIDER_WAIVER.md)

---

## 1. Repository-Trennung, Commits & Tags (A1, B5, D2)

| Stand / Rolle | Repository / Pfad | Eingabe-Commit | Ergebnis-Commit | Tag / Branch |
|---|---|---|---|---|
| **Factory-Repository (`F-BASE`)** | `https://github.com/BohdanBerlev/agentic_ai_peppe` (`.`) | `b112623` (Stand nach T3-Remediation) | `6da5414` (bzw. `HEAD` auf `main`) | `F-BASE` (`main`) |
| **Produkt Release Candidate (`R-BASE`)** | `https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website` (`client-01-website`) | `3e6121b` (`v0.1.0-t3`) / `fef6a55` (mit `issue_t4.md` & `test_website.py`) | `18d222b` | `v0.2.0-rc1` / `R-BASE` (`main`) |
| **Isolierter Fehlertest (Negativlauf)** | `runs/session-04/fault-test/557714eb-efba-4260-af95-46ee17d95e22/product` (isolierte Kopie) | `18d222b` | Isolierte 1-Zeilen-Mutation (nicht in `main`) | [`evidence/session-04/fault-injection/`](session-04/fault-injection/) |
| **Referenzversuch `R-01` (Baseline)** | `client-01-website` (separater Branch) | `18d222b` (`R-BASE`) | `ad7d304` | Branch `experiment/r-01-baseline` (nicht in `main` gemergt!) |

- **Frischer Checkout & Start ohne Factory (`AC-08` / `B5`):**
  ```powershell
  git clone https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website.git fresh-nordwerk-check
  cd fresh-nordwerk-check
  git checkout v0.2.0-rc1
  python test_website.py
  python -m http.server 8000
  ```

---

## 2. Realer Agenten-Folgelauf für `TASK-002` (A1, A2, L4.1)

- **Spezifikation:** [`client-01-website/issue_t4.md`](../client-01-website/issue_t4.md) (`TASK-002`: Ausbau auf alle Pflichtbausteine `N-01` bis `N-09` und `AC-01` bis `AC-08`)
- **Ausgeführter Befehl:**
  ```powershell
  .\.venv\Scripts\python.exe -m src.workflows.feature_pipeline --task-id TASK-002 --project-id client-01 --target-dir client-01-website --input-file index.html --test-target test_website.py --issue-file issue_t4.md --desc "Complete Nordwerk Industrie-Service Release Candidate (AC-01 to AC-08, N-01 to N-09) in index.html according to issue_t4.md so all 4 check families in test_website.py pass." --full-company --use-backend-agent --session session-04
  ```
- **Workflow-ID:** `cb3bcea8-4a03-4cc9-82cc-759136472b92`
- **Trace-Datei:** [`evidence/session-04/cb3bcea8-4a03-4cc9-82cc-759136472b92.jsonl`](session-04/cb3bcea8-4a03-4cc9-82cc-759136472b92.jsonl)
- **Überprüfbarer Produkt-Diff:** `git -C client-01-website diff fef6a55..18d222b -- index.html` (`https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website/commit/18d222b`)
- **Beteiligte Agentenrollen & Tool-Einsatz:**
  1. `product_owner_requirements` (`run_id: 39fa6f94...`), `project_manager` (`run_id: 40321be8...`), `agent_engineer` (`run_id: 78e2b33d...`): Analyse von `issue_t4.md` und des bestehenden RC1-Markups (`index.html`).
  2. `software_architect` (`run_id: ba6964ad...`): Architektur-Review des RC1-Eingabestands.
  3. `backend_api_engineer` (`run_id: cf08875b-7b67-41b2-9796-84f118d20108`): Schreibt per `write_repository_text_file` die vollständige `client-01-website/index.html` mit allen drei Leistungskarten (`N-03`, `N-04`, `N-05`), den Zielgruppen (`N-06`), der Arbeitsweise (`N-07`) und der vollständigen Navigation (`#leistungen`, `#zielgruppen`, `#arbeitsweise`, `#kontakt`).
  4. `qa_test_engineer` (`run_id: 962936c9-2b39-4343-ae54-65e4fad33aef`): Führt per `execute_repository_pytest` real `python test_website.py` aus (`tests_passed: true`, `exit_code: 0`, alle 4 Prüffamilien `F1`–`F4` bestanden).
  5. `ai_safety_security_engineer` (`run_id: f46d273c...`) & `integration_engineer` (`run_id: 2245fcfa...`): Sicherheits- und Handover-Prüfung (`approved`).
- **Menschliche Gate-Entscheidung (D1):**
  - **Reviewer:** `David Pisarkiewicz` (`run_id: a3c75be8-2f4f-4759-8db4-92b8b063830d`)
  - **Entscheidung:** `approved` (`quality_gate_blocked: false`, `product_tests_passed: true`)
  - **Prüfung der C4-Hypothese aus T3:** Dank der in `b112623` implementierten De-Eskalation von Pre-Implementation-Architekturbefunden in `_compute_agent_recommendation` meldete das Gate nach grünen Produkttests direkt `agent_recommendation: "approved"`, wodurch die menschliche Gate-Prüfzeit von `322,45 s` (in T3) auf **`45,0 s`** (unter den prognostizierten `120 s`) sank!

---

## 3. Vollständige AC-01 bis AC-08 Prüfliste & Vier Prüffamilien (B1–B6)

| AC | Anforderung | Automatisierte Prüffamilie (`test_website.py`) | Browser- / Sichtprüfung | Status |
|---|---|---|---|---|
| **AC-01** | Firmenname (`N-01`) & Hauptaussage (`N-02`) auf Startansicht | `F1 Pflichtinhalt` (`PASSED`) | Hero-Sektion geprüft | **Bestanden** |
| **AC-02** | Alle drei Leistungen (`N-03` Wartungsplanung, `N-04` Ersatzteilkoordination, `N-05` Betriebsdokumentation) erkennbar | `F1 Pflichtinhalt` (`PASSED`) | 3 Karten unter `#leistungen` geprüft | **Bestanden** |
| **AC-03** | Beide Zielgruppen (`N-06`) & Arbeitsweise (`N-07`) enthalten; keine erfundenen Leistungsversprechen | `F1 Pflichtinhalt` (`PASSED`) | `#zielgruppen` & `#arbeitsweise` geprüft | **Bestanden** |
| **AC-04** | Kontaktlink `mailto:kontakt@nordwerk.example` (`Anfrage stellen`, `N-08`) & Übungshinweis (`N-09`) | `F1 Pflichtinhalt` + `F2 Kontakt & Navigation` (`PASSED`) | Klicktest im Browser erfolgreich | **Bestanden** |
| **AC-05** | Navigation führt zu Leistungen & Kontakt; interne `#`-Links & lokale Assets (`styles.css`) funktionieren | `F2 Kontakt & Navigation` + `F3 Lokale Verweise & Assets` (`PASSED`) | Sprungmarken & `:target`-Fokus getestet | **Bestanden** |
| **AC-06** | Bei `375 px` und `1280 px` Breite kein horizontaler Überlauf; Text & Kontakt nutzbar | `F4 Bedienbarkeit statisch` (Viewport-Meta) | Manuelles Browser-Review ([`docs/customer-01/browser_review_t4.md`](../docs/customer-01/browser_review_t4.md)): `scrollWidth <= clientWidth` bei 375 px & 1280 px | **Bestanden** |
| **AC-07** | Dokumenttitel, `lang="de"`, sinnvolle Überschriften (`h1 -> h2 -> h3`), sichtbare Tastaturfokusse (`:focus-visible`), `alt`-Attribute | `F4 Bedienbarkeit statisch` (`PASSED`) | `Tab`-Reihenfolge & Fokusrahmen im Browser geprüft ([`browser_review_t4.md`](../docs/customer-01/browser_review_t4.md)) | **Bestanden** |
| **AC-08** | Frischer Produkt-Checkout startet ohne Factory/LLM/DB; Produkttests laufen separat | `F3` + Standalone-Lauf `python test_website.py` (`Exit-Code 0`) | Isolierter Start über `python -m http.server 8000` verifiziert | **Bestanden** |

---

## 4. Wirksames Qualitätsgate & Kontrollierter Fehlernachweis (A3, A4, L4.2, L4.3)

Wir unterscheiden strikt zwischen **deterministischen Factory-/Gate-Tests** und dem **kontrollierten Fehlerexperiment an der Produktkopie**:

1. **Kontrolliertes Fehlerexperiment in isolierter Testkopie (`src/quality/fault_injection.py`):**
   - **Befehl:**
     ```powershell
     .\.venv\Scripts\python.exe -m src.quality.fault_injection --fault contact --source-dir client-01-website
     .\.venv\Scripts\python.exe -m src.quality.fault_injection --fault link --source-dir client-01-website
     ```
   - **Evidenz-Dateien:**
     - Kontaktfehler (`mailto:kontakt@nordwerk-falsch.example`): [`evidence/session-04/fault-injection/557714eb-efba-4260-af95-46ee17d95e22.json`](session-04/fault-injection/557714eb-efba-4260-af95-46ee17d95e22.json)
     - Linkfehler (`href="#kontakt-kaputt"`): [`evidence/session-04/fault-injection/0210bc84-e836-4066-adc5-c6bf7fcfe032.json`](session-04/fault-injection/0210bc84-e836-4066-adc5-c6bf7fcfe032.json)
   - **Nachgewiesener Ablauf (3 Phasen ohne Beschädigung des Kunden-Release):**
     1. *Baseline-Prüfung der Kopie:* `python test_website.py` $\rightarrow$ `exit_code: 0` (`tests_passed: true`).
     2. *Injektion genau eines Fehlers:* `python test_website.py` schlägt sofort in Prüffamilie `F2 Kontakt & Navigation` fehl (`exit_code: 1`, `tests_passed: false`). `_compute_agent_recommendation` liefert zwingend `"changes_requested"`, und `enforce_quality_gate("approved", qa_rep)` **blockiert technisch jede Freigabe** (`quality_gate_blocked: true`, `effective_decision: "changes_requested"`, `released: false`).
     3. *Korrektur & erneute Prüfung:* Nach Wiederherstellung des korrekten Links besteht `python test_website.py` wieder (`exit_code: 0`, `quality_gate_blocked: false`, `released: true`).

2. **Deterministische Factory-Gate-Tests in `pytest` (`tests/test_quality_gate_t4.py`):**
   - `test_quality_gate_positive_candidate_passes_all_families` (Positivzustand `approved`)
   - `test_quality_gate_blocks_controlled_fault_and_prevents_approval[contact]` (Negativzustand Kontaktfehler blockiert Gate + verhindert menschlichen Override)
   - `test_quality_gate_blocks_controlled_fault_and_prevents_approval[link]` (Negativzustand Linkfehler blockiert Gate)
   - `test_controlled_fault_experiment_detects_blocks_and_recovers` (Vollständiger Negativ-/Korrektur-Zyklus)
   - `test_c4_hypothesis_does_not_override_failed_product_tests` (C4-Logik überstimmt niemals rote Produkttests)
   - **Gesamtergebnis `pytest`:** `75 passed, 2 skipped` ([`evidence/session-04/pytest.xml`](session-04/pytest.xml)).

---

## 5. Reproduzierbare Ausgangsmessung `R-01` auf `R-BASE` mit `F-BASE` inkl. Fehlläufen (C1, C3, L4.4)

Vor Beginn jeglicher Termin-5-Optimierung wurde der Release Candidate als **`R-BASE`** (`18d222b`) und die Factory als **`F-BASE`** (`6da5414`) eingefroren und die isolierte Referenzaufgabe **`R-01`** auf einem separaten Branch (`experiment/r-01-baseline`) ausgeführt:

- **Aufgabe `R-01` ([`client-01-website/issue_r01.md`](../client-01-website/issue_r01.md)):**
  > *„Ergänze unter den Leistungen die Karte **‚Projektkoordination‘** mit dem Text **‚Wir koordinieren klar abgegrenzte technische Vorhaben mit Ihrem Team.‘** Alle bisherigen Inhalte, Kontaktziele und Navigation müssen erhalten bleiben.“*
- **Ausgeführter Befehl:**
  ```powershell
  .\.venv\Scripts\python.exe -m src.workflows.feature_pipeline --task-id R-01 --project-id client-01 --target-dir client-01-website --input-file index.html --test-target test_r01.py --issue-file issue_r01.md --desc "R-01 Baseline: Add service card Projektkoordination under Leistungen while preserving all existing content, contact targets and navigation." --full-company --use-backend-agent --session session-04
  ```

### Übersicht aller Läufe für `R-01` (inklusive ehrlich ausgewiesener Quota-Fehlläufe)

| Messgröße | Versuch 1 (Fehllauf – 429 RPM Quota) | Versuch 2 (Fehllauf – 429 Daily Quota) | Versuch 3 (Vollständiger Baseline-Lauf) |
|---|---|---|---|
| **Factory-Commit (`F-BASE`)** | `6da5414` | `6da5414` | `6da5414` |
| **Produkt-Basis-Commit (`R-BASE`)** | `18d222b` (Tag `R-BASE`) | `18d222b` (Tag `R-BASE`) | `18d222b` (Tag `R-BASE`) |
| **Experiment-Branch & Ergebnis-Commit** | `experiment/r-01-baseline` (abgebrochen) | `experiment/r-01-baseline` (abgebrochen) | Branch `experiment/r-01-baseline`, Commit `ad7d304` (nicht in `main` gemergt) |
| **Workflow-ID / Trace** | [`cc5362a3-cb20-4c09-a14d-d8c2dfb58088.jsonl`](session-04/cc5362a3-cb20-4c09-a14d-d8c2dfb58088.jsonl) | [`1b7f1382-3448-4abf-84c7-6e891b48077c.jsonl`](session-04/1b7f1382-3448-4abf-84c7-6e891b48077c.jsonl) | [`0cef313b-b39e-4749-992f-c2c980403a8f.jsonl`](session-04/0cef313b-b39e-4749-992f-c2c980403a8f.jsonl) |
| **Modell & Provider** | `google` / `gemini-3.5-flash` | `google` / `gemini-3.5-flash` | `google` / `gemini-3.5-flash-lite` |
| **Anzahl LLM-Calls** | `6` (Abbruch vor Schritt 7 wegen 5 RPM Free-Tier-Limit) | `5` (Abbruch nach Schritt 5 wegen 20 RPD Free-Tier-Limit) | `8` (vollständiger Full-Company-Durchlauf) |
| **Prüfergebnis (`python test_r01.py`)** | `PASSED` in Schritt 6 (`exit_code: 0`), danach Pipeline-429 | Abbruch vor QA-Schritt (`429 RESOURCE_EXHAUSTED`) | **`PASSED` (alle 4 Familien `F1`–`F4` + `R-01 Zusatzleistung Projektkoordination`, 0 Regressionen)** |
| **Reine Agenten-Laufzeit (`duration_seconds`)** | `57.93 s` | `94.52 s` | **`118.40 s`** |
| **Menschliche Review-/Nacharbeitszeit** | `0 s` | `0 s` | **`30.0 s` Review, `0 s` Nacharbeit** |
| **Agenten-Kosten (`estimated_cost_credits`)** | `6.9086 Credits` | `6.2504 Credits` | **`9.4473 Credits`** |

---

## 6. Kosten, Aufwand & Planabweichung Termin 4 (C2)

- **Vereinbartes Planbudget Lieferung T3/T4:** `1.200,0 Credits` (+ `400,0 Credits` Reserve für T5).
- **Menschlicher Gesamtaufwand Termin 4 (4 Teammitglieder × 5,0 h = 20,0 h = `2.000,0 Credits` in [`costs/usage.csv`](../costs/usage.csv), strikt getrennt nach Kategorie):**
  1. **Kundenlieferung Termin 4 (`TASK-002`):** **`800,0 Credits` (8,0 h)** menschlicher Aufwand (`David 1.5h`, `Lars 3.5h`, `Mehrose 3.0h`) + **`9,5938 Credits`** Agentenlauf (`cb3bcea8`).
  2. **Factory- & Qualitätsgate-Entwicklung (`FACTORY-DEV`):** **`700,0 Credits` (7,0 h)** menschlicher Aufwand (`David 2.0h`, `Maxim 5.0h`) für `enforce_quality_gate`, `fault_injection.py`, `test_quality_gate_t4.py` und die 4 Prüffamilien.
  3. **Isoliertes Baseline-Experiment (`R-01`):** **`500,0 Credits` (5,0 h)** menschlicher Aufwand (`David 1.5h`, `Lars 1.5h`, `Mehrose 2.0h`) + **`22,6063 Credits`** Agentenkosten (`9,4473 Credits` erfolgreicher Lauf `0cef313b` + `6,9086 Credits` Fehllauf `cc5362a3` + `6,2504 Credits` Fehllauf `1b7f1382`).
- **Erklärung der Planabweichung (T3 + T4 kumuliert):**
  Da in Termin 3 bereits `1.250,0 Credits` (12,5 h) für die initiale Kundenlieferung (`TASK-001`) angefallen sind und in Termin 4 weitere `800,0 Credits` (8,0 h) für `TASK-002` hinzukamen, liegt die kumulierte Kundenlieferung T3+T4 bei `2.050,0 Credits` (gegenüber `1.200,0 Credits` ursprünglichem Schätzbudget bzw. `1.600,0 Credits` inkl. Reserve). Ursache war der hohe initiale Abstimmungs-, CSS- und Review-Aufwand beim ersten End-to-End-Lauf in Termin 3; in Termin 4 selbst konnte der Lieferaufwand von `1.250,0 Credits` auf `800,0 Credits` (**-36 %**) und die Agenten-Kosten von `30,9069 Credits` auf `9,5938 Credits` (**-69 %**) gesenkt werden.

---

## 7. Belegter Engpass & Geplante Verbesserung für Termin 5 (C4, L4.4)

- **Beobachteter Engpass in der `R-01`-Baseline:**
  1. Im Full-Company-Modus führt die Pipeline für eine lokal begrenzte Karten-Ergänzung (`R-01`) **8 sequentielle LLM-Aufrufe** aus (darunter je einen LLM-Aufruf für `agent_engineer`, `software_architect`, `qa_test_engineer`, `ai_safety_security_engineer` und `integration_engineer`), obwohl die Produktprüfung `test_r01.py` (`F1`–`F4` + `R-01`) bereits deterministisch alle Akzeptanzkriterien abdeckt.
  2. Genau diese hohe Call-Anzahl pro Lauf (8 Calls) führte auf dem Google Free-Tier in Versuch 1 (`cc5362a3`) und Versuch 2 (`1b7f1382`) direkt in das `429 RESOURCE_EXHAUSTED` Rate-Limit und erzwang im erfolgreichen Lauf (`0cef313b`) eine Drosselung auf `requests_per_second=0.08` (`118,40 s` Laufzeit).
- **Geplante Factory-Änderung für Termin 5 (wird erst *nach* Sicherung dieser `R-01`-Baseline in T5 umgesetzt):**
  **Deterministisches Pre-Gate & Lean-Company-Modus + Modell-Resolution-Caching:** Caching von `resolve_google_model()` (`@lru_cache`) in `src/llm/factory.py` sowie Einführung eines schlanken Ausführungsmodus in `feature_pipeline.py`, der die deterministische Produktprüfung (`execute_repository_pytest`) und den PHP/Security-Check (`detect_php_security_risks`) direkt als Gate-Validierung nutzt und redundante Post-Implementation-LLM-Wrapper-Aufrufe einspart.
- **Erwarteter Effekt & Messkriterium bei Wiederholung von `R-01` in Termin 5:**
  - **Anzahl LLM-Calls & Rate-Limit-Fehler:** Reduktion von `8` auf `<= 4` Calls pro Lauf (`0` Quota-Abbrüche).
  - **Laufzeit (`duration_seconds`):** Reduktion bei `R-01` um mindestens **40 %** (von `118,40 s` auf `< 70 s`).
  - **Agenten-Kosten (`estimated_cost_credits`):** Reduktion der Credits pro `R-01`-Lauf um mindestens **30 %** (von `9,4473 Credits` auf `< 6,60 Credits`) bei identischer Prüfqualität (`python test_r01.py` Exit-Code `0`, `0 Regressionen`).

---

## 8. Nächste Schritte für Termin 5 (maximal 3)

1. **Geplante Factory-Verbesserung umsetzen & `R-01` erneut messen:** Umsetzung des Lean-Gate-/Caching-Upgrades und direkter Vorher/Nachher-Vergleich gegen die heutige `R-01`-Baseline (`0cef313b`) auf `R-BASE`.
2. **Kundenänderung `CR-01` über die verbesserte Factory liefern (`AC-09`):** Bearbeitung der in Termin 5 gestellten Kundenänderung inklusive Regressionsprüfung (`AC-01` bis `AC-09`).
3. **Sicherheitsanfrage `SR-01` & Endabnahme finalisieren (`AC-10`):** Ausarbeitung der abgegrenzten Sicherheitsantwort zu `CVE-2026-109618` / `CVE-2026-109619` (auf Basis unserer Vorarbeit in [`docs/customer-01/clarifications.md`](../docs/customer-01/clarifications.md)) und Abschluss der Kundenübergabe.
