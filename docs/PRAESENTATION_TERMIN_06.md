# Termin 6 – Zweiter Kunde HansePack, dieselbe Factory: Technische Gesamterklärung & Präsentationsleitfaden

**Projekt:** Agentic AI Software Factory (HAW Hamburg, Wintersemester 2026/27)  
**Team 3 (PepeGroup):** David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq  
**Datum:** 16. November 2026  
**Zielgruppe dieses Dokuments:** Das ganze Team (Vorbereitung und Durchführung der Abnahme)

---

## Inhaltsverzeichnis
1. [Management Summary (Der 60-Sekunden-Elevator-Pitch)](#1-management-summary-der-60-sekunden-elevator-pitch)
2. [Was konkret getan wurde: Detaillierte Rekonstruktion (Bereiche A–D)](#2-was-konkret-getan-wurde-detaillierte-rekonstruktion-bereiche-ad)
   - [Bereich A: Factory & Multi-Project-Architektur (40 Punkte)](#bereich-a-factory--multi-project-architektur-40-punkte)
   - [Bereich B: Kundenprodukt HansePack (30 Punkte)](#bereich-b-kundenprodukt-hansepack-30-punkte)
   - [Bereich C: Messung, Kosten & Reuse-Lernen (20 Punkte)](#bereich-c-messung-kosten--reuse-lernen-20-punkte)
   - [Bereich D: Verantwortung & Übergabe (10 Punkte)](#bereich-d-verantwortung--übergabe-10-punkte)
3. [Präsentationsleitfaden für die Dozentenabnahme](#3-präsentationsleitfaden-für-die-dozentenabnahme)
   - [Vorgeschlagene Demostruktur (5–7 Minuten)](#vorgeschlagene-demostruktur-57-minuten)
   - [Live-Befehle für das Terminal (Copy & Paste bereit)](#live-befehle-für-das-terminal-copy--paste-bereit)
4. [Antizipierte Dozentenfragen & perfekte Antworten (FAQ / Grill-Me Schutz)](#4-antizipierte-dozentenfragen--perfekte-antworten-faq--grill-me-schutz)
5. [Git-Commit-Matrix & Verzeichnisübersicht](#5-git-commit-matrix--verzeichnisübersicht)

---

## 1. Management Summary (Der 60-Sekunden-Elevator-Pitch)

> *„Herr Professor / Herr Dozent, heute haben wir bewiesen, dass unsere Software Factory ein echter Mehr-Mandanten-Dienstleister ist und kein Einweg-Skript für Nordwerk:*
> 1. *Wir haben **keine neue Factory gebaut** und **keine Agenten dupliziert**. Über eine zentrale Registry (`src/projects.py`) konfigurieren wir HansePack als neuen Mandanten, während ein technischer Isolations-Guard (`assert_target_belongs_to_project`) absolut garantiert, dass Nordwerk-Dateien unberührt bleiben.*
> 2. *Unsere Factory hat über eine 8-Agenten-Pipeline (`src/workflows/feature_pipeline.py`) mit lokalem Ollama (`qwen3.5:9b`) die erste Version des neuen Angebotsrechners (`quotation.py`, Commit `d92d39a`) erzeugt. Das Team hat diese Fassung anschließend verfeinert (`2dfb7ae`, als Menschenarbeit gezählt), die Agenten haben das Ergebnis geprüft. Zusätzlich gab es einen verworfenen Gemini-Lauf (`HP-T6-01`).*
> 3. *Die Berechnung ist 100 % deterministisch ohne LLM zur Laufzeit. Alle Cent-Werte, kaufmännisches Runden über die Ganzzahlformel und Mengenrabatte stimmen auf den Cent genau – nicht nur für die heutigen Pflichtfälle Q01, Q03 und E01, sondern bereits für **alle 14 Referenzfälle (Q01–Q14)** und **alle 10 Fehlerfälle (E01–E10)** der Kundenfixtures.*
> 4. *Alle Agentenläufe wurden durch unseren **Cost & Observability Agent** forensisch analysiert (37,09 Credits Agentenkosten: 19,42 aus Lars' Läufen und 17,67 aus dem Gemini-Lauf HP-T6-01; 279,42 Credits Gesamtkosten inkl. menschlicher Zeit und CI).“*

---

## 2. Was konkret getan wurde: Detaillierte Rekonstruktion (Bereiche A–D)

### Bereich A: Factory & Multi-Project-Architektur (40 Punkte)
*Fokus: Projektwechsel, generische Wiederverwendung und technische Mandantentrennung (Lernziele L6.1 & L6.2).*

1. **Mandanten-Registry statt hartcodierter Pfade (`src/projects.py`):**
   - Statt Pfade für Nordwerk hart im Code zu belassen oder einen zweiten Satz an Agenten anzulegen, wurde ein zentrales Registrierungsmodul (`ProjectConfig`) geschaffen.
   - Konfiguriert Mandant 01 (`client-01`, Nordwerk) und Mandant 02 (`client-02`, HansePack) mit eigenem Checkout-Verzeichnis, GitHub-Repository, Default-Input-Dateien und Default-Test-Zielen.
2. **Technischer Isolations-Guard (`assert_target_belongs_to_project`):**
   - In `src/workflows/feature_pipeline.py` wird vor jedem Schreibvorgang strikt geprüft, ob der Zielordner zur autorisierten Mandantenkennung passt.
   - Ein Aufruf von `client-02` mit Ziel `client-01-website` wirft sofort einen harten `ValueError` und blockiert die Ausführung.
3. **Automatisierter Projekt-Trennungstest (`tests/test_project_separation_t6.py`):**
   - 5 automatisierte Tests prüfen in temporären Verzeichnissen deterministisch:
     - Ein HansePack-Lauf modifiziert keine Nordwerk-Dateien.
     - Mandant 02 darf nicht in Mandant 01 schreiben (und umgekehrt).
     - Unbekannte Projekt-IDs werden abgewiesen.
     - Die Registry liefert konsistente Defaults.
   - Ergebnis: **5 von 5 Tests bestanden** in 2,88 s.
4. **Realer LLM-Provider-Lauf mit strukturierter Datenübergabe:**
   - Provider: Lokales Ollama mit Modell `qwen3.5:9b`.
   - Durchlauf über die 8 Rollen der Company-Pipeline: PO (`requirements_agent`) $\rightarrow$ PM (`project_manager`) $\rightarrow$ Architekt (`architect_agent`) $\rightarrow$ Backend (`backend_agent`) $\rightarrow$ QA (`qa_security_agent`) $\rightarrow$ Security (`ai_safety_security_engineer`) $\rightarrow$ Integration (`integration_agent`) $\rightarrow$ Human Gate (`human_approval_gate`).
   - Alle Zwischenzustände wurden als strukturierte JSON-Artefakte im Graph übergeben und im Trace gesichert.
   - Pipeline-Struktur (`src/workflows/feature_pipeline.py`) und Rollen (`organization/roles.yaml`) blieben unverändert; angepasst wurden: Projekt-Registry und Isolations-Guard (`src/projects.py`), `json_mode` in Backend-, Cost-, Integration- und QA-Agent, `num_ctx=8192` für Ollama und eine robustere JSON-Auswertung im Backend-Agent. Keine Agenten wurden kopiert.

---

### Bereich B: Kundenprodukt HansePack (30 Punkte)
*Fokus: Deterministische Python-Berechnung, Kundenkatalog und unabhängige Tests (Lernziel L6.3).*

1. **Vollständig deterministischer Fachcode (`quotation.py`):**
   - **Kein LLM zur Laufzeit:** Die Angebotskalkulation erfolgt in reinem Python (Standardbibliothek `json`, `os`, `sys`).
   - **Katalog-Bindung:** Preise werden dynamisch aus `fixtures/HansePack_Katalog.json` geladen (`load_catalog()`). Keine Preise sind im Code hartcodiert.
   - **Cent-Genauigkeit & Kaufmännische Rundung (Ganzzahlformel):**  
     Implementierung der vom Kundenbriefing geforderten Ganzzahl-Formel für halbe Cent:
     $$\text{discount\_cents} = \frac{\text{list\_amount\_cents} \times \text{discount\_percent} + 50}{100}$$
     Damit werden z. B. 1.237,5 Cent exakt auf 1.238 Cent gerundet (Fall Q04) und 662,5 Cent auf 663 Cent (Fall Q14).
   - **Arbeitsteilung:** Die erste Version (`d92d39a`) erzeugte der `backend_agent`; die Verfeinerung (Rundungsformel, Validierung B1–B4) in `2dfb7ae` ist Team-Arbeit.
2. **Abdeckung aller Testfälle (Pflicht & Vollabgleich):**
   - **Q01 (HP-BOX × 1):** Warenwert 250 Cent, Versand 1.200 Cent, Gesamt **1.450 Cent**.
   - **Q03 (HP-BOX × 50):** Listenbetrag 12.500 Cent, 5 % Rabatt (-625 Cent), Warenwert 11.875 Cent, Versand 1.200 Cent, Gesamt **13.075 Cent**.
   - **E01 (HP-BOX × 0):** Zurückweisung mit `QuotationError("quantity_out_of_range")`, Exit-Code 1 auf stderr.
   - **Vollprüfung:** Darüber hinaus bestehen bereits **alle 14 Kundenreferenzfälle (Q01–Q14)** und **alle 10 Fehlerfälle (E01–E10)** der Datei `fixtures/HansePack_Referenzfaelle.json`.
3. **Altprodukt Nordwerk gesichert:**
   - Commit `d140f26` auf `main` ist sauber eingefroren.
   - `test_website.py` besteht weiterhin alle 4 Prüffamilien (`F1`–`F4`), 0 Regressionen.

---

### Bereich C: Messung, Kosten & Reuse-Lernen (20 Punkte)
*Fokus: Lückenlose Traces, exklusive Zeiterfassung, Kostenkalkulation und Schwachstellenanalyse (Lernziel L6.4).*

1. **Automatisierte Analyse durch den Cost & Observability Agent (`cost_analysis.json`):**
   - Unser dedizierter Factory-Agent `src/agents/cost_agent.py` wertete die JSONL-Logs in `evidence/session-06/` aus:
     - **15 Läufe (Lars)**, 356,11 s Gesamtlaufzeit.
     - **19,42 Credits** Agentenkosten (inkl. Fehllauf HP-T6-01 mit 9,53 Credits).
   - **Zusätzlicher Gemini-Lauf HP-T6-01 (Team):** 16 Aufrufe, 92,68 s, **17,67 Credits**; Code unvollständig, verworfen und als Patch archiviert. Agentenkosten gesamt: **37,09 Credits**.
2. **Exklusive menschliche Zeiterfassung (@ 100 Credits / Person-Stunde):**
   - *Kundenlieferung (Onboarding & Briefing):* 45 Min. = 75,00 Credits.
   - *Factory-Entwicklung (Multi-Project-Registry & Tests):* 45 Min. = 75,00 Credits.
   - *Nacharbeit (Fehleranalyse Fehllauf 1 & Truncation):* 30 Min. = 50,00 Credits.
   - *Review & Freigabe:* 20 Min. = 33,33 Credits.
   - **Summe Mensch:** 140 Min. (2,33 h) = **233,33 Credits**.
3. **CI-Läufe (@ 1 Credit je CI-Lauf):**
   - 9 GitHub-Actions-Läufe = **9,00 Credits** (je 1 Credit inkl. Fehlschläge; 5 Läufe rot: `419b795`, `7179c3c`, `517fb86`, `dc7d0c1`, `92f6ee0`).
   - Ursache: 2 Backend-Agent-Tests, deren Mock `json_mode` nicht kannte; behoben in `a740db5` (CI grün).
   - Lokale `pytest`-Aufrufe sind **keine** CI-Läufe.
   - Externe Cloud-Kosten außerhalb des Kursmodells: **0,00 Credits** (Lars’ Läufe lokal; der Gemini-Lauf ist oben mit der Agentenformel erfasst).
   - **Gesamtkosten Termin 6:** **279,42 Credits** (233,33 + 19,42 + 17,67 + 9,00 + 0,00). Budget T6–T8: 779,42 Credits.
4. **Schwachstellenanalyse & Behebung:**
   - *Problem:* Lokale LLMs (`qwen3.5:9b`) brachen bei 4.096 Kontext-Tokens wegen Token-Truncation (`truncated=1`) ab, wenn große Fixtures und Prompts kombiniert wurden $\rightarrow$ unvollständige JSON-Strings.
   - *Lösung:* Anhebung auf `num_ctx=8192` in `src/llm/factory.py` und seit `a740db5` die robuste Auswertung `_parse_backend_output` in `src/agents/backend_agent.py` (erst JSON, dann ein `json`-Codeblock, dann ein `python`-Codeblock, sonst Fehler; Umlaute bleiben erhalten; 4 Tests in `tests/test_backend_agent_parsing.py`). Der frühere Fallback über `unicode_escape` wurde damit ersetzt.
5. **Kausalitäts-Transparenz:**
   - Es wird ausdrücklich **keine kausale Ersparnis gegenüber Nordwerk** behauptet, da HTML-Webseitenerstellung und deterministische kaufmännische Cent-Berechnung unvergleichbare Aufgaben sind.

---

### Bereich D: Verantwortung & Übergabe (10 Punkte)
*Fokus: Menschliche Gate-Freigabe und konsistenter Übergabe-Index.*

1. **Menschliche Verantwortung (D1):**
   - Lars Boos (als in `roles.yaml` benannter Accountable Human für QA und PM) begutachtete den Diff `90953d3..2dfb7ae` und erteilte die Freigabe (**APPROVED**).
   - Saubere Trennung: Technische Teamfreigabe liegt vor; Kundenabnahme durch den Dozenten steht an.
2. **Schnittstellen-Audit durch den Integration Agent:**
   - `src/agents/integration_agent.py` prüfte die Konsistenz der Handovers (`PO -> PM -> SA -> QA/Sec -> Gate`) und erteilte `approved`.
3. **Zusätzlicher Gemini-Lauf HP-T6-01:**
   - Gate-Eingabe im Trace versehentlich `approved`, gemeint war `changes_requested` (Notiz „Verworfen …“); offen dokumentiert, Ergebnis nicht übernommen, Kosten dennoch gezählt.
4. **Tagesübergabe (D2) in `evidence/session-06.md`:**
   - Alle Repositories, Commits, Traces und Kosten tabellarisch verknüpft.
   - Genau **drei nächste Schritte für Termin 7**:
     1. Responsive Web-Oberfläche (HTML/CSS/JS) mit Nettohinweis bauen.
     2. JSON-Export & Download implementieren.
     3. Frischen Checkout und CI-Pipeline für alle Q01–Q14 und E01–E10 aufsetzen.

---

## 3. Präsentationsleitfaden für die Dozentenabnahme

### Vorgeschlagene Demostruktur (5–7 Minuten)

1. **Einleitung (30 Sekunden):**
   - Öffne die Datei `evidence/session-06.md` im Editor.
   - Zeige die Kopfdaten: Team 3, Datum, 2 Kundenprojekte, Factory auf Branch `termin-6-hansepack`.
2. **Multi-Project-Registry & Trennung (60 Sekunden):**
   - Zeige `src/projects.py`: Erkläre, dass beide Mandanten sauber getrennt konfiguriert sind.
   - Führe den Trennungstest im Terminal aus: `python -m pytest tests/test_project_separation_t6.py` (5 passed).
   - Zeige, dass Nordwerk weiterhin 100 % grün ist: `python test_website.py` im Nordwerk-Ordner.
3. **Agentenlauf & Trace-Nachweis (90 Sekunden):**
   - Zeige den Trace `evidence/session-06/fb1d7c6b-6a79-4eab-bc00-0a1fe437daae.jsonl` mit dem Aufruf des `backend_agent` (Lauf HP-T6-REPAIR), der die erste Version `d92d39a` von `quotation.py` erzeugte.
   - Öffne den Trace `evidence/session-06/8f912c03-2c2b-42ca-82ef-304bc0c4f1b9.jsonl`: Er zeigt die Prüfung der vom Team verfeinerten Fassung `2dfb7ae` durch QA und Integration.
   - Betone, dass die Verfeinerung Team-Arbeit war und die Agenten das Ergebnis geprüft haben.
4. **Kundenprodukt HansePack live vorführen (90 Sekunden):**
   - Wechsle in das Verzeichnis `client-02-quotation`.
   - Führe die CLI-Befehle vor:
     - `python quotation.py HP-BOX 1` $\rightarrow$ 1.450 Cent.
     - `python quotation.py HP-BOX 50` $\rightarrow$ 13.075 Cent.
     - `python quotation.py HP-BOX 0` $\rightarrow$ Fehlerabbruch mit Code 1 auf stderr.
   - Führe die Produkttests aus: `python -m pytest -q` $\rightarrow$ 4 passed.
   - *Bonus für den Dozenten:* Zeige, dass der Code sogar schon alle 14 Fälle Q01–Q14 und E01–E10 fehlerfrei meistert!
5. **Kosten & Observability (60 Sekunden):**
   - Öffne `evidence/session-06/cost_analysis.json`.
   - Erkläre, dass unser eigener `cost_agent` 15 Läufe (Lars) plus 1 Gemini-Lauf ausgewertet hat.
   - Zeige die Gesamtkosten (279,42 Credits) und die Trennung von Onboarding (75 Cr) und Factory-Entwicklung (75 Cr).
6. **Abschluss & nächste Schritte (30 Sekunden):**
   - Zeige die 3 nächsten Schritte in `evidence/session-06.md`. Bitte um die formale Kundenabnahme.

---

### Live-Befehle für das Terminal (Copy & Paste bereit)

```bash
# Hinweis: Windows: .venv\Scripts\python.exe, macOS/Linux: .venv/bin/python
# ==============================================================================
# SCHRITT 1: FACTORY-KUNDENTRENNUNG PRÜFEN (Bereich A & L6.1)
# ==============================================================================
cd <Factory-Checkout>
python -m pytest tests/test_project_separation_t6.py
# Erwartung: 5 passed in ~3s

# ==============================================================================
# SCHRITT 2: NORDWERK-UNVERÄNDERTHEIT PRÜFEN (Bereich B5 & L6.1)
# ==============================================================================
cd <Nordwerk-Checkout>
python test_website.py
# Erwartung: ERGEBNIS: ALLE PRUEFFAMILIEN BESTANDEN

# ==============================================================================
# SCHRITT 3: HANSEPACK KUNDENPRODUKT CLI & TESTS PRÜFEN (Bereich B & L6.3)
# ==============================================================================
cd <client-02-quotation-Checkout>

# Q01: HP-BOX x 1 (Warenwert 250, Versand 1200, Gesamt 1450 Cent)
python quotation.py HP-BOX 1

# Q03: HP-BOX x 50 (Listenbetrag 12500, Rabatt 625, Netto 11875, Versand 1200, Gesamt 13075 Cent)
python quotation.py HP-BOX 50

# E01: HP-BOX x 0 (Ungültig, Abbruch mit Fehlercode 1)
python quotation.py HP-BOX 0

# Produkttests gegen Kundenfixtures:
python -m pytest -q
# Erwartung: 4 passed in ~0.03s

# ==============================================================================
# SCHRITT 4: COST AGENT ANALYSE ANZEIGEN (Bereich C & L6.4)
# ==============================================================================
cd <Factory-Checkout>
python -m src.agents.cost_agent --dir evidence/session-06
```

---

## 4. Antizipierte Dozentenfragen & perfekte Antworten (FAQ / Grill-Me Schutz)

### Frage 1: „Habt ihr für HansePack einfach einen zweiten Agenten kopiert oder die Nordwerk-Pfade überschrieben?“
> **Antwort:**  
> *„Nein, absolut nicht. Wir haben in `docs/TERMIN_06_MULTI_PROJECT.md` genau dokumentiert, was wiederverwendet und was angepasst wurde. Keine Agenten wurden kopiert; Pipeline-Struktur (`src/workflows/feature_pipeline.py`) und Rollen (`organization/roles.yaml`) blieben unverändert. Angepasst wurden: Projekt-Registry und Isolations-Guard (`src/projects.py`), `json_mode` in Backend-, Cost-, Integration- und QA-Agent, `num_ctx=8192` für Ollama und eine robustere JSON-Auswertung im Backend-Agent. Die Registry entkoppelt Pfade, Repos und Default-Tests je Mandant. Zusätzlich schützt ein technischer Guard (`assert_target_belongs_to_project`) davor, dass fremde Checkouts adressiert werden können, was unser Test `test_project_separation_t6.py` deterministisch beweist.“*

### Frage 2: „Berechnet euer LLM die Preise zur Laufzeit?“
> **Antwort:**  
> *„Nein. Gemäß Kundenbriefing und Bewertungsraster B1 ist das Produkt vollständig frei von LLMs und Factory-Abhängigkeiten. Die Fachlogik in `quotation.py` rechnet rein deterministisch in Python mit ganzzahligen Cents. Das LLM (`qwen3.5:9b`) kam ausschließlich in der Factory zum Einsatz: Der `backend_agent` erzeugte die erste Version (`d92d39a`), das Team verfeinerte sie (`2dfb7ae`, als Menschenarbeit gezählt), und die Agenten prüften das Ergebnis.“*

### Frage 3: „Wie habt ihr sichergestellt, dass halbe Cent kaufmännisch korrekt gerundet werden?“
> **Antwort:**  
> *„Wir haben die im Kundenbriefing empfohlene Ganzzahl-Formel `(list_amount_cents * discount_percent + 50) // 100` implementiert. Dadurch wird bei genau halbem Cent deterministisch aufgerundet (kaufmännisches Runden). Wir haben das nicht nur für Q01 und Q03 validiert, sondern gegen alle 14 Fälle der Kunden-Referenzdatei – insbesondere Q04 (1.237,5 $\rightarrow$ 1.238 Cent) und Q14 (662,5 $\rightarrow$ 663 Cent), die exakt diese Rundungsregel testen.“*

### Frage 4: „Warum ist euer erster Factory-Lauf HP-T6-01 fehlgeschlagen und wie habt ihr darauf reagiert?“
> **Antwort:**  
> *„Beim ersten Lauf hat das Modell den Katalog als Dictionary statt als Liste unter dem Schlüssel `products` interpretiert. Unser QA-Test-Engineer hat diesen Fehler sofort erkannt und das Quality-Gate blockiert. Gleichzeitig haben wir festgestellt, dass bei 4.096 Tokens Standard-Kontext die Prompt-Länge zur Token-Truncation am Modell führte. Wir haben daraufhin die Factory zentral gehärtet: `num_ctx=8192` in `factory.py` und fehlertolerantes JSON-Parsing im Backend-Agenten (seit `a740db5` ohne `unicode_escape`-Fallback, Umlaute bleiben erhalten). Im Folgelauf HP-T6-02 haben die Agenten die vom Team verfeinerte Fassung `2dfb7ae` geprüft und freigegeben. Beide Läufe – inklusive Fehllauf – sind in unserer Kostenbilanz erfasst.“*

### Frage 5: „Woher kommen die 279,42 Credits und behauptet ihr eine Ersparnis gegenüber Nordwerk?“
> **Antwort:**  
> *„Die Kosten setzen sich zusammen aus 233,33 Credits Menschenzeit (140 Min. sauber aufgeteilt in Onboarding, Factory-Entwicklung, Reparatur und Review), 37,09 Credits Agentenkosten (19,42 aus Lars' 15 Läufen, ausgewertet durch unseren Cost Agent, plus 17,67 aus dem Gemini-Lauf HP-T6-01) und 9,00 Credits CI-Läufe (9 GitHub-Actions-Läufe à 1 Credit, inklusive Fehlschlägen). Zusätzliche Cloud-Kosten außerhalb des Kursmodells fallen nicht an (0,00 Credits); der Gemini-Lauf ist bereits über die Agentenformel erfasst. Wir behaupten ausdrücklich keine kausale Ersparnis gegenüber Nordwerk, weil semantische Webseiten-Entwicklung und kaufmännische Berechnungslogik methodisch grundverschiedene Anforderungen sind.“*

### Frage 6: „Warum waren fünf CI-Läufe rot?“
> **Antwort:**  
> *„Rot waren die GitHub-Actions-Läufe zu `419b795`, `7179c3c`, `517fb86`, `dc7d0c1` und `92f6ee0`. Ursache waren 2 Backend-Agent-Tests, deren Mock `json_mode` noch nicht kannte. Behoben wurde das in `a740db5`, seither ist die CI grün. Alle 9 Termin-6-Läufe zählen je 1 Credit, auch die Fehlschläge; lokale `pytest`-Aufrufe zählen nicht als CI.“*

### Frage 7: „Warum steht beim Gemini-Lauf ‚approved‘, obwohl er verworfen wurde?“
> **Antwort:**  
> *„Im Trace `1d9fdb94-c030-47f8-a535-a4f9882c6b11` wurde am Gate versehentlich `approved` durch Mehrose Farooq eingetragen, gemeint war `changes_requested`; eine Notiz im Trace hält die Absicht fest („Verworfen …“). Der Trace wurde bewusst nicht nachträglich geändert. Der Lauf lieferte unvollständigen Code, das Ergebnis wurde nicht übernommen und nur als Patch archiviert. Die Kosten von 17,67 Credits sind trotzdem in der Bilanz enthalten.“*

---

## 5. Git-Commit-Matrix & Verzeichnisübersicht

| Komponente | Repository | Branch | Git-Commit | Status |
| :--- | :--- | :--- | :--- | :--- |
| **HansePack Produkt** | `Vanitas50/client-02-quotation` | `main` | `2dfb7ae` | ✅ Clean, alle Tests bestanden |
| **Factory (Multi-Project)** | `BohdanBerlev/agentic_ai_peppe` | `termin-6-hansepack` | `992f707` | ✅ Clean, Trennungstest 5/5, CI grün |
| **Nordwerk Basis (Freeze)** | `DavidPisark/Nordwerk-Industrie-Service-Website` | `main` | `d140f26` | ✅ Clean, 0 Änderungen, Tests grün |

**Wichtigste Dokumente:**
- Übergabe-Index & vollständige Evidenz: `evidence/session-06.md`
- Multi-Project-Architektur & Registry-Doku: `docs/TERMIN_06_MULTI_PROJECT.md`
- Kunden-Issue & Spezifikation HansePack: `issue_hp01.md` (im Repository `client-02-quotation`)
- Strukturierter Cost-Agent-Bericht: `evidence/session-06/cost_analysis.json`
