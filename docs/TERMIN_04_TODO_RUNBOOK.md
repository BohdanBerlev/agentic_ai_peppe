# Termin 4 – Schritt-für-Schritt Runbook & To-do-Liste (02.11.2026, 10:00–15:00 Uhr)

**Projekt:** Agentic AI Software Factory (`agentic_ai_peppe`) & Kundenprojekt 01 (`client-01-website`, Nordwerk Industrie-Service)  
**Team 3 (`PepeGroup`):** David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq  
**Verbindliche Referenzdokumente:**
- Aufgabenblatt: [`task sheets/session-03-05/Aufgabenblatt_Termin_04_de.md`](../task%20sheets/session-03-05/Aufgabenblatt_Termin_04_de.md)
- Bewertungsraster (100 Punkte, Lernziele L4.1–L4.4): [`task sheets/session-03-05/Bewertungsraster_Termin_04_Factory.md`](../task%20sheets/session-03-05/Bewertungsraster_Termin_04_Factory.md)
- Kundenbriefing (`N-01` bis `N-09`, `AC-01` bis `AC-08`): [`task sheets/session-03-05/Kundenbriefing_Nordwerk_de.md`](../task%20sheets/session-03-05/Kundenbriefing_Nordwerk_de.md)

---

## 0. Kontext für Team & KI-Assistenten (Was bereits fertig vorbereitet ist!)

> **WICHTIGER HINWEIS FÜR KI-AGENTEN / ASSISTENTEN:**  
> Bitte die vorbereiteten Dateien **NICHT** neu erfinden oder überschreiben! Die komplette technische Infrastruktur für Termin 4 ist bereits implementiert, getestet (`75 passed, 2 skipped`) und eingecheckt. In Termin 4 müssen nur noch die untenstehenden **Schritte 1 bis 5** der Reihe nach ausgeführt und die dabei entstehenden echten `workflow_id`s / Commit-Hashes in [`evidence/session-04.md`](../evidence/session-04.md), [`docs/customer-01/browser_review_t4.md`](customer-01/browser_review_t4.md) und [`costs/usage.csv`](../costs/usage.csv) eingetragen werden.

### Bereits vorhandene Vorbereitung im Produkt-Repo (`client-01-website/`)
1. **[`client-01-website/issue_t4.md`](../client-01-website/issue_t4.md) (`TASK-002`):** Spezifikation für den Ausbau von `index.html` auf alle Pflichtinhalte `N-01` bis `N-09` und `AC-01` bis `AC-08` (inkl. der neuen Leistungen `N-04` Ersatzteilkoordination, `N-05` Betriebsdokumentation, `N-06` Zielgruppen, `N-07` Arbeitsweise und vollständiger Navigation `#leistungen`, `#zielgruppen`, `#arbeitsweise`, `#kontakt`).
2. **[`client-01-website/test_website.py`](../client-01-website/test_website.py) (Kriterium B6):** Prüft deterministisch in **4 Prüffamilien**:
   - `F1 Pflichtinhalt (AC-01..AC-04)`: Alle Bausteine `N-01` bis `N-09` vorhanden + Verbot erfundener Versprechen/Tracker.
   - `F2 Kontakt & Navigation (AC-04, AC-05)`: `mailto:kontakt@nordwerk.example` mit `Anfrage stellen`, `<nav>`-Links zu `#leistungen` und `#kontakt`, jedes interne `href="#..."` besitzt ein passendes `id="..."` im DOM.
   - `F3 Lokale Verweise & Assets / PHP-frei (AC-05, AC-08)`: Alle lokalen Assets (`styles.css`) existieren im Checkout, keine externen `http(s)`-Links, keine `.php`-Dateien oder PHP-Tags (`CVE-2026-109618` / `CVE-2026-109619`).
   - `F4 Bedienbarkeit statisch (AC-06/AC-07)`: `<title>`, `<html lang="de">`, `<meta name="viewport">`, genau eine `<h1>`, keine übersprungenen Überschriftenebenen (`h1 -> h2 -> h3`), `alt`-Attribute, sichtbarer `:focus-visible`-Rahmen in `styles.css`.
   - *Hinweis:* Aktuell ist `client-01-website/index.html` bewusst noch auf dem **Termin-3-Stand** (ohne `N-04` bis `N-07`), damit in **Schritt 1** der echte Agenten-Lauf (`TASK-002`) den substanziellen Produkt-Diff erzeugt!
