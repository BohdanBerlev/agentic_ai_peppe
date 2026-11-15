# Evidence Session 6 – Zweiter Kunde HansePack, Multi-Project Factory & Angebotsrechner

**Team:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Datum:** 2026-11-16  
**Kunde:** HansePack Handelsgesellschaft (fiktiv) · Projekt-ID: `client-02`  
**Session:** `session-06`  
**Regelversion:** `HP-V1`  

---

## 1. Repository-Trennung, Commits & Stände (`A1`, `A4`, `B5`, `C1`, `D2`)

| Rolle / Stand | Repository / Branch | Eingabe-Commit | Ergebnis-Commit & Git-Tag |
| :--- | :--- | :--- | :--- |
| **Produkt 01 (Nordwerk Basis)** | `DavidPisark/Nordwerk-Industrie-Service-Website` (`main`) | `f2feebb` (`CR-01-v1.0`) | **`d140f26`** (gesichert, eingefroren, 0 Änderungen durch T6) |
| **Produkt 02 (HansePack)** | `Vanitas50/client-02-quotation` (`main`) | `90953d3` (Kunden-Issue, Tests, Starter) | **`d92d39a`** (`quotation.py` durch Factory implementiert) |
| **Factory Multi-Project** | `BohdanBerlev/agentic_ai_peppe` (`termin-6-hansepack`) | `344df70` (Registry, Trennungstest) | **`a28a182`** (LLM-Robustheit, Session-06-Evidenz) |

---

## 2. Factory: Wiederverwendung, Anpassung & Isolierung (`A1`, `A4`, `C4`, `L6.1`)

### 2.1 Zentrale Projekt-Registry (`A1`)
Die Factory wurde generisch erweitert, um beliebige Kundenprojekte über eine zentrale Registry (`src/projects.py`) anzusprechen. Es gibt **keine zweite hartcodierte Agentenkopie** und **keine zweite Factory**.

- **Wiederverwendete Fähigkeiten:**
  - Komplette 8-Agenten-Pipeline (`src/workflows/feature_pipeline.py`) und Rollenkonfiguration (`organization/roles.yaml`).
  - Agenten-Implementierungen (`product_owner_requirements`, `project_manager`, `software_architect`, `backend_api_engineer`, `qa_test_engineer`, `ai_safety_security_engineer`, `integration_engineer`).
  - LLM-Factory (`src/llm/factory.py`) mit dynamischer Provider-Auswahl (Ollama, Gemini).
  - Sicherheitsmechanismen (`src/agents/common.py` zur Pfadvalidierung).
  - Human Approval Gate und automatische Trace-Aufzeichnung in `evidence/session-06/`.

- **Zentrale Anpassungen:**
  - `src/projects.py`: Zentrale Konfiguration von Checkout-Pfade, GitHub-Repos, Default-Inputs und Test-Skripten.
  - `src/workflows/feature_pipeline.py`: Dynamische Zuweisung von Inputs/Tests anhand der `project_id`.
  - `src/agents/qa_security_agent.py`: Automatisierte Erkennung von `pytest`-Testdateien ohne `__main__`-Block.
  - `src/llm/factory.py` & `src/agents/backend_agent.py`: Absicherung gegen Kontextbeschneidung (`num_ctx=8192`) und robuste JSON-Extraktion (`strict=False`).

### 2.2 Deterministische Kundentrennung (`A4`)
Der Zugriff wird zur Laufzeit technisch durch `assert_target_belongs_to_project(project_id, target_dir)` strikt beschränkt. Ein HansePack-Auftrag kann niemals Nordwerk-Dateien modifizieren.

- **Automatisierter Factory-Test:** `tests/test_project_separation_t6.py` (5/5 Tests bestanden in 4,56s):
  1. `test_hansepack_run_does_not_touch_nordwerk`: Ausführung eines HansePack-Laufs in isolierter Umgebung lässt Nordwerk unberührt.
  2. `test_client02_cannot_target_nordwerk_checkout`: Aufruf mit `client-02` und Ziel `client-01-website` wirft sofort `ValueError`.
  3. `test_client01_cannot_target_hansepack_checkout`: Aufruf mit `client-01` und Ziel `client-02-quotation` wirft sofort `ValueError`.
  4. `test_unknown_project_id_rejected`: Unbekannte Projekt-ID wird abgewiesen.
  5. `test_registry_defaults`: Registry liefert korrekte Defaults für beide Mandanten.

---

## 3. Agentischer Produktbeitrag & Zusammenarbeit (`A2`, `A3`, `L6.2`)

### 3.1 Trace-Evidenz der Factory-Läufe (`A2`, `C1`)

