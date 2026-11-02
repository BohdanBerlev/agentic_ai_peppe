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
| **Factory-Repository (`F-BASE`)** | `https://github.com/BohdanBerlev/agentic_ai_peppe` (`.`) | `b112623` (Stand nach T3-Remediation) | `6da5414` | `F-BASE` (`main`) |
| **Produkt Release Candidate (`R-BASE`)** | `https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website` (`client-01-website`) | `3e6121b` (`v0.1.0-t3`) | `18d222b` | `v0.2.0-rc1` / `R-BASE` (`main`) |
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
- **Trace-Datei:** `evidence/session-04/cb3bcea8-4a03-4cc9-82cc-759136472b92.jsonl`
- **Beteiligte Agentenrollen & Tool-Einsatz:**
  1. `product_owner_requirements`, `project_manager`, `agent_engineer`: Analyse von `issue_t4.md` und des bestehenden RC1-Markups (`index.html`).
  2. `software_architect`: Architektur-Review des RC1-Eingabestands.
  3. `backend_api_engineer` (`my_backend_agent`): Schreibt per `write_repository_text_file` die vollständige `client-01-website/index.html` mit allen drei Leistungskarten (`N-03`, `N-04`, `N-05`), den Zielgruppen (`N-06`), der Arbeitsweise (`N-07`) und der vollständigen Navigation (`#leistungen`, `#zielgruppen`, `#arbeitsweise`, `#kontakt`).
  4. `qa_test_engineer`: Führt per `execute_repository_pytest` real `python test_website.py` aus (`tests_passed: true`, `exit_code: 0`, alle 4 Prüffamilien `F1`–`F4` bestanden).
  5. `ai_safety_security_engineer` & `integration_engineer`: Sicherheits- und Handover-Prüfung (`approved`).
- **Menschliche Gate-Entscheidung (D1):**
  - **Reviewer:** `David Pisarkiewicz`
  - **Entscheidung:** `approved` (`quality_gate_blocked: false`, `product_tests_passed: true`)
  - **Prüfung der C4-Hypothese aus T3:** Dank der in `b112623` implementierten De-Eskalation von Pre-Implementation-Architekturbefunden in `_compute_agent_recommendation` meldete das Gate nach grünen Produkttests direkt `agent_recommendation: "approved"`, wodurch die menschliche Gate-Prüfzeit von `322,45 s` (in T3) auf `45.0 s` (unter den prognostizierten `120 s`) sank!

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
     - Kontaktfehler (`mailto:kontakt@nordwerk-falsch.example`): `evidence/session-04/fault-injection/557714eb-efba-4260-af95-46ee17d95e22.json`
     - Linkfehler (`href="#kontakt-kaputt"`): `evidence/session-04/fault-injection/0210bc84-e836-4066-adc5-c6bf7fcfe032.json`
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
   - **Gesamtergebnis `pytest`:** `75 passed, 2 skipped` (`evidence/session-04/pytest.xml`).

---

## 5. Reproduzierbare Ausgangsmessung `R-01` auf `R-BASE` mit `F-BASE` (C1, C3, L4.4)

Vor Beginn jeglicher Termin-5-Optimierung wurde der Release Candidate als **`R-BASE`** und die Factory als **`F-BASE`** eingefroren und die isolierte Referenzaufgabe **`R-01`** auf einem separaten Branch (`experiment/r-01-baseline`) ausgeführt:

- **Aufgabe `R-01` ([`client-01-website/issue_r01.md`](../client-01-website/issue_r01.md)):**
  > *„Ergänze unter den Leistungen die Karte **‚Projektkoordination‘** mit dem Text **‚Wir koordinieren klar abgegrenzte technische Vorhaben mit Ihrem Team.‘** Alle bisherigen Inhalte, Kontaktziele und Navigation müssen erhalten bleiben.“*
- **Ausgeführter Befehl:**
  ```powershell
  .\.venv\Scripts\python.exe -m src.workflows.feature_pipeline --task-id R-01 --project-id client-01 --target-dir client-01-website --input-file index.html --test-target test_r01.py --issue-file issue_r01.md --desc "R-01 Baseline: Add service card Projektkoordination under Leistungen while preserving all existing content, contact targets and navigation." --full-company --use-backend-agent --session session-04
  ```

| Messgröße (`R-01` Baseline) | Wert (Lauf 1 – Pflichtlauf) |
|---|---|
| **Factory-Commit (`F-BASE`)** | `6da5414` |
| **Produkt-Basis-Commit (`R-BASE`)** | `18d222b` (Tag `R-BASE`) |
| **Experiment-Branch & Ergebnis-Commit** | Branch `experiment/r-01-baseline`, Commit `ad7d304` (nicht in `main` gemergt) |
| **Workflow-ID / Trace** | `0cef313b-b39e-4749-992f-c2c980403a8f` (`evidence/session-04/0cef313b-b39e-4749-992f-c2c980403a8f.jsonl`) |
| **Modell & Provider** | `google` / `gemini-3.5-flash-lite` (gemäß GEMINI_PROVIDER_WAIVER; gemini-3.8-flash wies Server-Demand-Spikes auf) |
| **Anzahl LLM-Calls** | `8` (Full-Company-Modus) |
| **Prüfergebnis (`python test_r01.py`)** | `PASSED` (alle 4 Familien `F1`–`F4` + `R-01 Zusatzleistung Projektkoordination`, **0 Regressionen**) |
| **Reine Agenten-Laufzeit (`duration_seconds`)** | `118.40 s` |
| **Menschliche Review-/Nacharbeitszeit** | `30.0 s` Review, `0 s` Nacharbeit |
| **Agenten-Kosten (`estimated_cost_credits`)** | `9.4473 Credits` |