3. **[`client-01-website/issue_r01.md`](../client-01-website/issue_r01.md) & [`client-01-website/test_r01.py`](../client-01-website/test_r01.py) (Kriterien C1, C3):** Spezifikation und Prüfskript für die isolierte Referenzaufgabe **`R-01`** (*„Ergänze unter den Leistungen die Karte ‚Projektkoordination‘ mit dem Text ‚Wir koordinieren klar abgegrenzte technische Vorhaben mit Ihrem Team.‘“* + Regressionsfreiheit für `F1`–`F4`).
4. **[`client-01-website/styles.css`](../client-01-website/styles.css) & [`client-01-website/README.md`](../client-01-website/README.md):** CSS-Regeln für `.service-card` und Zielgruppen-Listen sowie Start-/Testanleitung sind bereits aktualisiert.

### Bereits vorhandene Vorbereitung im Factory-Repo (`agentic_ai_peppe`)
1. **[`src/workflows/feature_pipeline.py`](../src/workflows/feature_pipeline.py) & [`src/agents/backend_agent.py`](../src/agents/backend_agent.py):**
   - Unterstützt `--issue-file issue_t4.md` bzw. `--issue-file issue_r01.md`.
   - Gibt bei jedem Knoten eine Live-Fortschrittszeile (`[pipeline HH:MM:SS] Schritt X/6 ...`) aus.
   - **Technisches Qualitätsgate (`product_tests_failed` & `enforce_quality_gate`):** Wenn die Produkttests (`test_website.py`) fehlschlagen (`tests_passed == False`), liefert `_compute_agent_recommendation` zwingend `"changes_requested"` und `enforce_quality_gate` blockiert technisch jede `"approved"`-Freigabe (`quality_gate_blocked=True`).
   - **C4-Fix aus Termin 3 (`b112623`):** Ein `changes_requested` vom Pre-Implementation-Architect wird automatisch zu `"approved"` de-eskaliert, sobald Backend, QA (`tests_passed == True`) und Integration nach der Code-Generierung `"approved"` melden.
2. **[`src/quality/fault_injection.py`](../src/quality/fault_injection.py) (Kriterium A3, Lernziel L4.3):**
   - Kopiert `client-01-website` in ein isoliertes Arbeitsverzeichnis (`runs/session-04/fault-test/<run_id>/product`), injiziert gezielt genau **einen** Fehler (`--fault contact` oder `--fault link`), beweist das Fehlschlagen von `test_website.py` und die Blockade am Gate (`quality_gate_blocked: true`, `released: false`), repariert den Fehler wieder, beweist das Bestehen nach Korrektur und speichert den JSON-Nachweis unter `evidence/session-04/fault-injection/<run_id>.json`.
3. **[`tests/test_quality_gate_t4.py`](../tests/test_quality_gate_t4.py) (Kriterium A4):**
   - 5 deterministische `pytest`-Tests für positiven und abgelehnten/blockierten Gate-Zustand.
4. **[`evidence/session-04.md`](../evidence/session-04.md) & [`docs/customer-01/browser_review_t4.md`](customer-01/browser_review_t4.md):**
   - Vollständig vorbereitete Abgabedokumente mit klaren `<PLATZHALTERN>`, die in Schritt 5 mit den echten Werten aus den Läufen gefüllt werden.

---

## Schritt-für-Schritt To-do-Liste für Termin 4

### [x] Schritt 0 (10:00–10:15 Uhr): Git-Stand im Team synchronisieren (ERLEDIGT)
Alle Teammitglieder holen sich den aktuellen Stand von `main` in beiden Repositories:

```powershell
git pull origin main
git -C client-01-website pull origin main --tags
```
*(Falls bei einem Teammitglied der Ordner `client-01-website/` noch nicht mit `https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website.git` verbunden ist, einmal das Repo dorthin klonen).*

Kurz prüfen, wo der Eingabe-Commit des Produkts vor dem Agentenlauf steht:
```powershell
git -C client-01-website rev-parse --short HEAD
```
*(Diesen Commit-Hash als Eingabe-Commit für `TASK-002` merken).*

---

### [x] Schritt 1 (10:20–11:15 Uhr): Echten Agenten-Lauf für `TASK-002` ausführen (Kriterien A1, A2, B1, B2, L4.1) (ERLEDIGT: `cb3bcea8-4a03-4cc9-82cc-759136472b92`)

1. **Pipeline-Befehl im Hauptverzeichnis (`agentic_ai_peppe`) starten:**
   ```powershell
   .\.venv\Scripts\python.exe -m src.workflows.feature_pipeline --task-id TASK-002 --project-id client-01 --target-dir client-01-website --input-file index.html --test-target test_website.py --issue-file issue_t4.md --desc "Complete Nordwerk Industrie-Service Release Candidate (AC-01 to AC-08, N-01 to N-09) in index.html according to issue_t4.md so all 4 check families in test_website.py pass." --full-company --use-backend-agent --session session-04
   ```
2. **Während der Lauf läuft:**
   - Ihr seht im Terminal jetzt live `[pipeline HH:MM:SS] Schritt 0/6 ...` bis `Schritt 5/6`.
   - `backend_agent` überschreibt `client-01-website/index.html` mit dem vollständigen Release Candidate (`N-01` bis `N-09`), und `qa_test_engineer` führt `python test_website.py` aus.
3. **Am interaktiven Human Approval Gate (`Schritt 5/6`):**
   - Prüfen, dass `QA / Security Status : approved` und `Agent Recommendation : approved` angezeigt wird.
   - Vollständigen Namen eingeben (z. B. `David Pisarkiewicz`).
   - Entscheidung **`a`** (`Approved`) wählen.
   - Kurze Begründung eingeben:
     `Release Candidate erfuellt AC-01 bis AC-08; alle 4 Prueffamilien F1-F4 in test_website.py bestanden.`
4. **Ergebnis prüfen & Werte notieren:**
   - Produktprüfung direkt ausführen:
     ```powershell
     .\.venv\Scripts\python.exe client-01-website/test_website.py
     ```
     *(Erwartete Ausgabe: `PASSED` für `F1`, `F2`, `F3`, `F4` und `ALLE PRUEFFAMILIEN BESTANDEN`).*
   - Aus der Konsolenausgabe bzw. der neuesten Datei in `evidence/session-04/<workflow_id>.jsonl` notieren:
     - `<TASK_002_WORKFLOW_ID>`
     - `<HUMAN_REVIEW_SEC_T4>` (`human_review_seconds`)
     - `<TASK_002_AGENT_CREDITS>` (`estimated_cost_credits`)

---

### [x] Schritt 2 (11:15–11:50 Uhr): Browser-Prüfung (375 px / 1280 px & Tastaturfokus) + Release Candidate taggen (`v0.2.0-rc1` & `R-BASE`) (Kriterien B3, B4, B5, D1) (ERLEDIGT: `18d222b`)

1. **Lokalen Webserver ohne Factory starten:**
   ```powershell
   python -m http.server 8000 --directory client-01-website
   ```
