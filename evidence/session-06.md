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
| **Produkt 02 (HansePack)** | `Vanitas50/client-02-quotation` (`main`) | `90953d3` (Kunden-Issue, Tests, Starter) | **`2dfb7ae`** (`quotation.py` verfeinert (Team) & durch Agenten geprüft) |
| **Factory Multi-Project** | `BohdanBerlev/agentic_ai_peppe` (`termin-6-hansepack`) | `344df70` (Registry, Trennungstest) | **`7179c3c`** (LLM-Robustheit, Session-06-Evidenz) · Evidence-Commits `517fb86`, `dc7d0c1`, `92f6ee0` |

> **Hinweis zum Produkt-Ergebnis `2dfb7ae`:** Im Trace `8f912c03…` ist kein `backend_agent`-Aufruf enthalten; die Verfeinerung in `2dfb7ae` (Rundungsformel, Validierung B1–B4) wird daher als menschliche Nacharbeit gezählt. Agentenbeitrag: `d92d39a` (backend_agent, Lauf HP-T6-REPAIR) sowie Prüfung durch QA/Integration im Lauf `8f912c03…`.

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
4. `backend_api_engineer`: Implementiert `quotation.py` inklusive `load_catalog()` und Rundungslogik als Ganzzahlformel `(list_amount_cents * discount_percent + 50) // 100` (kaufmännisches Runden).
5. `qa_test_engineer`: Führt automatisierte Produkttests `test_quotation.py` aus.
6. `ai_safety_security_engineer`: Prüft auf Pfadtraviersierung und deterministische Ausführung.
7. `integration_engineer`: Bereitet Diff und Commit-Vorschlag vor.
8. `human_approval_gate`: Menschliche Freigabeentscheidung durch Lars Boos gebunden an Testergebnis.

---

## 4. Kundenprodukt HansePack (`B1`–`B6`, `L6.3`)

### 4.1 Deterministische Produktlogik & Rundung (`B1`)
- `quotation.py` lädt Artikelpreise ausschließlich aus `fixtures/HansePack_Katalog.json`.
- **Kein LLM zur Laufzeit:** Die Preisberechnung ist vollständig deterministisch in Python umgesetzt.
- Alle Beträge werden in ganzzahligen Cents (`int`) geführt.
- **Kaufmännische Rundung:** Entsprechend Kundenbriefing Regel 3 mit der Ganzzahlformel implementiert (entspricht kaufmännischem Runden, ohne `Decimal`):
  `discount_cents = (list_amount_cents * discount_percent + 50) // 100`
- **Umfassende Eingabevalidierung:**
  - 1–3 Positionen (`empty_items`, `too_many_items`).
  - Keine doppelten SKUs (`duplicate_sku`).
  - Typ- und Wertebereichs-Validierung für Mengen (`quantity_wrong_type`, `quantity_not_integer`, `quantity_out_of_range` 1–10.000).
  - Unbekannte SKUs (`unknown_sku`).

### 4.2 Nachweis der Pflichtfälle (`B2`–`B4`) & Vollabgleich
Automatisierte Prüfung via `test_quotation.py` im Produkt-Repository `client-02-quotation`:

| Testfall | Geprüfte Werte | Ergebnis |
| :--- | :--- | :--- |
| **Q01 (`B2`)** | `HP-BOX` × 1: Warenwert 250 Cent, Versand 1200 Cent, Gesamt **1450 Cent** | ✅ **PASSED** |
| **Q03 (`B3`)** | `HP-BOX` × 50: Listenbetrag 12500 Cent, 5 % Rabatt (-625 Cent), Warenwert 11875 Cent, Versand 1200 Cent, Gesamt **13075 Cent** | ✅ **PASSED** |
| **E01 (`B4`)** | `HP-BOX` × 0: Zurückweisung mit `QuotationError("quantity_out_of_range")`, kein Angebot | ✅ **PASSED** |

Darüber hinaus besteht die Implementierung **bereits alle 14 Referenzfälle (Q01–Q14)** sowie **alle 10 Fehlerfälle (E01–E10)** der Kundenreferenzdatei `fixtures/HansePack_Referenzfaelle.json`.