| Parameter | Lauf 1 (Erstlauf / Fehlererkennung) | Lauf 2 (`HP-T6-02` / Verifikationslauf) |
| :--- | :--- | :--- |
| **Workflow-ID** | `fb1d7c6b-6a79-4eab-bc00-0a1fe437daae` | `8f912c03-2c2b-42ca-82ef-304bc0c4f1b9` |
| **Run-ID** | `10bb82fa-d821-440f-9573-012a9265d487` | `1a9a33df-ccbd-4c34-b40b-94f6b3e9c0ad` |
| **Trace-Datei** | [`evidence/session-06/fb1d7c6b-6a79-4eab-bc00-0a1fe437daae.jsonl`](session-06/fb1d7c6b-6a79-4eab-bc00-0a1fe437daae.jsonl) | [`evidence/session-06/8f912c03-2c2b-42ca-82ef-304bc0c4f1b9.jsonl`](session-06/8f912c03-2c2b-42ca-82ef-304bc0c4f1b9.jsonl) |
| **Provider / Modell** | Local Ollama (`qwen3.5:9b`, `num_ctx=8192`) | Local Ollama (`qwen3.5:9b`, `num_ctx=8192`) |
| **Status** | `qa_failed` (Katalog-Schema nicht als Liste geparst) | `success` (Alle Tests grün, Human Gate freigegeben) |
| **Laufzeit** | 59,8 s | 75,1 s |
| **Kosten (Credits)** | 9,53 Credits | 8,08 Credits |

### 3.2 Strukturierte Datenübergabe & Bounded Loops (`A3`)
In der Full-Company-Pipeline übergeben mindestens 8 Agentenrollen strukturierte Artefakte:
1. `product_owner_requirements`: Parst `issue_hp01.md`, extrahiert Akzeptanzkriterien für HP-BOX und Regelversion HP-V1.
2. `project_manager`: Erstellt Aufgabenplan mit Priorisierung Q01, Q03, E01.
3. `software_architect`: Definiert Funktionssignatur `calculate_quote(items, rule_version)` und Exception-Hierarchie (`QuotationError`).
4. `backend_api_engineer`: Implementiert `quotation.py` inklusive `load_catalog()` und Rundungslogik (`ROUND_HALF_UP`).
5. `qa_test_engineer`: Führt automatisierte Produkttests `test_quotation.py` aus.
6. `ai_safety_security_engineer`: Prüft auf Pfadtraviersierung und deterministische Ausführung.
7. `integration_engineer`: Bereitet Diff und Commit-Vorschlag vor.
8. `human_approval_gate`: Menschliche Freigabeentscheidung durch Lars Boos gebunden an Testergebnis.

---

## 4. Kundenprodukt HansePack (`B1`–`B6`, `L6.3`)

### 4.1 Deterministische Produktlogik (`B1`)
- `quotation.py` lädt Artikelpreise ausschließlich aus `fixtures/HansePack_Katalog.json`.
- **Kein LLM zur Laufzeit:** Die Preisberechnung ist vollständig deterministisch in Python umgesetzt.
- Alle Beträge werden in ganzzahligen Cents (`int`) geführt, Rundungen erfolgen kaufmännisch (`ROUND_HALF_UP`).

### 4.2 Nachweis der Pflichtfälle (`B2`–`B4`)
Automatisierte Prüfung via `test_quotation.py` im Produkt-Repository `client-02-quotation`:

| Testfall | Geprüfte Werte | Ergebnis |
| :--- | :--- | :--- |
| **Q01 (`B2`)** | `HP-BOX` × 1: Warenwert 250 Cent, Versand 1200 Cent, Gesamt **1450 Cent** | ✅ **PASSED** |
| **Q03 (`B3`)** | `HP-BOX` × 50: Listenbetrag 12500 Cent, 5 % Rabatt (-625 Cent), Warenwert 11875 Cent, Versand 1200 Cent, Gesamt **13075 Cent** | ✅ **PASSED** |
| **E01 (`B4`)** | `HP-BOX` × 0: Zurückweisung mit `QuotationError("quantity_out_of_range")`, kein Angebot | ✅ **PASSED** |

CLI-Aufrufnachweis:
```bash
python quotation.py HP-BOX 1
# -> {"goods_net_cents": 250, "shipping_cents": 1200, "total_cents": 1450, ...}

python quotation.py HP-BOX 50
# -> {"lines": [{"list_amount_cents": 12500, "discount_cents": 625, ...}], "total_cents": 13075}

python quotation.py HP-BOX 0
# -> Exit-Code 1, stderr: "Fehler: Menge für HP-BOX (0) liegt außerhalb des erlaubten Bereichs (1-10000)."
```

