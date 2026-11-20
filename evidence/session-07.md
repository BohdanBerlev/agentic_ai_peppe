# Evidence Session 7 – HansePack HP-V1 Candidate, Fehlererkennung & R-02 Baseline

**Team:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Datum:** 2026-11-20  
**Kunde:** HansePack Handelsgesellschaft (fiktiv) · **Projekt-ID:** `client-02`  
**Session:** `session-07` · **Regelversion:** `HP-V1` (CR-02 / HP-V2 bewusst erst in Termin 8)  
**Provider:** **100 % lokales Ollama (`qwen3.5:9b`, `temperature=0.0`, `num_ctx=8192`)** – keine externen Cloud-Tokens.

---

## 1. Repository-Trennung, Commits & Tags (`A1`, `B6`, `C1`, `D2`)

| Rolle / Stand | Repository / Branch | Eingabe-Commit | Ergebnis-Commit & Git-Tag | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Produkt 01 (Nordwerk)** | `DavidPisark/Nordwerk-Industrie-Service-Website` (`main`) | `d140f26` | **`d140f26`** | ✅ Unberührt (0 Änderungen durch T7) |
| **Produkt 02 (HansePack Candidate)** | `Vanitas50/client-02-quotation` (`main`) | `2dfb7ae` (T6) → `924ed18` (`issue_hp02.md`) | **`dfb7604`** (Tag: **`Q-BASE`**) | ✅ 64/64 Tests grün, frischer Checkout verifiziert |
| **Isolierter Fehler-Branch (A3)** | `Vanitas50/client-02-quotation` (`t7-fault-injection-q03`) | `d0b16d5` | **`e91db5c`** *(nur Nachweis, **nicht** gemergt!)* | ⛔ Absichtlicher Rabattfehler (`> 50`), vom Gate blockiert |
| **Factory-Basis vor R-02** | `BohdanBerlev/agentic_ai_peppe` (`main`) | `dde1ea1` (T6-Korrektur) | **`0d3a93a`** (Tag: **`F-BASE-T7`**; historischer T4/T5-Tag `F-BASE` bleibt unverändert auf `5a146a3`) | ✅ Saubere Baseline vor T8-Intervention |
| **Factory T7 Evidenz & Kosten** | `BohdanBerlev/agentic_ai_peppe` (`main`) | `0d3a93a` (`F-BASE-T7`) | `4a33c7a` → `d392312` → aktueller Sync-Commit | ✅ 95/95 Factory-Tests grün |

---

## 2. Factory: Reale Ollama-Folgeläufe & Eingriffsprotokoll (`A1`, `A2`, `L7.1`)

Alle substanziellen Produktaufgaben wurden über die bestehende Multi-Project-Factory (`src/projects.py`, Mandant `client-02`) und unser lokales Ollama (`qwen3.5:9b`) ausgeführt. Jeder Trace endet mit einem expliziten, revisionssicheren `human_approval_event`:

| Task-ID | Zweck / Zieldatei | Trace-Datei (`evidence/session-07/`) | Calls / Dauer / Credits | Gate-Event & Produkt-Commit | Eingriffsprotokoll |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **`HP-T7-01`** | `quotation.py`: `build_export_payload`, `export_quote_json`, CLI | [`13bf2f9a...jsonl`](session-07/13bf2f9a-4fa9-4835-8c09-87a4006e1012.jsonl) | 12 / 471,5 s / 17,74 Cr. | `approved` (Lars Boos, **`d0b16d5`**) | **0 manuelle Code-Änderungen** (rein agentisch, 77 Zeilen) |
| **`HP-T7-B-TESTS`** | `test_quotation.py`: alle 38 Fachtests (`Q01`–`Q14`, `E01`–`E10`, Export) | [`ee32a17f...jsonl`](session-07/ee32a17f-2e02-4ee4-b0aa-0d7c6144bd80.jsonl) | 8 / 288,0 s / 11,41 Cr. | `approved` (Lars Boos, **`5e7aa52`**) | **0 manuelle Code-Änderungen** (1. Versuch `38 passed`) |
| **`HP-T7-B-WEBUI`** *(Fehllauf)* | `app.py` (kombiniertes Python+HTML) | [`76eed45c...jsonl`](session-07/76eed45c-7107-462d-b5f7-d4bdb2364089.jsonl) | 7 / 363,0 s / 11,23 Cr. | `changes_requested` (Lars Boos, kein Diff) | `Unterminated string` bei kombiniertem File → Task sauber in `HP-T7-B-API` + `HP-T7-B-HTML` gesplittet |
| **`HP-T7-B-API`** | `app.py`: FastAPI (`GET /`, `/api/catalog`, `/api/quote` Roh-JSON, `/api/quote/export`) | [`a3deb97b...jsonl`](session-07/a3deb97b-1f2d-43a2-b987-eff8e0ef6319.jsonl) | 8 / 387,7 s / 12,54 Cr. | `approved` (Lars Boos, **`7a1f037`**) | **0 manuelle Code-Änderungen** (1. Versuch alle 24 Fälle grün) |
| **`HP-T7-B-HTML`** | `static/index.html`: HTML5/CSS/JS UI + Nettohinweis | [`cd227006...jsonl`](session-07/cd227006-f612-4ef2-8bfd-48299dd7ad11.jsonl) | 8 / 333,6 s / 11,92 Cr. | `approved` (Lars Boos, **`fdead8e`** → **`dfb7604`**) | Agentischer Roh-Commit `fdead8e`; menschlicher Review behob JS-Bindings (`data.items`→`data.lines`, Number-Parsing, `err.error.message`, Ausblenden bei Fehler) + ergänzte `test_api_webui.py`, `README.md`, `requirements.txt` in **`dfb7604`** (`Q-BASE`) |

---

## 3. Kontrollierte Fehler-Injektion & Factory-Gate-Tests (`A3`, `A4`, `L7.2`, `L7.3`)

### 3.1 Realer Fehler- und Korrekturlauf (`A3`)
1. **Kontrollierte Fehler-Injektion (`t7-fault-injection-q03`, Commit `e91db5c`):**  
   In `quotation.py` wurde genau eine Bedingung verändert: `if 1 <= quantity <= 50:` / `elif 51 <= quantity <= 99:` (5 %-Rabatt fälschlich erst **oberhalb 50** statt **ab 50**). Alle Kundenfixtures und Tests blieben unverändert.
   - Beobachtete Wirkung: `Q03` (`HP-BOX × 50`) berechnete **`13700` statt `13075` Cent** (`test_quotation.py` schlug mit `2 failed, 2 passed` fehl).
2. **Wirksame Blockierung durch die Factory (`HP-T7-FAULT-Q03`):**  
   - Trace: [`dd27bc0e-bd77-453d-b1df-38175264a3f3.jsonl`](session-07/dd27bc0e-bd77-453d-b1df-38175264a3f3.jsonl) (7 Calls, `257,14 s`, `10,21 Cr.`).
   - Ergebnis: `tests_passed: False`, **`quality_gate_blocked: True`**. Selbst ein expliziter menschlicher Freigabeversuch (`record_human_decision(..., decision="approved")`) wurde von `enforce_quality_gate` technisch auf **`changes_requested`** zurückgehalten.
3. **Korrektur & erneute Prüfung (`HP-T7-FAULT-FIXED`):**  
   - Rückwechsel auf `main` (`d0b16d5`, korrekte Bedingung `>= 50`; Branch `t7-fault-injection-q03` bleibt isoliert und wird **nicht** ausgeliefert).
   - Trace: [`116b8593-6739-4bf8-b863-20d5d06516ac.jsonl`](session-07/116b8593-6739-4bf8-b863-20d5d06516ac.jsonl) (`parent_workflow_id=dd27bc0e-...`, 7 Calls, `242,23 s`, `10,04 Cr.`).
   - Ergebnis: `tests_passed: True` (`Q03 == 13075`), `quality_gate_blocked: False`, `human_approval_event` (`approved`, Lars Boos).