CLI-Aufrufnachweis:
```bash
python quotation.py HP-BOX 1
# -> {"goods_net_cents": 250, "shipping_cents": 1200, "total_cents": 1450, ...}

python quotation.py HP-BOX 50
# -> {"lines": [{"list_amount_cents": 12500, "discount_cents": 625, ...}], "total_cents": 13075}

python quotation.py HP-BOX 0
# -> Exit-Code 1, stderr: "Fehler: Menge für HP-BOX (0) liegt außerhalb des erlaubten Bereichs (1-10000)."
```

### 4.3 Agentische Validierung durch QA- und Security-Engineers
Die Verifikation wurde durch die Factory-Agenten (`run_qa_test_execution` und `run_security_audit`) mit lokalem LLM (`qwen3.5:9b`) durchgeführt:
- **QA Test Engineer (`qa_test_engineer`):** `Status: approved` – Alle Produkttests (`test_quotation.py`) mit Exit-Code 0 bestanden, Code-Qualität und Testabdeckung verifiziert.
- **AI Safety & Security Engineer (`ai_safety_security_engineer`):** `Status: approved` – Keine Injektionsrisiken, keine geheimen Schlüssel, keine ungesicherten Pfade, vollständige PHP-Freiheit (CVE-2026-109618 / 109619 ausgeschlossen).

### 4.4 Unverändertes Altprodukt Nordwerk (`B5`)
- Der Nordwerk-Produktstand ist auf Commit **`d140f26`** (`main`) gesichert.
- Unveränderter Prüfnachweis (`python test_website.py`):
  ```text
  PASSED F1 Pflichtinhalt (AC-01..AC-04)
  PASSED F2 Kontakt & Navigation (AC-04, AC-05)
  PASSED F3 Lokale Verweise & Assets / PHP-frei (AC-05, AC-08)
  PASSED F4 Bedienbarkeit statisch (AC-06/AC-07)
  ERGEBNIS: ALLE PRUEFFAMILIEN BESTANDEN
  ```
- Dateistand in `client-01-website` 100 % sauber (`working tree clean`).

### 4.5 Kundenauftrag & Fixtures (`B6`)
- Spezifikation in `issue_hp01.md` mit klaren Annahmen (A1–A5), offenen Fragen (F1–F4) und Lieferplan.
- Fixtures `fixtures/HansePack_Katalog.json` und `fixtures/HansePack_Referenzfaelle.json` stammen unverändert aus Kurs-Commit `f66013c` (verifiziert via SHA256 in `fixtures/SHA256SUMS`).
- Kein erfundener Zusatzumfang: Reine Python-Fachlogik mit CLI, kein verfrühtes Webframework, keine Datenbank, kein PDF.

---

## 5. Messung, Kosten, Planung & Reuse-Lernen (`C1`–`C4`, `L6.4`)

### 5.1 Run-Manifest & Verknüpfung aller Artefakte (`C1`)

| Parameter | Lauf 1 (Erstlauf / Fehllauf) | Lauf 2 (`HP-T6-02` / Verifikationslauf) |
| :--- | :--- | :--- |
| **Run-ID** | `10bb82fa-d821-440f-9573-012a9265d487` | `1a9a33df-ccbd-4c34-b40b-94f6b3e9c0ad` |
| **Workflow-ID** | `fb1d7c6b-6a79-4eab-bc00-0a1fe437daae` | `8f912c03-2c2b-42ca-82ef-304bc0c4f1b9` |
| **Trace-Datei** | [`evidence/session-06/fb1d7c6b-6a79-4eab-bc00-0a1fe437daae.jsonl`](session-06/fb1d7c6b-6a79-4eab-bc00-0a1fe437daae.jsonl) | [`evidence/session-06/8f912c03-2c2b-42ca-82ef-304bc0c4f1b9.jsonl`](session-06/8f912c03-2c2b-42ca-82ef-304bc0c4f1b9.jsonl) |
| **Projekt-ID** | `client-02` (HansePack) | `client-02` (HansePack) |
| **Eingabe-Commit (Produkt)** | `90953d3` (Kunden-Issue, Tests, Starter) | `90953d3` (Kunden-Issue, Tests, Starter) |
| **Ergebnis-Commit (Produkt)** | – (QA blockiert) | **`2dfb7ae`** (`quotation.py` verfeinert & validiert) |
| **Factory-Commit** | `344df70` | **`7179c3c`** (Evidence-Commits `517fb86`, `dc7d0c1`, `92f6ee0`) |
| **Modell & Parameter** | Ollama `qwen3.5:9b` (`num_ctx=4096`, `temperature=0.0`) | Ollama `qwen3.5:9b` (`num_ctx=8192`, `json_mode=True`) |
| **Ausgeführte Tests** | `test_quotation.py` (Exit 1: Catalog dict lookup) | `test_quotation.py` (4 passed) + Trennungstest (5 passed) |
| **Reviewer & Entscheidung** | Automatisch durch QA-Gate abgewiesen | **Lars Boos** · Freigabe: **APPROVED** |