2. **Im Browser unter `http://localhost:8000` prüfen:**
   - **Responsive Check (`AC-06` / `B3`):** Browser-DevTools (`F12`) $\rightarrow$ Device Toolbar (`Strg+Shift+M`) $\rightarrow$ Breite nacheinander auf **`375`** px und **`1280`** px setzen. Prüfen, dass kein horizontaler Scrollbalken entsteht und alle Inhalte (`N-01` bis `N-09`) lesbar sind. Optional in der Browser-Konsole prüfen:
     `document.documentElement.scrollWidth <= document.documentElement.clientWidth` (muss `true` ergeben).
   - **Tastaturfokus & Navigation (`AC-05`, `AC-07` / `B4`):** Mit der `Tab`-Taste durch alle Links (`Leistungen`, `Zielgruppen`, `Arbeitsweise`, `Kontakt`, beide `Anfrage stellen`-Buttons) navigieren $\rightarrow$ orangener Fokusrahmen (`:focus-visible`) muss überall sichtbar sein; Klick auf die Navigationslinks springt zum jeweiligen Abschnitt.
   - Server wieder mit `Strg+C` beenden.
3. **Fertigen Release Candidate im Produkt-Repo (`client-01-website`) committen, als `v0.2.0-rc1` und `R-BASE` taggen und pushen:**
   ```powershell
   git -C client-01-website diff
   git -C client-01-website add index.html
   git -C client-01-website commit -m "feat(TASK-002): complete Nordwerk Release Candidate (AC-01 to AC-08)"
   git -C client-01-website tag -f v0.2.0-rc1
   git -C client-01-website tag -f R-BASE
   git -C client-01-website push origin main --tags
   git -C client-01-website rev-parse --short HEAD
   ```
   - Den ausgegebenen Commit-Hash als **`<CANDIDATE_COMMIT_T4>`** (gleichzeitig **`R-BASE`**) notieren!

---

### [x] Schritt 3 (12:30–13:15 Uhr): Kontrollierte Fehlersituation am Qualitätsgate durchführen (Kriterien A3, A4, L4.2, L4.3) (ERLEDIGT: `557714eb` & `0210bc84`)

Jetzt weist ihr nach, dass ein gezielter Kontakt- bzw. Linkfehler in einer isolierten Testkopie von `test_website.py` erkannt wird, das Gate die Freigabe verhindert (`quality_gate_blocked: true`, `released: false`) und nach der Reparatur wieder besteht:

1. **Beide kontrollierten Fehler-Experimente ausführen:**
   ```powershell
   .\.venv\Scripts\python.exe -m src.quality.fault_injection --fault contact --source-dir client-01-website
   .\.venv\Scripts\python.exe -m src.quality.fault_injection --fault link --source-dir client-01-website
   ```
   - Prüfen, dass beide Ausgaben `"status": "passed"` und `"expected_behaviour_observed": true` melden.
   - Die beiden erzeugten JSON-Dateien liegen nun in `evidence/session-04/fault-injection/<run_id>.json`. Deren `run_id`s als `<FAULT_CONTACT_RUN_ID>` und `<FAULT_LINK_RUN_ID>` notieren.
2. **Factory-Gate-Unit-Tests (`pytest`) ausführen und JUnit-Report aktualisieren:**
   ```powershell
   .\.venv\Scripts\python.exe -m pytest --junitxml=evidence/session-04/pytest.xml -v
   ```

---

### [x] Schritt 4 (13:30–14:15 Uhr): Ausgangsversuch `R-01` auf `R-BASE` mit `F-BASE` sichern (Kriterien C1, C3, C4, L4.4) (ERLEDIGT: `0cef313b-b39e-4749-992f-c2c980403a8f`, Commit `ad7d304`)

> **WICHTIG:** `R-01` ist eine isolierte Referenzaufgabe für den Vergleich mit Termin 5. Das Ergebnis von `R-01` gehört auf den separaten Branch `experiment/r-01-baseline` und darf **nicht** in den Kunden-Release (`main`) gemergt werden!

1. **Factory-Basisstand als `F-BASE` markieren:**
   ```powershell
   git tag -f F-BASE
   git rev-parse --short HEAD
   ```
2. **Im Produkt-Repo (`client-01-website`) ab `R-BASE` auf einen eigenen Experiment-Branch wechseln:**
   ```powershell
   git -C client-01-website checkout -B experiment/r-01-baseline R-BASE
   ```