### 3.2 Automatisierte Factory-Gate- & Isolationstests (`A4`)
- **[`tests/test_quality_gate_t7.py`](../tests/test_quality_gate_t7.py) (4/4 bestanden):**
  1. `test_t7_quality_gate_passed_state_allows_human_approval` (bestandener Gate-Zustand)
  2. `test_t7_quality_gate_blocks_discount_boundary_fault_q03` (zurückgehaltener Gate-Zustand bei `13700 != 13075`, inkl. blockiertem Freigabeversuch)
  3. `test_t7_quality_gate_bounded_repair_loop_respects_max_retries` (Schleifengrenze `max_impl_retries=2`)
  4. `test_t7_quality_gate_recovers_after_fault_correction` (End-to-End Recovery)
- **[`tests/test_project_separation_t6.py`](../tests/test_project_separation_t6.py) (9/9 bestanden):** Gehärtete Projektgrenzen (inkl. Unterverzeichnisse und positivem Projekt-Scope) bestehen vollständig weiter.

---

## 4. Kundenprodukt HansePack – Candidate `Q-BASE` (`B1`–`B6`, `HP-AC01`–`HP-AC07`)

- **Fach-, API- & Export-Tests (`python -m pytest -v` in `client-02-quotation`):** **`64 passed in 0.53s`**
  - `test_quotation.py` (**38 Tests**): Alle 14 gültigen Fälle `Q01`–`Q14` (alle Positionswerte, `int`-Typprüfung, `Q04`/`Q13`/`Q14` `ROUND_HALF_UP`, `Q06`/`Q07` Versandschwelle 50.000 Cent), alle 10 ungültigen Fälle `E01`–`E10` mit exaktem `reason`, alle 14 Export-Konsistenzprüfungen.
  - `test_api_webui.py` (**26 Tests**): `GET /` (Pflicht-Nettohinweis *„Nettobeträge – Lehrprojekt, kein verbindliches Angebot“*), `GET /api/catalog` (`HP-BOX`, `HP-TAPE`, `HP-FILM`), `POST /api/quote` & `POST /api/quote/export` für alle 14 gültigen Fälle (bitgenaue Gleichheit Anzeige == Export == `calculate_quote`) sowie Abweisung aller 10 ungültigen Fälle mit HTTP `400` ohne stille Typumwandlung (Roh-JSON-Parsing in `app.py`).
- **Frischer-Checkout-Nachweis (`B6`, `HP-AC01`, `HP-AC07`):**
  - Sauberer `git clone` von `client-02-quotation` (`Q-BASE`, `dfb7604`) in ein temporäres Verzeichnis komplett außerhalb der Factory.
  - SHA-256-Abgleich der unabhängigen Kundenfixtures gegen `task sheets/session-06-08/`:
    - `HansePack_Katalog.json`: `85a5f467b5ad5a68...` (identisch, unverändert)
    - `HansePack_Referenzfaelle.json`: `80a1e8a58c15b87b...` (identisch, unverändert)
  - `python -m pytest -q` im frischen Checkout ohne Factory/LLM: **`64 passed in 0.57s`**.
- **Menschlicher UI- & Export-Review (`B4`, `B5`, `D1`):**
  - Prüfer: **Lars Boos** (`qa_test_engineer` & `project_manager`).
  - Prüfpunkte: Mehrpositionsfall `Q12` (`HP-BOX × 50` + `HP-TAPE × 10` → Warenwert `15875`, Versand `1200`, Gesamt `17075` Cent), JSON-Download (`hansepack-angebot-HP-V1.json`) gegen Anzeige verglichen (Integer-Cent, `EUR`, `HP-V1` identisch), ungültige Menge `E01` (`0`) eingegeben → verständliche Fehlermeldung aus Python-Backend, Ergebnis-/Download-Bereich ausgeblendet.

---

## 5. Messung, R-02-Baseline, Hypothese & Tageskosten (`C1`–`C4`, `L7.4`)