### 4.3 Unverändertes Altprodukt Nordwerk (`B5`)
- Der Nordwerk-Produktstand ist auf Commit **`d140f26`** (`main`) gesichert.
- Unveränderter Prüfnachweis (`python test_website.py`):
  ```text
  PASSED F1 Pflichtinhalt (AC-01..AC-04)
  PASSED F2 Kontakt & Navigation (AC-04, AC-05)
  PASSED F3 Lokale Verweise & Assets / PHP-frei (AC-05, AC-08)
  PASSED F4 Bedienbarkeit statisch (AC-06/AC-07)
  ERGEBNIS: ALLE PRUEFFAMILIEN BESTANDEN
  ```

### 4.4 Kundenauftrag & Fixtures (`B6`)
- Spezifikation in `issue_hp01.md` mit klaren Annahmen (A1–A5), offenen Fragen (F1–F4) und Lieferplan.
- Fixtures `fixtures/HansePack_Katalog.json` und `fixtures/HansePack_Referenzfaelle.json` stammen unverändert aus Kurs-Commit `f66013c` (verifiziert via SHA256 in `fixtures/SHA256SUMS`).

---

## 5. Kosten, Messung & Planung (`C1`–`C4`, `L6.4`)

### 5.1 Zeit- und Kostenaufstellung (`C2`)
- **Menschliche Arbeitszeit (exklusiv erfasst):**
  - Projektstart & Analyse Kundenbriefing HansePack: ~45 Min.
  - Implementierung Registry & Trennungstest (`A1`, `A4`): ~30 Min.
  - Review & Fehlerkorrektur JSON-Parsing / Kontextgröße: ~30 Min.
  - Freigabe & Evidenzsicherung: ~15 Min.
- **Agenten-Laufzeiten & Fehlläufe:**
  - Lauf 1 (`fb1d7c6b...`, Fehllauf wg. Katalog-Schema): 59,8 s | 9,53 Credits
  - Lauf 2 (`8f912c03...`, Verifikationslauf `HP-T6-02`): 75,1 s | 8,08 Credits
  - Gesamtverbrauch Session 6: **17,61 Credits**

### 5.2 Lieferplanung T6–T8 (`C3`)
- **Termin 6 (Heute):** Kernlogik Angebotsberechnung (HP-BOX mit Q01, Q03, E01) als eigenständig ausführbares Python-Modul mit CLI und Tests.
- **Termin 7:** Ausbau aller Referenzfälle Q01–Q14 und Fehlerfälle E01–E10, browserbasierte Weboberfläche, JSON-Export, vollständige CI/CD-Pipeline.
- **Termin 8:** Reserve für Kundenänderung CR-02 (dynamische Versandkostenstaffel HP-V2) und finale Abnahme.

### 5.3 Reuse-Lernen & Schwachstellenanalyse (`C4`)
- **Was ließ sich wiederverwenden?**
  Die gesamte Multi-Agenten-Orchestrierung (LangGraph-Workflow, Rollenhierarchie, Prompt-Templates, Tool-Aufrufe und Sicherheitschecks) konnte zu 100 % für das neue Projekt übernommen werden.
- **Was war kundenspezifisch?**
  Pfade, Repositories, Testskripte sowie die Schema-Definition der Ein- und Ausgabedaten (`quotation.py` vs. statische HTML-Seiten).
- **Konkrete untersuchte Schwachstelle:**
  Bei lokalen LLMs (`qwen3.5:9b`) führte das Einspeisen vollständiger Fixture-JSONs bei standardmäßigem Kontextfenster (4.096 Tokens) zum vorzeitigen Abbruch der Modell-Ausgabe (`truncated=1`), wodurch JSON-Strings unvollständig blieben. Durch Anhebung des Kontextfensters auf `num_ctx=8192` und eine fehlertolerante JSON-Bereinigung (`strict=False` mit Regex-Fallback) wurde das Problem nachhaltig gelöst.

---

## 6. Menschliche Verantwortung & Freigabe (`D1`)

- **Reviewer:** Lars Boos (`lars.boos@haw-hamburg.de`)
- **Geprüfter Diff:** `git diff 90953d3..d92d39a` im Repository `client-02-quotation`.
- **Entscheidung:** **APPROVED** am 2026-11-16.
- **Begründung:** Fachlogik erfüllt alle Rechenregeln nach `HP-V1`, Produkttests (Q01, Q03, E01) und Factory-Trennungstests laufen deterministisch fehlerfrei durch.

---

## 7. Höchstens drei nächste Schritte für Termin 7 (`D2`)

1. **Web-Frontend realisieren:** Erstellung der responsiven, barrierefreien Browseroberfläche für HansePack zur interaktiven Angebotserstellung.
2. **Vollständige Testabdeckung:** Erweiterung der Testsuite auf alle Referenzfälle Q01–Q14 sowie alle Fehlerfälle E01–E10.
3. **JSON-Export & Download:** Bereitstellung des standardkonformen JSON-Downloads der kalkulierten Angebote.