3. **Echten Agenten-Lauf für `R-01` starten (nutzt `issue_r01.md` und `test_r01.py`):**
   ```powershell
   .\.venv\Scripts\python.exe -m src.workflows.feature_pipeline --task-id R-01 --project-id client-01 --target-dir client-01-website --input-file index.html --test-target test_r01.py --issue-file issue_r01.md --desc "R-01 Baseline: Add service card Projektkoordination under Leistungen with text 'Wir koordinieren klar abgegrenzte technische Vorhaben mit Ihrem Team.' while preserving all existing content, contact targets and navigation." --full-company --use-backend-agent --session session-04
   ```
   - Am Human Gate wieder mit Namen und `a` (`Approved`) bestätigen, sobald `test_r01.py` grün ist.
4. **`R-01`-Prüfung verifizieren, auf dem Experiment-Branch committen & pushen, und `client-01-website` wieder zurück auf `main` (`R-BASE`) stellen:**
   ```powershell
   .\.venv\Scripts\python.exe client-01-website/test_r01.py
   git -C client-01-website add index.html
   git -C client-01-website commit -m "experiment(R-01): baseline run on R-BASE with F-BASE"
   git -C client-01-website rev-parse --short HEAD
   git -C client-01-website push -u origin experiment/r-01-baseline
   git -C client-01-website checkout main
   ```
   - Den Commit-Hash von `experiment/r-01-baseline` als **`<R01_COMMIT>`** sowie aus der Trace-Datei `evidence/session-04/<R01_WORKFLOW_ID>.jsonl` die Werte `<R01_WORKFLOW_ID>`, `<R01_AGENT_SEC>`, `<R01_HUMAN_REVIEW_SEC>` und `<R01_CREDITS>` notieren.

---

### [x] Schritt 5 (14:35–15:00 Uhr): Evidenz, Browser-Review & Kosten finalisieren und pushen (Kriterien C2, D1, D2) (ERLEDIGT)

*(Tipp: Ihr könnt an dieser Stelle einfach euren KI-Assistenten bitten: „Lies die neuen Traces in `evidence/session-04/` und die Git-Commits aus und fülle alle Platzhalter in `evidence/session-04.md`, `docs/customer-01/browser_review_t4.md` und `costs/usage.csv` aus!“)*

1. **Platzhalter in [`docs/customer-01/browser_review_t4.md`](customer-01/browser_review_t4.md) ersetzen:**
   - `<CANDIDATE_COMMIT>` durch den Commit-Hash von `v0.2.0-rc1` / `R-BASE` ersetzen.
2. **Platzhalter in [`evidence/session-04.md`](../evidence/session-04.md) ersetzen:**
   - `<FACTORY_COMMIT_T4>`, `<CANDIDATE_COMMIT_T4>`, `<TASK_002_WORKFLOW_ID>`, `<HUMAN_REVIEW_SEC_T4>`, `<FAULT_CONTACT_RUN_ID>`, `<FAULT_LINK_RUN_ID>`, `<R01_COMMIT>`, `<R01_WORKFLOW_ID>`, `<R01_AGENT_SEC>`, `<R01_HUMAN_REVIEW_SEC>`, `<R01_CREDITS>`.
3. **Kosten in [`costs/usage.csv`](../costs/usage.csv) ergänzen:**
   - Die beiden echten Agenten-Runs (`TASK-002` und `R-01`) mit ihren exakten Credits aus den `.jsonl`-Traces eintragen.
   - Die menschlichen Stunden für Termin 4 pro Teammitglied sauber getrennt nach **`TASK-002`** (Kundenlieferung/Review), **`R-01`** (Baseline-Messung) und **`FACTORY-DEV`** (Gate-/Test-Ausbau) eintragen.
4. **Alles im Factory-Repo committen und auf GitHub pushen:**
   ```powershell
   git add evidence/session-04/ evidence/session-04.md docs/customer-01/browser_review_t4.md costs/usage.csv
   git commit -m "docs(session-04): finalize T4 evidence, fault-injection records, R-01 baseline, and cost records"
   git push origin main --tags
   ```