### 5.1 Isolierte Vergleichsaufgabe `R-02-BASELINE-1` (`C1`, `C3`)
- **Basisstände:** Factory **`F-BASE-T7`** (`0d3a93a`), Produkt **`Q-BASE`** (`dfb7604`), `git status` clean, **nicht** in den Kunden-Candidate gemergt.
- **Nachweise:** Manifest [`r02-baseline-manifest.json`](session-07/r02-baseline-manifest.json), isolierter Patch [`r02-baseline-run1.patch`](session-07/r02-baseline-run1.patch), Trace [`5ea9dada...jsonl`](session-07/5ea9dada-74fb-4760-b579-85e031910e78.jsonl).
- **Messwerte (`F-BASE-T7`, Ollama `qwen3.5:9b`, `temperature=0.0`, `num_ctx=8192`):**
  - `12` Calls, `494,88 s`, **`18,1157 Credits`**, Gate-Abschluss `changes_requested`.
  - **Qualität:** `calculation_note: "Net amounts; shipping shown separately."` wurde korrekt im Export-JSON ergänzt (`TOTAL_CENTS: 13075`, `IN_QUOTE_DICT: False`); `36 passed, 28 failed` (`exit_code = 1`), weil `F-BASE-T7` nur 1 Datei (`quotation.py`) pro Lauf ändern kann und `test_quotation.py` nicht synchron aktualisierte.

### 5.2 Gezielte Hypothese für Termin 8 (`C4`)
- Vollständig dokumentiert in [`r02-hypothesis.md`](session-07/r02-hypothesis.md).
- **Engpass:** Single-File-Limit im `backend_agent` (verursachte 28 Export-Testfehler + 2. Retry in `R-02-BASELINE-1`) sowie `unparseable`-JSON-Antworten in Vorstufen-Agenten (`requirements_agent`).
- **Geplante kleine Änderung (erst in T8 nach Baseline!):** Multi-File-Support (begrenzt auf autorisierte `input_files` + `test_targets`) im `backend_agent` + einmaliger JSON-Repair-Retry im `requirements_agent`.
- **Ziel-Messgrößen in T8 (`F-NEW-T8` vs. `F-BASE-T7`):** `pytest exit_code == 0` inkl. neuem `calculation_note`-Test, `≤ 8` Calls, `≤ 13,00 Credits`, `0` `unparseable`-Abbrüche.

### 5.3 Tageskosten Termin 7 & Budgetabweichung (`C2`)
Forensisch ausgewertet durch unseren eigenen **`cost_agent`** ([`cost_analysis.json`](session-07/cost_analysis.json)) und vollständig verbucht in [`costs/usage.csv`](../costs/usage.csv):

| Kategorie | Details | Credits |
| :--- | :--- | ---: |
| **Mensch – Factory-Entwicklung** | `test_quality_gate_t7.py` + T6-Feedback-Härtung (`0,50 h`) | `50,00` |
| **Mensch – Kundenlieferung** | `issue_hp02*.md`, `test_api_webui.py`, `README`, `requirements`, Fresh Checkout (`0,50 h`) | `50,00` |
| **Mensch – Nacharbeit** | HTML-JS-Review-Fix `fdead8e → dfb7604` (`0,3333 h`) | `33,33` |
| **Mensch – Review & Gate** | Diff-Reviews, Human-Gate-Events, A3-Injektion, UI-/Export-Check (`0,50 h`) | `50,00` |
| **Mensch – Experiment R-02** | Isolierte R-02-Auswertung & Hypothese C4 (`0,25 h`, getrennt!) | `25,00` |
| **Agenten – Kundenlieferung** | 5 Ollama-Läufe (`HP-T7-01`, `B-TESTS`, Fehllauf `B-WEBUI`, `B-API`, `B-HTML`; 43 Calls) | `64,85` |
| **Agenten – Qualitätssicherung A3** | 2 Ollama-Läufe (`HP-T7-FAULT-Q03`, `HP-T7-FAULT-FIXED`; 14 Calls) | `20,25` |
| **Agenten – Experiment R-02** | `R-02-BASELINE-1` (12 Calls, separat ausgewiesen!) | `18,12` |
| **Agenten – Cost & Integration Audit** | `cost_agent` (`1,20 Cr.`) + `integration_agent` Handover-Audit (`1,06 Cr.`) | `2,26` |
| **CI-Läufe (GitHub Actions)** | 5 Läufe auf `main`: `44818087291` (`dde1ea1` ✅), `44829427257` (`0d3a93a` ✅), `44831252679` (`4a33c7a` ✅), `44832158410` (`d392312` ❌ transienter CI-Fehllauf), + Abschluss-Sync-Push (vorab gezählt à 1,00 Cr.) | `5,00` |
| **Externe Cloud-Kosten** | 100 % lokales Ollama (`qwen3.5:9b`) | `0,00` |
| **GESAMT TERMIN 7 (Ist)** | **Planbudget T7 aus T6: `300,00 Credits`** | **`318,80 Credits`** |