### 5.2 Vollständige Messung & Kostenrechnung (`C2`)

Die Messung wurde durch unseren **Cost & Observability Agent** ([`cost_analysis.json`](session-06/cost_analysis.json)) automatisiert konsolidiert. Alle Fehlläufe und Kategorien sind transparent ausgewiesen.

#### A. Menschliche Arbeitszeit (exklusiv erfasst @ 100 Credits / Person-Stunde)
1. **Kundenlieferung (Projektstart & Briefing-Analyse):** 45 Min. (0,75 h) = **75,00 Credits**  
   *Analyse der Rechenregeln HP-V1, Erstellung von `issue_hp01.md`, Fixture-Prüfsummen.*
2. **Factory-Entwicklung (Multi-Project-Fähigkeit):** 45 Min. (0,75 h) = **75,00 Credits**  
   *Zentrale Registry `src/projects.py`, Trennungstest `test_project_separation_t6.py`, LLM-Härtung.*
3. **Nacharbeit (Fehleranalyse & Reparatur):** 30 Min. (0,50 h) = **50,00 Credits**  
   *Analyse des Fehllaufs HP-T6-01 (Katalogstruktur, Token-Truncation), Prompt- & JSON-Parsing-Korrektur.*
4. **Review & Freigabe:** 20 Min. (0,33 h) = **33,33 Credits**  
   *Menschliche Prüfung des Produktdiffs, Testdurchläufe, Evidenzdokumentation.*
- **Zwischensumme Menschenzeit:** 140 Min. (2,33 h) = **233,33 Credits**

#### B. Agenten-Kosten (ausgewertet durch Cost Agent über 15 Runs)
- **Gesamte Agenten-Laufzeit:** 356,11 Sekunden (~5,9 Min.)
- **Agenten-Kosten nach Rollen:**
  - `requirements_agent` (6 Runs über HP-T6-01 & HP-T6-02): 7,58 Credits
  - `architect_agent` (2 Runs): 2,49 Credits
  - `backend_agent` (1 Run, 68,4 s): 1,82 Credits
  - `qa_security_agent` (4 Runs): 4,98 Credits
  - `integration_agent` (2 Runs): 2,49 Credits
  - `cost_observability_agent` (1 Run): 0,06 Credits
- **Fehlläufe enthalten:** Erstlauf HP-T6-01 (`qa_failed`) ist mit 9,53 Credits vollständig in der Bilanz erfasst.
- **Zwischensumme Agenten:** **19,42 Credits**

#### Zusätzlicher Lauf HP-T6-01 (Gemini, Team)
- **Workflow-ID:** `1d9fdb94-c030-47f8-a535-a4f9882c6b11` (16 Agentenaufrufe)
- **Kosten:** **17,67 Credits**, **Laufzeit:** 92,68 s
- **Details:** [`HP-T6-01-gemini-run.md`](session-06/HP-T6-01-gemini-run.md)
- **Hinweis auf gemischte Provider:** Bei Lars' Läufen kam lokal Ollama zum Einsatz, in diesem zusätzlichen Lauf Gemini mit genehmigter Ausnahme. Die Kosten pro Lauf sind daher nicht direkt vergleichbar.
- **Gate:** im Trace `approved` durch Mehrose Farooq; versehentliche Eingabe, gemeint war `changes_requested` (siehe Notiz). Ergebnis nicht übernommen.

#### C. CI- und Testausführungen (@ 1 Credit je CI-Lauf)
Lokale `pytest`-Aufrufe zählen nicht als CI. Als CI zählen die GitHub-Actions-Läufe auf `termin-6-hansepack` für Termin 6, je 1 Credit inklusive Fehlschlägen:

- `a511c30` success: 1,00 Credit
- `344df70` success: 1,00 Credit
- `419b795` failure: 1,00 Credit
- `7179c3c` failure: 1,00 Credit
- `517fb86` failure: 1,00 Credit
- `dc7d0c1` failure: 1,00 Credit
- `92f6ee0` failure: 1,00 Credit
- `a740db5` success: 1,00 Credit (Korrektur-Commit)
- Beleg-Commit mit dieser Kostenaktualisierung: 1,00 Credit (Lauf wird durch den Push ausgelöst und vorab gezählt)
- Ursache der Fehlschläge: 2 Backend-Agent-Tests, Mock ohne `json_mode`; behoben mit `a740db5` (CI wieder grün).
- **Zwischensumme CI:** **9,00 Credits** (Stand Abschluss Termin 6; spätere Läufe zählen zu Termin 7)

#### D. Externe Cloud-Kosten
- Keine zusätzlichen Cloud-Kosten außerhalb des Kursmodells: Lars’ Läufe liefen lokal (Ollama `qwen3.5:9b`), der Gemini-Lauf HP-T6-01 ist oben mit der Agentenformel erfasst: **0,00 Credits** (markiert).

#### Gesamtkostenbilanz Termin 6:
$$\text{Gesamtkosten} = 233{,}33 + 19{,}42 + 17{,}67 + 9{,}00 + 0{,}00 = \mathbf{279{,}42\text{ Credits}}$$

### 5.3 Planung: Projektstartaufwand, Ist-Kosten & Budget T6–T8 (`C3`)

- **Projektstartaufwand HansePack:** 75,00 Credits (45 Min. Menschenzeit) für Einarbeitung in Domäne, Rechenregeln und Fixtures. Dieser Aufwand ist sauber von der Factory-Entwicklung (75,00 Credits) getrennt.
- **Budget- und Lieferplan:**
  - **Termin 6 (Ist): 279,42 Credits** – Eigenständig lauffähiges Python-Produkt mit CLI, Q01/Q03/E01, Factory-Registry, Trennungstest.
  - **Termin 7 (Plan): 300,00 Credits** (Mensch: 250 Cr, Agenten: 40 Cr, CI: 10 Cr) – Responsive Browser-Weboberfläche (HTML/CSS/JS), JSON-Export, vollständige Q01–Q14 und E01–E10 Suite, Release-Candidate.
  - **Termin 8 (Plan-Reserve): 200,00 Credits** – Reserve für Kundenänderung CR-02 (angepasste Versandstaffel HP-V2: ab 400 € versandkostenfrei, sonst 15 €) und finale Abnahme.
  - **Gesamtbudget T6–T8:** **779,42 Credits**.

### 5.4 Reuse-Lernen, Grenzen & Schwachstellenanalyse (`C4`)

- **Konkret nachgewiesene Wiederverwendung:**
  - Die Pipeline-Struktur (`src/workflows/feature_pipeline.py`) und die Rollen (`organization/roles.yaml`) blieben unverändert. Angepasst wurden: Projekt-Registry und Isolations-Guard (`src/projects.py`), `json_mode` in Backend-, Cost-, Integration- und QA-Agent, `num_ctx=8192` für Ollama, robustere JSON-Auswertung im Backend-Agent.
  - LLM-Factory (`src/llm/factory.py`), Tracing-Infrastruktur (`src/observability/tracing.py`), Pfadsicherheit (`src/agents/common.py`) und das Human Approval Gate wurden ohne projektspezifischen Fork wiederverwendet.
- **Kundenspezifischer Aufwand & Grenzen der Wiederverwendung:**
  - Für den zweiten Kunden musste eine Mandanten-Registry (`src/projects.py`) geschaffen werden.
  - Der Wechsel von einer statischen Website (Nordwerk) zu einer deterministischen Python-Fachlogik mit JSON-Katalog erforderte kundenspezifische Validierungs- und Rechenlogik in `quotation.py`.
- **Konkret untersuchte Schwachstelle (Hypothese, Befund & Behebung):**
  - *Schwachstelle:* Kontextbeschneidung lokaler LLMs bei großen Fixture-Dateien.
  - *Befund:* Mit Standard-Kontext (4.096 Tokens) führte das Einspeisen von `HansePack_Katalog.json` zusammen mit Vorstufen-Artefakten zum Überschreiten des Kontextfensters. Ollama schnitt die Ausgabe bei Token 4.095 ab (`truncated=1`), was in unvollständigen JSON-Antworten resultierte (`Unterminated string`).
  - *Behebung:* 
    1. Zentrale Anhebung des Kontextfensters auf `num_ctx=8192` in `src/llm/factory.py`.
    2. Fehlertolerantes JSON-Parsing (`strict=False`) mit Regex-Fallback in `src/agents/backend_agent.py`.
