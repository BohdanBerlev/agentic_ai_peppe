# Hypothese für Termin 8 (C4 – Gezielte Factory-Verbesserung nach R-02-Baseline)

**Baseline-Stände (vor Intervention gesichert):**
- **Factory-Basis (`F-BASE`):** `0d3a93a` (`Agentic-AI-Projekt`, `main`)
- **Produkt-Basis (`Q-BASE`):** `dfb7604` (`client-02-quotation`, `main`, 64/64 Tests grün)
- **Baseline-Lauf (`R-02-BASELINE-1`):** Workflow `5ea9dada-74fb-4760-b579-85e031910e78`, Patch [`r02-baseline-run1.patch`](r02-baseline-run1.patch), Manifest [`r02-baseline-manifest.json`](r02-baseline-manifest.json)

---

## 1. Empirisch beobachteter Factory-Engpass (aus T7-Traces)

In `R-02-BASELINE-1` (und den übrigen sieben T7-Läufen auf lokalem Ollama `qwen3.5:9b`) wurden zwei direkt messbare Engpässe in `F-BASE` beobachtet:

1. **Single-File-Limit im `backend_agent` (primärer Engpass in `R-02-BASELINE-1`):**
   - Unser `backend_agent` konnte in `F-BASE` nur exakt `input_files[0]` (`quotation.py`) verändern.
   - Er fügte `"calculation_note": "Net amounts; shipping shown separately."` zwar fachlich korrekt in `export_quote_json` ein (`CALC_NOTE` verifiziert, `TOTAL_CENTS: 13075`, `IN_QUOTE_DICT: False`), konnte jedoch die zugehörige Testdatei (`test_quotation.py`) **nicht gleichzeitig** anpassen und keinen neuen Test für `calculation_note` ergänzen.
   - Folge: `28` bestehende Export-Gleichheitstests schlugen fehl (`isolated_pytest_exit_code = 1`), der Reparatur-Loop lief bis `max_impl_retries = 2` (`12` LLM-Calls, `494,88 s`, `18,12 Credits`) und endete mit `changes_requested`.
2. **Wiederholte `unparseable`-JSON-Antworten in Vorstufen-Agenten (`requirements_agent`):**
   - In mehreren T7-Läufen auf `qwen3.5:9b` lieferten `product_owner_requirements` oder `project_manager` leeres/abgebrochenes JSON (`Expecting value` / `Unterminated string`), wodurch der Workflow trotz funktionierendem Produktcode auf `status: "invalid_output"` / `escalate_to_human_review` sprang.

---

## 2. Geplante kleine Factory-Änderung für Termin 8 (`F-NEW-T8`)

> **Wichtig:** Diese Änderung wird **erst in Termin 8** (nach Sicherung der `F-BASE`/`Q-BASE`-Baseline) implementiert – nicht vorweg in Termin 7!

1. **Multi-File-Support (begrenzt auf autorisierte `input_files` + `test_targets`) im `backend_agent`:**  
   Erweiterung des JSON-Antwortschemas in `src/agents/backend_agent.py` um ein optionales Feld `"files": [{"path": "...", "code": "..."}]`, abgesichert über `write_target_text_file` + `assert_target_belongs_to_project`, damit der Agent bei Schema-Änderungen wie `R-02` Produktcode (`quotation.py`) und zugehörige Tests (`test_quotation.py`) in einem Schritt konsistent aktualisieren kann.
2. **Einmaliger deterministischer JSON-Repair-Retry (`max_retries=1`) im `requirements_agent`:**  
   Bei leerem oder abgeschnittenem JSON wird genau ein kompakter Retry mit `json_mode=True` ausgelöst, bevor `unparseable` gemeldet wird.

---

## 3. Erwartete Messgrößen im T8-Vergleich (`F-NEW-T8` vs. `F-BASE` auf `R-02`)

| Messgröße | Gemessene Baseline (`F-BASE`, `5ea9dada`) | Erwartung nach Intervention (`F-NEW-T8`) |
| :--- | :---: | :---: |
| **Produkt-/Export-Tests (`pytest` in isolierter Kopie)** | `36 passed, 28 failed` (`exit_code = 1`) | Alle Tests inkl. neuem `calculation_note`-Test bestehen (`exit_code = 0`) |
| **Benötigte LLM-Calls (`R-02`)** | `12` Calls (`2` Backend-Versuche) | `≤ 8` Calls (`1` Backend-Versuch ohne Fehl-Retry) |
| **Agenten-Kosten (`R-02`)** | `18,12 Credits` | `≤ 13,00 Credits` |
| **Menschliche Nacharbeit für fehlende Tests** | Erforderlich (Testdatei nicht mitgeändert) | `0 Min.` (Test automatisch miterzeugt) |
| **`unparseable`-Status in Vorstufen-Agenten** | `> 0` (`status: invalid_output`) | `0` (`status: success`) |