- **Erklärung der Planabweichung (`+18,80 Credits` / `+6,3 %`):** Die Überschreitung entsteht durch den ehrlich verbuchten Fehllauf `HP-T7-B-WEBUI` (`11,23 Cr.`), die 5 GitHub-Actions-CI-Läufe (inkl. Fehllauf `44832158410`) sowie die bewusste Entscheidung, alle Bereich-B-Einzeltasks real über das lokale LLM durch die 8-Agenten-Pipeline laufen zu lassen. Die Termin-8-Änderungsreserve (`200,00 Credits`) bleibt unangetastet.

---

## 6. Menschliche Verantwortung, Integration-Audit & Freigabestatus (`D1`)

- **Benannter Reviewer:** **Lars Boos** (`qa_test_engineer` & `project_manager` gemäß `organization/roles.yaml`).
- **Integration-Agent-Audit (`HP-T7-HANDOVER-AUDIT`):** Ausgeführt über lokales Ollama (`qwen3.5:9b`), Trace [`integration_handover_audit.jsonl`](session-07/integration_handover_audit.jsonl) → **`status_str: "approved"`**, `interface_gaps: []`, validierte Handovers `PO->PM`, `PM->SA`.
- **Klare Status-Trennung:**
  - **Kunden-Candidate `Q-BASE` (`dfb7604`):** ✅ **Technische Teamfreigabe erteilt** (Lars Boos für Team 3).
  - **Isolierter Fehlerstand `t7-fault-injection-q03` (`e91db5c`):** ⛔ **Nicht freigegeben / nicht ausgeliefert** (vom Quality Gate blockiert).
  - **Experiment `R-02-BASELINE-1` (`5ea9dada`):** 🧪 **Isolierte Baseline, nicht im Kunden-Candidate** (`changes_requested`).
  - **Kundenabnahme (Dozent in Rolle HansePack):** ⏳ **Ausstehend**.

---

## 7. Höchstens drei nächste Schritte für Termin 8 (`D2`)

1. **Factory-Verbesserung `F-NEW-T8` umsetzen & gegen `F-BASE` messen:** Multi-File-Support im `backend_agent` und JSON-Repair-Retry im `requirements_agent` implementieren und `R-02` auf einer frischen Kopie von `Q-BASE` erneut ausführen, um die Hypothese aus `r02-hypothesis.md` empirisch zu prüfen.
2. **Kundenänderung CR-02 (`HP-V2`) umsetzen:** Versandregeln auf `HP-V2` aktualisieren (unter 400 € Warenwert nach Rabatt → 15 € Versand, ab 400 € versandkostenfrei), alle `Q01`–`Q14` (HP-V2) + `E01`–`E10` + UI/Export-Konsistenz absichern.
3. **Finales Kunden-Release & Projektabschluss:** Versioniertes Release für HansePack erstellen, finale Gesamtkostenbilanz T6–T8 sowie Übergabehinweise in `evidence/session-08.md` dokumentieren und die Kundenabnahme abschließen.