---

## 6. Kosten, Aufwand & Planabweichung Termin 4 (C2)

- **Vereinbartes Planbudget Lieferung T3/T4:** `1.200,0 Credits` (+ `400,0 Credits` Reserve für T5).
- **Aufwand in Termin 4 (erfasst in [`costs/usage.csv`](../costs/usage.csv), strikt getrennt nach Kategorie):**
  - **Kundenlieferung Termin 4 (`TASK-002`):** `350.0 Credits` menschlicher Aufwand + `9.5938 Credits` Agentenlauf.
  - **Qualitätsgate-Entwicklung & R-01-Baseline (`FACTORY-DEV` & `R-01`):** `450.0 Credits` menschlicher Aufwand + `9.4473 Credits` für den isolierten Referenzlauf `R-01`.
- **Erklärung der Planabweichung (T3 + T4 kumuliert):**
  Da in Termin 3 bereits `1.250,0 Credits` für die initiale Kundenlieferung (`TASK-001`) angefallen sind, überschreitet die kumulierte Kundenlieferung T3+T4 das ursprüngliche 1.200-Credit-Schätzbudget. Ursache war der hohe initiale Abstimmungs-, CSS- und Review-Aufwand beim ersten End-to-End-Lauf in Termin 3; in Termin 4 selbst konnte der Lieferaufwand für `TASK-002` durch die wiederverwendete Factory (`--issue-file issue_t4.md`), die automatisierten Prüffamilien (`F1`–`F4`) und die behobene Gate-Empfehlungslogik (`C4`) deutlich gesenkt werden.

---

## 7. Belegter Engpass & Geplante Verbesserung für Termin 5 (C4, L4.4)

- **Beobachteter Engpass in der `R-01`-Baseline:**
  Im Full-Company-Modus führt die Pipeline für eine lokal begrenzte Text-/Karten-Ergänzung (`R-01`) vor und nach dem `backend_agent` insgesamt **8 sequentielle LLM-Aufrufe** aus (darunter einen LLM-gestützten `qa_test_engineer`-Aufruf und einen `software_architect`-Aufruf vor der Implementierung), obwohl die Produktprüfung `test_r01.py` (`F1`–`F4` + `R-01`) bereits deterministisch alle Akzeptanzkriterien abdeckt. Zudem fragt `resolve_google_model()` bei jedem Agenten-Schritt die Modellliste ab, was die Laufzeit (`duration_seconds`) und die Aufrufkosten (`calls * 1.0 Credit + 0.01/s`) dominiert.
- **Geplante Factory-Änderung für Termin 5 (wird erst *nach* Sicherung dieser `R-01`-Baseline in T5 umgesetzt):**
  1. **Deterministisches Pre-Gate-Short-Circuiting & Modell-Resolution-Caching:** Caching der Modellauflösung in `src/llm/factory.py` (`@lru_cache`) sowie ein schlanker Fast-Track-Modus in `feature_pipeline.py`, der nach erfolgreicher `backend_agent`-Implementierung die deterministische Produktprüfung (`execute_repository_pytest`) direkt ausführt und redundante LLM-Wrapper-Aufrufe einspart.
- **Erwarteter Effekt & Messkriterium bei Wiederholung von `R-01` in Termin 5:**
  - **Laufzeit (`duration_seconds`):** Reduktion bei `R-01` um mindestens **40 %** gegenüber dem `R-01`-Baseline-Messwert aus Termin 4.
  - **Agenten-Kosten (`estimated_cost_credits`):** Reduktion der Credits pro `R-01`-Lauf um mindestens **30 %** bei identischer Prüfqualität (`python test_r01.py` Exit-Code `0`, `0 Regressionen`).

---

## 8. Nächste Schritte für Termin 5 (maximal 3)

1. **Geplante Factory-Verbesserung umsetzen & `R-01` erneut messen:** Umsetzung des Modell-Cachings / Pre-Gate-Checks und direkter Vorher/Nachher-Vergleich gegen die heutige `R-01`-Baseline auf `R-BASE`.
2. **Kundenänderung `CR-01` über die verbesserte Factory liefern (`AC-09`):** Bearbeitung der in Termin 5 gestellten Kundenänderung inklusive Regressionsprüfung (`AC-01` bis `AC-09`).
3. **Sicherheitsanfrage `SR-01` & Endabnahme finalisieren (`AC-10`):** Ausarbeitung der abgegrenzten Sicherheitsantwort zu `CVE-2026-109618` / `CVE-2026-109619` (auf Basis unserer Vorarbeit in [`docs/customer-01/clarifications.md`](../docs/customer-01/clarifications.md)) und Abschluss der Kundenübergabe.