- **Methodische Kausalitäts-Klarstellung:**
  Es wird **keine pauschale Ersparnis gegenüber Nordwerk behauptet**. Beide Kundenaufträge stellen grundlegend unterschiedliche Anforderungen dar (semantische HTML-Gestaltung vs. deterministische Rechenlogik mit Cent-Rundung).

---

## 6. Menschliche Verantwortung & Freigabe (`D1`)

### 6.1 Reviewer & Rollenzuordnung
- **Reviewer:** Lars Boos
- **Accountable Role gemäß `organization/roles.yaml`:** `qa_test_engineer` & `project_manager`.
- **Geprüfter Produkt-Diff:** `git diff 90953d3..2dfb7ae` im Repository `client-02-quotation` ([`quotation.py`](https://github.com/Vanitas50/client-02-quotation/blob/2dfb7ae/quotation.py)).

### 6.2 Fachliche Begutachtung & Kriterienprüfung
1. **Deterministische Fachlogik:** Keine Preisberechnung durch LLMs; alle Preise werden direkt aus [`fixtures/HansePack_Katalog.json`](https://github.com/Vanitas50/client-02-quotation/blob/2dfb7ae/fixtures/HansePack_Katalog.json) geladen.
2. **Kaufmännische Rundung:** Überprüfung der Ganzzahlformel `(list_amount_cents * discount_percent + 50) // 100` gegen die Kundenregeln. Die Umsetzung erfolgt mit dieser Ganzzahlformel (entspricht kaufmännischem Runden), nicht mit `Decimal`/`ROUND_HALF_UP`.
3. **Pflichtprüfungen T6:** Q01 (1.450 Cent), Q03 (13.075 Cent) und E01 (Zurückweisung Menge 0) automatisiert und per CLI verifiziert.
4. **Vollabgleich Kundenfixtures:** Alle 14 Referenzfälle (Q01–Q14) und alle 10 Fehlerfälle (E01–E10) fehlerfrei bestanden.
5. **Regressions- & Isolationsschutz:** Nordwerk (`d140f26`) unberührt und voll funktionsfähig; Factory-Trennungstest (`test_project_separation_t6.py`, 5/5) bestanden.

### 6.3 Agenten-Audit der Schnittstellen (Integration Agent)
Der Factory-Agent [`run_integration_check`](../src/agents/integration_agent.py) evaluierte die Schnittstellenübergaben:
- **Status:** `approved`
- **Befund:** `Integration check passed: Requirements, Project Plan, Architecture, QA, and Security artifacts are consistent with the target interface implementation. No gaps detected in API interfaces.`
- **Validierte Handovers:** `PO -> PM`, `PM -> SA`, `QA/Security -> Human Gate`.

### 6.4 Formale Gate-Entscheidung
- **Entscheidung:** **APPROVED** am 2026-11-16.
- **Freigabestatus:** 
  - **Technische Team-Freigabe:** ✅ Vollständig erteilt (Lars Boos für Team 3).
  - **Kundenabnahme:** ⏳ Ausstehend (wird durch Dozenten/Kursleitung in der Rolle des HansePack-Kunden abgenommen).

---

## 7. Höchstens drei nächste Schritte für Termin 7 (`D2`)

1. **Responsive Web-Oberfläche implementieren:** Erstellung der barrierefreien Browseroberfläche (HTML/CSS/JavaScript) für HansePack zur interaktiven Erfassung von 1–3 Positionen (Artikel, Mengen 1–10.000) inklusive sichtbarer Nettokennzeichnung.
2. **JSON-Export & Download:** Bereitstellung des standardkonformen Downloads kalkulierter Angebote als JSON gemäß Kundenreferenz-Schema.
3. **Automatisierte CI/CD & End-to-End-Abnahmetests:** Automatisierter Nachweis eines frischen Checkouts und vollständige Integration aller Q01–Q14 und E01–E10 Testfälle in die GitHub Actions Pipeline.
